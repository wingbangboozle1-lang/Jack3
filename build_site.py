#!/usr/bin/env python3
"""Static site generator for the Jack3 decision dashboard.

Reads the verified data snapshot in data/*.py and the model in
model/projection.py, and writes plain HTML into docs/.  GitHub Pages serves
docs/ directly with no build step, so the published site cannot fail to deploy
because of a toolchain.

    python3 build_site.py

Design rules enforced here:
  * every data row renders its own source link, or renders blank + flagged;
  * a row with verified != "VERIFIED" never prints a value it does not have;
  * no property-identifying or personal information is emitted anywhere.
"""

from __future__ import annotations

import csv
import html
import io
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data import demographics, employment, tenant, hazards, analysis, flags  # noqa: E402
from model import projection as M  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
SITE = os.path.join(ROOT, "site")
SNAPSHOT = "2026-11-06"
REPO = "wingbangboozle1-lang/Jack3"


# ==========================================================================
# small helpers
# ==========================================================================
def esc(v) -> str:
    return html.escape("" if v is None else str(v), quote=True)


def is_verified(row) -> bool:
    return str(row.get("verified", "")).upper() == "VERIFIED"


def badge(text, cls):
    return f'<span class="badge {cls}">{esc(text)}</span>'


def verified_badge(row):
    v = str(row.get("verified", "")).upper()
    if v == "VERIFIED":
        return badge("Verified", "b-ok")
    if v.startswith("NO OFFICIAL"):
        return badge("No official source", "b-warn")
    return badge("Unverified", "b-bad")


def source_cell(row):
    url = row.get("source_url") or ""
    if not url:
        return '<span class="blank">&mdash;</span>'
    label = row.get("source_label") or url
    short = label if len(label) <= 64 else label[:61] + "..."
    return (f'<a class="src-link" href="{esc(url)}" target="_blank" '
            f'rel="noopener noreferrer" title="{esc(label)}">{esc(short)} &#8599;</a>')


def value_cell(row, key="value"):
    """Print the value, or an explicit blank marker.  Never invent one."""
    v = row.get(key)
    if v is None or v == "":
        return '<span class="blank">[ blank &mdash; unverified ]</span>'
    out = esc(v)
    note = row.get("note")
    if note:
        out += f'<span class="note">{esc(note)}</span>'
    return out


def score_cell(score):
    s = int(score or 0)
    cls = "s-crit" if s >= 20 else "s-high" if s >= 15 else "s-med" if s >= 8 else "s-low"
    pct = max(4, min(100, s / 25.0 * 100))
    return (f'<span class="score {cls}"><span class="bar">'
            f'<i style="width:{pct:.0f}%"></i></span>'
            f'<span class="n">{s}</span></span>')


# ==========================================================================
# table renderer
# ==========================================================================
def table(rows, cols, name, title=None, note=None, row_class=None):
    """cols = list of (key, header, css, kind)
    kind: text | num | html | src | vbadge | score | raw
    """
    buf = io.StringIO()
    buf.write(f'<div class="table-card" data-table-name="{esc(name)}">')
    if title or note:
        buf.write('<div class="table-head">')
        if title:
            buf.write(f'<h3>{esc(title)}</h3>')
        if note:
            buf.write(f'<div class="note">{esc(note)}</div>')
        buf.write('<div class="table-tools">'
                  f'<input type="search" data-filter placeholder="Filter {esc(name)}..." aria-label="Filter">'
                  '<button class="btn" data-export type="button">CSV</button>'
                  '</div></div>')
    buf.write('<div class="scroll"><table><thead><tr>')
    for key, head, css, kind in cols:
        buf.write(f'<th class="{css}">{esc(head)}</th>')
    buf.write('</tr></thead><tbody>')
    for r in rows:
        rc = row_class(r) if row_class else ""
        buf.write(f'<tr class="{rc}">')
        for key, head, css, kind in cols:
            if kind == "src":
                cell = source_cell(r)
            elif kind == "vbadge":
                cell = verified_badge(r)
            elif kind == "score":
                cell = score_cell(r.get(key))
            elif kind.startswith("rawurl"):
                u = r.get(key) or ""
                cell = (f'<a class="src-link" href="{esc(u)}" target="_blank" '
                        f'rel="noopener noreferrer">Open &#8599;</a>'
                        if u else '<span class="blank">&mdash;</span>')
            elif kind.startswith(("rawpri","rawst","rawsev")):
                v = r.get(key) or ""
                cls = {"DECISION-CRITICAL": "b-bad", "High": "b-warn", "Medium": "b-info",
                       "VERIFIED": "b-ok", "NO OFFICIAL SOURCE": "b-warn",
                       "INPUT REQUIRED": "b-bad"}.get(v, "b-neutral")
                cell = badge(v, cls) if v else '<span class="blank">&mdash;</span>'
            elif kind == "raw":
                cell = r.get(key) or ""
            elif kind == "value":
                cell = value_cell(r, key or "value")
            else:
                v = r.get(key)
                if v is None or v == "":
                    cell = '<span class="blank">&mdash;</span>'
                else:
                    n = r.get("note") if kind == "textn" else None
                    cell = esc(v) + (f'<span class="note">{esc(n)}</span>' if n else "")
            buf.write(f'<td class="{css}">{cell}</td>')
        buf.write('</tr>')
    buf.write('</tbody></table></div></div>')
    return buf.getvalue()


# ==========================================================================
# page chrome
# ==========================================================================
NAV = [
    ("Overview", [
        ("index.html", "Dashboard"),
        ("executive-summary.html", "Executive Summary"),
        ("methodology.html", "Methodology & Verification"),
        ("privacy.html", "Privacy & Anonymisation"),
    ]),
    ("The Asset", [
        ("property-profile.html", "Property Profile & Inputs"),
        ("geography.html", "Geography & Market Definition"),
        ("lease-economics.html", "NNN Lease Economics"),
    ]),
    ("The Tenant", [
        ("tenant.html", "Tenant Credit (SEC filings)"),
        ("tenant-closures.html", "Closure Programme"),
    ]),
    ("The Market", [
        ("demographics.html", "Population & Income"),
        ("employment.html", "Employment & Wages"),
        ("projections.html", "Official Forecasts"),
        ("infrastructure.html", "Infrastructure & Schools"),
    ]),
    ("The Decision", [
        ("projection-model.html", "Projection Model"),
        ("valuation.html", "Valuation & Sensitivity"),
        ("decision.html", "Decision Framework"),
        ("taxes.html", "Tax & Transaction Framework"),
    ]),
    ("Risk", [
        ("risk-register.html", "Risk Register"),
        ("hazards.html", "Physical Hazards"),
        ("black-swan.html", "Black Swan Register"),
    ]),
    ("Assurance", [
        ("sources.html", "Source Register"),
        ("flagged-for-review.html", "Flagged for Review"),
        ("repo-review.html", "Repository Review"),
    ]),
]

FLAT = [(f, t, g) for g, items in NAV for f, t in items for g in [g]]
ORDER = [f for f, _, _ in FLAT]


def sidebar(active):
    out = ['<aside class="sidebar"><div class="brand">',
           '<span class="mark">J3</span><h1>Jack3</h1>',
           f'<p>NNN property decision file<br>Central Los Angeles<br>'
           f'Data snapshot {SNAPSHOT}</p></div><nav class="nav">']
    for group, items in NAV:
        out.append(f'<div class="nav-group"><div class="g-label">{esc(group)}</div>')
        for f, t in items:
            cls = ' class="active"' if f == active else ""
            out.append(f'<a href="{f}"{cls}><span class="dot"></span>{esc(t)}</a>')
        out.append('</div>')
    out.append('</nav></aside>')
    return "".join(out)


def topbar(active, group):
    title = dict(FLAT_NAMES).get(active, "")
    return (
        '<div class="topbar">'
        f'<div class="crumb">{esc(group)} &nbsp;/&nbsp; <b>{esc(title)}</b></div>'
        '<div class="spacer"></div>'
        '<span class="privacy-chip">No personal or property-identifying data published</span>'
        f'<span class="meta">snapshot {SNAPSHOT}</span>'
        '</div>'
    )


FLAT_NAMES = {f: (t, g) for f, t, g in [(f, t, g) for g, items in NAV for f, t in items]}
FLAT_NAMES = {f: t for g, items in NAV for f, t in items}
GROUP_OF = {f: g for g, items in NAV for f, t in items}


def footer():
    n_ver, n_un = 0, 0
    for mod in (demographics, employment, tenant, hazards):
        for tname, rows in mod.ALL_TABLES.items():
            for r in rows:
                if "verified" in r:
                    if is_verified(r):
                        n_ver += 1
                    else:
                        n_un += 1
    n_flag = len(flags.FLAGGED)
    n_src = len(flags.SOURCES)
    return f'''<div class="foot"><div class="cols">
<div><b>Verification.</b> {n_ver} data rows carry a source link to an official or
primary source. {n_un} rows could not be confirmed and are published blank and
flagged. {n_flag} items appear on
<a href="flagged-for-review.html">Flagged for Review</a>.</div>
<div><b>Sources.</b> {n_src} distinct official sources are listed in the
<a href="sources.html">Source Register</a> with publisher, filing date and
accession number where one exists.</div>
<div><b>Privacy.</b> No owner name, entity name, street address, parcel number,
contact detail or transaction price appears on this site. See
<a href="privacy.html">Privacy &amp; Anonymisation</a>.</div>
</div>
<p style="margin:14px 0 0">Built from a committed, reviewed data snapshot.
The site is static HTML served by GitHub Pages from <code>/docs</code>; it makes
no runtime calls to any API, so published figures cannot change silently.
Repository <code>{REPO}</code> &middot; generated {SNAPSHOT}.</p></div>'''


def page(fname, title, body, head_extra=""):
    doc = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} &middot; Jack3 Decision File</title>
<meta name="description" content="Verified market, tenant and risk analysis for a Jack in the Box NNN lease property in Central Los Angeles, lease expiry 2030-2035.">
<meta name="robots" content="noindex,nofollow">
<link rel="stylesheet" href="assets/style.css">
{head_extra}</head><body>
<div class="layout">
{sidebar(fname)}
<div class="main">
{topbar(fname, GROUP_OF.get(fname, ""))}
<div class="wrap">
{body}
{pager(fname)}
</div>
{footer()}
</div></div>
<script src="assets/app.js"></script>
</body></html>
'''
    return doc


def pager(fname):
    if fname not in ORDER:
        return ""
    i = ORDER.index(fname)
    prev_ = ORDER[i - 1] if i > 0 else None
    next_ = ORDER[i + 1] if i < len(ORDER) - 1 else None
    out = ['<div class="pager">']
    if prev_:
        out.append(f'<a href="{prev_}"><div class="dir">&larr; Previous</div>'
                   f'<div class="ttl">{esc(FLAT_NAMES[prev_])}</div></a>')
    else:
        out.append('<span style="flex:1 1 240px"></span>')
    if next_:
        out.append(f'<a href="{next_}"><div class="dir">Next &rarr;</div>'
                   f'<div class="ttl">{esc(FLAT_NAMES[next_])}</div></a>')
    out.append('</div>')
    return "".join(out)


def head(title, lede=""):
    out = [f'<div class="page-head"><h2>{esc(title)}</h2>']
    if lede:
        out.append(f'<p class="lede">{lede}</p>')
    out.append('</div>')
    return "".join(out)


def callout(title_, body_html, kind=""):
    cls = f"callout {kind}".strip()
    return (f'<div class="{cls}"><div class="t">{esc(title_)}</div>'
            f'{body_html}</div>')


def stat(k, v, sub="", src="", tone=""):
    cls = f"stat {tone}".strip()
    s = f'<div class="s">{sub}</div>' if sub else ""
    sr = f'<div class="src">{src}</div>' if src else ""
    return f'<div class="{cls}"><div class="k">{esc(k)}</div><div class="v">{v}</div>{s}{sr}</div>'


# ==========================================================================
# geography label helper
# ==========================================================================
GEO_LABEL = {
    "la-county": "LA County",
    "la-city": "LA City",
    "la-msa": "LA Metro (MSA)",
    "california": "California",
    "united-states": "United States",
    "orange-county": "Orange County",
    "Los Angeles County": "LA County",
    "Los Angeles County and adjacent": "LA County + adjacent",
    "Los Angeles County and adjacent counties": "LA County + adjacent",
    "Los Angeles region": "LA region",
    "California": "California",
    "PROPERTY-01": "PROPERTY-01",
}


def geo_label(g):
    return GEO_LABEL.get(g, g)


# ==========================================================================
# DATA-DRIVEN PAGES
# ==========================================================================
def p_tenant():
    t = tenant
    b = [head("Tenant Credit — Jack in the Box Inc.",
              "Everything on this page is taken from filings the tenant made with the "
              "U.S. Securities and Exchange Commission, or from the tenant's own earnings "
              "release filed with the SEC the same day. SEC EDGAR CIK 0000807882. "
              "No broker commentary, no press summary, no inferred figure.")]
    b.append(callout(
        "Why the tenant dominates this decision",
        "<p>In a single-tenant NNN structure the property's income is one credit. "
        "The tenant's own filings describe a 150&ndash;200 restaurant closure programme "
        "in which the remaining closures occur <em>&ldquo;based upon respective franchise "
        "agreement termination dates&rdquo;</em>. A lease expiring between 2030 and 2035 is "
        "that date. This is the single most important fact in the entire file.</p>", "bad"))

    cols_i = [("field", "Field", "", "text"), ("value", "Value", "", "value"),
              ("", "Status", "", "vbadge"), ("", "Source", "", "src")]
    rows = [t.resolve(r) for r in t.ISSUER]
    b.append(table(rows, cols_i, "issuer", "Registrant identity",
                   "As recorded on the SEC EDGAR filing index.",
                   lambda r: "" if is_verified(r) else "unverified"))

    cols_p = [("brand", "Brand", "geo", "text"),
              ("category", "Real estate category", "", "textn"),
              ("company_operated", "Company-operated", "num", "text"),
              ("franchise", "Franchised", "num", "text"),
              ("total", "Total", "num", "text"),
              ("", "Source", "", "src")]
    rows = [t.resolve(dict(r, source_url=t.SRC[r["source_key"]]["url"])) for r in t.PROPERTIES_FY2025]
    b.append(table(rows, cols_p, "properties",
                   "How the brand itself holds restaurant real estate — Form 10-K FY2025, Item 2 Properties",
                   "As of 2025-09-28. The last row is the ownership pattern that matches an "
                   "independent third-party NNN landlord.",
                   lambda r: ""))

    b.append('<div class="grid g3">')
    b.append(stat("System restaurants", "2,115", "as of 2026-07-05 (Q3 FY2026 Form 10-Q)",
                  "SEC EDGAR", "neg"))
    b.append(stat("System restaurants", "2,191", "at FY2024 year end, 2024-09-29",
                  "SEC EDGAR", ""))
    b.append(stat("Net change", "&minus;76", "restaurants in under two years",
                  "SEC EDGAR", "neg"))
    b.append('</div>')

    cols_l = [("term", "Lease / franchise term", "", "textn"),
              ("value", "As disclosed by the issuer", "", "value"),
              ("", "Source", "", "src")]
    rows = [t.resolve(dict(r, source_url=t.SRC[r["source_key"]]["url"])) for r in t.LEASE_STRUCTURE]
    b.append(table(rows, cols_l, "lease-structure",
                   "Disclosed lease and franchise economics",
                   "These are the tenant's OWN lease terms as lessor and lessee. They are the "
                   "best available evidence of how this brand behaves at expiry, and they are "
                   "not the same document as the owner's lease."))

    cols_s = [("period", "Reporting period", "", "text"),
              ("company", "Company", "num", "text"),
              ("franchise", "Franchise", "num", "text"),
              ("system", "System", "num", "text"),
              ("", "Source", "", "src")]
    rows = [t.resolve(dict(r, source_url=t.SRC[r["source_key"]]["url"])) for r in t.SAME_STORE_SALES]
    b.append(table(rows, cols_s, "sss", "Same-store sales, percent change",
                   "Every recent period is negative. Declines were driven by lower "
                   "transactions, only partially offset by menu price increases."))

    cols_q = [("metric", "Metric", "", "textn"),
              ("value", "Q3 FY2026", "", "value"),
              ("prior_year", "Q3 FY2025", "", "text"),
              ("change", "Change", "num", "text"),
              ("", "Source", "", "src")]
    rows = [t.resolve(dict(r, source_url=t.SRC[r["source_key"]]["url"])) for r in t.Q3_FY2026]
    b.append(table(rows, cols_q, "q3", "Quarterly results, 12 weeks ended 2026-07-05",
                   "From the issuer's earnings release, furnished to the SEC on Form 8-K "
                   "(Items 2.02 and 9.01) the same day."))

    cols_c = [("metric", "Cost and margin metric", "", "textn"),
              ("value", "Latest", "", "value"),
              ("prior_year", "Prior year", "", "text"),
              ("", "Source", "", "src")]
    rows = [t.resolve(dict(r, source_url=t.SRC[r["source_key"]]["url"])) for r in t.COST_PRESSURE]
    b.append(table(rows, cols_c, "cost", "Cost structure pressure",
                   "Food and packaging costs are rising as a share of sales while labour costs "
                   "fall — the tenant is trading labour savings against commodity inflation."))
    return "".join(b)


def p_tenant_closures():
    t = tenant
    b = [head("The Closure Programme — JACK on Track",
              "The tenant's disclosed restructuring programme, in the tenant's own words, "
              "with the consequence for a landlord whose lease expires inside the window "
              "the programme uses as its trigger.")]
    cols = [("item", "Element", "", "textn"), ("value", "As disclosed", "", "value"),
            ("", "Source", "", "src")]
    rows = [t.resolve(dict(r, source_url=t.SRC[r["source_key"]]["url"])) for r in t.JACK_ON_TRACK]
    b.append(table(rows, cols, "jack-on-track", "Programme disclosures",
                   "Read the second and third rows together. They are the mechanism by which "
                   "a 2030–2035 lease expiry becomes a closure decision."))

    cols_r = [("as_of", "As of", "", "text"),
              ("company", "Company-operated", "num", "value"),
              ("franchise", "Franchised", "num", "value"),
              ("total", "Total system", "num", "value"),
              ("", "Source", "", "src")]
    rows = [t.resolve(dict(r, source_url=t.SRC[r["source_key"]]["url"])) for r in t.RESTAURANT_COUNTS]
    b.append(table(rows, cols_r, "counts", "System restaurant count over time", "",
                   lambda r: "" if is_verified(r) else "unverified"))

    b.append(callout(
        "What this means for PROPERTY-01",
        "<p>Three disclosures combine into one exposure. First, the programme targets "
        "restaurants <em>&ldquo;in the system for over three decades&rdquo;</em>. Second, the "
        "remaining closures happen <em>&ldquo;based upon respective franchise agreement "
        "termination dates&rdquo;</em>. Third, the company has said the programme is running "
        "slower than planned <em>because franchisees must evaluate lease obligations before "
        "closing</em>.</p>"
        "<p>A long-operating site with a lease expiring in 2030&ndash;2035 matches the stated "
        "profile on all three counts. That does not mean it will close. It means the owner "
        "should not assume renewal, and should establish the site's status with the tenant "
        "before committing capital to either a renewal negotiation or a marketing process.</p>",
        "warn"))
    b.append(callout(
        "The asymmetry the owner faces",
        "<p>Under the disclosed structure, renewal options are generally exercisable "
        "<em>at the company's sole discretion</em>. If the owner's lease follows the same "
        "pattern, the option to extend belongs to the tenant, not the owner. The owner is "
        "therefore long an asset whose continuation depends on a decision made by a "
        "counterparty that is publicly contracting. Confirm from the lease document whether "
        "the options run in the tenant's favour or the landlord's — this single clause "
        "changes which strategies are even available.</p>", "bad"))
    return "".join(b)


def _std_cols():
    return [("metric", "Metric", "", "textn"), ("value", "Value", "num", "value"),
            ("unit", "Unit", "", "text"), ("geography", "Geography", "geo", "raw"),
            ("as_of", "As of", "", "text"), ("", "Status", "", "vbadge"),
            ("", "Official source", "", "src")]


def _demo_rows(rows):
    out = []
    for r in rows:
        d = dict(r)
        d["geography"] = f'<span title="{esc(r.get("geography",""))}">{esc(geo_label(r.get("geography","")))}</span>'
        out.append(d)
    return out


def p_demographics():
    d = demographics
    b = [head("Population, Households and Income",
              "All figures from U.S. Census Bureau QuickFacts for the two official geographies "
              "that contain the subject market, plus the 2022 Economic Census spending data. "
              "Every row states its own reference period — the Census Bureau warns that "
              "estimates from different sources and vintages are not comparable.")]
    b.append('<div class="grid g4">')
    b.append(stat("LA County population", "9,694,934", "estimate, 1 July 2025 (Vintage 2025)",
                  "U.S. Census Bureau QuickFacts"))
    b.append(stat("LA County change since 2020", "&minus;3.2%",
                  "from an estimates base of 10,017,414", "U.S. Census Bureau", "neg"))
    b.append(stat("LA City population", "3,869,089", "estimate, 1 July 2025 (Vintage 2025)",
                  "U.S. Census Bureau QuickFacts"))
    b.append(stat("LA City change since 2020", "&minus;0.8%",
                  "from an estimates base of 3,899,342", "U.S. Census Bureau", "neg"))
    b.append('</div>')
    b.append(callout("The finding that matters most",
                     "<p>Los Angeles County has lost population in every year since the 2020 "
                     "estimates base, at an official &minus;3.2% over five years. A "
                     "drive-thru quick-service restaurant sells to people inside a short "
                     "drive-time ring. A shrinking base erodes transaction counts — which is "
                     "exactly what the tenant reports. Any hold strategy that depends on "
                     "demographic growth is underwriting against the measured trend.</p>", "bad"))

    for key, title_, note in [
        ("population", "Population", "Decennial census counts and Census Bureau population estimates."),
        ("density", "Density and land area", "Density is the single best proxy available here for drive-thru catchment volume."),
        ("households", "Households and housing", "Building permits are a leading indicator of future trade-area volume."),
        ("income", "Income, housing cost and poverty", "Median household income is the demand anchor for a value-oriented quick-service brand."),
        ("composition", "Age, education and market composition", "Age structure and language composition shape menu and daypart demand."),
        ("economic_census", "Spending and economic activity", "Accommodation and food services sales is the demand pool the tenant competes in."),
    ]:
        rows = d.ALL_TABLES[key]
        b.append(table(_demo_rows(rows), _std_cols(), key, title_, note,
                       lambda r: "" if is_verified(r) else "unverified"))

    b.append(callout("Deliberately omitted",
                     "<p>The Los Angeles <em>city</em> race and ethnicity breakdown from "
                     "QuickFacts does not sum to approximately 100%, while the equivalent "
                     "county breakdown sums to 99.8%. One or more city values appear to have "
                     "been mis-extracted. The city race breakdown is therefore omitted rather "
                     "than published with a possibly incorrect figure. Hispanic or Latino "
                     "share is published for both geographies. Recorded as "
                     "<strong>F-12</strong> on the Flagged for Review page.</p>", "warn"))
    return "".join(b)


def p_employment():
    e = employment
    b = [head("Employment, Wages and Prices",
              "U.S. Bureau of Labor Statistics products: the Los Angeles Area Economic "
              "Summary (updated 5 October 2026), the Metropolitan Area Employment and "
              "Unemployment release USDL-26-1618, and County Business Patterns from the "
              "U.S. Census Bureau.")]
    b.append('<div class="grid g4">')
    b.append(stat("LA metro nonfarm payrolls", "6,289.1k", "Aug 2026, +0.6% year on year",
                  "BLS, Los Angeles Area Economic Summary"))
    b.append(stat("Leisure & hospitality", "+2.2%", "795.8k jobs — the tenant's own sector is growing",
                  "BLS", "pos"))
    b.append(stat("Information sector", "&minus;6.1%", "190.4k jobs — the sharpest contraction",
                  "BLS", "neg"))
    b.append(stat("LA metro unemployment", "4.4%", "Sept 2026 preliminary, from 5.5% a year earlier",
                  "BLS USDL-26-1618", "pos"))
    b.append('</div>')

    cols_u = [("metric", "Indicator", "", "textn"), ("value", "Value", "num", "value"),
              ("unit", "Unit", "", "text"), ("geography", "Geography", "geo", "raw"),
              ("as_of", "As of", "", "text"), ("", "Status", "", "vbadge"),
              ("", "Official source", "", "src")]
    b.append(table(_demo_rows(e.LABOR_FORCE), cols_u, "labor",
                   "Labour force and unemployment",
                   "Read the unemployment rate together with the labour-force level. The rate "
                   "fell while the labour force also fell.",
                   lambda r: ""))

    cols_p = [("metric", "Industry sector", "", "text"),
              ("value", "Employment (000s)", "num", "value"),
              ("change_num", "Change (000s)", "num", "text"),
              ("change_pct", "Change %", "num", "text"),
              ("geography", "Geography", "geo", "raw"),
              ("as_of", "As of", "", "text"), ("", "Source", "", "src")]
    b.append(table(_demo_rows(e.PAYROLLS), cols_p, "payrolls",
                   "Nonfarm payrolls by major industry sector — Los Angeles metro area",
                   "A two-speed economy: education and health services and leisure and "
                   "hospitality are adding jobs while information, financial activities, "
                   "manufacturing and professional services are shedding them.",
                   lambda r: ""))

    cols_t = [("metric", "Indicator", "", "textn"), ("value", "Value", "num", "value"),
              ("unit", "Unit", "", "text"), ("benchmark", "Benchmark", "", "text"),
              ("as_of", "As of", "", "text"), ("", "Status", "", "vbadge"),
              ("", "Official source", "", "src")]
    b.append(table(_demo_rows(e.EMPLOYMENT_TREND), cols_t, "trend",
                   "Employment growth trend and business counts", "",
                   lambda r: "" if is_verified(r) else "unverified"))

    cols_w = [("metric", "Wage measure", "", "textn"), ("value", "Value", "num", "value"),
              ("unit", "Unit", "", "text"), ("geography", "Geography", "geo", "raw"),
              ("as_of", "As of", "", "text"), ("benchmark", "Benchmark", "", "text"),
              ("", "Source", "", "src")]
    b.append(table(_demo_rows(e.WAGES), cols_w, "wages", "Wages and compensation",
                   "Average weekly wages in Los Angeles County run above the national "
                   "average, which is a headwind for a value-positioned quick-service "
                   "operator and a support for consumer spending.", lambda r: ""))

    cols_i = [("metric", "Price measure", "", "textn"), ("value", "Value", "num", "value"),
              ("unit", "Unit", "", "text"), ("geography", "Geography", "geo", "raw"),
              ("as_of", "As of", "", "text"), ("benchmark", "vs United States", "", "text"),
              ("", "Source", "", "src")]
    b.append(table(_demo_rows(e.INFLATION), cols_i, "inflation",
                   "Consumer and producer prices",
                   "Under a true NNN lease these cost increases land on the tenant, not the "
                   "owner — until they exceed what the tenant can absorb.", lambda r: ""))
    return "".join(b)


def p_projections():
    h = hazards
    b = [head("Official Population and Economic Forecasts",
              "The lease decision spans 2030 to 2035. This page collects what the official "
              "forecasting bodies actually publish for that horizon — and discloses, plainly, "
              "that they disagree with each other.")]
    b.append(callout("Two official bodies, opposite signs",
                     "<p>SCAG, the federally designated Metropolitan Planning Organization for "
                     "the region, projected Los Angeles County to <strong>grow 16.6%</strong> to "
                     "11,674,000 by 2045 in its Connect SoCal 2020 plan. The California "
                     "Department of Finance projection cited in the City of Los Angeles 2024 "
                     "workforce plan has the county <strong>falling</strong> to about 9.3 "
                     "million by 2040 and 8.3 million by 2060. The only line in the table below "
                     "that is measurement rather than forecast is the Census Bureau's observed "
                     "&minus;3.2% since 2020.</p>"
                     "<p>This analysis underwrites to the <strong>observed</strong> trend and "
                     "treats growth as upside, never as the base case.</p>", "warn"))

    cols = [("source", "Official source", "", "text"),
            ("direction", "Direction", "", "raw"),
            ("detail", "What it projects", "", "textn"),
            ("", "Status", "", "vbadge"),
            ("url", "Official link", "", "raw")]
    rows = []
    for r in h.PROJECTION_CONFLICT:
        d = dict(r)
        cls = "b-bad" if r["direction"] == "DECLINE" else "b-info"
        d["direction"] = badge(r["direction"], cls)
        d["url"] = f'<a href="{esc(r["url"])}" target="_blank" rel="noopener noreferrer">Open &#8599;</a>'
        rows.append(d)
    b.append(table(rows, cols, "conflict", "Direction of travel, by official source", ""))

    b.append(table(_demo_rows(h.PROJECTIONS), _std_cols(), "proj",
                   "Baseline characteristics and forecasts",
                   "Rows without a value were not readable from the official publisher in this "
                   "session and are left blank — see F-04.",
                   lambda r: "" if is_verified(r) else "unverified"))

    b.append(callout("F-04 — the most important missing number",
                     "<p>The California Department of Finance publishes county projections only "
                     "as spreadsheet files (<code>P2A_County_Total.xlsx</code>), and this "
                     "environment has no network route to <code>dof.ca.gov</code>. Third-party "
                     "restatements of the same DOF series disagree by more than 100,000 "
                     "residents for the same year across vintages. The projected county "
                     "population for <strong>2030, 2035 and 2040</strong> is therefore left "
                     "blank rather than approximated.</p>"
                     "<p>The 2035 value is the mid-point of the stated expiry window and is the "
                     "single most useful forecast number for this decision. "
                     '<a href="https://dof.ca.gov/forecasting/demographics/projections/" '
                     'target="_blank" rel="noopener noreferrer">Download P-2A from the official '
                     "Department of Finance page &#8599;</a> and read the Los Angeles row. Note "
                     "the vintage: Vintage 2026, Baseline 2024.</p>", "bad"))

    b.append('<div class="grid g3">')
    b.append(stat("Observed county change", "&minus;3.2%", "2020 estimates base to July 2025 — measured, not forecast",
                  "U.S. Census Bureau Vintage 2025", "neg"))
    b.append(stat("SCAG successive revisions", "+14.41% &rarr; +10.15% &rarr; negative",
                  "2024–2050 projected change across Connect SoCal 2020, 2024 and the preliminary 2050 plan",
                  "SCAG", "neg"))
    b.append(stat("Forecast reliability", "Downward every time",
                  "Every successive official forecast for this county has been revised lower",
                  "This analysis, from the sources above", "neg"))
    b.append('</div>')
    return "".join(b)


def p_hazards():
    h = hazards
    b = [head("Physical Hazard Exposure",
              "Wildfire, earthquake and post-fire flooding, from CAL FIRE, the County of Los "
              "Angeles, the U.S. Geological Survey and the Congressional Research Service. "
              "The January 2025 Los Angeles County fires are not a hypothetical tail for this "
              "market — they are a realised event inside the analysis period.")]
    b.append('<div class="grid g4">')
    b.append(stat("M6.7+ within 30 years", "60%", "Los Angeles region, UCERF3", "U.S. Geological Survey", "neg"))
    b.append(stat("M7.0+ within 30 years", "46%", "Los Angeles region, UCERF3", "U.S. Geological Survey", "neg"))
    b.append(stat("Structures destroyed, Jan 2025", "15,251", "Eaton 9,414 + Palisades 6,837", "County of Los Angeles", "neg"))
    b.append(stat("Economic output lost", "$5.2–10.1B", "Eaton and Palisades Fires combined", "County of Los Angeles", "neg"))
    b.append('</div>')

    cols = [("metric", "Hazard record", "", "textn"), ("value", "Value", "", "value"),
            ("unit", "Unit", "", "text"), ("geography", "Geography", "geo", "raw"),
            ("as_of", "As of", "", "text"), ("", "Status", "", "vbadge"),
            ("", "Official source", "", "src")]
    rows = [h.resolve(dict(r, geography=f'<span title="{esc(r.get("geography",""))}">{esc(geo_label(r.get("geography","")))}</span>'))
            for r in h.WILDFIRE]
    b.append(table(rows, cols, "wildfire", "Wildfire — realised events and statutory mapping",
                   "The Fire Hazard Severity Zone of PROPERTY-01 cannot be determined without "
                   "the parcel identity and is left blank.",
                   lambda r: "" if is_verified(r) else "unverified"))

    rows = [h.resolve(dict(r, geography=f'<span title="{esc(r.get("geography",""))}">{esc(geo_label(r.get("geography","")))}</span>'))
            for r in h.SEISMIC]
    b.append(table(rows, cols, "seismic", "Earthquake — 30-year probabilities and federal risk model",
                   "USGS figures are official. The FEMA National Risk Index dollar figures "
                   "were not readable on fema.gov in this session and are left blank (F-03).",
                   lambda r: "" if is_verified(r) else "unverified"))

    b.append(callout("Why the FEMA county average is the wrong number to use",
                     "<p>FEMA's National Risk Index is published down to census-tract level, "
                     "and wildfire loss in Los Angeles County is extremely concentrated: most "
                     "tracts have effectively none, while a small minority carry very large "
                     "expected losses. A county average therefore tells an owner almost nothing "
                     "about a specific parcel. The correct action is to query the subject tract "
                     "in FEMA's Resilience Analysis and Planning Tool once the address is "
                     "known.</p>"
                     '<p><a href="https://www.fema.gov/emergency-managers/practitioners/'
                     'resilience-analysis-and-planning-tool" target="_blank" rel="noopener '
                     'noreferrer">FEMA Resilience Analysis and Planning Tool &#8599;</a> '
                     '&middot; <a href="https://www.fema.gov/flood-maps/products-tools/'
                     'national-risk-index" target="_blank" rel="noopener noreferrer">National '
                     "Risk Index overview &#8599;</a></p>", "warn"))

    b.append(callout("CAL FIRE re-mapped Los Angeles County in 2025",
                     "<p>Los Angeles County Fire Department Local Responsibility Area Fire "
                     "Hazard Severity Zones were <strong>established in 2025</strong>, and the "
                     "2025 revision adds Moderate and High categories where the previous map "
                     "showed only Very High. Any fire-zone determination taken from a pre-2025 "
                     "map, a title report or an old insurance submission is stale. Separately, "
                     "State Responsibility Area mapping has not been updated since 1985 except "
                     "for boundary changes.</p>", "warn"))
    return "".join(b)


def p_wage_floor():
    h = hazards
    b = [head("Statutory Wage Floor — the Tenant's Unavoidable Cost",
              "A landlord's rent is paid out of what is left after the tenant's statutory "
              "costs. In California those costs are set by statute and enforced by a "
              "regulator. These are official published rates, not estimates.")]
    cols = [("metric", "Wage measure", "", "textn"), ("value", "Rate", "num", "value"),
            ("as_of", "Effective", "", "text"), ("", "Status", "", "vbadge"),
            ("", "Official source", "", "src")]
    rows = [h.resolve(dict(r, source_url=h.SRC[r["source_key"]]["url"])) for r in h.WAGE_FLOOR]
    b.append(table(rows, cols, "wages", "Statutory minimum wages",
                   "A Jack in the Box restaurant inside the City of Los Angeles is governed by "
                   "the $20.00 fast-food floor, which is higher than the City's $18.42 general "
                   "rate.", lambda r: ""))
    b.append(callout("The structural point",
                     "<p>AB 1228 applies to fast-food employees <em>regardless of whether the "
                     "employer is the brand owner or a franchisee</em>. The tenant cannot avoid "
                     "it by restructuring. The statute also created a council with authority to "
                     "raise the rate further through 2029, capped at the lesser of 3.5% or the "
                     "change in CPI-W. This is a ratchet that only moves in one direction, and "
                     "it operates directly against the tenant's margin — and therefore against "
                     "the rent the tenant can pay at renewal.</p>", "bad"))
    return "".join(b)


def p_risk_register():
    a = analysis
    b = [head("Risk Register",
              "Every risk the owner faces on this asset, scored for likelihood and impact, "
              "with the verified evidence behind it and the mitigation available. Scores are "
              "analytical judgement anchored to cited official facts — the evidence class on "
              "each row says which.")]
    b.append('<div class="legend">'
             '<span><i class="sw" style="background:#9f1239"></i> 20–25 critical</span>'
             '<span><i class="sw" style="background:#c2410c"></i> 15–19 high</span>'
             '<span><i class="sw" style="background:#a16207"></i> 8–14 moderate</span>'
             '<span><i class="sw" style="background:#0f766e"></i> 1–7 low</span>'
             '</div>')
    rows = sorted(a.RISKS, key=lambda r: (-r["score"], r["id"]))
    cols = [("id", "ID", "num", "text"),
            ("category", "Category", "", "text"),
            ("risk", "Risk", "", "textn"),
            ("evidence_class", "Evidence", "", "rawec"),
            ("evidence", "Verified evidence", "", "textn"),
            ("likelihood", "L", "num", "text"),
            ("impact", "I", "num", "text"),
            ("score", "Score", "", "score"),
            ("source_url", "Source", "", "raw")]
    for r in rows:
        r["_ec"] = r["evidence_class"]          # keep the plain word for the prose below
        cls = {"VERIFIED": "b-ok", "MODELLED": "b-info", "JUDGEMENT": "b-neutral"}.get(
            r["evidence_class"], "b-neutral")
        r["evidence_class"] = badge(r["evidence_class"], cls)
        u = r.get("source_url")
        r["source_url"] = (f'<a class="src-link" href="{esc(u)}" target="_blank" '
                           f'rel="noopener noreferrer">Official source &#8599;</a>'
                           if u else '<span class="blank">&mdash;</span>')
    b.append(table(rows, cols, "risks", "Risk register, highest score first",
                   f"{len(rows)} risks. L and I are 1–5 judgement scales; score = L x I."))
    b.append("<h3>Why each risk matters, and what to do about it</h3>")
    for r in sorted(analysis.RISKS, key=lambda x: (-x["score"], x["id"])):
        b.append(f'''<div class="panel"><h3 style="margin-top:0">{esc(r["id"])} &mdash;
{esc(r["risk"])}</h3>
<p><strong>Category:</strong> {esc(r["category"])} &nbsp;
<strong>Risk score:</strong> {score_cell(r["score"])} &nbsp;
<strong>Evidence class:</strong> {esc(r["_ec"])}</p>
<p><strong>Why it matters:</strong> {esc(r["why_it_matters"])}</p>
<p><strong>Mitigation:</strong> {esc(r["mitigation"])}</p></div>''')
    return "".join(b)


def p_black_swan():
    a = analysis
    b = [head("Black Swan and Tail-Event Register",
              "Events that could destroy the local economy or the asset itself. Business-as-"
              "usual risk is on the Risk Register; this page is for the events that are rare, "
              "severe, and — in two cases here — already realised.")]
    b.append(callout("One of these is not a tail. It already happened.",
                     "<p>The Eaton and Palisades Fires of January 2025 burned 37,469 acres "
                     "between them and destroyed 16,251 structures in Los Angeles County. The "
                     "County's own fact sheet puts economic output lost at <strong>$5.2 to "
                     "$10.1 billion</strong>, with approximately 6,800 businesses and 47,000 "
                     "workers impacted and tax revenue losses of $900 million to $1.6 billion. "
                     "For a Los Angeles property, wildfire is a realised hazard with a measured "
                     "economic cost, not a hypothetical.</p>", "bad"))
    cols = [("id", "ID", "num", "text"), ("event", "Event", "", "textn"),
            ("precedent", "Precedent", "", "textn"),
            ("evidence_class", "Evidence", "", "rawec"),
            ("observed", "Observed / measured", "", "value"),
            ("horizon_relevance", "Relevance to 2030–2035", "", "textn"),
            ("source_url", "Source", "", "raw")]
    rows = []
    for r in a.BLACK_SWANS:
        d = dict(r)
        cls = {"VERIFIED": "b-ok", "UNVERIFIED": "b-bad"}.get(r["evidence_class"], "b-neutral")
        d["evidence_class"] = badge(r["evidence_class"], cls)
        u = r.get("source_url")
        d["source_url"] = (f'<a class="src-link" href="{esc(u)}" target="_blank" '
                           f'rel="noopener noreferrer">Official source &#8599;</a>'
                           if u else '<span class="blank">&mdash;</span>')
        rows.append(d)
    b.append(table(rows, cols, "blackswans", "Tail-event register",
                   "Two entries are UNVERIFIED and carry no asserted figure."))
    b.append("<h3>Transmission mechanisms — how each event reaches the owner's return</h3>")
    for r in a.BLACK_SWANS:
        b.append(f'''<div class="panel tight"><h4 style="margin-top:0">{esc(r["id"])} &mdash; {esc(r["event"])}</h4>
<p style="margin-bottom:6px"><strong>Transmission to value:</strong> {esc(r["transmission_to_value"])}</p>
<p class="small" style="margin:0">Precedent: {esc(r["precedent"])}</p></div>''')
    b.append(callout("The insurance mechanism deserves separate emphasis",
                     "<p>B-07 is the one tail that requires no physical damage at all. If "
                     "commercial property insurance becomes unavailable or unaffordable for "
                     "this building type in this county, the NNN lease cannot be performed and "
                     "no institutional buyer will finance the asset. That is a total-loss "
                     "mechanism arriving through a contract, not through a fire. It is marked "
                     "<strong>UNVERIFIED</strong> because no official source was retrieved for "
                     "it in this session — but it should be checked with the California "
                     "Department of Insurance before any hold strategy is relied upon.</p>", "warn"))
    return "".join(b)


# ==========================================================================
# MODEL-DRIVEN PAGES
# ==========================================================================
def p_projection_model():
    b = [head("Projection Model",
              "A reproducible, deterministic model that compares every available strategy for "
              "PROPERTY-01. It is written so that it needs <em>no</em> private property data to "
              "produce a defensible ranking — and it says so when it is guessing.")]
    b.append(callout("Read this before any number below",
        "<p>The owner's actual lease economics were never supplied. Rather than invent a rent, "
        "a basis or a building size, the model is written in units of <strong>R = one year of "
        "the property's current contractual base rent</strong>. Every output is a dimensionless "
        "multiple of R.</p>"
        "<p>This is not a workaround — it is the right form for this decision. Sell-versus-hold "
        "compares two cash-flow streams from the <em>same</em> asset, so the rent level largely "
        "cancels out of the ranking. The owner reads &ldquo;strategy X returns 15.28 R versus "
        "strategy Y at 6.78 R&rdquo; and multiplies by their own actual rent in private. No "
        "private figure has to be published for the analysis to work.</p>", "ok"))

    b.append('<h3>Verified anchors</h3>')
    b.append('<div class="grid g4">')
    y = M.TREASURY_PAR_YIELD_JAN_2026
    b.append(stat("Risk-free anchor", f"{y['10 Yr']}%",
                  "U.S. Treasury 10-year par yield, 2 January 2026",
                  "U.S. Department of the Treasury"))
    b.append(stat("Long anchor", f"{y['20 Yr']}% / {y['30 Yr']}%",
                  "20-year and 30-year par yields, same date", "U.S. Department of the Treasury"))
    b.append(stat("Local inflation", f"{M.BLS_LA_CPI_ALL_ITEMS_AUG2026}%",
                  "CPI-U all items, Los Angeles metro, 12 months to Aug 2026",
                  "U.S. Bureau of Labor Statistics"))
    b.append(stat("Local wage growth", f"{M.BLS_LA_ECI_JUN2026}%",
                  "Employment Cost Index, LA–Long Beach CSA, 12 months to Jun 2026",
                  "U.S. Bureau of Labor Statistics"))
    b.append('</div>')
    b.append(table([
        dict(metric="1 Yr", value=f"{y['1 Yr']}%", unit="%", geography="United States",
             as_of=y["_date_read"], verified="VERIFIED", source_url=y["_url"],
             source_label="U.S. Treasury Daily Par Yield Curve"),
        dict(metric="3 Yr", value=f"{y['3 Yr']}%", unit="%", geography="United States",
             as_of=y["_date_read"], verified="VERIFIED", source_url=y["_url"],
             source_label="U.S. Treasury Daily Par Yield Curve"),
        dict(metric="5 Yr", value=f"{y['5 Yr']}%", unit="%", geography="United States",
             as_of=y["_date_read"], verified="VERIFIED", source_url=y["_url"],
             source_label="U.S. Treasury Daily Par Yield Curve"),
        dict(metric="10 Yr", value=f"{y['10 Yr']}%", unit="%", geography="United States",
             as_of=y["_date_read"], verified="VERIFIED", source_url=y["_url"],
             source_label="U.S. Treasury Daily Par Yield Curve"),
        dict(metric="20 Yr", value=f"{y['20 Yr']}%", unit="%", geography="United States",
             as_of=y["_date_read"], verified="VERIFIED", source_url=y["_url"],
             source_label="U.S. Treasury Daily Par Yield Curve"),
        dict(metric="30 Yr", value=f"{y['30 Yr']}%", unit="%", geography="United States",
             as_of=y["_date_read"], verified="VERIFIED", source_url=y["_url"],
             source_label="U.S. Treasury Daily Par Yield Curve"),
    ], [("metric", "Maturity", "", "text"), ("value", "Par yield", "num", "value"),
        ("as_of", "As of", "", "text"), ("", "Status", "", "vbadge"),
        ("", "Official source", "", "src")],
        "treasury", "U.S. Treasury Daily Par Yield Curve Rates, January 2026",
        "The discount rate is this verified official rate plus an explicitly declared risk "
        "premium. Pull the current curve from the same page at decision time."))

    b.append('<h3>Declared assumptions</h3>')
    b.append(callout("Every one of these is a guess, and is labelled as one",
        "<p>No assumption below is verified data. Each carries a low, base and high value and a "
        "<em>favourability direction</em> — which extreme is good for the owner. Without the "
        "direction, an &ldquo;optimistic&rdquo; scenario silently mixes optimistic and "
        "pessimistic inputs, which is the most common way a sensitivity grid lies. The "
        "optimistic scenario takes the favourable extreme of <em>every</em> assumption; the "
        "pessimistic scenario takes the unfavourable extreme of every one.</p>", "warn"))
    rows = []
    for k, v in M.ASSUMPTIONS.items():
        rows.append(dict(name=k.replace("_", " "), low=v["low"], base=v["base"],
                         high=v["high"], unit=v["unit"],
                         fav="high is good" if v["fav"] == "high" else "low is good",
                         status=v["status"]))
    b.append(table(rows, [
        ("name", "Assumption", "", "text"),
        ("low", "Low", "num", "raw"), ("base", "Base", "num", "raw"),
        ("high", "High", "num", "raw"),
        ("unit", "Unit", "", "text"), ("fav", "Favourable side", "", "text"),
        ("status", "Status", "", "rawst")],
        "assumptions", "Model assumptions — all judgement, none verified",
        "Two of these have no official source at all: commercial cap rates are private data."))
    for r in rows:
        pass
    b.append(callout("F-02 — cap rates cannot be verified",
        "<p>No United States government agency publishes commercial capitalisation rates or "
        "comparable sale prices for single-tenant net-lease restaurants. That data is private "
        "and sold by commercial vendors. The two cap-rate assumptions above are therefore "
        "swept across a deliberately wide band (5.0% to 8.5%) and every valuation conclusion on "
        "this site is presented as a range. Any adviser quoting a single precise market value is "
        "quoting a private dataset, not an official statistic.</p>", "bad"))

    b.append('<h3>Strategies evaluated</h3>')
    for s in analysis.STRATEGIES:
        b.append(f'''<div class="panel tight"><h4 style="margin-top:0">{esc(s["id"])} &mdash; {esc(s["name"])}</h4>
<p style="margin-bottom:8px">{esc(s["summary"])}</p>
<p style="margin-bottom:4px"><strong>Wealth preservation:</strong> {esc(s["preserves_wealth"])}</p>
<p style="margin-bottom:4px"><strong>Growth:</strong> {esc(s["growth"])}</p>
<p style="margin-bottom:4px"><strong>Key dependency:</strong> {esc(s["key_dependency"])}</p>
<p class="small" style="margin:0"><strong>How the model prices it:</strong> {esc(s["model_note"])}</p></div>''')

    b.append('<h3>Expiry-window treatment</h3>')
    b.append(table([
        dict(exp="2030", yrs=4, note="Earliest stated expiry. Shortest remaining term; hardest to finance for a buyer; least rent collected before rollover."),
        dict(exp="2032", yrs=6, note="Mid-point of the stated window. Used as the central case."),
        dict(exp="2035", yrs=9, note="Latest stated expiry. Most rent collected; longest exposure to tenant closure decisions and to seismic hazard."),
    ], [("exp", "Expiry year", "", "text"), ("yrs", "Years from Nov 2026", "num", "raw"),
        ("note", "What changes", "", "textn")],
        "expiry", "The stated expiry is a five-year range, not a date",
        "Lease economics differ materially across 2030–2035, so the model evaluates both "
        "bookends and the mid-point rather than silently picking one."))
    b.append("<h3>Reproduce</h3>")
    b.append('<div class="panel tight"><p style="margin:0"><code>python3 -m model.projection</code> '
             'prints every scenario and every strategy ranked by risk-adjusted present value in R. '
             'The model is deterministic: same inputs, same outputs, no randomness, no network '
             'calls. Source: <code>model/projection.py</code>.</p></div>')
    return "".join(b)


def p_valuation():
    b = [head("Valuation and Sensitivity",
              "Present value of each strategy in units of R, across three coherent scenarios. "
              "Nothing here asserts a market price — it ranks the choices, and shows how wide "
              "the band around each one is.")]

    rs = M.rank_stability()
    ev = {r["strategy"]: r for r in M.expected_value()}
    rows = []
    for r in rs:
        rows.append(dict(
            strategy=r["strategy"], expiry=r["expiry"],
            opt=r["pv_optimistic"], base=r["pv_base"], pes=r["pv_pessimistic"],
            worst=r["pv_min"], spread=r["pv_spread"],
            expv=ev[r["strategy"]]["expected_pv_R"],
            ro=r["rank_optimistic"], rb=r["rank_base"], rp=r["rank_pessimistic"],
        ))
    rows.sort(key=lambda x: -x["worst"])
    cols = [("strategy", "Strategy", "", "text"),
            ("expiry", "Expiry case", "", "text"),
            ("opt", "Optimistic (R)", "num", "raw"),
            ("base", "Base (R)", "num", "raw"),
            ("pes", "Pessimistic (R)", "num", "raw"),
            ("expv", "Weighted E[R]", "num", "raw"),
            ("worst", "Worst case (R)", "num", "rawb"),
            ("spread", "Spread (R)", "num", "raw"),
            ("ro", "Rank O", "num", "raw"), ("rb", "Rank B", "num", "raw"),
            ("rp", "Rank P", "num", "raw")]
    for r in rows:
        for k in ("opt", "base", "pes", "expv", "worst", "spread", "ro", "rb", "rp"):
            r[k] = f"{r[k]:,.2f}" if k not in ("ro", "rb", "rp") else str(r[k])
    b.append(table(rows, cols, "valuation", "Risk-adjusted present value by strategy and scenario",
                   "Sorted by worst-case present value — the floor. All figures are multiples "
                   "of R (one year of current base rent) and are net of transaction friction, "
                   "re-tenanting capital, vacancy, tenant-survival probability and "
                   "catastrophe expectation."))

    b.append(callout("The one number that decides it",
        "<p><strong>Selling now has the highest worst-case present value of any strategy.</strong> "
        "In the pessimistic scenario it returns 11.62 R, against 9.88 R for the next-best "
        "strategy and 1.18 R for renewing the Jack in the Box lease to a 2030 expiry. Under the "
        "stated objective — preservation of wealth at a manageable level of risk — the floor "
        "matters more than the ceiling, because the owner cannot choose the scenario in "
        "advance.</p>", "ok"))

    b.append('<h3>Cap-rate sensitivity — value of one year of rent</h3>')
    caps = [0.050, 0.055, 0.060, 0.0625, 0.065, 0.070, 0.075, 0.080, 0.085, 0.090]
    rows = []
    for c in caps:
        gross = 1.0 / c
        rows.append(dict(cap=f"{c*100:.2f}%", gross=f"{gross:,.2f} R",
                         net45=f"{gross*(1-0.045):,.2f} R",
                         net70=f"{gross*(1-0.07):,.2f} R",
                         implied=gross))
    b.append(table(rows, [
        ("cap", "Capitalisation rate", "num", "raw"),
        ("gross", "Gross value (R)", "num", "raw"),
        ("net45", "Net of 4.5% friction (R)", "num", "raw"),
        ("net70", "Net of 7.0% friction (R)", "num", "raw")],
        "capsens", "Direct capitalisation of one year of base rent",
        "ARITHMETIC, NOT AN OBSERVED MARKET PRICE. No official cap rate exists (F-02). Read it "
        "as: if your net rent is R and the market cap rate is c, the asset is worth R/c before "
        "costs."))
    b.append(callout("How much of the answer depends on the cap rate",
        "<p>Between a 5.0% and an 8.5% cap rate the same income stream is worth 20.0 R or "
        "11.8 R — a 41% swing in value from an input nobody can officially verify. That is why "
        "the recommendation is framed around the <em>worst case</em> rather than the expected "
        "case: selling now wins the pessimistic scenario outright, and it does so at every cap "
        "rate in the band, because it also removes the cap-rate risk itself.</p>", "warn"))

    b.append('<h3>Breakeven — what would have to be true to hold instead of sell</h3>')
    b.append(table([
        dict(q="At what exit cap rate does holding to expiry beat selling now?",
             a="Not at any rate in the tested band on a worst-case basis. Holding wins the optimistic scenario only, where the exit cap rate falls to about 5.0% AND the alternative use of the land is worth 20 R.",
             cls="bad"),
        dict(q="At what probability of tenant non-renewal does renewing stop being viable?",
             a="Renewing already ranks last at the base assumption of 45% non-renewal. It only competes if non-renewal probability falls below roughly 25% AND downtime below 0.5 years AND the replacement rent at or above current rent.",
             cls="bad"),
        dict(q="How long can the site stand empty before re-letting destroys the hold case?",
             a="In the pessimistic case, about 3 years of downtime plus 3.0 R of re-tenanting capital takes a re-let strategy from 12.30 R to 2.51 R. Vacancy, not the exit cap rate, is the fastest way to lose the hold case.",
             cls="warn"),
        dict(q="Does the length of the remaining term help?",
             a="Yes for holding, but weakly. Collecting rent to 2035 rather than 2030 adds about 1.3 R of discounted rent, while adding three more years of catastrophe and tenant-closure exposure. The model does not reward waiting.",
             cls="neutral"),
    ], [("q", "Question", "", "textn"), ("a", "Answer from the model", "", "textn")],
        "breakeven", "Breakeven questions", ""))
    return "".join(b)


def p_decision():
    a = analysis.RECOMMENDATION
    b = [head("Decision Framework",
              "The recommendation, the reasoning, the conditions under which it changes, and "
              "what evidence would overturn it.")]
    b.append(f'<div class="verdict"><div class="label">Recommendation</div>'
             f'<div class="headline">{esc(a["headline"])}</div>'
             f'<p>Selling now has the highest worst-case present value of every strategy '
             f'modelled. Renewing the Jack in the Box lease ranks last in both the base and '
             f'the pessimistic scenario. The tenant&rsquo;s own SEC filings describe a '
             f'150&ndash;200 restaurant closure programme in which the remaining closures '
             f'occur &ldquo;based upon respective franchise agreement termination dates&rdquo; '
             f'&mdash; and 2030&ndash;2035 is that date.</p></div>')

    b.append("<h3>Why</h3><ol>")
    for r in a["rationale"]:
        b.append(f"<li>{esc(r)}</li>")
    b.append("</ol>")

    b.append("<h3>Strategy comparison</h3>")
    cols = [("id", "ID", "", "text"), ("name", "Strategy", "", "text"),
            ("summary", "What it is", "", "textn"),
            ("preserves_wealth", "Wealth preservation", "", "textn"),
            ("growth", "Growth", "", "textn"),
            ("key_dependency", "Key dependency", "", "textn")]
    b.append(table(analysis.STRATEGIES, cols, "strategies",
                   "The six strategies, compared", ""))

    b.append("<h3>Conditions attached to this recommendation</h3>")
    for c in a["conditions"]:
        b.append(callout("Condition", f"<p>{esc(c)}</p>", "warn"))

    b.append("<h3>What would change the answer</h3><ul>")
    for c in a["what_would_change_the_answer"]:
        b.append(f"<li>{esc(c)}</li>")
    b.append("</ul>")

    b.append(callout("Balancing preservation against growth, as the brief asks",
        "<p>The two objectives pull in different directions and the model quantifies the trade. "
        "<strong>Selling now</strong> maximises the floor: 11.62 R in the worst case, the "
        "highest of any strategy, with the narrowest spread. <strong>Holding to expiry and "
        "re-letting to a different operator</strong> maximises the weighted expected value at "
        "17.15 R, but its worst case is 4.82 R — a spread more than three times wider. That is "
        "the growth option, and it is only appropriate if the owner can absorb the downside "
        "without distress and has independently confirmed a demand for the box from a tenant "
        "other than Jack in the Box.</p>"
        "<p>A middle path exists and is modelled as S5: negotiate an early extension with the "
        "tenant, then sell the lengthened lease. It has the best mean rank across the three "
        "scenarios (6th, 1st, 2nd) and the second-highest floor. Its weak link is that it "
        "requires a tenant that is publicly contracting to agree to a longer commitment.</p>",
        "ok"))

    b.append("<h3>Sequenced action plan</h3>")
    b.append(table([
        dict(n="1", act="Establish whether PROPERTY-01 is inside the tenant's closure programme.",
             why="Every later step is conditional on this. Ask the tenant or the operator directly and get the answer in writing.",
             when="Immediately", cost="None"),
        dict(n="2", act="Complete the Input Register privately.",
             why="The model is normalised to R precisely because these inputs are missing. Supplying them converts rankings into dollar figures.",
             when="Immediately", cost="None"),
        dict(n="3", act="Read the lease: option holder, option terms, guaranty, percentage rent, assignment and recapture clauses.",
             why="If renewal options run in the tenant's sole favour — as the issuer discloses for its own leases — the owner cannot force a renewal, and strategy S3 is not the owner's to choose.",
             when="Week 1", cost="Legal review"),
        dict(n="4", act="Commission an MAI appraisal and obtain current transaction comparables.",
             why="Cap rates are the one input with no official source. This is the only legitimate way to replace the modelled band with a market number.",
             when="Weeks 1–4", cost="Appraisal fee"),
        dict(n="5", act="Obtain a written California tax opinion covering gain, depreciation recapture, section 1031 eligibility and withholding.",
             why="Net proceeds decide the comparison, not gross price. No tax rate is asserted anywhere on this site — see F-05.",
             when="Weeks 1–4", cost="Tax adviser fee"),
        dict(n="6", act="Determine the CAL FIRE Fire Hazard Severity Zone (2025 map) and confirm insurance placement and renewability.",
             why="An uninsurable asset cannot be sold to a financed buyer. This is a precondition of every sell strategy, not a footnote.",
             when="Weeks 1–4", cost="None to low"),
        dict(n="7", act="Run the City of Los Angeles zoning lookup and test whether a better use exists for the land.",
             why="This is the only evidence that would make S6 (hold and redevelop) outrank selling. Without it, redevelopment upside is hope.",
             when="Weeks 2–6", cost="Planning consultant"),
        dict(n="8", act="If the site is off the closure list and a guaranty exists, open an early-extension conversation. Otherwise go straight to market.",
             why="S5 dominates S1 only when the tenant will actually extend. Test it cheaply before committing to a marketing process.",
             when="Weeks 4–8", cost="None"),
        dict(n="9", act="Market the asset with a full verified-data pack: this file, the appraisal, the fire zone, the zoning position and the tenant status.",
             why="An asset sold with documented verification clears faster and at a tighter cap rate than one sold on a broker's one-page teaser.",
             when="Weeks 6–20", cost="Broker commission"),
    ], [("n", "#", "num", "text"), ("act", "Action", "", "textn"),
        ("why", "Why", "", "textn"), ("when", "When", "", "text"),
        ("cost", "Cost", "", "text")],
        "actions", "Sequenced action plan", "Ordered so that the cheapest, most decision-critical steps come first."))
    return "".join(b)


# ==========================================================================
# NARRATIVE PAGES
# ==========================================================================
def p_index():
    rs = {r["strategy"]: r for r in M.rank_stability()}
    sell_now = [r for r in M.rank_stability() if r["strategy"].startswith("S1")][0]
    ev = {r["strategy"]: r for r in M.expected_value()}
    best_ev = max(ev.values(), key=lambda r: r["expected_pv_R"])
    b = [f'''<div class="verdict">
<div class="label">Decision &mdash; PROPERTY-01 &middot; Jack in the Box NNN &middot; lease expiry 2030&ndash;2035 &middot; Central Los Angeles</div>
<div class="headline">{esc(analysis.RECOMMENDATION["headline"])}</div>
<p>The model gives selling now the highest worst-case present value of every strategy tested
({sell_now["pv_pessimistic"]:,.2f} R against {best_ev["worst_pv_R"]:,.2f} R for the
highest-expected-value alternative). Renewing the Jack in the Box lease ranks last in both the
base and the pessimistic scenario, because it is the only strategy whose entire value depends on
a counterparty that is publicly contracting and that has tied its closure decisions to exactly
the dates in question. <a href="decision.html">Read the full decision framework &rarr;</a></p>
</div>''']

    b.append('<div class="grid g4">')
    b.append(stat("LA County population", "9,694,934", "&minus;3.2% since the 2020 estimates base",
                  "U.S. Census Bureau, Vintage 2025", "neg"))
    b.append(stat("LA metro unemployment", "4.4%", "Sept 2026 preliminary, from 5.5%",
                  "U.S. BLS USDL-26-1618", "pos"))
    b.append(stat("Tenant system count", "2,115", "from 2,191 at FY2024 year end",
                  "SEC Form 10-Q, period ended 2026-07-05", "neg"))
    b.append(stat("Tenant system same-store sales", "&minus;4.2%", "fiscal 2025; &minus;1.1% in Q3 FY2026",
                  "SEC Form 10-K FY2025", "neg"))
    b.append(stat("M6.7+ within 30 years", "60%", "Los Angeles region",
                  "U.S. Geological Survey, UCERF3", "neg"))
    b.append(stat("Fast-food wage floor", "$20.00/hr", "statutory, AB 1228, applies to franchisees",
                  "California DIR", "neg"))
    b.append(stat("LA metro CPI-U", "+3.6%", "12 months to Aug 2026; energy +17.6%",
                  "U.S. BLS", "neg"))
    b.append(stat("Jan 2025 wildfire losses", "$5.2&ndash;10.1B", "economic output lost, Eaton and Palisades Fires",
                  "County of Los Angeles", "neg"))
    b.append('</div>')

    b.append('<h3>Top-line findings</h3>')
    findings_rows = [
        dict(f="The tenant is contracting, and its closure trigger is the lease expiry date.",
             d="Jack in the Box Inc. discloses a 150–200 restaurant block closure programme. Remaining closures occur “based upon respective franchise agreement termination dates”. The system fell from 2,191 restaurants at FY2024 year end to 2,115 at 2026-07-05.",
             s="VERIFIED", u="https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm"),
        dict(f="The county is losing population, and the official forecasts disagree on the sign.",
             d="Census Vintage 2025 measures −3.2% since the 2020 estimates base. SCAG’s 2020 plan projected +16.6% to 2045; the state projection has the county falling to about 9.3 million by 2040. This analysis underwrites to the measured trend, not to either forecast.",
             s="VERIFIED", u="https://www.census.gov/quickfacts/losangelescountycalifornia"),
        dict(f="The labour market looks better than it is.",
             d="Unemployment fell from 5.5% to 4.4% year on year, but the civilian labour force also fell by about 121,600 over the same period. A falling rate driven by people leaving the labour force is not an expanding economy.",
             s="VERIFIED", u="https://www.bls.gov/news.release/pdf/metro.pdf"),
        dict(f="The tenant’s sector is one of the few growing ones.",
             d="Leisure and hospitality added 16.8 thousand jobs (+2.2%) in the Los Angeles metro area in the year to August 2026, while information fell 6.1% and manufacturing 1.1%. Total nonfarm rose only 0.6%.",
             s="VERIFIED", u="https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf"),
        dict(f="A statutory wage ratchet compresses the tenant’s margin.",
             d="California’s $20.00 fast-food floor applies to franchisee employers and cannot be avoided by restructuring. A council exists with authority to raise it further through 2029.",
             s="VERIFIED", u="https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm"),
        dict(f="The tail risk is already realised in this county.",
             d="The January 2025 Eaton and Palisades Fires destroyed 16,251 structures and cost $5.2–10.1 billion in economic output. USGS puts the 30-year probability of an M6.7+ earthquake in the region at 60%.",
             s="VERIFIED", u="https://file.lacounty.gov/SDSInter/lac/1199046_Eaton_Palisades_Fires_Anniversary_Fact_Sheet.pdf"),
        dict(f="The single most important number in the decision has no official source.",
             d="No U.S. government agency publishes commercial cap rates or comparable sale prices. Valuation is therefore presented as a sensitivity range, never as a point estimate.",
             s="NO OFFICIAL SOURCE", u=""),
        dict(f="The property itself was never identified.",
             d="No address, APN, lot size, building size, rent, escalation schedule, basis or guaranty status was supplied. All property-specific fields are blank and flagged rather than invented.",
             s="INPUT REQUIRED", u=""),
    ]
    for r in findings_rows:
        cls = {"VERIFIED": "b-ok"}.get(r["s"], "b-warn")
        r["s"] = badge(r["s"], cls)
        r["u"] = (f'<a class="src-link" href="{esc(r["u"])}" target="_blank" '
                  f'rel="noopener noreferrer">Official source &#8599;</a>'
                  if r["u"] else '<span class="blank">&mdash;</span>')
    b.append(table(findings_rows,
                   [("f", "Finding", "", "textn"), ("d", "Evidence", "", "textn"),
                    ("s", "Status", "", "raw"), ("u", "Official source", "", "raw")],
                   "findings", "Eight findings that drive the recommendation", ""))

    b.append('<h3>Browse by category</h3><div class="navcards">')
    for group, items in NAV:
        if group == "Overview":
            continue
        for f, t in items:
            desc = CARD_DESC.get(f, "")
            b.append(f'<a class="navcard" href="{f}"><div class="cat">{esc(group)}</div>'
                     f'<h4>{esc(t)}</h4><p>{esc(desc)}</p></a>')
    b.append('</div>')

    b.append('<h3>Assurance status</h3>')
    b.append('<div class="grid g3">')
    nv = sum(1 for mod in (demographics, employment, tenant, hazards)
             for rows in mod.ALL_TABLES.values() for r in rows if is_verified(r))
    nu = sum(1 for mod in (demographics, employment, tenant, hazards)
             for rows in mod.ALL_TABLES.values() for r in rows
             if "verified" in r and not is_verified(r))
    b.append(stat("Rows with an official source", str(nv),
                  "each links directly to the publisher", "This site"))
    b.append(stat("Rows left blank", str(nu),
                  "could not be confirmed from an official source; none inferred", "This site", "neg"))
    b.append(stat("Flagged for review", str(len(flags.FLAGGED)),
                  "published on the Flagged for Review page; none blocks the decision", "This site", "neg"))
    b.append('</div>')
    return "".join(b)


CARD_DESC = {
    "executive-summary.html": "One page: the decision, the evidence, the conditions and the risks.",
    "methodology.html": "How every figure was obtained, checked and labelled.",
    "privacy.html": "What personal information was found, removed and never published.",
    "property-profile.html": "The asset as it is known — and the Input Register of what is not.",
    "geography.html": "Why “Central Los Angeles” is mapped to three official geographies.",
    "lease-economics.html": "How an NNN lease works here and what the tenant’s own leases disclose.",
    "tenant.html": "Tenant credit from SEC filings only — identity, real estate, sales, costs.",
    "tenant-closures.html": "The JACK on Track closure programme and why the expiry date is its trigger.",
    "demographics.html": "Population, households, density, income and spending, by official geography.",
    "employment.html": "Labour force, payrolls by sector, wages, prices and business counts.",
    "projections.html": "Official forecasts for the 2030–2035 horizon — and the conflict between them.",
    "infrastructure.html": "Transit, land use and school reference routes; what is verified and what is not.",
    "projection-model.html": "The model: R-normalisation, verified anchors, declared assumptions.",
    "valuation.html": "Present value by strategy and scenario, cap-rate sensitivity, breakevens.",
    "decision.html": "The recommendation, its conditions, and a sequenced action plan.",
    "taxes.html": "The mechanisms that apply to a sale, with official sources and no asserted rates.",
    "risk-register.html": "Seventeen risks scored for likelihood and impact, with mitigations.",
    "hazards.html": "Wildfire, earthquake and post-fire flooding from official sources.",
    "black-swan.html": "Tail events that could destroy the local economy or the asset.",
    "sources.html": "Every official source used, with publisher, date, accession and use.",
    "flagged-for-review.html": "Everything blank, unverified, conflicting or needing owner input.",
    "repo-review.html": "The repository audit and the irregularities found in it.",
}


def p_exec_summary():
    a = analysis.RECOMMENDATION
    rs = M.rank_stability()
    sell = [r for r in rs if r["strategy"].startswith("S1")][0]
    renew = [r for r in rs if r["strategy"].startswith("S3") and "4y" in r["strategy"]][0]
    b = [head("Executive Summary",
              "For an owner of a single-tenant Jack in the Box NNN property in Central Los "
              "Angeles with a lease expiring between 2030 and 2035. Every figure below is "
              "traceable to an official source named inline; every judgement is labelled as "
              "one.")]
    b.append(f'<div class="verdict"><div class="label">Recommendation</div>'
             f'<div class="headline">{esc(a["headline"])}</div>'
             f'<p>Sell. If the tenant will commit to an early extension first, buy the term and '
             f'then sell the lengthened lease. Do not plan around renewing at expiry.</p></div>')

    b.append("<h3>The situation</h3>")
    b.append("<p>The owner holds a freehold interest in a single-tenant quick-service restaurant "
             "property in Central Los Angeles, occupied under a triple-net lease by a Jack in the "
             "Box restaurant, with the primary term expiring somewhere between 2030 and 2035. "
             "Under a true NNN structure the tenant pays property taxes, insurance and "
             "maintenance, so the owner's operating exposure is close to zero while the lease "
             "runs. The owner's exposure is entirely to two things: whether the tenant stays, and "
             "what the site is worth if it does not.</p>")

    b.append("<h3>What the evidence shows</h3><ol>")
    for r in a["rationale"]:
        b.append(f"<li>{esc(r)}</li>")
    b.append("</ol>")

    b.append("<h3>The numbers that decide it</h3>")
    b.append('<div class="grid g3">')
    b.append(stat("Sell now — worst case", f"{sell['pv_pessimistic']:,.2f} R",
                  "the highest floor of any strategy tested", "model/projection.py, pessimistic scenario"))
    b.append(stat("Renew JIB to 2030 — worst case", f"{renew['pv_pessimistic']:,.2f} R",
                  "the lowest floor of any strategy tested", "model/projection.py, pessimistic scenario", "neg"))
    b.append(stat("Ratio", f"{sell['pv_pessimistic']/renew['pv_pessimistic']:,.1f}x",
                  "selling protects roughly ten times more value than renewing in the bad case",
                  "model/projection.py", "pos"))
    b.append('</div>')
    b.append('<p class="small">R = one year of the property&rsquo;s current contractual base '
             'rent. The model is normalised this way because the actual rent was never supplied '
             'and no figure has been invented. Multiply by your own rent to get dollars. See '
             '<a href="projection-model.html">Projection Model</a>.</p>')

    b.append("<h3>Risk position</h3>")
    top = sorted(analysis.RISKS, key=lambda r: -r["score"])[:5]
    b.append(table([dict(id=r["id"], cat=r["category"], risk=r["risk"],
                         sc=r["score"], ec=r["evidence_class"]) for r in top],
                   [("id", "ID", "num", "text"), ("cat", "Category", "", "text"),
                    ("risk", "Risk", "", "textn"), ("ec", "Evidence", "", "text"),
                    ("sc", "Score", "", "score")],
                   "toprisks", "Five highest-scoring risks",
                   f"Of {len(analysis.RISKS)} on the register. Scores are 1–25; likelihood and "
                   "impact are judgement anchored to the cited evidence."))
    b.append('<p><a href="risk-register.html">Full risk register &rarr;</a> &nbsp; '
             '<a href="black-swan.html">Black swan register &rarr;</a></p>')

    b.append("<h3>What is deliberately not known</h3>")
    b.append("<p>This analysis refuses to invent the things it was not given. Four categories of "
             "figure are published blank across the site, and each is explained on the "
             "<a href='flagged-for-review.html'>Flagged for Review</a> page:</p><ul>"
             "<li><strong>The property itself</strong> — no address, APN, lot size, building "
             "size, rent, escalation schedule, basis or guaranty status was supplied (F-01).</li>"
             "<li><strong>Commercial cap rates and comparable sales</strong> — no United States "
             "government agency publishes these; they are private data (F-02).</li>"
             "<li><strong>Los Angeles County population projections for 2030, 2035 and 2040</strong> "
             "— published only as spreadsheets on a domain this environment cannot reach, and "
             "third-party restatements disagree by more than 100,000 residents (F-04).</li>"
             "<li><strong>Tax rates on a sale</strong> — the relevant IRS and California "
             "Franchise Tax Board pages returned errors when retrieved, so the mechanisms are "
             "described and linked but no rate is asserted (F-05).</li></ul>")

    b.append("<h3>Conditions</h3>")
    for c in a["conditions"]:
        b.append(callout("Condition", f"<p>{esc(c)}</p>", "warn"))

    b.append("<h3>Next steps</h3>")
    b.append("<p>Nine sequenced actions, ordered so the cheapest and most decision-critical come "
             "first, are set out on the <a href='decision.html'>Decision Framework</a> page. "
             "The first costs nothing and takes one conversation: establish whether this "
             "property is inside the tenant's closure programme. Everything else depends on the "
             "answer.</p>")
    return "".join(b)


def p_methodology():
    b = [head("Methodology and Verification Protocol",
              "How every figure in this file was obtained, what was accepted as evidence, what "
              "was rejected, and how the reader can check any of it.")]
    b.append("<h3>Evidence classes</h3>")
    b.append(table([
        dict(c="VERIFIED", w="Accepted as", d="Read directly on an official .gov page, or in a filing the issuer made with the U.S. Securities and Exchange Commission, during this analysis session. Every VERIFIED row carries the exact URL it was read from."),
        dict(c="MODELLED", w="Treated as", d="An arithmetic output of model/projection.py computed from declared assumptions. Reproducible, but not an observation of the world."),
        dict(c="JUDGEMENT", w="Treated as", d="A qualitative assessment by this analysis. The reasoning is traceable to cited verified facts; the severity rating itself is opinion and is labelled as such."),
        dict(c="UNVERIFIED", w="Rejected as a value", d="Appeared only in a secondary source, or on an official page that could not be retrieved. Published blank, with the official route to confirm it."),
        dict(c="NO OFFICIAL SOURCE", w="Does not exist", d="No government body publishes this figure at all. Never asserted anywhere on this site."),
        dict(c="INPUT REQUIRED", w="Withheld", d="Property-specific or personal. Withheld by design under the privacy directive."),
    ], [("c", "Label", "", "text"), ("w", "Meaning", "", "text"),
        ("d", "Definition and handling", "", "textn")],
        "classes", "The six evidence classes used across the site", ""))

    b.append("<h3>Source hierarchy applied</h3><ol>"
             "<li><strong>Primary federal and state agencies.</strong> SEC EDGAR, U.S. Census "
             "Bureau, U.S. Bureau of Labor Statistics, U.S. Geological Survey, U.S. Department of "
             "the Treasury, FEMA, CAL FIRE, California Department of Industrial Relations, "
             "California Department of Finance, Congressional Research Service.</li>"
             "<li><strong>County and municipal governments.</strong> County of Los Angeles, City "
             "of Los Angeles Office of Wage Standards, City of Los Angeles Economic and Workforce "
             "Development Department, Los Angeles County Fire Department open data.</li>"
             "<li><strong>The issuer itself.</strong> Jack in the Box Inc. earnings release — "
             "accepted only because the same figures were furnished to the SEC on Form 8-K the "
             "same day.</li>"
             "<li><strong>Rejected outright.</strong> Commercial brokerage listings, net-lease "
             "aggregator sites, investor forums, media restatements of government data, and any "
             "third-party restatement of a figure that could be read at source. Where a "
             "third-party figure was the only one obtainable, the value is left blank and the "
             "official route is given instead.</li></ol>")

    b.append(callout("Three concrete cases where the protocol changed the answer",
        "<p><strong>Minimum wage.</strong> Third-party sources gave $17.00 for the California "
        "rate. The California Department of Industrial Relations page gives <strong>$16.90</strong> "
        "effective 1 January 2026. The official figure was used and the conflict recorded.</p>"
        "<p><strong>Population projections.</strong> Two official bodies disagree on the "
        "<em>direction</em> of travel for Los Angeles County. Rather than average them or pick "
        "the convenient one, both are published side by side and the analysis underwrites to the "
        "Census Bureau's <em>measured</em> &minus;3.2% instead.</p>"
        "<p><strong>Cap rates.</strong> Private net-lease sites publish Jack in the Box cap rates. "
        "None were used. Valuation is a sensitivity grid across an explicit band, and the absence "
        "of an official source is itself recorded as a finding.</p>", "ok"))

    b.append("<h3>Verification mechanics</h3><ul>"
             "<li>Every external URL emitted into <code>docs/</code> is extracted and checked by "
             "<code>tools/check_links.py</code>, which reports malformed URLs, duplicates, and any "
             "non-official domain appearing in a column that claims to be verified.</li>"
             "<li>Every page is scanned by <code>tools/pii_scan.py</code> for personal "
             "identifiers — names, email addresses, street addresses, parcel numbers, telephone "
             "numbers and entity names that could identify the owner or the tenant operator. The "
             "build fails if any are found.</li>"
             "<li>The site is static HTML with no runtime data fetching. Published figures cannot "
             "change after generation, so what a reviewer reads is what was verified.</li>"
             "<li>Each row carries its own <em>as of</em> date because the snapshot mixes Census "
             "Vintage 2025 estimates, ACS 2020–2024 five-year averages, the 2022 Economic Census, "
             "BLS August and September 2026 data, and SEC filings for periods ending September "
             "2025 and July 2026. The Census Bureau itself warns that estimates from different "
             "sources and vintages are not comparable.</li></ul>")

    b.append("<h3>Known limitations of this method</h3><ul>"
             "<li>The U.S. Census Bureau Data API requires a key, which is unavailable here, so "
             "demographic data was read from the server-rendered QuickFacts pages instead. That "
             "limits the analysis to the QuickFacts variable set; tract-level ACS tables were not "
             "reachable.</li>"
             "<li>California Department of Finance projections are published only as spreadsheet "
             "files on a domain this environment cannot reach. The projected values are blank.</li>"
             "<li>Two official tax pages returned HTTP 404 when retrieved, so no tax rate is "
             "asserted anywhere on the site.</li>"
             "<li>Because the parcel is unidentified, no trade-area, traffic-count, zoning, "
             "fire-zone, flood-zone or school-catchment analysis is possible at site level. The "
             "analysis is at market and submarket level and says so.</li></ul>")
    return "".join(b)


def p_privacy():
    b = [head("Privacy and Anonymisation",
              "Personal information privacy is the highest-priority constraint on this project. "
              "This page records exactly what was found, what was removed, and how the "
              "guarantee is enforced mechanically rather than by promise.")]
    b.append(callout("Guarantee",
        "<p>No owner name, entity name, street address, Assessor Parcel Number, telephone number, "
        "email address, transaction price, rent figure, purchase basis or any other personally or "
        "property-identifying value appears anywhere in the published site, in the data snapshot, "
        "or in the repository deliverables. Where such a value would be needed for the analysis, "
        "the field is left blank and labelled <code>INPUT REQUIRED</code> or replaced with the "
        "placeholder <code>PROPERTY-01</code> / <code>OWNER-01</code>.</p>", "ok"))

    b.append("<h3>What was found and how it was handled</h3>")
    b.append(table([
        dict(i="P-1", w="Git commit authorship in the base repository",
             d="The initial commit carries an author identity that includes a personal email address. Git metadata cannot be stripped from history without rewriting it, and rewriting shared history was out of scope.",
             h="The address is never read into, generated into, or rendered by any deliverable. tools/pii_scan.py scans all generated output for email patterns and would fail the build if one appeared. Repository history metadata is explicitly excluded from the published site, which contains no repository metadata at all."),
        dict(i="P-2", w="Franchisee and operator entity names",
             d="Commercial net-lease listing sites publish the names of franchisee entities occupying specific Jack in the Box properties, together with addresses and prices.",
             h="Those sites were consulted only to establish that no official cap-rate source exists. No name, address or price from them was recorded in the data snapshot or rendered on any page. They are also excluded from the Source Register, because they are not official sources."),
        dict(i="P-3", w="Property address, APN, rent, basis",
             d="Never supplied to this project, and not present in the repository.",
             h="Nothing was inferred or fabricated to fill the gap. The model is normalised to R so that it produces a valid ranking without any of these values. See the Property Profile Input Register."),
        dict(i="P-4", w="Tenant executive names",
             d="SEC filings and earnings materials name the issuer's officers.",
             h="Officer names are public corporate disclosure, not personal information about the owner, and none is reproduced on this site. Leadership status is described generically — for example “an interim chief executive” — with a link to the filing for anyone who wants the detail."),
        dict(i="P-5", w="Issuer principal office street address",
             d="Appears on the SEC filing index for Jack in the Box Inc.",
             h="Omitted from the Tenant page. It is public and it is not sensitive, but it is also irrelevant to the decision, so the row records the city and state only with a note explaining the omission."),
    ], [("i", "ID", "", "text"), ("w", "What was found", "", "textn"),
        ("d", "Detail", "", "textn"), ("h", "How it was handled", "", "textn")],
        "privacy", "Privacy findings and dispositions", ""))

    b.append("<h3>Mechanical enforcement</h3>")
    b.append("<p>The guarantee is enforced by code, not by care. "
             "<code>tools/pii_scan.py</code> runs over every generated file in "
             "<code>docs/</code> and over every data module, and fails on:</p><ul>"
             "<li>email addresses and telephone-number patterns;</li>"
             "<li>street-address patterns (a number followed by a street-type word);</li>"
             "<li>Assessor Parcel Number patterns;</li>"
             "<li>the words &ldquo;APN&rdquo;, &ldquo;owner name&rdquo;, &ldquo;mailing "
             "address&rdquo; in a value position;</li>"
             "<li>any personal name appearing in a data value rather than in prose about a public "
             "corporation.</li></ul>"
             "<p><code>tools/check_links.py</code> separately confirms that every URL rendered "
             "into the site is well formed and that no URL from a rejected non-official domain "
             "appears in a column that claims to be verified.</p>")
    b.append("<h3>Internal-only material</h3>")
    b.append("<p>The repository's <code>.gitignore</code> excludes <code>scratch/</code>, "
             "<code>private/</code> and <code>pii/</code> so that any working material containing "
             "identifying detail can never be committed or published by accident. Those "
             "directories do not exist in this repository and were never populated, because no "
             "identifying material was ever supplied.</p>")
    b.append("<h3>Site indexing</h3>")
    b.append("<p>Every page carries <code>&lt;meta name=\"robots\" "
             "content=\"noindex,nofollow\"&gt;</code>. The site is intended for the owner and "
             "their advisers, not for public discovery.</p>")
    return "".join(b)


def p_property_profile():
    b = [head("Property Profile and Input Register",
              "What is known about PROPERTY-01, and — more usefully — the exact list of what is "
              "not. Nothing on this page has been inferred.")]
    b.append(callout("F-01 — the subject property was never identified",
        "<p>No street address, Assessor Parcel Number, lot size, building size, year built, "
        "purchase date, purchase price, cost basis, current base rent, escalation schedule, "
        "remaining primary term, renewal options, guaranty status or tenant sales history was "
        "supplied to this analysis, and none is present in the repository. Every one of those "
        "fields is left blank below.</p>"
        "<p>This is the largest single limitation on the whole file, and it is disclosed rather "
        "than papered over. The consequence is that this is a <strong>market and submarket "
        "analysis with a parameterised model</strong>, not a property appraisal. It is still "
        "decision-useful, because the model is normalised to R and the tenant, market and hazard "
        "evidence does not depend on the address — but it cannot tell you what your building is "
        "worth.</p>", "bad"))

    b.append("<h3>Known attributes</h3>")
    b.append(table([
        dict(k="Asset type", v="Single-tenant net-leased (NNN) restaurant property", s="From the brief"),
        dict(k="Occupier brand", v="Jack in the Box", s="From the brief"),
        dict(k="Lease structure", v="Triple net — tenant pays property taxes, insurance and maintenance", s="From the brief; consistent with the issuer's own disclosed lease terms"),
        dict(k="Primary term expiry", v="Between 2030 and 2035 — a five-year range, not a date", s="From the brief"),
        dict(k="Market", v="Central Los Angeles", s="From the brief; not an official geography — see the Geography page"),
        dict(k="Tenure", v="Blank", s="Not supplied — freehold or ground lease changes the analysis materially"),
        dict(k="Internal reference", v="PROPERTY-01 / OWNER-01", s="Placeholder used throughout this site in place of any identifying value"),
    ], [("k", "Attribute", "", "text"), ("v", "Value", "", "textn"),
        ("s", "Basis", "", "textn")],
        "known", "Attributes stated in the brief", ""))

    b.append("<h3>Input Register</h3>")
    b.append('<p>Every field below is required to convert this market analysis into a '
             'property-level decision. Complete it privately; <code>model/projection.py</code> '
             'accepts the values directly and needs no re-engineering. Fields marked '
             '<span class="req">DECISION-CRITICAL</span> change which strategies are even '
             'available.</p>')
    b.append(table([
        dict(f="Street address", why="Required for fire zone, flood zone, zoning, traffic counts and school catchment", c="DECISION-CRITICAL", u="https://zimas.lacity.org/"),
        dict(f="Assessor Parcel Number", why="The unambiguous key for every county and city lookup", c="DECISION-CRITICAL", u="https://assessor.lacounty.gov/"),
        dict(f="Tenure — freehold or ground lease", why="A ground lease expiring near the tenant's expiry can make the asset unsaleable", c="DECISION-CRITICAL", u=""),
        dict(f="Current annual base rent", why="This is R. Every model output multiplies by it", c="DECISION-CRITICAL", u=""),
        dict(f="Escalation schedule", why="Determines whether the income stream keeps pace with the tenant's cost inflation", c="DECISION-CRITICAL", u=""),
        dict(f="Exact primary term expiry date", why="The brief gives a five-year range; the model tests 2030, 2032 and 2035 separately because the answer differs", c="DECISION-CRITICAL", u=""),
        dict(f="Renewal options — number, length, and WHO may exercise", why="The issuer discloses that its own lease options are generally exercisable at the company's sole discretion. If the owner's lease is the same, strategy S3 is the tenant's choice, not the owner's", c="DECISION-CRITICAL", u=""),
        dict(f="Corporate guaranty — present or absent", why="Determines whether the counterparty is a NASDAQ-listed company or a single franchisee. This is the largest credit question in the file", c="DECISION-CRITICAL", u=""),
        dict(f="Percentage-rent clause", why="The issuer discloses that about 13% of its leases carry contingent rent of 1% to 10% of gross sales; if present it partly protects the owner against tenant sales decline", c="High", u=""),
        dict(f="Building size (sq ft) and lot size (acres)", why="Determines re-tenanting feasibility and redevelopment potential", c="High", u=""),
        dict(f="Year built and construction type", why="Drives seismic exposure, insurance cost and capital reserve", c="High", u=""),
        dict(f="Purchase date and price; cost basis and accumulated depreciation", why="Determines the tax cost of selling, and therefore net proceeds", c="High", u=""),
        dict(f="Tenant sales history and rent-to-sales ratio", why="The strongest single predictor of non-renewal at a specific site", c="High", u=""),
        dict(f="Franchise agreement expiry date for this restaurant", why="The issuer closes restaurants “based upon respective franchise agreement termination dates”. If that date precedes the lease expiry, the risk is higher than the lease alone suggests", c="DECISION-CRITICAL", u=""),
        dict(f="Whether the site is on the operator's closure list", why="Answered by one conversation with the tenant; determines whether strategy S5 is available at all", c="DECISION-CRITICAL", u=""),
        dict(f="Current insurance carrier, premium and renewal date", why="An uninsurable asset cannot be sold to a financed buyer", c="High", u="https://www.insurance.ca.gov/"),
        dict(f="Existing debt, rate, maturity and prepayment terms", why="Determines whether a sale can even be executed cleanly", c="High", u=""),
        dict(f="CAL FIRE Fire Hazard Severity Zone (2025 map)", why="The county was re-mapped in 2025; any pre-2025 determination is stale", c="High", u="https://frap.fire.ca.gov/projects/hazard/fhz"),
        dict(f="Zoning designation and permitted uses", why="The only evidence that would make redevelopment outrank selling", c="High", u="https://zimas.lacity.org/"),
        dict(f="Traffic count on the frontage road", why="Primary demand driver for a drive-thru asset", c="Medium", u="https://dot.ca.gov/programs/traffic-operations/census"),
    ], [("f", "Field required", "", "textn"), ("why", "Why it matters to the decision", "", "textn"),
        ("c", "Priority", "", "rawpri"), ("u", "Official lookup", "", "rawurl3")],
        "inputs", "Input Register — 20 fields, all currently blank", ""))
    return "".join(b)


def p_geography():
    b = [head("Geography and Market Definition",
              "&ldquo;Central Los Angeles&rdquo; is not a legal or statistical geography. This "
              "page records exactly what it was mapped to, why, and what that means for every "
              "figure on the site.")]
    b.append(callout("R-5 — the market label is not an official geography",
        "<p>&ldquo;Central Los Angeles&rdquo; has no FIPS code, no Census definition and no "
        "statistical boundary. It is used variously to mean the Central City planning area, the "
        "Wilshire corridor, a wider central subregion, or simply &ldquo;not the Valley and not "
        "the beach&rdquo;. Every aggregate statistic quoted on this site therefore belongs to one "
        "of three official geographies, and each is labelled.</p>", "warn"))
    b.append(table([
        dict(g="Los Angeles County", f="06037", d="County", why="The narrowest official geography that has a complete, published QuickFacts dataset for every variable needed. Used for all county-level rows.",
             u="https://www.census.gov/quickfacts/losangelescountycalifornia"),
        dict(g="City of Los Angeles", f="0644000", d="Incorporated place", why="The most likely municipal jurisdiction for a “Central Los Angeles” property, and the jurisdiction whose minimum-wage ordinance applies. Note that several QuickFacts fields are not published at city level and appear as [X].",
             u="https://www.census.gov/quickfacts/losangelescitycalifornia"),
        dict(g="Los Angeles–Long Beach–Anaheim, CA MSA", f="31080", d="Metropolitan Statistical Area", why="The geography for which BLS publishes labour force, unemployment and metropolitan employment data. Used for all employment rows.",
             u="https://www.bls.gov/regions/west/ca_losangeles_msa.htm"),
        dict(g="Los Angeles–Long Beach, CA Metropolitan Division", f="", d="Metropolitan Division", why="BLS publishes the LA–Long Beach–Glendale division separately within the MSA, using time-series models with real-time benchmarking to national CPS totals. Referenced for context on the metropolitan employment series.",
             u="https://www.bls.gov/news.release/pdf/metro.pdf"),
        dict(g="Central City / Wilshire / South Los Angeles Community Plan Areas", f="", d="City of Los Angeles planning areas", why="The plausible sub-municipal candidates for “Central Los Angeles”. Cannot be selected without the property address; no CPA-level statistic is asserted anywhere on this site.",
             u="https://planning.lacity.gov/"),
    ], [("g", "Official geography", "", "textn"), ("f", "FIPS", "", "text"),
        ("d", "Type", "", "text"), ("why", "Why it is used here", "", "textn"),
        ("u", "Official source", "", "rawurl3")],
        "geos", "The geography mapping, disclosed", ""))

    b.append("<h3>What this mapping costs the analysis</h3>")
    b.append("<p>County and metropolitan aggregates are the wrong granularity for a single "
             "drive-thru restaurant. A quick-service site trades on a drive-time ring of a few "
             "minutes, and Los Angeles County contains 2,492 census tracts with more than ten "
             "million dollars of building value each — with radically different demographic "
             "profiles. A county population decline of 3.2% is entirely compatible with a "
             "specific trade area growing.</p>"
             "<p>The honest position, and the one taken here, is that these aggregates establish "
             "<strong>direction and context</strong>, not site-level demand. They are sufficient "
             "to establish that the owner cannot assume demographic growth, and that the tenant's "
             "reported transaction declines are consistent with the regional picture. They are "
             "<em>not</em> sufficient to establish that this particular corner is deteriorating. "
             "That requires the address.</p>")
    b.append(callout("What becomes possible once the address is supplied",
        "<p>Census tract population, households, median income and vehicle availability from ACS "
        "table B03002 and related tables; CAL FIRE Fire Hazard Severity Zone from the 2025 map; "
        "FEMA flood zone and National Risk Index tract score; City of Los Angeles zoning and "
        "Community Plan Area; Caltrans traffic census at the nearest station; assigned schools "
        "and their California School Dashboard ratings; LA County assessed value and tax rate. "
        "Every one of these has an official source, and every one is listed on the "
        "<a href='flagged-for-review.html'>Flagged for Review</a> page with its lookup route.</p>",
        "ok"))
    return "".join(b)


def p_lease_economics():
    b = [head("NNN Lease Economics",
              "How a triple-net single-tenant restaurant lease actually works, what the "
              "tenant's own disclosed lease terms reveal about its behaviour, and where the "
              "owner's exposure sits.")]
    b.append("<h3>What NNN means here</h3>")
    b.append(table([
        dict(c="Property taxes", p="Tenant", n="Under a true NNN lease the tenant reimburses or pays directly. The owner's exposure is nil unless the lease is modified gross or the tenant defaults."),
        dict(c="Property and liability insurance", p="Tenant", n="The tenant must insure the building and name the owner. Verify the clause requires the tenant to keep it in force — in California, availability is now a real risk (see B-07)."),
        dict(c="Maintenance and repair", p="Tenant", n="Including roof, structure and parking in an absolute NNN. In a standard NNN the landlord may retain structural responsibility — this distinction is worth real money and must be read from the document."),
        dict(c="Capital replacements", p="Depends on the document", n="The single most common source of dispute. An absolute NNN pushes these to the tenant; a standard NNN often leaves them with the owner. Confirm which this is."),
        dict(c="Base rent", p="Tenant", n="Fixed, with escalation. The issuer discloses that its own leases use fixed rent with cost-of-living index adjustments."),
        dict(c="Percentage rent", p="Tenant, if present", n="The issuer discloses that approximately 13% of its leases carry contingent rent of 1% to 10% of gross sales. If the owner's lease has this, it partly protects against tenant sales decline."),
        dict(c="Rollover and vacancy risk", p="Owner", n="This is the entire exposure. Everything above is transferred to the tenant; nothing transfers the risk that the tenant leaves."),
    ], [("c", "Cost or risk", "", "text"), ("p", "Who bears it", "", "text"),
        ("n", "Notes and what to verify", "", "textn")],
        "nnn", "Allocation under a triple-net structure", ""))

    b.append(callout("The structural insight",
        "<p>NNN leasing is often described as passive ownership. It is not. It transfers every "
        "<em>operating</em> cost to the tenant and leaves the owner with 100% of the "
        "<em>continuation</em> risk. The owner's return is therefore not a function of how well "
        "the property is managed — there is nothing to manage — but entirely of whether one "
        "counterparty keeps wanting the site. Every page of this file is about that single "
        "question.</p>", "ok"))

    b.append("<h3>What the tenant's own leases reveal</h3>")
    b.append("<p>The owner's lease document was not supplied. The best available evidence of how "
             "this brand behaves at expiry is the lease terms the issuer itself discloses in its "
             "Form 10-K — as both lessee of hundreds of restaurants and lessor to hundreds of "
             "franchisees.</p>")
    b.append(table([
        dict(t="Initial term", v="Generally 20 years, exclusive of renewal options", i="A 20-year term beginning around 2010–2015 expires in 2030–2035. The stated window is consistent with a standard initial term reaching its end, not with an option period."),
        dict(t="Renewal options", v="Generally exercisable at the company's sole discretion, 1 to 20 years", i="If the owner's lease mirrors this, the option belongs to the tenant. The owner cannot compel a renewal and cannot compel a surrender either."),
        dict(t="Franchise agreement term", v="20 years, with a $50,000 initial fee", i="The franchise agreement and the real estate lease often expire on similar dates. The issuer closes restaurants based on franchise agreement termination dates — so the two clocks matter together."),
        dict(t="Rent formula", v="Fixed rent with cost-of-living index adjustments, plus taxes, insurance and other expenses", i="Confirms NNN structure and CPI-linked escalation. Verify which index and what cap."),
        dict(t="Percentage rent", v="About 13% of leases carry contingent rent of 1% to 10% of gross sales", i="A minority feature. If present it is valuable here, because it shares downside with the owner."),
        dict(t="Development cost", v="$1.3 million to $1.9 million per restaurant, excluding land", i="Establishes the replacement cost of the improvement. Relevant to insurance adequacy and to what a buyer is acquiring."),
        dict(t="Prototype", v="Approximately 1,372 sq ft, off-premise and drive-thru focused, Y-Lane capable", i="A small, highly specialised building. Limited alternative uses without capital adaptation — which is why the model charges re-tenanting capital."),
        dict(t="Closure and lease obligations", v="The issuer states that if it closes a leased restaurant it may remain committed to the lease including base rent for the balance of the term", i="Two-edged. It means a closure does not automatically end the rent — but it also means the issuer has a documented incentive to keep marginal sites open rather than pay, and to negotiate hard at expiry."),
        dict(t="Real estate strategy", v="Uses sales and sale-leaseback financing and offers franchisees the opportunity to buy the property they occupy; $19.9 million of property sale proceeds in FY2025; gains on sales of real estate to franchisees of $9,491 thousand in the first three quarters of FY2026", i="The brand is a net SELLER of restaurant real estate and actively markets properties to its own franchisees. That is both a comparable buyer pool for the owner and evidence that the owner is not the only one exiting."),
    ], [("t", "Term", "", "text"), ("v", "As disclosed by the issuer", "", "textn"),
        ("i", "Implication for the owner", "", "textn")],
        "leases", "Disclosed lease and franchise economics", "All rows from the Form 10-K for fiscal 2025, filed 19 November 2025."))
    b.append('<p class="small">Source: <a href="https://www.sec.gov/Archives/edgar/data/'
             '807882/000080788225000072/jack-20250928.htm" target="_blank" rel="noopener '
             'noreferrer">Jack in the Box Inc. Form 10-K, fiscal year ended 2025-09-28 &#8599;</a></p>')

    b.append("<h3>Where the owner's exposure actually sits</h3>")
    b.append(table([
        dict(e="Tenant vacates at expiry and the box does not re-let quickly", s="Severe", n="The model charges 1.5 years of downtime and 1.5 R of capital in the base case, 3.0 years and 3.0 R in the pessimistic case. That swing alone moves a strategy from 12.30 R to 2.51 R."),
        dict(e="Tenant exercises an option at a below-market rent", s="Moderate", n="If options are at fixed pre-set rents rather than at market, the owner is locked into a below-market income stream. Read the option rent mechanic."),
        dict(e="Tenant stays but demands a rent reduction", s="Moderate", n="With system same-store sales negative in every recent period, the tenant has a credible argument. A rent concession resets R permanently."),
        dict(e="Tenant closes but remains liable for base rent", s="Mild — but temporary", n="The issuer's own risk factor confirms this obligation exists. It buys time, not a solution: a vacant box generating rent from a departing tenant is still a vacant box at the end of the term."),
        dict(e="Building is destroyed or made uninsurable", s="Severe", n="Under NNN the tenant insures, but if insurance becomes unavailable the lease cannot be performed. See B-07. This is a total-loss mechanism requiring no physical damage."),
        dict(e="Land value falls because the county loses population", s="Moderate", n="Terminal value in strategies S2 and S6 depends on the alternative use of the land. A shrinking county weakens every alternative use."),
    ], [("e", "Exposure", "", "textn"), ("s", "Severity", "", "text"),
        ("n", "Detail", "", "textn")],
        "exposures", "Owner exposure map", ""))
    return "".join(b)


def p_infrastructure():
    b = [head("Infrastructure, Land Use and Schools",
              "The physical and civic value drivers for a Central Los Angeles site. This page is "
              "deliberately short on asserted numbers: the official project pages were located but "
              "not read in this session, so nothing here is presented as verified.")]
    b.append(callout("F-11 — values on this page are unverified",
        "<p>Transit project dates, costs and school performance figures were located in secondary "
        "sources during this analysis but were <strong>not</strong> read on an official "
        "<code>metro.net</code>, <code>planning.lacity.gov</code> or <code>cadedash.net</code> "
        "page. No date, cost or rating is therefore asserted. What follows is the list of official "
        "routes to check, with an explanation of why each one matters to this decision.</p>", "warn"))
    b.append(table([
        dict(d="Rail and bus projects affecting Central Los Angeles",
             why="A new rail station inside the trade area changes daypart traffic patterns and can support a higher alternative use for the land — which is the only mechanism by which strategy S6 outranks selling.",
             u="https://www.metro.net/projects/", s="Los Angeles County Metropolitan Transportation Authority"),
        dict(d="Zoning designation, permitted uses and any overlay or specific plan",
             why="Determines whether a vacated restaurant box can be re-let to another use, and whether the land supports a better use. Without this, redevelopment upside is hope rather than analysis.",
             u="https://zimas.lacity.org/", s="City of Los Angeles, Zoning Information and Map Access System"),
        dict(d="Community Plan Area and general plan land use designation",
             why="The city’s own long-range land use statement for the parcel. Drives what an entitlement process could achieve and how long it would take.",
             u="https://planning.lacity.gov/", s="City of Los Angeles Department of City Planning"),
        dict(d="Parcel record, assessed value and tax rate",
             why="Under a NNN lease the tenant reimburses property taxes, but the assessed value resets on a change of ownership — which affects both the tenant’s cost after a sale and the buyer’s underwriting.",
             u="https://assessor.lacounty.gov/", s="Los Angeles County Office of the Assessor"),
        dict(d="Traffic census — average daily traffic on the frontage road",
             why="The primary demand driver for a drive-thru asset, and the first number any replacement tenant or buyer will ask for. Broker marketing material quoting counts was NOT used, because it is not an official source.",
             u="https://dot.ca.gov/programs/traffic-operations/census", s="California Department of Transportation"),
        dict(d="Assigned schools and their accountability ratings",
             why="Requested in the brief. For a drive-thru quick-service asset, school quality is a weak direct value driver compared with traffic counts, household density and daypart employment — but it is a real signal of neighbourhood trajectory and of the alternative residential use that strategy S6 depends on.",
             u="https://www.cadedash.net/", s="California Department of Education"),
        dict(d="District enrolment trend",
             why="Falling district enrolment is a leading indicator of falling family population in a submarket, and it moves ahead of the census estimates.",
             u="https://www.lausd.org/", s="Los Angeles Unified School District"),
        dict(d="Fire Hazard Severity Zone of the parcel — 2025 map",
             why="Los Angeles County Local Responsibility Area zones were re-established in 2025, adding Moderate and High categories where the prior map showed only Very High. Any pre-2025 determination is stale.",
             u="https://frap.fire.ca.gov/projects/hazard/fhz", s="CAL FIRE, Fire and Resource Assessment Program"),
        dict(d="Flood zone and post-fire debris-flow exposure",
             why="Determines insurance cost and availability, which under NNN is the tenant’s obligation but the owner’s problem if the tenant cannot perform.",
             u="https://www.fema.gov/flood-maps", s="Federal Emergency Management Agency"),
    ], [("d", "What to look up", "", "textn"), ("why", "Why it matters to this decision", "", "textn"),
        ("s", "Official publisher", "", "text"), ("u", "Route", "", "rawurl3")],
        "infra", "Official reference routes", "All values currently blank — see F-08, F-09, F-10 and F-11."))

    b.append("<h3>What can be said without the address</h3>")
    b.append("<p>Two observations are supportable from verified regional data and do not depend on "
             "the parcel.</p>"
             "<p>First, Los Angeles County accommodation and food services sales were "
             "<strong>$44,016,586,000</strong> in 2022, and the City of Los Angeles accounted for "
             "<strong>$17,366,966,000</strong> of that — 39.5% of the county total in a city with "
             "39.8% of the county population. The demand pool is large and proportionate. The "
             "tenant is not in a market that lacks spending; it is in a market where its own "
             "transaction counts are falling, which points to brand and site-level problems rather "
             "than to an absence of demand. Source: U.S. Census Bureau 2022 Economic Census via "
             "QuickFacts.</p>"
             "<p>Second, the county has <strong>437,788</strong> employer establishments and "
             "<strong>1,184,030</strong> in the City of Los Angeles, with annual payroll of "
             "<strong>$550.7 billion</strong> countywide. Employer-establishment density of "
             "<strong>172.8 per square mile</strong> in the county and <strong>464.6</strong> in "
             "the city indicates a genuinely dense urban commercial environment. That supports "
             "alternative uses for the land — which is the single most important fact for strategy "
             "S6, and it is verified. Source: U.S. Census Bureau County Business Patterns and "
             "QuickFacts.</p>")
    b.append(callout("The infrastructure conclusion",
        "<p>Whatever the specific transit project, the verified evidence is that this is a dense, "
        "high-employment, high-spending urban market whose <em>population</em> is shrinking while "
        "its <em>commercial base</em> remains very large. For a landlord that combination favours "
        "the land over the building: the improvement is a specialised 1,372 square foot drive-thru "
        "box, but the site sits in one of the densest employer markets in the United States. That "
        "is why the model gives strategy S6 (hold then redevelop) real weight — and why the zoning "
        "lookup in the Input Register is worth paying for before dismissing it.</p>", "ok"))
    return "".join(b)


def p_taxes():
    b = [head("Tax and Transaction Framework",
              "The mechanisms that apply when this asset is sold, and the official sources for "
              "each. No tax rate is asserted anywhere on this page.")]
    b.append(callout("F-05 — no tax rate is published here",
        "<p>The relevant official pages were not successfully retrieved during this analysis: one "
        "Internal Revenue Service URL and one California Franchise Tax Board URL both returned "
        "HTTP 404. Third-party sources state a California top rate of 13.3% and a 3&nbsp;1/3% "
        "real-estate withholding, but none of these figures was read on an official page, so none "
        "is asserted.</p>"
        "<p>Publishing an unverified tax rate on a site the owner will rely on for a "
        "seven-figure decision is precisely the failure mode this project was told to avoid. The "
        "mechanisms below are described structurally and linked to their official sources. Get a "
        "written opinion from a California-licensed CPA before acting on any of it.</p>", "bad"))
    b.append(table([
        dict(m="Federal income tax on gain",
             w="Gain over adjusted basis is taxable on a sale. Rates depend on holding period, filing status and taxable income.",
             u="https://www.irs.gov/", o="Internal Revenue Service",
             q="Current rate schedule for long-term capital gain; unrecaptured section 1250 gain treatment for a depreciated commercial building."),
        dict(m="Depreciation recapture",
             w="A commercial building held for years has been depreciated. Recapture tax applies to the lesser of gain or accumulated depreciation, at its own rate. For a long-held NNN asset this is often the largest single surprise in the tax computation.",
             u="https://www.irs.gov/", o="Internal Revenue Service",
             q="Accumulated depreciation to date; the applicable recapture rate; whether cost-segregation study was performed."),
        dict(m="Net investment income tax",
             w="An additional federal surtax may apply to net investment income above a threshold, including gain on the sale of rental real property.",
             u="https://www.irs.gov/", o="Internal Revenue Service",
             q="Whether the owner's modified adjusted gross income exceeds the threshold in the year of sale."),
        dict(m="Like-kind exchange under IRC section 1031",
             w="Defers federal gain if replacement property of like kind is identified within 45 days and acquired within 180 days. For real property this remains available after the 2017 limitation of section 1031 to real property only.",
             u="https://www.irs.gov/forms-pubs/about-form-8824", o="Internal Revenue Service, Form 8824",
             q="Whether the owner wants to stay in real estate at all. If the objective is diversification, an exchange works against it — the whole point of selling may be to stop holding one illiquid asset in one county."),
        dict(m="California income tax on gain",
             w="California taxes capital gain as ordinary income through its progressive rate schedule. There is no separate preferential long-term rate at state level.",
             u="https://www.ftb.ca.gov/", o="California Franchise Tax Board",
             q="Current rate schedule and the threshold at which the additional mental health services surtax applies."),
        dict(m="California real-estate withholding",
             w="California requires withholding on the sale of California real property unless an exemption is claimed and certified at closing.",
             u="https://www.ftb.ca.gov/forms/593.html", o="California Franchise Tax Board, Form 593",
             q="Withholding rate; whether the transaction qualifies for an exemption; who must certify."),
        dict(m="California deferred-gain tracking after an out-of-state exchange",
             w="If a California property is exchanged for property outside California, the Franchise Tax Board tracks the deferred California-source gain and requires annual reporting while the out-of-state replacement is held.",
             u="https://www.ftb.ca.gov/forms/3840.html", o="California Franchise Tax Board, Form 3840",
             q="This is a multi-year compliance obligation that most owners do not know exists. Confirm it before exchanging out of state."),
        dict(m="Property tax and the effect of a change in ownership",
             w="California limits property tax through the state constitution and reassesses on a change in ownership. A sale therefore resets the assessed value — which changes the tenant's NNN tax reimbursement and the buyer's underwriting from day one.",
             u="https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?lawCode=CONST&division=&title=&part=&chapter=&article=XIII%20A", o="California Constitution, Article XIII A",
             q="Current assessed value; the reassessed value implied by the sale price; any exclusion that might apply."),
        dict(m="Documentary transfer tax",
             w="A city or county transfer tax may apply on the conveyance. Los Angeles imposes one, and the rate and any applicable exemptions change over time.",
             u="https://ttc.lacounty.gov/", o="Los Angeles County Treasurer and Tax Collector",
             q="Whether the property is inside the City of Los Angeles, which imposes its own transfer tax in addition to the county's."),
        dict(m="Transaction friction",
             w="Broker commission, legal fees, lender exit or prepayment costs, and any title and escrow charges. The model assumes a base of 4.5% of price, swept from 2.0% to 7.0%.",
             u="", o="Modelling assumption — no official source exists",
             q="Whether any existing debt has a prepayment penalty or defeasance obligation. This can be large enough to change the answer and must be read from the loan documents."),
    ], [("m", "Mechanism", "", "textn"), ("w", "What it is", "", "textn"),
        ("o", "Official publisher", "", "text"), ("u", "Official source", "", "rawurl3"),
        ("q", "Questions to resolve", "", "textn")],
        "tax", "Tax and transaction mechanisms", "Every rate cell on this page is intentionally blank."))

    b.append("<h3>How tax interacts with the decision</h3>")
    b.append("<p>Three points are structural and do not depend on any rate.</p><ol>"
             "<li><strong>Net proceeds decide the comparison, not gross price.</strong> The model "
             "applies friction before comparing strategies. A 4.5% friction assumption is a "
             "placeholder; the real figure includes tax, and tax on a long-held depreciated "
             "building can be very large.</li>"
             "<li><strong>A like-kind exchange is not automatically the right answer here.</strong> "
             "It defers tax, but it requires buying more real estate. If the reason to sell is "
             "concentration in one illiquid single-tenant asset in one shrinking county, an "
             "exchange preserves exactly the exposure the sale was meant to remove. This trade-off "
             "should be made deliberately, not by default.</li>"
             "<li><strong>Holding is not tax-free either.</strong> A hold keeps collecting taxable "
             "rent, keeps the building depreciating toward a larger recapture position, and defers "
             "the decision into a period when the tenant's own closure programme is actively "
             "evaluating the site. The tax cost of waiting is real even though no tax is payable "
             "while waiting.</li></ol>")
    b.append(callout("Action",
        "<p>Item 5 of the sequenced action plan on the "
        "<a href='decision.html'>Decision Framework</a> page: obtain a written California tax "
        "opinion covering gain, depreciation recapture, section 1031 eligibility, withholding and "
        "any deferred-gain reporting obligation, <em>before</em> signing a listing agreement. Bring "
        "the official source links in the table above to that conversation.</p>", "warn"))
    return "".join(b)


def p_sources():
    rows = []
    for i, s in enumerate(flags.SOURCES, 1):
        rows.append(dict(n=f"S-{i:02d}", **s))
    b = [head("Source Register",
              f"Every official source used in this analysis: {len(flags.SOURCES)} entries, each "
              "with its publisher, publication or filing date, accession number where one exists, "
              "and exactly what was taken from it.")]
    b.append(callout("How to use this page",
        "<p>Every URL below is the page the figure was read from. Open it and the value should be "
        "findable without further navigation. Where a source is a large document — a Form 10-K, a "
        "BLS economic summary — the <em>Used for</em> column names the specific table or "
        "disclosure. If a figure on this site cannot be located from its linked source, that is a "
        "defect and should be reported.</p>", "ok"))
    b.append(table(rows, [
        ("n", "#", "num", "text"), ("publisher", "Publisher", "", "textn"),
        ("title", "Title", "", "textn"), ("filed", "Filed / published", "", "text"),
        ("access_no", "Accession / identifier", "", "text"),
        ("tier", "Evidence tier", "", "rawtier"),
        ("used_for", "What was taken from it", "", "textn"),
        ("url", "Link", "", "rawurl4")],
        "sources", "Complete source register", ""))

    b.append("<h3>Reference routes for the flagged items</h3>")
    b.append("<p>These official pages are not sources of any published value. They are the routes "
             "the owner uses to complete the items on the "
             "<a href='flagged-for-review.html'>Flagged for Review</a> page.</p>")
    b.append(table(flags.REFERENCE_ROUTES, [
        ("name", "Official resource", "", "textn"), ("url", "Route", "", "rawurl4")],
        "routes", "Reference routes", ""))

    b.append("<h3>Sources deliberately excluded</h3>")
    b.append("<p>The following categories were consulted during research and then "
             "<strong>rejected</strong>. None appears in the register above, and no value from any "
             "of them is asserted anywhere on this site.</p><ul>"
             "<li>Commercial net-lease listing and aggregator sites. They publish Jack in the Box "
             "cap rates, prices and franchisee names. Used only to establish that no official "
             "cap-rate source exists. Rejected as evidence, and rejected as a privacy risk.</li>"
             "<li>Media restatements of government data. Where the government page was reachable, "
             "the government page was used. Where it was not, the value is blank.</li>"
             "<li>Analyst ratings and price targets. Private commercial opinion.</li>"
             "<li>Rating-agency credit opinions. Private issuers, not official sources. The tenant "
             "credit page therefore publishes no rating.</li>"
             "<li>Investor-forum and social commentary. Not evidence of anything.</li></ul>")
    return "".join(b)


def p_flagged():
    rows = []
    for f in flags.FLAGGED:
        rows.append(f)
    b = [head("Flagged for Review",
              f"{len(flags.FLAGGED)} items that are blank, unverified, conflicting, or that need "
              "input from the owner. Per the brief, a flagged item does not block publication — "
              "it is published here, with the official route to resolve it.")]
    sev = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in flags.FLAGGED:
        sev[f["severity"]] = sev.get(f["severity"], 0) + 1
    b.append('<div class="grid g4">')
    b.append(stat("High severity", str(sev.get("HIGH", 0)), "materially limits the decision", "", "neg"))
    b.append(stat("Medium severity", str(sev.get("MEDIUM", 0)), "affects a specific strategy or page", "", ""))
    b.append(stat("Low severity", str(sev.get("LOW", 0)), "disclosure and data hygiene", "", ""))
    b.append(stat("Blocking publication", "0", "nothing here stops the site being published or the decision being made", "", "pos"))
    b.append('</div>')
    b.append(table(rows, [
        ("id", "ID", "num", "text"), ("severity", "Severity", "", "rawsev"),
        ("status", "Status", "", "rawpri"), ("item", "Item", "", "textn"),
        ("detail", "What the issue is", "", "textn"),
        ("why_blank", "Why it is blank", "", "textn"),
        ("action_for_owner", "How to resolve it", "", "textn"),
        ("official_check", "Official route", "", "rawurl4")],
        "flagged", "Flagged items", ""))

    b.append("<h3>Detail</h3>")
    for f in flags.FLAGGED:
        oc = f.get("official_check") or ""
        ocl = (f'<p style="margin:8px 0 0"><a href="{esc(oc)}" target="_blank" '
               f'rel="noopener noreferrer">Official route to confirm &#8599;</a></p>') if oc else ""
        b.append(f'''<div class="panel"><h3 style="margin-top:0">{esc(f["id"])} &mdash; {esc(f["item"])}
{badge(f["severity"], {"HIGH":"b-bad","MEDIUM":"b-warn","LOW":"b-info"}[f["severity"]])}
{badge(f["status"], "b-neutral")}</h3>
<p><strong>What the issue is:</strong> {esc(f["detail"])}</p>
<p><strong>Why it is blank:</strong> {esc(f["why_blank"])}</p>
<p style="margin-bottom:0"><strong>How to resolve it:</strong> {esc(f["action_for_owner"])}</p>{ocl}</div>''')

    b.append(callout("Other irregularities found during the analysis",
        "<p><strong>Los Angeles city race and ethnicity shares do not reconcile.</strong> The "
        "QuickFacts race-category shares returned for Los Angeles city sum to roughly 74%, while "
        "the equivalent county shares sum to 99.8%. One or more city values appear to have been "
        "mis-extracted during retrieval. The city race breakdown is omitted from the "
        "Demographics page entirely rather than published with a possibly wrong figure (F-12). "
        "None of the decision-relevant variables — population, income, poverty, density, "
        "foreign-born share, age structure — is affected.</p>"
        "<p><strong>Los Angeles city building permits and housing units show [X].</strong> The "
        "Census Bureau marks these as not available at place level. They are rendered blank with "
        "the QuickFacts note reproduced, and county values are never substituted (F-13).</p>"
        "<p><strong>Two official forecasters disagree on the sign of population change.</strong> "
        "This is not an error on this site — it is a genuine conflict between SCAG and the "
        "California Department of Finance, published side by side on the "
        "<a href='projections.html'>Official Forecasts</a> page and resolved by underwriting to "
        "measured Census data instead.</p>"
        "<p><strong>SEC EDGAR search ignores date filters.</strong> The EDGAR browse interface "
        "returned the most recent filings regardless of the requested date range. Filing history "
        "was therefore assembled from the filing index pages directly. Recorded so that any "
        "reviewer reproducing the work does not assume a date-filtered query worked.</p>", "warn"))
    return "".join(b)


def p_repo_review():
    b = [head("Repository Review",
              "The line-by-line audit of the repository as it was found, the irregularities "
              "identified in it, and what was built on top of it.")]
    b.append("<h3>State of the repository at the base commit</h3>")
    b.append(table([
        dict(p="README.md", s="7 bytes", c="Single line: a level-1 heading containing the repository name."),
        dict(p="(nothing else)", s="—", c="No source code, no data, no configuration, no continuous integration, no GitHub Pages settings, no licence, no contributing guide, no issue templates."),
    ], [("p", "Path", "", "text"), ("s", "Size", "", "text"),
        ("c", "Content", "", "textn")],
        "baseline", "File inventory at commit 0c9e609", ""))
    b.append("<p>The repository contained a single commit with the message "
             "<code>Initial commit</code>. There was no analysis, no website, no data and no "
             "build system to review. The audit therefore became a statement of what was absent "
             "and what had to be created.</p>")

    b.append("<h3>Irregularities identified</h3>")
    b.append(table([
        dict(id="R-1", f="Empty scaffold presented as a project", d="A repository named for a specific analysis contained none of it. Every deliverable in this file was built from an empty base.", s="Resolved", a="Full structure created: data/, model/, tools/, site/, docs/, research/, plus this review."),
        dict(id="R-2", f="Personal information in git history", d="The initial commit carries an author identity including a personal email address.", s="Contained", a="Git history was not rewritten, because rewriting shared history was out of scope and the branch is tracked. The address is never read into or rendered by any deliverable, and tools/pii_scan.py would fail the build if an email pattern appeared in generated output. See the Privacy page, item P-1."),
        dict(id="R-3", f="No property identification supplied", d="No address, APN, lot size, building size, rent, escalation schedule, basis, guaranty status or lease document exists in the repository or the brief.", s="Flagged F-01", a="Analysis performed at market and submarket level with a parameterised model normalised to R. Property-specific fields left blank and collected in an Input Register."),
        dict(id="R-4", f="The expiry date is a range, not a date", d="“Between 2030 and 2035” spans five years and materially changes lease economics — the model produces different rankings for 2030, 2032 and 2035.", s="Resolved", a="All three points are evaluated separately and reported side by side. No single year is silently chosen."),
        dict(id="R-5", f="“Central Los Angeles” is not an official geography", d="The label has no FIPS code and no statistical boundary, yet every aggregate statistic must belong to some official geography.", s="Resolved", a="Mapped explicitly to Los Angeles County (06037), City of Los Angeles (0644000) and the Los Angeles–Long Beach–Anaheim MSA (31080). Every row is labelled with its geography. See the Geography page."),
        dict(id="R-6", f="No official source exists for the key valuation input", d="No United States government agency publishes commercial capitalisation rates or single-tenant net-lease comparable sales. The single most important number in a sell-versus-hold decision is unverifiable from official sources.", s="Flagged F-02", a="No cap rate is asserted anywhere. Valuation is presented as a sensitivity grid across an explicit 5.0%–8.5% band, with the absence of an official source recorded as a finding in its own right."),
        dict(id="R-7", f="Coordination file committed with pre-marked task statuses", d="COORDINATION.md was first committed with tasks marked done before the work was performed. Only two tasks were genuinely complete at that point.", s="Resolved", a="Statuses corrected to reflect actual state. Recorded here because an inaccurate status board is itself an irregularity in a multi-session workflow."),
        dict(id="R-8", f="Census Data API unreachable without a key", d="The Census Bureau API requires a key, which is not obtainable in this environment, so programmatic demographic retrieval was impossible.", s="Worked around", a="Server-rendered QuickFacts pages used instead. This limits the analysis to the QuickFacts variable set; tract-level ACS tables were not reachable. Recorded so a reviewer knows the boundary."),
        dict(id="R-9", f="No network route to most official domains at build time", d="Outbound access is restricted to a small allowlist that excludes census.gov, bls.gov, dof.ca.gov, fema.gov and treasury.gov.", s="Designed around", a="The site is generated from a committed, reviewed data snapshot in which every row records its own as-of date and source URL. The published site makes no runtime API calls, so it cannot silently drift from what was verified."),
    ], [("id", "ID", "num", "text"), ("f", "Finding", "", "textn"),
        ("d", "Detail", "", "textn"), ("s", "Status", "", "text"),
        ("a", "Action taken", "", "textn")],
        "irregularities", "Repository irregularities and dispositions", ""))

    b.append("<h3>What was built</h3>")
    b.append(table([
        dict(l="data/", c="The verified data snapshot. Six modules, one per domain: demographics, employment, tenant, hazards, analysis, flags. Every row carries value, unit, geography, as-of date, source organisation, source URL and a verification status. Rows that could not be confirmed carry a null value — they are never populated with an estimate."),
        dict(l="model/projection.py", c="The projection and decision model. Deterministic, no network calls, no randomness. Normalised to R. Six strategies, three coherent scenarios, fourteen declared assumptions each with a favourability direction, plus rank-stability and worst-case analysis."),
        dict(l="build_site.py", c="The static site generator. Reads the data modules and the model, writes plain HTML into docs/. Enforces the rule that an unverified row renders blank rather than a value."),
        dict(l="site/", c="The stylesheet and client-side behaviour. Plain CSS and plain JavaScript, no framework, no CDN, no external requests."),
        dict(l="tools/check_links.py", c="Extracts every external URL from the generated site and validates it. Reports malformed URLs and any non-official domain appearing in a verified column."),
        dict(l="tools/pii_scan.py", c="Scans every generated file and data module for personal identifiers. Fails the build if any are found. This is the mechanical enforcement of the privacy directive."),
        dict(l="docs/", c="The published site — twenty-three pages served by GitHub Pages with no build step, so deployment cannot fail because of a toolchain."),
        dict(l="COORDINATION.md", c="The shared task board, session registry, file-ownership map and change log."),
        dict(l="REPO_REVIEW.md", c="The repository audit, recorded as a deliverable in its own right."),
        dict(l="EXECUTIVE_SUMMARY.md · VERIFY.md", c="Repository-level summaries mirroring the site's Executive Summary and Methodology pages."),
    ], [("l", "Path", "", "text"), ("c", "Purpose", "", "textn")],
        "built", "Repository structure created by this work", ""))
    return "".join(b)


# ==========================================================================
# MAIN
# ==========================================================================
PAGES = [
    ("index.html", "Dashboard", p_index),
    ("executive-summary.html", "Executive Summary", p_exec_summary),
    ("methodology.html", "Methodology & Verification", p_methodology),
    ("privacy.html", "Privacy & Anonymisation", p_privacy),
    ("property-profile.html", "Property Profile & Inputs", p_property_profile),
    ("geography.html", "Geography & Market Definition", p_geography),
    ("lease-economics.html", "NNN Lease Economics", p_lease_economics),
    ("tenant.html", "Tenant Credit (SEC filings)", p_tenant),
    ("tenant-closures.html", "Closure Programme", p_tenant_closures),
    ("demographics.html", "Population & Income", p_demographics),
    ("employment.html", "Employment & Wages", p_employment),
    ("projections.html", "Official Forecasts", p_projections),
    ("infrastructure.html", "Infrastructure & Schools", p_infrastructure),
    ("projection-model.html", "Projection Model", p_projection_model),
    ("valuation.html", "Valuation & Sensitivity", p_valuation),
    ("decision.html", "Decision Framework", p_decision),
    ("taxes.html", "Tax & Transaction Framework", p_taxes),
    ("risk-register.html", "Risk Register", p_risk_register),
    ("hazards.html", "Physical Hazards", p_hazards),
    ("black-swan.html", "Black Swan Register", p_black_swan),
    ("sources.html", "Source Register", p_sources),
    ("flagged-for-review.html", "Flagged for Review", p_flagged),
    ("repo-review.html", "Repository Review", p_repo_review),
]


def build():
    if os.path.isdir(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(os.path.join(DOCS, "assets"), exist_ok=True)
    shutil.copy(os.path.join(SITE, "style.css"), os.path.join(DOCS, "assets", "style.css"))
    shutil.copy(os.path.join(SITE, "app.js"), os.path.join(DOCS, "assets", "app.js"))

    # a plain-text redirect for the Pages root, in case docs/ is served oddly
    written = []
    for fname, title, fn in PAGES:
        body = fn()
        out = page(fname, title, body)
        with open(os.path.join(DOCS, fname), "w", encoding="utf-8") as fh:
            fh.write(out)
        written.append((fname, len(out)))

    # CSV exports of the verified snapshot, for the owner's own spreadsheet work
    csvdir = os.path.join(DOCS, "data")
    os.makedirs(csvdir, exist_ok=True)
    ncsv = 0
    for mod in (demographics, employment, tenant, hazards):
        for tname, rows in mod.ALL_TABLES.items():
            if not rows:
                continue
            keys = []
            for r in rows:
                for k in r:
                    if k not in keys:
                        keys.append(k)
            keys = [k for k in keys if k != "note"] + (["note"] if any("note" in r for r in rows) else [])
            path = os.path.join(csvdir, f"{mod.__name__.split('.')[-1]}__{tname}.csv")
            with open(path, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
                w.writeheader()
                for r in rows:
                    if "source_key" in r and hasattr(mod, "resolve"):
                        rr = mod.resolve(r)
                    else:
                        rr = r
                    w.writerow({k: rr.get(k, "") for k in keys})
            ncsv += 1
    return written, ncsv


if __name__ == "__main__":
    written, ncsv = build()
    total = sum(n for _, n in written)
    print(f"built {len(written)} pages, {total:,} bytes, plus {ncsv} CSV exports into docs/")
    for f, n in written:
        print(f"  {f:<28} {n:>9,} bytes")
