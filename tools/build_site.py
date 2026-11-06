#!/usr/bin/env python3
"""Build the Jack3 static site into docs/ from data/site_data.json + content modules."""
import json, html, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from content_part1 import pages_part1
from content_part2 import pages_part2
from content_part3 import pages_part3
from content_part4 import pages_part4, flagged_page

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
DATA = json.load(open(ROOT / 'data' / 'site_data.json'))

# ---------------- badges & tables ----------------
BADGE = {
    'verified': '<span class="badge b-verified"><span class="dot"></span>VERIFIED · OFFICIAL SOURCE</span>',
    'industry': '<span class="badge b-industry"><span class="dot"></span>INDUSTRY · NON-GOVERNMENTAL</span>',
    'flagged':  '<span class="badge b-flagged"><span class="dot"></span>FLAGGED · UNVERIFIED</span>',
}

def esc(s): return html.escape(str(s), quote=True)

def render_table(tid):
    t = DATA['tables'][tid]
    cols = t['columns']
    tid_attr = f'tbl-{tid}'
    out = ['<div class="tbl-wrap"><div class="tbl-head">',
           f'<h3>{esc(t["title"])}</h3>',
           f'<div class="filter-box"><input data-filter="{tid_attr}" placeholder="Filter rows…" aria-label="Filter table"></div>',
           '</div><div class="tbl-scroll">',
           f'<table class="tbl sortable" id="{tid_attr}"><thead><tr>']
    for c in cols:
        out.append(f'<th>{esc(c)}</th>')
    out.append('<th>Source</th><th>Verification</th></tr></thead><tbody>')
    for row in t['rows']:
        out.append('<tr>')
        for cell in row:
            out.append(f'<td>{cell}</td>')   # cells may contain <a> links (escaped at authoring time)
        out.append(f'<td><a class="src-link" href="{esc(t["url"])}" target="_blank" rel="noopener noreferrer">{esc(t["source"])} ↗</a></td>')
        out.append(f'<td>{BADGE[t["status"]]}</td></tr>')
    out.append('</tbody>')
    out.append(f'<tfoot><tr><td colspan="{len(cols)+2}">Source: <a class="src-link" href="{esc(t["url"])}" target="_blank" rel="noopener noreferrer">{esc(t["source"])}</a> · Retrieved 2026-11-06 · <a href="methodology.html">Methodology &amp; verification protocol</a></td></tr></tfoot>')
    out.append('</table></div></div>')
    return ''.join(out)

def T(tid):
    return render_table(tid)

# ---------------- nav ----------------
NAV = [
    ("Home", [("index", "Dashboard", "🏠")]),
    ("Overview", [("executive-summary", "Executive Summary", "📋"),
                  ("decision-analysis", "Decision Analysis", "⚖️"),
                  ("projection-studio", "Projection Studio", "📈")]),
    ("Market & Area", [("demographics", "Demographics & Geography", "🗺️"),
                       ("economy-jobs", "Economy & Jobs", "💼"),
                       ("population-projections", "Population Projections", "📉"),
                       ("income-housing", "Income, Poverty & Housing", "🏘️"),
                       ("schools-education", "Schools & Education", "🎓"),
                       ("real-estate-market", "Real Estate Market", "🏢"),
                       ("growth-catalysts", "Growth Catalysts", "🚀")]),
    ("Asset & Tenant", [("tenant-jackinthebox", "Tenant: Jack in the Box", "🍔"),
                        ("property-operations", "Asset & NNN Operations", "🔑")]),
    ("Risk", [("hazards-black-swans", "Hazards & Black Swans", "🌋"),
              ("risk-register", "Risk Register", "🛡️")]),
    ("Reference", [("methodology", "Methodology & Privacy", "📚"),
                   ("flagged-for-review", "Flagged for Review", "🚩")]),
]
ALL_PAGES = [slug for _, items in NAV for slug, _, _ in items] + ['404']

def nav_html(active):
    out = ['<nav class="nav" aria-label="Site navigation">']
    for group, items in NAV:
        out.append(f'<div class="nav-group">{esc(group)}</div>')
        for slug, label, icon in items:
            cls = ' class="active" aria-current="page"' if slug == active else ''
            tag = '<span class="tag">REVIEW</span>' if slug == 'flagged-for-review' else ''
            out.append(f'<a href="{slug}.html"{cls}><span aria-hidden="true">{icon}</span><span>{esc(label)}</span>{tag}</a>')
    out.append('</nav>')
    return ''.join(out)

def shell(page_id, title, body, crumb):
    flagged_n = len(DATA['flagged'])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Jack3 — Central LA NNN Jack in the Box</title>
<meta name="description" content="Anonymized analytical dashboard for a single-tenant NNN Jack in the Box in Central Los Angeles: sell vs renew decision, official-source verified data, risk register and projections.">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div class="layout">
<aside class="sidebar" id="sidebar">
  <div class="brand">
    <div class="brand-mark" aria-hidden="true">📦</div>
    <div><h1>Jack3 — NNN Decision Desk</h1><small>Central LA · Sell vs Renew</small></div>
  </div>
  {nav_html(page_id)}
</aside>
<div class="main">
  <div class="topbar">
    <button class="hamburger" id="hamburger" aria-label="Toggle navigation" aria-expanded="false" aria-controls="sidebar">☰</button>
    <div class="crumb">Jack3 / <b>{esc(crumb)}</b></div>
    <div class="top-right">
      <span class="pill pill-privacy">🔒 Anonymized — no PII</span>
      <span class="pill pill-date">Data as of 2026-11-06</span>
    </div>
  </div>
  <main class="content">
{body}
  </main>
  <footer class="footer">
    <b>Jack3 Decision Desk</b> · Anonymized analysis for a Central Los Angeles NNN Jack in the Box (lease expiry 2030–2035).
    Not legal, tax, or investment advice. Every figure carries a source link on-page or is explicitly flagged.
    <a href="methodology.html">Methodology &amp; sources</a> · <a href="flagged-for-review.html">Flagged for review ({flagged_n})</a> ·
    <a href="https://github.com/wingbangboozle1-lang/Jack3" target="_blank" rel="noopener noreferrer">GitHub repo</a> · Generated 2026-11-06.
  </footer>
</div>
</div>
<script src="assets/app.js"></script>
</body>
</html>"""

# ---------------- decision matrix embed ----------------
def decision_matrix_block():
    dm = DATA['decision_matrix']
    weights = [c['weight'] for c in dm['criteria']]
    rows = []
    totals = [0.0] * len(dm['options'])
    for i, c in enumerate(dm['criteria']):
        cells = []
        for j, o in enumerate(dm['options']):
            s = o['scores'][i]
            totals[j] += s * c['weight']
            bar = int(round(s / 5 * 120))
            cells.append(f'<td><div class="score-bar"><div class="bar-track"><div class="bar" style="width:{bar}px"></div></div><span>{s}</span></div></td>')
        rows.append(f'<tr><td>{esc(c["name"])} <span class="small">({int(c["weight"]*100)}%)</span></td>' + ''.join(cells) + '</tr>')
    tot_cells = ''.join(f'<td class="num"><b>{t:.2f}</b> / 5.00</td>' for t in totals)
    return ''.join(rows), tot_cells, totals

# ---------------- home page ----------------
def index_page():
    kpis = [
        ("LA County population (2025)", "9,694,934", "DOF proj. 2035: 9.71M", "census.gov / dof.ca.gov"),
        ("LA city population (2025)", "3,869,089", "−0.8% vs 2020", "census.gov"),
        ("LA MSA unemployment", "4.4%", "Sep 2026 (NSA) · US 4.2% · CA 5.1%", "BLS via FRED"),
        ("LA MSA payrolls", "6.30M", "Sep 2026 (SA) · flat", "BLS via FRED"),
        ("10-Year Treasury", "4.90%", "2026-11-04", "FRED DGS10"),
        ("LA County FHFA HPI", "403.74", "+28.4% since 2021 (2000=100)", "FHFA via FRED"),
        ("Median HH income (city)", "$81,939", "vs county $90,112 (2024$)", "census.gov"),
        ("LAUSD graduation rate", "86.5%", "2025 · chronic absenteeism 21.9%", "CA School Dashboard"),
        ("JACK system SSS", "−1.1%", "Q3 FY2026 (Jul 5, 2026)", "SEC/IR"),
        ("JACK restaurants", "2,115", "Q3 FY2026 · 93% franchised", "SEC/IR"),
        ("Net-lease cap rate", "6.9%", "Q2 2026 · retail avg (industry)", "CBRE (industry)"),
        ("Eaton + Palisades fires", "16,264", "structures destroyed, Jan 2025", "CAL FIRE (9,419 + 6,845)"),
    ]
    kpi_html = ''.join(
        f'<div class="kpi"><div class="k-label">{esc(a)}</div><div class="k-value">{esc(b)}</div>'
        f'<div class="k-sub">{esc(c)}</div><div class="k-src">Source: {esc(d)}</div></div>'
        for a, b, c, d in kpis)

    cats = [
        ("executive-summary.html", "📋", "Executive Summary", "The whole decision in one page: situation, data, options, recommendation."),
        ("decision-analysis.html", "⚖️", "Decision Analysis", "Weighted matrix: sell vs renew vs hybrid. Triggers for action."),
        ("projection-studio.html", "📈", "Projection Studio", "Interactive PV model: renew-and-hold vs sell, with sensitivity grid."),
        ("demographics.html", "🗺️", "Demographics & Geography", "Density 8,304/sq mi; 47.2% Hispanic/Latino; foreign-born 35.7%."),
        ("economy-jobs.html", "💼", "Economy & Jobs", "LA MSA unemployment 4.4%; payrolls 6.30M; $81.4B city retail sales."),
        ("population-projections.html", "📉", "Population Projections", "DOF P-2A: 9.73M (2030) → 9.71M (2035) → 8.96M (2060)."),
        ("income-housing.html", "🏘️", "Income, Poverty & Housing", "$81,939 median HH income; 16.5% poverty; rent $1,933."),
        ("schools-education.html", "🎓", "Schools & Education", "LAUSD graduation 86.5% (2025); absenteeism 21.9%, improving."),
        ("real-estate-market.html", "🏢", "Real Estate Market", "FHFA HPI +28.4% since 2021; net-lease cap 6.9% (industry)."),
        ("growth-catalysts.html", "🚀", "Growth Catalysts", "2028 Olympics ($13.6–17.6B SCAG); transit; infill housing 22,250 permits."),
        ("tenant-jackinthebox.html", "🍔", "Tenant: Jack in the Box", "FY2025 rev $1.47B (−6.7%); SSS −1.1%; de-leveraging to 4–5x ND/EBITDA."),
        ("property-operations.html", "🔑", "Asset & NNN Operations", "NNN mechanics, compliance checklist, landlord calendar."),
        ("hazards-black-swans.html", "🌋", "Hazards & Black Swans", "Puente Hills $82–252B loss scenario; Jan 2025 fires; insurance repricing."),
        ("risk-register.html", "🛡️", "Risk Register", "14 scored risks: BAU vs black swan, mitigants, owners."),
        ("methodology.html", "📚", "Methodology & Privacy", "Line-by-line verification protocol; official sources; privacy pledge."),
        ("flagged-for-review.html", "🚩", f"Flagged for Review", f"{len(DATA['flagged'])} items not verified vs official sources — each with an action."),
    ]
    cat_html = ''.join(f'<a class="cat-card" href="{h}"><div class="cat-ico" aria-hidden="true">{i}</div><h3>{esc(t)}</h3><p>{esc(d)}</p></a>' for h, i, t, d in cats)

    return f"""
<h1 class="page-title">The Central LA Jack in the Box — Sell or Renew?</h1>
<p class="lede">A privacy-first, official-source analytical desk for one question: keep the NNN lease through its
2030–2035 expiry, or sell beforehand. Everything below is sourced — or honestly flagged. No owner data, no address, no invention.</p>

<div class="callout callout-rec"><div class="c-ico">✅</div><div><b>Recommendation (detail: <a href="executive-summary.html">Executive Summary</a> · <a href="decision-analysis.html">Decision Analysis</a>):</b>
Negotiate renewal/extension <b>now</b> with a +10–20% rent reset and full NNN re-affirmation (Option C — Hybrid), keep the asset market-ready, and sell only if a hard trigger fires
(failed renewal, credit inflection, cap-rate compression, or a ≥ +15% unsolicited bid). Do not let the term decay silently, and do not fire-sale into a 4.90% 10-year world.</div></div>

<h2>Key indicators at a glance</h2>
<div class="grid kpis">{kpi_html}</div>

<h2>Explore by category</h2>
<div class="grid cat-grid">{cat_html}</div>

<h2>How to read this site</h2>
<p class="small">Status badges — <span class="badge b-verified"><span class="dot"></span>VERIFIED</span> = official source (.gov / SEC / state) linked on the row;
<span class="badge b-industry"><span class="dot"></span>INDUSTRY</span> = brokerage/commissioned study, never presented as fact of government;
<span class="badge b-flagged"><span class="dot"></span>FLAGGED</span> = could not verify — value withheld, remediation listed on <a href="flagged-for-review.html">Flagged for Review</a>.
Tables are filterable (top-right of each table) and sortable (click any column header). Nothing here is appraisal, legal or tax advice.</p>
"""

# ---------------- build all pages ----------------
def build():
    bodies = {}
    bodies.update(pages_part1(T))
    bodies.update(pages_part2(T))
    bodies.update(pages_part3(T))
    bodies.update(pages_part4(T, DATA['risks']))
    bodies['flagged-for-review'] = flagged_page(DATA['flagged'])
    bodies['index'] = index_page()

    # decision matrix table injection
    dm_rows, dm_totals, _totals = decision_matrix_block()
    bodies['decision-analysis'] = bodies['decision-analysis'].replace(
        '<tbody></tbody>\n<tfoot><tr id="dm-total"><td>Weighted total (max 5.00)</td><td></td><td></td><td></td></tr></tfoot>',
        f'<tbody>{dm_rows}</tbody>\n<tfoot><tr id="dm-total"><td><b>Weighted total (max 5.00)</b></td>{dm_totals}</tr></tfoot>'
    )

    titles = {
        'index': 'Dashboard', 'executive-summary': 'Executive Summary', 'decision-analysis': 'Decision Analysis',
        'projection-studio': 'Projection Studio', 'demographics': 'Demographics & Geography', 'economy-jobs': 'Economy & Jobs',
        'population-projections': 'Population Projections', 'income-housing': 'Income, Poverty & Housing',
        'schools-education': 'Schools & Education', 'real-estate-market': 'Real Estate Market',
        'growth-catalysts': 'Growth Catalysts', 'tenant-jackinthebox': 'Tenant: Jack in the Box',
        'property-operations': 'Asset & NNN Operations', 'hazards-black-swans': 'Hazards & Black Swans',
        'risk-register': 'Risk Register', 'methodology': 'Methodology & Privacy', 'flagged-for-review': 'Flagged for Review',
        '404': 'Page not found',
    }
    crumbs = titles

    DOCS.mkdir(exist_ok=True)
    for slug in ALL_PAGES:
        if slug == '404':
            body = '<h1 class="page-title">404 — page not found</h1><p class="lede">That page does not exist. Return to the <a href="index.html">dashboard</a>.</p>'
        else:
            body = bodies[slug]
        (DOCS / f'{slug}.html').write_text(shell(slug, titles[slug], body, crumbs[slug]), encoding='utf-8')

    # decision matrix live data (used to keep static markup consistent; harmless if unused)
    (DOCS / 'assets' / 'decision_matrix.json').write_text(json.dumps(DATA['decision_matrix'], indent=2))
    print(f'Built {len(ALL_PAGES)} pages into {DOCS}')

if __name__ == '__main__':
    build()
