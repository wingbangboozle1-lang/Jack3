# Line-by-line verification record — 2026-11-10

**Session:** `arena/882bff85-jack3` (final integration + fresh verification)
**Date:** 2026-11-10 (UTC)
**Scope:** every row in `data/evidence.json` (141 rows, 10 pages) re-read against its registered
publisher page on 2026-11-10. Prior record: `research/VERIFICATION-2026-11-08.md`.

**Standard:** a row is `Verified` only if the publisher page reports the observation. `Analysis` rows are
labelled judgement (no value asserted). `Unverified` rows publish no value. Nothing was inferred.
No personal, parcel or owner information was collected or published; the asset remains *Asset A*.

## Result

| Check | Result |
|---|---|
| Rows re-read | 141 (all pages) |
| Verified rows confirmed unchanged | all except 3 freshness/closure updates below |
| Rows flipped Unverified → Verified | 2 (county transfer tax; LAUSD graduation rate) |
| Sources re-read | 24 registered + 2 new (26 total) |
| Values corrected | 0 (no published value was wrong) |
| Values left blank | all property-specific rows (lease, rent, parcel, insurance) — correctly blank |

## Source-by-source record (all read 2026-11-10)

### U.S. Census Bureau — QuickFacts LA city (V2025)
https://www.census.gov/quickfacts/losangelescitycalifornia
Confirmed: population 3,869,089; estimates base 3,899,342; change −0.8%; under-18 19.2%; 65+ 14.2%;
foreign-born 35.7%; owner-occupied 36.0%; median home value $921,200; median gross rent $1,933;
households 1,439,097; persons/household 2.61; language other than English 56.4%; HS+ 79.6%;
bachelor's+ 38.5%; labor-force participation 66.4%; accommodation & food sales $17.37bn (2022);
retail sales $81.35bn, $21,281 per capita (2022); commute 30.7 min; median HH income $81,939;
per capita $47,685; poverty 16.5%; density 8,304.2/sq mi (2020). All match published rows.

### U.S. Census Bureau — QuickFacts LA County (V2025)
https://www.census.gov/quickfacts/losangelescountycalifornia
Confirmed: population 9,694,934; base 10,017,414; change −3.2%; 65+ 17.1%; foreign-born 33.4%.
All match published rows.

### Bureau of Labor Statistics — LA Area Economic Summary (updated 2026-11-04)
https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf
Still the 2026-11-04 vintage; September 2026 data. Confirmed: unemployment US 4.0 / CA 5.1 /
metro 4.4 / county 4.5 / city 4.5; Q1 2026 weekly wage $1,704; nonfarm 6,282.1k (+0.5%);
education & health +3.8%; information −5.7%; CPI-U +3.7% (food +2.8%, energy +20.3%);
ECI +3.9%; West spending housing $33,016 / food $12,447 / transport $14,110 (2025).
All match published rows. No newer vintage exists as of 2026-11-10.

### Federal Reserve via FRED — DGS10
https://fred.stlouisfed.org/series/DGS10
Latest observation at read time: **4.86% on 2026-11-06** (2026-11-05: 4.84%; 2026-11-04: 4.90%).
Published rows updated from the dated 4.84% (2026-11-05) to the latest dated 4.86% (2026-11-06).
The prior value was correct for its date; this is a freshness update, not a correction.

### Jack in the Box Inc. — Q3 FY2026 earnings (2026-08-12)
https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx
Confirmed: same-store sales −1.1% (12 weeks ended 2026-07-05); systemwide −1.4%; 4 openings,
17 closures; count 2,115 (149 company / 1,966 franchise); revenues $257.7m (−1.8%);
restaurant-level margin 17.6%; franchise-level margin 37.4% (from 39.3%); bad-debt expense higher;
$110.0m 2019-1 Class A-2-II prepaid; $500m 2026-1 Class A-2 issued (anticipated repayment May 2031).
All match published rows. Chain-level only; no store-level inference drawn.

### Jack in the Box Inc. — JACK on Track (2025-04-23)
https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Unveils-JACK-on-Track-Plan-to-Improve-Long-Term-Financial-Performance/default.aspx
Confirmed: ~150–200 underperforming closures; ~80–120 by 2025-12-31, remainder on franchise
agreement termination dates; ongoing ~1%/yr from FY2026; selling selected owned real estate for
debt paydown. All match published rows. Franchise dates are not lease expiries.

### California DIR — minimum wage FAQs
https://www.dir.ca.gov/dlse/FAQ_MinimumWage.htm · https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm
Confirmed: state minimum $16.90/hour from 2026-01-01; covered fast-food $20.00/hour from
2024-04-01 (AB 1228). No 2027 figure appears on the DIR page; the $17.40 secondary-source figure
remains unpublished (F-17/V-2 handling unchanged).

### California Department of Education
- LAUSD district profile (https://www.cde.ca.gov/sdprofile/details.aspx?cds=19647330000000):
  enrollment 497,105; English learners 81,328 (16.4%), 2025-26. Confirmed.
- Largest & smallest districts (https://www.cde.ca.gov/ds/ad/ceflargesmalldist.asp):
  LAUSD 1st (497,105); San Diego Unified 112,250; statewide 5,731,260. Confirmed.
- ACGR data files (https://www.cde.ca.gov/ds/ad/filesacgr.asp): file index only (2025-26 file
  posted 2026-10-15); no district value on the page. Correctly not used as a value source.
- Dashboard landing (https://www.cde.ca.gov/ta/ac/cm/): confirms the Dashboard is CDE's
  accountability system. No values.

### California School Dashboard — LAUSD 2025 (NEW source, closes V-4)
https://www.caschooldashboard.org/reports/19647330000000/2025/academic-engagement
Read 2026-11-10: **86.5% graduated** (All Students, 5-year; 4-year 84.6%, 5th-year 1.8%);
series 2019 82.1% / 2022 86.0% / 2023 83.6% / 2024 86.7% / 2025 86.5%. Published as a Verified
row on `schools.html`, labelled with both the 5-year headline and the 4-year component to avoid
mislabel. This is CDE's official Dashboard site (linked as "California School Dashboard Report"
from the CDE district profile).

### LA County Assessor — Proposition 13
https://assessor.lacounty.gov/real-estate-toolkit/proposition-13
Confirmed: 1% general levy; 2% annual assessed-value cap; reassessment on change of ownership /
new construction; voter-approved add-ons. All match published rows.

### City of Los Angeles Office of Finance — Measure ULA FAQ
https://finance.lacity.gov/faq/measure-ula
Confirmed: base tax 0.45% ($2.25/$500); ULA 4% above $5,400,000 / 5.5% at or above $10,900,000
for closings after 2026-06-30; thresholds indexed to Chained CPI; ULA on gross value, base on net
of liens. All match published rows.

### LA County Registrar-Recorder — documentary transfer tax (NEW source, closes V-3)
https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info
Read 2026-11-10: county rate **$0.55 per $500 ($1.10 per $1,000)** per Revenue & Taxation Code
§§11911–11933; city of LA $2.25/$500 plus ULA schedule (consistent with the Finance FAQ).
Published as a Verified row on `taxes.html`. The 2026-11-08 "page could not be retrieved" flag
is closed.

### IRS — §1031 and Topic 409; California FTB
- https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips:
  real property only; held primarily for sale does not qualify; Form 8824. Confirmed.
- https://www.irs.gov/taxtopics/tc409: 0/15/20% (2025 thresholds); 25% max unrecaptured §1250.
  Confirmed.
- https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html:
  no preferential rate; taxed as ordinary income. Confirmed.

### Hazard sources
- CAL FIRE Palisades (https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire): 23,448 acres;
  6,845 destroyed, 975 damaged. Confirmed.
- CAL FIRE Eaton (https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire): 14,021 acres;
  9,419 destroyed, 1,076 damaged. Combined 16,264. Confirmed.
- USGS OFR 2008-1150 (https://pubs.usgs.gov/of/2008/1150/): M7.8 scenario, ~1,800 deaths,
  ~$213bn losses. Confirmed (scenario, not forecast).
- OSFM Fire Hazard Severity Zones (https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones):
  hazard vs. risk distinction. Confirmed.
- CGS EQ Zapp (https://www.conservation.ca.gov/cgs/geohazards/eq-zapp): ground-failure zones;
  maps do not replace site investigations. Confirmed.
- FEMA MSC (https://msc.fema.gov/portal/home): official NFIP flood-hazard source. Confirmed.

### ZIMAS (https://zimas.lacity.org/)
Interactive application; no parcel fact extractable without an address. Correctly used only as a
research route; all parcel rows remain blank.

## Irregularities found this pass

| # | Finding | Action |
|---|---|---|
| W-1 | FRED DGS10 latest observation moved to 4.86% (2026-11-06); published rows cited 4.84% (2026-11-05) | Updated all 3 rows + landing + summary to the latest dated value. Prior value was correct for its date. |
| W-2 | County transfer tax (V-3) and LAUSD grad rate (V-4) closable | Both retrieved from official pages and published as Verified rows. Review entries updated to "Closed". |
| W-3 | Dashboard headline 86.5% is a 5-year rate (4-year 84.6%) | Published with both components labelled; row renamed "District graduation rate" to avoid a four-year mislabel. |
| W-4 | PRs #31/#32 stale (2026-11-08), overlapping shared files; #32 commits `_pages_artifact/` | Not merged. This session supersedes their shared-file claims per the board's stale rule; PRs left open for owners. |

## Still blank (correctly)

Property identity, executed lease and exact expiry, rent/escalations/options, legal tenant/guarantor,
store financials, parcel zoning/hazards/insurance, trade-area catchment, school assignment, cap rate /
sale price / NOI, owner's tax basis and debt. Each is listed on `review.html` with the official page
that would close it. None blocks publication; none was inferred.
