# Line-by-line re-verification — 2026-11-10 (session `cd1d5bcb`)

**Scope.** The curated, currently published dashboard (root `index.html`, `economy`, `demographics`, `tenant`, `risk`,
`place`, `schools`, `decisions`, `taxes`, `model`, `review`, `sources`), the staged `dashboard/` companion, and the
live GitHub Pages site. No other session's scope was edited.

**Method.** Each load-bearing published figure was re-read directly from the linked official page on 2026-11-10 (UTC).
A row is marked *Confirmed* only when the page shows the same value with the same geography and period. Items that
could not be confirmed remain blank on the site and are listed on the Flagged for Review page. No value was inferred.

## 1. Load-bearing figures re-read on 2026-11-10

| Published value | Official source (re-fetched) | Result |
|---|---|---|
| LA city population 3,869,089; base 3,899,342; −0.8% (V2025, Jul-2025) | https://www.census.gov/quickfacts/losangelescitycalifornia | Confirmed |
| LA city median household income $81,939 (2024 USD); per capita $47,685 | same | Confirmed |
| LA city median gross rent $1,933; owner-occupied 36.0%; poverty 16.5% | same | Confirmed |
| LA city mean commute 30.7 min; density 8,304.2/sq mi; HS ≥ graduate 79.6%; bachelor's ≥ 38.5% | same | Confirmed |
| LA County population 9,694,934; base 10,017,414; −3.2% (V2025, Jul-2025) | https://www.census.gov/quickfacts/losangelescountycalifornia | Confirmed |
| Metro unemployment 4.4% (Sep-2026); LA County 4.5%; LA city 4.5%; California 5.1%; U.S. 4.0% | https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf (updated 2026-11-04) | Confirmed |
| Nonfarm payroll 6,282.1k, +30.2k / +0.5% YoY (Sep-2026, NSA); information −5.7%; education & health +3.8% (1,340.7k) | same | Confirmed |
| CPI-U all items +3.7% YoY Sep-2026 (LA metro and U.S.); energy +20.3% | same | Confirmed |
| ECI LA–Long Beach CSA +3.9% (Sep-2026) | same | Confirmed |
| Average weekly wage LA County $1,704 (Q1 2026, QCEW) | same | Confirmed |
| 10-year Treasury DGS10 4.84% on 2026-11-05 (series note: 4.86% on 2026-11-06, published 11-09) | https://fred.stlouisfed.org/series/DGS10 | Confirmed as dated on the page; see note N-1 |
| Fast-food minimum wage $20.00/hour from 2024-04-01 (AB 1228; 60+ establishment chains; franchisees covered) | https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm | Confirmed |
| State minimum wage $16.90/hour from 2026-01-01 | https://www.dir.ca.gov/dlse/FAQ_MinimumWage.htm | Confirmed |
| Measure ULA: closings after 2026-06-30 → 4% over $5,400,000; 5.5% at/above $10,900,000; base tax $2.25/$500 (0.45%); ULA on gross value incl. liens, base tax on net value excl. liens; thresholds indexed to Chained CPI | https://finance.lacity.gov/faq/measure-ula | Confirmed verbatim, including the gross-vs-net lien distinction published on the taxes page |
| Jack in the Box Q3 FY2026 (ended 2026-07-05): system S.S.S. −1.1% (co −0.9% / fr −1.2%); systemwide sales −1.4%; 4 openings / 17 closures; end-of-quarter 2,115 restaurants (149 company / 1,966 franchise); franchise-level margin 37.4% (vs 39.3%); franchisee bad-debt expense higher | https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx | Confirmed |
| Palisades Fire: 6,845 structures destroyed; active 24 days (2025-01-07 → 2025-01-31) | https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire | Confirmed |
| Eaton Fire: 9,419 structures destroyed; 19 confirmed civilian fatalities; active 24 days | https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire | Confirmed (total destroyed both fires: 16,264) |

## 2. Live-site sweep (2026-11-10, cache-busted fetches)

- `/` (Executive summary) — renders; recommendation unchanged; evidence boundary banner present.
- `/economy.html`, `/demographics.html`, `/tenant.html`, `/risk.html`, `/place.html`, `/schools.html`,
  `/decisions.html`, `/taxes.html`, `/model.html`, `/review.html`, `/sources.html` — all render; every table row
  carries its official source link; unverified cells are blank and carry `Unverified` labels.
- `/dashboard/` — renders; 185-row dataset intact; flagged page reachable at `/dashboard/flagged.html`.
- Root nav includes the additive `13 · Category dashboard` link; no broken links reported by the artifact checker.

## 3. Automated gates (run 2026-11-10 on this branch)

- `scripts/build.py` — exit 0 (deterministic; tree clean after rebuild)
- `scripts/validate.py` — PASS: 141 evidence rows; 12 pages
- `scripts/stage_pages.py` — PASS: staged artifact links and source-linked rows
- `tools/check_site.py` — ALL CHECKS PASSED (brief/ 9 pages, 213 references)
- `tools/linkcheck.py` — OK, no broken internal links or anchors
- `tools/check_links.py` — OK (official/primary hosts only)
- `tools/pii_scan.py` — OK: 84 files, 0 findings
- `_advisory_src/verify_advisory.py` — PASS (advisory remains withheld from Pages; repository copy intact)
- `_dashboard_src/verify.py` — PASS (incl. deterministic rebuild byte-identical)
- `git diff --exit-code -- '*.html'` — clean (build is byte-identical)

## 4. Repository and CI state of `main` (commit `4278c1a`, PR #33 merge)

- `Validate public research` on `main` succeeded (run 42534304796).
- `pages build and deployment` succeeded; Pages API `builds/latest` reports `status=built` for `4278c1a`
  (created 2026-11-08T23:15:38Z). Live site fetched successfully 2026-11-10.

## 5. Notes and irregularities

- **N-1 (staleness, not an error).** The site publishes DGS10 = 4.84% dated 2026-11-05. FRED now prints 4.86% for
  2026-11-06 (page updated 2026-11-09). The published cell is explicitly dated, so it remains accurate as published;
  any re-quote should move with the series.
- **N-2 (open PRs, reported not merged).** #4, #12, #22, #26, #31, #32 remain open. All report `mergeable=CONFLICTING`
  against `main`; #22 and #26 also have failing `validate` checks; #4, #12, #31, #32 are green but conflict. Merging them
  without rebase/resolution would risk the published site and is outside this session's authority. They remain for their
  owners or a later integration. `#12` only records a deployment note; `#31`/`#32` carry further integration changes that
  a later session may rebase and adopt.
- **N-3 (no defect found requiring a page change).** Nothing fetched on 2026-11-10 contradicts a published value. The
  `review.html` Flagged for Review page remains the correct place for the open gaps (property identity, lease, cap rates,
  parcel hazards, LA County transfer tax, LAUSD graduation rate, advisory withholding).
- **N-4 (scope discipline).** No file outside the claim in `COORDINATION.md` (`research/VERIFICATION-2026-11-10.md`, an
  appended board section) was created or edited by this session.
