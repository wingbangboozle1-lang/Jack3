# Line-by-line verification record — snapshot 2026-11-10

Session `4f0b3fa2`. Branch `arena/4f0b3fa2-jack3`.

This is the audit trail behind `data/evidence.json`. Every published value was re-read on its publisher's page on
**10 November 2026**, between about 00:30 and 02:00 UTC. Nothing here is quoted from memory, from a search snippet, or
from an earlier layer of this repository. Where a value was read out of a document that is updated in place (a rolling
PDF, a daily rates table), the access date is stated so a later reader can tell whether the source has moved.

Method for each row: open the linked page, find the value, compare it with the row already in the dataset, record the
result as MATCH, CORRECTED, or BLANKED. A row can only carry the status `Verified` if it was read this way.

---

## 1. Sources read for this snapshot

| Key | Document | Host | Read |
|---|---|---|---|
| `city` | QuickFacts: Los Angeles city, California (V2025) | census.gov | 2026-11-10 |
| `county` | QuickFacts: Los Angeles County, California (V2025) | census.gov | 2026-11-10 |
| `bls` | Los Angeles Area Economic Summary, updated 2026-11-04 (PDF) | bls.gov | 2026-11-10 |
| `blsmsa` | Los Angeles–Long Beach–Anaheim, CA: Economy at a Glance, Sep 2026 preliminary | bls.gov | 2026-11-10 |
| `blseci` | Changing Compensation Costs in the Los Angeles Metropolitan Area, September 2026 (released 2026-11-04) | bls.gov | 2026-11-10 |
| `treasury` | Daily Treasury Par Yield Curve Rates, November 2026 | home.treasury.gov | 2026-11-10 |
| `jackq3` | Jack in the Box Inc., Q3 FY2026 earnings release, 2026-08-12 | investors.jackinthebox.com | 2026-11-10 |
| `jacktrack` | Jack in the Box Inc., "JACK on Track" plan, 2025-04-23 | investors.jackinthebox.com | 2026-11-10 |
| `jack10k` | Form 10-K, fiscal year ended 2025-09-28 | sec.gov | 2026-11-10 (index only) |
| `prop13` | Proposition 13 | assessor.lacounty.gov | 2026-11-10 |
| `ula` | Real Property Transfer Tax and Measure ULA FAQ | finance.lacity.gov | 2026-11-10 |
| `lavote` | Documentary Transfer Tax | lavote.gov | 2026-11-10 |
| `rtc11911` | Rev. & Tax. Code §11911 | leginfo.legislature.ca.gov | 2026-11-10 |
| `irs409` | Topic no. 409, Capital gains and losses | irs.gov | 2026-11-10 |
| `irs559` | Topic no. 559, Net investment income tax | irs.gov | 2026-11-10 |
| `irs1031` | Like-kind exchanges — real estate tax tips | irs.gov | 2026-11-10 |
| `irsfs` | FS-2008-18, Like-Kind Exchanges Under IRC §1031 | irs.gov | 2026-11-10 |
| `ftb` | Capital gains and losses | ftb.ca.gov | 2026-11-10 |
| `dir` | Minimum Wage FAQ | dir.ca.gov | 2026-11-10 |
| `dirff` | Fast Food Minimum Wage FAQ (AB 1228) | dir.ca.gov | 2026-11-10 |
| `cdelarge` | Largest & Smallest Public School Districts, 2025–26 | cde.ca.gov | 2026-11-10 |
| `cdeacgr` | Adjusted Cohort Graduation Rate and Outcome Data | cde.ca.gov | 2026-11-10 (index only) |
| `usgs` | The ShakeOut Scenario, OFR 2008-1150 | pubs.usgs.gov | 2026-11-10 |
| `osfm` | Fire Hazard Severity Zones | osfm.fire.ca.gov | 2026-11-10 |
| `palisades` | Palisades Fire incident page | fire.ca.gov | 2026-11-10 |
| `eaton` | Eaton Fire incident page | fire.ca.gov | 2026-11-10 |
| `cgs` | EQ Zapp | conservation.ca.gov | 2026-11-10 |
| `fema` | Flood Map Service Center | msc.fema.gov | 2026-11-10 |
| `dof` | Population Projections (Baseline 2024) | dof.ca.gov | 2026-11-10 |
| `zimas` | Zoning Information and Map Access System | zimas.lacity.org | 2026-11-10 (portal only) |
| `scag` | Data & Tools | scag.ca.gov | 2026-11-10 |

## 2. Row-level results

### 2.1 Census QuickFacts (`city`, `county`)

Read: population and percent change (V2025); age, race, foreign-born, housing, households, income, poverty, labour
force, education, travel time, density, land area, Economic Census sales and receipts.

| Row | Published | Source value | Result |
|---|---|---|---|
| E-01 to E-27 (economy) | see dataset | — | n/a (BLS rows, below) |
| P-01 | 3,869,089 | 3,869,089 | MATCH |
| P-02 | −0.8% | −0.8% (base 3,899,342) | MATCH |
| P-03 | 9,694,934 | 9,694,934 | MATCH |
| P-04 | −3.2% | −3.2% (base 10,017,414) | MATCH |
| P-05, P-06 | 1,439,097; 2.61 | 1,439,097; 2.61 | MATCH |
| P-07 | 19.2% | 19.2% (city and county) | MATCH |
| P-08 | 14.2% / 17.1% | 14.2% city; 17.1% county | MATCH |
| P-09 | 35.7% / 33.4% | 35.7%; 33.4% | MATCH |
| P-10 | 56.4% / 55.1% | 56.4%; 55.1% | MATCH |
| P-11 | $81,939 / $90,112 | $81,939; $90,112 | MATCH |
| P-12 | $47,685 / $45,792 | $47,685; $45,792 | MATCH |
| P-13 | 16.5% / 13.3% | 16.5%; 13.3% | MATCH |
| P-14 | 36.0% / 45.9% | 36.0%; 45.9% | MATCH |
| P-15 | $921,200 / $834,200 | $921,200; $834,200 | MATCH |
| P-16 | $1,933 / $1,954 | $1,933; $1,954 | MATCH |
| P-17 | 66.4% / 64.7% | 66.4%; 64.7% | MATCH |
| P-18 | 79.6% / 80.9% | 79.6%; 80.9% | MATCH |
| P-19 | 38.5% / 36.0% | 38.5%; 36.0% | MATCH |
| P-20 | 10.7% / 8.3% | 10.7%; 8.3% | MATCH |
| P-21 | 89.3% / 90.8% | 89.3%; 90.8% | MATCH |
| G-01 | 469.49 / 4,059.28 sq mi | 469.49; 4,059.28 | MATCH |
| G-02 | 8,304.2 / 2,466.9 per sq mi | 8,304.2; 2,466.9 | MATCH |
| G-03 | 30.7 / 30.4 minutes | 30.7; 30.4 | MATCH |
| G-04 | 3,726,923 housing units (county) | 3,726,923 | MATCH. City housing units show flag X ("not applicable") and are **not** published. |
| G-05 | 22,250 permits (county) | 22,250; city flag X | MATCH. City permits are blank on QuickFacts, so the county figure is published and labelled as county only. |
| G-06 | $213.9bn (county), $81.35bn (city) | 213,932,785 and 81,351,523 ($1,000s) | MATCH |
| G-07 | $44.0bn (county), $17.37bn (city) | 44,000,801 and 17,366,966 ($1,000s) | MATCH |
| G-08 | $22,010 / $21,281 | $22,010; $21,281 | MATCH |

Note on the city race shares: the earlier layers of this repository flagged that the city's race-alone percentages sum
to about 74% while the county's sum to about 99.8%. Re-reading the page on 2026-11-10 reproduces the same arithmetic
(33.4 + 8.4 + 1.3 + 12.1 + 0.2 + 18.9 = 74.3 with Hispanic 47.2 shown separately; the county sums to 99.8). This
snapshot therefore publishes **no** race shares at all: the discrepancy is real, and publishing a breakdown whose
components do not reconcile would be worse than leaving it out. Flagged as F-19 on the review page.

### 2.2 BLS (`bls`, `blsmsa`, `blseci`)

| Row | Published | Source value | Result |
|---|---|---|---|
| E-01 to E-05 | 4.0 / 5.1 / 4.4 / 4.5 / 4.5 | same, Sep-26 column of the Economic Summary | MATCH |
| E-06, E-07 | 6,646.9; 6,352.9 thousand | 6,646.9; 6,352.9 | MATCH |
| E-08 | 6,282.1 thousand | 6,282.1 | MATCH |
| E-09 | +0.5% (+30.2k) | 0.5; 30.2 | MATCH |
| E-10 | +3.8% (+49.1k; 1,340.7k) | 3.8; 49.1; 1,340.7 | MATCH |
| E-11 | +1.5% (+11.5k; 782.0k) | 1.5; 11.5; 782.0 | MATCH |
| E-12 | −5.7% (−11.4k; 187.0k) | −5.7; −11.4; 187.0 | MATCH |
| E-13 | −1.7% (−5.1k; 300.4k) | −1.7; −5.1; 300.4 | MATCH |
| E-14 | −0.5% (−5.2k; 975.5k) | −0.5; −5.2; 975.5 | MATCH |
| E-15 | −1.2% (−5.4k; 444.8k) | −1.2; −5.4; 444.8 | MATCH |
| E-16 | −1.1% (−8.4k; 734.8k) | −1.1; −8.4; 734.8 | MATCH |
| E-17 | +0.3% (+2.9k; 1,047.9k) | 0.3; 2.9; 1,047.9 | MATCH |
| E-18 | 0.0% (+0.1k; 251.5k) | 0.0; 0.1; 251.5 | MATCH |
| E-19 | +3.7% | 3.7 (area) and 3.7 (U.S.) | MATCH |
| E-20 | +2.8% | 2.8 (area); U.S. 2.5 | MATCH |
| E-21 | +20.3% | 20.3 (area); U.S. 20.4 | **CORRECTED.** Earlier layers published 20.4% for the Los Angeles area. The table's area column reads 20.3; 20.4 is the U.S. city average. |
| E-22 | +4.2% | 4.2, total compensation, private industry, LA–Long Beach CSA | **CORRECTED.** Earlier root rows labelled the 3.9% wages figure as the "Employment Cost Index". The release's headline is 4.2%. |
| E-23 | +3.9% | 3.9, wages and salaries, same release | Added as a separate row so the distinction is explicit. |
| E-24 | $1,704 | 1704 (Q1 2026, LA County) | MATCH |
| E-25 | $37.15 | 37.15 (May 2025, LA metro, all occupations) | MATCH |
| E-26 | $33,016 / $14,110 / $12,447 / $6,713 | 33016 / 14110 / 12447 / 6713 (West, 2025) | MATCH |

Cross-check performed: E-06 minus E-07 = 294.0 thousand unemployed; 294.0 ÷ 6,646.9 = 4.42%, which reproduces the
published 4.4% local rate to one decimal. This is the arithmetic the validator repeats on every build.

### 2.3 Treasury (`treasury`)

Daily Par Yield Curve, November 2026 table, read 2026-11-10:

| Date | 10 YR |
|---|---|
| 11/02/2026 | 4.91 |
| 11/03/2026 | 4.95 |
| 11/04/2026 | 4.90 |
| 11/05/2026 | 4.84 |
| 11/06/2026 | 4.86 |
| **11/09/2026** | **4.88** |

Published as 4.88% (the latest observation on the access date). Earlier layers used 4.84% (2026-11-05) and, in one
layer, 4.19% (2026-01-02, nine months stale). Both are superseded. This is a rolling source: the figure will change
again, which is why every page carries the snapshot date and the row carries the observation date.

### 2.4 Tenant (`jackq3`, `jacktrack`)

| Row | Published | Source value | Result |
|---|---|---|---|
| T-01 | −1.1% (co −0.9, fr −1.2) | −1.1; −0.9; −1.2 | MATCH |
| T-02 | −1.4% | 1.4% decrease in systemwide sales | MATCH |
| T-03 | 2,115 (149/1,966) | 2,115; 149; 1,966 | MATCH |
| T-04 | 4 opened, 17 closed | 4; 17 | MATCH |
| T-05 | 17.6% ($17.0m), prior 17.9% | 17.6%; $17.0m; 17.9% | MATCH |
| T-06 | 37.4% ($60.3m), prior 39.3% ($66.2m) | 37.4%; 60.3; 39.3; 66.2 | MATCH |
| T-07 | $257.7m, −1.8% | 257.7; 1.8%; prior 262.4 | MATCH |
| T-08 | $21.0m (prior $22.8m) | 21.0; 22.8 | MATCH |
| T-09 | $61.2m (prior $57.1m) | 61.2; 57.1 | MATCH |
| T-10 | $1.08 / $0.96 | 1.08; 0.96 | MATCH |
| T-11 | Bad debt higher, no amount | "Bad debt expense was also higher versus the prior year quarter" | MATCH (direction only; no figure disclosed, so none is published) |
| T-12 | $110.0m prepaid; $500m issued | 110.0; 500 | MATCH |
| T-13 | Del Taco closed 2025-12-22 | 22 December 2025 | MATCH |
| T-14 to T-18 | 150–200 closures; 80–120 by 12/31/2025; ~1% annually; sell real estate; dividend discontinued | all stated | MATCH |
| T-19 | San Diego headquarters | "founded and headquartered in San Diego, California" | MATCH. An inherited note claimed a Texas headquarters; the issuer's own release and 10-K say San Diego. |

The 10-K was opened and the filing index confirmed (accession `0000807882-25-000072`), but the XBRL render is
approximately 1.5 MB of tagged data. No 10-K figure is published in this snapshot that was not also available on the
earnings release. `jack10k` is registered as a source and is not the citation for any published row, which is the
honest position.

### 2.5 Hazards (`palisades`, `eaton`, `usgs`, `osfm`, `cgs`, `fema`)

| Row | Published | Source value | Result |
|---|---|---|---|
| R-10 | M7.8 scenario; ~1,800 deaths; $213bn | "about 1800 deaths and $213 billion of economic losses" | MATCH |
| R-11 | 16,264 structures destroyed in 24 days | 6,845 + 9,419 | DERIVED (validator re-adds) |
| R-12 | 23,448 acres; 6,845 destroyed; 975 damaged; 12 civilian fatalities | identical | MATCH |
| R-13 | 14,021 acres; 9,419 destroyed; 1,076 damaged; 19 civilian fatalities | identical | MATCH. This resolves an earlier repository discrepancy (17 vs 19 fatalities): the incident page states 19. |
| R-14 | blank | CAL FIRE maps hazard, not risk; LRA maps are adopted locally | BLANKED (no parcel overlay) |
| R-15 | blank | CGS states EQ Zapp is not a substitute for a geotechnical investigation | BLANKED |
| R-16 | blank | FEMA MSC states maps change over time | BLANKED |

### 2.6 Taxes (`ula`, `lavote`, `rtc11911`, `prop13`, `irs*`, `ftb`, `dir`)

| Row | Published | Source value | Result |
|---|---|---|---|
| X-01 to X-04 | 1%; 2% cap; reassessment triggers; voter debt and assessments | Assessor's page, including its $420,000 / $4,200 example | MATCH |
| X-05 | $2.25 per $500 = 0.45% | "$2.25 per $500"; summary table "0.45%" | MATCH |
| X-06 | 4% above $5,400,000; 5.5% at or above $10,900,000 | note and summary table | MATCH |
| X-07 | Chained-CPI indexation | "adjusted annually based on the Bureau of Labor Statistics Chained Consumer Price Index" | MATCH |
| X-08 | Effective 2023-04-01 | "on or after April 1, 2023" | MATCH |
| X-09 | $0.55 per $500 | §11911(a) text | MATCH. **This closes the gap earlier sessions left blank.** |
| X-10 | $1.10 per $1,000 in the five special cities | Recorder's "Additional Tax Rates for Specific Cities" note, plus its $21,100 worked example ($96.75 total) | MATCH. Also closes an earlier "page could not be retrieved" flag. |
| X-11 | 0/15/20% with thresholds | Topic 409, 2025 thresholds | MATCH |
| X-12 | 25% max on unrecaptured §1250 | Topic 409 | MATCH |
| X-13 | 3.8% NIIT above $200k/$250k/$125k | Topic 559 | MATCH |
| X-14 | no preferential CA rate | FTB: "All capital gains are taxed as ordinary income" | MATCH |
| X-15 | real property, not held primarily for sale | IRS tax tips | MATCH |
| X-16 | 45 days / 180 days | FS-2008-18 | MATCH |
| X-17 | deferred, not forgiven; basis carries | FS-2008-18 | MATCH |
| R-02 | $20.00/hour fast food | DIR fast-food FAQ, effective 2024-04-01 | MATCH |
| R-03 | $16.90/hour from 2026-01-01 | DIR minimum-wage FAQ | MATCH. No 2027 figure is stated on the page, so none is published. |

Two tax rows require arithmetic rather than a quotation, and both are recomputed by the validator:

* **M-07 / R-08.** $6,000,000 sale, City of Los Angeles: 0.45% ($27,000) + 4% ULA ($240,000) + $0.55/500 ($6,600) =
  **$273,600 = 4.56%**. The threshold check matters: at $5,400,000 the ULA line disappears and the total falls to
  $30,240 (0.56%).
* **M-08.** 1 ÷ 1.0488⁴ = **0.8264**.

### 2.7 Schools (`cdelarge`, `cdeacgr`)

| Row | Published | Source value | Result |
|---|---|---|---|
| S-01 | 497,105 | 497,105 | MATCH |
| S-02 | 5,731,260 | 5,731,260 | MATCH |
| S-03 | 112,250; 61,679 | 112,250; 61,679 | MATCH |
| S-04 | blank | cohort data published only as data files | BLANKED |
| S-05 | blank | see §3, item 4 | BLANKED (was 81,328 / 16.4% in an earlier layer) |

## 3. Attempted and failed

These were tried and did not yield a publishable value. Each is recorded rather than papered over.

1. **BLS HTML summary.** `blssummary_losangeles.htm` returns a not-found page; only the PDF exists. The PDF is the
   registered source.
2. **LA County Recorder transfer-tax page (old URL).** Several paths under `lavote.gov/home/recorder/…` return
   "resource removed". The working URL is
   `https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info`, which
   was located and read.
3. **CDE district profile.** `sdprofile/details.aspx?cds=1964733…` returns "No districts found" for both the 14-digit
   and 7-digit forms of the LAUSD CDS code, and DataQuest returns its error page. Consequently the earlier
   81,328 / 16.4% English-learner figure cannot be reproduced today and is **withheld**, not republished.
4. **CDE adjusted cohort graduation file.** `acgr25.txt` is 16 MB of fixed-width text. Downloading and parsing it was
   outside this pass, so no LAUSD graduation rate is published. The number 86.5% asserted by `dashboard/` could not be
   verified on any CDE page; it is flagged, not adopted.
5. **CA DOF population projections.** Published only as `.xlsx` workbooks (P-2A, P-3). Not extracted, so no 2030/2035
   projection is published. Flagged as the single most valuable item still to extract.
6. **California Department of Insurance FAIR Plan pages.** Two candidate URLs both returned the Department's
   "document not found" page. No residual-market figure is published.
7. **FEMA National Risk Index.** Not queried; county-level values were not readable in earlier attempts and no
   third-party mirror is acceptable under the no-aggregator rule.
8. **SEC 10-K XBRL render.** Opened and confirmed, ~1.5 MB of tagged data; no figure is published from it. The
   earnings release is the citation for every published issuer row.

## 4. Rollover from earlier snapshots

The repository contains figures from 2026-11-06, 2026-11-07 and 2026-11-08. Where a figure has moved or was wrong,
this snapshot supersedes it and the older layers are left untouched as an audit trail. The differences that matter:

| Item | Earlier | Now | Why |
|---|---|---|---|
| 10-year Treasury | 4.84% (2026-11-05); one layer 4.19% (2026-01-02) | 4.88% (2026-11-09) | daily source |
| LA ECI | 3.9% labelled "Employment Cost Index" | 4.2% compensation; 3.9% wages | source labels the sub-index separately |
| Energy CPI (LA) | 20.4% | 20.3% | 20.4% is the U.S. figure |
| County transfer tax | blank | $0.55 per $500 | statute and Recorder page read |
| LAUSD graduation | blank in one layer, 86.5% in another | blank | not reproducible from CDE |
| LAUSD English learners | 81,328 (16.4%) | blank | CDE profile unreachable on 2026-11-10 |
| Eaton fatalities | 17 in one layer, 19 in another | 19 | incident page |

## 5. What automated checks do and do not prove

`scripts/validate.py` proves that every published row carries a registered source link, that no unverified row
renders a value, that the derived arithmetic is right, that internal links and anchors resolve, that the pages carry
no third-party scripts or trackers, and that a rebuild is byte-identical. `tools/check_links.py` proves every external
link is https and on an approved official or issuer host.

None of these proves that the Census Bureau still publishes 3,869,089 tomorrow. That is what §1 and §2 are for, and
why both carry a date. When the snapshot ages, the honest action is to re-read the pages, not to trust the checker.
