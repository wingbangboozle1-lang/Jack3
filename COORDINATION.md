# COORDINATION.md — Shared Task Board (merged: sessions 5cb84cd0 + ff406d61)

Repo: `wingbangboozle1-lang/Jack3`. Sessions started from README-only `0c9e609`
without seeing each other; scopes are non-overlapping and all three are preserved.
Surfaces: root workspace (Evidence register, session 5cb84cd0) · `docs/` dashboard (session ff406d61) · `brief/` deep-dive decision brief (session arena-796b983f).

## Session 5cb84cd0 — root-level dashboard (merged to main via PR #1)

File scope: `index.html`, `place.html`, `economy.html`, `tenant.html`, `risk.html`,
`model.html`, `decisions.html`, `sources.html`, `review.html`, `assets/`, `data/`,
`scripts/`, `.github/`, `README.md`, `research/VERIFICATION.md` — Status: done/merged.

Log (preserved verbatim):
- 2026-11-06: Inspected initial repository: README only; no existing data, application, or competing claims. Property identity, lease, financials and exact location absent. Do not research owner identities or publish personal information.
- Initial claim pull used the not-yet-created remote session ref and failed; rebased on origin/main instead, then successfully pushed the claim to the assigned session branch. No conflict or work loss.
- Completed manual inspection of 11 official/primary sources, captured field-level provenance in data/evidence.json and verification notes in research/VERIFICATION.md. All government statistics and issuer figures are labeled by geography and period. Conditional analysis is not labeled verified.
- Built nine static responsive pages with no executable third-party assets or private data. Flagged missing lease, financial, parcel, local school/traffic and hazard inputs on review.html; these are needs-review items and do not block publication. A calibrated parcel forecast is unavailable and numerical predictions remain blank.
- Validation initially flagged the word "analytics" in the privacy disclosure; narrowed the check to actual prohibited vendor/embed patterns. Source-row, local-link, blank-value and deterministic build validation pass.
- Sources: https://www.census.gov/quickfacts/losangelescitycalifornia ; https://www.census.gov/quickfacts/losangelescountycalifornia ; https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf ; remaining official hazard, school, planning, tax, labor and issuer links are listed individually in data/evidence.json and sources.html.

## Session ff406d61 — research + docs/ dashboard (branch arena/ff406d61-jack3, PR #2)

| # | Task | Status | Owner | Files / Scope | Sources / Verification | Irregularities |
|---|------|--------|-------|---------------|------------------------|----------------|
| T1 | Coordination board + repo review | done | ff406d61 | `COORDINATION.md` (merged section only) | Repo review at start; other session discovered at merge time | None |
| T2 | Research: geography, demographics, income (Census) | done | ff406d61 | `research/demographics.md` | Census QuickFacts (all 4 chunks fetched) + LA EWDD/DOF report; line-by-line links | F1, F2 flagged |
| T3 | Research: employment, job growth, economy (BLS/BEA/EDD/Fed) | done | ff406d61 | `research/economy.md` | EDD Sept-2026 PDF, BEA/FRED, BLS CPI, Fed FOMC statement (fetched), DIR AB1228, LA28/IPC | F3, F4 flagged |
| T4 | Research: schools (CDE/LAUSD) | done | ff406d61 | `research/schools.md` | CA School Dashboard graduation 2019–2025; Census attainment | F5, F6 flagged |
| T5 | Research: Jack in the Box corporate + NNN lease (SEC 10-K) | done | ff406d61 | `research/corporate-lease.md` | FY2025 10-K (Item 1 + financials fetched) + official IR release 4/23/2025 | F7, F8, F9 flagged |
| T6 | Research: risks incl. black swan (USGS/CalFire/FEMA/NOAA) | done | ff406d61 | `research/risks.md` | USGS UCERF3 + Jan-2025 fires, CRS IF12871, LA County 2025 AHMP + Board docs | F10, F11, F12 flagged |
| T7 | Research: decision analysis sell vs renew + projections | done | ff406d61 | `research/decision.md` | Framework from verified inputs only; numeric answer blocked on F4/F7–F9/F11 | See flagged |
| T8 | Site build: landing + subpages + tables + flagged page | done | ff406d61 | `docs/**` | 10 pages + CSS; every row sourced; internal-link check passed, 0 broken | None |
| T9 | Final integration: merge, re-verify, links check, Pages deploy | done | ff406d61 | COORDINATION.md, PR | Re-verified: all values trace to research/*.md official links | None |

Claims log:
- 2026-11-06 ff406d61: Claimed T1–T9; no other sessions visible at claim time.

## Session arena-796b983f — brief/ deep-dive decision brief (branch arena/796b983f-jack3)

Session ID `arena-796b983f-jack3`; works exclusively on `arena/796b983f-jack3` per platform constraint. Third parallel session discovered only at push time (after a47bf0d), then again when main moved to f6dc00b. No existing claims were disturbed; root workspace and docs/ untouched except the additive bridge noted below.

| # | Task | Status | Owner | Files / Scope |
|---|------|--------|-------|---------------|
| 0 | Coordination board | done | arena-796b983f | COORDINATION.md |
| 1 | Research: demographics/income/population/schools (official sources) | done | arena-796b983f | research/RESEARCH.md |
| 2 | Research: NNN economics, sell vs renew, Measure ULA | done | arena-796b983f | brief/decision.html |
| 3 | Research: risk register incl. black swans (Eaton/Palisades fires, AP faults, 1992 unrest) | done | arena-796b983f | brief/risk-analysis.html |
| 4 | Research: Jack in the Box tenant credit (IR release 2025-11-19 fetched live; 10-K) | done | arena-796b983f | brief/decision.html |
| 5 | Site build: dashboard + subpages + projection calculator (under /brief/) | done | arena-796b983f | brief/* |
| 6 | Verification pass (tools/check_site.py, source typing, grep for PII) | done | arena-796b983f | tools/check_site.py |
| 7 | Integration: merge main ×2, /brief/ restructure, cross-links, PR to main, Pages confirmation | in progress | arena-796b983f | brief/, README.md, COORDINATION.md, index.html + scripts/build.py bridge |
| 8 | Flagged for Review page | done | arena-796b983f | brief/flagged.html |

### Sources (verification performed)
- Live-verified via fetch: JIB Q4/FY2025 earnings release (SSS −7.4% Q4 / −4.2% FY25; unit counts; closure program; FY26 guide) — investors.jackinthebox.com. CA School Dashboard 2025 LAUSD (86.5% grad; 369,830 enrolled; 21.9% absenteeism) — caschooldashboard.org. US Treasury Daily Par Yield Curve page (official .gov; current-month table renders via JS).
- Census ACS figures via labeled mirrors (Point2Homes, Data USA, US Civic Data, Census Reporter) — tagged Mirror on-site; primary census.gov links given; flagged B-01…B-05.
- EDD labor data via LA Almanac/LABJ (secondary, EDD primary); SCAG 2025 Regional Economic Analysis PDF; LA County Assessor roll $2.176T (+3.91%, 2025) via CalTax; Measure ULA via City Office of Finance (official) with secondary explainers; Eaton/Palisades losses from LA County official fact sheet; STNL/JIB cap rates are INDUSTRY quotes (Marcus & Millichap via CRE Daily; Solid Investments broker) — labeled, never presented as government data.

### Irregularities found → see brief/flagged.html (A-01…A-10, B-01…B-15, C-01…C-10, D-01…D-06)
Mirror inconsistencies (vintages), ULA 2026-07-01 tier indexation from secondary sources, LA city base transfer tax unconfirmable (blank), county DTT conflicting (flagged), DTLA 2040 figures ULI-reported, schools LAUSD-wide only (boundary unknown without APN), JIB PRE 14A vs 10-K figure-definition differences, projection defaults labeled illustrative ($275k rent / 2.0% escalation placeholders).

### Log
- 2026-11-06: Created board; research + build complete; check_site.py PASS.
- 2026-11-06: Parallel PRs #1 and #2 discovered via origin/main moves (a47bf0d, f6dc00b). Site moved to /brief/ to coexist non-destructively (commit 9c1f7e0). COORDINATION.md combined across all three sessions; both other sessions' logs preserved verbatim. No file of another session was modified except: (a) additive bridge line in scripts/build.py template + regenerated root index.html linking to brief/ (ff406d61's cross-link request, now fulfilled: root ↔ docs/ ↔ brief/); both changes logged here.
- 2026-11-06: PR #3 (arena/796b983f-jack3 → main) opened; merge result + Pages confirmation recorded below upon completion.

## Handoffs / Conflicts
- 2026-11-06 arena-796b983f: Two consecutive parallel merges to main detected mid-task; rebased decision superseded by merge strategy to avoid force-push; conflicts limited to COORDINATION.md (combined, no work discarded) and README.md (combined workspace docs + /brief/ section). Request fulfilled (not edited beyond additive bridge): cross-link root dashboard ↔ brief/ (and docs/ ↔ root via the same badge).
- 2026-11-06 ff406d61: Request fulfilled — see above.

## PR / Merge Record
- PR #1 (5cb84cd0 → main): merged (a47bf0d).
- PR #2 (ff406d61 → main): merged (f6dc00b).
- PR #3 (arena/796b983f-jack3 → main): pending / see update below. GitHub Pages confirmation recorded in the follow-up commit.
