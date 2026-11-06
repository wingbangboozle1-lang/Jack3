"""Page body content (part 4)."""

def pages_part4(T, RISKS):
    risk_rows = []
    for r in sorted(RISKS, key=lambda x: -(x['likelihood'] * x['impact'])):
        s = r['likelihood'] * r['impact']
        cls = 'rs-low' if s <= 4 else ('rs-med' if s <= 9 else ('rs-high' if s <= 14 else 'rs-crit'))
        chip = '<span class="chip chip-bau">BUSINESS AS USUAL</span>' if r['cat'] == 'Business as usual' else '<span class="chip chip-bs">BLACK SWAN</span>'
        risk_rows.append(
            f"<tr><td>{r['id']}</td><td>{chip}</td><td>{r['risk']}</td>"
            f"<td class='num'>{r['likelihood']}</td><td class='num'>{r['impact']}</td>"
            f"<td><span class='risk-score {cls}'>{s}</span></td><td>{r['mitigant']}</td></tr>")
    risk_table = (
        '<div class="tbl-wrap"><div class="tbl-head"><h3>Risk register — all tracked risks (sorted by score)</h3>'
        '<div class="filter-box"><input data-filter="tbl-risks" placeholder="Filter risks…" aria-label="Filter risk register"></div></div>'
        '<div class="tbl-scroll"><table class="tbl sortable" id="tbl-risks"><thead><tr>'
        '<th>ID</th><th>Category</th><th>Risk</th><th>Likelihood (1–5)</th><th>Impact (1–5)</th><th>Score</th><th>Mitigant / action</th>'
        '</tr></thead><tbody>' + ''.join(risk_rows) + '</tbody>'
        '<tfoot><tr><td colspan="7">Likelihood × Impact (max 25). Scores ≤4 low · 5–9 medium · 10–14 high · 15+ critical. '
        'Categories: BAU = business-as-usual variance; BLACK SWAN = rare, severe. Register owner: property owner (internal). '
        'Review quarterly and at every 8-K/major rate move.</td></tr></tfoot></table></div></div>'
    )

    return {

    "risk-register": f"""
<h1 class="page-title">Risk Register</h1>
<p class="lede">Every decision-relevant risk, scored, mitigated, and categorized into business-as-usual (expected variance) and
black-swan (rare, severe) events. Likelihood and impact are analytical judgments; factual anchors are sourced on the linked pages.</p>
<div class="callout callout-info"><div class="c-ico">🧮</div><div><b>Scoring.</b> Score = likelihood × impact (1–25). Critical ≥ 15 · High 10–14 · Medium 5–9 · Low ≤ 4.
The register balances <b>wealth preservation</b> (mitigating R-02/R-09/R-12) against <b>opportunity</b> (rejecting an over-discounted forced sale).</div></div>
{risk_table}
<h2>Portfolio-level view</h2>
<ul class="tight">
  <li><b>Dominant exposures:</b> remaining-term value cliff (R-02, score 16) and tenant-closure risk (R-01, 15) — both mitigated by the Option C playbook (act by 2028, not at expiry).</li>
  <li><b>Tail exposures:</b> earthquake (R-09, 10) and civil unrest (R-13, 8) — capped by insurance verification + seismic confirmation; retention of risk is explicit and sized.</li>
  <li><b>Diversification is the only cure for concentration (R-14, 15):</b> if you cannot hold the concentration comfortably, the rational endpoint is a 1031 into diversified income real estate — price it with two broker opinions before deciding.</li>
</ul>
""",

    "methodology": f"""
<h1 class="page-title">Methodology, Sources & Privacy</h1>
<p class="lede">How every number on this site was produced, verified, and sourced — and the privacy rules under which the work was done.</p>

<h2>Verification protocol (line-by-line)</h2>
<ol class="action tight">
  <li>Every table row on this site is tagged <span class="badge b-verified">VERIFIED · OFFICIAL SOURCE</span> (link to a .gov / SEC / state source), <span class="badge b-industry">INDUSTRY · NON-GOVERNMENTAL</span> (brokerage/commissioned studies — never presented as official), or <span class="badge b-flagged">FLAGGED · UNVERIFIED</span> (confirmed blank or approximate).</li>
  <li>If a value could not be confirmed from an official source, the cell is left as “—” or an explicit “unverified” note and the item is reproduced on <a href="flagged-for-review.html">Flagged for Review</a> with a remediation action. No value was invented, interpolated, or “estimated” without a label.</li>
  <li>Where two official agencies publish the same fact with different methodologies (e.g., Census decennial vs DOF projections), both are shown and the discrepancy is disclosed in Flagged for Review.</li>
  <li>Derived figures (e.g., 2021→2025 HPI change +28.4%; 2025→2035 population change −1.5%) are computed from the cited official series and labeled as computed.</li>
  <li>Analysis, judgment and recommendations are labeled as such and are not “verified data.”</li>
</ol>

<h2>Official sources used</h2>
<ul class="tight">
  <li>U.S. Census Bureau — <a href="https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia,losangelescountycalifornia/PST045224" target="_blank" rel="noopener">QuickFacts: LA city &amp; LA County</a></li>
  <li>U.S. Bureau of Labor Statistics via <a href="https://fred.stlouisfed.org/" target="_blank" rel="noopener">FRED (Federal Reserve Bank of St. Louis)</a> — LOSA106URN (LA MSA unemployment); SMS06310800000000001 (LA MSA payrolls); CAUR (CA unemployment); UNRATE (US unemployment); DGS10 (10Y Treasury); ATNHPIUS06037A (FHFA HPI, LA County)</li>
  <li>California Department of Finance — <a href="https://dof.ca.gov/forecasting/demographics/" target="_blank" rel="noopener">Demographics unit</a>; P-2A County Population Projections 2020–2070 (Vintage 2026) — <a href="https://dof.ca.gov/media/docs/forecasting/Demographics/projections/P2A_County_Total.xlsx" target="_blank" rel="noopener">P2A_County_Total.xlsx</a></li>
  <li>California Department of Education — <a href="https://www.caschooldashboard.org/reports/19647330000000/2025" target="_blank" rel="noopener">California School Dashboard — LA Unified (2025)</a></li>
  <li>U.S. Securities and Exchange Commission — <a href="https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm" target="_blank" rel="noopener">Jack in the Box Inc. Form 10-K (FY2025)</a>; <a href="https://www.sec.gov/Archives/edgar/data/807882/000080788225000076/jack-20251216.htm" target="_blank" rel="noopener">Proxy FY2025</a></li>
  <li>Jack in the Box Inc. investor relations (official) — <a href="https://investors.jackinthebox.com/" target="_blank" rel="noopener">investors.jackinthebox.com</a> (Q1/Q3 FY2026 earnings; JACK on Track; Del Taco sale completion)</li>
  <li>CAL FIRE — <a href="https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire" target="_blank" rel="noopener">Eaton Fire</a>; <a href="https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire" target="_blank" rel="noopener">Palisades Fire</a></li>
  <li>FEMA — <a href="https://gis-fema.hub.arcgis.com/pages/1ee8ccb97b8d44a7ae2ae0d23e90ee26" target="_blank" rel="noopener">DR-4856-CA</a>; Flood maps: <a href="https://msc.fema.gov/" target="_blank" rel="noopener">msc.fema.gov</a></li>
  <li>U.S. Geological Survey — <a href="https://pubs.usgs.gov/publication/70029508" target="_blank" rel="noopener">Puente Hills loss estimates (Earthquake Spectra 2005)</a></li>
  <li>Southern California Association of Governments (SCAG) — 2025 Southern California Economic Update (LA28 GDP estimate $13.6–17.6B) — <a href="https://www.scag.ca.gov" target="_blank" rel="noopener">scag.ca.gov</a></li>
</ul>
<h3>Industry / non-official (labeled, never as verified)</h3>
<ul class="tight">
  <li>CBRE — <a href="https://www.cbre.com/press-releases/net-lease-investment-rises-q2-2026-extending-broad-market-momentum" target="_blank" rel="noopener">US Net-Lease Investment, Q2 2026</a> (6.9% avg net-lease cap rate)</li>
  <li>MMCG (third-party) citing CBRE H1 2026 — NET-lease QSR ~4–6% — flagged secondary source</li>
  <li>LAEDC (non-profit), study commissioned by LA28 — $20–40B output estimate — flagged</li>
  <li>Los Angeles Times, Politico, E&amp;E News, indexbox/USA Today — reporting on LA28 budget, FAIR Plan growth, activist stake — flagged, not primary</li>
</ul>

<h2>Privacy statement</h2>
<div class="callout callout-privacy"><div class="c-ico">🔒</div><div><b>No personal information appears on this site.</b> The property is described only as “a NNN-leased Jack in the Box restaurant in Central Los Angeles
(lease expiring 2030–2035).” No owner identity, address, parcel number, rent roll, loan, entity name, listing link, or tax data is published anywhere in this
repository or the live site. Internal research marked “internal” stays in this repository only as COORDINATION.md process notes — and even there, no personal data.
Any personal information encountered during research was disregarded for publication purposes.</div></div>

<h2>Disclaimers</h2>
<p class="small">This site is informational only and is <b>not legal, tax, accounting, appraisal, or investment advice</b>; it is not a broker opinion of value and not an appraisal.
Figures are as of retrieval dates shown (mostly 2026-11-06) and change. NNN lease, real-estate and tax outcomes depend on documents and counsel this analysis has not seen.
Consult a licensed CPA, attorney, real-estate broker and structural engineer before transacting. Sources are linked for your manual review — broken or moved links should be reported to the repo issue tracker.</p>
<p class="small">Repository: <a href="https://github.com/wingbangboozle1-lang/Jack3" target="_blank" rel="noopener">github.com/wingbangboozle1-lang/Jack3</a> · Coordination log: COORDINATION.md at repo root · Site generated 2026-11-06.</p>
""",

    "flagged-for-review": None,  # rendered from data JSON at build time

    "index": None,               # built in build_site.py

    }


def flagged_page(FLAGGED):
    items = []
    for i, f in enumerate(FLAGGED, 1):
        items.append(f"""<div class="card" style="margin:.6rem 0"><h3 style="margin:.1rem 0 .3rem">Flag {i}: {f['item']}</h3>
<p style="margin:.2rem 0"><b>Detail:</b> {f['detail']}</p>
<p style="margin:.2rem 0"><b>Action:</b> {f['action']}</p></div>""")
    return f"""
<h1 class="page-title">Flagged for Review</h1>
<p class="lede">Every item that could not be verified against an official source, or that needs your confirmation. <b>None of these block the recommendation — they are called out honestly instead of guessed.</b> Review at your leisure; each carries a concrete remediation step.</p>
<div class="callout callout-warn"><div class="c-ico">🚩</div><div><b>{len(FLAGGED)} items flagged.</b> Until resolved, treat the flagged values as <b>unknown</b>, not as zero, not as estimated. The recommendation (Option C) is robust to all of them — it is driven by structure (term decay, escalators, concentration), not by any single flagged figure.</div></div>
{''.join(items)}
"""
