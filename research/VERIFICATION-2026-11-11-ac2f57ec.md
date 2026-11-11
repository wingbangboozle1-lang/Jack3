# Line-by-line verification record — 2026-11-11 (UTC)

**Session:** `ac2f57ec` · **Branch:** `arena/ac2f57ec-jack3` · **Base tree:** the merged PR #42 tree
(`b3fa7ae`, which already contained the 222-row canonical register from session `b98090a0`).

This file records **only what this session personally re-read on 2026-11-11**. It does not claim independent
re-verification of rows it did not open. Where a published value was checked, the exact text observed on the
official page is quoted below.

---

## 1. Sources re-read on 2026-11-11

| Key | Publisher | Official URL | Result |
|---|---|---|---|
| FRED | Federal Reserve H.15 via FRED | https://fred.stlouisfed.org/series/DGS10 | **New observation.** Page reports `2026-11-09: 4.88`, updated Nov 10 2026 3:16 PM CST. Prior rows `2026-11-06: 4.86`, `2026-11-05: 4.84`. Anchor refreshed to 4.88% / 2026-11-09. |
| BLS | U.S. Bureau of Labor Statistics | https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf | **Reproduces.** Updated November 04, 2026. Unemployment Sep-26: US 4.0, CA 5.1, LA metro 4.4, LA County 4.5, LA city 4.5 (Sep-25: 4.3 / 5.6 / 5.5 / 5.9 / 5.9). Total nonfarm 6,282.1 thousand, +30.2 thousand, +0.5%. Education & health 1,340.7 thousand, +3.8%. Information 187.0 thousand, −5.7%. Leisure & hospitality 782.0 thousand, +1.5%. Government 734.8, −1.1%. Average weekly wage Q1 2026 LA County 1,704. CPI-U all items +3.7%, Food +2.8%, Energy +20.3%. ECI Sep-26 LA-Long Beach CSA +3.9%, US +3.1%. All-industry average hourly wage May 2025 $37.15. |
| BLS | BLS Western Information Office | https://www.bls.gov/regions/west/news-release/consumerpriceindex_losangeles.htm | **New, re-read.** CPI-U Los Angeles-Long Beach-Anaheim, October 2026 release dated November 10, 2026, series `CUURS49ASA0`. Sep 2026 index 358.725, Oct 2026 360.965. 12-month change is *not published* for October 2026 because October 2025 data were not collected during the lapse in appropriations — noted, not used to fill a gap. |
| CITY | U.S. Census Bureau | https://www.census.gov/quickfacts/losangelescitycalifornia | **Reproduces.** 3,869,089 (V2025); estimates base 3,899,342; change −0.8%; 2020 Census 3,898,747; density 8,304.2/sq mi (2020); land area 469.49 sq mi; mean travel time 30.7 min; median household income $81,939; per capita $47,685; poverty 16.5%; retail sales 2022 $81,351,523 thousand; retail sales per capita $21,281; total employer establishments `X` (not published at city level — the inherited register correctly leaves the city building-permit row blank). |
| COUNTY | U.S. Census Bureau | https://www.census.gov/quickfacts/losangelescountycalifornia | **Reproduces.** 9,694,934 (V2025); base 10,017,414; change −3.2%; 2020 Census 10,014,009; density 2,466.9/sq mi; land area 4,059.28 sq mi; mean travel time 30.4 min; median household income $90,112; per capita $45,792; poverty 13.3%; foreign-born 33.4%; under 18 19.2%; 65+ 17.1%; Hispanic or Latino 49.3%; retail sales 2022 213,932,785 thousand; retail per capita $22,010; employer establishments 304,988; total employment 3,987,736; employment change 2022-2023 2.3%. |
| DOFPROJ | CA Department of Finance | https://dof.ca.gov/forecasting/demographics/public-k-12-graded-enrollment/ | **New rows.** 2026 Series, August 2026. State enrollment 5,731,300 in 2025-26, falling 710,500 to 5,020,800 by 2035-36. Los Angeles County falls by **240,800** pupils by 2035-36. Graduates fall from 453,600 (2024-25) to 381,300 by 2035-36. Method stated: grade progression ratio / cohort survival. |
| ULA | City of Los Angeles Office of Finance | https://finance.lacity.gov/faq/measure-ula | **Reproduces.** Effective for closings after June 30, 2026 the thresholds are $5,400,000 and $10,900,000; 4% above $5.4m and 5.5% at or above $10.9m. Base tax 0.45% ($2.25 per $500). Table reproduces 0.45% / 4.45% / 5.95%. ULA effective April 1, 2023. Thresholds indexed to the BLS **Chained** CPI. |
| DTT | LA County Registrar-Recorder/County Clerk | https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info | **Reproduces.** $0.55 per $500 on consideration/value **exclusive of liens remaining at time of sale**. Los Angeles row "Effective 7/1/26": $2.25 per $500 **and either** 4% above $5.4m but under $10.9m **or** 5.5% at or above $10.9m. County rate for the five special cities is computed at the full $1.10 per $1,000. |
| ASSESSOR | LA County Assessor | https://assessor.lacounty.gov/real-estate-toolkit/proposition-13 | **Reproduces.** General levy limited to 1% of assessed value; assessed value cannot increase more than 2% a year except on change in ownership, new construction, a Proposition 8 temporary decline, or Mills Act designation; voter-approved indebtedness and direct assessments are additional. |
| SECQ3 | SEC EDGAR / issuer 8-K Ex. 99.1 | https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm | **Reproduces.** Same-store sales −1.1% (company −0.9%, franchise −1.2%, prior year −7.1%); systemwide sales −1.4%; 4 openings, 17 closures; 2,115 restaurants (149 company / 1,966 franchise); franchise-level margin $60.3m or 37.4% vs $66.2m or 39.3%, with **higher bad-debt expense** cited; total revenues $257.7m, −1.8%; Adjusted EBITDA $61.2m; Del Taco sale completed December 22, 2025. The release carries named IR contact details — **not reproduced anywhere in this repository's published pages**. |
| DIRFF | CA Dept of Industrial Relations | https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm | **Reproduces.** From April 1, 2024 covered fast-food employees must be paid at least $20.00/hour (AB 1228). Applies to franchisees (Q19). A local general minimum wage higher than the fast-food floor would govern. |
| DIRMW | CA Dept of Industrial Relations | https://www.dir.ca.gov/dlse/FAQ_MinimumWage.htm | **Reproduces.** Effective January 1, 2026 the state minimum wage is $16.90/hour. The 2027 rate is **not** stated on the page — the inherited F-11 flag stands. |
| IRS409 | Internal Revenue Service | https://www.irs.gov/taxtopics/tc409 | **Reproduces.** Thresholds quoted for taxable years beginning in **2025** (0% ≤ $48,350 / $96,700 / $64,750; 15% bands; 20% above). Unrecaptured §1250 gain max 25%; collectibles 28%; NIIT referenced. The 2025 vintage is flagged (F-16) and not silently updated. |
| IRS1031 | Internal Revenue Service | https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips | **Reproduces, with a scope correction.** Confirms real property only (TCJA), like-kind definition, US-only, Form 8824. **It does not state the 45/180-day deadlines.** Those were moved to the correct source, below. |
| IRS8824 | Internal Revenue Service | https://www.irs.gov/pub/irs-pdf/i8824.pdf | **New source, added because of the gap above.** 2026 Instructions for Form 8824, "Deferred Exchanges": replacement property must be **identified within 45 days** after the transfer and **received within 180 days, or by the due date of the return including extensions, whichever is earlier**; qualified intermediary safe harbour described. |
| BOE220 | CA State Board of Equalization | https://www.boe.ca.gov/proptaxes/pdf/220_0345.pdf | **Reproduces.** Annotations 220.0345: creation, termination or transfer of a leasehold with a term of 35 years or more (including renewal options) is a change in ownership; transfer of a **lessor's** interest subject to a lease with **35 years or more** remaining is **not** a change in ownership. Letter is advisory and not binding on a county assessor — stated on the page. |
| UCERF3 | U.S. Geological Survey | https://pubs.usgs.gov/fs/2015/3009/pdf/fs2015-3009.pdf | **Reproduces exactly.** Table 1, Los Angeles region: M≥5 100%, M≥6 96%, M≥6.7 **60%** (repeat 40 yr), M≥7 **46%** (61 yr), M≥7.5 **31%** (109 yr), M≥8 **7%** (532 yr). Southern California region: M≥6.7 **93%**. Narrative: greater-California M≥6.7 is near-certain (>99%); M≥8 is 7%, repeat 494 years. Every published earthquake row matches. |
| PALISADES | CAL FIRE | https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire | **Reproduces.** 23,448 acres; 6,845 structures destroyed; 975 damaged; **12** confirmed civilian fatalities; 3 civilian injuries; 1 firefighter injury; started 01/07/2025 10:30, contained 01/31/2025 10:48 (**active 24 days**); cause arson; jurisdiction LA City Fire Department. |
| EATON | CAL FIRE | https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire | **Reproduces.** 14,021 acres; 9,419 structures destroyed; 1,076 damaged; **19** confirmed civilian fatalities; 9 firefighter injuries; contained 01/31/2025 10:48 (active 24 days); cause electrical. Derived row 6,845 + 9,419 = **16,264** confirmed. |
| CDEPROF | CA Dept of Education | https://www.cde.ca.gov/sdprofile/details.aspx?cds=19647330000000 | **Reproduces.** Los Angeles Unified, CDS 19 64733 0000000, school year 2025-26: enrollment **497,105**; English learners **81,328 (16.4%)**. The page also carries a named superintendent — **not reproduced on the published site**. |

## 2. Corrections made in this session

1. **Treasury anchor refreshed** from 4.86% (2026-11-06) to **4.88% (2026-11-09)**, read directly off FRED. The
   earlier observations are retained as an audit trail in the flag text rather than deleted.
2. **§1031 deadline citation corrected.** The 45-day / 180-day rule was cited to the IRS *real estate tax tips*
   page, which does **not** contain it. The claim is retained but re-cited to the **Instructions for Form 8824**
   (2026), which states it verbatim. This is recorded rather than silently re-pointed because a link that does
   not support its claim is exactly the failure mode this project is meant to catch.
3. **Statewide enrollment discrepancy flagged as F-23.** CDE reports **5,731,260** (Census Day 2025-26); CA DOF
   reports **5,731,300** for the same year. Both are published with their publisher; neither is averaged.
4. **New flag F-24** records that the scenario model's outputs are arithmetic on disclosed assumptions, are
   labelled `ANALYSIS`, and move materially with the entry cap alone (0.907 to 1.323).
5. **Added a rule that model inputs cannot be misrepresented**: the scenario engine's discount-rate grid is
   anchored on a *verified* Treasury observation, and every other input is labelled `ASSUMPTION` on the page.

## 3. What this session did NOT verify

- The 27 inherited sources it did not open (BEA, SCAG, ZIMAS, FEMA MSC, FHSZ, EQ Zapp, NRI, FTB, BOE800,
  CDELARGE, DASH, CDEEOY, CDEACGR, SHAKEOUT, IR25, SEC10K). Their rows remain as published by session
  `b98090a0` and are **not** claimed as independently re-verified here.
- Any parcel-level fact. There is no address, parcel number, lease or rent, so no parcel fact could be checked.
- Any cap rate, sale price, rent, NOI, basis or debt figure. None exists in the public record.

## 4. Automated gates run after the changes

```
python3 scripts/build_canonical.py     # 22 pages, 224 rows, 36 sources
python3 scripts/validate.py            # PASS: provenance, links, PII, determinism
python3 scripts/stage_pages.py         # PASS: 23-file artifact, every row sourced
python3 tools/check_site.py            # ALL CHECKS PASSED
python3 tools/linkcheck.py             # 0 broken internal links/anchors
python3 tools/check_links.py           # every verified link on an official/primary domain
python3 tools/pii_scan.py              # 0 findings
python3 _advisory_src/verify_advisory.py   # PASS
python3 _dashboard_src/verify.py           # PASS
python3 scripts/scenario_engine.py     # SELF-TEST PASS (closed form vs brute force; break-evens invert)
```

## 5. Privacy statement for this session

No personal information was collected, inferred or published. Official pages consulted on 2026-11-11 contain
named individuals (an issuer investor-relations contact, a CDE district superintendent, an LA Metro regional
commissioner in the CPI release byline) and real street addresses (assessor office locations, disaster recovery
centres). **None of it is reproduced** in any published page, dataset or log. The subject property remains
`Asset A` with no address, parcel number, rent, basis or debt anywhere in the repository's published output.
