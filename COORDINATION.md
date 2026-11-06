# COORDINATION.md — Shared Task Board

Repo: wingbangboozle1-lang/Jack3 (branch `arena/28eacae6-jack3`)
Purpose: coordinate parallel agent sessions working on this repository.
Rule: never start a task another session has claimed. Keep scopes non-overlapping.
Claim a task by writing your session ID + file scope, then commit and push immediately.
`needs review` items are published on the "Flagged for Review" page and do not block anything.
If a session crashes or its claim is >60 minutes old with no commits, another session may take over (log the handoff).

Session ID: arena-28eacae6 (this session). Note: platform constraint — all work happens on branch `arena/28eacae6-jack3`; PR is opened from this branch to `main`.

## Task Board

| # | Task | Status | Owner | File scope | Notes |
|---|------|--------|-------|------------|-------|
| 1 | Repo review (README only, initial commit) + create COORDINATION.md | done | arena-28eacae6 | COORDINATION.md, repo root | Repo contained only README.md ("# Jack3") + git metadata. Nothing to line-audit except README. |
| 2 | Research: Jack in the Box Inc (tenant) — SEC 10-K FY2025 | in progress | arena-28eacae6 | research/tenant.md, data/tenant.json | Sources: sec.gov only. |
| 3 | Research: LA metro/city demographics, income, schools, population projections | in progress | arena-28eacae6 | research/area.md, data/area.json | Official: census.gov, dof.ca.gov, cde.ca.gov, bls.gov, fred.stlouisfed.org (republishes BLS/Census). |
| 4 | Research: rates, cap-rate context, FHFA HPI, hazards (fire/seismic/flood) | in progress | arena-28eacae6 | research/rates-hazards.md, data/rates-hazards.json | Official: fred.stlouisfed.org, treasury.gov, fire.ca.gov, fema.gov, usgs.gov. |
| 5 | Anonymization pass: no personal info / no specific property address on site or in repo | done (rule set) | arena-28eacae6 | all | Property referred to as "the Property" / "Central Los Angeles NNN Jack in the Box". No owner identity, no address. |
| 6 | Site: static dashboard in docs/ (landing + category subpages + tables) | unclaimed -> claimed next | arena-28eacae6 | docs/**, tools/**, data/** | GitHub Pages serves from docs/ on main. |
| 7 | Verification pass: every table row has official source link or is flagged blank | unclaimed | arena-28eacae6 | data/**, docs/** | Flagged rows go on Flagged for Review page. |
| 8 | Final integration: build, link check, gh-pages enable, PR, merge, confirm deploy | unclaimed | arena-28eacae6 | docs/**, .github/**, COORDINATION.md | PR from arena/28eacae6-jack3 to main. |

## Status log

- 2026-11-06 — Commit `0c9e609` contains only README.md ("# Jack3"). No code to audit. No credentials, no PII present.
- 2026-11-06 — Privacy rule applied: the subject property (NNN Jack in the Box, Central LA, term expiring 2030–2035) is anonymized throughout; no street address, no owner details, no listing URLs will be published.
- Note on branches: this session is restricted to `arena/28eacae6-jack3`; work is done there, then a single PR is opened to `main`. No other branches will be created or pushed.
