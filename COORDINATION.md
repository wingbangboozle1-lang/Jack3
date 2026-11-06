# COORDINATION.md — Shared Task Board (Jack3)

**Project:** Jack in the Box NNN Lease — Sell vs. Renew Decision Analysis (Central Los Angeles)
**Branch policy:** Session works exclusively on `arena/796b983f-jack3` (platform-assigned). The brief's `session-<id>/<task>` convention noted; this session may not create/push other branches.
**Session ID:** `arena-796b983f-jack3`
**Last updated:** 2026-11-06 (UTC)

## Task Board

| # | Task | Status | Owner | Files / Scope |
|---|------|--------|-------|---------------|
| 0 | Create COORDINATION.md task board | done | arena-796b983f-jack3 | COORDINATION.md |
| 1 | Research: demographics/income/population/schools/jobs (official sources) | done | arena-796b983f-jack3 | research/RESEARCH.md |
| 2 | Research: NNN economics, sell vs renew, Measure ULA | done | arena-796b983f-jack3 | research/RESEARCH.md, decision.html |
| 3 | Research: risk register incl. black swans | done | arena-796b983f-jack3 | risk-analysis.html |
| 4 | Research: Jack in the Box Inc. tenant credit signals | done | arena-796b983f-jack3 | decision.html, RESEARCH.md |
| 5 | Build static GitHub Pages site (dashboard + subpages) | done | arena-796b983f-jack3 | *.html, assets/ |
| 6 | Verification pass (links resolve; sources typed; unverified → flagged) | done | arena-796b983f-jack3 | tools/check_site.py |
| 7 | Integration: PR to main, merge, enable Pages, confirm deploy | in progress | arena-796b983f-jack3 | repo root, gh |
| 8 | Publish Flagged for Review page | done | arena-796b983f-jack3 | flagged.html |

## Rules in force

- Every table row carries a source link; values that can't be confirmed are blank/flagged — never silently filled.
- No personal information anywhere on the site ("The Property" / "The Tenant" / "Owner" only). Verified by grep: no emails/addresses/names present.
- `git pull --rebase` before every push; small frequent commits.
- Other sessions: do not edit files claimed above; log cross-scope requests here.

## Sources (summary of the verification performed)

- Live-verified 2026-11-06 via fetch: Jack in the Box Q4/FY2025 earnings release (investors.jackinthebox.com) — SSS −7.4% Q4 / −4.2% FY25 confirmed; CA School Dashboard 2025 LAUSD page (caschooldashboard.org) — 86.5% grad rate, 369,830 enrollment, 21.9% chronic absenteeism confirmed; US Treasury Daily Par Yield Curve page — official .gov resource confirmed (current-month table renders via JS).
- EDD labor figures via LA Almanac + LA Business Journal (official EDD data, secondary reporting); SCAG 2025 Regional Economic Analysis PDF (official statutory agency).
- Census ACS figures reached through labeled third-party mirrors (Point2Homes, Data USA, US Civic Data, Census Reporter, Civic Data Atlas, Data Commons) — all tagged **Mirror** on-site; primary links (census.gov QuickFacts) provided; flagged B-01…B-05.
- Measure ULA rates from City of LA Office of Finance (official) via 2026 explainers; tagged official with verification note C-04; city base DTT left blank (C-05); county DTT flagged (C-06).
- Jan 2025 wildfire losses from LA County official fact sheet (Eaton 14,021 ac/9,414 structures/19 deaths; Palisades 23,448 ac/6,837 structures/12 deaths).
- Cap rates (STNL 6.5%, JIB ~5.0–6.0%) are INDUSTRY quotes (Marcus & Millichap via CRE Daily; Solid Investments broker) — labeled Industry, never presented as government data.

## Irregularities found (full detail on site /flagged.html)

1. Census figures inconsistent across mirrors (vintage differences) — labeled, not blended (B-01…B-05, C-01…C-03).
2. Measure ULA 2026-07-01 thresholds ($5.4M/$10.9M) from secondary sources citing Office of Finance — needs written confirmation (C-04).
3. LA City base transfer tax unconfirmable; county DTT conflicting ($0.55 vs $1.10 per $1,000) — left blank / flagged (C-05, C-06).
4. DTLA 2040 growth numbers (ULI-reported; City adoption docs not fetched) — flagged B-06.
5. Schools reported LAUSD-wide; attendance-boundary schools unknown without APN — flagged C-07.
6. Exact lease date, rent, escalation, guarantor, unit P&L — owner input required; projection defaults clearly labeled illustrative (A-01…A-10, D-01…D-06).
7. SEC figures (revenue $1.5B / Adj. EBITDA $270.9M) from contested PRE 14A; 10-K is primary (S-22) — flagged B-15.
8. Treasury URL carries a current-month table rendered via JS; figure (4.89–4.90% 10Y, 2026-11-04) corroborated by three trackers of Treasury data.

## Activity Log

- 2026-11-06 — Board created (b6cf35d). Research performed across official/industry sources (this entry). Site built: 9 pages + assets; tools/check_site.py passes (9 pages, 195 internal refs, 0 broken). README rewritten. No PII present.
- 2026-11-06 — PR to `main` to be opened from `arena/796b983f-jack3`; GitHub Pages to be enabled from `main` root; PR link and merge result to be recorded below and in a follow-up commit.
