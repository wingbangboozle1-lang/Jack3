# Line-by-line verification — canonical dataset (`data/canonical.json`, 222 rows)

**Session:** `b7ead2a1` · **Date:** 2026-11-11 (UTC) · **Dataset snapshot:** 2026-11-10 (as published)
**Scope:** every row of the merged canonical dataset (PR #42) was re-read against its registered
official/issuer source on 2026-11-11 by direct page fetch. This is the first independent re-read of
the canonical dataset by a session other than its author (`b98090a0`).

## Method

1. Grouped all 222 rows by their registered source key (34 sources in `data/canonical.json`).
2. Fetched each source page directly (U.S. Census, BLS, SEC/EDGAR, IRS, FTB, CA BOE, LA County
   Assessor, City of LA Office of Finance, LA County Registrar-Recorder (lavote.gov), CA DOF, BEA,
   SCAG, CAL FIRE/OSFM, USGS, CGS, FEMA, CDE, California School Dashboard, FRED, issuer IR).
3. Compared every value-bearing cell to the fetched official content; checked every `Blank` row is
   genuinely unconfirmable from the registered source (i.e. an asset-specific fact no public source
   publishes); re-computed every `Derived` row.
4. Values that could not be confirmed were to be blanked and flagged — **none was found necessary**.

## Result: 222 / 222 rows confirmed · 0 value errors

| Source key | Rows | Publisher | Verified on 2026-11-11 against | Result |
|---|---|---|---|---|
| CITY | 30 | U.S. Census Bureau | QuickFacts Los Angeles city (V2025), all table chunks | all match; 5 blank rows correctly blank (permits [X], trade area, race shares F-10, demand growth) |
| COUNTY | 27 | U.S. Census Bureau | QuickFacts Los Angeles County (V2025), all table chunks | all match |
| BLS | 24 | U.S. Bureau of Labor Statistics | Los Angeles Area Economic Summary, updated 2026-11-04 (PDF) | all match (Sep-2026 unemployment, payrolls, CPI, ECI, QCEW wages, OEWS wage, CE West expenditures) |
| SECQ3 | 34 | SEC EDGAR / issuer | Form 8-K Exhibit 99.1, Q3 FY2026 (filed 2026-08-12), 6 chunks | 29 values match (SSS, counts, revenues 257,657 / rental 242,526 / occupancy 166,043, margins, guidance, notes); 5 asset-specific rows correctly blank |
| SEC10K | 2 | SEC EDGAR | FY2025 Form 10-K link registered | both rows deliberately blank (not republished) — consistent with the register |
| IR25 | 6 | Issuer IR | "JACK on Track" plan, 2025-04-23 | 5 values match (150–200 block closures, 80–120 by 2025-12-31, franchise-agreement termination timing, ~1%/yr, real-estate sales to debt paydown); site row blank |
| DIRFF | 3 | CA DIR | Fast-Food Minimum Wage FAQ | $20.00 from 2024-04-01 ✓; applies to franchisees ✓; City general wage blank (not on this page) |
| DIRMW | 2 | CA DIR | Minimum Wage FAQ | $16.90 from 2026-01-01 ✓; 2027 rate not stated on page → blank ✓ |
| ULA | 8 | City of LA Office of Finance | Real Property Transfer Tax and Measure ULA FAQ, both chunks | all match: $2.25/$500 (0.45%), 4% / 5.5% at $5.4M / $10.9M after 2026-06-30, eff. 2023-04-01, Chained-CPI indexation, gross-vs-net lien basis; derived 4.45% / 5.95% match the official chart |
| DTT | 3 | LA County Registrar-Recorder (lavote.gov) | Documentary Transfer Tax page | $0.55/$500 ✓; five special cities at $1.10/$1,000 ✓; City rates eff. 7/1/26 confirmed independently ✓ |
| FRED | 6 | Federal Reserve H.15 via FRED | DGS10 series page | 4.90 (11-04), 4.84 (11-05), 4.86 (11-06) all match; anchor row dated 2026-11-06 ✓; 2 asset rows blank |
| IRS409 | 2 | IRS | Topic 409 | 0/15/20% (2025 thresholds) ✓; unrecaptured §1250 max 25% ✓ |
| IRS1031 | 3 | IRS | Like-kind exchanges page | real property only / held-for-sale excluded ✓; Form 8824 ✓; owner row blank |
| FTB | 1 | CA Franchise Tax Board | Capital gains and losses page | "no preferential rate; taxed as ordinary income" ✓ |
| ASSESSOR | 4 | LA County Assessor | Proposition 13 page | 1% levy ✓; ≤2% annual cap ✓; change-in-ownership/new-construction triggers ✓; voter-approved add-ons ✓ |
| BOE800 | 2 | CA BOE | Publication 800-10 (PDF) | CA-CPI inflation factor ≤2% ✓; Prop 8 decline-in-value ✓ |
| BOE220 | 2 | CA BOE | Annotation 220.0345 (PDF) | R&T §61(c)(1) 35+ yr leasehold rule ✓; §62(g) lessor transfer exclusion ✓ |
| PALISADES | 5 | CAL FIRE | Palisades Fire incident page | 23,448 acres ✓; 6,845 destroyed ✓; 12 fatalities ✓; 24 days (01-07→01-31) ✓; derived 16,264 = 6,845+9,419 ✓ |
| EATON | 3 | CAL FIRE | Eaton Fire incident page | 14,021 acres ✓; 9,419 destroyed ✓; 19 fatalities ✓ (current official page; historical 17-count reports are superseded) |
| FHSZ | 7 | CAL FIRE / OSFM | Fire Hazard Severity Zones page | Moderate/High/Very High ✓; SRA effective 2024-04-01 ✓; LRA phases 2025-02-10/02-24/03-10/03-24 ✓; hazard-vs-risk 30–50 yr wording ✓; 2026 SRA comment period open ✓; 2 asset rows blank |
| SHAKEOUT | 3 | USGS | OFR 2008-1150 landing page | M7.8 southern San Andreas ✓; ~1,800 deaths ✓; ~$213B losses ✓ |
| UCERF3 | 7 | USGS | Fact Sheet 2015-3009 (PDF), Table 1 | LA region: M≥6.0 96%, M≥6.7 60%, M≥7.0 46%, M≥7.5 31%, M≥8.0 7%, avg repeat 40 yr ✓; SoCal M≥6.7 93% ✓ |
| EQZAPP | 3 | CA Geological Survey | EQ Zapp page | three ground-failure types ✓; not a substitute for site investigation ✓; parcel row blank |
| FEMA | 3 | FEMA | Flood Map Service Center | official NFIP source ✓; maps superseded over time ✓; 2 asset rows blank |
| NRI | 1 | FEMA | National Risk Index portal | correctly blank (county values not extractable; mirrors rejected) |
| ZIMAS | 4 | LA City Planning | ZIMAS portal | 3 asset rows blank; 1 row labelled **Analysis** (jurisdiction gate) — not published as fact |
| CDEPROF | 2 | CA Dept. of Education | District Profile: Los Angeles Unified | enrollment 497,105 (2025-26) ✓; EL 81,328 (16.4%) ✓ |
| CDELARGE | 3 | CA Dept. of Education | Largest & Smallest Districts page | LAUSD 1st, 497,105 ✓; San Diego 112,250 ✓; statewide 5,731,260 ✓ |
| DASH | 5 | California School Dashboard | LAUSD 2025 Academic Engagement report (official caschooldashboard.org content) | 5-yr graduation 86.5% ✓; series 82.1 / 86.0 / 83.6 / 86.7 ✓; EL four-year 64.1% ✓; chronic absenteeism 21.9%, −1.5pp, 18.2% (2019), 39.8% (2022) ✓; school-level row blank |
| CDEEOY | 4 | CA Dept. of Education | 2024–25 End-of-Year Reports | ACGR 87.5% (from 86.4%) ✓; 5-yr 88.7% (from 88.4%) ✓; chronic absenteeism 19.4% (from 30.0% spike) ✓; suspension 2.9% (from 3.3%) ✓ |
| CDEACGR | 1 | CA Dept. of Education | ACGR dataset registered | correctly blank (address-specific assignment) |
| BEA | 2 | U.S. BEA | GDP by County / Personal Income by County, 2024 release | LA County personal income $818.5bn (2024) ✓; metro statistics discontinued with this release ✓ |
| SCAG | 7 | SCAG | Connect SoCal 2024 Demographics & Growth Forecast (PDF), Tables 2/4/6 + §3.1 | employment 8,937k (2022)→10,276k (2050), +0.50%/yr ✓; accommodation & food service 832k→938k, +12.8% ✓; population 18,827,000 (2019)→20,909,000 (2050) ✓; peak 18,966,261 (Jan 2019, DOF) ✓; duplicate anchor rows match ✓ |

## Derived-row arithmetic (re-computed)

| Row | Computation | Check |
|---|---|---|
| Combined structures destroyed, Jan 2025 fires | 6,845 + 9,419 | = 16,264 ✓ |
| Franchise rental revenue change | 242,526 / 260,254 − 1 | = −6.81% → −6.8% ✓ |
| Combined city rate tier 1 | 0.45% + 4.00% | = 4.45% ✓ (matches official chart) |
| Combined city rate tier 2 | 0.45% + 5.50% | = 5.95% ✓ (matches official chart) |
| SCAG accommodation/food future change | 938 / 832 − 1 | = +12.74% → +12.8% ✓ (matches table) |

## Observations (non-blocking, no value change)

- **O-1 (FRED freshness):** on 2026-11-11 the latest DGS10 observation shown on FRED is 4.88%
  (2026-11-09). The published rows are explicitly dated (4.84% on 2026-11-05; 4.86% on 2026-11-06)
  and are correct for those dates; the parenthetical "latest shown" reflects the 2026-11-10 dataset
  snapshot. No value is wrong; refresh belongs to the next snapshot, not to this verification.
- **O-2 (Dashboard rendering):** caschooldashboard.org is a client-rendered application; its official
  content was read via the indexed page content of the official URL, not a hand-typed third party.
  Values match the published row set exactly, including the by-year series.
- **O-3 (LAUSD four-year overall rate):** the Dashboard shows Four Year = 84.6% alongside the
  published 5-year 86.5%; the dataset publishes only the 5-year headline and the EL four-year
  subgroup, both correct. No four-year overall figure is published, so no conflict exists on the site.
- **O-4 (Eaton fatalities):** the current CAL FIRE incident page states 19 confirmed civilian
  fatalities; older layers citing 17 are superseded. The dataset publishes 19 ✓.
- **O-5 (ULA/DTT cross-check):** the City ULA thresholds and the County recorder's "Los Angeles
  (Effective 7/1/26)" row agree exactly ($5,400,000 / $10,900,000; 4% / 5.5%; $2.25 per $500).

## Privacy

No personal information was collected, inferred or published during this verification. The dataset's
asset placeholders ("Asset A", "Owner A") were used throughout; owner, address, parcel and lease
identifiers remain absent. `tools/pii_scan.py`: 136 files scanned, 0 findings (2026-11-11).

## Gate results on the combined tree (2026-11-11, this session)

| Gate | Result |
|---|---|
| `python3 scripts/build.py` | PASS — 20 pages, 222 rows, 34 sources; HTML determinism clean |
| `python3 scripts/build_canonical.py` | PASS — byte-identical rebuild |
| `python3 scripts/validate.py` | PASS — 222 rows, 21 published files, 25 official hosts |
| `python3 scripts/stage_pages.py` | PASS — every table row source-linked, every internal link resolves |
| `python3 -m unittest discover -s scripts -p test_publication.py` | PASS — 8/8 after this session's repair of the inventory gate |
| `python3 tools/check_site.py` / `linkcheck.py` / `check_links.py` | PASS |
| `python3 tools/pii_scan.py` | PASS — 136 files, 0 findings |
| `python3 _advisory_src/verify_advisory.py` / `_dashboard_src/verify.py` | PASS |
| `git diff --exit-code -- '*.html'` | PASS (deterministic rebuild) |
| Jekyll build + byte-comparison | verified by GitHub Actions only (RubyGems unavailable in sandbox) |

## Delta re-verification after main advanced to `ab514ee` (PRs #52/#53, this session)

The dataset grew from 222 to **223 rows** (snapshot 2026-11-11) while this session worked.
Every changed or new row was re-read against its source on 2026-11-11; all confirmed:

| Change | Row(s) | Source | Result |
|---|---|---|---|
| FRED refresh | 10-yr Treasury **4.88% (2026-11-09)**; anchor note updated | FRED DGS10 (direct fetch 2026-11-11) | latest observation on the series page is 4.88% (2026-11-09) ✓ — also resolves observation O-1 above |
| New graduation row | Combined four-/five-year **87.6%** = 25,255 graduates / 28,831 students; prior 86.5% | CDE `graddownload2026.txt` (GRAD2026), LAUSD district row `19647330000000` studentgroup ALL | currnumer 25255, currdenom 28831, currstatus 87.6, priorstatus 86.5 ✓ (25,255/28,831 = 87.598%) |
| New ACGR row | Four-year ACGR **87.4%** (2025-26, LAUSD) | DataQuest CohRate district report (ACGR2026) | Report Totals: 28,447 cohort / 24,857 graduates / 87.4% ✓ |
| FEMA source URL | `msc.fema.gov/portal/home` → `fema.gov/flood-maps` | FEMA Flood Maps page | official FEMA page; states MSC is the official NFIP mapping location; 1%-annual-chance definition ✓ |
| New page | `questions.html` registered in `data/canonical.json` | — | registered → inventory gate follows automatically (test 8/8) |

**Final tally: 223 / 223 rows confirmed against official sources; 0 value errors; 0 blanking needed.**
