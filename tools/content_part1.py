"""Page body content (part 1). Returns {page_id: html_body}. Imported by build_site.py."""

def pages_part1(T):
    """T = render_table callable(tid) -> html."""
    return {

    "executive-summary": f"""
<h1 class="page-title">Executive Summary</h1>
<p class="lede">Decision brief: whether to <b>sell a single-tenant, NNN-leased Jack in the Box restaurant
in Central Los Angeles before its lease expires (2030–2035)</b>, or <b>renew/extend the lease</b> — assessed against
current economic activity, verified official data, and a structured risk register. Property and owner are
deliberately anonymized throughout this site.</p>

<div class="callout callout-privacy"><div class="c-ico">🔒</div><div><b>Privacy first.</b> No owner name, no street address, no parcel
number, no listing references, and no personal financial data appear anywhere on this site or in this repository. All research was
conducted on public, official sources only. See the <a href="methodology.html">Methodology & Privacy</a> page.</div></div>

<h2>1&nbsp;·&nbsp;Situation</h2>
<div class="grid kpis">
  <div class="kpi"><div class="k-label">Asset</div><div class="k-value" style="font-size:1.02rem">NNN QSR</div><div class="k-sub">Jack in the Box, Central LA</div></div>
  <div class="kpi"><div class="k-label">Lease</div><div class="k-value" style="font-size:1.02rem">Expires 2030–2035</div><div class="k-sub">Tenant pays taxes, insurance, maintenance</div></div>
  <div class="kpi"><div class="k-label">Tenant</div><div class="k-value" style="font-size:1.02rem">NASDAQ: JACK</div><div class="k-sub">~2,115 restaurants (Q3 FY2026)</div></div>
  <div class="kpi"><div class="k-label">10-Year Treasury</div><div class="k-value">4.90%</div><div class="k-sub">2026-11-04 (FRED DGS10)</div></div>
</div>
<p>This is a single-tenant, single-market, triple-net retail asset: passive income today, but with material
<b>remaining-term, tenant-credit and interest-rate</b> exposure. The lease’s 2030–2035 expiry window is the pivotal fact:
NNN assets lose value as the term burns down, and the window between now and expiry is when leverage over
renewal terms is greatest.</p>

<h2>2&nbsp;·&nbsp;What the official data says</h2>
<ul class="tight">
  <li><b>Population is flat-to-declining.</b> California DOF projects LA County falling from 9.85M (2025) to 9.71M (2035), 9.64M (2040) and 8.96M (2060) — see <a href="population-projections.html">Population Projections</a>.</li>
  <li><b>Density is extreme.</b> LA city density is 8,304 people/sq mi with 47.2% Hispanic/Latino population and a very large food-away-from-home market: <b>$17.4B restaurant &amp; food-service sales in the city (2022)</b> (<a href="economy-jobs.html">Economy &amp; Jobs</a>).</li>
  <li><b>Labor market is soft but not in recession.</b> LA MSA unemployment 4.4% (Sep 2026) vs US 4.2% and California 5.1%; payrolls 6.30M, flat (<a href="economy-jobs.html">Economy &amp; Jobs</a>).</li>
  <li><b>Income is mid-tier for coastal CA.</b> Median household income $81,939 (city) / $90,112 (county); 16.5% city poverty (<a href="income-housing.html">Income &amp; Housing</a>).</li>
  <li><b>Schools improving.</b> LAUSD graduation rate 86.5% (2025), chronic absenteeism down to 21.9% from 39.8% in 2022 — still elevated (<a href="schools-education.html">Schools &amp; Education</a>).</li>
  <li><b>Housing costs are severe.</b> Median gross rent $1,933/mo; median owner value $921,200 (city) (<a href="income-housing.html">Income &amp; Housing</a>) — wages vs housing mismatch is the area’s structural affordability problem.</li>
  <li><b>Tenant is stressed but de-leveraging.</b> JACK FY2025 revenue $1.465B (−6.7%); system SSS −4.2% in FY2025 and −1.1% in Q3 FY2026; stock ~72% below FY2020; Del Taco sold (Dec 2025, ~$119M) and proceeds applied to debt; $110M note prepayment and $500M refinance completed; targeting Net Debt/EBITDA 4–5x; 150–200 store closure program underway (<a href="tenant-jackinthebox.html">Tenant &amp; Brand</a>).</li>
  <li><b>Hazards are real.</b> Jan 2025 fires destroyed ~16,000 structures region-wide; Puente Hills blind-thrust full-rupture scenario: $82–252B losses (<a href="hazards-black-swans.html">Hazards &amp; Black Swans</a>).</li>
  <li><b>2028 Olympics</b> are a once-in-a-generation demand catalyst inside the holding window (SCAG estimate: $13.6–17.6B regional GDP add, 2024–2029) — <a href="growth-catalysts.html">Growth Catalysts</a>.</li>
</ul>

<h2>3&nbsp;·&nbsp;Options considered</h2>
<div class="card">
  <p style="margin-top:0"><b>Option A — Sell before expiry (2026–2028).</b> Capture remaining-term premium now; crystallize gain; redeploy (e.g., 1031 exchange). Cons: sells the 2028–2035 renewal upside; locks today’s cap-rate environment (net-lease avg 6.9% retail; QSR tighter, ~5–6% industry estimate); taxes.</p>
  <p><b>Option B — Renew and hold through expiry and beyond.</b> Keeps passive NNN income; rent bump at renewal resets value; tax basis protected; inflation passed through. Cons: concentration; tenant credit risk; term/value decay if renewal falters; illiquidity.</p>
  <p style="margin-bottom:0"><b>Option C — Hybrid (recommended): negotiate renewal/extension NOW with an escalator reset, while keeping the asset market-ready.</b> Retains upside, preserves optionality, forces the tenant to reveal intentions early. Sell only if pre-set triggers are breached.</p>
</div>

<div class="callout callout-rec"><div class="c-ico">✅</div><div><b>Recommendation.</b> Do not fire-sale today — but do not drift toward expiry either.
Execute the <b>Option C playbook</b>: (1) commission a lease abstract + estoppel now; (2) open renewal talks 24–36 months pre-expiry targeting a +10–20% reset plus NNN re-affirmation (illustrative targets — verify against your lease and market quotes); (3) keep a sale-ready package and 2 broker opinions of value on file; (4) set hard triggers for selling (below). If the tenant cannot or will not meet the reset, list 2027–2028 — inside the Olympic-catalyst window and with years of term remaining. Full logic and weighted scoring on <a href="decision-analysis.html">Decision Analysis</a>; PV modeling on <a href="projection-studio.html">Projection Studio</a>.</div></div>

<h2>4&nbsp;·&nbsp;Decision triggers (any one → move from “hold/renew” to “sell”)</h2>
<ol class="action tight">
  <li>Tenant declines renewal/extension or demands flat reset (no escalator catch-up).</li>
  <li>Two consecutive quarters of deteriorating system SSS worse than −3% or subject-store sales coverage &lt;1.2× rent (coverage not publicly verifiable — obtain internally).</li>
  <li>JACK net debt/EBITDA not trending toward the 4–5x target, or any 8-K signaling liquidity distress.</li>
  <li>Unsolicited bid at ≥ +15% over the broker opinion of value, or net-lease QSR cap rates compress ≥75 bps below today’s quotes.</li>
  <li>Significant capital requirement emerges (seismic retrofit mandate, roof, parking, ADA) exceeding 12 months of rent.</li>
</ol>

<h2>5&nbsp;·&nbsp;Risk posture</h2>
<p>Balanced BB-style profile: strong infill location and NNN structure, offset by single-asset concentration and tenant credit.
All 14 tracked risks — likelihood × impact, mitigants, BAU vs black-swan — are on the <a href="risk-register.html">Risk Register</a>; hazard quantification on <a href="hazards-black-swans.html">Hazards &amp; Black Swans</a>. Manageable with: early renewal, insurance certificates, seismic verification, diversified redeployment of any sale proceeds, and liquidity buffer.</p>

<h2>6&nbsp;·&nbsp;Verification & privacy statement</h2>
<p>Every table on this site carries a per-row source link to an official source (.gov / SEC / state of California) or is explicitly marked
<span class="badge b-industry">INDUSTRY</span> or <span class="badge b-flagged">FLAGGED</span>. Items that could not be verified are
<b>left blank and flagged</b> (<a href="flagged-for-review.html">Flagged for Review</a>), never invented. This is not legal, tax, accounting or investment advice.</p>
""",

    "decision-analysis": f"""
<h1 class="page-title">Decision Analysis — Sell vs. Renew</h1>
<p class="lede">Structured comparison of the three available strategies for the Property, weighted for the owner’s stated
objective: <b>preservation of wealth + opportunity for growth, with manageable risk</b>. Scores are analytical judgments
(1 = poor, 5 = excellent), not verified data; every factual input underpinning them is sourced on the linked pages.</p>

<h2>Weighted decision matrix</h2>
<div class="tbl-wrap"><div class="tbl-head"><h3>Criteria weights &amp; option scores (weighted totals computed live from the data file)</h3></div>
<div class="tbl-scroll"><table class="tbl" id="dm-table">
<thead><tr><th>Criterion (weight)</th><th>Option A — Sell 2026–28</th><th>Option B — Renew &amp; hold</th><th>Option C — Hybrid (recommended)</th></tr></thead>
<tbody></tbody>
<tfoot><tr id="dm-total"><td>Weighted total (max 5.00)</td><td></td><td></td><td></td></tr></tfoot>
</table></div>
<p class="small" style="padding:0 .85rem .6rem;margin:.4rem 0 0">Weights: wealth preservation 25% · income stability 20% · growth 15% · manageable risk 20% · tax efficiency 10% · liquidity 10%. Scores: analytical judgment; see Methodology. Totals are computed in-browser from <code>assets/app.js</code> data embedded at build time.</p>
</div>

<div class="callout callout-rec"><div class="c-ico">🎯</div><div><b>Decision.</b> Adopt <b>Option C (Hybrid)</b>: negotiate the renewal/extension now with a rent reset and keep the asset fully market-ready.
Option C dominates on wealth preservation (5.0), tax efficiency (4.0) and liquidity (4.0) without sacrificing income quality — and it converts
the expiry “cliff” into a negotiated event on your timeline, not the tenant’s.</div></div>

<h2>Option-by-option detail</h2>
<h3>Option A — Sell before expiry (2026–2028 window)</h3>
<ul class="tight">
  <li><b>Pros:</b> captures remaining-term premium; eliminates tenant-credit tail risk; liquidity unlocked; potential 1031 deferral into diversified income assets/DSTs; Olympics-window demand (2028) could lift sale pricing for well-located urban assets.</li>
  <li><b>Cons:</b> crystallizes capital gains + depreciation recapture (federal + CA); forfeits renewal rent bump (often the single largest value creator for NNN QSR); exits a replacement for basis that Prop 13 preserves; redeploys into a higher-rate world (10Y 4.90%).</li>
  <li><b>Best if:</b> any sell-trigger from the executive summary fires, or a bid ≥ +15% over independent value opinion appears.</li>
</ul>

<h3>Option B — Renew at expiry and hold (2030–2035 → 2040+)</h3>
<ul class="tight">
  <li><b>Pros:</b> long-term NNN passive income; tenant pays opex/taxes/insurance (inflation hedge); Prop 13 basis protection; renewal reset typically re-marks rent to market; preserves 30+ year wealth-building vehicle (QSR real estate with drive-through is scarce urban land).</li>
  <li><b>Cons:</b> single-asset concentration; term decay risk; tenant credit (JACK stock −72% FY2020→FY2025; SSS negative; activist campaign; restructuring); LA County population projected to decline → flat demand growth; illiquid exit if needed mid-term.</li>
  <li><b>Best if:</b> renewal is achieved with a meaningful reset and re-affirmed NNN + corporate/franchisee guarantee; you need the income, not the lump sum.</li>
</ul>

<h3>Option C — Hybrid: negotiate now, keep optionality (recommended)</h3>
<ul class="tight">
  <li><b>Mechanics:</b> (1) estoppel certificate within 30 days; (2) open extension talks 24–36 months before expiry; (3) target rent reset +10–20% (illustrative), NNN re-affirmation, updated guarantee + SNDA, % rent if applicable, notice deadlines calendared; (4) simultaneously: broker opinion of value ×2, sale-ready package (rent roll, lease abstract, insurance certificates, permits), 1031 pre-planning with CPA; (5) sell only on trigger breach.</li>
  <li><b>Pros:</b> highest expected value; keeps Olympic-window sale available later; de-risks the expiry cliff; tests tenant commitment early at zero cost.</li>
  <li><b>Cons:</b> requires active management; possible negotiation friction with tenant; broker opinions cost ~0.1–0.3% (fee estimate — not verified; typical practice).</li>
</ul>

<h2>Tax note (general information, not tax advice)</h2>
<div class="callout callout-warn"><div class="c-ico">🧾</div><div>A sale triggers federal capital gains + depreciation recapture (gain on depreciable property generally taxed up to 25% federal on recapture) and California tax on the gain; ongoing NNN income is taxed as ordinary passive income with depreciation shelter. A §1031 exchange can defer all federal and California gain only into like-kind property identified/acquired on strict deadlines. <b>Engage a qualified CPA/tax attorney before signing anything.</b> No parcel-specific tax bill or basis data appears here by design.</div></div>

<h2>Scenario comparison over the 2030–2035 expiry window</h2>
{T('rates_returns')}
<p class="small">Rate context above; see <a href="projection-studio.html">Projection Studio</a> for present-value modeling of the three paths.</p>
""",

    "projection-studio": f"""
<h1 class="page-title">Projection Studio — Renew vs. Sell model</h1>
<p class="lede">Interactive present-value comparison of (A) selling today vs (B) holding and renewing through the expiry window and beyond.
<b>All defaults are illustrative placeholders, not your lease terms.</b> Replace them with your lease abstract and broker quotes; nothing
here is a verified market value or investment advice.</p>

<div class="callout callout-info"><div class="c-ico">ℹ️</div><div><b>How it works.</b> Scenario A capitalizes next year’s base rent at the exit cap rate (less transaction costs) — i.e., today’s implied price — and reinvests the net proceeds at the reinvestment rate. Scenario B models escalated rent through the expiry, applies the renewal bump at the reset date, then values the property at sale at the exit cap rate on forward NOI, and discounts everything at the discount rate (your opportunity cost of capital). The sensitivity table shows Scenario&nbsp;B−A present-value advantage across exit cap rates (rows) × renewal bumps (columns); green = holding wins, red = selling wins.</div></div>

<div class="proj-grid">
  <form id="proj-form" class="card" autocomplete="off">
    <h3 style="margin-top:0">Inputs (editable)</h3>
    <div class="field"><label for="in-base-rent">Current annual base rent ($)</label><input id="in-base-rent" type="number" min="0" step="1000" value="180000"><small>Illustrative placeholder — use your lease. Never published externally.</small></div>
    <div class="field"><label for="in-growth">Annual escalation until expiry (%)</label><input id="in-growth" type="number" step="0.1" value="2.0"><small>Leases often carry stacked 5-year bumps (e.g., ~8% per 5 yrs ≈ 1.55%/yr). Verify lease.</small></div>
    <div class="field"><label for="in-years-expiry">Years until lease expiry (today 2026-11-06)</label><input id="in-years-expiry" type="number" step="0.25" value="6"><small>2030–2035 window → 4 to 9 years; default 6.</small></div>
    <div class="field"><label for="in-renew-bump">Rent reset at renewal (%)</label><input id="in-renew-bump" type="number" step="1" value="10"><small>Industry-typical NNN reset 10–20% (not verified official data).</small></div>
    <div class="field"><label for="in-post-growth">Escalation after renewal (% / yr)</label><input id="in-post-growth" type="number" step="0.1" value="2.0"><small>Illustrative.</small></div>
    <div class="field"><label for="in-hold-years">Model horizon (years)</label><input id="in-hold-years" type="number" step="0.5" value="10"><small>Total years to model, then terminal sale.</small></div>
    <div class="field"><label for="in-cap-rate">Exit / pricing cap rate (%)</label><input id="in-cap-rate" type="number" step="0.1" value="6.9"><small>Net-lease average 6.9% (CBRE Q2 2026, industry — not official); QSR often tighter.</small></div>
    <div class="field"><label for="in-sale-costs">Transaction costs (% of price)</label><input id="in-sale-costs" type="number" step="0.1" value="3.5"><small>Commission + closing estimate; illustrative.</small></div>
    <div class="field"><label for="in-reinvest">Reinvestment return on sale proceeds (%)</label><input id="in-reinvest" type="number" step="0.1" value="5.0"><small>Illustrative blended after-tax return.</small></div>
    <div class="field"><label for="in-discount">Discount rate / opportunity cost of capital (%)</label><input id="in-discount" type="number" step="0.1" value="6.5"><small>Illustrative.</small></div>
  </form>

  <div class="card">
    <h3 style="margin-top:0">Results (Scenario B minus Scenario A)</h3>
    <div class="proj-results">
      <div class="result-box" id="box-hold"><div class="r-label">PV — Hold &amp; renew (B)</div><div class="r-value" id="out-pv-hold">—</div></div>
      <div class="result-box" id="box-sell"><div class="r-label">PV — Sell now (A)</div><div class="r-value" id="out-pv-sell">—</div></div>
      <div class="result-box"><div class="r-label">B − A (advantage)</div><div class="r-value" id="out-delta">—</div></div>
      <div class="result-box"><div class="r-label">Implied sale price today</div><div class="r-value" id="out-sale-price">—</div></div>
      <div class="result-box"><div class="r-label">Terminal value (net, end of horizon)</div><div class="r-value" id="out-terminal">—</div></div>
      <div class="result-box"><div class="r-label">Future value of selling &amp; reinvesting</div><div class="r-value" id="out-fv-sell">—</div></div>
    </div>
    <p id="proj-verdict" class="small" style="font-weight:700;color:var(--navy)"></p>
    <h3>Sensitivity — PV advantage of holding (B − A)</h3>
    <div class="tbl-scroll"><table class="tbl sens-table" id="sens-table">
      <thead><tr><th>Exit cap rate \ Renewal bump</th><th>+0%</th><th>+5%</th><th>+10%</th><th>+15%</th><th>+20%</th></tr></thead>
      <tbody></tbody>
    </table></div>
    <p class="small">Holding generally wins when the renewal reset is ≥ +10% and cap rates stay ≤ ~7.5%; selling wins if the reset is flat or cap rates rise materially. This is a screening tool — not a valuation.</p>
  </div>
</div>
""",

    "demographics": f"""
<h1 class="page-title">Demographics & Geography</h1>
<p class="lede">Who lives around the Property — official U.S. Census Bureau figures for the City of Los Angeles and Los Angeles County.
Central LA sits at the dense core of the nation’s largest county by several measures; demand for drive-through QSR is rooted in density,
not sprawl growth.</p>
{T('population_overview')}
{T('demographics_composition')}
<div class="callout callout-info"><div class="c-ico">🧭</div><div><b>Read-through for the asset.</b> 8,304 people per square mile in the city vs 2,467 in the county; 47.2% Hispanic/Latino
(over-index for QSR value menus); dense multifamily housing with low owner-occupied rates (36.0%) → car-borne, grab-and-go consumption
patterns suit a Jack in the Box drive-through. Population is declining modestly — the investment case rests on <b>density + traffic counts + renewal escalators</b>, not on growth.</div></div>
<p class="small">Trade-area (Census-tract) figures for the specific corridor are not asserted here; see Flagged for Review. Census QuickFacts: <a href="https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia,losangelescountycalifornia/PST045224" target="_blank" rel="noopener">official page</a>. Vintage caveats: QuickFacts mixes 2025 population estimates, 2020–2024 ACS, 2025 SAIPE and 2023/2024 CBP/SUSB — methodology notes on the Census page.</p>
""",

    "economy-jobs": f"""
<h1 class="page-title">Economy & Jobs</h1>
<p class="lede">Employment, unemployment and the consumer-economy base supporting Central LA retail. Official: Bureau of Labor Statistics
(retrieved via FRED), U.S. Census Bureau.</p>
{T('labor_market')}
{T('business_economy')}
{T('labor_force_commute')}
<h2>What the numbers mean</h2>
<ul class="tight">
  <li><b>Labour market:</b> LA MSA unemployment 4.4% (Sep 2026, NSA) — better than California (5.1% SA) and slightly above the US (4.2% SA). The 2026 trend: May 4.8 → Jun 5.0 → Jul 5.0 → Aug 4.8 → Sep 4.4; easing, not deteriorating. Payrolls flat at ~6.30M — no recession signal, no boom either.</li>
  <li><b>Consumer scale:</b> $44.0B food &amp; accommodation sales countywide (2022) and $81.35B retail sales in the city (2022, $21,281 per capita). The operating pond for a QSR is enormous; capture rate, not market size, is the question.</li>
  <li><b>Chain-area jobs base:</b> 3.99M county payroll jobs across 304,988 employer establishments (2023), +2.3% employment growth 2022→2023 — modest but positive.</li>
  <li><b>Commute burden:</b> 30.4–30.7 minutes average — heavy car dependence favors drive-through; weekday lunch/dinner dayparts near employment nodes.</li>
</ul>
<div class="callout callout-warn"><div class="c-ico">⚠️</div><div><b>Watch item.</b> LA metro payrolls are essentially flat (6,311K Jun → 6,300K Sep 2026) while California unemployment sits a full point above the national rate.
A flat-to-soft 2026–27 is a headwind for same-store sales — exactly what JACK reported (system SSS −1.1% Q3 FY2026). Underwrite the renewal on
<b>contractual escalators</b>, not on sales growth.</div></div>
""",

    "population-projections": f"""
<h1 class="page-title">Population Projections (2025–2070)</h1>
<p class="lede">California Department of Finance P-2A projections (2024 Baseline, Vintage 2026 release, March 2026) for Los Angeles County —
the official planning series every public agency in the state uses. This is the single most important long-run demand indicator for the Property.</p>
{T('population_projections')}
<h2>Reading the projection</h2>
<ul class="tight">
  <li><b>2030:</b> 9,727,305 (−1.3% vs 2025) — essentially flat through the early expiry window.</li>
  <li><b>2035:</b> 9,708,647 (−1.5%) — flat-to-negative when the current lease expires.</li>
  <li><b>2040:</b> 9,637,524 (−2.2%); <b>2050:</b> 9,390,823 (−4.7%); <b>2060:</b> 8,961,332 (−9.1%); <b>2070:</b> 8,413,331 (−14.6%).</li>
  <li>Implied 2025→2035 CAGR ≈ <b>−0.15%/yr</b>; 2025→2060 ≈ <b>−0.27%/yr</b>. California as a whole keeps growing (39.5M → 41.1M peak ~2049, then slowly declining) — LA bleeds relative share to inland counties.</li>
</ul>
<div class="callout callout-warn"><div class="c-ico">📉</div><div><b>Investment implication.</b> A shrinking county does not kill a dense infill drive-through QSR — it caps growth. Do not underwrite
any revenue growth into the renewal negotiation; underwrite <b>rent escalations and the renewal reset</b>. Note the 2020 Census (10.014M) vs DOF 2024-baseline
2020 figure (10.012M) — series differ by methodology; QuickFacts/2020 Census used for historical fact, DOF P-2A for projections only (see Flagged for Review).</div></div>
<h2>Why LA shrinks in the projection</h2>
<p>DOF methodology ages the population forward with fertility, mortality and migration assumptions; LA shows decades of negative net domestic
migration and declining births. SCAG (the regional government) is more optimistic than DOF, but both agree on <b>flat to modestly negative</b> growth — neither
forecaster shows a boom. Any pro-forma assuming &gt;0.5%/yr population growth for LA County should be treated as aggressive.</p>
<p class="small">Source file (Excel): <a href="https://dof.ca.gov/media/docs/forecasting/Demographics/projections/P2A_County_Total.xlsx" target="_blank" rel="noopener">dof.ca.gov/media/docs/forecasting/Demographics/projections/P2A_County_Total.xlsx</a> · methodology: <a href="https://dof.ca.gov/forecasting/demographics/projections/" target="_blank" rel="noopener">DOF Population Projections</a>. Extracted and verified 2026-11-06; totals for FIPS 6037 LOS ANGELES row, all races/sexes/ages.</p>
""",

    }

