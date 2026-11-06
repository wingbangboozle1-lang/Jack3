# COORDINATION.md — Shared Task Board (Jack3)

Two sessions worked this repository in parallel on 2026-11-06. Both sections are preserved verbatim (with status markers updated during integration). Branch note: session `arena-796b983f-jack3` works on `arena/796b983f-jack3`; session `5cb84cd0` worked on `arena/5cb84cd0-jack3` and merged to `main` via PR #1.

## Integration record (2026-11-06, session `arena-796b983f-jack3`)

- Parallel session `5cb84cd0-jack3` completed first and merged **PR #1** ("Publish privacy-safe net lease decision research dashboard") to `main`. Its site is the repository-root workspace: evidence register (`data/evidence.json`), deterministic build (`scripts/build.py`) and validation (`scripts/validate.py`), GitHub Action `.github/workflows/validate.yml`.
- Session `arena-796b983f-jack3` had built an independent deep-dive decision brief. To avoid overwriting the merged workspace, all of its pages/assets were moved to **`/brief/`** (`brief/index.html` … `brief/flagged.html`, `brief/assets/`) with breadcrumb links back to the main workspace (`../index.html`).
- Root `index.html` (5cb84cd0's generated file) is intentionally **not hand-edited**, except one additive bridge badge linking to `brief/` is added to `scripts/build.py` and the generated `index.html` so the workspace links to the deep-dive brief (logged here; additive only).
- Conflicts resolved during merge: `README.md` (kept combined version: workspace docs + `/brief/` section) and this file (both boards preserved, this section added).
- `tools/check_site.py` validates the `/brief/` site (internal links resolve, no localhost, noopener present). `scripts/validate.py` (5cb84cd0) remains the validator for the root workspace and its generated pages; it is non-recursive (`Path('.').glob('*.html')`) and does not scan `/brief/`.
- No personal information in either site (grep-verified by both sessions). Flagged items are published on both `review.html` (workspace) and `brief/flagged.html` (brief) and do not block merge.
- GitHub Pages: served from `main` root; the brief is live at `/Jack3/brief/` once this branch merges. PR link and merge result recorded at the bottom of this file.

## Board A — Session `5cb84cd0-jack3` (completed, merged via PR #1)

Session: `5cb84cd0` · started 2026-11-06 UTC. Claimed the main workspace scope and the final integration of the root site.

| Task | Status | Owner | File scope |
|---|---|---|---|
| Official-source research, privacy review, dashboard, automated validation and final integration | done | 5cb84cd0 | index.html, assets/, data/, scripts/, .github/, README.md, COORDINATION.md, research/ |

### Log (verbatim)
- 2026-11-06: Inspected initial repository: README only; no existing data, application, or competing claims. Property identity, lease, financials and exact location absent. Do not research owner identities or publish personal information.
- Initial claim pull used the not-yet-created remote session ref and failed; rebased on origin/main instead, then successfully pushed the claim to the assigned session branch. No conflict or work loss.
- Completed manual inspection of 11 official/primary sources, captured field-level provenance in data/evidence.json and verification notes in research/VERIFICATION.md. All government statistics and issuer figures are labeled by geography and period. Conditional analysis is not labeled verified.
- Built nine static responsive pages with no executable third-party assets or private data. Flagged missing lease, financial, parcel, local school/traffic and hazard inputs on review.html; these are needs-review items and do not block publication. A calibrated parcel forecast is unavailable and numerical predictions remain blank.
- Validation initially flagged the word “analytics” in the privacy disclosure; narrowed the check to actual prohibited vendor/embed patterns. Source-row, local-link, blank-value and deterministic build validation pass.
- Sources: https://www.census.gov/quickfacts/losangelescitycalifornia ; https://www.census.gov/quickfacts/losangelescountycalifornia ; https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf ; remaining official hazard, school, planning, tax, labor and issuer links are listed individually in data/evidence.json and sources.html.

## Board B — Session `arena-796b983f-jack3` (deep-dive decision brief, this branch)

**Branch policy:** works exclusively on `arena/796b983f-jack3` (platform-assigned). The brief's `session-<id>/<task>` convention noted; this session may not create/push other branches. Commits pushed; merges to `main` only via PR.

| # | Task | Status | Owner | Files / Scope |
|---|------|--------|-------|---------------|
| 0 | Create coordination board (this file, earlier revision) | done | arena-796b983f-jack3 | COORDINATION.md |
| 1 | Research: demographics/income/population/schools/jobs (official sources) | done | arena-796b983f-jack3 | research/RESEARCH.md |
| 2 | Research: NNN economics, sell vs renew, Measure ULA | done | arena-796b983f-jack3 | research/RESEARCH.md, brief/decision.html |
| 3 | Research: risk register incl. black swans (wildfire Eaton/Palisades, AP faults, 1992 unrest) | done | arena-796b983f-jack3 | brief/risk-analysis.html |
| 4 | Research: Jack in the Box Inc. tenant credit signals (IR release 2025-11-19 verified live) | done | arena-796b983f-jack3 | brief/decision.html |
| 5 | Build static decision-brief site | done | arena-796b983f-jack3 | brief/*.html, brief/assets/ |
| 6 | Verification pass — check_site.py; sources typed Official/Industry/Mirror/Unverified | done | arena-796b983f-jack3 | tools/check_site.py |
| 7 | Integration: merge main, /brief/ restructure, PR to main, merge, enable/confirm Pages | in progress | arena-796b983f-jack3 | brief/, README.md, COORDINATION.md, root bridge in index.html + scripts/build.py |
| 8 | Publish Flagged for Review page | done | arena-796b983f-jack3 | brief/flagged.html |

### Sources (summary of verification performed)
- Live-verified 2026-11-06 via fetch: Jack in the Box Q4/FY2025 earnings release (investors.jackinthebox.com) — SSS −7.4% Q4 / −4.2% FY25 confirmed; CA School Dashboard 2025 LAUSD (caschooldashboard.org) — 86.5% grad rate, 369,830 enrollment, 21.9% chronic absenteeism confirmed; US Treasury Daily Par Yield Curve page is the official .gov resource (current-month table renders via JS).
- EDD labor figures via LA Almanac + LA Business Journal (official EDD data, secondary reporting); SCAG 2025 Regional Economic Analysis PDF (official statutory agency).
- Census ACS figures reached via labeled third-party mirrors (Point2Homes, Data USA, US Civic Data, Census Reporter, Civic Data Atlas, Data Commons) — all tagged **Mirror**; primary links (census.gov QuickFacts) provided; flagged B-01…B-05.
- Measure ULA rates from City of LA Office of Finance (official) via 2026 explainers; city base DTT left blank (C-05); county DTT flagged (C-06); 2026-07-01 tier indexation flagged (C-04).
- Jan 2025 wildfire losses from LA County official fact sheet (Eaton 14,021 ac / 9,414 structures / 19 deaths; Palisades 23,448 ac / 6,837 structures / 12 deaths; contained 2025-01-31).
- Cap rates (STNL mean 6.5% M&M; JIB ~5.0–6.0% broker quote) are INDUSTRY quotes — labeled, never presented as government data.

### Irregularities found (full detail on `brief/flagged.html`)
1. Census figures inconsistent across mirrors (vintages) — labeled, not blended (B-01…B-05, C-01…C-03).
2. Measure ULA 2026-07-01 thresholds ($5.4M/$10.9M) from secondary sources citing Office of Finance — written confirmation needed (C-04).
3. LA City base transfer tax unconfirmable; county DTT conflicting ($0.55 vs $1.10 per $1,000) — blank / flagged (C-05, C-06).
4. DTLA 2040 growth figures ULI-reported; City adoption documents not fetched — flagged B-06.
5. Schools reported LAUSD-wide; attendance-boundary schools unknown without APN — flagged C-07.
6. Exact lease date, rent, escalation, guarantor, unit P&L — owner input required; projection defaults labeled illustrative (A-01…A-10, D-01…D-06).
7. SEC figures ($1.5B revenue / $270.9M Adj. EBITDA) from contested PRE 14A; 10-K is primary — flagged B-15.
8. 10Y Treasury 4.89–4.90% (2026-11-04) corroborated by three trackers of Treasury data; page renders table via JS.
9. Duplicate work with session 5cb84cd0 detected after merge: resolved by moving this site to /brief/ (see Integration record); no root content discarded.

### Activity log (Board B)
- 2026-11-06 — Board created (b6cf35d); research + site built; tools/check_site.py passed (then 9 pages / 195 refs; after /brief/ move: 9 pages / 204 refs).
- 2026-11-06 — Parallel merge of PR #1 detected (origin/main moved 0c9e609 → a47bf0d). /brief/ restructure committed (9c1f7e0); origin/main merged; README.md + COORDINATION.md conflicts resolved preserving both sessions' work.
- 2026-11-06 — Root bridge badge added to scripts/build.py + regenerated index.html (additive, logged here); PR to main opened; merge result recorded below.

## PR & merge record
- PR #1 (session 5cb84cd0): https://github.com/wingbangboozle1-lang/Jack3/pull/1 — MERGED to main 2026-11-06 (a47bf0d).
- PR #2 (this session): to be recorded upon merge. GitHub Pages confirmation to be recorded upon deploy.
