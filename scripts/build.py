"""Dependency-free static, privacy-safe public dashboard builder."""
import json
import html
from pathlib import Path

D = json.loads(Path("data/evidence.json").read_text(encoding="utf-8"))
e = html.escape
nav = [("index", "Executive summary")] + [(p["id"], p["title"]) for p in D["pages"]] + [("sources", "Sources & methodology")]


def shell(page_id: str, title: str, content: str) -> str:
    reviewed = D.get("reviewed", "2026-11-08")
    nav_html = "".join(
        f'<a {"aria-current=page" if key == page_id else ""} href="{key}.html">'
        f'<span>{str(i + 1).zfill(2)}</span>{e(label)}</a>'
        for i, (key, label) in enumerate(nav)
    )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="description" content="Privacy-safe, evidence-linked Los Angeles net lease property research. Unknown financial values are withheld.">'
        f'<title>{e(title)} · Jack / Property research</title>'
        '<link rel="stylesheet" href="assets/style.css"></head>'
        '<body><a class="skip" href="#main">Skip to content</a>'
        f'<aside><a class="brand" href="index.html"><span class="mark">J.</span> JACK<span class="brand-sub">PROPERTY INTELLIGENCE</span></a>'
        f'<div class="nav-label">RESEARCH WORKSPACE</div><nav>{nav_html}</nav>'
        '<div class="privacy"><span>◈</span><b>Privacy by design</b><p>Asset A · anonymized<br>No owner or parcel identifiers</p></div></aside>'
        f'<div class="workspace"><header><span>RESEARCH / LOS ANGELES</span><span class="stamp">● &nbsp; Evidence snapshot · {e(reviewed)}</span></header>'
        '<main id="main"><section class="callout"><b>Evidence boundary.</b> Regional data, SEC filings, statutory tax cliffs and algebraic break-even identities are verified as of '
        f'{e(reviewed)}. Private lease, tax-basis and parcel metrics remain blank pending owner records; no unverified probability weights or guessed cap rates are published. <a href="review.html">Flagged for Review</a>.</section>'
        f'{content}</main>'
        '<footer>Independent decision-support research. Not an appraisal, legal opinion or personalized financial advice.<br>'
        'Static evidence snapshot · No tracking, forms, third-party assets or private documents · <a href="sources.html">Methodology & limitations</a></footer>'
        '</div></body></html>'
    )


def render_table(columns: list[str], rows: list[dict], caption: str) -> str:
    heads = columns + ["Evidence", "Official source"]
    out = (
        '<div class="table-wrap"><table>'
        f'<caption>{e(caption)}</caption>'
        '<thead><tr>' + "".join(f'<th scope="col">{e(c)}</th>' for c in heads) + '</tr></thead><tbody>'
    )
    for r in rows:
        s = D["sources"][r["source"]]
        status = r["status"]
        cls = "verified" if status == "Verified" else "analysis" if status == "Analysis" else "unknown"
        cells_html = "".join(
            "<td" + (' class="empty" aria-label="Unverified value; intentionally blank"' if c == "" else "") + ">" + e(c) + "</td>"
            for c in r["cells"]
        )
        out += (
            f"<tr>{cells_html}"
            f'<td><span class="badge {cls}">{e(status)}</span></td>'
            f'<td><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["label"])} ↗</a></td></tr>'
        )
    return out + "</tbody></table></div>"


for p in D["pages"]:
    intro = (
        f'<div class="eyebrow">{e(p["kicker"])}</div>'
        f'<h1>{e(p["title"])}</h1>'
        f'<p class="lede">{e(p["description"])}</p>'
        '<div class="legend">'
        '<span class="badge verified">Verified</span> Source-matched observation '
        '<span class="badge analysis">Analysis</span> Conditional / algebraic identity '
        '<span class="badge unknown">Unverified</span> Missing private evidence'
        '</div>'
    )
    tables_html = render_table(p["columns"], p["rows"], p.get("caption", f"{p['title']} · evidence register"))
    for extra in p.get("extra_tables", []):
        tables_html += render_table(extra["columns"], extra["rows"], extra["caption"])
    Path(p["id"] + ".html").write_text(shell(p["id"], p["title"], intro + tables_html), encoding="utf-8")


index_content = '''<div class="eyebrow">ASSET A / LOS ANGELES QSR NET-LEASE BRIEF</div>
<h1>Audit the lease.<br><span>Price the 2029–2035 cliff early.</span></h1>
<p class="lede">Primary-source analysis of a Los Angeles Jack in the Box single-tenant property (reported 2030–2035 expiration). Separates directly verified SEC, Census, BLS, DOF, Treasury, tax and hazard facts from unverified parcel inputs—without guessed probabilities or fabricated cap rates.</p>
<div class="hero-note">
  <span class="badge analysis">RECOMMENDED POSTURE · TWO-TRACK AUDIT</span>
  <h2>Test an early creditworthy extension in parallel with pre-2029 §1031 price discovery.</h2>
  <p>Do not wait passively until 2029–2030. The tenant carries $432.25M of Series 2019-1 debt maturing in August 2029 amid −1.1% Q3 FY26 comps, $11.0M YTD franchisee payment deferrals, and a 150–200 unit closure plan tied to franchise expirations. Meanwhile, Measure ULA imposes harsh price cliffs above $5.40M (4.56% total) and $10.90M (6.06% total). Pull the executed lease, legal obligor, store sales and ZIMAS zoning first—then compare an extension bid directly against §1031 sale proceeds.</p>
  <a class="button" href="decisions.html">Inspect decision pathways &amp; gates <span>→</span></a>
  <a class="quiet" href="model.html">View algebraic break-even thresholds ↗</a>
</div>
<div class="section-heading"><h2>Verified regional &amp; tenant dashboard</h2><span>As of 08 Nov 2026 · official sources only</span></div>
<div class="cards">
  <article>
    <div class="eyebrow">DEMOGRAPHICS / DOF P-2A</div>
    <strong>−0.8% / 9.71M</strong>
    <p>LA City V2025 (−0.8% to 3.869M) &amp; CA DOF P-2A County 2035 projection (9.709M, −1.05% vs 2026); SCAG 2050 draft also shifts down.</p>
    <a href="economy.html">Census &amp; DOF projections →</a>
  </article>
  <article>
    <div class="eyebrow">JOBS &amp; INFLATION / BLS</div>
    <strong>+0.5% / −121.6k LF</strong>
    <p>Sep 2026 Metro payrolls 6,282.1k (+0.5% YoY), while Metro labor force shrank 121.6k and Energy CPI surged +20.3% YoY.</p>
    <a href="economy.html">Sep 2026 BLS tables →</a>
  </article>
  <article>
    <div class="eyebrow">TENANT &amp; 2029 WALL / SEC</div>
    <strong>−1.1% / $432.3M</strong>
    <p>JIB Q3 FY26 system SSS −1.1%; $1,874k FY25 franchise AUV; 1,585 master-leased units; $500M 7.624% refi &amp; Aug 2029 ARD wall.</p>
    <a href="tenant.html">10-K, 10-Q &amp; lease structure →</a>
  </article>
  <article>
    <div class="eyebrow">RATES &amp; QSR WAGE / UST &amp; DIR</div>
    <strong>4.86% / $20.00</strong>
    <p>Nov 6, 2026 10Y Treasury 4.86% (FOMC 3.75%–4.00% w/ 2 hike dissents); AB 1228 $20/hr QSR floor ($18.42 LA; $17.40 CA 2027).</p>
    <a href="tenant.html">Rates &amp; operating mandates →</a>
  </article>
  <article>
    <div class="eyebrow">STATUTORY TAX CLIFFS / LA &amp; BOE</div>
    <strong>4.56% / 35 Yrs</strong>
    <p>Post-7/1/2026 City+County transfer tax jumps from 0.56% to 4.56% above $5.40M ($5.40M–$5.63M dead zone); Prop 13 35-yr lease rule.</p>
    <a href="model.html">Measure ULA cliff table →</a>
  </article>
  <article>
    <div class="eyebrow">HAZARDS &amp; CATALYSTS / USGS &amp; LA</div>
    <strong>60% M6.7 / 28,526</strong>
    <p>30-yr LA quake odds, $5.2B–$10.1B Jan 2025 fires &amp; 2028 FAIR Plan sunset vs. Metro D Line Sec. 1 (May 2026) &amp; 242 CHIP infill projects.</p>
    <a href="place.html">Hazards &amp; corridor catalysts →</a>
  </article>
</div>
<section class="split">
  <div>
    <div class="eyebrow">WEALTH PRESERVATION VS. GROWTH</div>
    <h2>Why timing before 2029 matters—and when holding still wins.</h2>
    <p><b>Wealth-preservation floor:</b> For a low-basis owner prioritizing capital safety, a <b>pre-expiry IRC §1031 exchange</b> in 2027–2029 (or an early extension followed by §1031) avoids facing a dark box, CapEx, or franchisee non-renewal into JIB’s August 2029 $432.25M debt wall—provided gross pricing stays clear of City of LA ULA dead zones ($5.40M–$5.63M and $10.90M–$11.07M).</p>
    <p><b>When holding or repositioning wins:</b> If the executed lease runs to 2035 with a corporate master guaranty, store sales clear JIB’s $1,874k brand AUV, and ZIMAS shows C2/MIIP/CHIP or Metro D Line transit density, residual land value can justify holding—so long as an extension does not cross Prop 13’s 35-year reassessment line.</p>
  </div>
  <div class="callout">
    <h3>Five unverified private gates that control the call</h3>
    <p>No site-specific valuation or categorical sell/hold verdict is fabricated without these owner documents:</p>
    <p><b>1. Executed lease &amp; options:</b> exact expiry (2030 vs. 2035), notice dates, NNN scope, and remaining years vs. 35-year Prop 13 rule.<br>
       <b>2. Legal obligor &amp; unit P&amp;L:</b> JIB Inc. master lease vs. single-purpose franchisee LLC, store sales, and rent coverage.<br>
       <b>3. Jurisdiction &amp; zoning:</b> City of LA vs. adjacent city, Measure ULA applicability, Ord. 183893 seismic status, and CHIP/transit tier.<br>
       <b>4. Broker pricing &amp; §1031 basis:</b> unlevered BOV relative to 4.86% UST spreads, adjusted basis, and §1250 recapture.<br>
       <b>5. Parcel hazard &amp; insurance checks:</b> CGS EQ Zapp, FEMA FIRM, FHSZ map, and 2028 commercial coverage bindability.</p>
    <a href="review.html">Inspect all flagged gaps &amp; resolved checks →</a>
  </div>
</section>
<div class="section-heading"><h2>Explore the workspace</h2><span>Every table row carries its verified source</span></div>
<div class="route-grid">
  <a href="economy.html"><b>01 / Area fundamentals</b><p>Census V2025, Sep 2026 BLS jobs &amp; labor-force drop, Treasury yields, CA DOF P-2A vs. SCAG projections.</p>Read regional data →</a>
  <a href="tenant.html"><b>02 / Tenant &amp; lease</b><p>SEC 10-K/10-Q credit, $432.3M 2029 debt wall, $1,874k JIB AUV, AB 1228, Measure ULA &amp; Prop 13 35-yr rule.</p>Review credit &amp; taxes →</a>
  <a href="risk.html"><b>03 / Risk &amp; resilience</b><p>USGS UCERF3, Ord. 183893, Jan 2025 Palisades/Eaton fires, 2028 FAIR Plan sunset &amp; tail risks.</p>Inspect downside →</a>
  <a href="place.html"><b>04 / Neighborhood &amp; land</b><p>LAUSD 2025–26 scale &amp; Dashboard, Metro D Line Section 1 opening, DTLA 2040 &amp; CHIP Year-1 infill data.</p>Check land catalysts →</a>
  <a href="model.html"><b>06 / Projection framework</b><p>Official 2026–2035 horizons, Measure ULA dead-zone arithmetic &amp; unweighted 1.00 R break-even hurdles.</p>See quantitative tables →</a>
  <a href="review.html"><b>07 / Flagged for Review</b><p>Resolved F-04 / F-17 / IR-10 fixes, withheld companion rankings, and unverified private-document gates.</p>Audit limitations →</a>
</div>'''

Path("index.html").write_text(shell("index", "Executive summary", index_content), encoding="utf-8")

src = {
    "title": "Official source register",
    "columns": ["Publisher / document", "Type", "Reviewed", "Use and limits"],
    "rows": [
        dict(
            cells=[s["label"], s["type"], s["checked"], "Directly fetched official/issuer primary source; regional or issuer context, not a subject-parcel appraisal."],
            status="Verified",
            source=k,
        )
        for k, s in D["sources"].items()
    ],
}

sources_content = '''<div class="eyebrow">08 / AUDIT TRAIL</div>
<h1>Sources &amp; methodology</h1>
<p class="lede">Every numerical fact on this site traces directly to an inspected primary government, municipal, court/tax, or SEC/issuer filing reviewed on 8 November 2026 (UTC). Unverified private property facts remain blank.</p>
<section class="callout">
  <h2>Verification &amp; evidence discipline</h2>
  <p><b>Primary-source rule:</b> All demographic, wage, assessment-roll, transfer-tax, property-tax, yield-curve, school, planning, transit, and catastrophe metrics are read directly from their issuing U.S. federal, State of California, Los Angeles County, or City of Los Angeles agencies (including direct binary parsing of CA Dept. of Finance <code>P2A_County_Total.xlsx</code> and DIR News Release <code>2026-66</code> resolving prior item F-17). Corporate credit and real-estate footprint figures come from Jack in the Box Inc.’s FY2025 Form 10-K, Q3 FY2026 Form 10-Q, and official investor releases, labeled separately as <i>Issuer</i> records.</p>
  <p><b>Zero fabricated probabilities or cap rates:</b> Companion-layer rankings that relied on unverified scenario weights (20/50/20/10%), assumed cap rates, or assumed personal tax brackets remain excluded from GitHub Pages. Instead, <code>model/area_projection.py</code> computes pure statutory Measure ULA arithmetic and exact algebraic <code>1.00 R</code> break-even thresholds anchored to the November 6, 2026 10-Year U.S. Treasury yield (4.86%).</p>
  <p><b>Vintage &amp; geographic boundaries:</b> QuickFacts mixes V2025 population estimates with 2020–2024 ACS 5-year estimates and 2022–2023 economic surveys; BLS September 2026 figures are preliminary and not seasonally adjusted; LA County Anniversary Fact Sheet wildfire counts (6,837 / 9,414) and CAL FIRE 2026 updated incident counts (6,845 / 9,419) are both preserved transparently. Regional averages never override parcel-level underwriting.</p>
  <h3>Privacy, reproducibility &amp; Pages curation</h3>
  <p>No owner names, parcel IDs, APNs, street addresses, account details, third-party analytics, or external scripts are collected or published. <code>data/evidence.json</code> and <code>scripts/build.py</code> deterministically build these nine static HTML pages; <code>scripts/validate.py</code>, <code>scripts/stage_pages.py</code>, <code>tools/pii_scan.py</code>, and Jekyll CI verify byte-identical curation and official source links on every table row.</p>
</section>''' + render_table(src["columns"], src["rows"], "Official primary source register (42 verified references)")

Path("sources.html").write_text(shell("sources", "Sources & methodology", sources_content), encoding="utf-8")
