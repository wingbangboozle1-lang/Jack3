/* Jack3 site behaviour. Deliberately tiny and dependency-free.
   Three jobs: table filtering, CSV export, and nav state. */
(function () {
  "use strict";

  // ---- 1. Filter rows of a table by free text --------------------------
  function wireFilter(input, table) {
    if (!input || !table) return;
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      var rows = table.tBodies[0] ? table.tBodies[0].rows : [];
      for (var i = 0; i < rows.length; i++) {
        var txt = rows[i].textContent.toLowerCase();
        rows[i].style.display = (!q || txt.indexOf(q) !== -1) ? "" : "none";
      }
    });
  }

  // ---- 2. Export the visible rows of a table to CSV --------------------
  function csvCell(s) {
    s = (s || "").replace(/\s+/g, " ").trim();
    return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
  }

  function wireExport(btn, table, name) {
    if (!btn || !table) return;
    btn.addEventListener("click", function () {
      var lines = [];
      var i, j, row, cells, out;
      if (table.tHead && table.tHead.rows.length) {
        cells = table.tHead.rows[0].cells; out = [];
        for (j = 0; j < cells.length; j++) out.push(csvCell(cells[j].textContent));
        lines.push(out.join(","));
      }
      var rows = table.tBodies[0] ? table.tBodies[0].rows : [];
      for (i = 0; i < rows.length; i++) {
        if (rows[i].style.display === "none") continue;
        cells = rows[i].cells; out = [];
        for (j = 0; j < cells.length; j++) {
          var a = cells[j].querySelector("a[href]");
          var t = csvCell(cells[j].textContent);
          // keep the source link machine-readable in the export
          if (a && /^https?:/.test(a.getAttribute("href"))) {
            t = t + " <" + a.getAttribute("href") + ">";
          }
          out.push(t);
        }
        lines.push(out.join(","));
      }
      var blob = new Blob(["\ufeff" + lines.join("\r\n")],
                          { type: "text/csv;charset=utf-8;" });
      var url = URL.createObjectURL(blob);
      var link = document.createElement("a");
      link.href = url;
      link.download = (name || "table") + ".csv";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      setTimeout(function () { URL.revokeObjectURL(url); }, 1500);
    });
  }

  // ---- 3. Bootstrap ----------------------------------------------------
  document.addEventListener("DOMContentLoaded", function () {
    var cards = document.querySelectorAll(".table-card");
    Array.prototype.forEach.call(cards, function (card) {
      var table = card.querySelector("table");
      var input = card.querySelector("input[data-filter]");
      var btn = card.querySelector("button[data-export]");
      var name = card.getAttribute("data-table-name") || "table";
      wireFilter(input, table);
      wireExport(btn, table, name);
      if (table) {
        var n = table.tBodies[0] ? table.tBodies[0].rows.length : 0;
        var c = card.querySelector("[data-rowcount]");
        if (c) c.textContent = n;
      }
    });

    // Mark the nav entry that matches the current path.
    var here = location.pathname.split("/").pop() || "index.html";
    var links = document.querySelectorAll(".nav a");
    Array.prototype.forEach.call(links, function (a) {
      if (a.getAttribute("href") === here) a.className = "active";
    });

    // Render the timestamp of the data snapshot into any placeholder.
    var t = document.querySelectorAll("[data-snapshot]");
    Array.prototype.forEach.call(t, function (el) {
      el.textContent = el.getAttribute("data-snapshot");
    });
  });
})();
