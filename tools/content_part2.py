"""Page body content (part 2)."""

def pages_part2(T):
    return {

    "income-housing": f"""
<h1 class="page-title">Income, Poverty & Housing</h1>
<p class="lede">The affordability arithmetic that shapes QSR demand — and what it means for a Central LA location competing for
traffic against every other quick-service option. Official: U.S. Census Bureau; FHFA via FRED.</p>
{T('income_poverty')}
{T('housing_market')}
{T('housing_hpi')}
<h2>Read-through</h2>
<ul class="tight">
  <li><b>Affordability squeeze:</b> city median rent $1,933/mo vs median household income $81,939/yr → housing ≈ <b>28% of gross income</b> before tax; homeownership rate just 36.0% in the city. Cost-pressed consumers trade into value QSR — a structural tailwind for Jack in the Box’s price positioning, but they are also quick to cut frequency (ticket elasticity).</li>
  <li><b>Poverty:</b> 16.5% city / 13.3% county — value messaging matters; expect deep deal usage, which pressures restaurant-level margins (JACK FY2025 restaurant margin 19.6%).</li>
  <li><b>Asset appreciation:</b> FHFA HPI LA County +28.4% (2021→2025), +1.7% YoY 2025 (403.74 vs 2000=100). Replacement-cost reality: land + construction in infill LA is expensive — your NNN rent stream is backed by very high-cost dirt, which supports residual land value at expiry.</li>
  <li><b>Rent inflation vs wage inflation:</b> gross rents up sharply since 2020 while wages lag → consumer strain persists into 2027+; conservative underwriting advised.</li>
</ul>
<div class="callout callout-info"><div class="c-ico">🏠</div><div><b>Why this matters for a NNN decision.</b> The Property’s exit value at expiry is bounded below by land residual value, which in infill Central LA is elevated by housing scarcity — the same scarcity that squeezes tenants. Selling into a scarcity premium now vs. riding the renewal bump is the crux; see <a href="decision-analysis.html">Decision Analysis</a>.</div></div>
""",

    "schools-education": f"""
<h1 class="page-title">Schools & Education</h1>
<p class="lede">Educational attainment drives long-run income and spending power. District data: California School Dashboard (official,
California Department of Education). Attainment: U.S. Census Bureau ACS. Parcel-specific attendance zones require the address — see Flagged for Review.</p>
{T('education_attainment')}
{T('lausd_dashboard')}
<h2>LAUSD trajectory</h2>
<ul class="tight">
  <li><b>Graduation rate:</b> 82.1% (2019) → 86.0% (2022) → 83.6% (2023) → 86.7% (2024) → <b>86.5% (2025)</b> — sustained improvement vs pre-pandemic baseline.</li>
  <li><b>Chronic absenteeism:</b> 18.2% (2019) → <b>39.8% (2022)</b> → 31.0% (2023) → 23.3% (2024) → <b>21.9% (2025)</b> — crisis improved but not normalized; remains above the 2019 baseline.</li>
  <li><b>Attainment:</b> 79.6% of LA city adults hold a HS diploma (county 80.9%); 38.5% hold a bachelor’s degree (county 36.0%) — a highly service- and trade-oriented workforce, consistent with QSR employment availability and consumer mix.</li>
</ul>
<div class="callout callout-info"><div class="c-ico">🎓</div><div><b>Read-through.</b> School quality is a second-order driver of household formation and retail spending in family neighborhoods. The improvement in LAUSD metrics is genuinely positive for the corridor’s long-run residential value — but the Property’s performance is far more sensitive to tenant credit and traffic than to school metrics. Do not overweight this factor in the sell/renew decision; it matters for <b>resale liquidity</b> (family buyers) more than for operations.</div></div>
<p class="small">District-level figures only; attendance-zone lookup and school-specific ratings require the subject address and were not performed — see <a href="flagged-for-review.html">Flagged for Review</a>. Dashboard source: <a href="https://www.caschooldashboard.org/reports/19647330000000/2025" target="_blank" rel="noopener">caschooldashboard.org — LA Unified, 2025</a>.</p>
""",

    "real-estate-market": f"""
<h1 class="page-title">Real Estate & Net-Lease Market</h1>
<p class="lede">Pricing context for the Property. Official sources: FHFA (house prices) and Federal Reserve (rates) via FRED, U.S. Census Bureau.
Cap-rate benchmarks are <b>industry</b> data (CBRE) — there is no official government source for cap rates; they are shown labeled accordingly and never as verified fact.</p>
{T('housing_hpi')}
{T('industry_caprates')}
{T('housing_market')}
<h2>Net-lease mechanics you must internalize</h2>
<ul class="tight">
  <li><b>Remaining-term gravity.</b> Net-lease pricing embeds remaining term: as the lease approaches expiry with no renewal in hand, buyer demand thins and implied cap rates widen. The 2030–2035 window is the danger zone — value erosion is nonlinear.</li>
  <li><b>Cap rate math.</b> At a 6.9% net-lease average (industry), $1 of net rent ≈ $14.49 of value; at 7.5% ≈ $13.33 (−8.0%); at 6.0% ≈ $16.67 (+15.0%). Every +100 bps costs roughly 12–13% of value at these levels. Rate trajectory (10Y 4.90% as of 2026-11-04) is therefore a first-order sale-timing variable — see <a href="projection-studio.html">Projection Studio</a>.</li>
  <li><b>QSR premium positioning.</b> QSR NNN deals frequently trade tighter than the blended retail average (~5–6% per third-party reporting — FLAGGED, not primary). Branded, drive-through, corporate-guaranteed JACK assets would normally command that tighter range <i>if</i> the tenant and term are strong; JACK’s current credit trajectory argues for underwriting the <b>retail average or wider</b> until proven otherwise.</li>
  <li><b>Escalation compounding.</b> A stacked 8%-per-5-years structure compounds to ~1.55%/yr — modest real protection vs 3–4% inflation; renewal resets are where the value is made.</li>
</ul>
<div class="callout callout-warn"><div class="c-ico">🏷️</div><div><b>Pricing honesty.</b> Any specific price, cap rate or rent figure for the subject asset is deliberately absent — no official valuation exists, and listing data is excluded (privacy + not official). To underwrite a sale, obtain two signed broker opinions of value; to underwrite a hold, abstract the lease and model the renewal reset. Nothing on this page should be read as an appraisal.</div></div>
""",

    "growth-catalysts": f"""
<h1 class="page-title">Growth Catalysts — 2026 to 2035</h1>
<p class="lede">What could push demand and pricing up inside the holding window — and what is merely narrative. Official where possible;
estimates explicitly labeled.</p>
{T('la28_dates')}
{T('la28')}
<h2>Catalyst inventory</h2>
<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(280px,1fr))">
  <div class="card" style="margin:0"><h3 style="margin-top:0">🏟️ 2028 Olympic & Paralympic Games</h3>
    <p class="small">Paralympic Games <b>Aug 15–27, 2028</b> (verified, IPC); Olympic Games July 2028 (dates reported 14–30 July — not re-verified, Flagged F-16). LA Memorial Coliseum / Downtown &amp; regional venues. SCAG (governmental): <b>$13.6–17.6B</b> added regional GDP 2024–2029 (six counties). LAEDC commissioned study (non-governmental): $20–40B output. LA28 budget ~$7.15B (reported). <b>Not a measurement — an estimate.</b></p>
    <p class="small"><b>Property impact:</b> visitor surge 2027–2028 around venues; downtown/East-LA corridors see traffic spikes; retail leasing and consumer spending bump. One-time pulse, not a permanent lift — but it lands <i>inside</i> your sale window.</p>
  </div>
  <div class="card" style="margin:0"><h3 style="margin-top:0">🚇 Transit & infrastructure buildout</h3>
    <p class="small">Metro rail/BRT expansion and LAX modernization are budgeted — check <a href="https://metro.net" target="_blank" rel="noopener">metro.net</a> and <a href="https://www.flylax.com" target="_blank" rel="noopener">flylax.com</a> for official project scope/costs before relying on any number. No unverified figure is asserted on this page.</p>
    <p class="small"><b>Property impact:</b> accessibility improvements favor urban infill retail; construction-phase disruption is a short-term drag.</p>
  </div>
  <div class="card" style="margin:0"><h3 style="margin-top:0">🏗️ Housing construction permits (2025: 22,250 countywide)</h3>
    <p class="small">Countywide permits ticked at 22,250 (2025, QuickFacts) — active pipeline, mostly multifamily infill; net-new residents support local QSR counts even in a flat-population county (housing churn within LA is high — 90.8% of county residents live in the same house 1yr on, meaning 9.2% move annually).</p>
  </div>
  <div class="card" style="margin:0"><h3 style="margin-top:0">🌆 Downtown/East LA revitalization & adaptive reuse</h3>
    <p class="small">Office-to-residential conversions and streetscape programs (City Planning, <a href="https://planning.lacity.org" target="_blank" rel="noopener">planning.lacity.org</a>) — monitor ZIMAS/council files for the specific corridor. No quantity asserted as verified.</p>
  </div>
</div>
<div class="callout callout-info"><div class="c-ico">⏱️</div><div><b>Timing insight.</b> The Olympics catalyst peaks <b>2027–2029</b> — ahead of the 2030 expiry edge and squarely in the 2026–2028 sell window.
If you sell, sell into that strength with a fresh lease or strong estoppel in hand. If you renew, the catalyst still benefits tenant sales and
your escalations. Either way, do not let the expiry negotiation drift past <b>early 2028</b>.</div></div>
""",

    }

