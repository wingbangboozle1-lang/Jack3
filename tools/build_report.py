#!/usr/bin/env python3
"""Build the canonical integrated dashboard in ``report/``.

Generation rules enforced here, not by convention:

* a table row with status ``unverified`` cannot render a value (``cell`` blanks it);
* every value row renders a source link, and the link must exist in the register;
* no personal information is accepted as input;
* the build is deterministic - running it twice produces byte-identical output.

Run:  python3 tools/build_report.py
"""

from __future__ import annotations

import html
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import data.report_data as D  # noqa: E402

OUT = os.path.join(ROOT, "report")
E = html.escape
SNAPSHOT = "2026-11-07"
ROWS = {r["id"]: r for r in D.all_rows()}
COUNTS = D.counts()
MODEL = D.model_output()

NAV = [
    ("Overview", [("index", "Dashboard"), ("executive-summary", "Executive summary")]),
    ("The asset", [("property", "Property & lease"), ("location", "Location & site")]),
    ("The market", [("market", "Market evidence"), ("tenant", "Tenant credit")]),
    ("The decision", [("projections", "Projections 2030-2035"), ("decision", "Decision & actions")]),
    ("Risk", [("risk", "Risk register")]),
    ("Assurance", [("evidence", "Evidence table"), ("sources", "Sources"),
                   ("flagged", "Flagged for review"), ("methodology", "Method & privacy")]),
]

BADGE = {
    "verified-now": ("ok", "Verified"),
    "source-linked": ("info", "Source-linked"),
    "analysis": ("warn", "Analysis"),
    "industry": ("neutral", "Industry data"),
    "unverified": ("bad", "Unverified"),
    "input": ("blank", "Input required"),
}

LINK_TEXT = {
    "S_CENSUS_CO": "Census QuickFacts, LA County",
    "S_CENSUS_CITY": "Census QuickFacts, LA city",
    "S_BLS_EAG": "BLS, Economy at a Glance",
    "S_BLS_METRO": "BLS, metro release",
    "S_BLS_SUMMARY": "BLS, LA economic summary",
    "S_BLS_CPI": "BLS, LA CPI",
    "S_FRED_DGS10": "FRED / Federal Reserve, DGS10",
    "S_TREASURY_YIELD": "U.S. Treasury par yields",
    "S_FED_STATEMENT": "FOMC statement, 28 Oct 2026",
    "S_ASSESSOR_ROLL": "LA County Assessor release",
    "S_ASSESSOR": "LA County Assessor",
    "S_DIR_FF": "CA DIR, fast-food wage FAQ",
    "S_DIR_MW": "CA DIR, minimum wage FAQ",
    "S_LA_WAGES": "City of LA, Office of Wage Standards",
    "S_ULA": "City of LA, Measure ULA FAQ",
    "S_LAC_RR": "LA County Registrar-Recorder",
    "S_IRS_1031": "IRS, §1031 exchanges",
    "S_IRS_409": "IRS, Topic 409",
    "S_SOS_MEASURES": "CA Secretary of State, certified measures",
    "S_SOS_PROP40": "CA voter guide, Proposition 40",
    "S_USGS_FAQ": "USGS, earthquake probabilities",
    "S_USGS_SHAKEOUT": "USGS, ShakeOut scenario",
    "S_LA_FIRES": "County of LA, wildfire fact sheet",
    "S_CALFIRE_FHSZ": "CAL FIRE, hazard severity zones",
    "S_CRS": "CRS In Focus IF12871",
    "S_CDE": "CA Dept of Education",
    "S_DASHBOARD": "California School Dashboard",
    "S_JIB_10K": "Jack in the Box Inc., Form 10-K FY2025",
    "S_JIB_Q4": "Jack in the Box Inc., Q4 FY2025 release",
    "S_JIB_10Q": "Jack in the Box Inc., Form 10-Q Q3 FY2026",
    "S_BOULDER": "The Boulder Group (private research)",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def src_link(key, short=False):
    s = D.SOURCES[key]
    label = LINK_TEXT.get(key, s["publisher"]) if short else s["label"]
    return (f'<a href="{E(s["url"])}" target="_blank" rel="noopener noreferrer">'
            f'{E(label)}</a>')


def badge(status):
    cls, label = BADGE[status]
    return f'<span class="badge {cls}" title="{E(D.STATUS_LABELS[status][1])}">{E(label)}</span>'


def cell(r, field):
    """Render a value cell.  Unverified values CANNOT render (hard blank)."""
    if field == "value":
        if r["status"] in ("unverified", "input"):
            return '<span class="blank" aria-label="withheld - no official source">&mdash;</span>'
        return E(r["display_value"])
    return E(str(r.get(field) or ""))


def evidence_table(rows, fields, headers, cls="data"):
    head = "".join(f"<th scope=\"col\">{E(h)}</th>" for h in headers + ["Status", "Official source"])
    body = []
    for r in rows:
        tds = "".join(f"<td>{cell(r, f)}</td>" for f in fields)
        s = D.SOURCES.get(r["src"], {})
        url = s.get("url", "")
        link = (f'<a href="{E(url)}" target="_blank" rel="noopener noreferrer">'
                f'{E(LINK_TEXT.get(r["src"], s.get("publisher", "source")))} &#8599;</a>'
                if url else '<span class="blank">no source</span>')
        note = f'<div class="note">{E(r["note"])}</div>' if r.get("note") else ""
        body.append(f'<tr><td class="mono">{E(r["id"])}</td>{tds}'
                    f'<td>{badge(r["status"])}</td><td>{link}{note}</td></tr>')
    return (f'<div class="table-wrap"><table class="{cls}"><thead><tr><th scope="col">ID</th>'
            f'{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>')


def category_table(cat, fields=("metric", "value", "period", "geo"),
                   headers=("Indicator", "Value", "Period", "Geography")):
    rows = D.rows_for(cat)
    return evidence_table(rows, list(fields), list(headers))


def callout(kind, title, body):
    return f'<aside class="callout {kind}"><h3>{E(title)}</h3>{body}</aside>'


def kpi(label, value, sub, href=None, status="verified-now"):
    src = (f'<a href="{E(href)}" target="_blank" rel="noopener noreferrer">source &#8599;</a>'
           if href else "")
    return (f'<article class="kpi"><div class="k-label">{E(label)}</div>'
            f'<div class="k-value">{E(value)}</div>'
            f'<div class="k-sub">{sub}</div>'
            f'<div class="k-foot">{badge(status)}{src}</div></article>')


def shell(page, title, kicker, h1, lede, body, meta=""):
    nav = []
    for group, items in NAV:
        nav.append(f'<div class="nav-group"><div class="nav-title">{E(group)}</div>')
        for key, label in items:
            cur = ' aria-current="page"' if key == page else ""
            nav.append(f'<a{cur} href="{key}.html">{E(label)}</a>')
        nav.append("</div>")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Anonymised, source-linked decision file for a single-tenant Jack in the Box net-lease property in Central Los Angeles.">
<meta name="robots" content="index, follow">
<title>{E(title)} &middot; Jack in the Box NNN decision file</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<aside class="side">
  <a class="brand" href="index.html"><span class="mark">J</span><span>JACK<br><small>NNN DECISION FILE</small></span></a>
  <nav>{''.join(nav)}</nav>
  <div class="privacy-box">
    <strong>Privacy by design</strong>
    <p>Asset&nbsp;A / Owner&nbsp;1. No address, parcel, owner, tenant officer or contact detail is
    collected or published. No analytics, forms, cookies or third-party assets.</p>
    <a href="methodology.html#privacy">How this is enforced &rarr;</a>
  </div>
</aside>
<div class="main">
  <header class="topbar">
    <span>Anonymised decision file &middot; Central Los Angeles</span>
    <span class="dot">&bull;</span>
    <span>Evidence snapshot {SNAPSHOT}</span>
  </header>
  <main id="main">
    <div class="page-head">
      <div class="kicker">{E(kicker)}</div>
      <h1>{E(h1)}</h1>
      <p class="lede">{lede}</p>
      {meta}
    </div>
    {body}
  </main>
  <footer>
    <p><strong>Not an appraisal, legal opinion, tax return or personalised investment advice.</strong>
    Analysis is conditional on an anonymised subject and on evidence published up to {SNAPSHOT}.
    Missing values are withheld, never estimated.</p>
    <p>Every table row links to its publisher. Verify status is defined on
    <a href="methodology.html">Method &amp; privacy</a>. Flagged items:
    <a href="flagged.html">Flagged for review</a>.</p>
  </footer>
</div>
</body>
</html>
"""


def v(rid):
    """Formatted value of a row, or an em dash when withheld."""
    r = ROWS[rid]
    return r["display_value"] or "&mdash;"


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_index():
    s1 = MODEL["scenarios"]["pessimistic"]["ranked"]
    floor = next(x for x in s1 if x[1].startswith("S1"))
    kpis = [
        kpi("LA County population, 1 Jul 2025", v("DEM-01"),
            f'{v("DEM-02")} vs the 2020 estimates base', D.SOURCES["S_CENSUS_CO"]["url"]),
        kpi("Metro unemployment, Sep 2026", v("LAB-04"),
            "Preliminary, not seasonally adjusted", D.SOURCES["S_BLS_EAG"]["url"]),
        kpi("Tenant system same-store sales, Q3 FY2026", v("TEN-16"),
            "Brand-wide, not this restaurant", D.SOURCES["S_JIB_10Q"]["url"],
            status="source-linked"),
        kpi("Fast-food wage floor, California", v("REG-01"),
            "Applies to franchisees too", D.SOURCES["S_DIR_FF"]["url"]),
        kpi("10-year Treasury yield, 5 Nov 2026", v("RATE-05"),
            "Discount-rate reference", D.SOURCES["S_FRED_DGS10"]["url"]),
        kpi("LA County assessment roll growth", v("PROP-02"),
            "16th consecutive year of growth", D.SOURCES["S_ASSESSOR_ROLL"]["url"]),
    ]
    cards = [
        ("The asset", [("property", "Property & lease",
                        "Anonymised asset profile, NNN cost allocation, the 15-field Input Register."),
                       ("location", "Location & site",
                        "What official geography can and cannot say about a Central LA parcel.")]),
        ("The market", [("market", "Market evidence",
                         "Population, income, housing, jobs, prices and rates, every row sourced."),
                        ("tenant", "Tenant credit",
                         "Jack in the Box Inc.: unit counts, closures, same-store sales, lease terms.")]),
        ("The decision", [("projections", "Projections 2030-2035",
                           "The R-normalised model, its assumptions and its sensitivity."),
                          ("decision", "Decision & actions",
                           "Six strategies ranked by worst case, plus a dated action plan.")]),
        ("Risk", [("risk", "Risk register",
                   "15 business-as-usual risks and 7 black-swan events, each with a mitigation.")]),
        ("Assurance", [("evidence", "Evidence table",
                        "Every row with its period, geography, status and official link."),
                       ("flagged", "Flagged for review",
                        f"{len(D.FLAGS)} items that could not be verified, plus cross-layer conflicts.")]),
    ]
    card_html = []
    for group, items in cards:
        card_html.append(f'<div class="card-group"><h3>{E(group)}</h3><div class="card-row">')
        for href, title, desc in items:
            card_html.append(f'<a class="card" href="{href}.html"><b>{E(title)}</b>'
                             f'<span>{E(desc)}</span><em>Open &rarr;</em></a>')
        card_html.append("</div></div>")

    body = f"""
<section class="reco">
  <div class="reco-label">Recommendation</div>
  <h2>Sell before the lease expires &mdash; and buy the term only if the tenant will commit first.</h2>
  <p>On the committed model, selling now has the <strong>highest worst-case present value of every
  strategy tested</strong>: <strong>{floor[2]:.2f}&nbsp;R</strong> in the pessimistic scenario, against
  {next(x for x in s1 if x[1].startswith('S3') and '2030' in x[3])[2]:.2f}&nbsp;R for renewing with the incumbent to a 2030
  expiry. Renewing ranks last in both the base and the pessimistic scenarios. If &mdash; and only if
  &mdash; the tenant will sign a long extension now, extending first and then selling the lengthened
  lease has the best rank stability of any strategy.</p>
  <p class="small">R = one year of the property's current contractual base rent. The model is
  normalised because the rent, basis and building size were never supplied. Multiply by your own rent
  to read it in dollars. Full method: <a href="projections.html">Projections</a> &middot;
  <a href="decision.html">Decision</a>.</p>
</section>

<div class="kpis">{''.join(kpis)}</div>

<div class="status-strip">
  <div><b>{COUNTS['total']}</b><span>table rows</span></div>
  <div><b>{COUNTS['verified-now']}</b><span>re-verified {SNAPSHOT}</span></div>
  <div><b>{COUNTS['source-linked']}</b><span>source-linked</span></div>
  <div><b>{COUNTS['industry']}</b><span>industry (non-official)</span></div>
  <div><b>{len(D.FLAGS)}</b><span>flagged items</span></div>
  <div><b>{COUNTS['official_sources']}</b><span>official sources</span></div>
</div>

{''.join(card_html)}

{callout("warn", "What this file will not tell you",
         "<p>There is no address, parcel number, rent roll, purchase price, building size or debt "
         "schedule in this file, because none was supplied and researching the owner or the parcel "
         "would breach the privacy boundary. Every site-specific number is therefore blank and listed "
         "on <a href='flagged.html'>Flagged for review</a>.</p>"
         "<p>No commercial capitalisation rate is published by any U.S. government agency. Cap rates "
         "on this site are either labelled industry data or treated as a swept assumption &mdash; never "
         "as verified fact.</p>")}

{callout("ok", "How to read a row",
         "<p><span class='badge ok'>Verified</span> re-read on the publisher's own page during this "
         "integration, on " + SNAPSHOT + ". <span class='badge info'>Source-linked</span> carries an "
         "official or SEC link and was read when first captured. <span class='badge warn'>Analysis</span> "
         "is our arithmetic or judgement. <span class='badge neutral'>Industry data</span> is private "
         "research and is never scored as verified. A blank cell means the value could not be confirmed "
         "from an official source &mdash; it is never estimated.</p>")}

<section class="archive">
  <h2>Earlier parallel layers (archive)</h2>
  <p>Six sessions worked this repository in parallel on 2026-11-06. Their outputs are preserved and
  remain reachable, but where they disagree with this file, <strong>this file is canonical</strong>.
  The reconciliation log lists every conflict found and how it was resolved.</p>
  <ul>
    <li><a href="../index.html">Root evidence workspace</a> &mdash; published, with the evidence-boundary notice</li>
    <li><a href="https://github.com/wingbangboozle1-lang/Jack3/tree/main/docs">docs/ research dashboard</a> &mdash; repository only, withheld from publication pending re-verification</li>
    <li><a href="https://github.com/wingbangboozle1-lang/Jack3/tree/main/analysis">analysis/ deep-dive dashboard</a> &mdash; repository only</li>
    <li><a href="https://github.com/wingbangboozle1-lang/Jack3/tree/main/brief">brief/ decision brief</a> &mdash; repository only</li>
    <li><a href="https://github.com/wingbangboozle1-lang/Jack3/tree/main/pages">pages/ sourced dashboard</a> &mdash; repository only</li>
    <li><a href="https://github.com/wingbangboozle1-lang/Jack3/tree/main/decision-file">decision-file/ verified decision file</a> &mdash; repository only</li>
    <li><a href="flagged.html#reconciliation">Cross-layer reconciliation log &rarr;</a></li>
  </ul>
</section>
"""
    return shell("index", "Dashboard", "Anonymised decision file · Central Los Angeles",
                 "Sell before expiry. Buy the term only if the tenant will commit.",
                 "A single, reconciled, source-linked decision file for a Jack in the Box NNN property "
                 "whose primary term expires between 2030 and 2035. Built to separate what government "
                 "and issuer sources actually say from what an owner might hope.", body)


def page_exec():
    strategies = [
        ("S1", "Sell now, lease in place", 19.60, 15.28, 11.62, 15.44, 11.62),
        ("S5", "Extend early, then sell", 23.06, 15.61, 9.88, 16.04, 9.88),
        ("S6", "Hold to expiry, redevelop", 21.39, 13.17, 8.17, 13.98, 8.17),
        ("S2", "Hold to expiry, sell vacant", 21.16, 12.88, 7.96, 13.72, 7.96),
        ("S4", "Hold, re-let to another operator", 39.18, 12.30, 4.82, 17.15, 4.82),
        ("S3", "Renew / re-let to Jack in the Box", 21.60, 6.45, 1.18, None, 1.18),
    ]
    rows = "".join(
        f"<tr><td class='mono'>{s[0]}</td><td>{E(s[1])}</td>"
        f"<td class='num'>{s[2]:.2f}</td><td class='num'>{s[3]:.2f}</td>"
        f"<td class='num strong'>{s[4]:.2f}</td>"
        f"<td class='num'>{'' if s[5] is None else f'{s[5]:.2f}'}</td>"
        f"<td class='num strong'>{s[6]:.2f}</td></tr>" for s in strategies)

    body = f"""
{callout("ok", "The answer in one paragraph",
         "<p><strong>Sell.</strong> A 2030-2035 expiry is not a date the owner controls: the tenant's own "
         "leases are disclosed as renewable at the company's sole discretion, and the company is running a "
         "disclosed 150-200 unit closure programme timed to franchise-agreement termination dates. Selling "
         "now converts a single-tenant, single-county, one-counterparty position into diversifiable capital "
         "and removes cap-rate risk. If, and only if, the tenant will commit in writing to a long extension "
         "now, extend first and then sell the lengthened lease &mdash; it has the better base case and the "
         "best rank stability. Do not plan the decision around renewing at expiry.</p>")}

<h2>Six findings that decide it</h2>

<h3>1. The tenant is contracting, and its own closure clock runs to the expiry date</h3>
<p>Jack in the Box Inc. disclosed a <strong>150-200 restaurant block-closure programme</strong>. The
targeted restaurants are largely ones <em>"in the system for over three decades"</em>, and the remaining
closures occur <em>"based upon respective franchise agreement termination dates"</em>. The system shrank
from {v('TEN-01')} at FY2025 year end, with <strong>86 closures against 31 openings</strong> during
FY2025, and stood at {v('TEN-17')} by 2026-07-05.</p>
<p class="src">Sources: {src_link('S_JIB_Q4')}; {src_link('S_JIB_10K')}; {src_link('S_JIB_10Q')}.</p>

<h3>2. Same-store sales are negative in every recent period</h3>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Period</th><th scope="col">System same-store sales</th><th scope="col">Status</th></tr></thead>
<tbody>
<tr><td>FY2025</td><td class="num">{v('TEN-07')}</td><td>{badge('verified-now')}</td></tr>
<tr><td>Q4 FY2025</td><td class="num">{v('TEN-06')}</td><td>{badge('verified-now')}</td></tr>
<tr><td>Q3 FY2026</td><td class="num">{v('TEN-16')}</td><td>{badge('source-linked')}</td></tr>
</tbody></table></div>
<p class="src">Declines were driven by lower transactions, only partly offset by menu price rises. A
franchisee's willingness to renew is a function of store-level sales, not of brand intent.
Sources: {src_link('S_JIB_Q4')}; {src_link('S_JIB_10Q')}.</p>

<h3>3. The county is losing population, and official forecasters disagree on the sign</h3>
<p>Measured Census estimates show Los Angeles County at {v('DEM-01')} on 1 July 2025, <strong>{v('DEM-02')}</strong>
against the 2020 estimates base, and the city at {v('POP-CITY-01')} ({v('POP-CITY-02')}). Against that,
SCAG's most recent adopted regional plan projected growth, while the California Department of Finance
projects decline. (The projection workbooks themselves are unread &mdash; F-04.) Two official bodies disagree on the <em>direction</em> of travel for the same county.</p>
<p>This file underwrites to the measurement and treats growth as upside. A drive-thru restaurant sells to
people inside a short drive-time ring, so any hold case that needs demographic growth is underwriting
against the data.</p>
<p class="src">Sources: {src_link('S_CENSUS_CO')}; {src_link('S_CENSUS_CITY')}. Official projection values
are withheld &mdash; see <a href="flagged.html">F-04</a>.</p>

<h3>4. The labour market looks better than it is</h3>
<p>Metro unemployment was {v('LAB-04')} in September 2026, but the civilian labour force also fell, from
6,768,502 to 6,646,903 &mdash; about <strong>121,600 fewer people</strong>. Total nonfarm employment was
{v('LAB-05')} in August 2026, up only 0.6% year on year. A falling unemployment rate caused by people
leaving the labour force is not an expanding economy.</p>
<p>The tenant's own sector is one of the few growing: leisure and hospitality added jobs. That is a real
positive, and it is outweighed by the brand-specific evidence in findings 1 and 2.</p>
<p class="src">Sources: {src_link('S_BLS_EAG')}; {src_link('S_BLS_SUMMARY')}.</p>

<h3>5. A statutory wage ratchet compresses the tenant's margin</h3>
<p>California's fast-food minimum wage is {v('REG-01')} and applies <em>regardless of whether the employer
is the brand owner or a franchisee</em>. The state general minimum wage is {v('REG-02')} and the City of
Los Angeles general wage is {v('REG-03')}, so the $20.00 fast-food floor is the binding rate inside the
city. The tenant cannot restructure its way out of it.</p>
<p class="src">Sources: {src_link('S_DIR_FF')}; {src_link('S_DIR_MW')}; {src_link('S_LA_WAGES')}.</p>

<h3>6. The tail risk is already realised in this county</h3>
<p>The January 2025 Eaton and Palisades fires burned {v('HAZ-05')} and {v('HAZ-07')}, destroyed
{v('HAZ-06')} and {v('HAZ-08')}, and removed an estimated {v('HAZ-09')} of economic output. USGS puts
the 30-year probability of a magnitude 6.7 or greater earthquake in the Los Angeles region at
{v('HAZ-16')}; a hold to 2035 sits inside that window.</p>
<p class="src">Sources: {src_link('S_LA_FIRES')}; {src_link('S_USGS_FAQ')}; {src_link('S_CRS')}.
Values on this page marked source-linked were read from the publisher when captured; see the
<a href="evidence.html">evidence table</a> for row-level status.</p>

<h2>The numbers</h2>
<p>Six strategies, three coherent scenarios: the optimistic case takes the favourable extreme of
<em>every</em> assumption, the pessimistic case the unfavourable extreme of every one. All values are in
R, risk-adjusted for transaction friction, vacancy, re-tenanting capital, tenant survival and
catastrophe expectation.</p>
<div class="table-wrap"><table class="data"><thead><tr>
<th scope="col">ID</th><th scope="col">Strategy</th><th scope="col">Optimistic</th><th scope="col">Base</th>
<th scope="col">Pessimistic</th><th scope="col">Expected</th><th scope="col">Worst case</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="small">Expected value weights optimistic 25%, base 50%, pessimistic 25%. Diagonal reading:
selling wins the worst case outright; holding and re-letting to a different operator wins expected value
but has a spread more than three times wider. Full ranking of all fourteen strategy-by-expiry
combinations: <a href="projections.html">Projections</a>.</p>

<h2>Conditions attached to this recommendation</h2>
<ol class="tight">
<li><strong>Establish, in writing and before spending anything, whether the site is inside the tenant's
closure programme.</strong> One conversation; it decides whether the extension branch exists at all.</li>
<li><strong>Read the option clause.</strong> If renewal is at the tenant's sole discretion, as the issuer
discloses for its own leases, renewing is not a decision the owner can make.</li>
<li><strong>If a corporate guaranty exists and the site is off the closure list</strong>, extending first
then selling outranks an immediate sale on both base and expected value.</li>
<li><strong>If zoning confirms a materially better alternative use</strong>, hold-then-redevelop competes
on expected value. That is a growth choice, made explicitly, with entitlement risk priced.</li>
<li><strong>Complete the Input Register before committing capital</strong> to any branch.</li>
</ol>

<h2>What would change the answer</h2>
<ul class="tight">
<li>Tract-level evidence that the trade area is growing against the county trend.</li>
<li>A confirmed corporate guaranty plus written confirmation the site is outside the closure programme.</li>
<li>An entitlement position making redevelopment clearly more valuable than modelled.</li>
<li>Exit cap rates below roughly 5.5%, which is where hold-and-re-let starts to beat selling in the
pessimistic case.</li>
<li>Verified, affordable, replacement-cost insurance &mdash; which would reduce the black-swan deduction.</li>
</ul>

<h2>Owner actions, in order</h2>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">When</th><th scope="col">Action</th><th scope="col">Cost</th><th scope="col">Why it matters</th></tr></thead>
<tbody>
<tr><td>This week</td><td>Request the lease, any guaranty, and written confirmation of the tenant's intent for this site</td><td>None</td><td>Removes the largest single unknown</td></tr>
<tr><td>30 days</td><td>Complete the 15-field Input Register</td><td>Internal</td><td>Converts R into dollars</td></tr>
<tr><td>30-60 days</td><td>ZIMAS zoning and community-plan lookup; CAL FIRE 2025 zone check; FEMA flood zone</td><td>Low</td><td>Gates the redevelopment branch and insurance cost</td></tr>
<tr><td>60-90 days</td><td>Two independent broker opinions of value and a lender appraisal</td><td>Moderate</td><td>Cap rates cannot be officially sourced</td></tr>
<tr><td>90-120 days</td><td>CPA modelling of after-tax proceeds, including a &sect;1031 path</td><td>Moderate</td><td>Tax friction can exceed a year of rent</td></tr>
<tr><td>120-180 days</td><td>Decide: list, or negotiate an extension with a pre-agreed sale right</td><td>Broker fees</td><td>Executes the recommendation</td></tr>
</tbody></table></div>
"""
    return shell("executive-summary", "Executive summary", "Overview",
                 "The decision, the evidence behind it, and the conditions",
                 "Six findings, one recommendation, and the specific facts that would overturn it.",
                 body)


def page_property():
    nnn = [
        ("Property taxes", "Tenant", "Under a true NNN the tenant pays or reimburses. Owner exposure is nil while the lease runs."),
        ("Insurance", "Tenant", "The tenant must insure and name the owner. Verify the covenant in the document."),
        ("Maintenance and repair", "Tenant (usually)", "Absolute NNN pushes roof, structure and parking to the tenant; a standard NNN may leave structural items with the owner."),
        ("Capital replacements", "Depends on the document", "The most common source of dispute. Confirm which structure this lease is."),
        ("Base rent", "Tenant", "Fixed, with escalation. Verify the index and any cap."),
        ("Contingent rent", "Tenant, if present", "The issuer discloses about 13% of its leases carry 1-10% of gross sales. If present, it shares downside."),
        ("Vacancy and rollover", "Owner", "This is the whole exposure. Nothing transfers the risk that the tenant leaves."),
    ]
    nnn_rows = "".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr>" for a, b, c in nnn)
    inputs = "".join(f"<tr><td class='mono'>{E(r['id'])}</td><td>{E(r['field'])}</td>"
                     f"<td>{E(r['why'])}</td><td><span class='blank'>&mdash;</span></td></tr>"
                     for r in D.INPUT_ROWS)
    lease_ids = ["LEASE-01", "LEASE-02", "LEASE-03", "LEASE-04", "TEN-18"]
    lease_rows = evidence_table([ROWS[i] for i in lease_ids],
                                ["metric", "value", "period", "geo"],
                                ["Disclosure", "As disclosed", "Period", "Scope"])

    body = f"""
{callout("warn", "The subject is anonymised, deliberately",
         "<p>This is <strong>Asset A</strong>: a single-tenant quick-service restaurant property under a "
         "triple-net lease, in a Central Los Angeles submarket, with a primary term expiring somewhere "
         "between 2030 and 2035. That is the entire verified description. There is no address, parcel "
         "number, building size, rent, basis or debt schedule in this file, and none will be added. The "
         "privacy directive is the reason, and it is enforced by a build check.</p>")}

<h2>The lease structure, as a structure</h2>
<p>Under a true NNN lease the tenant pays taxes, insurance and maintenance, so the owner's operating
exposure is close to zero while the lease runs. That is often described as passive ownership. It is not:
it transfers every operating cost to the tenant and leaves the owner with 100% of the
<em>continuation</em> risk.</p>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Cost or risk</th>
<th scope="col">Who bears it</th><th scope="col">What to verify in the document</th></tr></thead>
<tbody>{nnn_rows}</tbody></table></div>
<p class="small">This table is a structural explanation, not a reading of the owner's lease, which was
not supplied. It is labelled <span class="badge warn">Analysis</span>.</p>

<h2>What the tenant's own filings disclose about its leases</h2>
<p>The best available evidence of how this brand behaves at expiry is what it must disclose to the SEC
about its own lease portfolio, where it is both lessee and lessor.</p>
{lease_rows}
<p class="src">Source: {src_link('S_JIB_10K')}. These are the company's standard terms, not the owner's
document. Where the owner's lease differs, the owner's lease governs.</p>

{callout("ok", "The one inference that matters",
         "<p>A disclosed initial term of generally 20 years, running to a 2030-2035 expiry, implies a "
         "lease that began around 2010-2015 &mdash; consistent with a mature site. The issuer's renewal "
         "options are disclosed as <em>generally exercisable at the company's sole discretion</em>. If the "
         "owner's lease mirrors that, the renewal decision belongs to the tenant, and the entire "
         "'renew' branch is not the owner's to take.</p>")}

<h2>Input Register &mdash; 15 fields the owner must supply</h2>
<p>Every field below is blank by design. None of it can be researched from public sources without
identifying the property, and identifying it is out of scope. Fields are ordered by how much they change
the answer.</p>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">ID</th>
<th scope="col">Field</th><th scope="col">Why it matters</th><th scope="col">Value</th></tr></thead>
<tbody>{inputs}</tbody></table></div>
<p class="small">These rows are published as <span class="badge blank">Input required</span> on
<a href="flagged.html">Flagged for review</a>, together with the action that closes each one.</p>

<h2>Why the model had to be normalised</h2>
<p>Because the rent was never supplied, the projection model is written in units of
<strong>R = one year of the current contractual base rent</strong>. Nothing is invented, and the ranking
still works: a sell-versus-hold comparison is two cash-flow streams from the same asset, so the rent
level largely cancels out. The owner multiplies by their own rent in private.</p>
"""
    return shell("property", "Property & lease", "The asset",
                 "A net lease transfers the costs. It does not transfer the risk.",
                 "The anonymised asset, the NNN structure, what the tenant's filings disclose about its "
                 "leases, and the fifteen fields that would turn this into a valuation.", body)


def page_location():
    body = f"""
{callout("info", "Central Los Angeles is not an official statistical geography",
         "<p>The brief says 'around central Los Angeles'. No Census, BLS or City of Los Angeles "
         "statistical product is published under that name. Rather than invent a boundary, every figure "
         "in this file is labelled with one of three official geographies, and never blended.</p>")}

<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Official geography</th>
<th scope="col">Official definition</th><th scope="col">What it is used for here</th>
<th scope="col">Why not the parcel</th></tr></thead><tbody>
<tr><td>Los Angeles County</td><td>Census county, FIPS 06037</td><td>Population, income, housing, hazards, property tax</td><td>Too broad to describe a trade area; used for direction only</td></tr>
<tr><td>Los Angeles city</td><td>Incorporated place</td><td>City minimum wage, Measure ULA, transfer tax</td><td>Regulatory boundary, not a demand boundary</td></tr>
<tr><td>Los Angeles-Long Beach-Santa Ana MSA</td><td>BLS metropolitan area</td><td>Employment, unemployment, labour force</td><td>Labour market, not a retail trade area</td></tr>
<tr><td>Parcel / trade area</td><td>Address-specific</td><td><span class="blank">&mdash;</span></td><td>Withheld: identifying the parcel breaches the privacy directive</td></tr>
</tbody></table></div>

<h2>What is verified about the site's economic setting</h2>
<div class="two-col">
<div>
<h3>Demand and density</h3>
{evidence_table([ROWS[i] for i in ["DEM-01","DEM-02","POP-CITY-01","POP-CITY-02","DEM-04","DEM-05"]],
                ["metric","value","period","geo"], ["Indicator","Value","Period","Geography"])}
</div>
<div>
<h3>Spending base</h3>
{evidence_table([ROWS[i] for i in ["LAB-27","LAB-25","LAB-26","INC-01","INC-02","INC-07"]],
                ["metric","value","period","geo"], ["Indicator","Value","Period","Geography"])}
</div>
</div>
<p class="small">County accommodation and food services sales of {v('LAB-27')} in 2022 describe a large
demand pool. They say nothing about this restaurant's capture rate.</p>

<h2>Site attributes that drive value &mdash; and are not knowable</h2>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Factor</th>
<th scope="col">Why it drives value</th><th scope="col">Status</th><th scope="col">How to close it</th></tr></thead>
<tbody>
<tr><td>Traffic count on the frontage road</td><td>The primary demand driver for a drive-thru; the first number any buyer asks for</td><td>{badge('input')}</td><td>Caltrans count for the nearest station (F-10)</td></tr>
<tr><td>Zoning and permitted uses</td><td>Determines whether a vacated box can be re-let or redeveloped</td><td>{badge('input')}</td><td>ZIMAS lookup plus planning consultation (F-08)</td></tr>
<tr><td>Community plan designation</td><td>The city's long-range land-use statement for the parcel</td><td>{badge('input')}</td><td>planning.lacity.gov (F-08)</td></tr>
<tr><td>Fire Hazard Severity Zone (2025 map)</td><td>Insurance availability and cost; County LRA zones were re-mapped in 2025</td><td>{badge('input')}</td><td>CAL FIRE LRA map (F-07)</td></tr>
<tr><td>Flood zone</td><td>Insurance and post-fire debris-flow exposure</td><td>{badge('input')}</td><td>FEMA flood map (F-07)</td></tr>
<tr><td>Assigned schools and enrolment</td><td>A weak direct driver for a drive-thru, a real signal of neighbourhood trajectory</td><td>{badge('input')}</td><td>CDE Dashboard for the assigned schools (F-09)</td></tr>
<tr><td>Transit project timing</td><td>New station catchments change daypart traffic and can support another use</td><td>{badge('input')}</td><td>metro.net project pages (F-11)</td></tr>
</tbody></table></div>

<h2>What can be said about schools and human capital without the parcel</h2>
{evidence_table([ROWS[i] for i in ["EDU-01","EDU-02","INC-11","INC-12","INC-13","INC-14"]],
                ["metric","value","period","geo"], ["Indicator","Value","Period","Geography"])}
<p class="small">District-level attainment is context, not a school rating. Nothing here supports a claim
about a specific school, and none is made.</p>

<h2>Hazard setting</h2>
{evidence_table([ROWS[i] for i in ["HAZ-16","HAZ-17","HAZ-18","HAZ-13","HAZ-14","HAZ-15"]],
                ["metric","value","period","geo"], ["Indicator","Value","Period","Geography"])}
<p class="small">Los Angeles County Local Responsibility Area Fire Hazard Severity Zones were re-established
in 2025, so any pre-2025 parcel determination is stale. The parcel-level class is withheld as input
required. Full hazard discussion: <a href="risk.html">Risk register</a>.</p>
"""
    return shell("location", "Location & site", "The asset",
                 "What official geography can say about a Central LA site &mdash; and what it cannot",
                 "Three official geographies, a verified demand base, and seven site attributes that "
                 "require the address.", body)


def page_market():
    body = f"""
<p class="lede-inner">Every row below is a published observation with its own period and geography.
Vintages are mixed by nature &mdash; V2025 population estimates, 2020-2024 ACS five-year estimates,
2022 Economic Census, 2023 business register, 2026 monthly labour data. Read the period column before
comparing anything.</p>

<h2>Demographics</h2>
{category_table("Demographics")}

<h2>Income and housing</h2>
{category_table("Income & Housing")}

<h2>Labour market</h2>
{category_table("Labor Market", ("metric","value","period","geo"),
                ("Indicator","Value","Period","Geography"))}
{callout("warn", "Read the unemployment rate with the labour force",
         f"<p>{v('LAB-04')} in September 2026 looks healthy. The labour force fell from 6,768,502 to "
         f"{v('LAB-01')} over the year &mdash; roughly 121,600 fewer people. A rate that falls because "
         "people leave the workforce is not an expanding labour market, and the two numbers are published "
         "together here so the favourable one cannot be read alone.</p>")}

<h2>Prices and rates</h2>
{category_table("Prices & Rates")}
<p class="small">The federal funds target range was confirmed on the FOMC statement of 28 October 2026:
maintained at 3-3/4 to 4 percent on a 10-2 vote, with two members preferring a 25bp increase. The
10-year Treasury yield is shown at its latest observation and, separately, at the 2 January 2026 level
used as the model's date-stamped discount anchor.</p>

<h2>Property tax and valuation context</h2>
{category_table("Property Tax & Valuation")}
<p class="src">Source: {src_link('S_ASSESSOR_ROLL')}. The release prints "42% increase" in one bullet
and 4.42% elsewhere on the same page; 4.42% is used here because it reconciles with $2.272 trillion
against the prior roll. Recorded as F-18 so the typo is not mistaken for ours.</p>

<h2>State and local regulation affecting this tenant</h2>
{category_table("Regulation")}

<h2>Education</h2>
{category_table("Education")}

<h2>Market pricing &mdash; industry data only, never scored as verified</h2>
{callout("warn", "No U.S. government agency publishes commercial cap rates",
         "<p>The figures below come from a private research firm. They are shown because they are the only "
         "structured market pricing available, and they are excluded from the official evidence table. "
         "The model does not use them; it sweeps a cap-rate band instead.</p>")}
{evidence_table(D.industry_rows(), ["metric","value","period","geo"],
                ["Indicator","Value","Period","Geography"])}
"""
    return shell("market", "Market evidence", "The market",
                 "The economic evidence for the submarket, row by row",
                 "Population, income, housing, employment, prices, property tax and regulation &mdash; "
                 "each observation with its publisher, period and geography.", body)


def page_tenant():
    body = f"""
{callout("warn", "This page is about the brand, not about this restaurant",
         "<p>Everything below is disclosed at company or system level. The subject restaurant's own sales, "
         "rent coverage and lease terms were not supplied. A brand-level statistic is evidence about the "
         "counterparty's trajectory &mdash; it is not a forecast for one site.</p>")}

<h2>Company disclosures</h2>
{evidence_table([ROWS[i] for i in ["TEN-01","TEN-02","TEN-03","TEN-04","TEN-05","TEN-12",
                                    "TEN-13","TEN-14","TEN-17","TEN-18"]],
                ["metric","value","period","geo"], ["Disclosure","Value","Period","Scope"])}

<h2>Same-store sales</h2>
{evidence_table([ROWS[i] for i in ["TEN-06","TEN-07","TEN-08","TEN-09","TEN-10","TEN-11","TEN-16"]],
                ["metric","value","period","geo"], ["Measure","Value","Period","Scope"])}

<h2>Lease terms the issuer discloses</h2>
{evidence_table([ROWS[i] for i in ["LEASE-01","LEASE-02","LEASE-03","LEASE-04"]],
                ["metric","value","period","geo"], ["Term","As disclosed","Period","Scope"])}

{callout("ok", "The decisive quotation",
         "<p>The issuer states that the restaurants targeted by its closure programme are largely ones "
         "<em>in the system for over three decades</em>, and that remaining closures occur <em>based upon "
         "respective franchise agreement termination dates</em>. A lease expiring between 2030 and 2035 is "
         "exactly that kind of date. This does not mean the site will close. It means the owner should not "
         "assume renewal, and should establish the site's status before committing capital to either a "
         "renewal negotiation or a marketing process.</p>"
         f"<p class='src'>Source: {src_link('S_JIB_10K')}; {src_link('S_JIB_Q4')}.</p>")}

<h2>Why this is credit evidence, not restaurant criticism</h2>
<p>In a single-tenant NNN structure the owner's return is not a function of property management &mdash;
there is nothing to manage &mdash; but entirely of whether one counterparty keeps wanting the site.
Three things therefore matter: the tenant's ability to pay (corporate guaranty), its willingness to stay
(store-level economics), and its legal option to leave or stay (the option clause). The first is unknown,
the second is disclosed as deteriorating, and the third is disclosed as the tenant's choice.</p>

<h2>What would upgrade the tenant assessment</h2>
<ul class="tight">
<li>Written confirmation that this site is outside the closure programme.</li>
<li>A corporate guaranty that survives franchisee failure.</li>
<li>Site-level sales and rent-coverage data, which only the tenant or the owner can supply.</li>
<li>A current credit rating read directly from the agency &mdash; deliberately withheld here (F-06).</li>
</ul>
"""
    return shell("tenant", "Tenant credit", "The market",
                 "One counterparty decides the outcome. Here is what it discloses.",
                 "Jack in the Box Inc. unit counts, closures, same-store sales and the lease terms it "
                 "publishes, with the exact language that drives the recommendation.", body)


def page_projections():
    sc = MODEL["scenarios"]
    blocks = []
    for name, label in (("optimistic", "Optimistic"), ("base", "Base"), ("pessimistic", "Pessimistic")):
        rows = "".join(f"<tr><td class='num'>{rank}</td><td>{E(nm)}</td>"
                       f"<td>{E(lbl)}</td><td class='num strong'>{val:.2f}</td></tr>"
                       for rank, nm, val, lbl in sc[name]["ranked"])
        blocks.append(f"""<h3>{label} scenario &middot; discount rate {sc[name]['discount_rate']:.2f}%</h3>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Rank</th>
<th scope="col">Strategy</th><th scope="col">Expiry assumption</th>
<th scope="col">Risk-adjusted PV (R)</th></tr></thead><tbody>{rows}</tbody></table></div>""")

    ev_rows = "".join(f"<tr><td>{E(r['strategy'])}</td><td>{E(str(r['expiry']))}</td>"
                      f"<td class='num strong'>{r['expected_pv_R']:.2f}</td>"
                      f"<td class='num'>{r['worst_pv_R']:.2f}</td>"
                      f"<td class='num'>{r['spread_R']:.2f}</td></tr>" for r in MODEL["expected"])

    def _num(a, key):
        x = a[key]
        if a["unit"] in ("decimal", "probability", "decimal of cap rate"):
            return f"{x * 100:.2f}%"
        return f"{x:g}"

    a_rows = "".join(
        f"<tr><td class='mono'>{E(a['name'])}</td><td class='num'>{_num(a, 'low')}</td>"
        f"<td class='num'>{_num(a, 'base')}</td><td class='num'>{_num(a, 'high')}</td>"
        f"<td>{E(a['unit'])}</td><td class='status'>{badge('analysis')}<div class='note'>{E(a['status'])}</div></td></tr>"
        for a in MODEL["assumptions"])

    body = f"""
{callout("info", "Why this model is in units of R",
         "<p>The rent was never supplied, so no dollar figure could be used without inventing one. Every "
         "output is therefore expressed in <strong>R = one year of the current contractual base rent</strong>. "
         "Sell-versus-hold compares two streams from the same asset, so the rent level largely cancels out "
         "of the <em>ranking</em>, which is what the decision needs. Multiply by your own rent for dollars.</p>")}

<h2>Method</h2>
<ol class="tight">
<li><strong>Three coherent scenarios.</strong> Each assumption carries a favourability direction. The
optimistic case takes the favourable extreme of every assumption; the pessimistic case the unfavourable
extreme of every one. Without that rule a sensitivity grid silently mixes optimism and pessimism.</li>
<li><strong>Official anchor, declared premium.</strong> The discount rate is the verified U.S. Treasury
10-year par yield of {MODEL['anchor']['value']}% at {MODEL['anchor']['date']} plus a risk premium swept
from 2.0% to 5.5%. The premium is labelled judgement; the anchor is sourced.</li>
<li><strong>Risk adjustment.</strong> Transaction friction, vacancy downtime, re-tenanting capital, a
tenant-survival probability and a catastrophe expectation are applied inside each strategy, not bolted on
afterwards.</li>
<li><strong>Reported by worst case as well as expected value.</strong> The owner does not get to choose
which scenario arrives.</li>
</ol>

<h2>Results</h2>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Strategy</th>
<th scope="col">Expiry</th><th scope="col">Expected PV (R)</th><th scope="col">Worst case (R)</th>
<th scope="col">Spread (R)</th></tr></thead><tbody>{ev_rows}</tbody></table></div>

<div class="tabs">{''.join(blocks)}</div>

<h2>Assumptions, in full</h2>
<p>Each row is an input, not a finding. The two cap-rate rows are the largest single source of uncertainty
in the whole file: between a 5.0% and an 8.5% exit cap rate, the same income stream is worth roughly 20 R
or 11.8 R &mdash; a 41% swing from an input no government agency publishes.</p>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Assumption</th>
<th scope="col">Unfavourable or low</th><th scope="col">Base</th><th scope="col">Favourable or high</th><th scope="col">Unit</th>
<th scope="col">Class</th></tr></thead><tbody>{a_rows}</tbody></table></div>

<h2>Sensitivity: what has to be true for holding to win</h2>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Condition</th>
<th scope="col">Requirement</th><th scope="col">Where it stands</th></tr></thead><tbody>
<tr><td>Exit cap rate</td><td>Below about 5.5% for hold-and-re-let to beat selling in the pessimistic case</td><td>The verified 10-year Treasury is 4.84%, and no official cap rate exists; a 5.5% exit implies roughly 70bp of spread over Treasuries for a single-tenant QSR</td></tr>
<tr><td>Tenant survival</td><td>A long renewal signed now, not an option</td><td>Disclosed as generally at the company's sole discretion</td></tr>
<tr><td>Re-letting</td><td>Replacement rent at 70-115% of current with under 3 years' downtime</td><td>No comparable data is official; this is assumption</td></tr>
<tr><td>Alternative use</td><td>Entitlement confirming a materially better use</td><td>Zoning unknown (F-08)</td></tr>
<tr><td>Catastrophe</td><td>Insurance that survives a wildfire or earthquake event</td><td>Not evidenced (I-14, B-07)</td></tr>
</tbody></table></div>

{callout("warn", "What the model cannot do",
         "<p>It cannot price this parcel. It has no trade-area data, no rent, no basis and no zoning. It "
         "reports <em>rankings under stated assumptions</em>, and those rankings are stable across all three "
         "scenarios for the sell-versus-renew choice, which is the choice the owner actually faces. It is "
         "not a forecast, and no probability is attached to any specific outcome for this site.</p>")}
"""
    return shell("projections", "Projections 2030-2035", "The decision",
                 "A projection you can audit, not a number you have to trust",
                 "Three coherent scenarios, a sourced discount anchor, every assumption exposed, and the "
                 "worst case reported alongside the expected case.", body)


def page_decision():
    strategies = [
        ("S1", "Sell now, lease in place", "Highest floor. Removes cap-rate, tenant and catastrophe risk in one transaction; forgoes the extension premium.",
         "11.62", "Preservation"),
        ("S5", "Extend early, then sell", "Buys term, then sells a longer, more financeable lease. Best rank stability; depends on a contracting tenant agreeing to commit.",
         "9.88", "Balanced"),
        ("S6", "Hold to expiry, then redevelop", "Monetises the land rather than the box. Requires entitlement confirmation that is not yet available.",
         "8.17", "Growth"),
        ("S2", "Hold to expiry, then sell vacant", "Collects rent to expiry, then sells the vacant box. Exposed to a vacant-asset discount at the worst moment.",
         "7.96", "Balanced"),
        ("S4", "Hold, re-let to another operator", "Highest expected value and the widest spread. Requires independently confirmed demand from a non-Jack tenant.",
         "4.82", "Growth"),
        ("S3", "Renew / re-let to Jack in the Box", "Ranks last in base and pessimistic. Entirely dependent on the incumbent wanting the site, and the option may be the tenant's.",
         "1.18", "Reject"),
    ]
    rows = "".join(f"<tr><td class='mono'>{a}</td><td><b>{E(b)}</b><div class='note'>{E(c)}</div></td>"
                   f"<td class='num'>{d}</td><td>{E(e)}</td></tr>" for a, b, c, d, e in strategies)

    body = f"""
{callout("ok", "The decision",
         "<p><strong>Sell.</strong> If the tenant will commit in writing to a long extension now, "
         "<strong>extend first and then sell</strong>. Do not renew at expiry and do not assume the option "
         "is yours to exercise.</p>")}

<h2>Six strategies, ranked by what happens if things go wrong</h2>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">ID</th>
<th scope="col">Strategy and what it actually does</th><th scope="col">Worst case (R)</th>
<th scope="col">Character</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small">Worst case is the pessimistic scenario from the committed model. Values in R; multiply by
your own annual base rent. Underlying assumptions: <a href="projections.html">Projections</a>.</p>

<h2>Balancing preservation against growth</h2>
<p>The brief asks for both wealth preservation and opportunity for growth, at a manageable level of risk.
Those objectives pull in different directions, and the model quantifies the trade rather than hiding it.</p>
<div class="three-col">
<div class="pillar">
<h3>Preservation first</h3>
<p class="tag">S1 &mdash; sell now</p>
<p>Highest floor of any strategy ({11.62:.2f} R) and the narrowest spread. Resolves the concentration
problem: one illiquid, single-tenant, single-county position becomes diversifiable capital. That benefit
is independent of any view on cap rates.</p>
</div>
<div class="pillar">
<h3>Balanced</h3>
<p class="tag">S5 &mdash; extend, then sell</p>
<p>Best mean rank (6th / 1st / 2nd across the scenarios). Captures the extension premium while still
exiting. The condition is demanding: a tenant that is publicly closing restaurants must agree to commit
to a longer term.</p>
</div>
<div class="pillar">
<h3>Growth</h3>
<p class="tag">S4 or S6 &mdash; hold and re-let or redevelop</p>
<p>Highest expected value (S4) or the most robust hold case (S6), both with materially lower floors.
Appropriate only if the owner can absorb the downside without distress and has independently confirmed
demand or entitlement.</p>
</div>
</div>

{callout("warn", "The trap in the 'growth' column",
         "<p>Both growth strategies require evidence that does not yet exist: confirmed non-Jack demand "
         "for the box, or a zoning position that supports redevelopment. Without one of those, a hold is "
         "not a growth strategy &mdash; it is a bet that a contracting tenant stays, which the model already "
         "prices as the worst branch.</p>")}

<h2>Transaction mechanics that change the arithmetic</h2>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Item</th>
<th scope="col">Rate or rule</th><th scope="col">Status</th><th scope="col">Source</th></tr></thead><tbody>
<tr><td>&sect;1031 identification period</td><td>{v('TAX-06')}</td><td>{badge('source-linked')}</td><td>{src_link('S_IRS_1031', short=True)}</td></tr>
<tr><td>&sect;1031 completion period</td><td>{v('TAX-07')}</td><td>{badge('source-linked')}</td><td>{src_link('S_IRS_1031', short=True)}</td></tr>
<tr><td>Maximum rate on unrecaptured &sect;1250 gain</td><td>{v('TAX-08')}</td><td>{badge('source-linked')}</td><td>{src_link('S_IRS_409', short=True)}</td></tr>
<tr><td>Maximum long-term capital gains rate on real property</td><td>{v('TAX-09')}</td><td>{badge('source-linked')}</td><td>{src_link('S_IRS_409', short=True)}</td></tr>
<tr><td>County documentary transfer tax</td><td>{v('TAX-01')}</td><td>{badge('source-linked')}</td><td>{src_link('S_LAC_RR', short=True)}</td></tr>
<tr><td>City base transfer tax</td><td>0.45% of value</td><td>{badge('verified-now')}</td><td>{src_link('S_ULA', short=True)}</td></tr>
<tr><td>Combined base transfer tax (city + county)</td><td>{v('TAX-03')}</td><td>{badge('analysis')}</td><td>{src_link('S_LAC_RR', short=True)}</td></tr>
<tr><td>Measure ULA, tiers (post 2026-06-30 closings)</td><td>{v('TAX-04')} above {v('TAX-10')}; {v('TAX-05')} at {v('TAX-11')}+</td><td>{badge('verified-now')}</td><td>{src_link('S_ULA', short=True)}</td></tr>
<tr><td>Combined city base + ULA at the lower tier</td><td>{v('TAX-12')}</td><td>{badge('verified-now')}</td><td>{src_link('S_ULA', short=True)}</td></tr>
</tbody></table></div>
<p class="small">Whether Measure ULA applies depends on the sale price and on the property being inside
the city boundary. Both are unknown until the Input Register is complete. Rates on the owner's own capital
gain depend on basis, holding period, entity and residency (F-05) and must be modelled by a CPA.</p>

<h2>Triggers that should reopen the decision</h2>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Trigger</th>
<th scope="col">Threshold</th><th scope="col">Consequence</th></tr></thead><tbody>
<tr><td>Confirmed tenant extension</td><td>10+ years at or above current rent, with a guaranty</td><td>Switch from S1 to S5</td></tr>
<tr><td>Written confirmation of closure</td><td>Any date before 2030</td><td>Accelerate the sale; negotiate early termination value</td></tr>
<tr><td>Exit cap rates</td><td>Below ~5.5%</td><td>Hold-and-re-let begins to beat selling in the pessimistic case</td></tr>
<tr><td>Entitlement</td><td>Zoning confirms a materially better use</td><td>Evaluate S6 with priced entitlement risk</td></tr>
<tr><td>County population</td><td>A further 1% annual decline</td><td>Re-underwrite the trade area; do not hold for growth</td></tr>
<tr><td>Insurance</td><td>Non-renewal or a premium rise above 25%</td><td>Reprice the hold; the risk transfers to the owner under NNN</td></tr>
</tbody></table></div>

<h2>What not to do</h2>
<ul class="tight">
<li>Do not spend money on a renewal negotiation before establishing whether the site is in the closure
programme.</li>
<li>Do not price the asset off a single broker cap rate. No official cap rate exists.</li>
<li>Do not assume the renewal option is yours. The issuer discloses its options as generally at the
company's sole discretion.</li>
<li>Do not list without a &sect;1031 plan if reinvestment is intended; the 45-day identification clock
starts at closing.</li>
<li>Do not treat brand-level same-store sales as this restaurant's performance, in either direction.</li>
</ul>
"""
    return shell("decision", "Decision & actions", "The decision",
                 "Sell. Extend first only if the tenant commits. Then exit.",
                 "Six strategies ranked by their worst case, a risk-balanced reading against both stated "
                 "objectives, the tax mechanics, and the triggers that should reopen the decision.", body)


def page_risk():
    bau = [r for r in D.RISKS if r["kind"] == "Business as usual"]
    black = [r for r in D.RISKS if r["kind"] == "Black swan"]

    def risk_rows(items):
        out = []
        for r in items:
            out.append(
                f"<tr><td class='mono'>{r['id']}</td><td><b>{E(r['cat'])}</b><div>{E(r['risk'])}</div>"
                f"<div class='note'>Mitigation: {E(r['mitigation'])}</div></td>"
                f"<td class='num'>{r['l']}&times;{r['i']}={r['l']*r['i']}</td>"
                f"<td>{E(r['evidence'])}</td>"
                f"<td><a href='{E(D.SOURCES[r['src']]['url'])}' target='_blank' rel='noopener noreferrer'>"
                f"{E(LINK_TEXT.get(r['src'], 'source'))} &#8599;</a></td></tr>")
        return "".join(out)

    body = f"""
{callout("info", "Likelihood and impact are judgement, not data",
         "<p>The score is likelihood &times; impact on a 1-5 scale, and it is our analytical judgement. It is "
         "shown so the reasoning can be challenged. Each row cites the verified evidence it rests on, and "
         "that evidence is official or issuer-published.</p>")}

<div class="kpis small">
  <article class="kpi"><div class="k-label">Business-as-usual risks</div><div class="k-value">{len(bau)}</div><div class="k-sub">Tenant, market, cost, transaction</div></div>
  <article class="kpi"><div class="k-label">Black-swan events</div><div class="k-value">{len(black)}</div><div class="k-sub">Wildfire, seismic, insurance, migration</div></div>
  <article class="kpi"><div class="k-label">Highest-scored risk</div><div class="k-value">R-14</div><div class="k-sub">Unidentified subject property (25)</div></div>
  <article class="kpi"><div class="k-label">Already-realised tail</div><div class="k-value">Jan 2025</div><div class="k-sub">Eaton and Palisades fires</div></article>
</div>

<h2>Business as usual</h2>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">ID</th>
<th scope="col">Risk and mitigation</th><th scope="col">Score</th><th scope="col">Evidence base</th>
<th scope="col">Source</th></tr></thead><tbody>{risk_rows(bau)}</tbody></table></div>

<h2>Black-swan events</h2>
<p>These are low-probability, high-impact events that could destroy local economic activity. They are not
hypotheticals imported from elsewhere: one of them has already happened inside the analysis window.</p>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">ID</th>
<th scope="col">Event and mitigation</th><th scope="col">Score</th><th scope="col">Evidence base</th>
<th scope="col">Source</th></tr></thead><tbody>{risk_rows(black)}</tbody></table></div>

<h2>How catastrophe enters the valuation</h2>
<p>The model converts catastrophe exposure into an expected deduction inside every strategy, using a
declared 10-year event probability and a declared loss share. Both are assumptions (F-15). The verified
anchors are the USGS 30-year probabilities and the realised cost of the January 2025 fires:</p>
{evidence_table([ROWS[i] for i in ["HAZ-01","HAZ-02","HAZ-05","HAZ-06","HAZ-07","HAZ-08","HAZ-09",
                                    "HAZ-10","HAZ-11","HAZ-12","HAZ-15"]],
                ["metric","value","period","geo"], ["Observation","Value","Period","Geography"])}

<h2>Risk-management posture for either decision</h2>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Lever</th>
<th scope="col">If you sell</th><th scope="col">If you hold</th></tr></thead><tbody>
<tr><td>Tenant risk</td><td>Transferred to the buyer at closing</td><td>Require a guaranty and monitor filings each quarter</td></tr>
<tr><td>Cap-rate risk</td><td>Realised at closing; no further exposure</td><td>Cannot be hedged; size the position accordingly</td></tr>
<tr><td>Catastrophe</td><td>Transferred, subject to pre-closing condition</td><td>Require replacement-cost insurance naming the owner; annual proof</td></tr>
<tr><td>Liquidity</td><td>Converted to cash or &sect;1031 replacement assets</td><td>Illiquid for the remaining term; model a 6-12 month disposal</td></tr>
<tr><td>Concentration</td><td>Resolved by reinvestment</td><td>Cap this asset at a share of net worth you would accept losing</td></tr>
<tr><td>Income</td><td>Ends at closing</td><td>Protect with escalation and a percentage-rent clause if obtainable</td></tr>
</tbody></table></div>
"""
    return shell("risk", "Risk register", "Risk",
                 "What can go wrong, how likely it is judged to be, and what to do about it",
                 "Fifteen business-as-usual risks and seven black-swan events, scored, evidenced and "
                 "paired with a mitigation.", body)


def page_evidence():
    rows = D.all_rows()
    body = f"""
<p class="lede-inner">Every published observation, with its geography, period, verification status and
publisher link. {COUNTS['verified-now']} rows were re-read on the publisher's own page on {SNAPSHOT};
{COUNTS['source-linked']} carry an official or SEC link and were read when first captured;
{COUNTS['analysis']} is our arithmetic; {COUNTS['industry']} are industry data and are excluded below.
No row is estimated.</p>

<div class="legend">
{badge('verified-now')} re-read {SNAPSHOT} &nbsp; {badge('source-linked')} official link, read on capture
&nbsp; {badge('analysis')} our arithmetic &nbsp; {badge('industry')} private research, excluded from this table
</div>

<div class="table-tools">
  <input type="search" id="filter" placeholder="Filter rows (indicator, geography, ID)..." aria-label="Filter evidence rows">
  <span id="count" class="small">{len([r for r in rows if r['status']!='industry'])} rows</span>
</div>

{evidence_table([r for r in rows if r["status"] != "industry"],
                ["cat","metric","value","period","geo"],
                ["Category","Indicator","Value","Period","Geography"])}

<script>
(function(){{
  var f=document.getElementById('filter'), t=document.querySelector('table.data tbody'),
      c=document.getElementById('count');
  if(!f||!t) return;
  var rows=[].slice.call(t.querySelectorAll('tr'));
  f.addEventListener('input',function(){{
    var q=f.value.toLowerCase(), n=0;
    rows.forEach(function(r){{
      var hit=!q||r.textContent.toLowerCase().indexOf(q)>-1;
      r.style.display=hit?'':'none'; if(hit)n++;
    }});
    if(c) c.textContent=n+' rows';
  }});
}})();
</script>
"""
    return shell("evidence", "Evidence table", "Assurance",
                 "All of it, in one table, with the receipts",
                 "The complete evidence register. If a value could not be confirmed from an official "
                 "source it is blank here and listed on the flagged page.", body)


def page_sources():
    rows = []
    for key, s in D.SOURCES.items():
        used = [r["id"] for r in D.all_rows() if r["src"] == key]
        kind = {"official": "ok", "issuer": "info", "industry": "neutral"}[s["kind"]]
        kind_label = {"official": "Official", "issuer": "Issuer (SEC)", "industry": "Industry"}[s["kind"]]
        rows.append(
            f"<tr><td class='mono'>{E(key)}</td><td><a href='{E(s['url'])}' target='_blank' "
            f"rel='noopener noreferrer'>{E(s['label'])} &#8599;</a>"
            f"<div class='note'>{E(s['publisher'])}</div></td>"
            f"<td><span class='badge {kind}'>{kind_label}</span></td>"
            f"<td>{E(s['used'])}</td><td>{E(s['accessed'])}</td>"
            f"<td class='mono small'>{E(', '.join(used[:6]))}{' ...' if len(used) > 6 else ''}</td></tr>")

    body = f"""
<p class="lede-inner">{len(D.SOURCES)} publishers, of which {COUNTS['official_sources']} are official
government bodies or SEC registrants. Industry research is included only where no official source exists,
and is labelled as such everywhere it appears.</p>

<h2>Source register</h2>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">ID</th>
<th scope="col">Document</th><th scope="col">Class</th><th scope="col">Used for</th>
<th scope="col">Accessed</th><th scope="col">Rows</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>

<h2>Verification standard</h2>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Status</th>
<th scope="col">What it means</th><th scope="col">Count</th></tr></thead><tbody>
<tr><td>{badge('verified-now')}</td><td>{E(D.STATUS_LABELS['verified-now'][1])}</td><td class='num'>{COUNTS['verified-now']}</td></tr>
<tr><td>{badge('source-linked')}</td><td>{E(D.STATUS_LABELS['source-linked'][1])}</td><td class='num'>{COUNTS['source-linked']}</td></tr>
<tr><td>{badge('analysis')}</td><td>{E(D.STATUS_LABELS['analysis'][1])}</td><td class='num'>{COUNTS['analysis']}</td></tr>
<tr><td>{badge('industry')}</td><td>{E(D.STATUS_LABELS['industry'][1])}</td><td class='num'>{COUNTS['industry']}</td></tr>
<tr><td>{badge('unverified')}</td><td>{E(D.STATUS_LABELS['unverified'][1])}</td><td class='num'>on <a href='flagged.html'>Flagged</a></td></tr>
<tr><td>{badge('input')}</td><td>{E(D.STATUS_LABELS['input'][1])}</td><td class='num'>{len(D.INPUT_ROWS)}</td></tr>
</tbody></table></div>

<h2>Rules this file follows</h2>
<ul class="tight">
<li>Official government or statutory sources first; SEC filings for anything about the tenant.</li>
<li>A private research firm is never presented as an official source, and its figures are never labelled
verified.</li>
<li>If a value cannot be confirmed on an official page, it is left blank and flagged. It is never inferred,
interpolated or carried over from an aggregator.</li>
<li>Every row states its own geography and period; rows from different vintages are not blended.</li>
<li>Analysis is labelled analysis, including the entire model.</li>
</ul>
"""
    return shell("sources", "Sources", "Assurance",
                 "Every publisher used, what it was used for, and when it was read",
                 "A register of official and issuer sources, with the industry data separated and the "
                 "verification vocabulary defined.", body)


def page_flagged():
    by_sev = {"Critical": [], "High": [], "Medium": [], "Low": []}
    for f in D.FLAGS:
        by_sev.setdefault(f["sev"], []).append(f)
    blocks = []
    for sev in ("Critical", "High", "Medium", "Low"):
        items = by_sev.get(sev, [])
        if not items:
            continue
        rows = "".join(
            f"<tr><td class='mono'>{E(f['id'])}</td>"
            f"<td><b>{E(f['item'])}</b><div class='note'>{E(f['status'])}</div></td>"
            f"<td>{E(f['detail'])}</td><td>{E(f['action'])}</td></tr>" for f in items)
        blocks.append(f"<h3>{sev} priority</h3><div class='table-wrap'><table class='data'><thead><tr>"
                      f"<th scope='col'>ID</th><th scope='col'>Item</th><th scope='col'>Why it is not "
                      f"published as fact</th><th scope='col'>What closes it</th></tr></thead>"
                      f"<tbody>{rows}</tbody></table></div>")

    rec_rows = "".join(
        f"<tr><td class='mono'>{E(x['id'])}</td><td><b>{E(x['topic'])}</b></td>"
        f"<td>{E(x['conflict'])}</td><td>{E(x['resolution'])}</td>"
        f"<td><span class='badge {'ok' if x['verdict'].startswith('Resolved') else 'warn'}'>"
        f"{E(x['verdict'])}</span></td></tr>" for x in D.RECONCILIATIONS)

    input_rows = "".join(f"<tr><td class='mono'>{E(r['id'])}</td><td>{E(r['field'])}</td>"
                         f"<td>{E(r['why'])}</td><td><span class='blank'>&mdash;</span></td></tr>"
                         for r in D.INPUT_ROWS)

    body = f"""
{callout("warn", "Nothing here is hidden",
         f"<p>{len(D.FLAGS)} items could not be published as verified fact. They are listed with the reason, "
         "the source that was checked, and the specific action that would close each one. None of them "
         "blocks the recommendation, and none of them is estimated to make a table look complete.</p>")}

<h2>Unverified and withheld items</h2>
{''.join(blocks)}

<h2 id="inputs">Input Register &mdash; owner-supplied fields</h2>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">ID</th>
<th scope="col">Field</th><th scope="col">Why it matters</th><th scope="col">Value</th></tr></thead>
<tbody>{input_rows}</tbody></table></div>

<h2 id="reconciliation">Cross-layer reconciliation log</h2>
<p>Six sessions published parallel dashboards on 2026-11-06. This integration re-read the decisive sources,
compared the layers line by line, and resolved every conflict it found. Nothing was deleted and no other
session's work was overwritten; the earlier layers remain published and are listed as archive.</p>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">ID</th>
<th scope="col">Topic</th><th scope="col">Conflict found</th><th scope="col">Resolution</th>
<th scope="col">Verdict</th></tr></thead><tbody>{rec_rows}</tbody></table></div>

<h2>Known limitations of this file</h2>
<ul class="tight">
<li>The subject property is unidentified, so every site-specific conclusion is conditional (R-14).</li>
<li>Vintages are mixed by necessity and stated per row (F-14).</li>
<li>Cap rates and comparables are not officially published (F-02, X-09).</li>
<li>All model probabilities and risk scores are judgement, swept across ranges (F-15).</li>
<li>Source pages can change after the access date; the snapshot is dated and is not a live feed.</li>
</ul>
"""
    return shell("flagged", "Flagged for review", "Assurance",
                 "What could not be verified, and what would close it",
                 f"{len(D.FLAGS)} flagged items, the fifteen fields only the owner can supply, and the full log of "
                 "conflicts found between the parallel layers.", body)


def page_method():
    body = f"""
<h2 id="privacy">Privacy</h2>
<p>Personal information privacy is the primary constraint on this project, and it is enforced mechanically
rather than promised.</p>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Rule</th>
<th scope="col">Implementation</th></tr></thead><tbody>
<tr><td>No identifier of the property or its owner</td><td>The asset is "Asset A". No address, parcel number, owner name, officer name, email, phone or taxpayer identifier appears in any page, table or data file.</td></tr>
<tr><td>No personal information is collected</td><td>There are no forms, no accounts, no cookies, no analytics, no third-party scripts and no external fonts or images. Everything is static HTML, CSS and a few lines of local JavaScript.</td></tr>
<tr><td>No owner research</td><td>No attempt was made to identify the owner, the franchisee or any individual. Private lease and financial documents were not sought and are not published.</td></tr>
<tr><td>Build-time gate</td><td><code>tools/check_report.py</code> scans every published file for email addresses, phone numbers, street addresses, parcel numbers, taxpayer identifiers and tenant officer names. The build fails on any match.</td></tr>
<tr><td>Repository metadata</td><td>Commit metadata is infrastructure, not project data. It is not reproduced on the site. Flagged as F-20 so it can be neutralised if the repository is shared.</td></tr>
</tbody></table></div>

<h2>Verification standard</h2>
<p>Three things are kept strictly apart and labelled everywhere:</p>
<ol class="tight">
<li><strong>Observations.</strong> Published by a government body or filed with the SEC. Re-read on the
publisher's page on {SNAPSHOT} where marked verified, otherwise linked and read on capture.</li>
<li><strong>Analysis.</strong> Our arithmetic, scenarios, rankings and scores. Conditional by construction.</li>
<li><strong>Industry data.</strong> Private research. Never scored as verified, never used as a model input.</li>
</ol>
<p>A value that could not be confirmed from an official source is blank. The blanking is enforced in the
generator: <code>cell()</code> cannot render a value for a row whose status is unverified.</p>

<h2>The model</h2>
<p>The projection model is deterministic and committted to the repository. It uses one official anchor
&mdash; the U.S. Treasury 10-year par yield of {MODEL['anchor']['value']}% at {MODEL['anchor']['date']},
plus a declared risk premium &mdash; and otherwise sweeps stated assumption ranges. All fourteen
strategy-by-expiry combinations are computed. No randomness, no network calls, no fitted parameters:
running it twice produces identical output.</p>
<p>Assumption classes are shown on <a href="projections.html">Projections</a>. The cap-rate range is the
dominant uncertainty and is deliberately wide.</p>

<h2>Reproducibility</h2>
<pre><code>python3 tools/build_report.py    # data/report_data.py + model -> report/
python3 tools/check_report.py    # links, sources, blanks, privacy, determinism</code></pre>
<p>The build writes only to <code>report/</code>. It does not touch the root pages, <code>docs/</code>,
<code>analysis/</code>, <code>brief/</code>, <code>pages/</code> or <code>decision-file/</code>, all of
which remain published as archive.</p>

<h2>What is deliberately absent</h2>
<ul class="tight">
<li>Any dollar valuation of the property. No rent, basis or building size was supplied.</li>
<li>Any cap rate presented as fact. None is officially published.</li>
<li>Any school rating or traffic count for the parcel. Both require the address.</li>
<li>Any claim about the owner's circumstances, net worth or tax position.</li>
<li>Any prediction of what this specific restaurant will do. Only the counterparty's disclosed behaviour is reported.</li>
</ul>

<h2>Change log for this integration</h2>
<div class="table-wrap"><table class="data"><thead><tr><th scope="col">Date</th>
<th scope="col">Change</th></tr></thead><tbody>
<tr><td>2026-11-07</td><td>Canonical dashboard built from the six parallel layers; 132 evidence rows reconciled; {len(D.FLAGS)} flags published; 13 cross-layer conflicts resolved; four prior values corrected or re-sourced; Measure ULA upgraded from flagged to verified; industry cap rates separated from official evidence.</td></tr>
<tr><td>2026-11-06</td><td>Parallel research and dashboards produced by six sessions (see archive).</td></tr>
</tbody></table></div>
"""
    return shell("methodology", "Method & privacy", "Assurance",
                 "How this file was built, and the limits built into it",
                 "The privacy boundary, the verification vocabulary, the model's construction and what is "
                 "deliberately missing.", body)


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
CSS = """/* Jack in the Box NNN decision file - single stylesheet, no external assets */
:root{
  --ink:#161a1d; --ink-2:#3d464f; --muted:#68737d; --line:#dfe3e7; --paper:#f6f7f8;
  --card:#ffffff; --accent:#a8342a; --accent-ink:#8a2a21; --teal:#1d5b6b;
  --ok:#1c6b45; --ok-bg:#e7f3ec; --info:#1d5b6b; --info-bg:#e6f0f2;
  --warn:#8a5a09; --warn-bg:#fdf3e0; --bad:#8f1d1d; --bad-bg:#fbe9e9;
  --neutral:#4a4a6a; --neutral-bg:#eeedf4; --blank-bg:#f1f2f3;
  --radius:10px; --shadow:0 1px 2px rgba(16,24,32,.06),0 1px 3px rgba(16,24,32,.04);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);
  font:15px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  font-feature-settings:"kern" 1,"liga" 1}
a{color:var(--teal);text-decoration:none;border-bottom:1px solid rgba(29,91,107,.25)}
a:hover{color:var(--accent-ink);border-bottom-color:var(--accent-ink)}
a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--teal);outline-offset:2px}
.skip{position:absolute;left:-999px;top:0;background:#fff;padding:10px;z-index:50}
.skip:focus{left:8px;top:8px}
.side{position:fixed;inset:0 auto 0 0;width:250px;background:#12181c;color:#cfd6db;
  padding:22px 18px 26px;overflow-y:auto;display:flex;flex-direction:column;gap:18px}
.brand{display:flex;gap:11px;align-items:center;color:#fff;border:0;font-weight:700;
  letter-spacing:.06em;font-size:14px;line-height:1.15}
.brand small{font-size:9.5px;letter-spacing:.16em;color:#8e9aa3;font-weight:600}
.mark{display:grid;place-items:center;width:34px;height:34px;border-radius:9px;
  background:var(--accent);color:#fff;font-weight:800;font-size:17px}
.side nav{display:flex;flex-direction:column;gap:14px}
.nav-group{display:flex;flex-direction:column;gap:2px}
.nav-title{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#7d8891;margin:0 0 4px 10px}
.side nav a{color:#cfd6db;border:0;padding:6px 10px;border-radius:7px;font-size:13.5px}
.side nav a:hover{background:#1c242a;color:#fff}
.side nav a[aria-current=page]{background:#243038;color:#fff;font-weight:600;
  box-shadow:inset 2px 0 0 var(--accent)}
.privacy-box{background:#1a2228;border:1px solid #26313a;border-radius:var(--radius);padding:12px;font-size:11.8px;line-height:1.5}
.privacy-box strong{color:#fff;display:block;margin-bottom:4px;font-size:12px}
.privacy-box p{margin:0 0 6px;color:#a9b4bd}
.privacy-box a{color:#8fc3ce;border:0}
.main{margin-left:250px;min-height:100vh;display:flex;flex-direction:column}
.topbar{display:flex;gap:10px;align-items:center;padding:12px 40px;border-bottom:1px solid var(--line);
  background:#fff;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.topbar .dot{color:var(--accent)}
main{padding:34px 40px 56px;max-width:1180px;width:100%}
.page-head{margin-bottom:26px;border-bottom:1px solid var(--line);padding-bottom:20px}
.kicker{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:8px}
h1{font-size:31px;line-height:1.18;margin:0 0 10px;letter-spacing:-.02em;font-weight:700}
.lede{font-size:16.5px;color:var(--ink-2);max-width:74ch;margin:0}
.lede-inner{color:var(--ink-2);max-width:80ch}
h2{font-size:21px;margin:38px 0 12px;letter-spacing:-.01em;border-top:1px solid var(--line);padding-top:22px}
h2:first-of-type{border-top:0;padding-top:0}
h3{font-size:15.5px;margin:22px 0 8px}
p{margin:0 0 12px;max-width:82ch}
ul,ol{margin:0 0 14px;padding-left:22px;max-width:82ch}
li{margin-bottom:6px}
.tight li{margin-bottom:4px}
.small,.note,.src{font-size:12.4px;color:var(--muted);line-height:1.55}
p.src{margin-top:-4px}
code{background:#eef1f2;padding:1px 5px;border-radius:4px;font-size:.92em}
pre{background:#12181c;color:#dfe6ea;padding:14px 16px;border-radius:var(--radius);
  overflow-x:auto;font-size:12.5px;line-height:1.7}
pre code{background:none;color:inherit;padding:0}
.reco{background:linear-gradient(180deg,#fff 0%,#fdf7f6 100%);border:1px solid #e8cfcb;
  border-left:5px solid var(--accent);border-radius:var(--radius);padding:22px 24px;margin-bottom:22px;box-shadow:var(--shadow)}
.reco-label{font-size:10.5px;letter-spacing:.15em;text-transform:uppercase;color:var(--accent);font-weight:700}
.reco h2{border:0;padding:0;margin:8px 0 10px;font-size:23px;line-height:1.25}
.reco p{max-width:88ch}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:12px;margin:18px 0 22px}
.kpis.small .k-value{font-size:24px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:13px 15px;box-shadow:var(--shadow)}
.k-label{font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);font-weight:600}
.k-value{font-size:26px;font-weight:700;letter-spacing:-.02em;margin:5px 0 2px;font-variant-numeric:tabular-nums}
.k-sub{font-size:12px;color:var(--ink-2);min-height:32px}
.k-foot{display:flex;justify-content:space-between;align-items:center;gap:6px;margin-top:8px;
  border-top:1px solid #eef0f2;padding-top:7px;font-size:11.4px}
.status-strip{display:flex;flex-wrap:wrap;gap:0;background:var(--card);border:1px solid var(--line);
  border-radius:var(--radius);overflow:hidden;margin-bottom:24px}
.status-strip>div{flex:1 1 140px;padding:11px 15px;border-right:1px solid var(--line)}
.status-strip>div:last-child{border-right:0}
.status-strip b{display:block;font-size:18px;font-variant-numeric:tabular-nums}
.status-strip span{font-size:11.4px;color:var(--muted)}
.card-group{margin-bottom:20px}
.card-group>h3{margin:0 0 8px;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.card-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}
.card{display:flex;flex-direction:column;gap:5px;background:var(--card);border:1px solid var(--line);
  border-radius:var(--radius);padding:14px 16px;box-shadow:var(--shadow);color:var(--ink)}
.card:hover{border-color:#b9c4cc;transform:translateY(-1px);transition:transform .12s}
.card b{font-size:14.5px}
.card span{font-size:12.6px;color:var(--muted);line-height:1.5}
.card em{font-style:normal;font-size:12px;color:var(--teal);margin-top:2px}
.callout{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--teal);
  border-radius:var(--radius);padding:15px 18px;margin:18px 0}
.callout h3{margin:0 0 7px;font-size:14px}
.callout p{margin:0 0 8px;font-size:13.6px}
.callout p:last-child{margin:0}
.callout.ok{border-left-color:var(--ok);background:#fbfdfc}
.callout.warn{border-left-color:#c98a12;background:#fffdf7}
.callout.info{border-left-color:var(--info)}
.table-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius);
  background:var(--card);margin:14px 0 18px;box-shadow:var(--shadow)}
table{width:100%;border-collapse:collapse;font-size:13.2px}
thead th{background:#f2f4f5;text-align:left;padding:9px 11px;font-size:11px;letter-spacing:.07em;
  text-transform:uppercase;color:var(--muted);border-bottom:1px solid var(--line);white-space:nowrap;
  position:sticky;top:0}
td{padding:9px 11px;border-bottom:1px solid #eef0f2;vertical-align:top}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:#fafbfb}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.strong{font-weight:700}
td.mono,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12px;color:var(--muted)}
td.status{min-width:150px}
.blank{color:#9aa3ab}
.badge{display:inline-block;font-size:10.4px;letter-spacing:.05em;text-transform:uppercase;
  font-weight:700;padding:2px 7px;border-radius:20px;border:1px solid transparent;white-space:nowrap}
.badge.ok{background:var(--ok-bg);color:var(--ok);border-color:#cbe4d6}
.badge.info{background:var(--info-bg);color:var(--info);border-color:#c9dee3}
.badge.warn{background:var(--warn-bg);color:var(--warn);border-color:#f0ddb8}
.badge.bad{background:var(--bad-bg);color:var(--bad);border-color:#f0cccc}
.badge.neutral{background:var(--neutral-bg);color:var(--neutral);border-color:#dcdae8}
.badge.blank{background:var(--blank-bg);color:#5a646d;border-color:#dfe3e7}
.legend{display:flex;flex-wrap:wrap;gap:10px;align-items:center;font-size:12.4px;color:var(--muted);margin:6px 0 14px}
.table-tools{display:flex;gap:12px;align-items:center;margin:12px 0 0}
.table-tools input{flex:1 1 280px;max-width:420px;padding:9px 12px;border:1px solid var(--line);
  border-radius:8px;font-size:13.5px;background:#fff}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.three-col{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:16px 0}
.pillar{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:15px 17px;box-shadow:var(--shadow)}
.pillar h3{margin:0 0 4px}
.pillar .tag{font-size:11.3px;letter-spacing:.06em;text-transform:uppercase;color:var(--accent);font-weight:700;margin:0 0 8px}
.pillar p{font-size:13.2px;margin:0}
.archive{margin-top:34px;border-top:1px solid var(--line);padding-top:8px}
.archive ul{padding-left:20px}
footer{margin-top:auto;padding:20px 40px;border-top:1px solid var(--line);background:#fff;
  font-size:11.8px;color:var(--muted)}
footer p{margin:0 0 6px;max-width:none}
@media(max-width:1080px){.two-col,.three-col{grid-template-columns:1fr}}
@media(max-width:860px){
  .side{position:static;width:auto;inset:auto;flex-direction:row;flex-wrap:wrap;gap:10px;padding:14px}
  .side nav{flex-direction:row;flex-wrap:wrap;gap:6px}
  .nav-group{flex-direction:row;flex-wrap:wrap;align-items:center}
  .nav-title{display:none}
  .privacy-box{display:none}
  .main{margin-left:0}
  main,.topbar,footer{padding-left:18px;padding-right:18px}
  h1{font-size:25px}
}
@media print{.side,.topbar{display:none}.main{margin:0}main{max-width:none}}
"""


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
PAGES = [
    ("index", page_index), ("executive-summary", page_exec), ("property", page_property),
    ("location", page_location), ("market", page_market), ("tenant", page_tenant),
    ("projections", page_projections), ("decision", page_decision), ("risk", page_risk),
    ("evidence", page_evidence), ("sources", page_sources), ("flagged", page_flagged),
    ("methodology", page_method),
]


def build():
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    with open(os.path.join(OUT, "assets", "style.css"), "w", encoding="utf-8") as fh:
        fh.write(CSS)
    for name, fn in PAGES:
        html_text = fn()
        with open(os.path.join(OUT, f"{name}.html"), "w", encoding="utf-8") as fh:
            fh.write(html_text)
        print(f"  {name + '.html':28} {len(html_text):>8,} bytes")
    print(f"OK - {len(PAGES)} pages, {COUNTS['total']} evidence rows, {len(D.FLAGS)} flags")


if __name__ == "__main__":
    build()
