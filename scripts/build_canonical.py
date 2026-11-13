#!/usr/bin/env python3
"""Build ONE canonical, privacy-safe GitHub Pages site from the verified register.

Outputs (all deterministic, all static HTML, no JavaScript, no external assets):

  data/canonical.json                    machine-readable evidence register
  research/VERIFICATION-2026-11-12-c56c569e.md    immutable 2026-11-12 line-by-line source verification log
  research/VERIFICATION-2026-11-12-f0b78eb6.md    hand-written 2026-11-12 re-verification log (session f0b78eb6; not generated)
  research/VERIFICATION-2026-11-10-b98090a0.md    earlier record, kept as committed (no longer rewritten)
  <root>/*.html                         every page in PAGES + flagged.html alias
  assets/style.css                      shared stylesheet

Every table body row carries an official source link.  Any value that could not be
confirmed from an official source is left as an EMPTY cell, labelled Unverified,
and published on the Flagged for Review page.

Run:  python3 scripts/build_canonical.py
"""
from __future__ import annotations

import html
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from data.canonical_rows import (  # noqa: E402
    SNAPSHOT, SOURCES, CATEGORIES, ROWS, RISKS, DECISIONS, PROJECTION, FLAGS, REPO_REVIEW,
    DECISION_RISKS, INFO_REGISTER, SUGGESTIONS, SUGGESTION_PATHS,
)

E = html.escape

# (id, title, group, kicker, description)
PAGES = [
    ("index", "Overview", "OVERVIEW", "ASSET A · CENTRAL LOS ANGELES · NET-LEASE DECISION FILE",
     "The decision at a glance, the evidence behind it, and the whole register in one place."),
    ("executive-summary", "Executive summary", "OVERVIEW", "01 / EXECUTIVE SUMMARY",
     "Recommendation, findings, decision matrix, risk balance, and everything that stays blank."),
    ("master", "All entries & findings", "OVERVIEW", "02 / MASTER REGISTER",
     "Every published row in one table, grouped by category, with its official source."),
    ("geography", "Geography", "EVIDENCE BY CATEGORY", "03 / GEOGRAPHY",
     "Where the asset sits, and what cannot be established without a parcel."),
    ("demographics", "People & income", "EVIDENCE BY CATEGORY", "04 / PEOPLE & INCOME",
     "Population, households, income, poverty, education and spending capacity."),
    ("economy", "Economy & jobs", "EVIDENCE BY CATEGORY", "05 / ECONOMY & JOBS",
     "Employment, wages, prices, output, interest rates and official long-range forecasts."),
    ("schools", "Schools", "EVIDENCE BY CATEGORY", "06 / SCHOOLS",
     "District scale, graduation outcomes and the attendance-boundary gap."),
    ("tenant", "Tenant & lease", "EVIDENCE BY CATEGORY", "07 / TENANT & LEASE",
     "What the issuer's own SEC filings disclose, and what the executed lease would add."),
    ("taxes", "Taxes & transfer", "EVIDENCE BY CATEGORY", "08 / TAXES & TRANSFER",
     "Proposition 13, transfer taxes, Measure ULA, capital gains and §1031."),
    ("hazards", "Hazards", "EVIDENCE BY CATEGORY", "09 / HAZARDS",
     "Earthquake, wildfire and flood: the official observations and scenarios."),
    ("risk", "Risk register", "ANALYSIS", "10 / RISK REGISTER",
     "Every business-as-usual and black-swan risk considered, with its context source."),
    ("projections", "Projection system", "ANALYSIS", "11 / PROJECTION SYSTEM",
     "A reliable, reproducible framework for the area, and the outputs deliberately withheld."),
    ("anchors", "Projection anchors", "ANALYSIS", "11A / PROJECTION ANCHORS",
     "The dated official observations and long-range projections that may bound a model."),
    ("questions", "Questions & answers", "ANALYSIS", "12 / QUESTIONS & ANSWERS",
     "What must be answered before deciding: what is known, what is not, and how to find out."),
    ("decisions", "Decision matrix", "ANALYSIS", "13 / DECISION MATRIX",
     "Every available pathway, its risks, its evidence gate and the recommended sequence."),
    ("model", "Model & method", "ANALYSIS", "14 / MODEL & METHOD",
     "Verification standard, arithmetic, monitoring rules and the limits of the analysis."),
    ("place", "Evidence boundary", "ANALYSIS", "15 / EVIDENCE BOUNDARY",
     "What this site deliberately does not assert about the subject property."),
    ("suggestions", "Suggestions to review", "GOVERNANCE", "16 / SUGGESTIONS",
     "Proposed improvements to this site, with options to choose from. Nothing here has been built."),
    ("review", "Flagged for Review", "GOVERNANCE", "17 / FLAGGED FOR REVIEW",
     "Every unverified value, conflict and irregularity, published for manual review after the site is live."),
    ("repo-review", "Repo review", "GOVERNANCE", "18 / REPO REVIEW",
     "Line-by-line findings from the inherited repository layers, with source links."),
    ("sources", "Sources & method", "GOVERNANCE", "19 / SOURCES & METHOD",
     "The official source register, the verification standard and the privacy boundary."),
]
PAGE_TITLES = {p[0]: p[1] for p in PAGES}
# One list owns the page numbers; page functions read them from here.
KICKER = {p[0]: p[3] for p in PAGES}
VERIFICATION_FILE = "research/VERIFICATION-2026-11-12-c56c569e.md"
STATUS_CLASS = {"Verified": "ok", "Derived": "derived", "Analysis": "analysis", "Blank": "blank"}
STATUS_LABEL = {"Verified": "Verified", "Derived": "Derived", "Analysis": "Analysis", "Blank": "Unverified"}


def src(key: str, label: str | None = None) -> str:
    s = SOURCES[key]
    text = E(label or s[0])
    return (f'<a class="srclink" href="{E(s[2])}" target="_blank" rel="noopener noreferrer" '
            f'title="{E(s[1])} — {E(s[0])}">{text} ↗</a>')


def badge(status: str) -> str:
    return f'<span class="badge {STATUS_CLASS[status]}">{E(STATUS_LABEL[status])}</span>'


def table(headers: list[str], body_rows: list[list[str]], caption: str, cls: str = "data") -> str:
    out = [f'<div class="table-wrap"><table class="{cls}"><caption>{E(caption)}</caption><thead><tr>']
    out += [f'<th scope="col">{E(h)}</th>' for h in headers]
    out.append('</tr></thead><tbody>')
    for row in body_rows:
        out.append('<tr>')
        out += [f'<td>{c}</td>' for c in row]
        out.append('</tr>')
    out.append('</tbody></table></div>')
    return ''.join(out)


def evidence_table(rows: list[dict], caption: str) -> str:
    body = []
    for r in rows:
        if r["status"] == "Blank":
            value = '<span class="empty" aria-label="Unverified value; intentionally blank"></span>'
        else:
            value = E(r["value"])
        body.append([
            E(r["indicator"]), value, E(r["scope"]), E(r["note"]),
            badge(r["status"]), src(r["source"]),
        ])
    return table(["Indicator", "Value", "Geography · period", "Decision relevance / note", "Status", "Official source"],
                 body, caption)


def shell(page_id: str, content: str, kicker: str = "", description: str = "") -> str:
    groups: list[tuple[str, list[tuple[str, str]]]] = []
    for pid, title, group, _k, _d in PAGES:
        if not groups or groups[-1][0] != group:
            groups.append((group, []))
        groups[-1][1].append((pid, title))
    nav_parts = []
    for group, items in groups:
        nav_parts.append(f'<div class="nav-label">{E(group)}</div>')
        for pid, title in items:
            cur = ' aria-current="page"' if pid == page_id else ''
            nav_parts.append(f'<a{cur} href="{pid}.html">{E(title)}</a>')
    nav = ''.join(nav_parts)
    desc = description or PAGE_TITLES[page_id]
    title = PAGE_TITLES[page_id]
    # Empty layout disables GitHub Pages' default theme wrapper and keeps the
    # published bytes identical to this generator's output after Jekyll strips
    # the front matter.  scripts/stage_pages.py strips the same front matter.
    return '''---
layout: null
---
''' + f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{E(desc)}">
<title>{E(title)} · Asset A decision desk</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="app">
<aside class="sidebar">
  <a class="brand" href="index.html"><span class="mark">A.</span><span><b>ASSET A</b><small>NET-LEASE DECISION DESK</small></span></a>
  <nav aria-label="Site navigation">{nav}</nav>
  <div class="privacy"><b>◈ Privacy by design</b><p>Asset A · Owner A · placeholders only.<br>No address, parcel, owner, account or lease identifier is published.<br><br>Evidence snapshot {E(SNAPSHOT)}.</p></div>
</aside>
<div class="main">
  <header class="topbar"><span>RESEARCH / LOS ANGELES / NET LEASE</span><span class="stamp">● Evidence snapshot · {E(SNAPSHOT)}</span></header>
  <main id="main">
    {f'<div class="eyebrow">{E(kicker)}</div>' if kicker else ''}
    {content}
  </main>
  <footer>Independent decision-support research, not an appraisal, legal opinion or personalised financial advice.<br>Static evidence snapshot · No forms, tracking, third-party assets or private documents · <a href="sources.html">Methodology &amp; limitations</a> · <a href="review.html">Flagged for Review</a></footer>
</div>
</div>
</body>
</html>
'''


def h1(title: str, lede: str) -> str:
    return f'<h1>{E(title)}</h1><p class="lede">{E(lede)}</p>'


def h2(title: str, note: str = "") -> str:
    n = f'<span>{E(note)}</span>' if note else ''
    return f'<div class="section-heading"><h2>{E(title)}</h2>{n}</div>'


CALLOUT_BOUNDARY = (
    '<section class="callout"><b>Evidence boundary.</b> Asset A is anonymised: no address, parcel, '
    'owner, account or executed lease is published. No valuation, cap rate, sale price or renewal '
    'probability is asserted. Regional evidence is context, not a forecast of this site. '
    '<a href="review.html">Flagged for Review</a> · <a href="sources.html">Verification standard</a>.</section>'
)


# --------------------------------------------------------------------------- pages
def page_index() -> str:
    counts = Counter(r["status"] for r in ROWS)
    cards = [
        ("LA COUNTY · JUL 2025", "9,694,934", "Census V2025 population · 3.2% below the 2020 estimates base", "COUNTY", "Census QuickFacts"),
        ("LA METRO · SEP 2026", "4.4%", "Unemployment · down from 5.5% a year earlier", "BLS", "BLS economic summary"),
        ("LA METRO · SEP 2026", "+0.5%", "Nonfarm payroll growth · 6,282.1 thousand jobs", "BLS", "BLS economic summary"),
        ("ISSUER · Q3 FY2026", "-1.1%", "System same-store sales · 2,115 restaurants", "SECQ3", "SEC 8-K Exhibit 99.1"),
        ("US · 2026-11-12", "5.10%", "10-year Treasury · dated reference, not a required return", "FRED", "FRED DGS10"),
        ("LA REGION · UCERF3", "60%", "30-year M≥6.7 likelihood from 2014, not parcel loss", "UCERF3", "USGS Fact Sheet 2015-3009"),
    ]
    card_html = ''.join(
        f'<article><div class="eyebrow">{E(k)}</div><strong>{E(v)}</strong><p>{E(d)}</p>{src(s, l)}</article>'
        for k, v, d, s, l in cards
    )
    cat_cards = ''.join(
        f'<a href="{E(slug)}.html"><b>{E(title)}</b><p>{E(desc)}</p><span>Read the evidence →</span></a>'
        for title, slug, desc in CATEGORIES
    )
    gate_links = ''.join(
        f'<a href="{pid}.html"><b>{E(PAGE_TITLES[pid])}</b><p>{E(t)}</p><span>Open →</span></a>'
        for pid, t in [
            ("risk", "Business-as-usual and black-swan risks, each with a context source."),
            ("projections", "The reproducible 2026-2035 framework and the outputs withheld."),
            ("decisions", "Eight pathways, their gates, the risk of each and the recommended sequence."),
            ("questions", "What must be answered before deciding, what is known and how to find the rest."),
            ("suggestions", "Proposed site improvements with options to choose from; nothing is built yet."),
            ("master", "Every row in this site, in one source-linked table."),
            ("review", "Unverified values, conflicts and irregularities for manual review."),
            ("repo-review", "Line-by-line findings on the inherited repository layers."),
        ]
    )
    body = [
        CALLOUT_BOUNDARY,
        '<div class="eyebrow">ASSET A · CENTRAL LOS ANGELES · NET-LEASE DECISION FILE</div>',
        '<h1>Protect the income.<br><span>Own the exit.</span></h1>',
        '<p class="lede">A source-linked decision desk for one anonymised Jack in the Box net-leased '
        'property in the Los Angeles area with a lease expiry reported somewhere in 2030 to 2035. '
        'Every published figure is traceable to a government or issuer page; everything that could not '
        'be verified is left blank and listed on the Flagged for Review page.</p>',
        '<section class="hero-note"><span class="badge analysis">CONDITIONAL RECOMMENDATION · ANALYST JUDGEMENT, NOT A VALUATION</span>'
        '<h2>Prepare both options now; choose only when the evidence supports a decision.</h2>'
        '<p>Privately establish the lease dates and options now, then seek sale and renewal terms on a timeline '
        'consistent with those rights. Compare documented after-tax proceeds with the risk-adjusted hold case. '
        'The reported 2030–2035 range does not establish a deadline or a suitable decision for the owner.</p>'
        '<a class="button" href="decisions.html">Decision matrix &amp; triggers <span>→</span></a> '
        '<a class="quiet" href="executive-summary.html">Read the executive summary ↗</a></section>',
        h2("Six verified anchors", "Regional context ≠ property forecast"),
        f'<div class="cards">{card_html}</div>',
        h2("Why now rather than at expiry", "The balance of verified evidence"),
        '<section class="split"><div><h3>What supports holding</h3><ul class="ticks good">'
        '<li>Unemployment fell to 4.4% in the metro and 4.5% in the city and county. ' + src("BLS", "BLS") + '</li>'
        '<li>Education and health services, the largest metro sector at 1,340.7 thousand jobs, grew 3.8%. ' + src("BLS", "BLS") + '</li>'
        '<li>Median household income is $81,939 in the city and $90,112 in the county. ' + src("CITY", "Census") + '</li>'
        '<li>Property tax assessment rules may favor holding; the actual assessed value and future changes are unknown. ' + src("ASSESSOR", "Assessor") + '</li>'
        '</ul></div><div><h3>What argues for acting early</h3><ul class="ticks bad">'
        '<li>City population is 0.8% below its 2020 estimates base; the county is 3.2% below. ' + src("COUNTY", "Census") + '</li>'
        '<li>The issuer reports −1.1% system same-store sales, 17 quarterly closures and FY2026 guidance of 50–60 closures. ' + src("SECQ3", "SEC") + '</li>'
        '<li>CPI-U is +3.7% and the employment cost index +3.9%; a fixed escalator may not keep pace. ' + src("BLS", "BLS") + '</li>'
        '<li>A City of LA sale above $5.4m can add a 4% ULA surcharge. ' + src("ULA", "City Finance") + '</li>'
        '</ul></div></section>',
        h2("Risk balance", "Business as usual, then the tail"),
        '<section class="split"><div><h3>Business as usual</h3>'
        '<p><b>Income concentration.</b> One tenant, one building, one lease. Vacancy removes the full rent '
        'while taxes, insurance and re-letting costs continue.</p>'
        '<p><b>Wage and cost pressure.</b> Covered fast-food work has a $20.00/hour floor; the City of LA '
        'general floor is $18.42/hour from 2026-07-01, and the state floor is $16.90/hour from 2026. '
        'Store-level rent coverage is unknown.</p>'
        '<p><b>Rates and exit yields.</b> A higher exit yield lowers price for the same rent.</p>'
        '<p><b>Taxes.</b> A qualifying §1031 exchange generally defers gain; eligibility and eventual tax depend on the facts.</p>'
        '<a class="quiet" href="risk.html">Full risk register →</a></div><div><h3>Tail events that can end the local economy</h3>'
        '<p><b>Wildfire.</b> In January 2025 the Palisades and Eaton fires destroyed 16,264 structures in this '
        'county in 24 days. Insurance availability and pricing can change region-wide afterwards.</p>'
        '<p><b>Earthquake.</b> USGS models a plausible M7.8 southern San Andreas event at about 1,800 deaths '
        'and $213bn in regional losses. Parcel-level ground-failure exposure has not been checked.</p>'
        '<p><b>Flood, correlated utility or pandemic disruption.</b> No parcel zone or probability is assigned.</p>'
        '<p><b>Tenant failure or accelerated closure.</b> The issuer closes underperforming units and sells '
        'owned real estate; a chain lease is not permanent.</p>'
        '<a class="quiet" href="hazards.html">Official hazard evidence →</a></div></section>',
        h2("Read by category", f"{len(CATEGORIES)} evidence categories · every row carries its source"),
        f'<div class="route-grid">{cat_cards}</div>',
        h2("Analysis & governance", "One navigation, one dataset, one verification standard"),
        f'<div class="route-grid">{gate_links}</div>',
        h2("What is published", f"{len(ROWS)} evidence rows · {len(SOURCES)} official sources"),
        '<div class="stats"><div><strong>' + str(len(ROWS)) + '</strong><span>Evidence rows</span></div>'
        '<div><strong>' + str(counts["Verified"]) + '</strong><span>Verified observations</span></div>'
        '<div><strong>' + str(counts["Derived"]) + '</strong><span>Derived (arithmetic shown)</span></div>'
        '<div><strong>' + str(counts["Analysis"]) + '</strong><span>Analysis rows</span></div>'
        '<div><strong>' + str(counts["Blank"]) + '</strong><span>Blank / unverified</span></div>'
        '<div><strong>' + str(len(SOURCES)) + '</strong><span>Official sources</span></div></div>',
    ]
    return shell("index", ''.join(body), description="Privacy-safe, source-linked Los Angeles net-lease decision dashboard.")


def page_executive_summary() -> str:
    findings = [
        ("1", "Lease clock, not market clock", "The reported 2030–2035 expiry is a range, not a verified date. Shortening term may affect leverage; this is an analytical risk, not an issuer disclosure.", "SECQ3"),
        ("2", "Demand is soft at regional scale", "City population is 0.8% below its 2020 estimates base; county is 3.2% below; a separate state estimate shows a −0.45% county year-over-year decline.", "DOF"),
        ("3", "Labour market is improving but uneven", "Metro unemployment fell to 4.4% and payrolls rose 0.5%, led by education and health (+3.8%) while information fell 5.7%.", "BLS"),
        ("4", "Tenant credit is the key unknown", "The issuer reports −1.1% same-store sales, 17 quarterly closures, a discontinued dividend and a $500m refinancing. The legal obligor at this site is unknown.", "SECQ3"),
        ("5", "Costs and rates compress real returns", "CPI-U +3.7%, ECI +3.9%, energy +20.3%, and a 5.10% 10-year Treasury observation on 2026-11-12. This dated reference is not a property return hurdle.", "FRED"),
        ("6", "Tail risk is real but unquantified", "USGS ShakeOut models ~1,800 deaths and $213bn in losses; the 2025 fires destroyed 16,264 structures. This is regional context, not a parcel forecast.", "UCERF3"),
    ]
    # Multi-source findings need links for every distinct published observation.
    finding_sources = {"2": ("DOF", "CITY", "COUNTY"), "5": ("BLS", "FRED"),
                       "6": ("SHAKEOUT", "PALISADES", "EATON")}
    frows = [[f'<b>{E(n)}</b>', E(t), E(d),
              ' · '.join(src(key) for key in finding_sources.get(n, (source,)))]
             for n, t, d, source in findings]
    drows = [[E(a), E(b), E(c), E(d), src(s)] for a, b, c, d, s in DECISIONS]
    gate_rows = [
        ["<b>Signed extension</b>", "Compare enforceable term, rent, credit, concessions and expenses against other options; no fixed minimum is established.", src("SECQ3")],
        ["<b>Verified after-tax bid</b>", "A documented offer that beats the risk-adjusted hold case after all transfer taxes and costs.", src("ULA")],
        ["<b>Block-level growth evidence</b>", "Trade-area population, traffic and competitive supply, not city or county averages.", src("CITY")],
        ["<b>Change in owner liquidity needs</b>", "Private to Owner A; deliberately unavailable on this public site.", src("IRS1031")],
    ]
    body = [
        CALLOUT_BOUNDARY,
        h1("Executive summary", "The decision, the evidence behind it, the risks of every route, and the limits of what public data can establish."),
        '<section class="hero-note"><span class="badge analysis">BASE CASE · CONDITIONAL RECOMMENDATION</span>'
        '<h2>Prepare both tracks; do not choose sale or renewal on regional averages alone.</h2>'
        '<p>Privately verify the lease and notice dates now, explore sale interest and written renewal terms, and '
        'compare after-tax outcomes, downside risks and owner needs. Marketing timing and extension length '
        'depend on the facts; neither is established by a public source. This is a provisional process, not a valuation.</p></section>',
        h2("Six findings that drive the decision", "Each links to its official publisher"),
        table(["#", "Finding", "What the official evidence says", "Official source"], frows,
              "Findings F1–F6 · evidence-linked"),
        h2("The decision matrix", "Every available pathway and its dominant risk"),
        table(["Pathway", "When it may be preferable", "Main risks / gate", "Evidence required", "Official source"],
              drows, "Eight pathways · no option is scored with invented weights"),
        h2("What would change this view", "Four evidence gates"),
        table(["Gate", "What must be true", "Official context"], gate_rows, "Evidence gates"),
        h2("Risk balance for wealth preservation", "Manageable risk, not zero risk"),
        '<section class="split"><div><h3>Concentration can be a major risk</h3>'
        '<p>A single-tenant net lease looks safe until the term ends. Holding to expiry concentrates '
        'tenant credit, lease-rollover, rate and catastrophe risk into one short window. Selling early '
        'spreads the decision across several years and converts an illiquid single asset into a choice.</p>'
        '<p>The cost of acting early is real: transfer taxes, a possible 4% ULA surcharge, capital-gain tax '
        'and reinvestment risk. Those are computable from published rules once the owner\'s figures exist.</p>'
        + src("ULA", "City of LA transfer-tax rules") + '</div><div><h3>Why not simply renew</h3>'
        '<p>Assess renewal term, rent, concessions and obligor credit together against sale and re-letting alternatives. '
        'The issuer\'s chain-wide results cannot establish this lease or tenant. An extension may change '
        'sale flexibility and bids; neither effect is guaranteed.</p>'
        '<p>Black-swan exposure is not diversified by renewing: the same parcel keeps the same '
        'earthquake, wildfire and flood exposure. Insurance verification and a concentration cap on '
        'net worth are required under either route.</p>'
        + src("UCERF3", "USGS UCERF3") + '</div></section>',
        h2("What stays blank", "Published on the Flagged for Review page"),
        '<p>The executed lease, exact expiry, rent, escalations, options, guarantor, store sales, basis, '
        'debt, owner tax rates, parcel identifiers, hazard overlays and insurance terms are all unverified. '
        '<b>No numerical sale price, cap rate, 2030–2035 value or renewal probability is published.</b> '
        'Any figure produced without those inputs would be an artefact of an assumption, not evidence.</p>'
        '<a class="button" href="review.html">Flagged for Review <span>→</span></a> '
        '<a class="quiet" href="master.html">All entries &amp; findings ↗</a>',
        h2("What to do next", "Three pages to read after this one"),
        '<section class="split"><div><h3>Answer the gate questions</h3>'
        f'<p>{sum(1 for q in INFO_REGISTER if q[1] == "Gate")} of the {len(INFO_REGISTER)} questions in the information register '
        'must be answered before any route can be chosen. Almost all are answered by documents the owner '
        'already holds or by an adviser, not by more public data.</p>'
        '<a class="quiet" href="questions.html">Questions &amp; answers →</a></div>'
        '<div><h3>Choose how the site should develop</h3>'
        f'<p>{len(SUGGESTIONS)} proposed improvements are listed with the options for each and four ways to combine them. '
        'None has been built; each waits for a choice.</p>'
        '<a class="quiet" href="suggestions.html">Suggestions →</a></div></section>',
    ]
    return shell("executive-summary", ''.join(body), KICKER["executive-summary"])


def page_master() -> str:
    jumps = ''.join(
        f'<a class="chip" href="#cat-{i}">{E(title)}</a>' for i, (title, _s, _d) in enumerate(CATEGORIES)
    )
    parts = [CALLOUT_BOUNDARY, h1("All entries & findings",
             "Every row published on this site, grouped by category. Blank cells are unverified values, never estimates."),
             f'<div class="chips">{jumps}</div>']
    for i, (title, slug, desc) in enumerate(CATEGORIES):
        rows = [r for r in ROWS if r["category"] == title]
        parts.append(f'<h2 id="cat-{i}" class="cat-head">{E(title)} <span>{len(rows)} rows</span> '
                     f'<a href="{E(slug)}.html">Open category page →</a></h2>')
        parts.append(f'<p class="small">{E(desc)}</p>')
        parts.append(evidence_table(rows, f"{title} · complete evidence register"))
    parts.append(h2("Structured registers", "Risks, pathways, method and review items"))
    parts.append('<div class="route-grid">'
                 '<a href="risk.html"><b>Risk register</b><p>Business-as-usual and black-swan risks.</p><span>Open →</span></a>'
                 '<a href="decisions.html"><b>Decision matrix</b><p>All eight pathways and their gates.</p><span>Open →</span></a>'
                 '<a href="projections.html"><b>Projection system</b><p>13 method steps with sources.</p><span>Open →</span></a>'
                 '<a href="review.html"><b>Flagged for Review</b><p>Unverified items and irregularities.</p><span>Open →</span></a>'
                 '<a href="repo-review.html"><b>Repo review</b><p>Line-by-line inherited-layer findings.</p><span>Open →</span></a>'
                 '<a href="sources.html"><b>Sources & method</b><p>Official source register.</p><span>Open →</span></a></div>')
    return shell("master", ''.join(parts), KICKER["master"])


def page_category(slug: str) -> str:
    title, _slug, desc = next(c for c in CATEGORIES if c[1] == slug)
    rows = [r for r in ROWS if r["category"] == title]
    idx = [p for p in PAGES if p[0] == slug][0]
    counts = Counter(r["status"] for r in rows)
    body = [CALLOUT_BOUNDARY, h1(title, desc),
            '<div class="stats compact"><div><strong>' + str(len(rows)) + '</strong><span>Rows</span></div>'
            '<div><strong>' + str(counts["Verified"]) + '</strong><span>Verified</span></div>'
            '<div><strong>' + str(counts["Derived"]) + '</strong><span>Derived</span></div>'
            '<div><strong>' + str(counts["Analysis"]) + '</strong><span>Analysis</span></div>'
            '<div><strong>' + str(counts["Blank"]) + '</strong><span>Unverified / blank</span></div></div>',
            evidence_table(rows, f"{title} · evidence register")]
    body.append('<p class="small">Legend — <b>Verified</b>: the publisher states this observation. '
                '<b>Derived</b>: arithmetic on two published observations, with the arithmetic shown. '
                '<b>Analysis</b>: conditional reasoning, not an official observation. '
                '<b>Unverified</b>: the value cell is empty; see <a href="review.html">Flagged for Review</a>.</p>')
    body.append('<a class="quiet" href="master.html">Back to all entries →</a>')
    return shell(slug, ''.join(body), idx[3])


def page_risk() -> str:
    bau = [r for r in RISKS if r[0] == "Business as usual"]
    bs = [r for r in RISKS if r[0] == "Black swan"]
    def rows(rs):
        return [[E(t), f'<span class="sev {E(s.lower())}">{E(s)}</span>', E(r), E(x), E(m), src(k)]
                for t, s, r, x, m, k in rs]
    hdr = ["Type", "Severity", "Risk", "Exposure / verified context", "Mitigation or decision test", "Official context source"]
    body = [CALLOUT_BOUNDARY,
            h1("Risk register", "Every decision considered on this site is tested against these risks. "
               "The source column supports context, not a probability or a parcel-level loss estimate."),
            h2("Business-as-usual risks", f"{len(bau)} risks"),
            table(hdr, rows(bau), "Business-as-usual risk register"),
            h2("Black-swan and correlated risks", f"{len(bs)} tail events"),
            table(hdr, rows(bs), "Black-swan risk register"),
            '<section class="callout"><b>No invented probabilities.</b> USGS and CAL FIRE publish regional '
            'likelihoods and observed severity; no official source publishes a probability that this specific '
            'building is lost. Every such cell is blank on the '
            '<a href="review.html">Flagged for Review</a> page.</section>',
            h2("Risk by decision", "The same risks, sorted by the route that carries them"),
            table(["Pathway", "Business-as-usual risks", "Black-swan exposure", "What limits the damage",
                   "Official context source"],
                  [[f'<b>{E(a)}</b>', E(b), E(c), E(d), src(k)] for a, b, c, d, k in DECISION_RISKS],
                  "Risk of every pathway · business as usual and black swan"),
            '<a class="quiet" href="decisions.html">Decision matrix and recommended sequence →</a>',
            h2("Risk-balanced conclusion", "Wealth preservation with growth optionality"),
            '<p>The lowest-risk route is the one that keeps a choice available: market while contractual income '
            'is still in place, require written renewal terms, and cap how much of Owner A\'s net worth this '
            'single asset represents. Insurance verification and a re-letting reserve are prerequisites for '
            '<em>either</em> route. Redevelopment and a pure wait-until-expiry strategy carry the widest '
            'dispersion of outcomes and are not the default.</p>']
    return shell("risk", ''.join(body), KICKER["risk"])


def page_projections() -> str:
    prows = [[E(a), E(b), E(c), src(k)] for a, b, c, k in PROJECTION]
    anchors = [r for r in ROWS if r["category"] == "Projection anchors"]
    body = [CALLOUT_BOUNDARY,
            h1("Projection system", "A proposed framework for the area — and a strict refusal "
               "to publish a property value that no official source can support."),
            h2("How the framework works", f"{len(PROJECTION)} steps, each tied to an official source"),
            table(["Step", "What it does", "Why it is reliable / what is withheld", "Official source"],
                  prows, "Projection and validation method"),
            h2("Verified anchors and withheld outputs", "Every row is source-linked"),
            evidence_table(anchors, "Projection anchors · observations, official forecasts and gaps"),
            h2("Why there is no 2030–2035 number", "The calibration problem"),
            '<section class="split"><div><h3>What a model would need</h3><p>Executed rent through the verified '
            'term, unreimbursed expenses, debt, renewal options, the legal obligor, a market cap rate, '
            'insurance terms and owner tax rates. None of these are public records held here.</p>'
            '<p>Compounding a 2020–2025 population change forward to 2035 would assume the driver persists — '
            'something no official release asserts. The result would be an artefact of the rule.</p>'
            + src("DOF", "CA DOF estimates") + '</div><div><h3>What is defensible instead</h3>'
            '<p>Dated observations, official long-range regional projections with their stated uncertainty, '
            'published statutory rates, and scenario stress tests that need no invented probabilities.</p>'
            '<p>A future implementation would still require private documents, model design, testing and a documented after-tax comparison '
            'before it could be relied upon. This is a research framework, not a calibrated or back-tested forecasting system.</p>'
            + src("SCAG", "SCAG adopted forecast") + '</div></section>',
            h2("Official long-range context", "Planning forecasts, not property forecasts"),
            '<p>SCAG\'s adopted Connect SoCal 2024 forecast projects six-county employment from 8,937 thousand '
            'in 2022 to 10,276 thousand in 2050 (+0.50% per year) and accommodation and food service jobs from '
            '832 thousand to 938 thousand (+12.8%). It also states that the region\'s population has declined '
            'since a January 2019 peak. These are statutory planning projections with explicit uncertainty; they '
            'are not a central-LA parcel forecast and are not mixed with Census V2025 estimates.</p>']
    return shell("projections", ''.join(body), KICKER["projections"])


def page_questions() -> str:
    rows = [
        ("What is the best current course?", "Run confidential sale market testing and a written renewal track in parallel; choose only after comparing actual after-tax bids with enforceable terms.", "Actual bids, tenant proposal, tax review and executed lease.", "Preserves both exit and extension options; analyst judgment, not a valuation.", "IRS1031"),
        ("When should sale marketing begin?", "Verify notice dates now; 24–36 months before expiry is an illustrative planning window, not a verified deadline. Start earlier if the documents or market warrant.", "Executed lease, amendments, options and notice calendar; reconcile the reported 2030–2035 range.", "Avoids marketing into shortening-term or vacancy risk.", "SECQ3"),
        ("Should the property simply be sold now?", "Not on regional data alone. Sell when a documented after-tax bid beats the risk-adjusted hold and reinvestment cases.", "Independent bids, closing costs, debt payoff, tax basis and replacement plan.", "No optimal sale year or price is established.", "IRS1031"),
        ("When is renewal preferable?", "Compare an enforceable extension, including term, credit, rent, concessions and expenses, with the sale and hold alternatives. No minimum term is established.", "Signed amendment, legal obligor, guaranty, tenant financials, rent coverage and concessions.", "A verbal intention or franchise agreement is not a lease extension.", "SECQ3"),
        ("Is holding unchanged to expiry acceptable?", "No, unless contractual income, reserves, insurance and a costed re-letting plan independently support it.", "Carrying-cost budget, vacancy/default stresses, capital plan and alternate demand.", "Avoids silently accepting expiry and concentration risk.", "SECQ3"),
        ("Could renewing first and then selling help?", "Potentially, if signed terms improve real bids enough to cover concessions and transaction costs.", "Compare as-is bids with extension bids; do not assume cap-rate compression.", "Evidence-gated alternative, not a guaranteed win.", "IRS1031"),
        ("When does re-tenanting or redevelopment make sense?", "Only if documented alternate demand and a costed, permitted plan beat existing-use and sale alternatives.", "ZIMAS/title review, entitlements, environmental/engineering work, budget and tenant interest.", "Higher-risk fallback, not the default wealth-preservation route.", "ZIMAS"),
        ("What does the regional economy establish?", "Population is below 2020 estimates bases and payroll growth is modest. SCAG is a separate planning case, not a parcel forecast.", "Define a trade area; obtain official tract/block-group histories with consistent vintages.", "Supports caution, not a mechanical 2030–2035 value forecast.", "BLS"),
        ("Which sale-cost rules are known?", "City/county transfer taxes, possible Measure ULA, capital-gain rules and §1031 deferral can materially change net proceeds.", "Confirm jurisdiction, price, liens, closing date, basis, holding purpose and owner-specific treatment.", "Compare after-tax proceeds; ULA applies to gross value.", "ULA"),
        ("Can §1031 remove tax and risk?", "Qualifying exchanges generally defer recognition; they do not automatically eliminate eventual tax or replacement-asset and concentration risks.", "Tax/legal review, qualified intermediary process and verified replacement options before closing.", "Underwrite every replacement independently.", "IRS1031"),
        ("How should catastrophe risks be handled?", "Use parcel overlays, engineering and actual policy terms; stress interrupted rent, uninsured cost and an illiquid exit together.", "CGS/CAL FIRE/FEMA checks, structural/geotechnical review, deductibles, exclusions and rent-loss cover.", "Do not infer safety from a city label or invent disaster probabilities.", "EQZAPP"),
        ("Which owner facts prevent a final suitability decision?", "", "Liquidity, concentration, tax position, debt, horizon and loss tolerance remain private. Keep them in secure offline adviser review.", "No personalized allocation or loss-capacity conclusion can be made publicly.", "IRS1031"),
        ("Which exact lease facts are missing?", "", "Executed lease/amendments: expiry, notice dates, options, rent, escalations, expenses, casualty, roof/structure and assignment rights.", "The reported 2030–2035 range and NNN label are not enough.", "SECQ3"),
        ("Which property and tenant facts are missing?", "", "Legal tenant/guarantor, store sales/rent coverage, arrears, estoppel, rent roll, debt, tax bill, title, zoning, traffic and pipeline.", "These gaps block a reliable value, closure probability and renewal forecast.", "SECQ3"),
        ("How should missing public-area evidence be discovered?", "", "Use Census tract/block-group downloads with margins of error; ZIMAS; CDE campus records; effective hazard maps; lawful public-agency requests.", "Do not substitute commercial estimates or nearby averages.", "CITY"),
        ("What evidence would change the recommendation?", "A signed market-rent extension with acceptable credit; a superior after-tax bid; demonstrated trade-area growth; or changed liquidity needs.", "Re-run the same after-tax and downside comparison when any gate changes.", "Keeps the decision conditional and falsifiable.", "BLS"),
    ]
    body = []
    for q, answer, needed, consequence, source in rows:
        value = E(answer) if answer else '<span class="empty" aria-label="Unverified value; intentionally blank"></span>'
        body.append([E(q), value, E(needed), E(consequence), badge("Analysis" if answer else "Blank"), src(source)])

    def sev(p: str) -> str:
        return f'<span class="sev {E(p.lower())}">{E(p)}</span>'

    gates = [q for q in INFO_REGISTER if q[1] == "Gate"]
    others = [q for q in INFO_REGISTER if q[1] != "Gate"]

    def info_rows(qs):
        return [[f'<b>{E(i)}</b>', sev(pr), E(q), E(known), E(unknown), E(how), E(holder), src(k)]
                for i, pr, q, known, unknown, how, holder, k in qs]
    info_hdr = ["ID", "Priority", "Question", "Known today (official sources)", "Not known",
                "How to find out", "Held by", "Official context source"]
    parts = [
        CALLOUT_BOUNDARY,
        h1("Questions & answers", "What has to be answered before a decision can reasonably be made, what is "
           "already known, what is not, and how to find the rest. Private documents belong in secure offline "
           "review, not on this public site."),
        '<div class="jump"><a href="#gate">Gate questions</a><a href="#supporting">Supporting questions</a>'
        '<a href="#order">Order of work</a><a href="#answers">Current answers</a></div>',
        '<div class="stats compact">'
        f'<div><strong>{len(INFO_REGISTER)}</strong><span>Questions in the register</span></div>'
        f'<div><strong>{len(gates)}</strong><span>Gate questions</span></div>'
        f'<div><strong>{sum(1 for q in INFO_REGISTER if q[1] == "High")}</strong><span>High priority</span></div>'
        f'<div><strong>{sum(1 for r in ROWS if r["status"] == "Blank")}</strong><span>Blank evidence cells</span></div></div>',
        '<div id="gate">' + h2("Gate questions", f"{len(gates)} answers without which no route can be chosen") + '</div>',
        '<p>Each of these is answered by a document the owner or tenant already holds, or by a professional. '
        'None can be answered from public data, which is why the recommendation on this site is conditional.</p>',
        table(info_hdr, info_rows(gates), "Gate questions · known, not known, how to find out"),
        '<div id="supporting">' + h2("Supporting questions", f"{len(others)} answers that refine price, structure and timing") + '</div>',
        table(info_hdr, info_rows(others), "Supporting questions · known, not known, how to find out"),
        '<div id="order">' + h2("Order of work", "The shortest route to a defensible decision") + '</div>',
        '<ol class="steps">'
        '<li><b>Read the lease.</b> A real-estate attorney abstracts the executed lease and amendments: Q-01, Q-02, Q-03, Q-12.</li>'
        '<li><b>Fix the place privately.</b> Jurisdiction, tax bill, zoning and the three hazard viewers: Q-06, Q-11, Q-13, Q-16.</li>'
        '<li><b>Ask the tenant in writing.</b> Estoppel, site sales and renewal intention, with a response date: Q-04, Q-05.</li>'
        '<li><b>Fix the owner\'s numbers.</b> Basis, depreciation, structure, debt and goals with the CPA and advisers: Q-08, Q-09, Q-10.</li>'
        '<li><b>Test the market.</b> Two or three independent price opinions and comparable sales: Q-07, Q-19.</li>'
        '<li><b>Check the downside.</b> Insurance, building condition and environmental history: Q-14, Q-15.</li>'
        '<li><b>Compare.</b> After-tax sale proceeds against the hold and extension cases, and against what the proceeds '
        'would earn elsewhere: Q-18.</li></ol>',
        '<div id="answers">' + h2("Current answers", f"{len(rows)} decision questions answered as far as the evidence allows") + '</div>',
        table(["Question", "Current answer", "Evidence needed / discovery route", "Decision consequence", "Status", "Official source"],
              body, "Decision questions, answers and evidence gaps"),
        '<a class="quiet" href="suggestions.html">Tools proposed to help answer these →</a>',
    ]
    return shell("questions", ''.join(parts), KICKER["questions"])


def page_suggestions() -> str:
    proposed = '<span class="badge proposed">Proposed</span>'
    # Seven process proposals published by an earlier session (PR #60); kept verbatim.
    # Recommendations are analyst proposals, not claims made by the linked agencies.
    process_items = [
        ("1", "Protect privacy first", "Keep all identifiers, lease files and owner finances offline with authorized advisers; publish only aggregate, non-identifying findings.", "Reduces exposure; makes independent parcel checks harder without private access.", "Approve a private review protocol before collecting anything.", "ZIMAS"),
        ("2", "Build a lease and notice calendar", "Have counsel review all amendments, options, notice periods, casualty terms and obligor documents privately.", "Prevents missed dates; legal review has cost and may uncover constraints.", "No sale or renewal deadline is verified yet.", "SECQ3"),
        ("3", "Compare executable alternatives", "Obtain confidential written sale interest and renewal proposals; compare after-tax proceeds, expenses, credit, reserves and reinvestment risk.", "Preserves options but preliminary bids and proposals may change.", "Do not commit or publish private figures; verify tax treatment with advisers.", "IRS1031"),
        ("4", "Resolve the trade area privately", "Use the location only in a secure workflow to select consistent Census tracts and local planning, traffic, school and competitor evidence.", "More relevant than city averages, but catchment boundaries and sampling uncertainty matter.", "Publish geography only if it cannot identify the asset.", "CITY"),
        ("5", "Stress correlated hazards", "Privately check seismic, flood and fire maps, engineering and insurance; stress loss of rent, repairs and exit liquidity together.", "Makes tail risks visible; regional probabilities are not parcel loss probabilities.", "Use effective maps and actual policy terms; do not assign invented odds.", "UCERF3"),
        ("6", "Improve the projection system", "Create and back-test a versioned, cash-flow model when verified inputs and sufficient comparable history exist; distinguish observations from assumptions.", "Supports repeatable comparisons but a model can be precise and still wrong.", "Until calibrated, withhold numeric parcel forecasts and review scenarios with advisers.", "SCAG"),
        ("7", "Maintain the evidence", "Assign a reviewer to refresh dated sources, check changed rules and test links and privacy before publication.", "Reduces stale claims; official releases have different vintages and may conflict.", "Review material changes before publishing; retain previous vintages.", "BLS"),
    ]
    # Six site proposals published by session f0b78eb6 (PR #63); kept verbatim.
    site_proposals = [
        ("S-1 · Publish break-even sensitivities", "Display the dimensionless 1 R sensitivity grid from scripts/projection.py on Projections alongside explicit blank owner-input cells.", "Makes exit-cap and rent-growth break-evens interactive for readers, vs. risking confusion between illustrative 5.0%–6.5% caps and market quotes.", "Confirm whether illustrative tables belong on the public site or offline only.", "FRED"),
        ("S-2 · Offline Census tract extractor", "Add a local script pulling ACS 5-year tract and block-group estimates with margins of error once Owner A selects a corridor privately.", "Eliminates city/county geographic mismatch without exposing parcel identity, vs. higher sampling variance in small tracts.", "Require Owner A sign-off on tract granularity and non-publication of tract codes if narrow.", "CITY"),
        ("S-3 · Offline parcel overlay workbook", "Bundle an air-gapped checklist querying ZIMAS zoning, CGS EQ Zapp, CAL FIRE FHSZ and FEMA flood maps for the private parcel file.", "Closes all parcel hazard and jurisdiction blanks locally, vs. requiring manual screening so private parcel output never enters Git.", "Keep parcel scripts out of published artifacts and run only on local private inputs.", "FEMA"),
        ("S-4 · Scheduled source-freshness checks", "Track upcoming statutory and issuer releases automatically, starting with the 2026-12-09 Q4/FY2026 earnings webcast, monthly BLS, FRED DGS10 and Measure ULA indexation.", "Catches stale figures and portal outages such as FEMA NRI HTTP 500 early, vs. automated monitors cannot evaluate nuanced policy notes.", "Assign reviewer sign-off before updating live rows from new releases.", "IR26Q4"),
        ("S-5 · Explicit vintage and methodology tags", "Keep dual-definition rows (87.4% four-year ACGR vs 87.6% combined rate; 2025 Topic 409 vs 2026 Rev. Proc. 2025-32 vs draft 2027 guidance) visually grouped with vintage tags.", "Prevents apples-to-oranges comparisons across agencies and tax years, vs. adds row density for readers wanting one headline figure.", "Choose preferred presentation rule before adding future dual-series indicators.", "IRSRP25"),
        ("S-6 · Archive legacy companion layers", "Move superseded repository directories (advisory/, analysis/, brief/, dashboard/, decision-file/, docs/, pages/) into a clearly tagged archive branch or folder.", "Eliminates contributor confusion over obsolete scripts and figures (R-01–R-13), vs. breaks relative links cited inside older audit logs.", "Confirm audit-trail retention preference before relocating historical files.", "DOF"),
    ]
    areas: list[str] = []
    for sg in SUGGESTIONS:
        if sg[1] not in areas:
            areas.append(sg[1])
    parts = [
        '<section class="callout warn"><b>Nothing on this page has been implemented.</b> These are proposals '
        'for review. Each lists the options available, so a path can be chosen before any change is made to '
        'the site or the repository.</section>',
        h1("Suggestions to review", "Ways to make this site and the decision process more useful, set out so that "
           "someone can review them and choose. These are analyst judgements; the official links provide "
           "context, not agency endorsement."),
        '<div class="stats compact">'
        f'<div><strong>{len(SUGGESTIONS)}</strong><span>Site suggestions</span></div>'
        f'<div><strong>{len(process_items)}</strong><span>Process proposals</span></div>'
        f'<div><strong>{len(site_proposals)}</strong><span>Technical options</span></div>'
        f'<div><strong>{len(areas)}</strong><span>Areas</span></div>'
        f'<div><strong>{len(SUGGESTION_PATHS)}</strong><span>Ways to combine them</span></div>'
        '<div><strong>0</strong><span>Implemented</span></div></div>',
        h2("Choose a path", "Four ways to combine the suggestions"),
        table(["Path", "Includes", "What the owner gets", "Privacy position", "Status", "Official context source"],
              [[f'<b>{E(a)}</b>', E(b), E(c), E(d), proposed, src(k)] for a, b, c, d, k in SUGGESTION_PATHS],
              "Paths · choose one before anything is built"),
        '<p class="small">Path 1 is recommended because it adds the tools the decision needs while keeping every '
        'owner-specific figure out of the repository and off the web.</p>',
    ]
    parts.append(h2("Process proposals", f"{len(process_items)} proposals in priority order"))
    parts.append(table(
        ["Priority", "Proposal", "Suggested action", "Trade-off / risk", "Review gate", "Status", "Official context"],
        [[E(n), E(proposal), E(action), E(tradeoff), E(gate), proposed, src(key)]
         for n, proposal, action, tradeoff, gate, key in process_items],
        "Process proposals · not yet implemented"))
    parts.append('<p>No private facts or user selections are collected on this static site. The missing property '
                 'documents cannot be obtained without authorized access.</p>')
    parts.append(h2("Site, data and model enhancements", f"{len(site_proposals)} technical options · none applied without approval"))
    parts.append(table(
        ["Option", "Proposed enhancement", "Trade-off / risk", "Review gate", "Status", "Official context"],
        [[E(opt), E(prop), E(trade), E(gate), proposed, src(key)] for opt, prop, trade, gate, key in site_proposals],
        "Proposed site and engineering enhancements · awaiting selection"))
    for area in areas:
        items = [sg for sg in SUGGESTIONS if sg[1] == area]
        parts.append(h2(area, f"{len(items)} suggestion{'s' if len(items) != 1 else ''}"))
        parts.append(table(
            ["ID", "Suggestion", "Why it helps the decision", "Options to choose from", "Privacy and effort", "Status",
             "Official context source"],
            [[f'<b>{E(i)}</b>', E(t), E(why), E(opts), E(cost), proposed, src(k)]
             for i, _a, t, why, opts, cost, k in items],
            f"{area} · proposed, not implemented"))
    parts.append(
        '<section class="callout"><b>How to choose.</b> Reply with a path, or with a list of suggestion IDs and '
        'the option letter for each, for example "Path 1, plus SG-08 A". Until a choice is recorded, the site '
        'stays as it is and only the evidence is refreshed.</section>'
        '<a class="quiet" href="questions.html">The questions these tools are meant to answer →</a>')
    return shell("suggestions", ''.join(parts), KICKER["suggestions"])


def page_decisions() -> str:
    drows = [[E(a), E(b), E(c), E(d), src(s)] for a, b, c, d, s in DECISIONS]
    body = [CALLOUT_BOUNDARY,
            h1("Decision matrix", "Every route available for the property, what has to be true for it, "
               "and the risk that dominates it. No route is scored with invented weights."),
            table(["Pathway", "When it may be preferable", "Main risks", "Evidence gate", "Official context source"],
                  drows, "Eight pathways · sell / renew / hold / re-tenant / redevelop"),
            '<div id="pathway-risks">' + h2("Risk of every pathway", "Business as usual, then the rare event") + '</div>',
            '<p>The same two questions are asked of each route: what can go wrong in ordinary conditions, and '
            'what happens to it in an earthquake, a wildfire or a tenant failure. No probability is assigned to '
            'any cell.</p>',
            table(["Pathway", "Business-as-usual risks", "Black-swan exposure", "What limits the damage",
                   "Official context source"],
                  [[f'<b>{E(a)}</b>', E(b), E(c), E(d), src(k)] for a, b, c, d, k in DECISION_RISKS],
                  "Risk of every pathway · business as usual and black swan"),
            '<section class="split"><div><h3>What separates the routes</h3>'
            '<p>Every route that keeps the property keeps the whole regional hazard exposure, whatever the lease '
            'says. Only a sale, or an exchange into property outside the region, removes it. The routes differ in '
            'how long the exposure lasts and in how much room is left to react.</p></div>'
            '<div><h3>Best fit for preservation with manageable risk</h3>'
            '<p>Running both tracks in parallel carries the smallest avoidable risk: it costs effort and advisory '
            'fees, and in return a sale and an extension are both still available when the documents arrive. '
            'Holding to expiry and redevelopment sit at the other end.</p>'
            '<a class="quiet" href="risk.html">Full risk register →</a></div></section>',
            h2("Recommended sequence", "Analyst judgement, not a valuation"),
            '<ol class="steps">'
            '<li><b>Now.</b> Obtain the executed lease, amendments, estoppel, rent roll, tax bill, insurance '
            'policies and the owner\'s basis and debt — privately, never on this site.</li>'
            '<li><b>Now.</b> Confirm jurisdiction, parcel hazard overlays and the remaining term including '
            'all renewal options.</li>'
            '<li><b>Plan timing.</b> Consider confidential marketing and written renewal terms in parallel. The '
            '24–36 month window is illustrative, not a verified deadline; lease notice rights may require earlier action.</li>'
            '<li><b>On receipt of both.</b> Compute after-tax net sale proceeds against the discounted hold '
            'case using the verified rules on the Taxes page.</li>'
            '<li><b>Decision.</b> Sell if the documented offer is acceptable; extend only against '
            'an enforceable extension when its risk-adjusted outcome better serves the owner.</li>'
            '<li><b>Either route.</b> Verify insurance, size a re-letting reserve and cap this asset\'s share '
            'of Owner A\'s net worth at a level that can be lost without changing their plans.</li>'
            '</ol>',
            h2("Dominant risk of each route", "The thing most likely to break it"),
            '<section class="split"><div><h3>Sell-side</h3><p>A failed marketing period, an unexpected '
            'transfer-tax liability, or reinvestment into an equally concentrated asset. Measure ULA and the '
            'county documentary tax are verified from the taxing authorities, but the owner\'s numbers are not.</p>'
            + src("DTT", "County transfer tax") + '</div><div><h3>Hold-side</h3>'
            '<p>A short or below-market extension, a weak guarantor, a closure, or a catastrophe that removes '
            'rent and exit liquidity together. Chain-wide results cannot establish this site\'s fate.</p>'
            + src("SECQ3", "Issuer Q3 FY2026") + '</div></section>']
    return shell("decisions", ''.join(body), KICKER["decisions"])


def page_model() -> str:
    checks = [
        ("Source tier", "Government agency pages, issuer SEC filings and issuer investor releases only. No aggregators, brokerages, law firms or media.", "BLS"),
        ("Row-level provenance", "Every table body row carries an https:// link into the official source register.", "CITY"),
        ("Blank-value rule", "If a value cannot be confirmed from an official source, the value cell is empty and the row is flagged.", "DOF"),
        ("Derived arithmetic", "The only computed figures show their arithmetic in the note cell (franchise rental revenue change, combined structure loss, combined city tax rates).", "SECQ3"),
        ("Vintage and geography", "Every row states its geography and period; different agencies and vintages are never averaged.", "COUNTY"),
        ("Qualitative statements", "Statements about what a portal does are labelled Analysis, not Verified.", "EQZAPP"),
        ("Privacy gate", "Automated scan for emails, phone numbers, street addresses, parcel numbers, taxpayer identifiers and account handles across every published file.", "CDEPROF"),
        ("Build determinism", "One generator writes every published page; CI rebuilds and asserts a byte-identical diff.", "BLS"),
        ("Link integrity", "Every internal href resolves inside the published artifact; external links are https and on the approved official host list.", "FEMA"),
        ("No calibration claim", "No model was trained, fitted or back-tested; no property-level numerical output is published.", "FRED"),
    ]
    crows = [[E(a), E(b), src(k)] for a, b, k in checks]
    body = [CALLOUT_BOUNDARY,
            h1("Model & method", "The verification standard applied to every row, the arithmetic that is "
               "actually shown, and the limits of this research."),
            h2("Verification standard", "Ten rules enforced by the build"),
            table(["Rule", "What it means", "Official example"], crows, "Method rules"),
            h2("Arithmetic that is published", "Only three derived values"),
            table(["Derived value", "Arithmetic", "Official source"],
                  [["-6.8% franchise rental revenue change", "242.526 / 260.254 − 1 = −6.81%, rounded", src("SECQ3")],
                   ["16,264 structures destroyed", "6,845 (Palisades) + 9,419 (Eaton)", src("EATON")],
                   ["4.45% and 5.95% combined city rates", "0.45% base + 4.00% / 5.50% ULA", src("ULA")]],
                  "Derived values · arithmetic shown"),
            h2("Known limits", "Read before relying on anything here"),
            '<ul class="ticks plain">'
            '<li>ACS estimates carry sampling error; no margins of error were obtained.</li>'
            '<li>QuickFacts mixes vintages and survey periods; different vintages are not comparable.</li>'
            '<li>The BLS area summary is not seasonally adjusted and may be revised.</li>'
            '<li>Issuer results describe a chain, not this restaurant or its legal obligor.</li>'
            '<li>Hazard figures are scenarios and regional forecasts, not parcel exposure.</li>'
            '<li>IRS Topic 409 displays 2025 brackets while Rev. Proc. 2025-32 establishes finalized 2026 '
            'brackets; draft 2027 Rev. Proc. 2026-35 carries placeholder dates and is withheld.</li>'
            '<li>Rolling sources change: re-read the official pages on every release.</li>'
            '</ul>',
            h2("Monitoring checklist", "What to re-check and where"),
            table(["Publisher", "What to re-read", "Official link"],
                  [["U.S. Bureau of Labor Statistics", "Monthly LA Area Economic Summary", src("BLS", "BLS summary")],
                   ["Federal Reserve / FRED", "Daily 10-year Treasury yield", src("FRED", "DGS10")],
                   ["City of Los Angeles", "Indexed Measure ULA thresholds", src("ULA", "ULA FAQ")],
                   ["LA County Registrar-Recorder", "Documentary transfer tax rates", src("DTT", "County DTT")],
                   ["CAL FIRE / OSFM", "Fire Hazard Severity Zone updates", src("FHSZ", "FHSZ")],
                   ["FEMA", "Effective flood maps", src("FEMA", "MSC")],
                   ["SEC EDGAR", "Issuer quarterly and annual filings", src("SECQ3", "Q3 FY2026")],
                   ["CA Dept of Finance", "Revised population estimates", src("DOF", "DOF estimates")]],
                  "Monitoring checklist"),
            '<a class="quiet" href="projections.html">See the 13-step projection system →</a>']
    return shell("model", ''.join(body), KICKER["model"])


def page_place() -> str:
    rows = [r for r in ROWS if r["category"] == "Geography"]
    blank = [r for r in rows if r["status"] == "Blank"]
    body = [CALLOUT_BOUNDARY,
            h1("Evidence boundary", "What this site deliberately does not assert about Asset A. "
               "The absence of a parcel is the single most important fact in this project."),
            '<section class="callout warn"><b>Nothing about the subject property is asserted.</b> '
            'No address, parcel number, lease, rent roll, debt statement or tax basis was supplied. '
            'Regional evidence is context, not a forecast of this site, and no government agency publishes '
            'a value for it. "Central Los Angeles" is a colloquialism, not a legal boundary.</section>',
            h2("Geography observations", "Official, city and county scale only"),
            evidence_table(rows, "Geography · evidence register"),
            h2("The gaps that block a property-level conclusion", f"{len(blank)} unverified rows"),
            table(["Unverified item", "Value", "Why it is unverified", "Status", "Official research route"],
                  [[E(r["indicator"]), '<span class="empty" aria-label="Unverified value; intentionally blank"></span>',
                    E(r["note"]), badge("Blank"), src(r["source"])] for r in blank],
                  "Unverified geography items"),
            h2("What cannot be said", "Deliberate omissions"),
            '<ul class="ticks plain">'
            '<li>The subject site\'s jurisdiction, zoning, entitlements or drive-through rights.</li>'
            '<li>Its FEMA flood zone, CAL FIRE fire zone or CGS seismic hazard zone.</li>'
            '<li>Its trade-area population, daytime workers, traffic counts or competitive supply.</li>'
            '<li>Its assigned schools, school performance, crime or environmental condition.</li>'
            '<li>Its rent, escalations, options, guarantor, store sales, value, cap rate or sale price.</li>'
            '</ul>',
            '<a class="button" href="review.html">Flagged for Review <span>→</span></a>']
    return shell("place", ''.join(body), KICKER["place"])


def page_flagged() -> str:
    frows = [[E(f[0]), f'<span class="sev {E(f[1].lower())}">{E(f[1])}</span>', E(f[2]), E(f[3]), E(f[4]), src(f[5])]
             for f in FLAGS]
    rrows = [[E(r[0]), E(r[1]), E(r[2]), E(r[3]), src(r[4])] for r in REPO_REVIEW]
    body = ['<section class="callout warn"><b>Flagged for Review — clearly labelled.</b> '
            'Everything on this page is unresolved, conflicting or unverified. It is published rather than '
            'hidden so it can be reviewed after the site is live. <b>None of these items blocks publication '
            'or the merge</b>, because no unverified value appears anywhere else on the site as a number.</section>',
            h1("Flagged for Review", "Unverified values, official-source conflicts, stale vintages and "
               "irregularities found during the line-by-line repository review."),
            h2("Review items", f"{len(FLAGS)} entries (open & closed log) · each linked to an official source"),
            table(["ID", "Priority", "Item", "Finding", "What closes it", "Official link"], frows,
                  "Flagged items · published for manual review"),
            h2("Irregularities from the repository review", f"{len(REPO_REVIEW)} line-by-line findings"),
            table(["ID", "Area", "Finding", "Disposition", "Official link"], rrows,
                  "Repo review irregularities · see the Repo review page for detail"),
            h2("Unverified values in the evidence register", "Every one has an empty value cell"),
            table(["Category", "Indicator", "Value", "Why it is blank", "Status", "Official source"],
                  [[E(r["category"]), E(r["indicator"]),
                    '<span class="empty" aria-label="Unverified value; intentionally blank"></span>',
                    E(r["note"]), badge("Blank"), src(r["source"])]
                   for r in ROWS if r["status"] == "Blank"],
                  "Blank evidence cells · no inferred values"),
            '<a class="quiet" href="repo-review.html">Full line-by-line repo review →</a>']
    return shell("review", ''.join(body), KICKER["review"])


def page_repo_review() -> str:
    rrows = [[E(r[0]), E(r[1]), E(r[2]), E(r[3]), src(r[4])] for r in REPO_REVIEW]
    layer_rows = [
        ["Root <code>*.html</code> + <code>assets/</code>", "Canonical published site", "This session · rebuilt from one dataset", src("BLS")],
        ["<code>docs/</code>", "Repository-only research & dashboard", "Excluded from Pages by <code>_config.yml</code>", src("CITY")],
        ["<code>analysis/</code>", "Repository-only deep-dive dashboard", "Excluded; contains non-official citations (R-12)", src("BLS")],
        ["<code>brief/</code>", "Repository-only decision brief", "Excluded from Pages", src("FRED")],
        ["<code>pages/</code>", "Repository-only sourced dashboard", "Excluded from Pages", src("IRS1031")],
        ["<code>decision-file/</code>", "Repository-only decision file", "Excluded; renders an account identifier (R-13)", src("ZIMAS")],
        ["<code>advisory/</code>", "Repository-only advisory model", "Excluded; unsupported scenario weights (R-11)", src("FRED")],
        ["<code>dashboard/</code>", "Formerly live second dashboard", "Now excluded so one canonical site is published (R-02)", src("ULA")],
        ["<code>audit/</code>, <code>research/</code>, <code>data/</code>, <code>model/</code>, <code>scripts/</code>, <code>tools/</code>", "Audit trail and generators", "Excluded from Pages; preserved for review", src("DOF")],
    ]
    body = [CALLOUT_BOUNDARY,
            h1("Repo review", "A line-by-line review of the inherited repository layers, every finding "
               "linked to an official source for manual verification."),
            '<p class="lede">The repository accumulated work from more than fifteen parallel sessions. '
            'This review does not delete any of it. It records what was checked, what was corrected, '
            'what remains unresolved, and which files are actually published.</p>',
            h2("Line-by-line findings", f"{len(REPO_REVIEW)} entries · R-01 … R-{len(REPO_REVIEW):02d}"),
            table(["ID", "Area", "Finding", "Disposition", "Official source"], rrows,
                  "Repository review register"),
            h2("Layer map", "What is published and what is audit trail"),
            table(["Path / scope", "Role", "Disposition", "Official example"], layer_rows,
                  "Repository layer map"),
            h2("How each claim was checked", "Procedure"),
            '<ol class="steps">'
            '<li>Read <code>COORDINATION.md</code> and the full file inventory before claiming a task.</li>'
            '<li>Enumerated every published HTML file and every external host it links to.</li>'
            '<li>The 2026-11-12 line-by-line audit re-fetched official publisher pages and compared the values then published, including geography, period, unit and vintage; later refreshes are separately dated and do not claim to re-check unrelated rows.</li>'
            '<li>Recorded disagreements between agencies and between inherited layers rather than '
            'silently choosing one.</li>'
            '<li>Left unconfirmable values empty and published them here and on the '
            '<a href="review.html">Flagged for Review</a> page.</li>'
            '<li>Redacted all personal information encountered during research; no owner, contact, '
            'address, parcel or account identifier appears on the site.</li>'
            '<li>Rebuilt the entire site from one dataset and asserted a byte-identical rebuild in CI.</li>'
            '</ol>',
            '<p class="small">Row-level verification logs in the repository: '
            '<code>' + VERIFICATION_FILE + '</code> (generated from the register on every build) and '
            '<code>research/VERIFICATION-2026-11-12-f0b78eb6.md</code> (a second, separately written 2026-11-12 pass), '
            'and <code>research/AUDIT-2026-11-13-02fb510c.md</code> (targeted FRED freshness update; no full re-verification claimed). '
            'Machine-readable register: <code>data/canonical.json</code>.</p>']
    return shell("repo-review", ''.join(body), KICKER["repo-review"])


def page_sources() -> str:
    srows = [[E(s[0]), E(s[1]), E(s[3]), src(k)] for k, s in SOURCES.items()]
    body = [CALLOUT_BOUNDARY,
            h1("Sources & method", f"{len(SOURCES)} official sources. Every table row on this site links "
               "to one of them. No aggregators, brokerages, media or private data."),
            h2("Official source register", "Government agencies and issuer filings only"),
            table(["Publisher / document", "Publisher", "Type", "Official link"], srows,
                  "Official source register"),
            h2("Verification standard", "What 'Verified' means here"),
            '<p><b>Verified</b> means the publisher states that observation, with the geography, period, unit and vintage shown in the row. '
            'The broad row-by-row publisher review is dated 2026-11-12; FRED DGS10 was refreshed on 2026-11-13, '
            'and the snapshot date does not imply every other source was re-read that day. It does not mean the observation predicts this property. <b>Derived</b> means arithmetic on '
            'two published observations; the arithmetic is printed in the row. <b>Analysis</b> is our '
            'conditional reasoning and its link supplies background context only. <b>Unverified</b> rows '
            'have an empty value cell and an entry on the <a href="review.html">Flagged for Review</a> page.</p>',
            '<p>QuickFacts observations use different vintages, geographies and survey periods. ACS '
            'estimates have sampling error; no tract estimates or margins of error were obtained. The BLS '
            'summary updated 2026-11-04 uses unadjusted data and may be revised. Hazard context comes '
            'from USGS scenario modelling, CAL FIRE incident records and FEMA programmes (the live FEMA '
            'NRI portal returned HTTP 500 on 2026-11-12, so archived March 2023 v1.19.0 county figures '
            'are cited with vintage caveats alongside blank live scores). Issuer Q4/FY2026 results are '
            'scheduled for release 2026-12-09. No model was trained, fitted or back-tested.</p>',
            h2("Privacy and publication boundary", "Highest-priority constraint"),
            '<p>Asset A and Owner A are placeholders. No address, parcel ID, owner name, account handle, '
            'contact detail, financial account, tax basis, debt statement or private lease record is '
            'collected or published. Official filings and agency pages encountered during research contain '
            'named contacts, emails, telephone numbers and street addresses; none of that is reproduced '
            'here. The site has no forms, analytics, tracking, third-party embeds or external scripts. '
            'Public source links open their publishers\' websites; GitHub hosting may retain standard '
            'access logs.</p>',
            h2("Reproducibility", "One dataset, one generator"),
            '<p>The evidence register lives in <code>data/canonical_rows.py</code> and is exported to '
            '<code>data/canonical.json</code>. <code>scripts/build_canonical.py</code> renders every page; '
            '<code>scripts/validate.py</code> checks row provenance, blank values, official hosts, internal '
            'links and personal information; <code>scripts/stage_pages.py</code> builds the exact Pages '
            'artifact and compares it with Jekyll\'s output. This is a fixed snapshot, not a live data feed.</p>',
            '<a class="quiet" href="model.html">Model &amp; method →</a>']
    return shell("sources", ''.join(body), KICKER["sources"])


# ------------------------------------------------------------------------- artifacts
def write_dataset() -> None:
    payload = {
        "snapshot": SNAPSHOT,
        "privacy": "Asset A / Owner A placeholders only; no personal or property identifiers.",
        "sources": {k: {"label": v[0], "publisher": v[1], "url": v[2], "type": v[3]}
                    for k, v in SOURCES.items()},
        "categories": [{"name": c[0], "page": c[1] + ".html", "description": c[2]} for c in CATEGORIES],
        "pages": [{"id": p[0], "title": p[1], "file": p[0] + ".html", "group": p[2]} for p in PAGES],
        "rows": ROWS,
        "risks": RISKS,
        "decisions": DECISIONS,
        "projection_steps": PROJECTION,
        "flags": FLAGS,
        "repo_review": REPO_REVIEW,
        "decision_risks": DECISION_RISKS,
        "information_register": INFO_REGISTER,
        "suggestions": SUGGESTIONS,
        "suggestion_paths": SUGGESTION_PATHS,
        "counts": dict(Counter(r["status"] for r in ROWS)),
    }
    (ROOT / "data/canonical.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_repo_review_md() -> None:
    lines = [
        f"# Repo review — line-by-line findings (updated {SNAPSHOT}, UTC)",
        "",
        "Canonical site review, originally consolidated by `b98090a0` (2026-11-10) and extended on 2026-11-12",
        "by sessions `f0b78eb6` (R-23, R-24) and `c56c569e` (R-25 onward). This file is the repository-side",
        "companion to the published [Repo review page](repo-review.html) and the row-level verification logs",
        f"[`{VERIFICATION_FILE}`]({VERIFICATION_FILE}) (generated) and",
        "[`research/VERIFICATION-2026-11-12-f0b78eb6.md`](research/VERIFICATION-2026-11-12-f0b78eb6.md).",
        "",
        "The repository accumulated work from more than fifteen parallel sessions and eight overlapping",
        "dashboard layers. This review does not delete any of that work. It records what was checked, what",
        "was corrected in the canonical site, what remains unresolved, and which files are actually",
        "published. **Every finding below carries an official source link for manual review.**",
        "",
        f"**Canonical site:** {len(PAGES) + 1} static HTML pages ({len(PAGES)} registered navigation pages "
        f"plus `flagged.html` alias) · {len(ROWS)} evidence rows "
        f"({Counter(r['status'] for r in ROWS)['Verified']} verified, "
        f"{Counter(r['status'] for r in ROWS)['Derived']} derived with arithmetic shown, "
        f"{Counter(r['status'] for r in ROWS)['Analysis']} analysis, "
        f"{Counter(r['status'] for r in ROWS)['Blank']} blank/unverified) · "
        f"{len(SOURCES)} official sources · {len(FLAGS)} review flags · "
        f"{len(REPO_REVIEW)} review findings.",
        "",
        "## Line-by-line findings",
        "",
        "| ID | Area | Finding | Disposition | Official source |",
        "|---|---|---|---|---|",
    ]
    for rid, area, finding, disposition, key in REPO_REVIEW:
        s = SOURCES[key]
        cell = lambda x: x.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {cell(rid)} | {cell(area)} | {cell(finding)} | {cell(disposition)} | "
                     f"[{cell(s[0])}]({s[2]}) |")
    lines += [
        "",
        "## Layer map",
        "",
        "| Path / scope | Role | Disposition |",
        "|---|---|---|",
        "| Root `*.html` + `assets/style.css` | Canonical published site | Generated by `scripts/build_canonical.py` |",
        "| `data/canonical.json`, `data/canonical_rows.py` | Machine-readable register | Source of truth; excluded from Pages |",
        f"| `{VERIFICATION_FILE}` | Row-by-row verification log | Excluded from Pages; internal audit |",
        "| `docs/`, `analysis/`, `brief/`, `pages/`, `decision-file/`, `advisory/`, `dashboard/` | Repository-only companion layers | Excluded from Pages by `_config.yml` |",
        "| `audit/`, `research/archive/`, `site/`, `model/`, `tools/`, `scripts/`, `_advisory_src/`, `_dashboard_src/` | Audit trail and generators | Excluded from Pages |",
        "",
        "## Verification procedure",
        "",
        "1. Read `COORDINATION.md` and the full file inventory before claiming a task.",
        "2. Enumerated every published HTML file and every external host it links to.",
        "3. Re-fetched each official publisher page and compared every published numeric value against the",
        "   text of that page, including geography, period, unit and vintage.",
        "4. Recorded disagreements between agencies and between inherited layers rather than silently",
        "   choosing one.",
        "5. Left unconfirmable values empty and published them on the Flagged for Review page.",
        "6. Redacted all personal information encountered during research; no owner, contact, address,",
        "   parcel or account identifier appears on the site.",
        "7. Rebuilt the entire site from one dataset and asserted a byte-identical rebuild in CI.",
        "",
        "## Published-source restriction",
        "",
        "The canonical site links only to government agencies and issuer filings. Repository-only layers",
        "that cite commercial brokerage or private law-firm domains are excluded (R-12); the inherited",
        "account-handle rendering is also excluded (R-13).",
        "",
        "## Build gates",
        "",
        "- `scripts/validate.py` — row provenance, official hosts, blank-value rule, internal links, PII,",
        "  deterministic rebuild.",
        "- `scripts/stage_pages.py` — exact Pages artifact, source-linked rows, Jekyll byte comparison.",
        "- `.github/workflows/validate.yml` — full CI, `git diff --exit-code -- '*.html'`, Jekyll build.",
        "",
    ]
    path = ROOT / "REPO_REVIEW.md"
    start = "<!-- b98090a0 canonical repo review: start -->"
    end = "<!-- b98090a0 canonical repo review: end -->"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if start in existing:
        head = existing.split(start, 1)[0]
        tail = existing.split(end, 1)[1] if end in existing else ""
        existing = head + tail
    section = "\n".join([start] + lines + [end, ""])
    path.write_text(existing.rstrip() + "\n\n" + section, encoding="utf-8")


def assert_verification_log_present() -> None:
    """Require the immutable 2026-11-12 audit; later checks get separate dated notes."""
    if not (ROOT / VERIFICATION_FILE).is_file():
        raise FileNotFoundError(f"Immutable dated verification record is missing: {VERIFICATION_FILE}")


CSS = """/* Asset A decision desk — single canonical stylesheet. No external assets. */
:root{--bg:#f4f6fa;--card:#fff;--ink:#16213b;--mut:#5d6b83;--line:#e2e7f0;--accent:#0f766e;--accent2:#1d4ed8;--ok:#157347;--okbg:#e8f6ee;--warn:#a15c00;--warnbg:#fff4dd;--bad:#b42318;--badbg:#fdecea;--an:#4c3fa3;--anbg:#efecfb}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent2);text-decoration:none}
a:hover{text-decoration:underline}
.skip{position:absolute;left:-9999px;top:0;background:#fff;padding:10px 16px;z-index:99}
.skip:focus{left:12px;top:12px}
.app{display:flex;min-height:100vh;max-width:1600px;margin:0 auto}
.sidebar{width:252px;flex:0 0 252px;background:#fff;border-right:1px solid var(--line);padding:22px 16px 30px;position:sticky;top:0;height:100vh;overflow-y:auto}
.brand{display:flex;gap:11px;align-items:center;color:var(--ink);padding:2px 6px 20px;border-bottom:1px solid var(--line);margin-bottom:16px}
.brand:hover{text-decoration:none}
.brand .mark{display:grid;place-items:center;width:38px;height:38px;border-radius:10px;background:var(--ink);color:#fff;font-weight:800;font-size:17px;letter-spacing:-1px}
.brand b{display:block;font-size:14px;letter-spacing:.09em}
.brand small{display:block;color:var(--mut);font-size:10px;letter-spacing:.11em;margin-top:2px}
.sidebar nav{display:flex;flex-direction:column;gap:1px}
.nav-label{font-size:10px;font-weight:700;letter-spacing:.13em;color:#8a97ab;margin:17px 10px 7px}
.sidebar nav a{padding:7px 11px;border-radius:7px;color:#39465c;font-size:13.5px;display:block}
.sidebar nav a:hover{background:#f1f4f9;text-decoration:none}
.sidebar nav a[aria-current=page]{background:var(--ink);color:#fff;font-weight:600}
.privacy{margin-top:24px;padding:13px;background:#f7f9fc;border:1px solid var(--line);border-radius:9px;font-size:11.5px;color:var(--mut)}
.privacy b{color:var(--accent);display:block;margin-bottom:6px;font-size:11.5px}
.privacy p{margin:0}
.main{flex:1;min-width:0;display:flex;flex-direction:column}
.topbar{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:12px 32px;background:#fff;border-bottom:1px solid var(--line);font-size:11px;letter-spacing:.11em;color:var(--mut);font-weight:600;flex-wrap:wrap}
.stamp{color:var(--accent);white-space:nowrap}
main{padding:30px 32px 54px;flex:1;min-width:0}
footer{padding:20px 32px 30px;border-top:1px solid var(--line);color:var(--mut);font-size:11.5px;background:#fff}
h1{font-size:34px;line-height:1.18;letter-spacing:-.02em;margin:6px 0 12px}
h1 span{color:var(--accent)}
h2{font-size:20px;margin:0;letter-spacing:-.01em}
h3{font-size:16px;margin:0 0 10px}
p{margin:0 0 12px}
.eyebrow{font-size:10.5px;font-weight:700;letter-spacing:.15em;color:var(--accent);margin:0 0 10px;text-transform:uppercase}
.lede{font-size:16.5px;color:#3d4b63;max-width:900px;margin:0 0 22px}
.small{font-size:12.5px;color:var(--mut)}
.section-heading{display:flex;justify-content:space-between;align-items:baseline;gap:14px;border-bottom:1px solid var(--line);padding:0 0 9px;margin:32px 0 16px;flex-wrap:wrap}
.section-heading span{font-size:12px;color:var(--mut)}
.callout{background:#eef7f5;border:1px solid #c9e6df;border-left:4px solid var(--accent);padding:14px 17px;border-radius:9px;font-size:13.5px;margin:0 0 22px;color:#22413d}
.callout.warn{background:#fff8e9;border-color:#f2dda9;border-left-color:#c98a00;color:#5a3d05}
.callout b{color:inherit}
.hero-note{background:var(--ink);color:#eaf0f8;border-radius:14px;padding:26px 28px;margin:0 0 26px}
.hero-note h2{color:#fff;font-size:23px;margin:12px 0 10px;line-height:1.3}
.hero-note p{color:#c7d3e4;max-width:900px}
.hero-note .badge{background:#26405e;color:#cfe8ff}
.button,.quiet{display:inline-block;font-size:13px;font-weight:600;margin-top:8px}
.button{background:#fff;color:var(--ink);padding:9px 16px;border-radius:8px}
.button:hover{text-decoration:none;background:#e9f4f2}
.hero-note .quiet{color:#a9e5dc;margin-left:14px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:13px}
.cards article{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:17px}
.cards .eyebrow{margin-bottom:7px;color:var(--mut);font-size:9.5px}
.cards strong{display:block;font-size:27px;letter-spacing:-.02em;line-height:1.15;margin-bottom:7px}
.cards p{font-size:12px;color:var(--mut);min-height:48px;margin-bottom:9px}
.cards a{font-size:11.5px}
.split{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.split>div{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:19px 21px}
.split h3{font-size:16px}
.split p{font-size:13.5px;color:#42506a}
.route-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.route-grid a{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 17px;transition:border-color .15s}
.route-grid a:hover{border-color:var(--accent);text-decoration:none}
.route-grid b{display:block;font-size:14px;color:var(--ink);margin-bottom:5px}
.route-grid p{font-size:12px;color:var(--mut);margin:0 0 9px;min-height:34px}
.route-grid span{font-size:11.5px;color:var(--accent);font-weight:600}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:11px}
.stats div{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:15px;text-align:center}
.stats strong{display:block;font-size:24px;line-height:1.2}
.stats span{font-size:11px;color:var(--mut)}
.stats.compact{margin-bottom:18px}
.stats.compact strong{font-size:20px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px}
.chip{background:#fff;border:1px solid var(--line);border-radius:20px;padding:5px 13px;font-size:12px;color:var(--accent2)}
.cat-head{display:flex;gap:12px;align-items:baseline;margin:30px 0 4px;font-size:19px;flex-wrap:wrap}
.cat-head span{font-size:11px;color:var(--mut);font-weight:400}
.cat-head a{font-size:12px;margin-left:auto}
.table-wrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px;margin:0 0 18px}
table{border-collapse:collapse;width:100%;font-size:12.6px}
caption{text-align:left;padding:12px 15px;font-weight:700;font-size:13px;color:var(--ink);border-bottom:1px solid var(--line)}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid #edf0f6;vertical-align:top}
thead th{background:#f7f9fc;color:#4a5870;font-size:10.5px;letter-spacing:.07em;text-transform:uppercase;position:sticky;top:0;white-space:nowrap;z-index:1}
tbody tr:nth-child(even){background:#fbfcfe}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:#f0f7f5}
td:first-child{font-weight:600;color:#26344c}
.badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:10.5px;font-weight:700;white-space:nowrap}
.badge.ok{background:var(--okbg);color:var(--ok)}
.badge.derived{background:#e6f0fb;color:#1c4f8f}
.badge.analysis{background:var(--anbg);color:var(--an)}
.badge.blank{background:var(--warnbg);color:var(--warn)}
.sev{display:inline-block;padding:2px 8px;border-radius:12px;font-size:10.5px;font-weight:700;white-space:nowrap;background:#eef1f6;color:#4a5870}
.sev.critical{background:var(--badbg);color:var(--bad)}
.sev.high{background:var(--warnbg);color:var(--warn)}
.sev.medium{background:#e6f0fb;color:#1c4f8f}
.sev.low{background:var(--okbg);color:var(--ok)}
.sev.closed{background:#eef4ef;color:#276749}
.sev.gate{background:var(--badbg);color:var(--bad)}
.badge.proposed{background:#f1ecfb;color:#4b2e83}
.jump{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 22px;font-size:12.5px}
.jump a{padding:5px 11px;border:1px solid var(--line);border-radius:14px;text-decoration:none;color:inherit;background:#fff}
.empty{display:inline-block;min-width:52px;height:14px;background:repeating-linear-gradient(45deg,#f5ead2,#f5ead2 5px,#fff8e9 5px,#fff8e9 10px);border:1px dashed #d9b96f;border-radius:3px;vertical-align:middle}
.srclink{font-size:11.5px;white-space:nowrap}
ul.ticks{margin:0 0 12px;padding-left:18px}
ul.ticks li{margin-bottom:8px;font-size:13.2px}
ul.ticks.good li::marker{color:var(--ok)}
ul.ticks.bad li::marker{color:var(--bad)}
ul.ticks.plain li{color:#42506a}
ol.steps{margin:0 0 18px;padding-left:20px}
ol.steps li{margin-bottom:9px;font-size:13.5px}
code{background:#eef1f6;padding:1px 5px;border-radius:4px;font-size:11.5px}
@media(max-width:900px){
 .app{display:block}
 .sidebar{position:static;width:auto;height:auto;border-right:0;border-bottom:1px solid var(--line);padding:14px}
 .brand{padding-bottom:12px;margin-bottom:8px}
 .sidebar nav{flex-direction:row;flex-wrap:wrap;gap:4px}
 .nav-label{display:none}
 .sidebar nav a{font-size:12px;padding:5px 9px;border:1px solid var(--line)}
 .privacy{display:none}
 .topbar{padding:10px 18px}
 main{padding:22px 18px 40px}
 footer{padding:18px}
 h1{font-size:28px}
 .split{grid-template-columns:1fr}
}
"""


def main() -> None:
    write_dataset()
    assert_verification_log_present()
    write_repo_review_md()
    (ROOT / "assets/style.css").write_text(CSS, encoding="utf-8")

    outputs: dict[str, str] = {
        "index.html": page_index(),
        "executive-summary.html": page_executive_summary(),
        "master.html": page_master(),
        "review.html": page_flagged(),
        "flagged.html": page_flagged(),
        "repo-review.html": page_repo_review(),
        "sources.html": page_sources(),
        "risk.html": page_risk(),
        "projections.html": page_projections(),
        "questions.html": page_questions(),
        "suggestions.html": page_suggestions(),
        "decisions.html": page_decisions(),
        "model.html": page_model(),
        "place.html": page_place(),
    }
    for _title, slug, _desc in CATEGORIES:
        outputs[slug + ".html"] = page_category(slug)

    for name, content in outputs.items():
        (ROOT / name).write_text(content, encoding="utf-8")

    counts = Counter(r["status"] for r in ROWS)
    print(f"Built {len(outputs)} pages, {len(ROWS)} evidence rows "
          f"({counts['Verified']} verified, {counts['Derived']} derived, "
          f"{counts['Analysis']} analysis, {counts['Blank']} blank), {len(SOURCES)} official sources.")
    print(f"Structured: {len(RISKS)} risks, {len(DECISIONS)} pathways, {len(PROJECTION)} projection steps, "
          f"{len(FLAGS)} flags, {len(REPO_REVIEW)} repo-review entries, {len(DECISION_RISKS)} pathway-risk rows, "
          f"{len(INFO_REGISTER)} information-register questions, {len(SUGGESTIONS)} suggestions.")


if __name__ == "__main__":
    main()
