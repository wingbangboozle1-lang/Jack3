
/* Filter + status chips. No dependencies, no network, no persistence. */
(function () {
  "use strict";
  function wire(input, table, chips) {
    if (!input || !table) return;
    var body = table.tBodies[0];
    if (!body) return;
    var rows = Array.prototype.slice.call(body.rows);
    var state = "all";
    function apply() {
      var q = (input.value || "").trim().toLowerCase();
      rows.forEach(function (tr) {
        var text = (tr.textContent || "").toLowerCase();
        var st = (tr.getAttribute("data-status") || "").toLowerCase();
        var okText = !q || text.indexOf(q) !== -1;
        var okState = state === "all" || st === state;
        tr.hidden = !(okText && okState);
      });
      var shown = rows.filter(function (tr) { return !tr.hidden; }).length;
      var out = document.getElementById("rowcount");
      if (out) out.textContent = shown + " of " + rows.length + " rows shown";
    }
    input.addEventListener("input", apply);
    (chips || []).forEach(function (c) {
      c.addEventListener("click", function () {
        state = c.getAttribute("data-filter") || "all";
        (chips || []).forEach(function (o) {
          o.setAttribute("aria-pressed", o === c ? "true" : "false");
        });
        apply();
      });
    });
    apply();
  }
  wire(document.getElementById("q"), document.getElementById("t"),
       Array.prototype.slice.call(document.querySelectorAll("[data-filter]")));
})();
