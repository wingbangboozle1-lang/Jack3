# Risk Analysis & Decision Framework — Sell vs. Renew (Task T4)

Session `93f3087c`, 2026-11-06. Subject: single-tenant Jack in the Box QSR on an **NNN lease expiring 2030–2035**, central Los Angeles, CA (`[PROPERTY ADDRESS REDACTED]`; owner `[OWNER NAME REDACTED]`). All sourced figures are cited in `docs/research-economy.md` and `docs/research-realestate.md`; this document is analysis built on those cited inputs (model logic is labeled as such).

## 1. Decision options

| Option | Description | Core economics (model logic on sourced inputs) |
|---|---|---|
| **A — Sell before expiry (base case)** | List now–2029; sell while 3–9 years of lease term remain; reinvest via IRC §1031 | Captures franchisee-QSR cap band 6.87–7.55% (Boulder Q3 2026) with maximum remaining term; eliminates expiry cliff; §1031 defers federal + CA tax (IRS/FTB rules) |
| **B — Hold to expiry, attempt renewal** | Keep NNN income to 2030–2035, then negotiate renewal/rewrite | Income stream ends at expiry unless a new agreement is signed; FDD Item 17 gives **no renewal right** — renewal is discretionary; at expiry value reverts to land/vacant value if no tenant |
| **C — Sell at/near expiry** | Wait until 2030–2035 to sell | Worst of both worlds: sells with ~0 years of term left (cap-rate band >7.55%+, distressed) and possibly vacant — deep discount |
| **D — Early extension + hold** | Negotiate a new 10+ yr lease/extension **now**, then hold | Converts the cliff into a term; only viable if franchisor/franchisee signs a new agreement at acceptable rent with escalations (10%/5yr typical for QSR) |

## 2. Valuation mechanics (model logic, labeled)

- Value ≈ NOI ÷ cap rate. NOI and current rent are property-specific and were **not provided (anonymized)** → left blank on the site, flagged as `[NOT PROVIDED — ANONYMIZED]`.
- Cap-rate inputs (sourced): net-lease avg 6.92%; corporate QSR 5.90%; franchisee QSR 6.87%; franchisee QSR <10 yrs remaining 7.55% (Boulder Group Q3 2026 [INDUSTRY]); LA retail avg cap 6.0%, sale price $372/SF (Kidder/CoStar Q3 2026 [INDUSTRY]).
- Rate backdrop (sourced): fed funds 3.75–4.00% (Fed, 10/28/2026); 10Y UST 4.90%, 30Y 5.28% (Treasury, 11/4/2026). A 6.9–7.5% cap is only ~200–260 bps over the 10Y — thin for a single-tenant, single-credit asset with a hard expiry date, especially with hike risk into Dec 2026 (flagged secondary).
- Illustrative only (NOT property data): $100,000 NOI at 6.87% ≈ $1.46M; at 7.55% ≈ $1.32M; at 5.90% ≈ $1.69M. Every year of remaining term lost moves price toward the high-cap end.

## 3. Risk matrix — every material risk by decision

Likelihood/impact are qualitative judgments (model logic) anchored to the cited data.

| # | Risk | Type | Likelihood | Impact | Most affects | Mitigation | Source link |
|---|---|---|---|---|---|---|---|
| R1 | Lease not renewed at 2030–2035 expiry (no contractual renewal right; franchisor discretion) | Business-as-usual / structural | High | Severe (income ends; value → land/vacant) | B, C | Sell before expiry (A), or lock extension now (D) | https://www.jackintheboxfranchising.com/ |
| R2 | Tenant (franchisee) default / store closure before expiry — JACK system shrinking (2,136 → guided 2,050–2,100 by end-2026), SSS −1% to +1% | Business-as-usual | Medium | Severe | A, B | Verify corporate guarantee & unit AUV (blank — anonymized); diversify proceeds via §1031 | https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm |
| R3 | Cap-rate expansion / rate hikes (fed funds 3.75–4.00%; 10Y 4.90%; Dec-2026 hike risk) | Business-as-usual (macro) | Medium–High | High (lower resale price each year held) | A timing, B, C | Sell sooner; the <10-yr band already prices at 7.55% | https://www.federalreserve.gov/newsevents/pressreleases/monetary20261028a.htm ; https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=202611 ; https://bouldergroup.com/media/pdf/2026-Q3-Net-Lease-Research-Report.pdf |
| R4 | Tax hit on sale (fed LTCG + CA 13.3% + depreciation recapture; CA 3⅓% withholding) | Business-as-usual | Certain if sold | Medium (reduces net proceeds) | A, C | §1031 exchange, 45/180-day rules, FTB Form 593; keep replacement in CA or plan clawback (Form 3840) | https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges ; https://www.ftb.ca.gov/ |
| R5 | **Black swan: major earthquake** — USGS UCERF3: 60% chance M6.7+ in LA region within 30 yrs (46% M7.0+); FEMA NRI earthquake EAL $4.57B/yr; county composite risk 100.0 (highest in US) | Black swan | Medium (60%/30yr) | Severe (structure damage; owner retains structural risk even under NNN) | All | Earthquake insurance (CEA), structural retrofit, maintain reserves; diversify geography via §1031 | https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area ; https://hazards.fema.gov/nri/ |
| R6 | **Black swan: wildfire** — Jan 2025 Eaton/Palisades: 37,469 acres, 16,256 structures destroyed, 31 deaths, $5.2–10.1B output loss; 2025 FHSZ maps expanded LA County very-high zones ~30% | Black swan | Low–Medium (urban core lower than foothills, but Santa Ana wind events reach central LA) | Severe | All | Central LA urban site is lower wildfire exposure than foothill zones (verify parcel's FHSZ class — blank/anonymized); insurance availability/cost | https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire ; https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire ; https://file.lacounty.gov/SDSInter/lac/1199046_Eaton_Palisades_Fires_Anniversary_Fact_Sheet.pdf ; https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones |
| R7 | **Black swan: flood** — FEMA riverine flood EAL $2.81B/yr (Very High) | Black swan | Low–Medium per year | Medium–High | All | Check FEMA flood zone for parcel (blank/anonymized); NFIP/ excess flood cover | https://hazards.fema.gov/nri/ ; https://msc.fema.gov/portal/home |
| R8 | Insurance market stress in CA — FAIR Plan 696,562 policies (June 2026, +8% YoY), $768B exposure; 29.1% dwelling rate increase eff. 10/15/2026; nonrenewal moratorium expired 1/7/2026 | Business-as-usual (market) | High | Medium (tenant pays under NNN during term; owner exposed at re-tenanting/expiry and for own liability/structure cover) | B, C, D | Confirm tenant insurance covenants in lease; owner keeps own property/liability/loss-of-rent cover | https://www.insurance.ca.gov/ ; https://www.fairplan.org/ |
| R9 | Area population decline (DOF P-2A: county −1.3% by 2030, −4.7% by 2050) vs SCAG growth case — divergence flagged | Business-as-usual | Medium | Medium (softer long-run trade-area growth) | B, D | Use conservative case; site-level traffic/AUV data (anonymized) is the real driver | https://dof.ca.gov/media/docs/forecasting/Demographics/projections/P2A_County_Total.xlsx ; https://scag.ca.gov/sites/default/files/2024-05/23-2987-tr-demographics-growth-forecast-final-040424.pdf |
| R10 | Recession / consumer pullback — QSR value segment resilient but not immune; city poverty 16.5% | Business-as-usual | Medium | Medium | All | NNN income is the cushion; hold liquidity; avoid leverage | https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225 |
| R11 | §1031 execution risk — 45-day ID / 180-day close are hard deadlines; CA 3⅓% withholding if Form 593 missed | Business-as-usual (process) | Low if planned | High (full gain taxable) | A | Engage qualified intermediary **before** listing; pre-identify replacement properties | https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges ; https://www.ftb.ca.gov/ |
| R12 | Prop 13 reassessment on sale raises buyer's tax load → caps bid price; conversely seller's locked basis disappears at sale | Business-as-usual | Certain if sold | Medium (embedded in price) | A, C | Factor into pricing expectation | https://boe.ca.gov/proptaxes/pdf/lta25023.pdf |

## 4. Scenario analysis (model logic on sourced inputs; property NOI blank/anonymized)

| Scenario | Assumptions | Outcome for owner | Verdict |
|---|---|---|---|
| S1 Base — sell 2027–2029 via §1031 | Cap 6.87–7.55% with 2–8 yrs term left; rates 3.75–4.00% fed funds | Full value capture before cliff; taxes deferred; capital redeployed to lower-hazard/better-growth assets | **Recommended base case** |
| S2 Hold to expiry, renewal granted | New 10–20 yr agreement at market rent + escalations | Continued NNN income at ~6.9% cap equivalent yield; but renewal is discretionary (FDD) — cannot be assumed | Acceptable only if extension signed now (Option D) |
| S3 Hold to expiry, no renewal | Income stops 2030–2035; re-tenant at LA retail market (vacancy 5.7–6.15%, asking $2.40–2.75/SF/mo) or sell vacant | Value cliff; re-tenanting cost, downtime, cap 6.0% on retail but on owner's (now full) expense load | Avoid |
| S4 Black swan — M7+ earthquake before sale | USGS 46% M7.0+ / 30 yrs; FEMA EAL $4.57B | Structural damage; insurance claim; possible total loss if uninsured | Mitigate: CEA policy, retrofit, reserves |
| S5 Black swan — wildfire reaches site | Jan-2025 precedent: 16,256 structures destroyed county-wide | Smoke/structure damage; business interruption; insurance market hardening (FAIR Plan +8%, +29.1% rates) | Lower for urban core; verify FHSZ class |
| S6 Macro — further rate hikes (Dec 2026 hike odds ~76%, flagged) | 10Y >5% | Cap rates expand → each year held is worth less at exit | Reinforces selling sooner |

## 5. Recommendation (balanced, risk-managed)

**Base case: Option A — sell before the lease expires, targeting a 2027–2029 sale window, executed as an IRC §1031 exchange.**

Rationale:
1. The dominant risk is the **2030–2035 expiry cliff**: no contractual renewal right (FDD Item 17), discretionary rewrite, and a tenant system that is shrinking (SEC 10-K / guidance). Selling with 2–8 years of term remaining monetizes the lease at the 6.87–7.55% band; holding to expiry risks a near-total income stop.
2. The **rate environment** (fed funds 3.75–4.00%, 10Y 4.90%, hike risk) pressures cap rates upward — time decay works against the holder.
3. Area fundamentals (3.87M city population, $81B retail sales, 4.4–5.0% unemployment, +8.7% projected jobs 2022–2032) keep the *site* attractive to net-lease buyers now — sell into that demand.
4. **Tax efficiency:** §1031 defers the gain (45/180-day rules; FTB Form 593 to avoid CA 3⅓% withholding; mind the CA clawback if moving out of state).
5. **Wealth preservation:** redeploy into 1–3 replacement NNN/other assets in lower-hazard, growing markets (diversify away from LA County's nation-highest FEMA NRI 100.0 and 60% M6.7+/30-yr earthquake odds), keep 6–12 months of expenses in cash, carry earthquake/liability cover on anything retained.

**Conditions that would flip the decision to hold (Option D):** a signed lease extension/new agreement now for ≥10 years at or above current rent with standard QSR escalations (10%/5 yr) and a creditworthy tenant or corporate guarantee — only then does holding beat selling, because the cliff is removed. Absent that, sell before expiry. Set a hard decision deadline **no later than 24 months before the exact expiry date** (exact date `[NOT PROVIDED — ANONYMIZED]` → use 2033 midpoint conservatively → decision deadline ≈ end of 2031, earlier if market softens).

**Risk level of the recommended path: manageable** — it converts an uncapped cliff risk into a planned, tax-deferred exit, while the main residual risks (execution, 1031 deadlines, replacement-asset selection) are controllable process risks.
