# Verification record — session `arena/c155a72c-jack3` — 2026-11-13 (UTC)

Scope: independent re-read of a sample of canonical rows against live official or issuer pages, one freshness
correction, and the full local gate suite. Privacy: `Asset A` / `Owner A` only. No owner identity, address,
parcel number, contact person or private lease fact was copied from any page read in this pass.

## 1. Pages read in this pass (live fetch, 2026-11-13)

| Key | Official URL | Part read | Rows checked | Result |
|---|---|---|---|---|
| ULA | https://finance.lacity.gov/faq/measure-ula | chunk 1 of 2 | 180, 181, 185, 186 | Match. Base $2.25 / $500 (0.45%); ULA 4% above $5,400,000 and 5.5% at or above $10,900,000 for transactions after 2026-06-30; combined rates 4.45% and 5.95% printed in the City's table. |
| CITY | https://www.census.gov/quickfacts/losangelescitycalifornia | chunk 1 of 4 | 15, 16, 17, 18 (population block) | Match. Population estimate July 1, 2025 (V2025) 3,869,089; base 3,899,342; change -0.8%; Census 2020 3,898,747; Hispanic 47.2%; under 18 19.2%; 65+ 14.2%. |
| FRED | https://fred.stlouisfed.org/series/DGS10 and https://fred.stlouisfed.org/data/DGS10 (last chunk) | series page; data table chunk 46 of 47 | 92, 93, 94, 234 | Match for 4.84% (2026-11-05), 4.86% (2026-11-06), 4.88% (2026-11-09), 4.90% (2026-11-04). **Newer print: 5.10% on 2026-11-12** (table last updated 2026-11-13 3:16 PM CST). Corrected in this pass. |
| BLS | https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf | full (1 chunk) | 65-79, 80-81, 85-86 | Match. LA metro unemployment Sep-26 4.4% (Sep-25 5.5%); LA County 4.5%; LA city 4.5%; California 5.1%; US 4.0%; nonfarm 6,282.1 thousand (+30.2, +0.5%); education & health +49.1 (+3.8%); leisure & hospitality 782.0 (+1.5%); information -5.7%; manufacturing -1.2%; government -1.1%; LA CPI-U +3.7%; energy +20.3%; average weekly wage LA County Q1 2026 $1,704; hourly wage all occupations $37.15 (May 2025); housing spending West $33,016. |
| DIR | https://www.dir.ca.gov/dlse/FAQ_MinimumWage.htm | chunk 1 of 2 | 87 | Match. California minimum wage $16.90/hour effective 2026-01-01. |
| IR | https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Announces-Fourth-Quarter-and-Full-Year-2026-Earnings-Webcast/default.aspx | full | 167, 153 | Match. Q4 and full-year FY2026 results after market close on Wednesday 2026-12-09; company describes 2,115 restaurants across 25 states, Mexico and Guam. The issuer's investor-relations contact is not reproduced here. |
| CAL FIRE / OSFM | https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones | chunk 1 of 2 | 217-221 | Match. Moderate / High / Very High classes; SRA map effective 2024-04-01; LRA phase release dates 2025-02-10, 2025-02-24, 2025-03-10, 2025-03-24; 2026 SRA public comment period open on the day read. |

Not re-read in this pass: the FY2025 Form 10-K (53 parts; franchise AUV row 161 was verified in earlier passes and
is not re-checked here), the Census county page, the CDE/Dashboard school rows, the SCAG, BEA, DOF and remaining
SEC rows, and the NRI / ZIMAS / CDE ACGR rows that are Blank.

## 2. Correction made (freshness)

- **10-year Treasury (DGS10):** the register's current-facing anchor was 4.88% (2026-11-09). FRED now publishes
  **5.10% for 2026-11-12**. Changed in `data/canonical_rows.py` (economy row; projection-anchor row), the
  `Verified` rate-anchor text in `scripts/build_canonical.py`, and the projection constants in
  `scripts/projection.py` (`TREASURY_ANCHOR` 0.0488 → 0.0510, `TREASURY_ANCHOR_DATE` 2026-11-09 → 2026-11-12,
  `DISCOUNT_RATES[0]` 0.0488 → 0.0510). The unit test that locks the anchor to a canonical FRED row reads the new
  row dynamically and passes.
- Earlier dated records (`research/VERIFICATION-2026-11-1*.md`, `research/DECISION-DOSSIER-2026-11-12-7b04b8ee.md`)
  still quote 4.88% and the sensitivity figures computed from it. They are dated history and were not rewritten.
  Logged as flag **F-32** for owner review.
- Projection effect: the discount-rate floor in the break-even tables moves from 4.88% to 5.10%. Output is
  arithmetic on disclosed assumptions only; it is not a valuation and is not calibrated to any property.

## 3. Irregularities for review

1. **F-32 (Medium)** — rate-anchor vintage, described above.
2. The Jekyll artifact comparison (`scripts/stage_pages.py _jekyll_test`) cannot run in this sandbox because Jekyll is
   not installed. It is a CI-only step and was not run locally; the static HTML gates all pass.

## 4. Gate results (local, this session)

`scripts/build.py`, `scripts/validate.py` (240 rows, 211 verified / 2 derived / 1 analysis / 26 blank; 45 sources;
row provenance and deterministic rebuild clean), `scripts/stage_pages.py` (23 files), `tools/check_site.py`,
`tools/linkcheck.py`, `tools/check_links.py` (all verified-source links on official or primary domains),
`tools/pii_scan.py` (0 findings), `_advisory_src/verify_advisory.py`, `_dashboard_src/verify.py`,
`python3 -m unittest discover -s scripts -p 'test_*.py'` (16 tests OK).
