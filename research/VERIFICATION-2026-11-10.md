# Independent re-verification — 2026-11-10 (session `c70571c7`)

Scope: root published site (`data/evidence.json` → 12 pages, 141 rows).
Method: each figure below was re-read from the live official publisher page on
2026-11-10 and compared to the published value. No value was changed: every
checked figure matched. Unverified/Analysis rows assert no values by design and
were confirmed blank.

## Checked and confirmed (live fetch, 2026-11-10)

| Published value | Official source (live) | Result |
|---|---|---|
| LA city pop. 3,869,089; −0.8%; under-18 19.2%; 65+ 14.2%; households 1,439,097; 2.61/hh; owner-occ. 36.0%; median HH income $81,939; per-capita $47,685; poverty 16.5%; density 8,304.2; commute 30.7 min; retail $81.35bn; per-capita $21,281; food services $17.37bn; HS+ 79.6%; bachelor's+ 38.5% | https://www.census.gov/quickfacts/losangelescitycalifornia (V2025) | Match |
| LA County pop. 9,694,934; −3.2%; 65+ 17.1% | https://www.census.gov/quickfacts/losangelescountycalifornia | Match |
| Metro unemployment 4.4%; city/county 4.5%; nonfarm 6,282.1k +0.5%; info −5.7%; educ/health +3.8%; CPI-U +3.7%; ECI +3.9%; weekly wage $1,704; food +2.8%; energy +20.3% | https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf (updated 2026-11-04) | Match |
| Jack Q3 FY2026: SSS −1.1%; systemwide −1.4%; 17 closures / 4 openings; 2,115 restaurants (149 + 1,966); revenues $257.7m −1.8%; restaurant margin 17.6%; franchise margin 37.4% vs 39.3%; $110m prepaid; $500m issued | https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx | Match |
| Fast-food wage $20.00 from 2024-04-01 (AB 1228) | https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm | Match |
| State minimum $16.90 from 2026-01-01 | https://www.dir.ca.gov/dlse/FAQ_MinimumWage.htm | Match |
| ULA: 4% above $5,400,000; 5.5% at/above $10,900,000; base 0.45% ($2.25/$500); thresholds indexed to Chained CPI | https://finance.lacity.gov/faq/measure-ula | Match |
| 10-yr Treasury 4.84% on 2026-11-05 | https://fred.stlouisfed.org/series/DGS10 | Match |
| Capital-gain rates 0/15/20% (2025 thresholds); §1250 max 25% | https://www.irs.gov/taxtopics/tc409 | Match |
| LAUSD 497,105, rank 1; statewide 5,731,260 | https://www.cde.ca.gov/ds/ad/ceflargesmalldist.asp | Match |
| Palisades: 23,448 acres; 6,845 structures destroyed | https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire | Match |

## Not re-fetched this session (carried from prior verified records)

Prop 13 levy/cap (LA County Assessor), §1031/Form 8824 (IRS), CA FTB ordinary-income
treatment, CAL FIRE Eaton, USGS ShakeOut, CDE English-learner count, JACK on Track
150–200 closures / ~1% annual rate. These were verified 2026-11-08 by prior sessions
(see `research/VERIFICATION-2026-11-08.md`) and their source URLs are unchanged.
No discrepancy was found in any row re-fetched above.

## Integrity checks (2026-11-10, local)

- `scripts/build.py` + `scripts/validate.py`: PASS — 141 rows, 12 pages.
- `tools/check_site.py`, `tools/linkcheck.py`, `tools/check_links.py`: PASS.
- `tools/pii_scan.py`: PASS — 84 files, 0 findings.
- `scripts/stage_pages.py`: PASS — staged artifact (32 entries) has no account
  handle, no PII; every body row carries an official source link.
- Live site https://wingbangboozle1-lang.github.io/Jack3/ fetched and confirmed
  serving the curated dashboard (Pages status: built).

## Irregularities flagged

1. **K-IR-01 (carried):** 26 HTML files in *excluded* companion layers
   (`decision-file/`, `pages/`, etc.) render the repository account handle.
   Not in the published artifact. Left for layer owners; does not block.
2. **Stale open PRs #22, #26, #31, #32** from prior sessions remain open.
   Not this session's branches; not touched.
3. No new discrepancies found. No values changed.
