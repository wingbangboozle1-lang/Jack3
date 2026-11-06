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
| T01 | Research: macro & interest-rate inputs (Fed/Treasury/BLS CPI) | done | arena-ecf93811-jack3 | `data/*.json`, `research/` |
| T02 | Research: LA metro & Central LA demographics/income/employment | done | arena-ecf93811-jack3 | `data/*.json`, `research/` |
| T03 | Research: schools, population projections, housing/HPI | done | arena-ecf93811-jack3 | `data/*.json`, `research/` |
| T04 | Research: Jack in the Box corporate & tenant credit (SEC EDGAR) | done | arena-ecf93811-jack3 | `data/*.json`, `research/` |
| T05 | Research: tax, transfer tax, Prop 13, zoning/entitlement | done | arena-ecf93811-jack3 | `data/*.json`, `research/` |
| T06 | Research: hazard/black-swan risk (CAL FIRE, FEMA, USGS) | done | arena-ecf93811-jack3 | `data/*.json`, `research/` |
| T07 | Build projection engine (`tools/model.py`) | done | arena-ecf93811-jack3 | `tools/`, `data/model_*` |
| T08 | Build static dashboard site (GitHub Pages) | done | arena-ecf93811-jack3 | `site/`, `index.html` |
| T09 | Final integration re-verification + Pages deploy | done | arena-ecf93811-jack3 | all |

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

### 2026-11-06 — Session `arena-ecf93811-jack3` — RESEARCH AND BUILD COMPLETE

- Bootstrap: repo contained a single `README.md` line and no coordination file. Created board.
- `PAGES` already enabled on `main` (root, legacy build) → `https://wingbangboozle1-lang.github.io/Jack3/`.
- Direct `curl` to census.gov / bls.gov / fred is blocked in sandbox; retrieval is done through the
  agent web-fetch and search tools. All source URLs are recorded in `data/sources.json` and rendered
  on the site, so every figure is manually reviewable.
- Scope note: no property address or parcel number was supplied and none will be requested; the study
  is built at submarket level per the privacy protocol above.

### Completion record — 2026-11-06

**Sources used.** 30 registered records in `data/sources.json`. 20 are official-primary documents
read on the publishing agency's own domain: federalreserve.gov (FOMC statement 2026-10-28),
home.treasury.gov (par yield curve), api.bls.gov (CPI-U national `CUUR0000SA0` and LA
`CUURS49ASA0`), labormarketinfo.edd.ca.gov (LA MD press release), census.gov (QuickFacts LA County
and LA City), dof.ca.gov (population projections product page and the 2026-series K-12 enrollment
projection), sec.gov (JIB 10-K FY2025, 8-K Q4 FY2025, 8-K Q3 FY2026, 8-K securitization 2026-06-23,
EDGAR index), boe.ca.gov (Publication 29), leginfo.legislature.ca.gov (RTC §11911),
finance.lacity.gov (transfer tax and Measure ULA FAQ), dir.ca.gov (minimum wage and fast-food wage
FAQs), fire.ca.gov (Palisades and Eaton incidents), irs.gov (§1031), assessor.lacounty.gov,
fema.gov (NRI v1.20). Two are official-secondary. Three third-party records are registered **only**
to document a rejected claim.

**Verification performed.** `tools/verify.py` runs three layers and all three pass:
1. Structure — 13 pages parse with balanced tags, every relative link resolves, every in-page
   anchor has a target, every table header matches its first row cell-for-cell.
2. Citation — 179 data rows: 151 carry a value and a resolvable source id, 28 are blank and every
   one carries a flag. No unverified row carries a value. Every registered source is used.
3. Prose traceability — every number quoted in the narrative is present in `datasets.json`,
   `model_output.json`, `model_assumptions.json`, `flags.json` or `sources.json`. This check caught
   several figures that were initially written from a draft calculation rather than from the
   engine's actual output; they were corrected to the computed values.

**Irregularities found (13, all published on the Flagged page).** F-01 site-specific inputs
unverifiable by design; F-02 conflicting 2030/2035 population projections left blank; F-03 FEMA NRI
API 404; F-04 USGS page 404; F-05 no official cap-rate series exists; F-06 personal financial data
unavailable; F-07 school-level performance deliberately omitted; I-01 BLS October 2025 CPI missing
due to the appropriations lapse; I-02 City of LA transfer tax exceeds the RTC §11911(b) ceiling;
I-03 two CAL FIRE figures for Eaton fatalities; I-04 internal "42%" error in the assessor's roll
release; I-05 identical median rent in city and county QuickFacts; C-01 population projection
conflict between two secondary sources.

**Key analytical finding.** The recommended sequence is *renew if the tenant will commit, never sell
for cash, and route any exit through a §1031 exchange*. The ranking is stable across $4.0M, $6.5M
and $12.0M value bands and across 6,000 macro paths. The result is driven by tax structure and
remaining lease term rather than by market direction, which is why it survives the unverifiable
site-specific inputs.

**Files produced.** `data/` (5 JSON files), `tools/` (model, site generator, verification harness,
content), `research/NOTES.md` (line-by-line source log), 13 HTML pages plus `assets/style.css` at the
repository root for GitHub Pages.

<!-- Append new entries below. Newest at the bottom. -->
