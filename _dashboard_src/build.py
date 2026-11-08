"""Deterministic generator for the /dashboard/ static site (session 27610006).

Outputs plain HTML + one stylesheet. No JavaScript, no forms, no trackers, no
external assets, no personal information. Every body row of every table carries a
link into the source register.
"""
from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import urlparse

import dataset as D

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dashboard"
DATA = D.to_json()

SRC = DATA["sources"]
FACTS = DATA["facts"]

PAGES = [
    ("index.html", "Overview", "01"),
    ("executive-summary.html", "Executive summary", "02"),
    ("geography.html", "Geography", "03"),
    ("demographics.html", "People & income", "04"),
    ("economy.html", "Economy & jobs", "05"),
    ("schools.html", "Schools", "06"),
    ("tenant.html", "Tenant & lease", "07"),
    ("tax.html", "Taxes & transfer", "08"),
    ("hazards.html", "Hazards", "09"),
    ("risk.html", "Risk register", "10"),
    ("projections.html", "Projections", "11"),
    ("decision.html", "Decision", "12"),
    ("repo-review.html", "Repo review", "13"),
    ("flagged.html", "Flagged for review", "14"),
    ("sources.html", "Sources & method", "15"),
]

STATUS_LABEL = {
    "verified": "Verified",
    "derived": "Derived",
    "unverified": "Unverified",
}

CSS = """
:root{--ink:#16191d;--mut:#5c6672;--line:#e3e7ec;--bg:#f6f8fa;--card:#ffffff;
--acc:#1d4ed8;--warn:#b45309;--bad:#b91c1c;--good:#15803d;}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
color:var(--ink);background:var(--bg)}
a{color:var(--acc);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{display:flex;min-height:100vh;align-items:flex-start}
aside{width:264px;flex:0 0 264px;background:#0f172a;color:#cbd5e1;padding:22px 18px;position:sticky;top:0;
max-height:100vh;overflow:auto}
aside .brand{display:block;color:#fff;font-weight:700;letter-spacing:.02em;font-size:15px;margin-bottom:2px}
aside .sub{display:block;color:#7d8da5;font-size:11px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:20px}
aside nav a{display:block;color:#cbd5e1;padding:7px 10px;border-radius:6px;font-size:13.5px;margin-bottom:1px}
aside nav a span{color:#64748b;font-size:11px;margin-right:8px;font-variant-numeric:tabular-nums}
aside nav a:hover{background:#1e293b;color:#fff;text-decoration:none}
aside nav a[aria-current=page]{background:#1e3a8a;color:#fff}
aside nav a[aria-current=page] span{color:#93c5fd}
aside .note{margin-top:20px;padding-top:14px;border-top:1px solid #1e293b;color:#7d8da5;font-size:11.5px;line-height:1.5}
main{flex:1;min-width:0;padding:26px 30px 60px;max-width:1180px}
header.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:baseline;justify-content:space-between;
border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:22px}
header.bar .eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
header.bar .stamp{font-size:12px;color:var(--mut)}
h1{font-size:26px;line-height:1.25;margin:0 0 6px}
h2{font-size:18px;margin:30px 0 10px}
h3{font-size:15px;margin:20px 0 6px}
p{margin:0 0 12px;max-width:76ch}
.lede{font-size:16px;color:#2b323b}
.mut{color:var(--mut);font-size:13px}
ul.clean{margin:0 0 14px;padding-left:20px;max-width:76ch}
ul.clean li{margin-bottom:6px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:12px;margin:16px 0 8px}
.card{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:14px 15px}
.card .k{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}
.card .v{font-size:25px;font-weight:650;margin:6px 0 4px;letter-spacing:-.01em}
.card .d{font-size:12.5px;color:var(--mut);line-height:1.45}
.card .s{font-size:11.5px;margin-top:8px;display:inline-block}
.callout{background:#eff6ff;border:1px solid #c7dbfe;border-left:3px solid var(--acc);border-radius:7px;
padding:13px 15px;margin:16px 0}
.callout.warn{background:#fffbeb;border-color:#fde68a;border-left-color:var(--warn)}
.callout.bad{background:#fef2f2;border-color:#fecaca;border-left-color:var(--bad)}
.callout h3{margin:0 0 6px;font-size:14px}
.callout p{margin:0 0 8px;font-size:13.5px}
.callout p:last-child{margin-bottom:0}
table{border-collapse:collapse;width:100%;background:var(--card);border:1px solid var(--line);
border-radius:8px;overflow:hidden;margin:10px 0 8px;font-size:13.5px}
caption{text-align:left;color:var(--mut);font-size:12px;padding:0 0 6px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
thead th{background:#f0f3f7;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:#414b58;
position:sticky;top:0}
tbody tr:last-child td{border-bottom:none}
tbody tr:nth-child(even){background:#fbfcfd}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
th.num{text-align:right}
.id{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px;color:var(--mut);white-space:nowrap}
.pill{display:inline-block;font-size:10.5px;padding:1px 7px;border-radius:99px;border:1px solid;white-space:nowrap}
.pill.v{color:var(--good);border-color:#a7f3d0;background:#ecfdf5}
.pill.d{color:var(--acc);border-color:#c7dbfe;background:#eff6ff}
.pill.u{color:var(--warn);border-color:#fde68a;background:#fffbeb}
.pill.sev{color:var(--bad);border-color:#fecaca;background:#fef2f2}
.pill.hi{color:#b45309;border-color:#fed7aa;background:#fff7ed}
.pill.mo{color:#92400e;border-color:#fde68a;background:#fffbeb}
.pill.lo{color:#3f6212;border-color:#d9f99d;background:#f7fee7}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px;margin:14px 0}
.panel{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:15px 16px}
.panel h3{margin-top:0}
.panel ul{margin:8px 0 0;padding-left:18px}
.panel li{margin-bottom:7px;font-size:13.5px}
.blank{color:#92400e;font-style:italic}
footer.foot{margin-top:34px;padding-top:14px;border-top:1px solid var(--line);color:var(--mut);font-size:12px}
.small{font-size:12.5px;color:var(--mut)}
.scroll{overflow-x:auto}
@media (max-width:860px){
 .wrap{flex-direction:column}
 aside{width:100%;flex:none;position:static;max-height:none}
 main{padding:18px 16px 46px}
}
"""


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def link(key: str, label: str | None = None) -> str:
    s = SRC[key]
    return f'<a href="{esc(s["url"])}">{esc(label or s["name"])}</a>'


def host(key: str) -> str:
    """Short, human-readable publisher label: the host of the official URL."""
    return urlparse(SRC[key]["url"]).netloc


def src_cell(key: str) -> str:
    s = SRC[key]
    return f'<a href="{esc(s["url"])}" title="{esc(s["name"])}">{esc(host(key))}</a>'


def pill(status: str) -> str:
    cls = {"verified": "v", "derived": "d", "unverified": "u"}[status]
    return f'<span class="pill {cls}">{STATUS_LABEL[status]}</span>'


def facts_table(category: str, title: str, extra_note: str = "") -> str:
    rows = [f for f in FACTS if f["category"] == category]
    n_v = sum(1 for f in rows if f["status"] == "verified")
    n_d = sum(1 for f in rows if f["status"] == "derived")
    n_u = sum(1 for f in rows if f["status"] == "unverified")
    out = [f'<h2>{esc(title)}</h2>']
    if extra_note:
        out.append(f'<p class="small">{extra_note}</p>')
    out.append(
        f'<p class="small">{len(rows)} rows · {n_v} verified · {n_d} derived · {n_u} unverified (left blank).</p>'
    )
    out.append('<div class="scroll"><table><caption>Every row links to the official source it was read from.</caption>')
    out.append("<thead><tr><th>ID</th><th>Indicator</th><th>Geography</th><th>Value</th>"
               "<th>Period</th><th>Status</th><th>Source</th></tr></thead><tbody>")
    for f in rows:
        val = f["value"]
        vcls = ' class="blank"' if f["status"] == "unverified" else ""
        note = f'<div class="small">{esc(f["note"])}</div>' if f["note"] else ""
        out.append(
            f'<tr><td class="id">{esc(f["id"])}</td>'
            f"<td><strong>{esc(f['indicator'])}</strong>{note}</td>"
            f'<td class="mut">{esc(f["geography"])}</td>'
            f"<td{vcls}>{esc(val)}</td>"
            f'<td class="mut">{esc(f["period"])}</td>'
            f"<td>{pill(f['status'])}</td>"
            f'<td class="small">{src_cell(f["source"])}</td></tr>'
        )
    out.append("</tbody></table></div>")
    return "\n".join(out)


def nav(current: str) -> str:
    items = []
    for fn, label, num in PAGES:
        cur = ' aria-current=page' if fn == current else ''
        items.append(f'<a href="{fn}"{cur}><span>{num}</span>{esc(label)}</a>')
    return "<nav>" + "".join(items) + "</nav>"


def page(current: str, title: str, body: str, eyebrow: str = "ASSET A · NET LEASE RESEARCH") -> str:
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<meta name="description" content="{esc(title)} — anonymised, source-linked Los Angeles net lease research.">'
        f"<title>{esc(title)} · Asset A dashboard</title>"
        '<link rel="stylesheet" href="assets/style.css"></head><body><div class="wrap">'
        '<aside><span class="brand">Asset A — Property Decision Desk</span>'
        "<span class=\"sub\">Anonymised · source-linked</span>"
        + nav(current)
        + '<div class="note">No address, parcel, owner or account identifier is collected or published. '
        "Unverified cells are left blank, never estimated.<br><br>"
        f"Evidence snapshot {esc(DATA['snapshot'])}.</div>"
        "</aside><main>"
        f'<header class="bar"><span class="eyebrow">{esc(eyebrow)}</span>'
        f'<span class="stamp">● Evidence snapshot · {esc(DATA["snapshot"])}</span></header>'
        + body
        + '<footer class="foot">Independent decision-support research built only from official sources. '
        "Not an appraisal, a legal opinion, or personalised financial, tax or investment advice. "
        "Static snapshot — no tracking, no forms, no third-party assets. "
        '<a href="sources.html">Method and limitations</a> · '
        '<a href="flagged.html">Flagged for review</a></footer>'
        "</main></div></body></html>\n"
    )


def src_footer(keys) -> str:
    seen, out = set(), []
    for k in keys:
        if k in seen:
            continue
        seen.add(k)
        s = SRC[k]
        out.append(f'<li><a href="{esc(s["url"])}">{esc(s["name"])}</a> — {esc(s["publisher"])}</li>')
    return ('<h2>Sources used on this page</h2><ul class="clean small">' + "".join(out) + "</ul>")


def fnum(x: float, nd: int = 2) -> str:
    return f"{x:,.{nd}f}"


def fpct(x: float, nd: int = 1) -> str:
    return f"{x*100:+.{nd}f}%"


# ---------------------------------------------------------------------------
# Page bodies
# ---------------------------------------------------------------------------
def body_index() -> str:
    v = sum(1 for f in FACTS if f["status"] == "verified")
    d = sum(1 for f in FACTS if f["status"] == "derived")
    u = sum(1 for f in FACTS if f["status"] == "unverified")
    b: list[str] = []
    b.append("<h1>Should you sell, or renew?</h1>")
    b.append('<p class="lede">A source-linked decision desk for one anonymised Jack in the Box net-leased property '
             "in the Los Angeles area with a lease expiry reported somewhere in 2030 to 2035. "
             "This dashboard separates what can be proved from official sources from what only you can supply, "
             "and it never fills the gap between them with an estimate.</p>")

    b.append('<div class="callout warn"><h3>Read this first</h3>'
             "<p>No address, parcel number, lease, rent roll, debt statement or tax basis was provided. "
             "Nothing about the subject property is asserted here. Regional evidence is context, not a forecast "
             "of this site, and no government agency publishes a value for it.</p>"
             '<p><a href="flagged.html">The 17 blocked or unverified items →</a></p></div>')

    b.append('<div class="cards">')
    for k, lab, val, desc, src in [
        ("Population, Los Angeles County", "July 2025", "9,694,934", "3.2% below the April 2020 estimates base", "S-02"),
        ("Unemployment, LA metro", "Sept 2026", "4.4%", "Down from 5.5% a year earlier", "S-03"),
        ("System same-store sales", "Q3 FY2026", "-1.1%", "Jack in the Box, 2,115 restaurants", "S-07"),
        ("10-Year Treasury", "5 Nov 2026", "4.84%", "The risk-free anchor a buyer will use", "S-04"),
        ("Earthquake, M≥6.7 in 30 years", "Los Angeles region", "60%", "USGS UCERF3, from 2014", "S-10"),
        ("Measure ULA above $5.4M", "City of LA", "4.00%", "Of gross consideration, not the excess", "S-15"),
    ]:
        b.append(f'<div class="card"><div class="k">{esc(lab)}</div><div class="v">{esc(val)}</div>'
                 f'<div class="d">{esc(k)} — {esc(desc)}</div>'
                 f'<a class="s" href="{esc(SRC[src]["url"])}">{esc(host(src))} ↗</a></div>')
    b.append("</div>")

    b.append('<h2>What the verified evidence actually says</h2>')
    b.append('<div class="grid2">')
    b.append('<div class="panel"><h3 style="color:var(--good)">Supporting the local economy</h3><ul>'
             "<li>Unemployment fell to 4.4% in the metro and 4.5% in the city and county, from 5.5% and 5.9% a year earlier. "
             f'{src_cell("S-03")}</li>'
             "<li>Nonfarm payrolls reached 6,282.1 thousand, up 30.2 thousand year over year. "
             f'{src_cell("S-03")}</li>'
             "<li>Median household income is $81,939 in the city and $90,112 in the county. "
             f'{src_cell("S-01")} {src_cell("S-02")}</li>'
             "<li>Education and health services, the metro's largest sector at 1,340.7 thousand jobs, grew 3.8%. "
             f'{src_cell("S-03")}</li>'
             "</ul></div>")
    b.append('<div class="panel"><h3 style="color:var(--bad)">Working against it</h3><ul>'
             "<li>The county has 3.2% fewer people than its 2020 estimates base and the city 0.8% fewer. "
             f'{src_cell("S-02")} {src_cell("S-01")}</li>'
             "<li>The tenant guided to 50 to 60 closures in fiscal 2026 and its franchise rental revenue fell 6.8% over 40 weeks. "
             f'{src_cell("S-07")}</li>'
             "<li>The tenant discontinued its dividend and share repurchase and refinanced $500 million of securitised notes. "
             f'{src_cell("S-07")}</li>'
             "<li>CPI-U is running at 3.7% with energy up 20.3%, while the employment cost index is up 3.9%. "
             f'{src_cell("S-03")}</li>'
             "</ul></div>")
    b.append("</div>")

    b.append('<h2>How this dashboard is organised</h2>')
    b.append('<div class="grid2">')
    for fn, label, what in [
        ("index.html", "Overview", "The headline picture and how to navigate it"),
        ("executive-summary.html", "Executive summary", "The decision, the reasoning, and the action plan"),
        ("geography.html", "Geography", "Where the asset sits and what that determines"),
        ("demographics.html", "People & income", "Population, households, income, poverty, education"),
        ("economy.html", "Economy & jobs", "Employment, wages, prices, rates, labour cost floors"),
        ("schools.html", "Schools", "Graduation outcomes as a stability and human-capital signal"),
        ("tenant.html", "Tenant & lease", "What the issuer's own SEC filings disclose"),
        ("tax.html", "Taxes & transfer", "Proposition 13, Measure ULA, transfer tax, and \u00a7 1031"),
        ("hazards.html", "Hazards", "Earthquake, wildfire and flood: what the agencies publish"),
        ("risk.html", "Risk register", "Business-as-usual and black-swan risks, each with a source"),
        ("projections.html", "Projections", "A transparent 2026-2035 extension with no invented probabilities"),
        ("decision.html", "Decision", "Four pathways, their drivers, and what has to be true for each"),
        ("repo-review.html", "Repo review", "Line-by-line findings from the inherited repository layers"),
        ("flagged.html", "Flagged for review", "Every blocked or unverified item and what closes it"),
        ("sources.html", "Sources & method", "The source register, the rules, and the limits"),
    ]:
        num = next(n for f, _, n in PAGES if f == fn)
        b.append(f'<div class="panel"><h3><a href="{fn}"><span class="id">{esc(num)}</span> '
                 f'{esc(label)}</a></h3><p class="small" style="margin:0">{esc(what)}</p></div>')
    b.append("</div>")

    b.append(f'<h2>Evidence counts</h2><p>{len(FACTS)} rows are published: {v} read directly from an official source '
             f'during this session, {d} derived with their arithmetic shown, and {u} left blank because they could '
             f'not be confirmed. {len(SRC)} official sources back them.</p>')
    b.append(src_footer(["S-01", "S-02", "S-03", "S-04", "S-07", "S-10", "S-15"]))
    return "\n".join(b)


def body_exec() -> str:
    b: list[str] = []
    b.append("<h1>Executive summary</h1>")
    b.append('<p class="lede">Written for the owner of one anonymised single-tenant net-leased Jack in the Box '
             "property in the Los Angeles area, with a lease expiry reported somewhere between 2030 and 2035.</p>")

    b.append('<div class="callout"><h3>The short answer</h3>'
             "<p><strong>Prepare to exit, but do not sign anything irreversible until four documents are in hand.</strong> "
             "The verified evidence points one way: the operator's system is contracting, its rental income is falling, "
             "and its cost floor is fixed by law at $20.00 an hour. The local economy is stable but not growing into "
             "new supply. That combination rewards an owner who controls the timing of the exit over an owner who waits "
             "to be told the terms.</p>"
             "<p>What it does <em>not</em> justify is a decision made today. The rent, the expiry date, the obligor and "
             "the tax basis are unknown. Any ranking of sell versus renew built on those blanks would be a guess dressed "
             "as arithmetic, so this dashboard refuses to produce one.</p>"
             '<p><a href="decision.html">See the four pathways and their drivers →</a></p></div>')

    b.append("<h2>1. The situation</h2>")
    b.append('<div class="scroll"><table><caption>What is known about the asset, and what is not.</caption>'
             "<thead><tr><th>Fact</th><th>Status</th><th>Consequence</th><th>Source</th></tr></thead><tbody>")
    for fact, status, cons, src in [
        ("A Jack in the Box with a net lease", "Reported, not verified", "Drives the whole analysis, but no lease document was supplied", "S-07"),
        ("Expiry window 2030 to 2035", "Reported, not verified", "A five-year range, not a date; the two ends give different answers", "S-07"),
        ("Central Los Angeles location", "Reported, not verified", "'Central Los Angeles' is not a legal or census boundary", "S-01"),
        ("Contract rent and escalations", "Unknown", "No income figure can be verified, so cash flows are expressed in multiples of one year of base rent", "S-07"),
        ("Lease obligor", "Unknown", "Corporate credit and single-unit franchisee credit are different risks", "S-07"),
        ("Tax basis and depreciation", "Unknown", "Determines the tax on a sale and the value of a § 1031 exchange", "S-17"),
    ]:
        cls = "u" if status != "Reported, not verified" else "d"
        b.append(f'<tr><td><strong>{esc(fact)}</strong></td><td><span class="pill {cls}">{esc(status)}</span></td>'
                 f'<td class="mut">{esc(cons)}</td><td class="small">{src_cell(src)}</td></tr>')
    b.append("</tbody></table></div>")

    b.append("<h2>2. Six findings that move the decision</h2>")
    b.append('<div class="scroll"><table><caption>Each finding is traceable to a named official source.</caption>'
             "<thead><tr><th>#</th><th>Finding</th><th>Why it matters here</th><th>Source</th></tr></thead><tbody>")
    findings = [
        ("The tenant is shrinking, and it is shrinking through franchised units.",
         "Management guided to about 2,100 restaurants for fiscal 2026 with roughly 25 openings against 50 to 60 closures, most of them franchised. A block closure programme is named in the release.",
         "S-07"),
        ("The tenant's rental income is falling faster than its revenue.",
         "Franchise rental revenue over 40 weeks was $242.526 million against $260.254 million a year earlier, a 6.8% decline, while total revenue fell 1.8% in the quarter. Rent is the line item that sits directly upstream of your rent.",
         "S-07"),
        ("The tenant's cost floor is set by statute, not by negotiation.",
         "California's fast-food minimum wage has been $20.00 per hour since April 1, 2024 and applies to franchisees as well as the brand owner. Unit margins cannot be repaired by cutting the wage line.",
         "S-09"),
        ("The local economy is steady, not expanding into new supply.",
         "Unemployment fell to 4.4% in the metro and nonfarm payrolls rose 0.5%, but the county has 3.2% fewer residents than its 2020 estimates base. Demand is not growing to absorb a marginal site.",
         "S-03"),
        ("Money is no longer cheap, and that is what a buyer prices against.",
         "The ten-year Treasury stood at 4.84% on 2026-11-05 and traded between 4.77% and 5.31% over the preceding two months. Net-lease values are discounted off this anchor.",
         "S-04"),
        ("Selling inside the City of Los Angeles can cost 4% to 5.5% of the price before anything else.",
         "Measure ULA charges 4% of gross consideration above $5,400,000 and 5.5% at or above $10,900,000, on the full price rather than the excess, on top of a 0.45% city base and 0.11% county tax.",
         "S-15"),
        ("The ground itself carries a 60% thirty-year earthquake likelihood.",
         "USGS UCERF3 puts the chance of one or more M≥6.7 events in the Los Angeles region at 60% over thirty years. Standard property policies generally exclude earthquake.",
         "S-10"),
    ]
    for i, (head, why, src) in enumerate(findings, 1):
        b.append(f'<tr><td class="id">F{i}</td><td><strong>{esc(head)}</strong></td>'
                 f'<td class="mut">{esc(why)}</td><td class="small">{src_cell(src)}</td></tr>')
    b.append("</tbody></table></div>")

    b.append("<h2>3. The risk balance</h2>")
    b.append('<div class="grid2">')
    b.append('<div class="panel"><h3>Risks that argue for exiting</h3><ul>'
             f'<li>Tenant credit is deteriorating while the system contracts. {src_cell("S-07")}</li>'
             f'<li>Concentration: one site, one operator, one intersection, no internal diversification. {src_cell("S-07")}</li>'
             f'<li>Earthquake likelihood of 60% over thirty years, generally uninsured. {src_cell("S-10")}</li>'
             f'<li>Cap-rate repricing risk while the ten-year Treasury sits near 4.84%. {src_cell("S-04")}</li>'
             f'<li>Transfer-tax exposure has a known, dated schedule and will not get cheaper by waiting. {src_cell("S-15")}</li>'
             "</ul></div>")
    b.append('<div class="panel"><h3>Risks that argue for patience</h3><ul>'
             f'<li>Selling crystallises tax now; a § 1031 exchange can defer it but must be executed to deadline. {src_cell("S-17")}</li>'
             f'<li>No cap rate can be verified from an official source, so the achievable price is unknown here. {src_cell("S-05")}</li>'
             f'<li>The local labour market is genuinely improving: unemployment 4.4%, payrolls up 0.5%. {src_cell("S-03")}</li>'
             f'<li>A sale with a short remaining term is discounted by buyers; an extension can restore term. {src_cell("S-07")}</li>'
             f'<li>Median household income of $81,939 in the city and $90,112 in the county supports local spend. {src_cell("S-01")}</li>'
             "</ul></div>")
    b.append("</div>")

    b.append("<h2>4. The action plan</h2>")
    b.append('<div class="scroll"><table><caption>Dated only where an official source fixes the date.</caption>'
             "<thead><tr><th>Step</th><th>Action</th><th>Gate it closes</th><th>Source</th></tr></thead><tbody>")
    for step, action, gate, src in [
        ("1", "Pull the deed, the executed lease with every amendment, the estoppel certificate and the current tax bill.",
         "K-F-01, K-F-03, K-F-04, K-F-05, K-F-06", "S-20"),
        ("2", "Establish whether the parcel is inside the incorporated City of Los Angeles.",
         "K-F-02 — decides whether Measure ULA applies", "S-15"),
        ("3", "Confirm the lease obligor and any guaranty, and test the total remaining term including options against the 35-year reassessment rule.",
         "K-F-06, K-F-07, K-F-08", "S-19"),
        ("4", "Order an as-built insurance quote including a difference-in-conditions earthquake quote, and look the parcel up in the CAL FIRE and FEMA viewers.",
         "K-F-13, K-F-14, R-14", "S-11"),
        ("5", "Ask the operator, in writing, whether this site is inside the block closure programme and whether they will commit to a term-certain extension.",
         "K-F-12, R-02", "S-07"),
        ("6", "Have a tax adviser model the after-tax proceeds both ways, with and without a § 1031 exchange, using your actual basis.",
         "K-F-10, R-13", "S-17"),
        ("7", "Only then compare the four pathways, using the present-value grids on the projections page with your own rent and your own discount rate.",
         "K-F-09, K-F-11", "S-04"),
    ]:
        b.append(f'<tr><td class="id">{esc(step)}</td><td>{esc(action)}</td>'
                 f'<td class="mut">{esc(gate)}</td><td class="small">{src_cell(src)}</td></tr>')
    b.append("</tbody></table></div>")

    b.append('<div class="callout bad"><h3>What this page deliberately does not give you</h3>'
             "<p>A price. A cap rate. A probability that the tenant renews. A ranking that says sell beats renew by a "
             "stated margin. None of those can be derived from an official source for this property, and inventing them "
             "would be the single most damaging thing this report could do. The four documents in step 1 supply them; "
             "until then the honest answer is that the decision is not yet determinable.</p></div>")

    b.append(src_footer(["S-01", "S-02", "S-03", "S-04", "S-05", "S-07", "S-09", "S-10", "S-11", "S-15", "S-17", "S-19", "S-20"]))
    return "\n".join(b)


CATEGORY_PAGES = [
    ("geography.html", "Geography", "geography",
     "Where the asset sits determines which taxes, hazard maps and school assignments apply to it. "
     "'Central Los Angeles' is a planning colloquialism, not a census or legal boundary, so every figure below is "
     "labelled with the official geography it was actually measured for.",
     ["S-01", "S-02", "S-11", "S-12", "S-15", "S-20"]),
    ("demographics.html", "People & income", "demographics",
     "Population and income set the demand ceiling for a quick-service restaurant. Both the level and the direction "
     "matter: Los Angeles has high incomes and a shrinking population count, which is an unusual and important combination.",
     ["S-01", "S-02"]),
    ("economy.html", "Economy & jobs", "economy",
     "Employment, wages, prices and the risk-free rate drive both the operator's ability to pay rent and the price a "
     "buyer will pay for that rent. Labour-cost floors are set by statute and are published by the state.",
     ["S-01", "S-02", "S-03", "S-04", "S-05", "S-08", "S-09"]),
    ("schools.html", "Schools", "schools",
     "School outcomes are a slow-moving signal of neighbourhood stability and household formation, and they feed into "
     "residential demand around a retail site. They are a weak signal for a drive-thru; treat them as context.",
     ["S-13", "S-14"]),
    ("tenant.html", "Tenant & lease", "tenant",
     "Everything here comes from the issuer's own filings with the SEC. System performance is not site performance, "
     "and franchise-agreement expiry is not your real-estate lease expiry — the two are often confused and they are not the same document.",
     ["S-06", "S-07"]),
    ("tax.html", "Taxes & transfer", "tax",
     "On a net-leased single tenant, the tax consequences of selling can exceed an entire year of rent. "
     "California reassesses on change of ownership, Los Angeles adds a graduated transfer tax, and federal law "
     "offers a deferral route with hard deadlines.",
     ["S-17", "S-18", "S-19", "S-15", "S-16"]),
    ("hazards.html", "Hazards", "hazards",
     "Agencies publish likelihoods, not predictions. Every number below is a published agency figure with its date and "
     "its region, and none of them can be converted into a statement about this specific parcel without the address.",
     ["S-10", "S-11", "S-12", "S-21"]),
]


def body_category(cat: str, title: str, lede: str, srcs) -> str:
    b = [f"<h1>{esc(title)}</h1>", f'<p class="lede">{esc(lede)}</p>']
    b.append(facts_table(cat, "Verified rows"))
    b.append(src_footer(srcs))
    return "\n".join(b)


def body_risk() -> str:
    b = ["<h1>Risk register</h1>"]
    b.append('<p class="lede">Eighteen risks: fourteen business-as-usual and four black swan. Each one is tied to a '
             "published official figure where one exists. Where no agency publishes a probability, no probability is asserted.</p>")
    b.append('<div class="scroll"><table><caption>Severity is analyst judgement based on the cited evidence, not an official rating.</caption>'
             "<thead><tr><th>ID</th><th>Type</th><th>Risk</th><th>Evidence</th><th>Severity</th><th>Source</th></tr></thead><tbody>")
    sev_cls = {"Severe": "sev", "High": "hi", "Medium": "mo", "Moderate": "mo", "Low": "lo"}
    for rid, rtype, name, ev, sev, src in DATA["risks"]:
        b.append(f'<tr><td class="id">{esc(rid)}</td><td class="mut">{esc(rtype)}</td>'
                 f'<td><strong>{esc(name)}</strong></td><td class="mut">{esc(ev)}</td>'
                 f'<td><span class="pill {sev_cls.get(sev,"mo")}">{esc(sev)}</span></td>'
                 f'<td class="small">{src_cell(src)}</td></tr>')
    b.append("</tbody></table></div>")
    b.append('<div class="callout warn"><h3>On black swan events</h3>'
             "<p>Wildfire and earthquake are not symmetrical with ordinary business risk. A 60% thirty-year likelihood "
             "of a magnitude 6.7 or greater earthquake in the Los Angeles region is a published USGS figure, but it says "
             "nothing about this building, its construction, its retrofit history or its soil. Those are engineering "
             "questions, and they need a site-specific answer before any of the pathway comparisons are meaningful.</p></div>")
    b.append(src_footer(sorted({r[5] for r in DATA["risks"]})))
    return "\n".join(b)


def body_projections() -> str:
    b = ["<h1>Projections 2026 to 2035</h1>"]
    b.append('<p class="lede">This page is arithmetic, not prophecy. It extends published official trends forward and '
             "shows every step. It assigns no probability to any scenario, because no official source assigns one.</p>")
    b.append('<div class="callout warn"><h3>What this is not</h3>'
             "<p>No government agency publishes a forecast for this parcel, and no official source ranks the scenarios below. "
             "The tables are extensions of measured aggregate trends for Los Angeles, offered so that the direction and the "
             "magnitude of the arithmetic are visible. A single restaurant site can move against its region in either direction.</p></div>")

    b.append("<h2>1. Verified inputs</h2>")
    b.append('<div class="scroll"><table><caption>Every input was read from the official source during this session.</caption>'
             "<thead><tr><th>Input</th><th>Value</th><th>Measured over</th><th>Source</th></tr></thead><tbody>")
    for p in DATA["projection_inputs"]:
        span = f'{p["span_years"]} years' if p["span_years"] else "point observation"
        b.append(f'<tr><td>{esc(p["label"])}</td><td class="num"><strong>{esc(p["value"])}</strong></td>'
                 f'<td class="mut">{esc(span)}</td><td class="small">{src_cell(p["source"])}</td></tr>')
    b.append("</tbody></table></div>")

    b.append("<h2>2. Scenario definitions</h2>")
    b.append('<div class="scroll"><table><caption>No weights are attached. These are conditional paths, not a probability distribution.</caption>'
             "<thead><tr><th>Scenario</th><th>Basis</th><th>Population</th><th>Employment</th><th>Rent index</th><th>Inputs</th></tr></thead><tbody>")
    for s in DATA["scenarios"]:
        b.append(f'<tr><td><strong>{esc(s["name"])}</strong></td><td class="mut">{esc(s["basis"])}</td>'
                 f'<td class="num">{fpct(s["pop_annual"])}/yr</td><td class="num">{fpct(s["emp_annual"])}/yr</td>'
                 f'<td class="num">{fpct(s["rent_annual"])}/yr</td>'
                 f'<td class="small">{src_cell("S-02")} {src_cell("S-03")}</td></tr>')
    b.append("</tbody></table></div>")
    b.append('<p class="small">The rent index uses the published Los Angeles CPI-U rate of +3.7% as its growth rate, '
             'so that no unverified escalation assumption enters the arithmetic. It is an index of purchasing power, '
             'not a forecast of what any tenant will agree to pay.</p>')

    b.append("<h2>3. Extended indices to 2030 and 2035</h2>")
    b.append('<div class="scroll"><table><caption>Index, 2026 = 1.000. Compounded from the annual rates above; the formula is (1 + r) ^ n.</caption>'
             "<thead><tr><th>Scenario</th><th>Measure</th><th>2030 (n=4)</th><th>2035 (n=9)</th><th>Source</th></tr></thead><tbody>")
    labels = {"population_index": "Population", "employment_index": "Employment", "rent_index": "Rent index"}
    srcmap = {"population_index": "S-02", "employment_index": "S-03", "rent_index": "S-03"}
    for proj in DATA["projections"]:
        s = next(x for x in DATA["scenarios"] if x["key"] == proj["key"])
        for key, lab in labels.items():
            y30 = proj["years"]["2030" if "2030" in proj["years"] else 2030][key]
            y35 = proj["years"]["2035" if "2035" in proj["years"] else 2035][key]
            b.append(f'<tr><td>{esc(s["name"])}</td><td class="mut">{esc(lab)}</td>'
                     f'<td class="num">{fnum(y30,3)}</td><td class="num">{fnum(y35,3)}</td>'
                     f'<td class="small">{src_cell(srcmap[key])}</td></tr>')
    b.append("</tbody></table></div>")

    b.append("<h2>4. What a buyer is discounting against</h2>")
    b.append(f'<p>The ten-year Treasury constant maturity yield was {D.RISK_FREE*100:.2f}% on 2026-11-05. '
             "Net-lease buyers price off this anchor plus a spread. The grids below show the present value of an "
             "annuity-due of one unit of current annual base rent, which lets you read the multiple directly once you "
             "know your own rent. No residual or sale value is included, because no cap rate can be verified from an "
             "official source.</p>")

    for name, key, growth, cap in [
        ("Level rent (no escalator)", "level", 0.0, "PV of 1.000 of base rent per year, received at the start of each year, no growth."),
        (f"Rent growing at the published CPI-U rate of 3.7%", "growth", 0.037,
         "PV of 1.000 of base rent per year growing at the Los Angeles CPI-U rate of +3.7% measured to September 2026."),
    ]:
        b.append(f"<h3>{esc(name)}</h3>")
        b.append(f'<div class="scroll"><table><caption>{esc(cap)}</caption><thead><tr><th>Discount rate</th>'
                 + "".join(f'<th class="num">{y} yrs<br><span class="mut">exp {2026+y}</span></th>' for y in DATA["horizons"])
                 + "<th>Anchor</th></tr></thead><tbody>")
        for row in DATA["grids"][key]:
            b.append(f'<tr><td>{row["rate"]*100:.2f}%<div class="small mut">4.84% + {row["premium"]*100:.0f}%</div></td>'
                     + "".join(f'<td class="num">{fnum(c)}</td>' for c in row["cells"])
                     + f'<td class="small">{src_cell("S-04")}</td></tr>')
        b.append("</tbody></table></div>")

    b.append("<h3>How to use these grids</h3>")
    b.append('<ul class="clean">'
             "<li>Choose the column matching the actual remaining term once you have the expiry date.</li>"
             "<li>Choose the row matching the discount rate you believe a buyer would use: the verified 4.84% risk-free anchor plus your judgement of the spread.</li>"
             "<li>Multiply the cell by your annual base rent. The result is the present value of the contracted rent alone, before any residual value, tax, closing cost or vacancy assumption.</li>"
             "<li>Compare that figure with what the market would pay. That comparison needs a cap rate, which no official source publishes — see the flagged items.</li>"
             "</ul>")
    b.append('<p class="small">Formula: PV = sum over t = 0 to n-1 of ((1 + g) / (1 + d)) ^ t, with g = 0 for the first grid '
             "and g = 3.7% for the second. Published to two decimal places; the build computes it deterministically.</p>")
    b.append(src_footer(["S-01", "S-02", "S-03", "S-04", "S-07"]))
    return "\n".join(b)


def body_decision() -> str:
    b = ["<h1>Decision pathways</h1>"]
    b.append('<p class="lede">Four realistic paths. This page states what each one depends on and what has to be true '
             "for it to work. It does <strong>not</strong> rank them with a score, because a score would require "
             "probabilities and prices that no official source supplies.</p>")
    b.append('<div class="callout warn"><h3>Why there is no winner declared here</h3>'
             "<p>Earlier layers of this repository published numerical rankings of these pathways, and they disagreed "
             "with each other. They disagreed because each one quietly assumed a rent, a cap rate and a renewal "
             "probability. None of those was ever supplied. A ranking built that way is not analysis; it is a guess with "
             "decimal places. The drivers are laid out below so that you can weight them yourself once the blocker "
             "documents are in hand.</p></div>")

    for p in DATA["pathways"]:
        b.append(f'<h2>Option {esc(p["key"])} — {esc(p["name"])}</h2>')
        b.append(f'<p>{esc(p["summary"])}</p>')
        b.append('<div class="grid2">')
        b.append('<div class="panel"><h3 style="color:var(--good)">What supports it</h3><ul>')
        for text, src in p["drivers"]:
            b.append(f'<li>{esc(text)} {src_cell(src)}</li>')
        b.append("</ul></div>")
        b.append('<div class="panel"><h3 style="color:var(--bad)">What could break it</h3><ul>')
        for text, src in p["risks"]:
            b.append(f'<li>{esc(text)} {src_cell(src)}</li>')
        b.append("</ul></div>")
        b.append("</div>")

    b.append("<h2>The hinge: what has to be true</h2>")
    b.append('<div class="scroll"><table><caption>Conditions that change the answer, and where to verify each one.</caption>'
             "<thead><tr><th>Condition</th><th>If true, it favours</th><th>Verified by</th></tr></thead><tbody>")
    for cond, fav, src in [
        ("The lease obligor is Jack in the Box Inc. corporate, not a single-unit franchisee",
         "Renewing or extending — corporate credit survives a site closure", "S-07"),
        ("The remaining term including options would reach 35 years on renewal",
         "Selling — a renewal that long creates a reassessment under California law", "S-19"),
        ("The parcel is inside the incorporated City of Los Angeles and would sell above $5,400,000",
         "Structuring the price or timing around Measure ULA, or exchanging rather than selling outright", "S-15"),
        ("The operator will commit to a term-certain extension at or above current rent",
         "A short extension then selling from strength", "S-07"),
        ("The site is inside the announced block closure programme",
         "Exiting early, before the closure is known to the market", "S-07"),
        ("Your adjusted basis is low relative to today's value",
         "A § 1031 exchange rather than an outright sale", "S-17"),
        ("Existing debt matures before the lease expires",
         "Selling or refinancing early — a maturity inside the term is a hard constraint", "S-04"),
    ]:
        b.append(f'<tr><td>{esc(cond)}</td><td class="mut">{esc(fav)}</td><td class="small">{src_cell(src)}</td></tr>')
    b.append("</tbody></table></div>")

    b.append("<h2>Balancing wealth preservation against growth</h2>")
    b.append('<p>Preservation and growth pull in different directions here, and the honest framing is that this asset '
             "is a preservation instrument exposed to a growth question. A net lease with a credit tenant preserves "
             "capital by producing a contractual, inflation-linked income stream; it grows only if the rent steps up "
             "or the cap rate falls. Right now the verified evidence says the rent is at risk — system same-store sales "
             f'fell 1.1% in Q3 FY2026 — and the cap rate anchor has risen, with the ten-year Treasury at '
             f'{D.RISK_FREE*100:.2f}%. Both halves of the growth case are under pressure at the same time.</p>')
    b.append('<p>Preservation, meanwhile, is threatened by concentration rather than by income. One site and one '
             "operator in a region with a published 60% thirty-year likelihood of a magnitude 6.7 or greater earthquake "
             "is an undiversified position regardless of how good the lease looks. If this property is a meaningful "
             "share of your net worth, the diversification argument is stronger than any argument about the lease.</p>")
    b.append('<p class="mut">This is reasoning from published evidence, not personalised investment advice. Your tax '
             "position, liquidity needs, other holdings and time horizon all matter and none of them is known here.</p>")

    b.append(src_footer(sorted({s for p in DATA["pathways"] for _, s in p["drivers"] + p["risks"]})))
    return "\n".join(b)


def body_repo_review() -> str:
    b = ["<h1>Repository review</h1>"]
    b.append('<p class="lede">A line-by-line pass over the inherited layers of this repository, conducted on '
             f'{esc(DATA["snapshot"])}. Findings are irregularities, not accusations: earlier sessions worked from '
             "the same incomplete brief, and every one of these items is reproducible.</p>")

    b.append('<div class="cards">')
    counts = {}
    for f in FACTS:
        counts[f["category"]] = counts.get(f["category"], 0) + 1
    b.append(f'<div class="card"><div class="k">Layers inherited</div><div class="v">6</div>'
             f'<div class="d">Root workspace, docs/, analysis/, brief/, pages/, decision-file/, plus advisory/ and audit/.</div></div>')
    b.append(f'<div class="card"><div class="k">Irregularities found</div><div class="v">{len(DATA["irregularities"])}</div>'
             f'<div class="d">Two high-severity privacy or sourcing issues and three high-severity accuracy issues.</div></div>')
    b.append(f'<div class="card"><div class="k">Rows re-verified here</div><div class="v">{sum(1 for f in FACTS if f["status"]=="verified")}</div>'
             f'<div class="d">Read directly from official sources during this session, none inherited on trust.</div></div>')
    b.append(f'<div class="card"><div class="k">Left blank</div><div class="v">{sum(1 for f in FACTS if f["status"]=="unverified")}</div>'
             f'<div class="d">Cells that could not be confirmed, published empty rather than estimated.</div></div>')
    b.append("</div>")

    b.append("<h2>Layer inventory</h2>")
    b.append('<div class="scroll"><table><caption>What each inherited layer is, and how this session treated it.</caption>'
             "<thead><tr><th>Layer</th><th>Origin</th><th>This session's finding</th><th>Source</th></tr></thead><tbody>")
    for layer, origin, finding, src in [
        ("Root workspace (9 HTML pages)", "sessions 5cb84cd0, 7d4577fd, 9fa62774",
         "Evidence-gated and internally consistent. Its Flagged page correctly states that no property valuation is available. Not modified by this session.", "S-01"),
        ("docs/ (10 pages)", "sessions ff406d61, 93f3087c",
         "Rows without direct source links and two non-official hosts cited. Read-only here.", "S-01"),
        ("analysis/ (11 pages)", "session 8d650ba0",
         "Verified this session: 22 links to a commercial brokerage domain and 4 to a private law firm inside published tables. Read-only here.", "S-01"),
        ("brief/ (9 pages)", "session 796b983f",
         "Published Measure ULA thresholds that expired on 2026-06-30. Read-only here; corrected values are on the taxes page.", "S-15"),
        ("pages/ (9 pages)", "session 93f3087c",
         "Renders the repository account handle in three pages and cites aggregator domains. Read-only here.", "S-01"),
        ("decision-file/ (23 pages)", "session d989a5c6",
         "All external links are official, but the model anchors to a January 2026 Treasury yield and treats franchise-agreement dates as the lease expiry. Read-only here.", "S-04"),
        ("advisory/ (12 pages)", "session e04af39b",
         "Withheld from the published site by another session after this session's base commit, on the grounds that its scenario weights and pathway rankings are not established by the official sources it cites.", "S-01"),
    ]:
        b.append(f'<tr><td><strong>{esc(layer)}</strong></td><td class="mut">{esc(origin)}</td>'
                 f'<td class="mut">{esc(finding)}</td><td class="small">{src_cell(src)}</td></tr>')
    b.append("</tbody></table></div>")

    b.append("<h2>Irregularities flagged</h2>")
    b.append('<div class="scroll"><table><caption>Each finding is reproducible from the working tree or from the official source linked beside it.</caption>'
             "<thead><tr><th>ID</th><th>Severity</th><th>Finding</th><th>How it was verified</th><th>How this layer handles it</th><th>Ref</th></tr></thead><tbody>")
    for rid, sev, finding, verif, remedy, src in DATA["irregularities"]:
        cls = "sev" if sev.startswith("High") else ("hi" if sev.startswith("Medium") else "lo")
        b.append(f'<tr><td class="id">{esc(rid)}</td><td><span class="pill {cls}">{esc(sev)}</span></td>'
                 f'<td>{esc(finding)}</td><td class="mut">{esc(verif)}</td><td class="mut">{esc(remedy)}</td>'
                 f'<td class="small">{src_cell(src)}</td></tr>')
    b.append("</tbody></table></div>")

    b.append('<div class="callout"><h3>Scope note</h3>'
             "<p>This session edits only <code>dashboard/</code>, <code>dashboard_src/</code> and its own append-only "
             "section of the coordination board. Irregularities in other layers are reported for manual review, not "
             "silently corrected, because those files belong to other sessions. Two are logged as cross-session requests.</p></div>")
    b.append(src_footer(sorted({r[5] for r in DATA["irregularities"]})))
    return "\n".join(b)


def body_flagged() -> str:
    b = ["<h1>Flagged for review</h1>"]
    b.append('<p class="lede">Everything that could not be confirmed from an official source. These cells are left '
             "blank in the tables above rather than filled with an estimate, and nothing here blocks publication — "
             "it is a list of what remains open.</p>")
    b.append('<div class="scroll"><table><caption>Each item states what closes it.</caption>'
             "<thead><tr><th>ID</th><th>Priority</th><th>Unverified item</th><th>Why it matters</th><th>What closes it</th><th>Ref</th></tr></thead><tbody>")
    sev_cls = {"Blocker": "sev", "High": "hi", "Medium": "mo", "Low": "lo"}
    for fid, prio, item, why, closes, src in DATA["flags"]:
        b.append(f'<tr><td class="id">{esc(fid)}</td><td><span class="pill {sev_cls.get(prio,"mo")}">{esc(prio)}</span></td>'
                 f'<td><strong>{esc(item)}</strong></td><td class="mut">{esc(why)}</td>'
                 f'<td class="mut">{esc(closes)}</td><td class="small">{src_cell(src)}</td></tr>')
    b.append("</tbody></table></div>")

    b.append('<div class="callout bad"><h3>The four blockers</h3>'
             "<p>K-F-01 through K-F-04 are the ones that stop the analysis. Without the deed, the lease, the rent and "
             "the obligor, no price, no cash-flow forecast and no ranking can be verified for this property. Every other "
             "item on this page refines an answer; those four decide whether an answer exists.</p></div>")

    b.append("<h2>Values deliberately left blank in the tables</h2>")
    b.append('<div class="scroll"><table><caption>These rows appear in their category tables with an empty value cell.</caption>'
             "<thead><tr><th>Row</th><th>Category</th><th>Would come from</th><th>Source</th></tr></thead><tbody>")
    for f in FACTS:
        if f["status"] != "unverified":
            continue
        b.append(f'<tr><td><strong>{esc(f["indicator"])}</strong><div class="small mut">{esc(f["id"])}</div></td>'
                 f'<td class="mut">{esc(f["category"])}</td>'
                 f'<td class="mut">{esc(f["note"] or "Owner-supplied document")}</td>'
                 f'<td class="small">{src_cell(f["source"])}</td></tr>')
    b.append("</tbody></table></div>")
    b.append(src_footer(sorted({f[5] for f in DATA["flags"]})))
    return "\n".join(b)


def body_sources() -> str:
    b = ["<h1>Sources and method</h1>"]
    b.append(f'<p class="lede">{len(SRC)} official sources, every one fetched and read during this session. '
             "No aggregator, brokerage, law firm or news site was used as a source of any published value.</p>")

    b.append("<h2>The rules this layer follows</h2>")
    b.append('<ul class="clean">'
             "<li><strong>Official or blank.</strong> A value is published only if it was read from the linked official "
             "source during this session. Otherwise the cell is left empty and flagged.</li>"
             "<li><strong>Derived means the arithmetic is shown.</strong> A derived cell prints its inputs and its formula "
             "on the page. It is never presented as an observation.</li>"
             "<li><strong>No inherited trust.</strong> Nothing was copied from an earlier layer of this repository. "
             "Where an earlier session's figure was useful but not re-verified, it is on the flagged page instead.</li>"
             "<li><strong>No probabilities.</strong> Where no agency publishes a likelihood, no likelihood is asserted.</li>"
             "<li><strong>No personal information.</strong> No name, address, parcel identifier, email, phone number or "
             "account handle is collected or published. The asset is called Asset A throughout.</li>"
             "<li><strong>No scripts, no trackers, no forms, no third-party assets.</strong> The site is static HTML and one stylesheet.</li>"
             "</ul>")

    b.append("<h2>Source register</h2>")
    b.append('<div class="scroll"><table><caption>All sources were accessed on ' + esc(DATA["snapshot"]) + ".</caption>"
             "<thead><tr><th>ID</th><th>Source</th><th>Publisher</th><th>URL</th></tr></thead><tbody>")
    for k, s in SRC.items():
        b.append(f'<tr><td class="id">{esc(k)}</td><td><strong>{esc(s["name"])}</strong>'
                 f'<div class="small mut">{esc(s["accessed"])}</div></td><td class="mut">{esc(s["publisher"])}</td>'
                 f'<td class="small"><a href="{esc(s["url"])}">{esc(s["url"])}</a></td></tr>')
    b.append("</tbody></table></div>")

    b.append("<h2>Limitations</h2>")
    b.append('<ul class="clean">'
             "<li>Regional data is not a parcel forecast. Census, BLS and CDE figures describe a city or a county, not a site.</li>"
             "<li>Issuer filings describe a system of 2,115 restaurants, not the one you own.</li>"
             "<li>Source links were read on the snapshot date. Published series are revised; the BLS area summary is a rolling document and its contents change with each release.</li>"
             "<li>Cap rates, comparable sales, insurance premiums and construction costs have no official source and are therefore absent.</li>"
             "<li>Severity ratings in the risk register are analyst judgement applied to cited evidence, not official ratings.</li>"
             "<li>The projection tables extend published trends arithmetically. They are not forecasts and carry no probability weight.</li>"
             "<li>This is not an appraisal, a legal opinion, or personalised financial, tax or investment advice.</li>"
             "</ul>")
    return "\n".join(b)


def build() -> None:
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "style.css").write_text(CSS, encoding="utf-8")

    bodies = {
        "index.html": (body_index(), "Overview"),
        "executive-summary.html": (body_exec(), "Executive summary"),
        "risk.html": (body_risk(), "Risk register"),
        "projections.html": (body_projections(), "Projections"),
        "decision.html": (body_decision(), "Decision pathways"),
        "repo-review.html": (body_repo_review(), "Repository review"),
        "flagged.html": (body_flagged(), "Flagged for review"),
        "sources.html": (body_sources(), "Sources and method"),
    }
    for fn, title, lede, cat, srcs in CATEGORY_PAGES:
        bodies[fn] = (body_category(cat, title, lede, srcs), title)

    for fn, title, _num in PAGES:
        body, _ = bodies[fn]
        (OUT / fn).write_text(page(fn, title, body), encoding="utf-8")
    print(f"built {len(PAGES)} pages in {OUT}")


if __name__ == "__main__":
    build()
