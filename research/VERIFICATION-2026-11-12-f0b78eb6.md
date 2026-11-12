# Line-by-line verification record — 2026-11-12 (UTC)

**Session:** `f0b78eb6` (branch `arena/f0b78eb6-jack3`)
**Canonical snapshot:** `2026-11-12`
**Scope:** 230 canonical evidence rows (199 `Verified`, 4 `Derived`, 1 `Analysis`, 26 `Blank`), 40 official/issuer sources, 22 published HTML pages (21 registered + `flagged.html` alias), plus `assets/style.css` (23-file Pages artifact).

## Executive verification summary

Every external official source in the canonical register (`36` inherited sources plus `4` newly verified official/issuer sources) was independently fetched and inspected on **2026-11-12** using `fetch_page`. Every numeric value, date, geography, unit, and vintage in `data/canonical_rows.py` was compared verbatim against the fetched source text, and every internal consistency check across `scripts/projection.py`, `scripts/build_canonical.py`, `README.md`, `EXECUTIVE_SUMMARY.md`, `VERIFY.md`, and `REPO_REVIEW.md` was verified.

### Corrections and verified gap closures applied on 2026-11-12

1. **Census QuickFacts V2025 date typo fixed (`data/canonical_rows.py`):** Los Angeles city (`3,869,089`) and Los Angeles County (`9,694,934`) V2025 population rows previously said `2026-07-01 estimate (V2025)` instead of `2025-07-01 estimate (V2025)`, contradicting the fetched QuickFacts tables (`Population estimates, July 1, 2025, (V2025)`). Fixed to `2025-07-01 estimate (V2025)`.
2. **City of Los Angeles general minimum wage verified (`LAMWO`, closing `F-12`):** Direct fetch of `https://wagesla.lacity.gov/` and the official Office of Wage Standards rate-increase memo confirmed **$18.42 / hour effective 2026-07-01** (CPI-W indexed, up from `$17.87/hour` effective `2025-07-01`). Replaced the prior `Blank` row with a `Verified` row and marked `F-12` `Closed`. AB 1228's `$20.00/hour` fast-food floor remains applicable to covered limited-service chains.
3. **FY2025 Form 10-K (`SEC10K`) Item 2, Item 7 & Note 8 verified and closed:** Direct inspection of `jack-20250928.htm` (period ended `2025-09-28`) verified verbatim:
   - **California footprint (Item 2):** `941` of `2,136` Jack in the Box units (`44.1%`; `96` company-operated, `845` franchised); Item 7 reports ~`7.6%` FY2025 company-operated wage inflation driven primarily by California AB 1228.
   - **Property tenure split (Item 2):** `164` company-owned buildings on company-owned land (`8` co-op / `156` franchise), `565` company-owned buildings on leased land (`55` / `510`), `1,020` company-leased buildings on leased land (`87` / `933`), and `387` franchise directly-owned or directly-leased units (`2,136` total; `729` company-owned buildings; `1,585` company-leased land sites).
   - **Contingent / percentage rent (Item 2):** approximately `13%` of Jack in the Box leases provide contingent rent (`1%–10%` of gross sales above thresholds).
   - **Franchise AUV (Item 7):** `$1,874 thousand` in FY2025 vs `$1,949 thousand` in FY2024 (`-3.8%` YoY).
   - **Lessee / lessor terms (Note 8 & Note 3):** consolidated GAAP operating-lease weighted-average remaining term `11.2 years` (`6.1%` weighted-average discount rate); `$245,062 thousand` leased vs `$16,859 thousand` owned base franchise operating lease income (`$105,355 thousand` variable; `$368,643 thousand` total franchise rental revenue); `$12,743 thousand` of franchise-leased properties classified held for sale in Note 3.
4. **Upcoming Q4 & FY2026 earnings release trigger verified (`IR26Q4`):** Direct fetch of the issuer's `2026-10-26` release confirmed Q4 & FY2026 results will be issued after market close on **2026-12-09** (5:00 p.m. ET webcast), reconfirming `2,115` systemwide stores across 25 states, Mexico, and Guam. Added to `Tenant & lease` and `F-24`. No executive or IR contact names are reproduced anywhere.
5. **Federal 2026 LTCG brackets verified (`IRSRP25`, updating `F-16`):** Direct fetch of IRS `Rev. Proc. 2025-32` § 4.03 (`rp-25-32.pdf`) verified finalized 2026 thresholds (`0%` max `$98,900` MFJ/SS, `$66,200` HoH, `$49,450` Unmarried/MFS, `$3,300` Estates/Trusts; `15%` max `$613,700` MFJ/SS, `$579,600` HoH, `$545,500` Unmarried, `$306,850` MFS, `$16,250` Estates/Trusts). IRS Topic 409 still displays 2025 thresholds (`IRS409` retained accurately), and `rp-26-35.pdf` (2027) still carries `[Release Date, 2026]` draft placeholders and remains withheld.
6. **FEMA National Risk Index portal status & archived baseline (`NRIDECK`, updating `F-18`):** Live `https://hazards.fema.gov/nri/` returned **HTTP 500** on `2026-11-12`; live portal county scores remain `Blank`. Added archived March 2023 NRI v1.19.0 LA County baseline (`#1` nationally, `$3.9B` EAL Value, `$5.3B` Risk Value, `CRF 1.36`) from official FEMA PrepToolkit (`preptoolkit.fema.gov`) with explicit vintage caveats.
7. **Repository code & documentation repairs (`R-24`):**
   - `scripts/projection.py`: aligned `TREASURY_ANCHOR` and `DISCOUNT_RATES[0]` from `0.0486` to `0.0488` matching the `2026-11-09` DGS10 comment (`F-25` marked `Closed`).
   - `scripts/build_canonical.py`: fixed duplicate `12A /` kicker collision (`decisions.html` moved to `12B / DECISION MATRIX`), fixed duplicate `an an` typo in `page_decisions()`, fixed hardcoded `20 static HTML pages` in `write_repo_review_md()` (`{len(PAGES) + 1}` = `22`), updated `page_model()` IRS note, expanded `page_suggestions()` with six concrete site/data/model proposals (`S-1`–`S-6`) plus trade-offs and review gates, and added `.sev.closed` styling.
   - `README.md`, `EXECUTIVE_SUMMARY.md`, and `VERIFY.md`: synchronized page/row/source counts (`22` HTML / `23`-file artifact, `230` rows, `40` sources), added missing `/questions.html` and `/suggestions.html` documentation entries, linked this `2026-11-12` audit record, and removed withdrawn rigid `24–36 month` and `≥10-year` mandates (`F-23`).

## Official source verification register (40 sources re-checked 2026-11-12)

| Key | Publisher | Title | URL | Fetch outcome (2026-11-12) |
|---|---|---|---|---|
| `CITY` | U.S. Census Bureau | Census QuickFacts · Los Angeles city (V2025) | https://www.census.gov/quickfacts/losangelescitycalifornia | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `COUNTY` | U.S. Census Bureau | Census QuickFacts · Los Angeles County (V2025) | https://www.census.gov/quickfacts/losangelescountycalifornia | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `BLS` | U.S. Bureau of Labor Statistics | Los Angeles Area Economic Summary · updated 2026-11-04 | https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `DOF` | California Department of Finance | July 2025 population estimates · revised release 2026-02-04 | https://dof.ca.gov/media/docs/forecasting/Demographics/estimates/July2025_Population_Estimates_Feb26_release.pdf | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `BEA` | U.S. Bureau of Economic Analysis | GDP by county and personal income by county, 2024 (BEA 26-08) | https://www.bea.gov/news/2026/gross-domestic-product-county-and-personal-income-county-2024 | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `SCAG` | Southern California Association of Governments | Connect SoCal 2024 · Demographics & Growth Forecast (adopted 2024-04-04) | https://www.scag.ca.gov/sites/default/files/2024-05/23-2987-tr-demographics-growth-forecast-final-040424.pdf | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `SECQ3` | U.S. Securities and Exchange Commission / issuer filing | Form 8-K Exhibit 99.1 · Q3 FY2026 results (quarter ended 2026-07-05) | https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `SEC10K` | U.S. Securities and Exchange Commission / issuer filing | FY2025 Form 10-K (fiscal year ended 2025-09-28) | https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `IR25` | Issuer investor relations | 'JACK on Track' plan announcement · 2025-04-23 | https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Unveils-JACK-on-Track-Plan-to-Improve-Long-Term-Financial-Performance/default.aspx | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `DIRFF` | California Department of Industrial Relations | Fast Food Minimum Wage FAQ (AB 1228) | https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `DIRMW` | California Department of Industrial Relations | Minimum Wage FAQ | https://www.dir.ca.gov/dlse/FAQ_MinimumWage.htm | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `ULA` | City of Los Angeles, Office of Finance | Real Property Transfer Tax and Measure ULA FAQ | https://finance.lacity.gov/faq/measure-ula | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `DTT` | Los Angeles County Registrar-Recorder / County Clerk | Documentary Transfer Tax · general information | https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `FRED` | Federal Reserve H.15 via Federal Reserve Bank of St. Louis FRED | 10-Year Treasury constant maturity yield (DGS10) | https://fred.stlouisfed.org/series/DGS10 | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `IRS409` | Internal Revenue Service | Topic no. 409 · Capital gains and losses | https://www.irs.gov/taxtopics/tc409 | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `IRS1031` | Internal Revenue Service | Like-kind exchanges · real estate tax tips | https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `FTB` | California Franchise Tax Board | Capital gains and losses (California treatment) | https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `ASSESSOR` | Los Angeles County Assessor | Proposition 13 | https://assessor.lacounty.gov/real-estate-toolkit/proposition-13 | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `BOE800` | California State Board of Equalization | Publication 800-10 · How property is assessed | https://boe.ca.gov/pdf/pub800-10.pdf | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `BOE220` | California State Board of Equalization | Property Tax Annotation 220.0345 · Leases | https://www.boe.ca.gov/proptaxes/pdf/220_0345.pdf | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `PALISADES` | CAL FIRE | Palisades Fire incident record (January 2025) | https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `EATON` | CAL FIRE | Eaton Fire incident record (January 2025) | https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `FHSZ` | CAL FIRE / Office of the State Fire Marshal | Fire Hazard Severity Zones | https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `SHAKEOUT` | U.S. Geological Survey | The ShakeOut Scenario · USGS OFR 2008-1150 | https://pubs.usgs.gov/of/2008/1150/ | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `UCERF3` | U.S. Geological Survey | UCERF3 · USGS Fact Sheet 2015-3009 | https://pubs.usgs.gov/fs/2015/3009/pdf/fs2015-3009.pdf | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `EQZAPP` | California Geological Survey | EQ Zapp · earthquake hazard zone application | https://www.conservation.ca.gov/cgs/geohazards/eq-zapp | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `FEMA` | Federal Emergency Management Agency | FEMA Flood Maps | https://www.fema.gov/flood-maps | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `NRI` | Federal Emergency Management Agency | National Risk Index | https://hazards.fema.gov/nri/ | HTTP 500 returned by live portal on 2026-11-12; live county score row retained Blank (`F-18`). |
| `ZIMAS` | Los Angeles City Planning | ZIMAS · planning and zoning information system | https://zimas.lacity.org/ | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `CDEPROF` | California Department of Education | District Profile · Los Angeles Unified (2025-26) | https://www.cde.ca.gov/sdprofile/details.aspx?cds=19647330000000 | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `CDELARGE` | California Department of Education | Largest & Smallest Public School Districts (2025-26) | https://www.cde.ca.gov/ds/ad/ceflargesmalldist.asp | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `DASH` | California Department of Education | California School Dashboard · Los Angeles Unified 2025 academic engagement | https://www.caschooldashboard.org/reports/19647330000000/2025/academic-engagement | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `CDEEOY` | California Department of Education | 2024-25 End-of-Year Reports | https://www.cde.ca.gov/ds/cm/dqeoy25.asp | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `GRAD2026` | California Department of Education | 2026 Graduation Rate Indicator · district data file | https://www3.cde.ca.gov/researchfiles/cadashboard/graddownload2026.txt | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `ACGR2026` | California Department of Education | DataQuest · Los Angeles Unified 2025-26 four-year ACGR | https://dq.cde.ca.gov/dataquest/dqcensus/CohRate.aspx?agglevel=District&cds=1964733&year=2025-26 | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `CDEACGR` | California Department of Education | Adjusted Cohort Graduation Rate data files | https://www.cde.ca.gov/ds/ad/filesacgr.asp | Fetched directly on 2026-11-12; canonical rows matched verbatim. |
| `LAMWO` | City of Los Angeles · Office of Wage Standards (Wages LA) | Minimum Wage Ordinance · July 2026 rate schedule | https://wagesla.lacity.gov/ | Fetched `wagesla.lacity.gov` & MWR memo PDF: `$18.42/hour` effective `2026-07-01` verified. |
| `IRSRP25` | Internal Revenue Service | Rev. Proc. 2025-32 · tax year 2026 inflation-adjusted items (§ 4.03) | https://www.irs.gov/pub/irs-drop/rp-25-32.pdf | Fetched `rp-25-32.pdf` chunks 0–2: § 4.03 finalized 2026 LTCG brackets verified (`rp-26-35.pdf` remains draft). |
| `NRIDECK` | Federal Emergency Management Agency · PrepToolkit | National Risk Index overview presentation (v1.19.0, March 2023) | https://www.preptoolkit.fema.gov/documents/d/caes/1d_national-risk-index-_sheehan?download=true | Fetched PDF deck (chunks 0–2): March 2023 v1.19.0 LA County metrics verified (`EAL $3.9B`, `Risk Value $5.3B`). |
| `IR26Q4` | Issuer investor relations | Q4 & FY2026 earnings release and webcast notice (2026-12-09) | https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Announces-Fourth-Quarter-and-Full-Year-2026-Earnings-Webcast/default.aspx | Fetched `2026-10-26` IR notice: `2026-12-09` webcast (`2,115` stores) verified; contact names excluded. |

## Row-by-row canonical register (230 rows)

| # | Category | Indicator | Value | Geography / Period | Status | Source |
|---:|---|---|---|---|---|---|
| 1 | Geography | Land area | 469.49 sq mi | Los Angeles city · 2020 | Verified | CITY |
| 2 | Geography | Population density | 8,304.2 per sq mi | Los Angeles city · 2020 | Verified | CITY |
| 3 | Geography | Land area | 4,059.28 sq mi | Los Angeles County · 2020 | Verified | COUNTY |
| 4 | Geography | Population density | 2,466.9 per sq mi | Los Angeles County · 2020 | Verified | COUNTY |
| 5 | Geography | Mean travel time to work | 30.7 minutes | Los Angeles city · workers 16+ · 2020-2024 | Verified | CITY |
| 6 | Geography | Mean travel time to work | 30.4 minutes | Los Angeles County · workers 16+ · 2020-2024 | Verified | COUNTY |
| 7 | Geography | Building permits | 22,250 | Los Angeles County · 2025 | Verified | COUNTY |
| 8 | Geography | Building permits | (Blank — intentionally empty) | Los Angeles city · 2025 | Blank | CITY |
| 9 | Geography | Subject parcel address, APN and census tract | (Blank — intentionally empty) | Asset A | Blank | ZIMAS |
| 10 | Geography | Whether the site lies inside the incorporated City of Los Angeles | (Blank — intentionally empty) | Asset A | Blank | ULA |
| 11 | Geography | Trade-area population, income and daytime workers | (Blank — intentionally empty) | Asset A | Blank | CITY |
| 12 | Geography | Zoning, entitlements, easements, redevelopment cost | (Blank — intentionally empty) | Asset A | Blank | ZIMAS |
| 13 | Geography | Competition, traffic counts, transit, crime, development pipeline | (Blank — intentionally empty) | Asset A | Blank | ZIMAS |
| 14 | Geography | Heat, air quality, contamination and insurability | (Blank — intentionally empty) | Asset A | Blank | FHSZ |
| 15 | Geography | Jurisdiction gate | Confirm the competent planning authority before applying any city rule | Asset A | Analysis | ZIMAS |
| 16 | People & income | Population | 3,869,089 | Los Angeles city · 2025-07-01 estimate (V2025) | Verified | CITY |
| 17 | People & income | Population estimates base | 3,899,342 | Los Angeles city · 2020-04-01 (V2025) | Verified | CITY |
| 18 | People & income | Population change | -0.8% | Los Angeles city · 2020 base to 2025-07-01 (V2025) | Verified | CITY |
| 19 | People & income | Decennial census population | 3,898,747 | Los Angeles city · 2020-04-01 | Verified | CITY |
| 20 | People & income | Population | 9,694,934 | Los Angeles County · 2025-07-01 estimate (V2025) | Verified | COUNTY |
| 21 | People & income | Population estimates base | 10,017,414 | Los Angeles County · 2020-04-01 (V2025) | Verified | COUNTY |
| 22 | People & income | Population change | -3.2% | Los Angeles County · 2020 base to 2025-07-01 (V2025) | Verified | COUNTY |
| 23 | People & income | Decennial census population | 10,014,009 | Los Angeles County · 2020-04-01 | Verified | COUNTY |
| 24 | People & income | Population (state estimate, revised) | 9,853,435 | Los Angeles County · 2025-07-01 · CA DOF Feb-2026 revision | Verified | DOF |
| 25 | People & income | Population change (state estimate) | -44,822 (-0.45%) | Los Angeles County · 2024-07-01 to 2025-07-01 · CA DOF | Verified | DOF |
| 26 | People & income | State population | 39,528,899 | California · 2025-07-01 · CA DOF | Verified | DOF |
| 27 | People & income | Households | 1,439,097 | Los Angeles city · 2020-2024 ACS | Verified | CITY |
| 28 | People & income | Households | 3,416,449 | Los Angeles County · 2020-2024 ACS | Verified | COUNTY |
| 29 | People & income | Persons per household | 2.61 | Los Angeles city · 2020-2024 ACS | Verified | CITY |
| 30 | People & income | Persons per household | 2.81 | Los Angeles County · 2020-2024 ACS | Verified | COUNTY |
| 31 | People & income | Median household income | $81,939 | Los Angeles city · 2020-2024 · 2024 dollars | Verified | CITY |
| 32 | People & income | Median household income | $90,112 | Los Angeles County · 2020-2024 · 2024 dollars | Verified | COUNTY |
| 33 | People & income | Per capita income | $47,685 | Los Angeles city · 2020-2024 · 2024 dollars | Verified | CITY |
| 34 | People & income | Per capita income | $45,792 | Los Angeles County · 2020-2024 · 2024 dollars | Verified | COUNTY |
| 35 | People & income | Persons in poverty | 16.5% | Los Angeles city · 2025 SAIPE estimate | Verified | CITY |
| 36 | People & income | Persons in poverty | 13.3% | Los Angeles County · 2025 SAIPE estimate | Verified | COUNTY |
| 37 | People & income | Owner-occupied housing rate | 36.0% | Los Angeles city · 2020-2024 ACS | Verified | CITY |
| 38 | People & income | Owner-occupied housing rate | 45.9% | Los Angeles County · 2020-2024 ACS | Verified | COUNTY |
| 39 | People & income | Median value, owner-occupied homes | $921,200 | Los Angeles city · 2020-2024 ACS | Verified | CITY |
| 40 | People & income | Median value, owner-occupied homes | $834,200 | Los Angeles County · 2020-2024 ACS | Verified | COUNTY |
| 41 | People & income | Median gross rent | $1,933 / month | Los Angeles city · 2020-2024 ACS | Verified | CITY |
| 42 | People & income | Median gross rent | $1,954 / month | Los Angeles County · 2020-2024 ACS | Verified | COUNTY |
| 43 | People & income | Foreign-born persons | 35.7% | Los Angeles city · 2020-2024 ACS | Verified | CITY |
| 44 | People & income | Foreign-born persons | 33.4% | Los Angeles County · 2020-2024 ACS | Verified | COUNTY |
| 45 | People & income | Persons under 18 | 19.2% | Los Angeles city · V2025 | Verified | CITY |
| 46 | People & income | Persons 65 and over | 14.2% | Los Angeles city · V2025 | Verified | CITY |
| 47 | People & income | Persons under 18 | 19.2% | Los Angeles County · V2025 | Verified | COUNTY |
| 48 | People & income | Persons 65 and over | 17.1% | Los Angeles County · V2025 | Verified | COUNTY |
| 49 | People & income | High school graduate or higher | 79.6% | Los Angeles city · age 25+ · 2020-2024 | Verified | CITY |
| 50 | People & income | High school graduate or higher | 80.9% | Los Angeles County · age 25+ · 2020-2024 | Verified | COUNTY |
| 51 | People & income | Bachelor's degree or higher | 38.5% | Los Angeles city · age 25+ · 2020-2024 | Verified | CITY |
| 52 | People & income | Bachelor's degree or higher | 36.0% | Los Angeles County · age 25+ · 2020-2024 | Verified | COUNTY |
| 53 | People & income | Language other than English at home | 56.4% | Los Angeles city · age 5+ · 2020-2024 | Verified | CITY |
| 54 | People & income | Civilian labor force participation | 66.4% | Los Angeles city · age 16+ · 2020-2024 | Verified | CITY |
| 55 | People & income | Civilian labor force participation | 64.7% | Los Angeles County · age 16+ · 2020-2024 | Verified | COUNTY |
| 56 | People & income | Total retail sales | $81.35bn ($81,351,523 thousand) | Los Angeles city · 2022 Economic Census | Verified | CITY |
| 57 | People & income | Retail sales per capita | $21,281 | Los Angeles city · 2022 | Verified | CITY |
| 58 | People & income | Accommodation and food services sales | $17.37bn ($17,366,966 thousand) | Los Angeles city · 2022 Economic Census | Verified | CITY |
| 59 | People & income | Accommodation and food services sales | $44.00bn ($44,000,801 thousand) | Los Angeles County · 2022 Economic Census | Verified | COUNTY |
| 60 | People & income | Total employer establishments | 304,988 | Los Angeles County · 2023 | Verified | COUNTY |
| 61 | People & income | Total employment | 3,987,736 | Los Angeles County · 2023 | Verified | COUNTY |
| 62 | People & income | Employment change 2022-2023 | +2.3% | Los Angeles County · County Business Patterns | Verified | COUNTY |
| 63 | People & income | Race-alone shares (city) | (Blank — intentionally empty) | Los Angeles city · V2025 | Blank | CITY |
| 64 | People & income | Hispanic or Latino | 49.3% | Los Angeles County · V2025 | Verified | COUNTY |
| 65 | Economy & jobs | Unemployment rate | 4.4% | Los Angeles metro · September 2026 · not seasonally adjusted | Verified | BLS |
| 66 | Economy & jobs | Unemployment rate | 4.5% | Los Angeles County · September 2026 · not seasonally adjusted | Verified | BLS |
| 67 | Economy & jobs | Unemployment rate | 4.5% | Los Angeles city · September 2026 · not seasonally adjusted | Verified | BLS |
| 68 | Economy & jobs | Unemployment rate | 5.1% | California · September 2026 · not seasonally adjusted | Verified | BLS |
| 69 | Economy & jobs | Unemployment rate | 4.0% | United States · September 2026 · not seasonally adjusted | Verified | BLS |
| 70 | Economy & jobs | Unemployment rate, prior year | 5.5% / 5.9% / 5.9% | Metro / County / City · September 2025 | Verified | BLS |
| 71 | Economy & jobs | Total nonfarm employment | 6,282.1 thousand | Los Angeles metro · September 2026 | Verified | BLS |
| 72 | Economy & jobs | Nonfarm employment change | +30.2 thousand (+0.5%) | Los Angeles metro · Sep 2025 to Sep 2026 | Verified | BLS |
| 73 | Economy & jobs | Education and health services employment | 1,340.7 thousand (+3.8%) | Los Angeles metro · September 2026 | Verified | BLS |
| 74 | Economy & jobs | Leisure and hospitality employment | 782.0 thousand (+1.5%) | Los Angeles metro · September 2026 | Verified | BLS |
| 75 | Economy & jobs | Information employment change | -5.7% | Los Angeles metro · 12-month change to Sep 2026 | Verified | BLS |
| 76 | Economy & jobs | Manufacturing employment change | -1.2% | Los Angeles metro · 12-month change to Sep 2026 | Verified | BLS |
| 77 | Economy & jobs | Financial activities employment change | -1.7% | Los Angeles metro · 12-month change to Sep 2026 | Verified | BLS |
| 78 | Economy & jobs | Professional and business services change | -0.5% | Los Angeles metro · 12-month change to Sep 2026 | Verified | BLS |
| 79 | Economy & jobs | Government employment change | -1.1% | Los Angeles metro · 12-month change to Sep 2026 | Verified | BLS |
| 80 | Economy & jobs | Average weekly wages, all industries | $1,704 | Los Angeles County · Q1 2026 · QCEW | Verified | BLS |
| 81 | Economy & jobs | Average hourly wage, all occupations | $37.15 | Los Angeles metro · May 2025 · OEWS | Verified | BLS |
| 82 | Economy & jobs | Employment Cost Index, wages and salaries | +3.9% | Los Angeles-Long Beach CSA · 12 months to Sep 2026 | Verified | BLS |
| 83 | Economy & jobs | CPI-U, all items | +3.7% | Los Angeles metro · 12 months to Sep 2026 | Verified | BLS |
| 84 | Economy & jobs | CPI-U, food | +2.8% | Los Angeles metro · 12 months to Sep 2026 | Verified | BLS |
| 85 | Economy & jobs | CPI-U, energy | +20.3% | Los Angeles metro · 12 months to Sep 2026 | Verified | BLS |
| 86 | Economy & jobs | Consumer spending · West region | Housing $33,016 · food $12,447 · transport $14,110 | West region · 2025 average annual expenditures | Verified | BLS |
| 87 | Economy & jobs | State minimum wage | $16.90 / hour from 2026-01-01 | California · DIR | Verified | DIRMW |
| 88 | Economy & jobs | State minimum wage from 2027-01-01 | (Blank — intentionally empty) | California · DIR | Blank | DIRMW |
| 89 | Economy & jobs | Covered fast-food minimum wage (AB 1228) | $20.00 / hour from 2024-04-01 | California · DIR | Verified | DIRFF |
| 90 | Economy & jobs | AB 1228 applies to franchisees | Yes | California · DIR | Verified | DIRFF |
| 91 | Economy & jobs | City of Los Angeles general minimum wage | $18.42 / hour from 2026-07-01 | City of Los Angeles · Wages LA (CPI-W indexed) | Verified | LAMWO |
| 92 | Economy & jobs | 10-year Treasury constant maturity yield | 4.84% | United States · 2026-11-05 · daily | Verified | FRED |
| 93 | Economy & jobs | 10-year Treasury constant maturity yield | 4.88% | United States · 2026-11-09 · daily (latest shown) | Verified | FRED |
| 94 | Economy & jobs | 10-year Treasury constant maturity yield | 4.90% | United States · 2026-11-04 · daily | Verified | FRED |
| 95 | Economy & jobs | Total personal income | $818.5 billion | Los Angeles County · 2024 · current dollars | Verified | BEA |
| 96 | Economy & jobs | Metropolitan-area GDP / personal income publication | Discontinued with the 2024 county release | United States · BEA | Verified | BEA |
| 97 | Economy & jobs | Total employment (regional forecast) | 8,937 thousand (2022) → 10,276 thousand (2050) | SCAG six-county region · Connect SoCal 2024 adopted forecast | Verified | SCAG |
| 98 | Economy & jobs | Annual employment growth (regional forecast) | +0.50% per year (2022-2050) | SCAG six-county region · Connect SoCal 2024 adopted forecast | Verified | SCAG |
| 99 | Economy & jobs | Accommodation and food service jobs (regional forecast) | 832 thousand (2022) → 938 thousand (2050), +12.8% | SCAG six-county region · Connect SoCal 2024 adopted forecast | Verified | SCAG |
| 100 | Economy & jobs | Population (regional forecast) | 18,827,000 (2019) → 20,909,000 (2050) | SCAG six-county region · Connect SoCal 2024 adopted forecast | Verified | SCAG |
| 101 | Economy & jobs | Population peak (historical estimate) | 18,966,261 (January 2019) | SCAG six-county region · CA DOF estimate cited in adopted forecast | Verified | SCAG |
| 102 | Economy & jobs | Market cap rate for single-tenant net-leased restaurants | (Blank — intentionally empty) | Asset A | Blank | FRED |
| 103 | Schools | District enrollment | 497,105 | Los Angeles Unified · 2025-26 Census Day | Verified | CDEPROF |
| 104 | Schools | English learners | 81,328 (16.4%) | Los Angeles Unified · 2025-26 | Verified | CDEPROF |
| 105 | Schools | Rank by enrollment | 1st in California | Los Angeles Unified · 2025-26 | Verified | CDELARGE |
| 106 | Schools | Second-largest district enrollment | 112,250 | San Diego Unified · 2025-26 | Verified | CDELARGE |
| 107 | Schools | Statewide public enrollment | 5,731,260 | California · 2025-26 | Verified | CDELARGE |
| 108 | Schools | Combined four-/five-year graduation rate | 87.6% | Los Angeles Unified · 2026 Dashboard | Verified | GRAD2026 |
| 109 | Schools | Four-year adjusted cohort graduation rate (ACGR) | 87.4% | Los Angeles Unified · 2025-26 DataQuest | Verified | ACGR2026 |
| 110 | Schools | Graduation rate · prior years | 82.1% (2019) · 86.0% (2022) · 83.6% (2023) · 86.7% (2024) | Los Angeles Unified · Dashboard by-year series | Verified | DASH |
| 111 | Schools | Four-year graduation rate, English learners | 64.1% | Los Angeles Unified · 2025 Dashboard | Verified | DASH |
| 112 | Schools | Chronic absenteeism | 21.9% (2025) | Los Angeles Unified · Dashboard | Verified | DASH |
| 113 | Schools | Statewide four-year ACGR | 87.5% | California · 2024-25 | Verified | CDEEOY |
| 114 | Schools | Statewide five-year graduation rate | 88.7% | California · 2024-25 | Verified | CDEEOY |
| 115 | Schools | Statewide chronic absenteeism | 19.4% | California · 2024-25 | Verified | CDEEOY |
| 116 | Schools | Statewide suspension rate | 2.9% | California · 2024-25 | Verified | CDEEOY |
| 117 | Schools | Assigned public schools for the subject parcel | (Blank — intentionally empty) | Asset A | Blank | CDEACGR |
| 118 | Schools | School-level performance measures | (Blank — intentionally empty) | Asset A | Blank | DASH |
| 119 | Tenant & lease | System same-store sales | -1.1% | Issuer systemwide · 12 weeks ended 2026-07-05 | Verified | SECQ3 |
| 120 | Tenant & lease | Franchise same-store sales | -1.2% | Issuer systemwide · Q3 FY2026 | Verified | SECQ3 |
| 121 | Tenant & lease | Company-operated same-store sales | -0.9% | Issuer systemwide · Q3 FY2026 | Verified | SECQ3 |
| 122 | Tenant & lease | System same-store sales, prior-year quarter | -7.1% | Issuer systemwide · Q3 FY2025 | Verified | SECQ3 |
| 123 | Tenant & lease | Systemwide sales change | -1.4% | Issuer systemwide · Q3 FY2026 | Verified | SECQ3 |
| 124 | Tenant & lease | Total restaurants at quarter end | 2,115 | Issuer systemwide · Q3 FY2026 | Verified | SECQ3 |
| 125 | Tenant & lease | Company-operated restaurants | 149 | Issuer systemwide · Q3 FY2026 | Verified | SECQ3 |
| 126 | Tenant & lease | Franchised restaurants | 1,966 | Issuer systemwide · Q3 FY2026 | Verified | SECQ3 |
| 127 | Tenant & lease | Openings in the quarter | 4 | Issuer systemwide · Q3 FY2026 | Verified | SECQ3 |
| 128 | Tenant & lease | Closures in the quarter | 17 | Issuer systemwide · Q3 FY2026 | Verified | SECQ3 |
| 129 | Tenant & lease | Net restaurant change in the quarter | -13 | Issuer systemwide · Q3 FY2026 | Verified | SECQ3 |
| 130 | Tenant & lease | Total revenues | $257.657 million (-1.8%) | Issuer consolidated · Q3 FY2026 | Verified | SECQ3 |
| 131 | Tenant & lease | Restaurant-level margin (non-GAAP) | 17.6% | Issuer company restaurants · Q3 FY2026 | Verified | SECQ3 |
| 132 | Tenant & lease | Franchise-level margin (non-GAAP) | 37.4% (from 39.3%) | Issuer · Q3 FY2026 | Verified | SECQ3 |
| 133 | Tenant & lease | Franchise rental revenues | $242.526 million | Issuer · 40 weeks ended 2026-07-05 | Verified | SECQ3 |
| 134 | Tenant & lease | Franchise rental revenues, prior-year period | $260.254 million | Issuer · 40 weeks ended 2025-07-06 | Verified | SECQ3 |
| 135 | Tenant & lease | Franchise rental revenue change | -6.8% | Issuer · 40 weeks year over year | Derived | SECQ3 |
| 136 | Tenant & lease | Franchise occupancy expenses | $166.043 million | Issuer · 40 weeks ended 2026-07-05 | Verified | SECQ3 |
| 137 | Tenant & lease | Bad-debt expense | Higher year over year (no amount stated) | Issuer · Q3 FY2026 | Verified | SECQ3 |
| 138 | Tenant & lease | Prepayment of securitised notes | $110.0 million · Series 2019-1 Class A-2-II | Issuer · Q3 FY2026 | Verified | SECQ3 |
| 139 | Tenant & lease | New securitised notes | $500 million · Series 2026-1 Class A-2 (anticipated repayment May 2031) | Issuer · Q3 FY2026 | Verified | SECQ3 |
| 140 | Tenant & lease | FY2026 guidance · restaurant count | approximately 2,100 | Issuer systemwide · FY ending 2026-09-27 | Verified | SECQ3 |
| 141 | Tenant & lease | FY2026 guidance · closures | approximately 50 to 60, mostly franchised | Issuer systemwide · FY2026 | Verified | SECQ3 |
| 142 | Tenant & lease | FY2026 guidance · openings | approximately 25 | Issuer systemwide · FY2026 | Verified | SECQ3 |
| 143 | Tenant & lease | FY2026 guidance · Adjusted EBITDA | $225 - $230 million | Issuer consolidated · FY2026 | Verified | SECQ3 |
| 144 | Tenant & lease | FY2026 guidance · SG&A | $112 - $115 million | Issuer consolidated · FY2026 | Verified | SECQ3 |
| 145 | Tenant & lease | Dividend and share repurchase programme | Discontinued | Issuer · stated in Q3 FY2026 release | Verified | SECQ3 |
| 146 | Tenant & lease | 2025 block closure programme | approximately 150-200 underperforming restaurants | Issuer plan announced 2025-04-23 | Verified | IR25 |
| 147 | Tenant & lease | 2025 plan · near-term closures | approximately 80-120 by 2025-12-31 | Issuer plan announced 2025-04-23 | Verified | IR25 |
| 148 | Tenant & lease | 2025 plan · timing of remaining closures | Tied to franchise agreement termination dates | Issuer plan announced 2025-04-23 | Verified | IR25 |
| 149 | Tenant & lease | Ongoing closure rate from FY2026 | approximately 1% of system units annually | Issuer plan announced 2025-04-23 | Verified | IR25 |
| 150 | Tenant & lease | Issuer real-estate strategy | Sell select owned real estate; direct proceeds to debt paydown | Issuer plan announced 2025-04-23 | Verified | IR25 |
| 151 | Tenant & lease | Del Taco divestiture | Completed 2025-12-22; reported as discontinued operations | Issuer · Q3 FY2026 release | Verified | SECQ3 |
| 152 | Tenant & lease | Geographic footprint | 25 states, Mexico and Guam | Issuer systemwide · Q3 FY2026 | Verified | SECQ3 |
| 153 | Tenant & lease | Exact expiration and notice deadlines | (Blank — intentionally empty) | Asset A | Blank | SECQ3 |
| 154 | Tenant & lease | Legal tenant, guarantor and financial coverage | (Blank — intentionally empty) | Asset A | Blank | SECQ3 |
| 155 | Tenant & lease | Rent, escalations, options, landlord obligations | (Blank — intentionally empty) | Asset A | Blank | SECQ3 |
| 156 | Tenant & lease | Store profitability, arrears, renewal intention | (Blank — intentionally empty) | Asset A | Blank | SECQ3 |
| 157 | Tenant & lease | California concentration (Jack in the Box) | 941 restaurants (96 company, 845 franchise) of 2,136 | Issuer systemwide · FY2025 10-K Item 2 (2025-09-28) | Verified | SEC10K |
| 158 | Tenant & lease | Property tenure split (Jack in the Box) | 164 co-owned land & bldg; 565 co-owned bldg on leased land; 1,020 co-leased land & bldg; 387 franchise owned/leased | Issuer systemwide · FY2025 10-K Item 2 (2025-09-28) | Verified | SEC10K |
| 159 | Tenant & lease | Percentage-rent leases across system | approximately 13% of Jack in the Box leases (1%–10% of gross sales) | Issuer · FY2025 10-K Item 2 | Verified | SEC10K |
| 160 | Tenant & lease | Franchise average unit volume (AUV) | $1,874 thousand (FY2025 vs $1,949 thousand in FY2024) | Issuer Jack in the Box franchise system · FY2025 10-K Item 7 | Verified | SEC10K |
| 161 | Tenant & lease | Portfolio operating lease weighted-average remaining term | 11.2 years (6.1% weighted-average discount rate) | Issuer lessee portfolio · FY2025 10-K Note 8 (2025-09-28) | Verified | SEC10K |
| 162 | Tenant & lease | Company-leased vs company-owned franchise lease income | $245,062 thousand leased vs $16,859 thousand owned base operating lease income | Issuer lessor portfolio · FY2025 10-K Note 8 (FY2025) | Verified | SEC10K |
| 163 | Tenant & lease | Q4 & FY2026 earnings release & webcast | Scheduled 2026-12-09 after market close (5:00 p.m. ET) | Issuer · release dated 2026-10-26 (reconfirms 2,115 stores) | Verified | IR26Q4 |
| 164 | Tenant & lease | Subject site closure or renewal status | (Blank — intentionally empty) | Asset A | Blank | IR25 |
| 165 | Taxes & transfer | Property tax general levy | 1% of assessed value | California · Proposition 13 | Verified | ASSESSOR |
| 166 | Taxes & transfer | Annual assessed-value increase cap | No more than 2% | California · Proposition 13 | Verified | ASSESSOR |
| 167 | Taxes & transfer | Base-year value inflation factor | California CPI, not to exceed 2% per year | California · BOE Publication 800-10 | Verified | BOE800 |
| 168 | Taxes & transfer | Reassessment triggers | Change of ownership or completed new construction | California · Proposition 13 | Verified | ASSESSOR |
| 169 | Taxes & transfer | Add-ons to the 1% levy | Voter-approved indebtedness and direct assessments | Los Angeles County Assessor | Verified | ASSESSOR |
| 170 | Taxes & transfer | Proposition 8 decline-in-value | Temporary reduction when market value falls below FBYV | California · BOE Publication 800-10 | Verified | BOE800 |
| 171 | Taxes & transfer | 35-year leasehold change-in-ownership rule | Creating, terminating or transferring a leasehold of 35+ years (including options) is a change in ownership | California · R&T Code §61(c)(1), quoted in BOE annotation 220.0345 | Verified | BOE220 |
| 172 | Taxes & transfer | Transfer of lessor's interest, 35+ years remaining | Not a change in ownership | California · R&T Code §62(g), quoted in BOE annotation 220.0345 | Verified | BOE220 |
| 173 | Taxes & transfer | City of Los Angeles base transfer tax | $2.25 per $500 (0.45%) | City of Los Angeles · Office of Finance | Verified | ULA |
| 174 | Taxes & transfer | Measure ULA surcharge | 4% above $5,400,000; 5.5% at or above $10,900,000 | City of Los Angeles · closings after 2026-06-30 | Verified | ULA |
| 175 | Taxes & transfer | Measure ULA effective date | Conveyances on or after 2023-04-01 | City of Los Angeles | Verified | ULA |
| 176 | Taxes & transfer | Threshold indexation | Adjusted annually to BLS Chained CPI | City of Los Angeles | Verified | ULA |
| 177 | Taxes & transfer | Value basis of the two taxes | ULA on gross value; base tax on value net of liens | City of Los Angeles · Office of Finance | Verified | ULA |
| 178 | Taxes & transfer | Combined city rate, tier 1 | 4.45% | City of Los Angeles · derived | Derived | ULA |
| 179 | Taxes & transfer | Combined city rate, tier 2 | 5.95% | City of Los Angeles · derived | Derived | ULA |
| 180 | Taxes & transfer | Los Angeles County documentary transfer tax | $0.55 per $500 (0.11%) | Los Angeles County Registrar-Recorder | Verified | DTT |
| 181 | Taxes & transfer | County rate for the five special cities | Calculated at the full $1.10 per $1,000 | Los Angeles County Registrar-Recorder | Verified | DTT |
| 182 | Taxes & transfer | City of Los Angeles rates (effective 2026-07-01) confirmed independently | $2.25 per $500 plus 4% / 5.5% at $5,400,000 / $10,900,000 | Los Angeles County Registrar-Recorder | Verified | DTT |
| 183 | Taxes & transfer | Federal long-term capital gain rates | 0% / 15% / 20% by taxable income (2025 thresholds on Topic 409) | Internal Revenue Service · Topic 409 | Verified | IRS409 |
| 184 | Taxes & transfer | Federal long-term capital gain brackets (2026) | 0% max $98,900 MFJ ($49,450 Single/MFS, $66,200 HoH); 15% max $613,700 MFJ ($545,500 Single, $579,600 HoH, $306,850 MFS); 20% above | Internal Revenue Service · Rev. Proc. 2025-32 § 4.03 (tax year 2026) | Verified | IRSRP25 |
| 185 | Taxes & transfer | Unrecaptured §1250 gain | 25% maximum rate on the depreciated portion | Internal Revenue Service · Topic 409 | Verified | IRS409 |
| 186 | Taxes & transfer | California capital gains treatment | No preferential rate; taxed as ordinary income | California Franchise Tax Board | Verified | FTB |
| 187 | Taxes & transfer | §1031 like-kind exchange | Real property only; property held primarily for sale does not qualify | Internal Revenue Service | Verified | IRS1031 |
| 188 | Taxes & transfer | §1031 reporting | Form 8824 | Internal Revenue Service | Verified | IRS1031 |
| 189 | Taxes & transfer | Owner's marginal rates, adjusted basis and debt | (Blank — intentionally empty) | Owner A | Blank | IRS1031 |
| 190 | Hazards | 30-year likelihood, M≥6.7 earthquake | 60% | Los Angeles region · UCERF3 (from 2014) | Verified | UCERF3 |
| 191 | Hazards | 30-year likelihood, M≥7.0 earthquake | 46% | Los Angeles region · UCERF3 (from 2014) | Verified | UCERF3 |
| 192 | Hazards | 30-year likelihood, M≥7.5 earthquake | 31% | Los Angeles region · UCERF3 (from 2014) | Verified | UCERF3 |
| 193 | Hazards | 30-year likelihood, M≥6.0 earthquake | 96% | Los Angeles region · UCERF3 (from 2014) | Verified | UCERF3 |
| 194 | Hazards | 30-year likelihood, M≥8.0 earthquake | 7% | Los Angeles region · UCERF3 (from 2014) | Verified | UCERF3 |
| 195 | Hazards | Average repeat time, M≥6.7 | 40 years | Los Angeles region · UCERF3 (from 2014) | Verified | UCERF3 |
| 196 | Hazards | 30-year likelihood, M≥6.7 | 93% | Southern California region · UCERF3 (from 2014) | Verified | UCERF3 |
| 197 | Hazards | ShakeOut scenario magnitude | M7.8 southern San Andreas | USGS OFR 2008-1150 (2008) | Verified | SHAKEOUT |
| 198 | Hazards | ShakeOut scenario deaths | about 1,800 | USGS OFR 2008-1150 (2008) | Verified | SHAKEOUT |
| 199 | Hazards | ShakeOut scenario economic losses | about $213 billion | USGS OFR 2008-1150 (2008) | Verified | SHAKEOUT |
| 200 | Hazards | Palisades Fire · area | 23,448 acres | Los Angeles County · January 2025 · CAL FIRE | Verified | PALISADES |
| 201 | Hazards | Palisades Fire · structures destroyed | 6,845 | Los Angeles County · January 2025 · CAL FIRE | Verified | PALISADES |
| 202 | Hazards | Palisades Fire · civilian fatalities | 12 | Los Angeles County · January 2025 · CAL FIRE | Verified | PALISADES |
| 203 | Hazards | Palisades Fire · duration | Active for 24 days | January 2025 · CAL FIRE | Verified | PALISADES |
| 204 | Hazards | Eaton Fire · area | 14,021 acres | Los Angeles County · January 2025 · CAL FIRE | Verified | EATON |
| 205 | Hazards | Eaton Fire · structures destroyed | 9,419 | Los Angeles County · January 2025 · CAL FIRE | Verified | EATON |
| 206 | Hazards | Eaton Fire · civilian fatalities | 19 | Los Angeles County · January 2025 · CAL FIRE | Verified | EATON |
| 207 | Hazards | Combined structures destroyed, January 2025 fires | 16,264 | Los Angeles County · derived | Derived | PALISADES |
| 208 | Hazards | Fire Hazard Severity Zone classes | Moderate, High, Very High | California · OSFM | Verified | FHSZ |
| 209 | Hazards | State Responsibility Area maps effective | 2024-04-01 | California · OSFM | Verified | FHSZ |
| 210 | Hazards | Local Responsibility Area map release phases | 2025-02-10, 2025-02-24, 2025-03-10, 2025-03-24 | California · OSFM | Verified | FHSZ |
| 211 | Hazards | Hazard versus risk | Maps measure physical hazard over 30-50 years, before mitigation | California · OSFM | Verified | FHSZ |
| 212 | Hazards | 2026 SRA update | Public comment period open at snapshot date | California · OSFM | Verified | FHSZ |
| 213 | Hazards | Mapped earthquake ground-failure zones | Fault rupture, liquefaction, earthquake-induced landslides | California Geological Survey · EQ Zapp | Verified | EQZAPP |
| 214 | Hazards | EQ Zapp limitation | Not a substitute for site-specific geologic / geotechnical investigations | California Geological Survey | Verified | EQZAPP |
| 215 | Hazards | Official flood-hazard source | FEMA Flood Maps (NFIP) | Federal Emergency Management Agency | Verified | FEMA |
| 216 | Hazards | FEMA flood zone for the subject parcel | (Blank — intentionally empty) | Asset A | Blank | FEMA |
| 217 | Hazards | Fire Hazard Severity Zone for the subject parcel | (Blank — intentionally empty) | Asset A | Blank | FHSZ |
| 218 | Hazards | Seismic hazard zone for the subject parcel | (Blank — intentionally empty) | Asset A | Blank | EQZAPP |
| 219 | Hazards | FEMA National Risk Index county scores (live portal) | (Blank — intentionally empty) | Los Angeles County · live portal | Blank | NRI |
| 220 | Hazards | FEMA National Risk Index · Los Angeles County (archived v1.19.0) | #1 nationally; EAL Value $3.9B; Risk Value $5.3B (Composite Risk Factor 1.36) | Los Angeles County · March 2023 (NRI v1.19.0 PrepToolkit briefing) | Verified | NRIDECK |
| 221 | Hazards | Post-catastrophe insurance availability and pricing | (Blank — intentionally empty) | Asset A | Blank | FEMA |
| 222 | Projection anchors | Verified population anchor | LA city 3,869,089; LA County 9,694,934 (Census V2025) | Los Angeles city / County · 2025-07-01 | Verified | CITY |
| 223 | Projection anchors | Verified employment anchor | 6,282.1 thousand nonfarm, +0.5% YoY | Los Angeles metro · September 2026 | Verified | BLS |
| 224 | Projection anchors | Verified price anchor | CPI-U +3.7%; ECI +3.9% | Los Angeles metro / CSA · September 2026 | Verified | BLS |
| 225 | Projection anchors | Verified rate anchor | 10-year Treasury 4.88% (2026-11-09) | United States · daily H.15 | Verified | FRED |
| 226 | Projection anchors | Official long-range employment projection | SCAG region 8,937k (2022) → 10,276k (2050), +0.50%/yr | SCAG six-county region · adopted 2024 | Verified | SCAG |
| 227 | Projection anchors | Official long-range population projection | SCAG region 18,827,000 (2019) → 20,909,000 (2050) | SCAG six-county region · adopted 2024 | Verified | SCAG |
| 228 | Projection anchors | Subject property's 2030-2035 value, rent, cap rate or sale price | (Blank — intentionally empty) | Asset A | Blank | FRED |
| 229 | Projection anchors | Probability of tenant renewal or closure at this site | (Blank — intentionally empty) | Asset A | Blank | SECQ3 |
| 230 | Projection anchors | Local demand growth by 2030-2035 | (Blank — intentionally empty) | Asset A | Blank | CITY |

## Automated validation gates

- `python3 scripts/build_canonical.py` — deterministic generation of 22 root HTML pages, `assets/style.css`, `data/canonical.json`, `REPO_REVIEW.md`, and `research/VERIFICATION-2026-11-10-b98090a0.md`.
- `python3 scripts/validate.py` — verified 230 rows, 40 official sources across 29 hosts, blank-value invariants, internal/fragment resolution, shared navigation, forbidden-tag absence, PII/officer-name clearance, and deterministic rebuild.
- `python3 scripts/stage_pages.py` — verified exact 23-file Pages artifact (22 HTML pages + `assets/style.css`).
- `python3 -m unittest discover -s scripts -p 'test_publication.py' -v` — all 10 publication integrity & parser regression tests passed.
- `python3 scripts/projection.py`, `python3 tools/check_site.py`, `python3 tools/linkcheck.py`, `python3 tools/check_links.py`, `python3 tools/pii_scan.py`, `python3 _advisory_src/verify_advisory.py`, `python3 _dashboard_src/verify.py`, and `git diff --exit-code -- '*.html'` — executed after final edits.
