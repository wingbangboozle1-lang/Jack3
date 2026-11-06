/* Jack3 — Central LA NNN Jack in the Box | dashboard interactions */
'use strict';

/* ---------- sidebar (mobile) ---------- */
(function () {
  const btn = document.getElementById('hamburger');
  const sb = document.getElementById('sidebar');
  if (!btn || !sb) return;
  btn.addEventListener('click', () => {
    const open = sb.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.addEventListener('click', (e) => {
    if (window.innerWidth <= 860 && sb.classList.contains('open') &&
        !sb.contains(e.target) && e.target !== btn) {
      sb.classList.remove('open');
    }
  });
})();

/* ---------- per-table filter ---------- */
document.querySelectorAll('input[data-filter]').forEach((input) => {
  const table = document.getElementById(input.dataset.filter);
  if (!table) return;
  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase();
    table.querySelectorAll('tbody tr').forEach((tr) => {
      tr.style.display = tr.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  });
});

/* ---------- sortable tables ---------- */
document.querySelectorAll('table.sortable thead th').forEach((th, colIdx) => {
  th.setAttribute('tabindex', '0');
  th.setAttribute('role', 'button');
  th.setAttribute('aria-label', 'Sort by ' + th.textContent.trim());
  const sort = () => {
    const table = th.closest('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const dir = th.dataset.dir === 'asc' ? 'desc' : 'asc';
    th.dataset.dir = dir;
    const num = (v) => {
      const m = String(v).replace(/[^0-9.\-]/g, '');
      return m === '' || m === '-' ? NaN : parseFloat(m);
    };
    rows.sort((a, b) => {
      const av = a.children[colIdx] ? a.children[colIdx].textContent.trim() : '';
      const bv = b.children[colIdx] ? b.children[colIdx].textContent.trim() : '';
      const an = num(av), bn = num(bv);
      let cmp;
      if (!isNaN(an) && !isNaN(bn)) cmp = an - bn;
      else cmp = av.localeCompare(bv, undefined, { numeric: true, sensitivity: 'base' });
      return dir === 'asc' ? cmp : -cmp;
    });
    rows.forEach((r) => tbody.appendChild(r));
  };
  th.addEventListener('click', sort);
  th.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); sort(); } });
});

/* ---------- projection studio (renew vs sell) ---------- */
(function () {
  const form = document.getElementById('proj-form');
  if (!form) return;

  const $ = (id) => document.getElementById(id);
  const nf = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  const pct = (x) => (x * 100).toFixed(2) + '%';

  function readInputs() {
    const v = (id) => parseFloat($(id).value);
    return {
      baseRent: v('in-base-rent'),        // current annual base rent $
      annualGrowth: v('in-growth') / 100, // annual escalation %
      yearsToExpiry: v('in-years-expiry'),// years until lease expiry
      renewalBump: v('in-renew-bump') / 100,   // rent reset at renewal %
      postRenewGrowth: v('in-post-growth') / 100, // growth after renewal
      holdYears: v('in-hold-years'),      // total years to model (incl. post-expiry)
      saleCapRate: v('in-cap-rate') / 100,      // exit cap rate for terminal value
      saleCosts: v('in-sale-costs') / 100,      // transaction costs %
      reinvestRate: v('in-reinvest') / 100,     // rate proceeds are reinvested at
      discount: v('in-discount') / 100    // PV discount rate (opportunity cost of capital)
    };
  }

  function model(inp) {
    // Scenario B (renew/hold): rent stream for holdYears, with renewal bump at expiry,
    // terminal value = forward NOI / cap rate at end of hold, net of sale costs.
    const rents = [];
    let rent = inp.baseRent;
    for (let y = 1; y <= inp.holdYears; y++) {
      if (y === Math.ceil(inp.yearsToExpiry) + 1 && inp.renewalBump !== 0) {
        rent = rent * (1 + inp.renewalBump);
      }
      rent = rent * (1 + (y <= Math.ceil(inp.yearsToExpiry) ? inp.annualGrowth : inp.postRenewGrowth));
      rents.push(rent);
    }
    const noiForward = rents[rents.length - 1] * (1 + inp.postRenewGrowth);
    const terminalGross = noiForward / inp.saleCapRate;
    const terminalNet = terminalGross * (1 - inp.saleCosts);
    let pvRents = 0;
    rents.forEach((r, i) => { pvRents += r / Math.pow(1 + inp.discount, i + 1); });
    const pvTerminal = terminalNet / Math.pow(1 + inp.discount, inp.holdYears);
    const pvHold = pvRents + pvTerminal;

    // Scenario A (sell now): net proceeds at t=0 reinvested at reinvestRate, then terminal
    // value of that reinvested lump at end of holdYears.
    const impliedTerm = Math.max(inp.yearsToExpiry - 0, 0); // info only
    void impliedTerm;
    // Price today: current NOI capitalized at exit cap rate (conservative marker).
    const salePriceNow = inp.baseRent * (1 + inp.annualGrowth) / inp.saleCapRate;
    const netNow = salePriceNow * (1 - inp.saleCosts);
    const futureValue = netNow * Math.pow(1 + inp.reinvestRate, inp.holdYears);
    const pvSell = netNow; // PV at t=0

    return { pvHold, pvSell, salePriceNow, netNow, futureValue, terminalNet, rents };
  }

  function sensitivity(inp) {
    const rows = [];
    for (const cap of [0.055, 0.06, 0.065, 0.07, 0.075, 0.08]) {
      const row = [pct(cap)];
      for (const bump of [0, 0.05, 0.10, 0.15, 0.20]) {
        const m = model(Object.assign({}, inp, { saleCapRate: cap, renewalBump: bump }));
        row.push(m.pvHold - m.pvSell);
      }
      rows.push(row);
    }
    return rows;
  }

  function render() {
    const inp = readInputs();
    if (Object.values(inp).some((x) => isNaN(x))) return;
    const m = model(inp);

    $('out-pv-hold').textContent = nf.format(m.pvHold);
    $('out-pv-sell').textContent = nf.format(m.pvSell);
    const delta = m.pvHold - m.pvSell;
    $('out-delta').textContent = (delta >= 0 ? '+' : '−') + nf.format(Math.abs(delta));
    $('out-sale-price').textContent = nf.format(m.salePriceNow);
    $('out-terminal').textContent = nf.format(m.terminalNet);
    $('out-fv-sell').textContent = nf.format(m.futureValue);

    const winHold = delta >= 0;
    $('box-hold').classList.toggle('win', winHold);
    $('box-sell').classList.toggle('win', !winHold);

    // sensitivity table
    const tbody = document.querySelector('#sens-table tbody');
    tbody.innerHTML = '';
    sensitivity(inp).forEach((row) => {
      const tr = document.createElement('tr');
      row.forEach((cell, i) => {
        const td = document.createElement('td');
        if (i === 0) { td.textContent = cell; td.style.fontWeight = '700'; }
        else {
          const v = cell;
          td.textContent = (v >= 0 ? '+' : '−') + nf.format(Math.abs(v));
          td.style.color = v >= 0 ? '#1a7f4b' : '#b3261e';
        }
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });

    // verdict line
    $('proj-verdict').textContent = winHold
      ? 'Holding/renewing shows higher present value at these assumptions. Sensitivity to cap rate and renewal bump below.'
      : 'Selling now shows higher present value at these assumptions. Sensitivity to cap rate and renewal bump below.';
  }

  form.addEventListener('input', render);
  render();
})();
