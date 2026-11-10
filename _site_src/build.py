"""Build the published dashboard from the verified dataset.

Writes only the twelve published pages plus index.html. Nothing else in the
repository is touched. Every table row is rendered with its official source
link and status; unverified rows render blank cells, never numbers.
"""
from __future__ import annotations
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "_site_src"))
import dataset  # noqa: E402
import projection  # noqa: E402

E = html.escape
SNAPSHOT = dataset.SNAPSHOT
PROJ = projection.run()

NAV_GROUPS = {}
for p in dataset.PAGES:
    NAV_GROUPS.setdefault(p["group"], []).append(p)

STATUS_CLASS = {
    "Verified": "ok",
    "Verified · owner statement": "ok",
    "Derived": "der",
    "Analysis": "ana",
    "Unverified": "unv",
    "Unverified · withheld for privacy": "unv",
    "Unverified · not supplied": "unv",
    "Unverified · in the lease": "unv",
    "Unverified · owner records": "unv",
    "Unverified · not public": "unv",
    "Unverified · county roll": "unv",
    "Unverified · parcel-keyed": "unv",
    "Internal": "int",
}


def badge(status):
    cls = STATUS_CLASS.get(status, "ana")
    return f'<span class="badge {cls}">{E(status)}</span>'


def nav(current):
    out = []
    for group, pages in NAV_GROUPS.items():
        out.append(f'<div class="nav-group"><span class="nav-glabel">{E(group)}</span>')
        for p in pages:
            cur = ' aria-current="page"' if p["id"] == current else ""
            out.append(f'<a href="{p["id"]}.html"{cur}>{E(p["nav"])}</a>')
        out.append("</div>")
    return "".join(out)


def shell(page_id, title, description, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{E(description)}">
<title>{E(title)} · Asset A · Central Los Angeles net lease</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="app">
<aside class="sidebar">
  <a class="brand" href="index.html"><span class="dot">A</span><span>ASSET A<small>NET-LEASE DECISION FILE</small></span></a>
  <nav aria-label="Sections">{nav(page_id)}</nav>
  <div class="side-note">
    <b>Privacy by design.</b> No address, parcel, owner or account identifier is collected or published.
    <span class="snap">Evidence snapshot · {SNAPSHOT}</span>
  </div>
</aside>
<div class="content">
  <header class="topbar">
    <span class="crumb">ASSET A · CENTRAL LOS ANGELES · JACK IN THE BOX · NNN</span>
    <span class="stamp"><i></i> Verified {SNAPSHOT}</span>
  </header>
  <main id="main">
{body}
  </main>
  <footer class="foot">
    <p><b>Independent decision-support research.</b> Not an appraisal, a broker opinion of value, legal advice, or personalised
    financial, tax or investment advice. Values are a fixed snapshot taken on {SNAPSHOT}; rolling official releases change.</p>
    <p>Every table row carries the official page it was read from. Cells that could not be confirmed are blank and listed on
    <a href="flagged.html">Flagged for review</a>. <a href="methodology.html">Method</a> · <a href="privacy.html">Privacy</a> · <a href="sources.html">Sources</a></p>
  </footer>
</div>
</div>
</body>
</html>
"""


def table(page):
    heads = page["columns"] + ["Status", "Official source"]
    rows = []
    for r in page["rows"]:
        src = dataset.SOURCES.get(r["source"], getattr(dataset, "INTERNAL_SOURCE", {}))
        cells = []
        for i, c in enumerate(r["cells"]):
            if c == "":
                cells.append('<td class="blank" aria-label="Not verified; intentionally blank">—</td>')
            else:
                cells.append(f"<td>{E(c)}</td>")
        note = f'<div class="note">{E(r["note"])}</div>' if r.get("note") else ""
        link_url = r.get("url") or src["url"]
        link_label = src["host"] if not r.get("url") else src["host"]
        rows.append(
            "<tr>"
            + "".join(cells)
            + f"<td>{badge(r['status'])}</td>"
            + f'<td class="src"><a href="{E(link_url)}" target="_blank" rel="noopener noreferrer">{E(link_label)}</a>{note}</td>'
            + "</tr>"
        )
    head = "".join(f'<th scope="col">{E(h)}</th>' for h in heads)
    return (
        f'<div class="tablewrap"><table><caption>{E(page["title"])}</caption>'
        f"<thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"
    )


def page_body(page):
    legend = (
        '<div class="legend">'
        '<span class="badge ok">Verified</span> read on the named official page'
        '<span class="badge der">Derived</span> arithmetic on verified values'
        '<span class="badge ana">Analysis</span> this file\'s judgement'
        '<span class="badge unv">Unverified</span> blank, never estimated '
        '<span class="badge int">Internal</span> method, policy or declared model assumption'
        "</div>"
    )
    return (
        f'<div class="kicker">{E(page["kicker"])}</div>'
        f'<h1>{E(page["title"])}</h1>'
        f'<p class="lede">{E(page["description"])}</p>'
        f"{legend}{table(page)}"
    )


# ---------------------------------------------------------------- index page
counts = {"ok": 0, "der": 0, "ana": 0, "int": 0, "unv": 0}
for p in dataset.PAGES:
    for r in p["rows"]:
        counts[STATUS_CLASS.get(r["status"], "ana")] += 1
total_rows = sum(counts.values())


def kpi(label, value, sub, src_url, src_host):
    return (
        f'<article class="kpi"><span class="k">{E(label)}</span><strong>{E(value)}</strong>'
        f'<p>{E(sub)}</p><a href="{E(src_url)}" target="_blank" rel="noopener noreferrer">{E(src_host)}</a></article>'
    )


S = dataset.SOURCES
pathway_rows = []
for k in ("D", "A", "E", "C", "B"):
    s = PROJ["summary"][k]
    pathway_rows.append(
        f'<tr><td><b>{E(s["name"])}</b></td><td class="num">{s["floor"]:.2f}</td>'
        f'<td class="num">{s["expected"]:.2f}</td><td class="num">{s["ceiling"]:.2f}</td>'
        f'<td class="num">{s["mean_rank"]:.2f}</td>'
        f'<td class="src"><span class="badge int">Internal</span> <a href="valuation.html">model</a></td></tr>'
    )

index_body = f"""
<section class="hero">
  <div class="kicker">DECISION FILE · CENTRAL LOS ANGELES · NET LEASE</div>
  <h1>Sell, renew — or extend first and then sell?</h1>
  <p class="lede">A Jack in the Box net-leased restaurant in central Los Angeles, reported to expire between 2030 and 2035.
  This file reads only official sources, publishes the receipt for every number, and leaves blank what cannot be proved.</p>
  <div class="verdict">
    <span class="badge ana">CONDITIONAL RECOMMENDATION · ANALYST JUDGEMENT, NOT A VALUATION</span>
    <h2>Open renewal negotiations now. If the tenant will commit to ten years or more at market rent, sell the lengthened lease.
    If it will not, sell before expiry.</h2>
    <p>The only outcome to avoid is letting a 2030–2035 option clock run out with no written answer from the tenant. That route
    scores last on its worst case in the model on this site.</p>
    <div class="cta"><a class="btn" href="decision.html">See the five pathways</a>
    <a class="quiet" href="flagged.html">The {counts['unv']} items we could not verify →</a></div>
  </div>
</section>

<section>
  <h2 class="sec">The evidence in six numbers</h2>
  <div class="kpis">
    {kpi("Population · LA County", "9,694,934", "July 2025, down 3.2% from the 2020 estimates base", S["census_county"]["url"], "census.gov")}
    {kpi("Unemployment · LA metro", "4.4%", "September 2026, down from 5.5% a year earlier", S["bls_la"]["url"], "bls.gov")}
    {kpi("Tenant same-store sales", "−1.1%", "Q3 FY2026, system-wide; franchise −1.2%", S["sec_q3fy26"]["url"], "sec.gov")}
    {kpi("10-year Treasury", "4.86%", "2026-11-06; the risk-free anchor a buyer prices against", S["fred_dgs10"]["url"], "fred.stlouisfed.org")}
    {kpi("Earthquake M≥6.7 · 30 yrs", "60%", "Los Angeles region, USGS UCERF3 Table 1", S["usgs_ucerf3"]["url"], "pubs.usgs.gov")}
    {kpi("City transfer tax above $5.4m", "4.45%", "0.45% city base + 4.00% Measure ULA tier", S["ula"]["url"], "finance.lacity.gov")}
  </div>
</section>

<section>
  <h2 class="sec">The trade, in one paragraph</h2>
  <div class="split">
    <div>
      <h3>What the verified evidence says</h3>
      <p><b>The regional economy is flat, not collapsing.</b> Metro payrolls grew 0.5% year over year and unemployment fell a full
      point, but the county has 3.2% fewer residents than in 2020 and the state projects a further 1.5% decline by 2035.</p>
      <p><b>The tenant is shrinking deliberately.</b> Jack in the Box closed 17 restaurants in one quarter, guided to 50–60
      closures for the year, discontinued its dividend, and said the rest of a 150–200 unit closure programme would close at
      franchise-agreement termination dates. A 2030–2035 lease expiry is exactly that kind of date.</p>
      <p><b>The exit is taxed twice.</b> A City of Los Angeles sale above $5.4 million pays a 4.45% city transfer tax, and the gain
      is taxed federally and again in California, which gives capital gains no preferential rate.</p>
    </div>
    <div class="panel">
      <h3>What that implies for the decision</h3>
      <p>A net-lease buyer is paying for a contractual income stream. Its value comes from the term remaining, the credit behind it,
      and the rent. Extending the lease is the only action available to the owner that lengthens the stream without selling.</p>
      <p>Because the rent was never disclosed, this file does not assert a dollar value. It values every strategy in units of
      <b>R</b>, one year of current base rent, and ranks them on the worst case.</p>
      <a href="valuation.html">How the model works →</a>
    </div>
  </div>
</section>

<section>
  <h2 class="sec">Five pathways, scored on the downside</h2>
  <p class="sub">Values are present values in units of R. <b>Floor</b> is the pessimistic scenario — the number that matters when the
  objective is preserving wealth. Full assumptions are on the <a href="valuation.html">valuation model</a> page.</p>
  <div class="tablewrap">
    <table>
      <caption>Deterministic model, three scenarios, 2026–2036 horizon</caption>
      <thead><tr><th scope="col">Pathway</th><th scope="col" class="num">Floor (pessimistic)</th>
      <th scope="col" class="num">Expected</th><th scope="col" class="num">Ceiling (optimistic)</th>
      <th scope="col" class="num">Mean rank</th><th scope="col">Assumptions</th></tr></thead>
      <tbody>{''.join(pathway_rows)}</tbody>
    </table>
  </div>
  <p class="sub" style="margin-top:14px">Winner on the floor: <b>{E(PROJ['floor_winner'])}</b>. Winner on expected value:
  <b>{E(PROJ['expected_winner'])}</b>. Agreement between the two is why the recommendation is stable — but every input is an
  assumption, so read the <a href="flagged.html">flagged items</a> before acting.</p>
</section>

<section>
  <h2 class="sec">Risk balance</h2>
  <div class="split">
    <div>
      <h3 class="good">Business as usual</h3>
      <ul class="clean">
        <li><b>Income concentration.</b> One tenant, one building. Vacancy costs the full rent plus taxes, insurance and re-letting.</li>
        <li><b>Wage-floor pressure.</b> Fast-food work pays $20.00/hour under AB 1228; the city floor is $18.42 and the state floor $16.90.</li>
        <li><b>Rates.</b> A 10-year Treasury at 4.86% sets the floor under a buyer's required return. Higher yields mean lower prices.</li>
        <li><b>Taxes.</b> Measure ULA adds 4% of gross above $5.4 million, and the gain is taxed again at exit.</li>
      </ul>
    </div>
    <div>
      <h3 class="bad">Tail events</h3>
      <ul class="clean">
        <li><b>Earthquake.</b> USGS puts the Los Angeles region at 60% for M≥6.7 within 30 years and models a plausible M7.8 at ~1,800 deaths and $213 billion in losses.</li>
        <li><b>Wildfire.</b> Two January 2025 fires destroyed 16,264 structures in this county. Insurance availability, not the flame front, is the exposure for an urban pad.</li>
        <li><b>Flood and ground failure.</b> FEMA and CGS are the official maps; the parcel zone is unknown and left blank.</li>
        <li><b>Tenant failure.</b> The issuer's own plan closes stores and sells real estate. It is not a guarantee for this site.</li>
      </ul>
    </div>
  </div>
</section>

<section>
  <h2 class="sec">Read by category</h2>
  <div class="routes">
    {''.join(f'<a href="{p["id"]}.html"><b>{E(p["nav"])}</b><span>{E(p["kickcher"] if "kickcher" in p else p["kicker"])}</span></a>' for p in dataset.PAGES)}
  </div>
</section>

<section>
  <h2 class="sec">Evidence counts</h2>
  <div class="counts">
    <div><b>{total_rows}</b><span>table rows published</span></div>
    <div><b>{counts['ok']}</b><span>verified against an official page</span></div>
    <div><b>{counts['der']}</b><span>derived by shown arithmetic</span></div>
    <div><b>{counts['ana']}</b><span>labelled analysis</span></div>
    <div><b>{counts['int']}</b><span>internal method or assumption rows</span></div>
    <div><b>{counts['unv']}</b><span>left blank, flagged</span></div>
  </div>
</section>
"""

# ------------------------------------------------------------------- write
written = []
index_page = {"id": "index", "nav": "Overview"}
(ROOT / "index.html").write_text(shell("index", "Overview", "Decision dashboard for an anonymised Jack in the Box net lease in central Los Angeles.", index_body))
written.append("index.html")

for p in dataset.PAGES:
    body = page_body(p)
    (ROOT / f'{p["id"]}.html').write_text(shell(p["id"], p["title"], p["description"], body))
    written.append(f'{p["id"]}.html')

print(f"Wrote {len(written)} pages: {', '.join(written)}")
print(f"Rows: {total_rows} total · {counts['ok']} verified · {counts['der']} derived · "
      f"{counts['ana']} analysis · {counts['unv']} blank")
