#!/usr/bin/env node
/**
 * Regression harness for the private calculator's inline arithmetic engine.
 *
 * The engine (embedded in calculator.html by scripts/build_canonical.py) is the only
 * script allowed on the published site, so its arithmetic is tested line by line here
 * against an independent re-implementation of the same verified rules. The harness
 * stubs a minimal DOM — the engine performs no network or storage access by design
 * (enforced by scripts/validate.py), so a stub is sufficient and the test is offline.
 *
 * Run:  node tools/calculator_engine_test.js
 * Exit: 0 all checks pass; 1 otherwise. Requires node (any recent version).
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const candidates = [path.join(ROOT, 'calculator.html'), path.join(ROOT, '_pages_artifact', 'calculator.html')];
const file = candidates.find(p => fs.existsSync(p));
if (!file) {
  console.error('FAIL: calculator.html not found — run scripts/build_canonical.py first');
  process.exit(1);
}
const html = fs.readFileSync(file, 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error('FAIL: no inline script found in ' + file); process.exit(1); }

// ---- minimal DOM stub -------------------------------------------------------
const els = {};
function el(id) {
  if (!els[id]) {
    els[id] = {
      id, value: '', checked: false, tagName: undefined, textContent: '', innerHTML: '',
      style: {}, className: '', handlers: {},
      addEventListener(ev, fn) { this.handlers[ev] = fn; },
    };
  }
  return els[id];
}
global.document = {
  getElementById: el,
  querySelectorAll: (sel) => {
    if (!sel.includes('input')) { return []; }
    const out = [];
    for (const k of Object.keys(els)) {
      els[k].tagName = 'INPUT';
      out.push(els[k]);
    }
    return out;
  },
};
eval(m[1]);

// ---- helpers ----------------------------------------------------------------
function set(id, v) { el(id).value = String(v); }
function run(id) { el(id).handlers.click(); }
function get(id) { return el(id).textContent; }
const M = v => '$' + Math.round(v).toLocaleString('en-US');

// ---- independent re-implementation of the verified rules --------------------
// Transfer taxes: city base $2.25 per $500 or fractional part (rounded up to the next
// $500); county $0.55 per $500 (same rounding); ULA 4% above $5,400,000 and 5.5% at or
// above $10,900,000 (percentage-based, no rounding). Income taxes: unrecaptured §1250
// gain at a 25% maximum rate; remainder at the owner's LTCG rate; NIIT 3.8% on the gain
// (simplification); California ordinary-income treatment on the whole gain.
function taxes(gross, inCity, basis, depr, sellPct, fed, ca, niit) {
  const net = gross * (1 - sellPct);
  const base = inCity ? Math.ceil(gross / 500) * 2.25 : 0;
  const county = Math.ceil(gross / 500) * 0.55;
  const ula = inCity ? (gross >= 10900000 ? 0.055 * gross : gross > 5400000 ? 0.04 * gross : 0) : 0;
  const gain = net - (basis - depr);
  const pos = Math.max(gain, 0);
  const recap = 0.25 * Math.min(Math.max(depr, 0), pos);
  const fedT = fed * Math.max(gain - depr, 0);
  const niitT = niit ? 0.038 * pos : 0;
  const caT = ca * pos;
  const total = base + county + ula + recap + fedT + niitT + caT;
  return { net, base, county, ula, gain, recap, fedT, niitT, caT, total };
}

// ---- checks -----------------------------------------------------------------
let failures = 0;
function check(label, actual, expected) {
  const ok = String(actual) === String(expected);
  if (!ok) { failures++; }
  console.log((ok ? 'PASS' : 'FAIL') + ' | ' + label + (ok ? '' : ' | actual=' + actual + ' expected=' + expected));
}

// Case 1: full sale scenario, City of LA, tier 1.
set('c1_price', '8000000'); set('c1_basis', '3000000'); set('c1_depr', '714286');
set('c1_sellcost', '2'); set('c1_debt', '0'); set('c1_fedrate', '20'); set('c1_carate', '9.3');
el('c1_juris').value = 'city'; el('c1_niit').checked = true;
run('c1_go');
const t1 = taxes(8000000, true, 3000000, 714286, 0.02, 0.20, 0.093, true);
check('city base transfer tax', get('r1_base'), M(t1.base));
check('county DTT', get('r1_county'), M(t1.county));
check('ULA tier 1 amount', get('r1_ula'), M(t1.ula));
check('ULA tier 1 label', get('r1_tier'), 'Tier 1 — 4% above $5,400,000');
check('net price after costs', get('r1_net'), M(t1.net));
check('adjusted basis', get('r1_adj'), M(3000000 - 714286));
check('total gain', get('r1_gain'), M(t1.gain));
check('recapture at 25% max', get('r1_recap'), M(t1.recap));
check('federal LTCG on remainder', get('r1_fed'), M(t1.fedT) + ' at 20.0% on the non-recapture gain');
check('NIIT simplified', get('r1_niit'), M(t1.niitT) + ' (3.8% — simplified; your MAGI governs)');
check('California ordinary treatment', get('r1_ca'), M(t1.caT) + ' at 9.3% (ordinary-income treatment)');
check('total taxes and costs', get('r1_total'), M(t1.total));
check('after-tax proceeds', get('r1_proceeds'), M(t1.net - t1.total));
check('proceeds after debt payoff', get('r1_proceeds2'), M(t1.net - t1.total) + ' after debt payoff of $0');

// Case 2: ULA tier boundary at exactly $10,900,000; zero gain.
set('c1_price', '10900000'); set('c1_basis', '10900000'); set('c1_depr', '0');
set('c1_sellcost', ''); set('c1_fedrate', '0'); set('c1_carate', '0'); el('c1_niit').checked = false;
run('c1_go');
const t2 = taxes(10900000, true, 10900000, 0, 0, 0, 0, false);
check('tier 2 boundary label', get('r1_tier'), 'Tier 2 — 5.5% at or above $10,900,000');
check('tier 2 amount', get('r1_ula'), M(t2.ula));
check('zero gain', get('r1_gain'), M(t2.gain));
check('boundary proceeds', get('r1_proceeds'), M(t2.net - t2.total));

// Case 2b: below-threshold city sale.
set('c1_price', '5000000'); set('c1_basis', '5000000'); set('c1_fedrate', '0'); set('c1_carate', '0');
run('c1_go');
const t2b = taxes(5000000, true, 5000000, 0, 0, 0, 0, false);
check('no-ULA label', get('r1_tier'), 'At or below $5,400,000 — no ULA surcharge');
check('no-ULA amount', get('r1_ula'), M(t2b.ula));
check('no-ULA proceeds', get('r1_proceeds'), M(t2b.net - t2b.total));

// Case 2c: county jurisdiction — city taxes must not apply.
set('c1_price', '6000000'); set('c1_basis', '3000000'); set('c1_depr', '300000');
set('c1_fedrate', '15'); set('c1_carate', '9.3'); el('c1_niit').checked = true; set('c1_sellcost', '');
el('c1_juris').value = 'county';
run('c1_go');
const t2c = taxes(6000000, false, 3000000, 300000, 0, 0.15, 0.093, true);
check('county: base tax suppressed', get('r1_base'), 'not applied (outside the city, as entered)');
check('county: ULA suppressed', get('r1_ula'), 'not applied');
check('county: county DTT only', get('r1_county'), M(t2c.county));
check('county: proceeds', get('r1_proceeds'), M(t2c.net - t2c.total));

// Case 3: sell-now vs hold, 5-year horizon.
set('c1_price', '8000000'); set('c1_basis', '3000000'); set('c1_depr', '714286');
set('c1_sellcost', '2'); set('c1_debt', '0'); set('c1_fedrate', '20'); set('c1_carate', '9.3');
el('c1_juris').value = 'city'; el('c1_niit').checked = true; run('c1_go');
const proceedsNow = t1.net - t1.total;
set('c2_rent', '300000'); set('c2_renttax', '30'); set('c2_growth', '3'); set('c2_disc', '8');
set('c2_years', '5'); set('c2_pricegrowth', '2'); set('c2_reinvest', '6'); run('c2_go');
let pv = 0;
for (let t = 1; t <= 5; t++) { pv += 300000 * Math.pow(1.03, t) * 0.7 / Math.pow(1.08, t); }
const grossH = 8000000 * Math.pow(1.02, 5);
const tH = taxes(grossH, true, 3000000, 714286, 0.02, 0.20, 0.093, true);
const proceedsH = tH.net - tH.total;
const hold = pv + proceedsH / Math.pow(1.08, 5);
const sale = proceedsNow * Math.pow(1.06, 5);
check('hold: proceeds used', get('r2_proceeds'), M(proceedsNow));
check('hold: pv of after-tax rent', get('r2_pvrent'), M(pv));
check('hold: year-1 rent', get('r2_y1'), M(300000 * 0.7) + ' after tax in year 1');
check('hold track total', get('r2_hold'), M(hold));
check('sale track total', get('r2_sale'), M(sale) + ' at your 6.00% reinvestment rate');
check('neutral difference', get('r2_diff'),
  M(hold - sale) + ' — hold track minus sale-now track; positive means the hold path computes larger on your inputs');

// Case 4: short-lease discount from entered quotes.
set('c3_noi', '300000');
set('c3_p0', '4800000'); set('c3_t0', '4'); set('c3_c0', '6.25');
set('c3_p1', '5100000'); set('c3_t1', '9'); set('c3_c1', '');
set('c3_p2', ''); set('c3_t2', ''); set('c3_c2', '');
run('c3_go');
const r3 = el('r3_rows').innerHTML.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
check('quote A implied by cap', r3.includes(M(300000 / 0.0625) + ' implied by the 6.25% cap'), true);
check('quote B implied cap from offer', r3.includes((300000 / 5100000 * 100).toFixed(2) + '% implied cap from the offer'), true);
check('per-year remaining-term discount', r3.includes(M((5100000 - 4800000) / 5) + ' per year of remaining term (B vs A)'), true);

// Case 5: blank inputs must produce honest errors and cleared outputs.
el('calc_clear').handlers.click();
run('c1_go'); run('c2_go'); run('c3_go');
check('blank module 1 errors honestly', el('m1_msg').className.includes('bad'), true);
check('blank module 2 errors honestly', el('m2_msg').className.includes('bad'), true);
check('blank module 3 errors honestly', el('m3_msg').className.includes('bad'), true);
check('cleared proceeds output', get('r1_proceeds'), '—');

// Case 6: sale below basis — no invented positive taxes.
set('c1_price', '2000000'); set('c1_basis', '3000000'); set('c1_depr', '0');
set('c1_sellcost', '0'); set('c1_fedrate', '15'); set('c1_carate', '9.3');
el('c1_niit').checked = true; el('c1_juris').value = 'city';
run('c1_go');
const t6 = taxes(2000000, true, 3000000, 0, 0, 0.15, 0.093, true);
check('loss disclosed', get('r1_gain'), M(t6.gain) + ' (a loss — confirm treatment with your CPA)');
check('no tax on a loss', get('r1_ca'), M(t6.caT) + ' at 9.3% (ordinary-income treatment)');

console.log(failures === 0 ? 'ALL ENGINE CHECKS PASS' : failures + ' FAILURE(S)');
process.exit(failures > 0 ? 1 : 0);
