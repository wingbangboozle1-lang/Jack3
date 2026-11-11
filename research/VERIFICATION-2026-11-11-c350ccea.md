# Line-by-line re-verification — 2026-11-11 (`c350ccea`)

**Scope:** every row published on the 12 curated pages plus the new question register.
**Method:** each value was opened on the publisher's own page on 2026-11-11 and compared with the
published cell: publisher, geography, period and measure. Nothing was carried over from an earlier
audit without being re-read. Where a page could not be read as served, the value is reported as
unverifiable — not as verified.

**Verdict:** one provenance defect found and fixed (LAUSD graduation rates), one rolling anchor
refreshed (10-year Treasury), one new rate observation added. Every other published value reproduced
exactly.

---

## 1. Sources re-read on 2026-11-11

| # | Source | URL | Result |
|---|---|---|---|
| 1 | U.S. Census QuickFacts — Los Angeles city (V2025) | https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225 | All 20 published city cells reproduce exactly |
| 2 | U.S. Census QuickFacts — Los Angeles County (V2025) | https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225 | Population 9,694,934; −3.2%; 65+ 17.1%; foreign-born 33.4% — all reproduce |
| 3 | BLS, Los Angeles Area Economic Summary (updated 2026-11-04) | https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf | All published labour, wage, CPI, ECI and spending cells reproduce |
| 4 | Jack in the Box Inc., Q3 FY2026 results (2026-08-12) | https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx | All 14 issuer cells reproduce (SSS −1.1%, systemwide −1.4%, 17 closures / 4 openings, 2,115 units, 149/1,966 split, revenue $257.7m −1.8%, margins 17.6% / 37.4% vs 39.3%, debt actions) |
| 5 | Jack in the Box Inc., "JACK on Track" (2025-04-23) | https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Unveils-JACK-on-Track-Plan-to-Improve-Long-Term-Financial-Performance/default.aspx | 150–200 closures, remainder on franchise termination dates, ~1%/yr from FY2026, real-estate sales for debt paydown — all reproduce |
| 6 | City of Los Angeles Office of Finance — Measure ULA FAQ | https://finance.lacity.gov/faq/measure-ula | 4% above $5,400,000, 5.5% at/above $10,900,000 for closings after 2026-06-30; base $2.25 per $500 (0.45%); Chained-CPI indexing; ULA on value, base tax on value net of liens — all reproduce |
| 7 | LA County Registrar-Recorder — Documentary Transfer Tax | https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info | $0.55 per $500 or fraction, consideration exclusive of qualifying liens; Los Angeles (effective 7/1/26) rows match the ULA thresholds — reproduces |
| 8 | LA County Assessor — Proposition 13 | https://assessor.lacounty.gov/real-estate-toolkit/proposition-13 | 1% general levy; 2% annual cap; reassessment on change of ownership / new construction; voter-approved add-ons — reproduces |
| 9 | IRS — Topic no. 409 | https://www.irs.gov/taxtopics/tc409 | 0/15/20% long-term brackets; 25% maximum on unrecaptured §1250 gain — reproduces |
| 10 | California FTB — Capital gains and losses | https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html | "California does not have a lower rate for capital gains. All capital gains are taxed as ordinary income." — reproduces |
| 11 | California DIR — Fast Food Minimum Wage FAQ | https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm | $20.00/hour from 2024-04-01 for covered fast-food employees — reproduces |
| 12 | California DIR — Minimum Wage FAQ | https://www.dir.ca.gov/dlse/FAQ_MinimumWage.htm | $16.90/hour from 2026-01-01; no 2027 rate stated (confirms the existing flag) — reproduces |
| 13 | CAL FIRE — Palisades Fire | https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire | 23,448 acres; 6,845 structures destroyed; 100% contained 2025-01-31 after 24 days — reproduces |
| 14 | CAL FIRE — Eaton Fire | https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire | 14,021 acres; 9,419 structures destroyed; 19 civilian fatalities; 24 days — reproduces |
| 15 | USGS/CGS — The ShakeOut Scenario, OFR 2008-1150 | https://pubs.usgs.gov/of/2008/1150/ | M7.8 southern San Andreas scenario: ~1,800 deaths, ~$213bn economic losses, stated as a scenario that "may never happen" — reproduces |
| 16 | CA Dept. of Finance — Public K-12 Graded Enrollment, 2026 series | https://dof.ca.gov/forecasting/demographics/public-k-12-graded-enrollment/ | 5,731,300 (2025-26) → 5,020,800 (2035-36), −710,500; LA County −240,800; graduates 453,600 → 381,300 — reproduces |
| 17 | LA County — 2026 Assessment Roll release (2026-07-14) | https://lacounty.gov/2026/07/14/la-county-property-values-surpass-2-2-trillion/ | $2.272tn; +$96bn or 4.42%; Los Angeles city $926.1bn; the "42%" bullet typo is present on the page — reproduces, typo unresolved |
| 18 | LA Metro (The Source) — Games mobility funding | https://thesource.metro.net/congress-approves-94-3-million-for-los-angeles-2028-olympic-and-paralympic-games-transportation/ | $94.3m for the 2028 Games; $149m Vermont BRT in the same bill — reproduces |
| 19 | CA Dept. of Education — LAUSD district profile (2025-26) | https://www.cde.ca.gov/sdprofile/details.aspx?cds=19647330000000 | Enrollment 497,105; English learners 81,328 (16.4%) — reproduces |
| 20 | CA Dept. of Education — Largest & smallest districts | https://www.cde.ca.gov/ds/ad/ceflargesmalldist.asp | LAUSD rank 1 at 497,105; San Diego Unified 112,250; statewide 5,731,260 — reproduces |
| 21 | California School Dashboard 2026 — LAUSD academic engagement | https://www.caschooldashboard.org/reports/19647330000000/2026/academic-engagement | **Could not be read.** The served page contains no indicator values; the tables are rendered client-side. The published 86.2% and 87.6% figures could not be re-verified. See §2. |
| 22 | CA Dept. of Education — DataQuest four-year cohort report, LAUSD 2025-26 | https://dq.cde.ca.gov/dataquest/dqcensus/CohRate.aspx?cds=1964733&agglevel=District&year=2025-26 | LAUSD 4-year ACGR **87.4%** (28,447 cohort / 24,857 graduates) with charter schools excluded by default; county 92.0%; statewide 92.8% on this page — new verified rows added |
| 23 | CA Dept. of Education — news release 26-44 (2026-10-15) | https://www.cde.ca.gov/nr/ne/yr26/yr26rel44.asp | Statewide four-year graduation rate **87.9%**, "the highest level in the past decade" — new verified row added |
| 24 | Federal Reserve Board — H.15, series DGS10 via FRED | https://fred.stlouisfed.org/series/DGS10 | 2026-11-06: 4.86; 2026-11-09: 4.88 (series updated 2026-11-10) — published cells dated, both now shown |

Also re-read for context, unchanged and not re-published as new values: FEMA Map Service Center
(https://msc.fema.gov/portal/home), CAL FIRE OSFM Fire Hazard Severity Zones
(https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones),
California Geological Survey earthquake zones (https://www.conservation.ca.gov/cgs/geohazards/eq-zapp),
ZIMAS (https://zimas.lacity.org/), IRS like-kind exchange guidance,
SCAG Connect SoCal updated tables PDF, and the issuer's FY2026 release notice.

## 2. The defect: LAUSD graduation figures (C-01)

The published rows, marked Verified, said **86.2% four-year** and **87.6% combined four/five-year**,
sourced to the 2026 California School Dashboard. On 2026-11-11 that page returned no values at all —
it is a JavaScript application, so neither figure could be read from the source as published.

What the official, server-rendered records say for the same school year:

| Measure | Value | Population | Source |
|---|---|---|---|
| LAUSD four-year adjusted cohort graduation rate | **87.4%** | Charter schools excluded (CDE default for district reports) | DataQuest, 2025-26 |
| Los Angeles County four-year ACGR | 92.0% | County total as printed on that report | DataQuest, 2025-26 |
| California four-year ACGR | 87.9% | Statewide, press release basis | CDE release 26-44 |
| California four-year ACGR | 92.8% | Statewide total as printed on the DataQuest report page | DataQuest, 2025-26 |

The two statewide figures (87.9% and 92.8%) differ because CDE's news release and the DataQuest report
page are computed on different cohort/aggregation bases. Both are quoted with their own publisher
attribution rather than reconciled here; a reader must not splice them.

**Action taken.** The 86.2% and 87.6% rows were changed to **Unverified with the value blank**, and the
prior figures are recorded only in the row's explanation. Two new Verified rows were added
(87.4% DataQuest; 87.9% CDE release). This follows the project rule that an unverified value is never
published as a number. It also removes the earlier claim that the graduation gap was "closed".

**What would close it.** Read the 2026 Dashboard in a browser with the district filter reset to all
schools, or use CDE's Graduation Rate Additional Report, which CDE states will carry 2026 data by
2026-12-15. Record the exact filter set alongside the value.

## 3. The rolling anchor: 10-year Treasury (C-02)

Published: 4.86% on 2026-11-06. Re-read 2026-11-11: the series now also shows **4.88% on 2026-11-09**
(the FRED page was last updated 2026-11-10). Both observations are now shown as dated values on the
economy, risk, taxes and model pages, and the projection module keeps 4.86% (2026-11-06) as its
disclosed discount-rate floor with the date attached. A dated observation does not become false when
the series moves, so the earlier value was not deleted.

## 4. Corrections made to repository housekeeping

| Item | Before | After |
|---|---|---|
| Snapshot stamp on every page | "10 Nov 2026" | "11 Nov 2026" |
| `data/evidence.json` → `reviewed` | 2026-11-10 | 2026-11-11 |
| Sources page audit pointer | pointed only at the 2026-11-10 record | points at this record, earlier audits retained |
| Home page gap link | went to the review page | goes to the new question register |
| Site page count claims | "nine pages", "twelve pages", "Ten/eleven pages" in older text | corrected where generated; the artifact is now 13 HTML pages plus CSS |
| `scripts/validate.py` | checked every `<tr>`, including header rows | checks body rows only, matching the artifact checker |

## 5. New verification gate

`tools/check_public.py` runs in CI immediately after staging and tests the **published artifact**, not
the repository. It fails on: an unexpected or missing file; a broken internal link; an external link
that is not https or not on the official allow-list; a body row without a registered source; an
"Unverified" row that carries a value in its Value column; an email, phone number, SSN-like or parcel-like
string; any script, iframe, form, tracker or `mailto:`; a registered source that no page uses; and a
question-register row with an unregistered source or an unknown status.

Current result: **13 pages, 244 body rows, 236 internal and 249 external links — all pass.**

## 6. What remains unverified after this pass

- Any sale price, market rent, cap rate or renewal probability for Asset A.
- The parcel's jurisdiction, zoning, drive-through legality, FEMA/CAL FIRE/CGS designations and insurance.
- Store-level sales, rent coverage, arrears and the legal obligor / guarantor.
- The executed lease, its exact expiry, options and notice dates; and whether 2030–2035 refers to the
  lease, an option window or a franchise agreement.
- School assignment and campus-level performance.
- The charter-inclusive LAUSD district rate (see §2) and the 4.42%/42% Assessment Roll typo.
- Post-2026-12-09 issuer results.

All of these are listed with a discovery route on `questions.html`.
