#!/usr/bin/env node
/**
 * Regression harness for the private calculator's inline arithmetic engines
 * (calculator.html: the sell-versus-hold worksheet from session 7f1087ce, plus the
 * short-lease-discount module from session 87ca5536).
 *
 * The engines are the only scripts allowed on the published site apart from the
 * master-register filter, so their arithmetic is tested line by line here against an
 * independent re-implementation of the same verified rules. The harness stubs a minimal
 * DOM — the engines perform no network or storage access by design (enforced by
 * scripts/validate.py), so a stub is sufficient and the test runs offline.
 *
 * Verified rules under test (each with its official source on the calculator page):
 *   - City base transfer tax: $2.25 per $500 or FRACTIONAL PART of the conveyed value
 *     (value rounded up to the next $500) — ULA FAQ, City of LA Office of Finance.
 *   - County documentary transfer tax: $0.55 per $500 or fractional part — LA County
 *     Registrar-Recorder.
 *   - Measure ULA: 4% above $5,400,000 and below $10,900,000; 5.5% at or above
 *     $10,900,000; percentage-based (no per-$500 rounding) — ULA FAQ.
 *   - Unrecaptured §1250 gain taxed at the owner's recapture rate (25% maximum);
 *     remaining gain at the owner's LTCG rate; NIIT 3.8% on the gain when selected;
 *     California ordinary-income treatment on the whole gain — IRS Topics 409/559, FTB.
 *   - Hold case: PV of the rent stream at the owner's escalation and discount rates,
 *     plus an optional after-tax exit run through the same rules, discounted — FRED.
 *   - Short-lease discount: implied price from NOI/cap, implied cap from an offer, and
 *     the discount per year of remaining term between the longest- and shortest-term
 *     offers — method only; no market number is invented.
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
const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (blocks.length === 0) { console.error('FAIL: no inline script found in ' + file); process.exit(1); }

// ---- minimal DOM stub -------------------------------------------------------
const els = {};
function el(id) {
  if (!els[id]) {
    els[id] = {
      id, value: '', checked: false, tagName: 'INPUT', textContent: '', innerHTML: '',
      style: {}, handlers: {},
      addEventListener(ev, fn) { this.handlers[ev] = fn; },
      appendChild() {},
    };
  }
  return els[id];
}
global.document = {
  getElementById: el,
  querySelectorAll: () => [],
  createElement: (tag) => ({ tag, textContent: '', style: {} }),
};
for (const block of blocks) { eval(block); }

// ---- helpers ----------------------------------------------------------------
function set(id, v) { el(id).value = String(v); }
function fire(id, ev) { if (el(id).handlers[ev]) el(id).handlers[ev](); }
function get(id) { return el(id).textContent; }
const M = v => (Math.round(v) < 0 ? '-' : '') + '$' + Math.abs(Math.round(v)).toLocaleString('en-US');

// ---- independent re-implementation of the verified rules --------------------
function transferTaxes(v) {
  const base = Math.ceil(v / 500) * 2.25;
  const ula = v >= 10900000 ? v * 0.055 : v > 5400000 ? v * 0.04 : 0;
  const county = Math.ceil(v / 500) * 0.55;
  return { base, ula, county };
}
function gainTaxes(gain, depr, ltcg, recapRate, ca, niit) {
  // A negative gain (sale below basis) produces no tax on this line — every portion
  // clamped at zero, matching the engine and standard single-asset arithmetic.
  const positive = Math.max(0, gain);
  const deprGain = Math.max(0, Math.min(depr, positive));
  const otherGain = positive - deprGain;
  const recap = deprGain * recapRate;
  const fed = otherGain * ltcg;
  const niitT = niit ? positive * 0.038 : 0;
  const caT = positive * ca;
  const total = recap + fed + niitT + caT;
  return { deprGain, otherGain, recap, fed, niitT, caT, total };
}
function saleCase(o) {
  const realised = o.price * (1 - o.sellcost);
  const tt = transferTaxes(o.price);
  const gain = realised - o.basis;
  const t = gainTaxes(gain, o.depr, o.ltcg, o.recap, o.ca, o.niit);
  const afterTax = realised - tt.base - tt.ula - tt.county - o.debt - t.total;
  return { realised, tt, gain, t, afterTax };
}

// ---- checks -----------------------------------------------------------------
let failures = 0;
function check(label, actual, expected) {
  const ok = String(actual) === String(expected);
  if (!ok) { failures++; }
  console.log((ok ? 'PASS' : 'FAIL') + ' | ' + label + (ok ? '' : ' | actual=' + actual + ' expected=' + expected));
}

function fillSale(o) {
  set('in-price', o.price); set('in-basis', o.basis); set('in-depr', o.depr);
  set('in-debt', o.debt); set('in-sellcost', o.sellcost * 100);
  set('in-ltcg', o.ltcg * 100); set('in-recap', o.recap * 100); set('in-ca', o.ca * 100);
  el('in-niit').checked = o.niit;
}
function fillHold(o) {
  set('in-noi', o.noi); set('in-esc', o.esc); set('in-years', o.years);
  set('in-exit', o.exit); set('in-disc', o.disc);
}
function runSale(o) { fillSale(o); fillHold({ noi: 300000, esc: 3, years: 5, exit: '', disc: 8 }); fire('calc-run', 'click'); }

// Case 1: full sale scenario (round $8,000,000 — per-$500 rounding is exact here).
const o1 = { price: 8000000, basis: 3000000, depr: 714286, debt: 0, sellcost: 0.02, ltcg: 0.20, recap: 0.25, ca: 0.093, niit: true };
runSale(o1);
const s1 = saleCase(o1);
check('base transfer tax (round price)', get('o-base'), M(s1.tt.base));
check('ULA tier 1 surcharge', get('o-ula'), M(s1.tt.ula));
check('county transfer tax (round price)', get('o-county'), M(s1.tt.county));
check('amount realised after costs', get('o-realised'), M(s1.realised));
check('capital gain', get('o-gain'), M(s1.gain));
check('§1250 portion', get('o-deprgain'), M(s1.t.deprGain));
check('recapture tax at 25%', get('o-recap'), M(s1.t.recap));
check('federal tax on remaining gain', get('o-fed'), M(s1.t.fed));
check('NIIT 3.8%', get('o-niit'), M(s1.t.niitT));
check('California tax', get('o-ca'), M(s1.t.caT));
check('after-tax proceeds', get('o-aftertax'), M(s1.afterTax));

// Case 2: per-$500 rounding on a non-divisible price ($8,000,001).
const o2 = { ...o1, price: 8000001 };
runSale(o2);
const s2 = saleCase(o2);
check('base tax rounds UP per $500', get('o-base'), M(s2.tt.base));
check('county tax rounds UP per $500', get('o-county'), M(s2.tt.county));
check('ULA stays percentage-based', get('o-ula'), M(s2.tt.ula));

// Case 3: ULA tier boundary at exactly $10,900,000 (5.5%) and just below (4%).
const o3 = { ...o1, price: 10900000 };
runSale(o3);
check('ULA tier 2 at boundary', get('o-ula'), M(transferTaxes(10900000).ula));
const o3b = { ...o1, price: 10899999 };
runSale(o3b);
check('ULA tier 1 just below boundary', get('o-ula'), M(transferTaxes(10899999).ula));

// Case 4: hold case, rent stream only (exit blank).
fillSale(o1);
fillHold({ noi: 300000, esc: 3, years: 5, exit: '', disc: 8 });
fire('calc-run', 'click');
let pv = 0;
for (let t = 1; t <= 5; t++) { pv += 300000 * Math.pow(1.03, t) / Math.pow(1.08, t); }
check('PV of rent stream (rent modelled pre-tax)', get('o-holdnoi'), M(pv));
check('hold total equals rent PV without exit', get('o-holdtotal'), M(pv));
check('exit lines cleared without exit price', get('o-exitpv'), '—');

// Case 5: hold case with an after-tax exit at year 5.
fillSale(o1);
fillHold({ noi: 300000, esc: 3, years: 5, exit: 9000000, disc: 8 });
fire('calc-run', 'click');
const exitRealised = 9000000 * 0.98;
const exitTT = transferTaxes(9000000);
const exitGain = exitRealised - 3000000;
const exitTax = gainTaxes(exitGain, 714286, 0.20, 0.25, 0.093, true);
const afterTaxExit = exitRealised - exitTT.base - exitTT.ula - exitTT.county - 0 - exitTax.total;
const pvExit = afterTaxExit / Math.pow(1.08, 5);
check('exit transfer taxes (all three)', get('o-exittax'), M(exitTT.base + exitTT.ula + exitTT.county));
check('after-tax exit proceeds', get('o-exitaftertax'), M(afterTaxExit));
check('PV of after-tax exit', get('o-exitpv'), M(pvExit));
check('hold-case total', get('o-holdtotal'), M(pv + pvExit));
check('neutral verdict wording', get('calc-verdict').includes('This is arithmetic, not a recommendation.'), true);

// Case 6: short-lease discount from entered quotes.
set('q-noi', '300000');
set('q-p0', '4800000'); set('q-t0', '4'); set('q-c0', '6.25');
set('q-p1', '5100000'); set('q-t1', '9'); set('q-c1', '');
set('q-p2', ''); set('q-t2', ''); set('q-c2', '');
fire('q-run', 'click');
const qout = el('q-out').innerHTML;
check('quote A implied by cap', qout.includes(M(300000 / 0.0625) + ' implied by the 6.25% cap'), true);
check('quote B implied cap from offer', qout.includes((300000 / 5100000 * 100).toFixed(2) + '% implied cap from the offer'), true);
check('per-year remaining-term discount', qout.includes(M((5100000 - 4800000) / 5) + ' per year of remaining term (B vs A)'), true);

// Case 7: quote module honesty on missing inputs.
set('q-noi', ''); fire('q-run', 'click');
check('missing NOI errors honestly', el('q-msg').textContent.includes('no quote is invented here'), true);
set('q-noi', '300000'); set('q-p1', ''); set('q-t1', ''); fire('q-run', 'click');
check('fewer than two quotes errors honestly', el('q-msg').textContent.includes('at least two real quotes'), true);

// Case 8: sale case with a loss — no invented positive income taxes.
const o8 = { price: 2000000, basis: 3000000, depr: 0, debt: 0, sellcost: 0, ltcg: 0.15, recap: 0.25, ca: 0.093, niit: true };
runSale(o8);
const s8 = saleCase(o8);
check('loss computed honestly', get('o-gain'), M(s8.gain));
check('zero tax on a loss', get('o-ca'), M(s8.t.caT));

console.log(failures === 0 ? 'ALL ENGINE CHECKS PASS' : failures + ' FAILURE(S)');
process.exit(failures > 0 ? 1 : 0);
