// Jack3 dashboard — vanilla JS, no external dependencies (offline-safe, no broken links).
// Features: global table-row filter, current-page nav highlight.
(function () {
  "use strict";

  // Highlight active nav link
  var path = window.location.pathname;
  document.querySelectorAll("nav.main a").forEach(function (a) {
    var href = a.getAttribute("href");
    if (!href) return;
    var full = new URL(href, window.location.href).pathname;
    if (path === full || (full !== "/" && path.indexOf(full) === 0)) {
      a.classList.add("active");
    }
  });

  // Global filter across all data tables
  var input = document.getElementById("global-filter");
  var count = document.getElementById("filter-count");
  if (input) {
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      var rows = document.querySelectorAll("table.data tbody tr");
      var shown = 0, total = 0;
      rows.forEach(function (tr) {
        total++;
        var txt = tr.textContent.toLowerCase();
        var show = q === "" || txt.indexOf(q) !== -1;
        tr.style.display = show ? "" : "none";
        if (show) shown++;
      });
      if (count) count.textContent = q === "" ? total + " rows" : shown + " / " + total + " rows";
    });
  }
})();
