(function () {
  var q = document.getElementById('q');
  var cat = document.getElementById('cat');
  var status = document.getElementById('status');
  var count = document.getElementById('count');
  if (!q || !cat) return;

  var table = document.querySelector('#table table');
  if (!table) return;
  var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));

  function apply() {
    var term = (q.value || '').toLowerCase().trim();
    var c = cat.value;
    var s = status.value;
    var shown = 0;
    rows.forEach(function (tr) {
      var cells = tr.querySelectorAll('td');
      var text = tr.textContent.toLowerCase();
      var rowCat = cells[1] ? cells[1].textContent.trim() : '';
      var rowStatus = tr.getAttribute('data-status') || (cells[7] ? cells[7].textContent.trim() : '');
      var okTerm = !term || text.indexOf(term) !== -1;
      var okCat = !c || rowCat === c;
      var okStatus = !s || rowStatus.toLowerCase().indexOf(s) !== -1;
      var show = okTerm && okCat && okStatus;
      tr.style.display = show ? '' : 'none';
      if (show) shown++;
    });
    if (count) count.textContent = shown + ' of ' + rows.length + ' rows';
  }

  q.addEventListener('input', apply);
  cat.addEventListener('change', apply);
  if (status) status.addEventListener('change', apply);
  apply();
})();
