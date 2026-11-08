# Line-by-line verification record — 2026-11-08

**Session:** `abcebbee` · **Branch:** `arena/abcebbee-jack3` · **Scope:** the curated, currently published
dashboard (root `index.html`, `economy`, `tenant`, `risk`, `place`, `decisions`, `model`, `review`, `sources`).

**Method.** Every row below was read back against the publisher page named in its source cell, fetched directly on
2026-11-08 (UTC). A row is marked *Confirmed* only when the published cell value appears on that page with the same
geography and period. Where a value could not be confirmed, the row is left blank in the dataset and the gap is
recorded in §4. No value was inferred, interpolated or substituted.

**Independence.** This pass is independent of the earlier sessions' verification notes. Where a prior flag is now
closed by an official page, that is stated in §4; where a prior value differs from what the official page shows, the
difference is recorded rather than silently corrected.

## 1. Sources re-fetched (all 12 in the published register)

| Key | Publisher page | HTTP result | Note |
|---|---|---|---|
| city | U.S. Census QuickFacts, Los Angeles city | 200, 4 chunks read | V2025 + 2020–2024 ACS 5-year |
| county | U.S. Census QuickFacts, Los Angeles County | 200, chunk 0–1 read | V2025 + 2020–2024 ACS 5-year |
| bls | BLS, Los Angeles Area Economic Summary (updated 2026-11-04) | 200, full PDF text | September 2026 observations |
| jack | Jack in the Box Inc., Q3 FY2026 earnings release (2026-08-12) | 200 | Quarter ended 2026-07-05 |
| closure | Jack in the Box Inc., “JACK on Track” release (2025-04-23) | 200 | Closure program + real-estate sales plan |
| fire | CAL FIRE – OSFM, Fire Hazard Severity Zones | 200 | 2026 SRA comment period open; LRA maps released 2025 |
| quake | California Geological Survey, EQ Zapp | 200 | Interactive map; no parcel queried |
| flood | FEMA Flood Map Service Center | 200 | Official NFIP map source |
| school | California Department of Education, School Dashboard hub | 200 | Hub page; no school identified |
| wage | CA DIR, Fast Food Minimum Wage FAQ | 200 | $20.00/hour from 2024-04-01 |
| zoning | City of LA Planning, ZIMAS | 200 (application shell) | No parcel queried; no fact extracted |
| irs | IRS, Like-kind exchanges — real estate tax tips | 200 | §1031 deferral, real property only |

## 2. Row-by-row re-read

### Area fundamentals (`economy.html`)

| Row | Published value | Source (official) | Re-read 2026-11-08 |
|---|---|---|---|
| Population | 3,869,089 | [city](https://www.census.gov/quickfacts/losangelescitycalifornia) | Confirmed |
| Population change | −0.8% | [city](https://www.census.gov/quickfacts/losangelescitycalifornia) | Confirmed |
| Population | 9,694,934 | [county](https://www.census.gov/quickfacts/losangelescountycalifornia) | Confirmed |
| Population change | −3.2% | [county](https://www.census.gov/quickfacts/losangelescountycalifornia) | Confirmed |
| Median household income | $81,939 | [city](https://www.census.gov/quickfacts/losangelescitycalifornia) | Confirmed |
| Per capita income | $47,685 | [city](https://www.census.gov/quickfacts/losangelescitycalifornia) | Confirmed |
| Median gross residential rent | $1,933 / month | [city](https://www.census.gov/quickfacts/losangelescitycalifornia) | Confirmed |
| Bachelor’s degree or higher | 38.5% | [city](https://www.census.gov/quickfacts/losangelescitycalifornia) | Confirmed |
| High school graduate or higher | 79.6% | [city](https://www.census.gov/quickfacts/losangelescitycalifornia) | Confirmed |
| Population density | 8,304.2 / sq mi | [city](https://www.census.gov/quickfacts/losangelescitycalifornia) | Confirmed |
| Mean commute | 30.7 minutes | [city](https://www.census.gov/quickfacts/losangelescitycalifornia) | Confirmed |
| Unemployment | 4.5% | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Confirmed |
| Unemployment | 4.5% | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Confirmed |
| Total nonfarm employment | 6,282.1 thousand | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Confirmed |
| Nonfarm employment change | +0.5% year over year | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Confirmed |
| Education & health employment change | +3.8% year over year | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Confirmed |
| Information employment change | −5.7% year over year | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Confirmed |
| All-items CPI-U change | +3.7% year over year | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Confirmed |
| Average weekly wage | $1,704 | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Confirmed |

### Tenant & lease (`tenant.html`)

| Row | Published value | Source (official) | Re-read 2026-11-08 |
|---|---|---|---|
| System same-store sales | −1.1% | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Confirmed |
| Systemwide sales change | −1.4% | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Confirmed |
| Restaurant closures | 17 | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Confirmed |
| Restaurant openings | 4 | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Confirmed |
| Restaurant count | 2,115 | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Confirmed |
| 2025 announced closure program | Approximately 150–200 restaurants | [closure](https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Unveils-JACK-on-Track-Plan-to-Improve-Long-Term-Financial-Performance/default.aspx) | Confirmed |
| Covered fast-food minimum wage | $20.00 / hour | [wage](https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm) | Confirmed |
| Exact expiration / notice deadlines | _(blank)_ | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Blank confirmed |
| Legal tenant / guarantor / financial coverage | _(blank)_ | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Blank confirmed |
| Rent / escalations / options / landlord obligations | _(blank)_ | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Blank confirmed |
| Store profitability / arrears / renewal intention | _(blank)_ | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Blank confirmed |

### Risk & resilience (`risk.html`)

| Row | Published value | Source (official) | Re-read 2026-11-08 |
|---|---|---|---|
| Earthquake / liquefaction / fault rupture | CGS maps ground-failure zones; maps do not replace site investigations or measure all shaking risk. | [quake](https://www.conservation.ca.gov/cgs/geohazards/eq-zapp) | Confirmed |
| Wildfire / smoke / access disruption | CAL FIRE distinguishes physical hazard from mitigated risk. | [fire](https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones) | Confirmed |
| Flood / severe storm | FEMA MSC is the official NFIP flood-hazard information source; maps can change. | [flood](https://msc.fema.gov/portal/home) | Confirmed |
| Closure / default / franchise stress | Issuer reports negative same-store sales and restaurant closures. | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Stated as analysis/review — no numeric claim |
| Inflation / labor pressure | DIR lists a higher wage floor for covered fast-food workers. | [wage](https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm) | Stated as analysis/review — no numeric claim |
| Interest rates / refinancing / cap rates | No property borrowing terms or verified sale comparables available. | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Stated as analysis/review — no numeric claim |
| Permitting / loss of drive-through use | ZIMAS is the City Planning public information system; parcel not identified. | [zoning](https://zimas.lacity.org/) | Stated as analysis/review — no numeric claim |
| Pandemic / civil disruption / utility outage / correlated catastrophe | No verified probability or site loss estimate. | [flood](https://msc.fema.gov/portal/home) | Stated as analysis/review — no numeric claim |
| Concentration / liquidity / reinvestment | Owner portfolio and liquidity needs are deliberately unavailable. | [irs](https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips) | Stated as analysis/review — no numeric claim |

### Neighborhood & land (`place.html`)

| Row | Published value | Source (official) | Re-read 2026-11-08 |
|---|---|---|---|
| Geography / access / visibility | _(blank)_ | [zoning](https://zimas.lacity.org/) | Blank confirmed |
| School system performance | _(blank)_ | [school](https://www.cde.ca.gov/ta/ac/cm/) | Blank confirmed |
| Trade-area population / income / daytime workers | _(blank)_ | [city](https://www.census.gov/quickfacts/losangelescitycalifornia) | Blank confirmed |
| Zoning / redevelopment / permits / title constraints | _(blank)_ | [zoning](https://zimas.lacity.org/) | Blank confirmed |
| Competition / traffic / transit / crime / development pipeline | _(blank)_ | [zoning](https://zimas.lacity.org/) | Blank confirmed |
| Heat / air quality / contamination / insurability | _(blank)_ | [fire](https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones) | Blank confirmed |

### Decision pathways (`decisions.html`)

| Row | Published value | Source (official) | Re-read 2026-11-08 |
|---|---|---|---|
| Sell before expiration | A verified after-tax offer beats the risk-adjusted value of continued income and alternatives. | [irs](https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips) | Stated as analysis/review — no numeric claim |
| Negotiate early renewal / extension | Documented tenant credit, enforceable obligations, acceptable rent and expense allocation support holding. | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Stated as analysis/review — no numeric claim |
| Hold under existing lease | Contractual income, liquidity and insured downside are independently established and attractive relative to sale. | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Stated as analysis/review — no numeric claim |
| Renew then sell | A signed creditworthy extension improves actual bids enough to offset concessions and costs. | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Stated as analysis/review — no numeric claim |
| Re-tenant / reposition | Documented alternate demand and permitted use justify vacancy and capital spending. | [zoning](https://zimas.lacity.org/) | Stated as analysis/review — no numeric claim |
| Redevelop / ground-lease alternative | Verified legal feasibility and independently costed residual land value exceed existing-use value. | [zoning](https://zimas.lacity.org/) | Stated as analysis/review — no numeric claim |
| Sell with potential §1031 exchange | Qualified business/investment real-property exchange is suitable after tax/legal review. | [irs](https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips) | Stated as analysis/review — no numeric claim |

### Projection framework (`model.html`)

| Row | Published value | Source (official) | Re-read 2026-11-08 |
|---|---|---|---|
| Business as usual · 2030–2035 | _(blank)_ | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Blank confirmed |
| Renewal case · 2030–2035 | _(blank)_ | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Blank confirmed |
| Vacancy / re-tenant case | _(blank)_ | [zoning](https://zimas.lacity.org/) | Blank confirmed |
| Catastrophe / interrupted income | _(blank)_ | [quake](https://www.conservation.ca.gov/cgs/geohazards/eq-zapp) | Blank confirmed |
| Sale net proceeds / after-tax NPV | _(blank)_ | [irs](https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips) | Blank confirmed |
| Robust decision rule | _(blank)_ | [irs](https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips) | Stated as analysis/review — no numeric claim |
| Validation and monitoring | _(blank)_ | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Stated as analysis/review — no numeric claim |

### Flagged for Review (`review.html`)

| Row | Published value | Source (official) | Re-read 2026-11-08 |
|---|---|---|---|
| Critical | Property identity and lease | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Blank confirmed |
| Critical | Value, debt and owner suitability | [irs](https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips) | Blank confirmed |
| High | Geographic mismatch | [city](https://www.census.gov/quickfacts/losangelescitycalifornia) | Blank confirmed |
| High | Tenant and guarantee mismatch | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Blank confirmed |
| High | Unquantified hazards and insurance | [quake](https://www.conservation.ca.gov/cgs/geohazards/eq-zapp) | Blank confirmed |
| High | Missing neighborhood evidence | [school](https://www.cde.ca.gov/ta/ac/cm/) | Blank confirmed |
| High | Projection not calibrated | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Blank confirmed |
| Review | Source revisions and sampling | [city](https://www.census.gov/quickfacts/losangelescitycalifornia) | Stated as analysis/review — no numeric claim |
| Review | Source URL repairs | [fire](https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones) | Stated as analysis/review — no numeric claim |
| Review | Jurisdiction and entitlements | [zoning](https://zimas.lacity.org/) | Stated as analysis/review — no numeric claim |
| Review | Conflicting inherited strategy rankings | [irs](https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips) | Stated as analysis/review — no numeric claim |
| Review | Rolling BLS source updated | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Stated as analysis/review — no numeric claim |
| Review | CDE source unavailable during audit | [school](https://www.cde.ca.gov/ta/ac/cm/) | Stated as analysis/review — no numeric claim |
| Review | Franchise date is not lease expiration | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Stated as analysis/review — no numeric claim |
| Critical | Franchise agreement ≠ property lease | [closure](https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Unveils-JACK-on-Track-Plan-to-Improve-Long-Term-Financial-Performance/default.aspx) | Stated as analysis/review — no numeric claim |
| Critical | Prior model and recommendations | [jack](https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx) | Stated as analysis/review — no numeric claim |
| High | Companion report publication | [city](https://www.census.gov/quickfacts/losangelescitycalifornia) | Stated as analysis/review — no numeric claim |
| Review | Live source updates | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Stated as analysis/review — no numeric claim |
| High | Employment and CPI as-of corrections (F-16) | [bls](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | Stated as analysis/review — no numeric claim |
| Medium | California minimum wage from 2027-01-01 (F-17) | [wage](https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm) | Stated as analysis/review — no numeric claim |
## 3. Additional official pages read this session (used for new rows, not yet in the published register)

| Publisher | Page | Verified value(s) |
|---|---|---|
| LA County Assessor | https://assessor.lacounty.gov/real-estate-toolkit/proposition-13 | 1% general levy cap; 2% maximum annual assessed-value increase; reassessment on change of ownership / new construction; voter-approved debt and direct assessments sit on top |
| City of LA Office of Finance | https://finance.lacity.gov/faq/measure-ula | City base real property transfer tax $2.25 per $500 (0.45%); Measure ULA 4% above $5,400,000 and 5.5% at/above $10,900,000 for closings after 2026-06-30; thresholds indexed annually to Chained CPI; ULA measured on gross value, base tax on net value |
| CA DIR | https://www.dir.ca.gov/dlse/FAQ_MinimumWage.htm | State minimum wage $16.90/hour effective 2026-01-01, all employers |
| CA Dept of Education | https://www.cde.ca.gov/sdprofile/details.aspx?cds=19647330000000 | LAUSD 2025-26 enrollment 497,105; English learners 81,328 (16.4%) |
| CA Dept of Education | https://www.cde.ca.gov/ds/ad/ceflargesmalldist.asp | LAUSD ranks 1st of California districts at 497,105 enrolled; statewide 2025-26 enrollment 5,731,260 |
| CA Dept of Education | https://www.cde.ca.gov/ds/ad/filesacgr.asp | Adjusted cohort graduation-rate data published as state/county/district/school files (acgr26.txt, 16 MB, posted 2026-10-15); district value not extracted this pass |
| USGS | https://pubs.usgs.gov/of/2008/1150/ | ShakeOut scenario: hypothetical M7.8 southern San Andreas earthquake, ~1,800 deaths, ~$213bn economic losses |
| CAL FIRE | https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire | Palisades Fire: 23,448 acres, 6,845 structures destroyed, 975 damaged, 12 confirmed civilian fatalities |
| CAL FIRE | https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire | Eaton Fire: 14,021 acres, 9,419 structures destroyed, 1,076 damaged, 19 confirmed civilian fatalities |
| Federal Reserve (FRED DGS10) | https://fred.stlouisfed.org/series/DGS10 | 10-year Treasury constant-maturity yield 4.84% on 2026-11-05 (latest observation at read time) |

## 4. Gaps, irregularities and link repairs (published on the Flagged for Review page)

| ID | Item | Finding | Action |
|---|---|---|---|
| V-1 | Measure ULA thresholds | The 404 that forced earlier layers to flag Measure ULA is resolved: the official Office of Finance FAQ is live and states $5,400,000 / $10,900,000 with 4% / 5.5% for closings after 2026-06-30. | Verified and available for publication; earlier layers that still show $5.0m / $10.0m are stale. |
| V-2 | California minimum wage | The DIR page now states **$16.90/hour effective 2026-01-01** for all employers. The **$17.40/hour for 2027** figure reported elsewhere does **not** appear on that page. | $16.90 verified; $17.40 remains **unverified** and is not published. |
| V-3 | LA County documentary transfer tax | No official County page could be retrieved today (the Registrar-Recorder URL failed); the widely quoted $1.10 per $1,000 appears only in secondary sources on this pass. | Left **blank** and flagged; only the City of LA 0.45% base tax is published. |
| V-4 | LAUSD graduation / CAASPP | CDE DataQuest graduation-rate endpoints returned the DataQuest error page for the parameters tried; the Dashboard itself is an interactive application. | Enrollment and English-learner figures published from CDE; graduation rate left **blank**. |
| V-5 | USGS ShakeOut URL | `usgs.gov/programs/earthquake-hazards/science/shakeout-scenario` returns 404. The report host `pubs.usgs.gov/of/2008/1150/` serves the official document. | Link repaired to the publications warehouse; no value taken from the dead path. |
| V-6 | ZIMAS | The City planning application returns an empty application shell to a non-interactive fetch; no zoning fact can be read without a parcel. | Retained only as a research route; no value extracted. |
| V-7 | CDE hub page | `cde.ca.gov/ta/ac/cm/` is a navigation hub, not a performance dataset. A prior flag said the page was “inspected”; inspection confirms it contains no school-level result. | School-performance rows stay **blank**. |
| V-8 | BLS rolling document | The November 4, 2026 summary still reports September 2026 as its latest month; all published BLS cells match it. | No change needed; values remain as-of September 2026. |
| V-9 | County vs city divergence | County population is −3.2% from the 2020 estimates base while the city is −0.8%. Both are correctly labelled by geography; neither is a trade-area measure. | Published with geography labels intact. |
| V-10 | Anthropogenic context | The 2025 Palisades and Eaton fires destroyed 16,264 structures in Los Angeles County (6,845 + 9,419) within 24 days. This is context for insurance, labour and housing stress — not a probability for this parcel. | Published as a tail-risk context row with the CAL FIRE incident links. |

## 5. What this pass does **not** establish

- No parcel, address, owner, tenant entity, rent roll, lease, estoppel, debt or tax basis was available or sought.
  Nothing in this record should be read as a valuation of any specific property.
- No cap rate, sale price, renewal probability or expected return is asserted; no official publisher reports those
  for this asset.
- External link availability was checked on 2026-11-08 only. Rolling publications (BLS summary, QuickFacts) can be
  revised after that date.
- Automated checks (`scripts/validate.py`, `scripts/stage_pages.py`) verify provenance and link integrity, not the
  semantic truth of a publisher's statistic.
