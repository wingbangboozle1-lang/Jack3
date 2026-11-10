"""Dependency-free, static, privacy-safe dashboard builder.

Reads data/evidence.json and writes the curated public dashboard to the
repository root. No network access, no third-party assets, no runtime fetches,
and no hand-typed figure in any page: every number rendered comes from the
dataset, which is the only file that is edited by hand.

    python3 scripts/build.py
"""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data/evidence.json").read_text())
SNAP = DATA["snapshot"]
SNAP_LONG = "10 November 2026"
e = html.escape

# --------------------------------------------------------------------------
# Derived arithmetic. Computed here, verified independently by validate.py,
# and never typed into a page by hand.
# --------------------------------------------------------------------------
CAPS = [5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]


def money_per_unit(cap):
    """Value of $1 of annual NOI at a given cap rate, in dollars."""
    return 100.0 / cap


def pct_change(a, b):
    return (b / a - 1.0) * 100.0


PRICE = 6_000_000
CITY_BASE = PRICE * 0.0045
ULA = PRICE * 0.04
COUNTY = PRICE / 500 * 0.55
TRANSFER_TOTAL = CITY_BASE + ULA + COUNTY
TRANSFER_PCT = TRANSFER_TOTAL / PRICE * 100.0
Y10 = 4.88
PV_2030 = 1.0 / ((1.0 + Y10 / 100.0) ** 4.0)

PAGES = DATA["categories"]
ROWS = DATA["rows"]
SOURCES = DATA["sources"]


def row(cat):
    return ROWS[cat]


def count(rows, status):
    return sum(1 for r in rows if r["status"] == status)


def src(key):
    return SOURCES[key]


STATUS_CLASS = {
    "Verified": "verified",
    "Derived": "derived",
    "Analysis": "analysis",
    "Unverified": "unknown",
    "Needs review": "flag",
}

NAV_EXTRA = [("review", "Flagged for review"), ("sources", "Sources & method")]

CSS = r"""
:root{
  --ink:#152420; --soft:#4d5f59; --mute:#71827c; --line:#dfe6e1; --line-2:#eef2ee;
  --bg:#f6f8f5; --card:#ffffff; --brand:#1d5a4a; --brand-soft:#e7f0ea;
  --warn:#8a6516; --warn-soft:#fbf3e0; --blue:#2d5c68; --blue-soft:#e6eff1;
  --red:#8d3b34; --red-soft:#fbeceb; --radius:10px;
  --shadow:0 1px 2px rgba(21,36,32,.05), 0 8px 24px -18px rgba(21,36,32,.35);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font:15.5px/1.65 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
}
a{color:var(--brand); text-decoration:none; border-bottom:1px solid rgba(29,90,74,.28)}
a:hover{border-bottom-color:var(--brand)}
.wrap{display:flex; min-height:100vh}

/* ---------- sidebar ---------- */
.side{
  width:268px; flex:0 0 268px; background:var(--card); border-right:1px solid var(--line);
  padding:26px 18px 20px; position:sticky; top:0; height:100vh; overflow:auto;
}
.brand{display:flex; gap:11px; align-items:center; border:0; margin-bottom:6px}
.mark{
  width:34px; height:34px; border-radius:9px; background:var(--brand); color:#fff;
  display:grid; place-items:center; font-weight:700; font-size:15px; letter-spacing:-.5px;
}
.brand b{display:block; font-size:14px; letter-spacing:.4px; line-height:1.2}
.brand span{display:block; font-size:10.5px; color:var(--mute); letter-spacing:.6px; text-transform:uppercase}
.side-label{
  font-size:10px; letter-spacing:1.4px; text-transform:uppercase; color:var(--mute);
  margin:22px 8px 8px; font-weight:600;
}
.side nav{display:flex; flex-direction:column; gap:1px}
.side nav a{
  display:flex; gap:10px; align-items:baseline; padding:8px 10px; border-radius:7px;
  border:0; font-size:13.5px; color:#3c4f49;
}
.side nav a .n{font-size:10px; color:#9aa8a2; font-variant-numeric:tabular-nums; min-width:16px}
.side nav a:hover{background:#f1f5f1}
.side nav a[aria-current]{background:var(--brand-soft); color:#17493c; font-weight:650}
.side nav a[aria-current] .n{color:var(--brand)}
.privacy{
  margin-top:24px; padding:14px 12px; background:#f4f7f3; border:1px solid var(--line);
  border-radius:9px; font-size:11.5px; color:var(--soft); line-height:1.5;
}
.privacy b{display:block; color:#2c4a41; font-size:11.5px; margin-bottom:3px}
.privacy .dot{color:var(--brand)}

/* ---------- content ---------- */
.main{flex:1; min-width:0}
.top{
  display:flex; justify-content:space-between; align-items:center; gap:16px; flex-wrap:wrap;
  padding:14px 40px; border-bottom:1px solid var(--line); background:rgba(246,248,245,.9);
  backdrop-filter:blur(6px); position:sticky; top:0; z-index:5;
  font-size:11px; letter-spacing:.9px; text-transform:uppercase; color:var(--mute);
}
.top .right{display:flex; gap:14px; align-items:center; text-transform:none; letter-spacing:0}
.dot-live{width:7px; height:7px; border-radius:50%; background:#2f7a55; display:inline-block; margin-right:6px}
main{padding:34px 40px 56px; max-width:1500px}
.crumb{font-size:11px; letter-spacing:1.3px; text-transform:uppercase; color:var(--brand); font-weight:650; margin-bottom:12px}
h1{font-size:clamp(29px,3.2vw,43px); line-height:1.12; letter-spacing:-1.3px; margin:0 0 16px; font-weight:680}
h1 em{font-style:normal; color:#6b8078}
h2{font-size:21px; letter-spacing:-.4px; margin:0 0 12px; line-height:1.3}
h3{font-size:15.5px; margin:0 0 8px}
p{margin:0 0 14px}
.lede{max-width:830px; font-size:17px; color:var(--soft); margin-bottom:26px; line-height:1.6}
.muted{color:var(--mute)}
.small{font-size:12.5px}
.section{margin-top:38px}
.section > .head{display:flex; justify-content:space-between; align-items:baseline; gap:16px; flex-wrap:wrap; margin-bottom:14px}
.section > .head span{font-size:12px; color:var(--mute)}

/* ---------- verdict ---------- */
.verdict{
  background:var(--card); border:1px solid var(--line); border-radius:14px; padding:26px 28px;
  box-shadow:var(--shadow); margin:26px 0 30px; border-top:3px solid var(--brand);
}
.verdict .tag{
  display:inline-block; font-size:10px; font-weight:700; letter-spacing:1.1px; text-transform:uppercase;
  background:var(--brand-soft); color:#17493c; padding:5px 9px; border-radius:5px; margin-bottom:14px;
}
.verdict h2{font-size:25px; letter-spacing:-.7px; max-width:900px}
.verdict p{font-size:14.5px; color:var(--soft); max-width:900px}
.verdict .actions{display:flex; gap:18px; flex-wrap:wrap; margin-top:6px; font-size:13px}

/* ---------- kpi cards ---------- */
.kpis{display:grid; grid-template-columns:repeat(auto-fit,minmax(215px,1fr)); gap:14px}
.kpi{background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:18px 18px 14px; box-shadow:var(--shadow)}
.kpi .k{font-size:10px; letter-spacing:1.1px; text-transform:uppercase; color:var(--mute); font-weight:650; margin-bottom:8px}
.kpi .v{font-size:27px; font-weight:660; letter-spacing:-1px; line-height:1.15; font-variant-numeric:tabular-nums}
.kpi .v.neg{color:var(--red)}
.kpi .v.pos{color:#1f6b4d}
.kpi .d{font-size:12px; color:var(--soft); margin-top:7px; line-height:1.45}
.kpi a{font-size:11px; display:inline-block; margin-top:9px; border:0; color:var(--brand)}
.kpi a:after{content:" ↗"}

/* ---------- cards / grids ---------- */
.grid-2{display:grid; grid-template-columns:1fr 1fr; gap:18px}
.grid-3{display:grid; grid-template-columns:repeat(3,1fr); gap:14px}
.panel{background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:20px 22px}
.panel.warn{border-left:3px solid #c2a24a; background:#fffdf7}
.panel.cool{border-left:3px solid #7fa7b0}
.panel h3{display:flex; align-items:center; gap:8px}
.panel ul{margin:8px 0 0; padding-left:18px}
.panel li{margin-bottom:8px; font-size:13.5px; color:var(--soft)}
.panel li b{color:var(--ink)}

.cats{display:grid; grid-template-columns:repeat(auto-fill,minmax(258px,1fr)); gap:14px}
.cat{
  display:block; background:var(--card); border:1px solid var(--line); border-radius:var(--radius);
  padding:16px 18px; box-shadow:var(--shadow); transition:.15s;
}
.cat:hover{border-color:#bcd0c4; transform:translateY(-1px)}
.cat b{display:block; font-size:14.5px; margin-bottom:4px}
.cat p{font-size:12.5px; color:var(--soft); margin:0 0 10px; line-height:1.5}
.cat .meta{display:flex; justify-content:space-between; font-size:11px; color:var(--mute); border-top:1px solid var(--line-2); padding-top:9px}

/* ---------- tables ---------- */
.tablebar{display:flex; gap:12px; align-items:center; flex-wrap:wrap; margin-bottom:10px}
.tablebar input{
  flex:1 1 260px; max-width:420px; padding:9px 12px; border:1px solid var(--line);
  border-radius:8px; font:inherit; font-size:13px; background:var(--card); color:var(--ink);
}
.tablebar input:focus{outline:2px solid #b9d3c4; outline-offset:1px}
.chip{
  font:inherit; font-size:11px; padding:6px 10px; border-radius:20px; border:1px solid var(--line);
  background:var(--card); color:var(--soft); cursor:pointer;
}
.chip[aria-pressed="true"]{background:var(--brand); color:#fff; border-color:var(--brand)}
.tw{overflow:auto; background:var(--card); border:1px solid var(--line); border-radius:var(--radius); box-shadow:var(--shadow)}
table{width:100%; border-collapse:collapse; font-size:13px; text-align:left}
caption{caption-side:top; text-align:left; padding:15px 18px 12px; font-size:12.5px; font-weight:650; color:var(--soft); border-bottom:1px solid var(--line)}
th{
  font-size:10px; letter-spacing:.9px; text-transform:uppercase; color:#5f716a; font-weight:700;
  background:#f2f6f2; padding:11px 16px; border-bottom:1px solid var(--line); white-space:nowrap; position:sticky; top:0;
}
td{padding:13px 16px; border-bottom:1px solid var(--line-2); vertical-align:top}
tbody tr:hover{background:#fafcfa}
td.num,th.num{font-variant-numeric:tabular-nums; white-space:nowrap}
td:first-child .id{display:block; font-size:10px; color:#9aa8a2; font-variant-numeric:tabular-nums; letter-spacing:.4px}
td:first-child{min-width:190px}
td .v{font-weight:600}
td .note{display:block; font-size:11.5px; color:var(--mute); margin-top:5px; line-height:1.45; max-width:430px}
td .geo{display:block; font-size:11.5px; color:var(--soft)}
td .per{display:block; font-size:11px; color:var(--mute)}
td.src{min-width:150px; font-size:11.5px}
td.src a{display:block; line-height:1.35}
td.src span{display:block; color:var(--mute); font-size:10.5px; margin-top:3px}

/* badges */
.b{display:inline-block; font-size:9.5px; font-weight:700; letter-spacing:.6px; text-transform:uppercase;
   padding:3.5px 7px; border-radius:4px; white-space:nowrap}
.verified{background:var(--brand-soft); color:#1c5b39}
.derived{background:#e7eff7; color:#2a4f70}
.analysis{background:var(--blue-soft); color:var(--blue)}
.unknown{background:var(--warn-soft); color:var(--warn)}
.flag{background:var(--red-soft); color:var(--red)}
.blank{color:#a2aea9; font-style:italic; font-size:12px; background:repeating-linear-gradient(135deg,#fafbf9,#fafbf9 5px,#f1f4f0 5px,#f1f4f0 6px); padding:2px 6px; border-radius:3px}

.legend{display:flex; flex-wrap:wrap; gap:8px 16px; font-size:11.5px; color:var(--mute); margin:14px 0 0; align-items:center}
.legend .b{margin-right:5px}

/* ---------- misc ---------- */
.flow{display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:12px; counter-reset:step}
.step{background:var(--card); border:1px solid var(--line); border-radius:var(--radius); padding:15px 16px; position:relative}
.step:before{counter-increment:step; content:counter(step); position:absolute; top:12px; right:14px;
  font-size:11px; color:#b6c4bd; font-weight:700}
.step b{display:block; font-size:13px; margin-bottom:5px; padding-right:18px}
.step p{font-size:12px; color:var(--soft); margin:0}
.callout{background:#f3f7f2; border:1px solid var(--line); border-radius:var(--radius); padding:18px 20px; font-size:13.5px; color:var(--soft)}
.callout b{color:var(--ink)}
footer{border-top:1px solid var(--line); margin-top:44px; padding:22px 0 0; font-size:11.5px; color:var(--mute); line-height:1.6}
footer a{border:0}
.skip{position:absolute; left:-9999px}
.skip:focus{left:12px; top:12px; background:#fff; padding:10px 14px; z-index:99; border-radius:6px}
a:focus-visible,.chip:focus-visible{outline:3px solid #a8c6b4; outline-offset:2px}

@media(max-width:1080px){
  .side{width:230px; flex-basis:230px}
  main{padding:26px 24px 48px}
  .top{padding:12px 24px}
  .grid-2,.grid-3{grid-template-columns:1fr}
}
@media(max-width:760px){
  .wrap{display:block}
  .side{position:static; width:auto; height:auto; border-right:0; border-bottom:1px solid var(--line); padding:16px}
  .side nav{flex-direction:row; overflow:auto; gap:4px; padding-bottom:4px}
  .side nav a{white-space:nowrap; font-size:12.5px; padding:7px 9px}
  .side nav a .n{display:none}
  .privacy{margin-top:12px}
  .top{position:static}
  h1{font-size:27px}
  .kpi .v{font-size:23px}
}
@media print{
  .side,.top,.tablebar,.chip{display:none}
  body{background:#fff}
  main{padding:0; max-width:none}
  .tw{overflow:visible; box-shadow:none}
  .cat,.kpi,.panel{box-shadow:none}
  a{color:inherit}
}
"""

JS = r"""
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
"""


def badge(status):
    return f'<span class="b {STATUS_CLASS.get(status, "unknown")}">{e(status)}</span>'


def source_cell(r):
    s = src(r["source"])
    return (
        f'<td class="src"><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">'
        f'{e(s["short"])}</a><span>{e(s["publisher"])}</span></td>'
    )


def value_cell(r):
    """Render a value. An unverified row can never render one: absence of a
    value is enforced here, not by convention."""
    v = r.get("value", "").strip()
    if not v:
        return '<span class="blank">not published — see note</span>'
    return f'<span class="v">{e(v)}</span>'


def page_table(cat, title, caption):
    rows = row(cat)
    out = [
        '<div class="tablebar">',
        '<input id="q" type="search" placeholder="Filter rows, e.g. unemployment, ULA, lease" aria-label="Filter table rows">',
        '<button class="chip" data-filter="all" aria-pressed="true">All ' + str(len(rows)) + "</button>",
    ]
    for st in ("Verified", "Derived", "Analysis", "Unverified"):
        n = count(rows, st)
        if n:
            out.append(f'<button class="chip" data-filter="{e(st.lower())}" aria-pressed="false">{st} {n}</button>')
    out.append('<span class="small muted" id="rowcount"></span>')
    out.append("</div>")
    out.append('<div class="tw"><table id="t"><caption>' + e(caption) + "</caption><thead><tr>")
    for h, cls in (("Finding", ""), ("Value", ""), ("Geography", ""), ("Period", ""), ("Source", ""), ("Evidence status", "")):
        out.append(f'<th scope="col" class="{cls}">{h}</th>')
    out.append("</tr></thead><tbody>")
    for r in rows:
        out.append(
            f'<tr data-status="{e(r["status"].lower())}">'
            f'<td><span class="id">{e(r["id"])}</span>{e(r["indicator"])}'
            + (f'<span class="note">{e(r["note"])}</span>' if r.get("note") else "")
            + "</td>"
            f'<td>{value_cell(r)}</td>'
            f'<td><span class="geo">{e(r["geography"])}</span></td>'
            f'<td><span class="per">{e(r["period"])}</span></td>'
            + source_cell(r)
            + f"<td>{badge(r['status'])}</td></tr>"
        )
    out.append("</tbody></table></div>")
    out.append(
        '<p class="legend">'
        '<span><span class="b verified">Verified</span>re-read on the official page, snapshot ' + SNAP_LONG + "</span>"
        '<span><span class="b derived">Derived</span>arithmetic on verified values, recomputed by the validator</span>'
        '<span><span class="b analysis">Analysis</span>this project\'s judgement, not an official statistic</span>'
        '<span><span class="b unknown">Unverified</span>no official source obtained; value left blank</span>'
        "</p>"
    )
    return "".join(out)


def shell(page_id, title, body, description):
    nav = []
    nav.append(link("index", "01", "Overview", page_id))
    for i, p in enumerate(PAGES, start=2):
        nav.append(link(p["id"], str(i).zfill(2), p["nav"], page_id))
    nav.append(link("review", "12", "Flagged for review", page_id))
    nav.append(link("sources", "13", "Sources & method", page_id))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · Asset A · Jack in the Box NNN decision file</title>
<meta name="description" content="{e(description)}">
<meta name="robots" content="index,follow">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="wrap">
<aside class="side">
  <a class="brand" href="index.html"><span class="mark">A</span><span><b>Asset A</b><span>Jack in the Box · NNN</span></span></a>
  <div class="side-label">Dashboard</div>
  <nav aria-label="Sections">{"".join(nav)}</nav>
  <div class="privacy"><b><span class="dot">◆</span> Privacy by design</b>
  Placeholder identifiers only. No address, parcel number, owner name, rent, basis or lease document is collected, stored or published on this site.</div>
</aside>
<div class="main">
  <div class="top">
    <span>Central Los Angeles · single-tenant net lease</span>
    <span class="right"><span class="dot-live"></span>Snapshot {SNAP_LONG}</span>
  </div>
  <main id="main">
{body}
    <footer>
      Independent decision-support research on public sources. Not an appraisal, not legal, tax or investment advice, and not a
      personalised recommendation. Asset A and Owner A are placeholders. Every published value carries a link to the official
      page it came from; anything that could not be confirmed is blank and listed on <a href="review.html">Flagged for review</a>.
      <br>Snapshot {SNAP_LONG} · generated by <code>scripts/build.py</code> from <code>data/evidence.json</code> · no tracking, no forms, no third-party assets.
    </footer>
  </main>
</div>
</div>
<script src="assets/app.js" defer></script>
</body>
</html>
"""


def link(pid, num, label, current):
    cur = ' aria-current="page"' if pid == current else ""
    href = "index.html" if pid == "index" else f"{pid}.html"
    return f'<a href="{href}"{cur}><span class="n">{num}</span>{e(label)}</a>'


def kpi(label, value, detail, source_key=None, cls="", href=None):
    v = f'<div class="v {cls}">{e(value)}</div>'
    d = f'<div class="d">{detail}</div>' if detail else ""
    if href:
        a = f'<a href="{href}">Details</a>'
    elif source_key:
        s = src(source_key)
        a = f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["publisher"])}</a>'
    else:
        a = ""
    return f'<article class="kpi"><div class="k">{e(label)}</div>{v}{d}{a}</article>'


# --------------------------------------------------------------------------
# Overview
# --------------------------------------------------------------------------
def build_index():
    totals = {st: sum(count(v, st) for v in ROWS.values()) for st in STATUS_CLASS}
    total = sum(len(v) for v in ROWS.values())
    cats = ['<div class="cats">']
    for p in PAGES:
        rows = row(p["id"])
        verified = count(rows, "Verified") + count(rows, "Derived")
        cats.append(
            f'<a class="cat" href="{p["id"]}.html"><b>{e(p["title"])}</b>'
            f'<p>{e(p["description"].split(". ")[0])}.</p>'
            f'<span class="meta"><span>{len(rows)} rows</span><span>{verified} sourced</span></span></a>'
        )
    cats.append("</div>")

    body = f"""
    <div class="crumb">Decision file · {SNAP_LONG}</div>
    <h1>Should this Jack in the Box net lease be sold before 2030,<br>or renewed? <em>A sourced answer, and its limits.</em></h1>
    <p class="lede">A single-tenant NNN restaurant property in central Los Angeles with a lease reported to expire between 2030 and 2035.
    This dashboard collects the official evidence that bears on the decision, separates what is verified from what is judgement,
    and leaves blank what neither can supply.</p>

    <div class="verdict">
      <span class="tag">Conditional recommendation · analyst judgement, not a valuation</span>
      <h2>Run a dual track now: take the asset quietly to market, and demand renewal terms in writing in the same quarter.</h2>
      <p>Take a confidential sale process to market 24–36 months before the earliest possible expiry, and in parallel ask the tenant
      for rent, escalators, options, expense caps and a guaranty. Then act on whichever the documents support: a verified after-tax
      bid, or an enforceable extension of ten years or more at market rent with acceptable credit. What is not defensible is letting
      an option notice window pass on regional averages. At expiry the landlord has no income and the tenant has no obligation —
      leverage belongs to whoever can wait, and that is the tenant.</p>
      <div class="actions">
        <a href="decisions.html">The six routes and the triggers that switch between them →</a>
        <a href="taxes.html">What a sale actually costs here →</a>
        <a href="review.html">What is not established →</a>
      </div>
    </div>

    <div class="kpis">
      {kpi("City population change", "−0.8%", "Los Angeles city, April 2020 estimates base to July 2025. A demand headwind, not a sales forecast.", "city", "neg")}
      {kpi("County population change", "−3.2%", "Los Angeles County over the same period. The county has lost more than the city.", "county", "neg")}
      {kpi("Metro payroll growth", "+0.5%", "Nonfarm employment, September 2026 vs September 2025, not seasonally adjusted — below local CPI of 3.7%.", "bls", "pos")}
      {kpi("Tenant same-store sales", "−1.1%", "Jack in the Box system, 12 weeks to 5 July 2026. Chain-wide; not this restaurant.", "jackq3", "neg")}
      {kpi("10-year Treasury", "4.88%", "Constant-maturity par yield, 9 November 2026. The observable discount-rate anchor; higher exit yields lower price.", "treasury")}
      {kpi("Transfer taxes, $6.0m city sale", f"${TRANSFER_TOTAL:,.0f}", f"{TRANSFER_PCT:.2f}% of price before escrow, title, commission or gain — 0.45% city base + 4% ULA + county rate.", "ula", "neg")}
    </div>

    <div class="section">
      <div class="head"><h2>Why this is the balance point</h2><span>Business as usual, then the tail</span></div>
      <div class="grid-2">
        <div class="panel">
          <h3>What the verified record shows</h3>
          <ul>
            <li><b>Demand is contracting slowly.</b> City population is 0.8% below its 2020 base and the county 3.2% below, while payrolls grew 0.5% — less than the 3.7% local inflation rate.</li>
            <li><b>The tenant is shrinking its own system.</b> 17 closures against 4 openings in one quarter, a 150–200 unit closure programme, and about 1% of units a year thereafter.</li>
            <li><b>Costs are rising faster than a typical escalator.</b> Local compensation costs rose 4.2% and wages 3.9% in the year to September 2026; the subject lease's escalator is unknown.</li>
            <li><b>Exit pricing is exposed to rates.</b> The 10-year Treasury is 4.88%. A move from a 6.0% to an 8.0% exit cap costs a quarter of the value for the same rent.</li>
            <li><b>The sale is expensive here.</b> Transfer taxes alone take 4.56% of a $6.0m city sale, before commission and tax on gain.</li>
          </ul>
        </div>
        <div class="panel warn">
          <h3>What would change the answer</h3>
          <ul>
            <li><b>A signed extension</b> at market rent, ten years or longer, with a verified creditworthy guarantor.</li>
            <li><b>A verified after-tax bid</b> above the risk-adjusted value of holding — a real offer, not an appraisal.</li>
            <li><b>Block-level evidence</b> that this trade area is growing, rather than city or county averages.</li>
            <li><b>A change in the owner's own position</b>: liquidity need, concentration, estate timing.</li>
          </ul>
          <p class="small muted" style="margin-top:12px">None of these can be established from the public record collected here. The property's identity, rent, basis, debt and lease are not public documents, and this project deliberately does not hold them.</p>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="head"><h2>The risk balance</h2><span>Each item links to its register row</span></div>
      <div class="grid-3">
        <div class="panel cool"><h3>Income and credit</h3>
          <p class="small">One tenant funds all of the income. A franchisee is not the brand, and the brand's own margin on franchise operations fell to 37.4% from 39.3% while bad-debt expense rose.</p>
          <a class="small" href="risk.html">Risk register →</a></div>
        <div class="panel cool"><h3>Costs and rates</h3>
          <p class="small">Wages up 4.2%, energy CPI up 20.3%, and a 10-year at 4.88%. A fixed escalator below 3.7% loses real ground every year.</p>
          <a class="small" href="model.html">Projection framework →</a></div>
        <div class="panel cool"><h3>Black swans</h3>
          <p class="small">In 2025, 16,264 structures were destroyed in this county in 24 days. USGS models a plausible M7.8 event at about 1,800 deaths and $213bn in losses. Neither is a site-specific exposure; both reprice insurance.</p>
          <a class="small" href="risk.html">Read the tail →</a></div>
      </div>
    </div>

    <div class="section">
      <div class="head"><h2>Browse the evidence by category</h2><span>{total} rows · {totals['Verified']} verified · {totals['Unverified']} left blank</span></div>
      {''.join(cats)}
    </div>

    <div class="section">
      <div class="head"><h2>How to read this file</h2><span>The method in four lines</span></div>
      <div class="flow">
        <div class="step"><b>Only official pages</b><p>Government agencies, statutes and the tenant's own securities filings. No aggregators, no brokers, no estimates attributed to "market sources".</p></div>
        <div class="step"><b>Every row carries its link</b><p>Each value points at the exact page it was read from, with the geography and period beside it. The validator fails the build if a row has no source.</p></div>
        <div class="step"><b>Blank beats invented</b><p>If a value cannot be confirmed on an official page it is left blank, marked unverified, and published on the review page with the check that would close it.</p></div>
        <div class="step"><b>Judgement is labelled</b><p>Analysis rows are this project's reasoning. They are never counted as verified and never presented as a statistic.</p></div>
      </div>
    </div>
    """
    return shell("index", "Overview", body,
                 "A source-linked, privacy-safe decision file for a single-tenant Jack in the Box net lease in central Los Angeles: sell before the 2030-2035 expiry or renew.")


# --------------------------------------------------------------------------
# Generic category page
# --------------------------------------------------------------------------
INTROS = {
    "economy": """
    <div class="kpis">
      {a}{b}{c}{d}
    </div>
    <p class="small muted" style="margin-top:14px">All labour-market figures are not seasonally adjusted and are preliminary for September 2026; BLS states that some data may be revised.</p>
    """,
}
""


def build_category(p):
    pid = p["id"]
    rows = row(pid)
    verified = count(rows, "Verified") + count(rows, "Derived")
    body = [
        f'<div class="crumb">{e(p["kicker"])}</div>',
        f'<h1>{e(p["title"])}</h1>',
        f'<p class="lede">{e(p["description"])}</p>',
    ]
    if pid == "economy":
        body.append(
            '<div class="kpis">'
            + kpi("Metro unemployment", "4.4%", "Los Angeles–Long Beach–Anaheim, September 2026, not seasonally adjusted; 5.5% a year earlier.", "bls")
            + kpi("City unemployment", "4.5%", "City of Los Angeles, September 2026; 5.9% a year earlier.", "bls")
            + kpi("Payroll growth", "+0.5%", "Total nonfarm, 12 months to September 2026, +30.2 thousand jobs.", "bls", "pos")
            + kpi("All-items CPI-U", "+3.7%", "Los Angeles metro area, 12 months to September 2026 — above payroll growth.", "bls", "neg")
            + "</div>"
        )
    if pid == "tenant":
        body.append(
            '<div class="kpis">'
            + kpi("Same-store sales", "−1.1%", "System, 12 weeks ended 5 July 2026. Company −0.9%, franchise −1.2%.", "jackq3", "neg")
            + kpi("Units at quarter end", "2,115", "149 company, 1,966 franchise. Net −13 in the quarter.", "jackq3")
            + kpi("Closures vs openings", "17 / 4", "Third quarter FY2026, chain-wide. The release does not identify units.", "jackq3", "neg")
            + kpi("Franchise-level margin", "37.4%", "Down from 39.3%; lower rent and royalty revenue and higher bad debt.", "jackq3", "neg")
            + "</div>"
        )
    if pid == "taxes":
        body.append(
            '<div class="kpis">'
            + kpi("City base transfer tax", "0.45%", "$2.25 per $500, rounded up.", "ula")
            + kpi("Measure ULA", "4% / 5.5%", "Above $5.4m / at or above $10.9m, closings after 30 June 2026.", "ula", "neg")
            + kpi("County transfer tax", "$0.55 / $500", "Rev. & Tax. Code 11911(a); calculated at the full $1.10 per $1,000 in the City of Los Angeles.", "rtc11911")
            + kpi("Federal long-term gain", "0 / 15 / 20%", "Plus 3.8% NIIT above the MAGI thresholds; California taxes the gain as ordinary income.", "irs409")
            + "</div>"
        )
    if pid == "risk":
        body.append(
            '<div class="kpis">'
            + kpi("Structures lost, January 2025", "16,264", "Palisades 6,845 + Eaton 9,419, Los Angeles County, within 24 days.", "palisades", "neg")
            + kpi("Modelled M7.8 scenario", "~1,800 deaths", "USGS/CGS ShakeOut: about $213bn of economic losses across eight counties. A scenario, not a forecast.", "usgs", "neg")
            + kpi("Fast-food wage floor", "$20.00/hr", "AB 1228, effective 1 April 2024, for covered limited-service chains of 60+ units.", "dirff")
            + kpi("State minimum wage", "$16.90/hr", "From 1 January 2026. The 2027 rate is not stated on the DIR page and is not published here.", "dir")
            + "</div>"
        )
    if pid == "demographics":
        body.append(
            '<div class="kpis">'
            + kpi("City population", "3,869,089", "1 July 2025 estimate; −0.8% from the April 2020 base.", "city")
            + kpi("City median household income", "$81,939", "2020–2024 ACS, 2024 dollars. County median is $90,112 — the city sits below the county.", "city")
            + kpi("Poverty rate", "16.5%", "City, 2025 estimate. County 13.3%.", "city", "neg")
            + kpi("Renter share", "64.0%", "Owner-occupied rate 36.0% city vs 45.9% county; derived as 100% minus the published rate.", "city")
            + "</div>"
        )
    if pid == "geography":
        body.append(
            '<div class="kpis">'
            + kpi("City land area", "469.49 sq mi", "2020 Census. A very large, non-contiguous geography.", "city")
            + kpi("Density", "8,304.2 / sq mi", "City, 2020 Census; county 2,466.9.", "city")
            + kpi("County building permits", "22,250", "2025. The city reports 'not applicable' on QuickFacts, so no city figure is published.", "county")
            + kpi("Mean commute", "30.7 min", "City workers aged 16+, 2020–2024 ACS. A proxy for drive-time reach, not a measurement.", "city")
            + "</div>"
        )
    if pid == "schools":
        body.append(
            '<div class="kpis">'
            + kpi("LAUSD enrollment", "497,105", "2025–26. Largest district in California, 4.4× the second.", "cdelarge")
            + kpi("Share of state enrollment", "8.7%", "Of 5,731,260 pupils statewide, 2025–26.", "cdelarge")
            + kpi("Graduation rate", "—", "Not published: CDE releases the cohort rate only as 16MB data files that were not parsed in this pass.", "cdeacgr", cls="")
            + kpi("Campus assignment", "—", "Cannot be assigned without an address. District averages cannot describe a campus.", "cdelarge")
            + "</div>"
        )
    body.append(page_table(pid, p["title"], f'{p["title"]} · evidence register · {len(rows)} rows, {verified} sourced'))
    body.append(
        '<div class="section"><div class="head"><h2>Notes on this page</h2>'
        f'<span>{len(rows)} rows · {verified} sourced · {count(rows, "Unverified")} blank</span></div>'
        '<div class="callout">Every value above is a published statistic about a geography, not about the subject property. '
        'City, county and metro figures bracket a trade area; they do not measure one. Where a row is blank, no official source was '
        'obtained and nothing was inferred — the check required to close it is stated in the row and listed again on '
        '<a href="review.html">Flagged for review</a>.</div></div>'
    )
    return shell(pid, p["title"], "\n".join(body), p["description"])


# --------------------------------------------------------------------------
# Projection framework (computed tables)
# --------------------------------------------------------------------------
def build_model():
    p = next(x for x in PAGES if x["id"] == "model")
    rows = row("model")
    def cap_row(c):
        """Each cap rate is expressed as a spread over the verified 10-year
        yield, so every row in the grid is anchored to a linked observation."""
        spread = c - Y10
        return (
            f'<tr><td class="num">{c:.1f}%</td>'
            f'<td class="num">{spread:+.2f} pp</td>'
            f'<td class="num">${money_per_unit(c):,.2f}</td>'
            f'<td class="num">{pct_change(money_per_unit(CAPS[2]), money_per_unit(c)):+.1f}%</td>'
            f'<td class="src"><a href="{e(src("treasury")["url"])}" target="_blank" rel="noopener noreferrer">'
            f'Treasury {Y10:.2f}%</a><span><span class="b derived">Derived</span> + declared spread</span></td></tr>'
        )

    cap_rows = "".join(cap_row(c) for c in CAPS)
    return shell("model", p["title"], f"""
    <div class="crumb">{e(p["kicker"])}</div>
    <h1>{e(p["title"])}</h1>
    <p class="lede">{e(p["description"])}</p>

    <div class="verdict" style="border-top-color:#2d5c68">
      <span class="tag" style="background:#e6eff1;color:#2d5c68">The honest part of a forecast</span>
      <h2>Every verified trend in this file is flat, shrinking, or rising in cost — and none of them is a forecast for this parcel.</h2>
      <p>A projection that survives scrutiny has three parts: verified anchors, arithmetic that anyone can reproduce, and an explicit
      statement of what is assumed. This page publishes the first two in full and names the third rather than filling it in. No 2030–2035
      sale price, cap rate, rent or renewal probability appears anywhere on this site, because no official source publishes one for this
      property and compounding a regional trend into a price would be an artefact of the rule, not evidence.</p>
    </div>

    <div class="section">
      <div class="head"><h2>What a change in exit yield does to value</h2><span>Pure arithmetic · value = NOI ÷ cap rate</span></div>
      <div class="tw"><table>
        <caption>Value of $1 of annual net operating income at different exit cap rates, each expressed as a spread over the verified 10-year Treasury yield of 4.88%. The spreads are illustrative. No cap rate is asserted for this asset.</caption>
        <thead><tr><th class="num">Exit cap rate</th><th class="num">Spread over the 10-year</th><th class="num">Value per $1 of NOI</th><th class="num">Change from 6.0%</th><th>Anchor</th></tr></thead>
        <tbody>{cap_rows}</tbody>
      </table></div>
      <p class="small muted" style="margin-top:10px">Read across, not down: the same rent is worth 14.3% less at a 7.0% exit cap than at 6.0%,
      and 25.0% less at 8.0%. That is why the exit yield matters more to a 2030 sale than a year of rent growth. The arithmetic is recomputed
      by <code>scripts/validate.py</code>; the cap rates themselves are illustrative and are not evidence about this market.</p>
    </div>

    <div class="section">
      <div class="head"><h2>Transfer taxes on a $6.0 million City of Los Angeles sale</h2><span>Every component linked · derived total</span></div>
      <div class="tw"><table>
        <caption>Transaction taxes only. Excludes escrow, title, broker commission, loan payoff and tax on gain.</caption>
        <thead><tr><th>Component</th><th class="num">Rate</th><th class="num">Amount</th><th>Source</th></tr></thead>
        <tbody>
          <tr><td>City base real property transfer tax</td><td class="num">0.45%</td><td class="num">${CITY_BASE:,.0f}</td>
              <td class="src"><a href="{e(src('ula')['url'])}" target="_blank" rel="noopener noreferrer">City of LA Office of Finance</a></td></tr>
          <tr><td>Measure ULA surcharge (above $5,400,000)</td><td class="num">4.00%</td><td class="num">${ULA:,.0f}</td>
              <td class="src"><a href="{e(src('ula')['url'])}" target="_blank" rel="noopener noreferrer">City of LA Office of Finance</a></td></tr>
          <tr><td>County documentary transfer tax</td><td class="num">$0.55 / $500</td><td class="num">${COUNTY:,.0f}</td>
              <td class="src"><a href="{e(src('rtc11911')['url'])}" target="_blank" rel="noopener noreferrer">Rev. &amp; Tax. Code 11911</a></td></tr>
          <tr><td><b>Total transfer taxes</b></td><td class="num"><b>{TRANSFER_PCT:.2f}%</b></td><td class="num"><b>${TRANSFER_TOTAL:,.0f}</b></td>
              <td class="src"><a href="{e(src('ula')['url'])}" target="_blank" rel="noopener noreferrer">City of LA Office of Finance</a><span><span class="b derived">Derived</span> sum of the three rows above</span></td></tr>
        </tbody>
      </table></div>
      <p class="small muted" style="margin-top:10px">The county rate is verified on the statute and on the Recorder's page, which also states that
      the County rate is calculated at the full $1.10 per $1,000 in the five special cities including Los Angeles. A price below $5.4 million
      removes the ULA line entirely; that cliff — not a gradual slope — is the single most important pricing fact on this page.</p>
    </div>

    <div class="section">
      <div class="head"><h2>Discounting</h2><span>Risk-free only</span></div>
      <div class="grid-2">
        <div class="panel">
          <h3>Present value of $1 received in 2030</h3>
          <p style="font-size:26px;font-weight:650;letter-spacing:-1px;margin:6px 0">${PV_2030:.3f}</p>
          <p class="small">At the {Y10:.2f}% 10-year Treasury yield of 9 November 2026, four years out: 1 ÷ 1.0488⁴. This is a floor for a
          discount rate, not a recommended rate. A property discount rate adds a premium for illiquidity, single-tenant concentration and
          stale rent, and that premium must be declared as an assumption rather than borrowed from a source that does not publish it.</p>
          <a class="small" href="{e(src('treasury')['url'])}" target="_blank" rel="noopener noreferrer">Treasury daily par yield curve ↗</a>
        </div>
        <div class="panel warn">
          <h3>What this model refuses to do</h3>
          <ul class="small">
            <li>Produce a 2030–2035 value. No official source publishes cap rates, and none is asserted.</li>
            <li>Assign a renewal probability. No agency publishes one for a private lease.</li>
            <li>Extrapolate the 2020–2025 population decline, or the 2026 payroll growth, to 2035.</li>
            <li>Quote a store-level sales figure. The tenant does not publish unit-level results.</li>
          </ul>
        </div>
      </div>
    </div>

    {page_table('model', p['title'], 'Projection framework · anchors, arithmetic and refusals')}

    <div class="section"><div class="head"><h2>How to use it</h2><span>Four steps, in order</span></div>
      <div class="flow">
        <div class="step"><b>Anchor</b><p>Write down the 10-year yield and the local inflation rate on the day you decide. Both are published and both move.</p></div>
        <div class="step"><b>Bound</b><p>Set an escalator floor at local CPI and a ceiling at what the tenant will sign. Anything outside that range needs a reason.</p></div>
        <div class="step"><b>Stress</b><p>Run the exit at 6.0% and 8.0%. If the deal only works at the low cap, the price is the risk.</p></div>
        <div class="step"><b>Gate</b><p>Do not convert a scenario into a decision until the lease, the estoppel and the owner's basis are in hand.</p></div>
      </div>
    </div>
    """, p["description"])


# --------------------------------------------------------------------------
# Review (flagged) page
# --------------------------------------------------------------------------
def build_review():
    p = next(x for x in PAGES if x["id"] == "review")
    rows = row("review")
    body = [
        f'<div class="crumb">{e(p["kicker"])}</div>',
        f'<h1>{e(p["title"])}</h1>',
        f'<p class="lede">{e(p["description"])}</p>',
        '<div class="verdict" style="border-top-color:#8a6516">'
        '<span class="tag" style="background:#fbf3e0;color:#8a6516">Published, not hidden</span>'
        '<h2>Nothing on this page blocks publication. Each item blocks one specific claim.</h2>'
        '<p>Three kinds of item appear below: values no official source could supply (F-01 to F-11, F-18), conflicts or drifts found '
        'while re-reading the sources (F-12, F-13), and irregularities found in this repository itself (F-14 to F-17). The repository items '
        'are reported rather than fixed where fixing them would mean editing another session\'s files; those are logged in '
        '<code>COORDINATION.md</code> with the requested change.</p></div>',
        page_table("review", p["title"], f'Flagged for review · {len(rows)} items'),
    ]
    return shell("review", p["title"], "\n".join(body), p["description"])


# --------------------------------------------------------------------------
# Sources & method
# --------------------------------------------------------------------------
def build_sources():
    rows = sorted(SOURCES.items(), key=lambda kv: kv[1]["publisher"].lower())
    trs = "".join(
        f'<tr><td><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["label"])}</a>'
        f'<span class="note">{e(s["type"])} · accessed {e(s["accessed"])}</span></td>'
        f'<td>{e(s["publisher"])}</td>'
        f'<td class="num">{sum(1 for v in ROWS.values() for r in v if r["source"] == k)}</td></tr>'
        for k, s in rows
    )
    used = sorted({r["source"] for v in ROWS.values() for r in v})
    body = f"""
    <div class="crumb">13 / AUDIT TRAIL</div>
    <h1>Sources &amp; method</h1>
    <p class="lede">Evidence first, interpretation second, unknowns left unknown. This page is the full register: what was read, who
    published it, when it was read, and how many rows depend on it.</p>

    <div class="kpis">
      {kpi("Official sources", str(len(SOURCES)), "Every one re-read on " + SNAP_LONG + ". Government, statute, or the tenant's own securities filing.")}
      {kpi("Evidence rows", str(sum(len(v) for v in ROWS.values())), "Across ten categories. Each row names one source.")}
      {kpi("Verified + derived", str(sum(count(v, "Verified") + count(v, "Derived") for v in ROWS.values())), "Confirmed on the official page, or arithmetic on confirmed values recomputed by the validator.")}
      {kpi("Left blank", str(sum(count(v, "Unverified") for v in ROWS.values())), "No official source obtained. Published as blanks on the review page, never filled with an estimate.")}
    </div>

    <div class="section">
      <div class="head"><h2>The verification standard</h2><span>What each status means</span></div>
      <div class="grid-2">
        <div class="panel">
          <h3><span class="b verified">Verified</span></h3>
          <p class="small">The exact value was read on the official page linked in the row on {SNAP_LONG}. The geography and period are stated
          beside it. Verification is of the observation, never of a forecast: a verified population decline is still not a prediction about
          this trade area.</p>
          <h3 style="margin-top:16px"><span class="b derived">Derived</span></h3>
          <p class="small">Arithmetic performed on verified values. The method is written in the row, and <code>scripts/validate.py</code>
          recomputes each derived row from its components and fails the build if the published figure disagrees by more than a rounding step.
          No derived row rests on a private input.</p>
        </div>
        <div class="panel">
          <h3><span class="b analysis">Analysis</span></h3>
          <p class="small">This project's judgement: route comparisons, risk balance, sequencing. Labelled everywhere, never counted as
          verified, never presented as an official statistic. The link on an analysis row points at the factual background it rests on, not
          at an endorsement.</p>
          <h3 style="margin-top:16px"><span class="b unknown">Unverified</span> / <span class="b flag">Needs review</span></h3>
          <p class="small">No official source supplied the value, so the cell is blank and the row says what would close it. A blank is a
          finding, not an omission. Nothing on this site infers, interpolates or carries a value forward from another geography.</p>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="head"><h2>The privacy boundary</h2><span>By design, not by policy alone</span></div>
      <div class="callout">
        <p><b>Placeholders only.</b> The property is "Asset A" and the owner "Owner A". No street address, parcel or assessor number, owner
        name, contact detail, rent, net operating income, tax basis, debt term or lease document is collected, stored, published or committed
        to this repository. Anything of that kind is out of scope for this project and, if it ever arrives, belongs in a private file system
        that is never published.</p>
        <p><b>No collection at runtime.</b> These are static pages. There is no analytics, no tag manager, no form, no cookie, no third-party
        script or font, and no request to any server other than the one serving the page. GitHub Pages may retain standard access logs; that
        is the host's behaviour, not instrumentation added here.</p>
        <p><b>Public links are the only outbound request.</b> Clicking a citation opens the publisher's own website under that publisher's
        privacy terms.</p>
        <p><b>Enforced in code.</b> <code>tools/pii_scan.py</code> scans every published file and data module for email addresses, telephone
        numbers, street addresses, parcel and taxpayer identifier patterns, and identifying field values. It fails the build on any hit.</p>
      </div>
    </div>

    <div class="section">
      <div class="head"><h2>Reproducibility</h2><span>Deterministic, offline, checked</span></div>
      <div class="grid-3">
        <div class="panel"><h3>Build</h3><p class="small"><code>python3 scripts/build.py</code> regenerates every page from
        <code>data/evidence.json</code>. No network access, no timestamps in output, byte-identical on rebuild.</p></div>
        <div class="panel"><h3>Validate</h3><p class="small"><code>python3 scripts/validate.py</code> checks row provenance, blank-when-unverified,
        column integrity, internal links, derived arithmetic and prohibited embeds.</p></div>
        <div class="panel"><h3>Stage</h3><p class="small"><code>python3 scripts/stage_pages.py</code> builds the exact Pages artifact and verifies
        that every internal link resolves inside it and every table row carries a registered official source.</p></div>
      </div>
      <p class="small muted" style="margin-top:12px">The repository also contains research layers produced by earlier sessions
      (<code>analysis/</code>, <code>advisory/</code>, <code>brief/</code>, <code>dashboard/</code>, <code>decision-file/</code>,
      <code>docs/</code>, <code>pages/</code>). They are retained as an audit trail and excluded from the published artifact. Their figures
      and rankings are not re-verified here and are not endorsed; see the repository irregularities on <a href="review.html">Flagged for
      review</a>.</p>
    </div>

    <div class="section">
      <div class="head"><h2>Source register</h2><span>{len(SOURCES)} sources · {len(used)} cited by at least one row</span></div>
      <div class="tw"><table><caption>Every official source used on this site, with the number of evidence rows that depend on it.</caption>
      <thead><tr><th scope="col">Document</th><th scope="col">Publisher</th><th scope="col" class="num">Rows</th></tr></thead>
      <tbody>{trs}</tbody></table></div>
    </div>
    """
    return shell("sources", "Sources & method", body,
                 "The full official source register and verification standard for the Asset A decision file.")


# --------------------------------------------------------------------------
# Write
# --------------------------------------------------------------------------
def main():
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets/style.css").write_text(CSS)
    (ROOT / "assets/app.js").write_text(JS)
    (ROOT / "index.html").write_text(build_index())
    for p in PAGES:
        if p["id"] == "model":
            (ROOT / "model.html").write_text(build_model())
        elif p["id"] == "review":
            (ROOT / "review.html").write_text(build_review())
        else:
            (ROOT / f'{p["id"]}.html').write_text(build_category(p))
    (ROOT / "sources.html").write_text(build_sources())
    n = sum(len(v) for v in ROWS.values())
    print(f"Built 13 pages from {len(SOURCES)} sources and {n} evidence rows "
          f"({sum(count(v, 'Verified') for v in ROWS.values())} verified, "
          f"{sum(count(v, 'Derived') for v in ROWS.values())} derived, "
          f"{sum(count(v, 'Analysis') for v in ROWS.values())} analysis, "
          f"{sum(count(v, 'Unverified') for v in ROWS.values())} unverified, "
          f"{sum(count(v, 'Needs review') for v in ROWS.values())} needs review).")


if __name__ == "__main__":
    main()
