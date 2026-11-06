# COORDINATION.md — Shared Task Board

Repo: `wingbangboozle1-lang/Jack3` | Branch convention: `session-<id>/<task>`
Session active in this checkout: `ff406d61` on branch `arena/ff406d61-jack3`.

## Rules (from project brief)
- Claim a task by writing session ID + file scope here, commit + push immediately.
- Never start a task another session has claimed. Keep scopes non-overlapping.
- Shared outputs (table data, site index/nav) changed only by final integration session.
- Small frequent commits; `git pull --rebase` before every push.
- Stale claim (>60 min, no commits) may be taken over with a log note.
- Never mark verified without checking against an official source + link.

## Tasks

| # | Task | Status | Owner | Files / Scope | Sources / Verification | Irregularities |
|---|------|--------|-------|---------------|------------------------|----------------|
| T1 | Coordination board + repo review | done | ff406d61 | `COORDINATION.md` | Repo had only `README.md` at `0c9e609`; no other sessions active | None |
| T2 | Research: geography, demographics, income (Census) | done | ff406d61 | `research/demographics.md` | Census QuickFacts (all 4 chunks fetched) + LA EWDD/DOF report; line-by-line links | F1, F2 flagged |
| T3 | Research: employment, job growth, economy (BLS/BEA/EDD/Fed) | done | ff406d61 | `research/economy.md` | EDD Sept-2026 PDF, BEA/FRED, BLS CPI, Fed FOMC statement (fetched), DIR AB1228, LA28/IPC | F3, F4 flagged |
| T4 | Research: schools (CDE/LAUSD) | done | ff406d61 | `research/schools.md` | CA School Dashboard graduation 2019–2025; Census attainment | F5, F6 flagged |
| T5 | Research: Jack in the Box corporate + NNN lease (SEC 10-K) | done | ff406d61 | `research/corporate-lease.md` | FY2025 10-K (Item 1 + financials fetched) + official IR release 4/23/2025 | F7, F8, F9 flagged |
| T6 | Research: risks incl. black swan (USGS/CalFire/FEMA/NOAA) | done | ff406d61 | `research/risks.md` | USGS UCERF3 + Jan-2025 fires, CRS IF12871, LA County 2025 AHMP + Board docs | F10, F11, F12 flagged |
| T7 | Research: decision analysis sell vs renew + projections | done | ff406d61 | `research/decision.md` | Framework from verified inputs only; numeric answer blocked on F4/F7–F9/F11 | See flagged |
| T8 | Site build: landing + subpages + tables + flagged page | done | ff406d61 | `docs/**` | 10 pages + CSS; every row sourced; internal-link check passed, 0 broken | None |
| T9 | Final integration: merge, re-verify line by line, links check, Pages deploy | in progress | ff406d61 | COORDINATION.md, PR | Re-verified: all values trace to research/*.md official links | None |

## Claims Log
- 2026-11-06 ff406d61: Created board. Repo review: fresh repo, only `README.md` ("# Jack3"). No other sessions present; claiming T1–T9 sequentially in this session (single active session, no conflicts).

## Handoffs / Conflicts
- None.

## PR / Merge Record
- (pending)
