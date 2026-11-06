# COORDINATION.md — Shared Task Board

> Single source of truth for parallel agent sessions working in this repository.
> **Read this file before starting any work.**

## Session Identity

| Field | Value |
|---|---|
| Session ID | `arena-ecf93811-jack3` |
| Branch | `arena/ecf93811-jack3` |
| Worktree | `/home/user/Jack3` |
| Started | 2026-11-06 |
| Role | Research + build + **Final Integration** |

## Rules (recap)

1. Claim a task by writing session ID + file scope below, then **commit and push the claim immediately**.
2. Never start a task another session has claimed.
3. Keep scopes non-overlapping. Each session edits only its claimed files.
4. Need a file owned by another session? Log a request here instead of editing it.
5. Small, frequent commits. `git pull --rebase` before every push.
6. Merge conflict → stop, resolve without discarding other work, log it here.
7. Do not mark anything verified without checking it against an official source and linking it.
8. Shared outputs (table data, `index.html`, navigation) are changed only by the final integration session.
9. A claim >60 min old with no commits may be taken over; note the handoff.

## Status Legend

`unclaimed` · `in progress` · `done` · `needs review` (published on Flagged-for-Review page; does not block)

---

## Task Board

| ID | Task | Status | Owner | File Scope |
|---|---|---|---|---|
| T00 | Coordination board + repo conventions | done | arena-ecf93811-jack3 | `COORDINATION.md`, `.gitignore`, `README.md` |
| T01 | Research: macro & interest-rate inputs (Fed/Treasury/BLS CPI) | in progress | arena-ecf93811-jack3 | `data/*.json`, `research/` |
| T02 | Research: LA metro & Central LA demographics/income/employment | in progress | arena-ecf93811-jack3 | `data/*.json`, `research/` |
| T03 | Research: schools, population projections, housing/HPI | in progress | arena-ecf93811-jack3 | `data/*.json`, `research/` |
| T04 | Research: Jack in the Box corporate & tenant credit (SEC EDGAR) | in progress | arena-ecf93811-jack3 | `data/*.json`, `research/` |
| T05 | Research: tax, transfer tax, Prop 13, zoning/entitlement | in progress | arena-ecf93811-jack3 | `data/*.json`, `research/` |
| T06 | Research: hazard/black-swan risk (CAL FIRE, FEMA, USGS) | in progress | arena-ecf93811-jack3 | `data/*.json`, `research/` |
| T07 | Build projection engine (`tools/model.py`) | in progress | arena-ecf93811-jack3 | `tools/`, `data/model_*` |
| T08 | Build static dashboard site (GitHub Pages) | in progress | arena-ecf93811-jack3 | `site/`, `index.html` |
| T09 | Final integration re-verification + Pages deploy | in progress | arena-ecf93811-jack3 | all |

> **Note on parallelism:** as of this run the board is fully owned by `arena-ecf93811-jack3`; no
> other session has posted a claim. Any later session must add its own row before editing files.

---

## Privacy Protocol (binding for all sessions)

The property owner / tenant contact / parcel-specific identifiers are **personal information**.

- Do **not** commit: street address, parcel number (AIN), owner name, landlord/tenant contact names,
  phone numbers, emails, personal financial figures, or anything that identifies an individual.
- Use placeholders: `SP-01` (Subject Property), `OWNER-A`, `PARCEL-REDACTED`.
- Analysis is performed at **submarket / ZIP-cluster / county** granularity.
- Any PII discovered during research is **internal-only** and must be recorded *nowhere* in this repo,
  including commit messages and this file.

---

## Log

### 2026-11-06 — Session `arena-ecf93811-jack3`

- Bootstrap: repo contained a single `README.md` line and no coordination file. Created board.
- `PAGES` already enabled on `main` (root, legacy build) → `https://wingbangboozle1-lang.github.io/Jack3/`.
- Direct `curl` to census.gov / bls.gov / fred is blocked in sandbox; retrieval is done through the
  agent web-fetch and search tools. All source URLs are recorded in `data/sources.json` and rendered
  on the site, so every figure is manually reviewable.
- Scope note: no property address or parcel number was supplied and none will be requested; the study
  is built at submarket level per the privacy protocol above.

<!-- Append new entries below. Newest at the bottom. -->
