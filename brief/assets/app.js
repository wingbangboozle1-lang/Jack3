/* Jack3 — site interactions: nav toggle, table filtering, projection calculator */
document.addEventListener('DOMContentLoaded', function () {
  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('mainnav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () { nav.classList.toggle('open'); });
  }

  // Live table filter: any .filterbar input[data-filter-table] filters rows of target table
  document.querySelectorAll('[data-filter-table]').forEach(function (input) {
    var table = document.getElementById(input.getAttribute('data-filter-table'));
    if (!table) return;
    var type = input.tagName === 'SELECT' ? 'select' : 'text';
    var handler = function () {
      var q = (input.value || '').trim().toLowerCase();
      var rows = table.querySelectorAll('tbody tr');
      rows.forEach(function (row) {
        var text = row.innerText.toLowerCase();
        var match = !q || text.indexOf(q) !== -1;
        row.classList.toggle('hidden-row', !match);
      });
    };
    input.addEventListener('input', handler);
    input.addEventListener('change', handler);
  });

  // Projection calculator (projection-model.html)
  var form = document.getElementById('proj-form');
  if (form) {
    var $ = function (id) { return document.getElementById(id); };
    var recalc = function () {
      var rent = parseFloat($('p-rent').value) || 0;        // annual net rent, NNN
      var esc = (parseFloat($('p-esc').value) || 0) / 100;  // annual escalation
      var cap = (parseFloat($('p-cap').value) || 0) / 100;  // exit cap rate
      var years = parseInt($('p-years').value, 10) || 5;
      var ula = ($('p-ula').value || '0');                  // ula tier percent on full price
      var exitNOI = rent * Math.pow(1 + esc, years);
      var salePrice = cap > 0 ? exitNOI / cap : 0;
      var ulaTax = salePrice * (parseFloat(ula) / 100);
      var netProceeds = salePrice - ulaTax;
      // Cumulative net rent over holding period
      var cumRent = 0;
      for (var i = 0; i < years; i++) cumRent += rent * Math.pow(1 + esc, i);
      $('out-price').textContent = fmt(salePrice);
      $('out-ula').textContent = fmt(ulaTax);
      $('out-net').textContent = fmt(netProceeds);
      $('out-cumrent').textContent = fmt(cumRent);
      $('out-total').textContent = fmt(cumRent + netProceeds);
    };
    var fmt = function (n) {
      return '$' + Math.round(n).toLocaleString('en-US');
    };
    form.addEventListener('input', recalc);
    recalc();
  }
});
