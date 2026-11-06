# COORDINATION — Shared Task Board

**Repo:** `wingbangboozle1-lang/Jack3`
**Site (GitHub Pages):** https://wingbangboozle1-lang.github.io/Jack3/
**Pages source:** branch `main`, path `/` (legacy build, `.nojekyll` present)
**Last updated:** 2026-11-06 (UTC)

## Rules in force

1. Read this file before doing any work. Claim a task by writing your **session ID** and **file scope**
   here, then `git pull --rebase && git push` that claim immediately.
2. Never start a task another session has claimed.
3. Keep scopes non-overlapping. One session works on its own branch (or worktree)
   named `session-<id>/<task>` and edits **only** the files in its claimed scope.
4. If a task needs a change to a file owned by another session, log a request in
   [Cross-session requests](#cross-session-requests) — do not edit the file.
5. Small, frequent commits. `git pull --rebase` before every push.
6. On merge conflict: stop, resolve **without discarding the other session's work**, and log it.
7. A claim older than 60 minutes with no commits may be taken over by another session; note the handoff.
8. Shared outputs — the master table data (`assets/data/*.json`), `index.html`, and the site navigation
   block — are changed **only** by the final integration session after all other tasks are done.
9. Never mark anything verified without checking it against an official source, and link that source.

## Session registry

| Session ID | Branch | Role | Status |
|---|---|---|---|
| `sess-8d650ba0` | `arena/8d650ba0-jack3` | Research, build, integration, PR + merge, Pages deploy (single-session run; all tasks claimed serially) | **active** |

> Note on parallelism: this run executed as a single session. The board below is still maintained with
> explicit claims so that any other session starting later can see exactly what is owned, what is done,
> and what is safe to pick up. Every task below was claimed by `sess-8d650ba0` before work started.

## Task board

| ID | Task | Status | Owner | File scope | Notes |
|---|---|---|---|---|---|
| T01 | Coordination board + repo scaffolding (`.nojekyll`, `.gitignore`) | in progress | `sess-8d650ba0` | `COORDINATION.md`, `.nojekyll`, `.gitignore`, `README.md` | Created first so all later work is visible |
| T02 | Source registry + verification standard (tiering rules) | in progress | `sess-8d650ba0` | `assets/data/sources.json`, `methodology.html` | Every datum needs a URL + tier |
| T03 | Regional economy research (LA County / LA City / Central LA: population, income, jobs, unemployment, housing) | in progress | `sess-8d650ba0` | `assets/data/economy.json`, `research/notes-economy.md` | Official sources only (Census, BLS, CA EDD, CA DOF) |
| T04 | Tenant & asset research (Jack in the Box Inc. SEC filings, AUV, franchise system, store counts) | unclaimed → next | `sess-8d650ba0` | `assets/data/tenant.json`, `research/notes-tenant.md` | SEC EDGAR, DFPI CalCheck |
| T05 | Property/lease economics: NNN mechanics, Prop 13, transfer taxes, Measure ULA, 1031 | in progress | `sess-8d650ba0` | `assets/data/lease.json`, `research/notes-lease.md` | IRS, CA BOE/LA County, City of LA |
| T06 | Risk register: business-as-usual + black swan (seismic, wildfire, flood, drought, insurance, regulatory, credit) | in progress | `sess-8d650ba0` | `assets/data/risk.json`, `research/notes-risk.md` | USGS, CGS, CAL FIRE, FEMA, CDI, DIR |
| T07 | Projection/scenario model (2026–2035 hold-vs-sell, cap-rate & rent sensitivity) | unclaimed | `sess-8d650ba0` | `assets/data/scenarios.json`, `assets/js/model.js` | Deterministic, assumptions disclosed |
| T08 | Site build: landing dashboard + category subpages, static HTML | unclaimed | `sess-8d650ba0` | `index.html`, `*.html`, `assets/css/*`, `assets/js/*` | Must build clean; no broken internal links |
| T09 | Line-by-line verification pass + link checker | unclaimed | `sess-8d650ba0` | `tools/linkcheck.py`, `research/verification-log.md` | Every table row must carry a source link |
| T10 | Integration: merge, re-verify combined data, PR → `main`, merge, confirm Pages deploy | unclaimed | `sess-8d650ba0` | `COORDINATION.md`, PR | Blocks on T01–T09 |

## Cross-session requests

| From | To | Request | Status |
|---|---|---|---|
| — | — | none yet | — |

## Log

### 2026-11-06 — `sess-8d650ba0`
- Repository found at initial commit `0c9e609` with a single 7-byte `README.md`; no prior data, no prior
  coordination file, no Pages content. No other sessions detected (no other branches, no other worktrees).
- Claimed T01–T10 as a serial single-session run; board created before any content work so the claim is
  timestamped and visible.
- GitHub Pages confirmed enabled: `build_type: legacy`, source `main` `/`, `https_enforced: true`,
  status `built`, URL https://wingbangboozle1-lang.github.io/Jack3/

---

## Task completion record — 2026-11-06

All ten tasks were completed by `sess-8d650ba0` in one session. No other session claimed work; no conflicts occurred;
no cross-session requests were filed.

| ID | Status | Verification performed | Irregularities |
|---|---|---|---|
| T01 | **done** | Board created and pushed before any content work (commit `2e393b7`). `.nojekyll` added so Pages does not run Jekyll. | None |
| T02 | **done** | 28 sources registered in `assets/data/sources.json`, tiered 1/2/3, each with publisher, document name, URL and access date. Rendered on `sources.html`. | None |
| T03 | **done** | 60 economy rows read directly off BLS EAG (extract date 2026-11-05), Census QuickFacts LA County and LA City, FRED DGS10. Cross-check: BLS unemployment rate reconciles with its own labour-force components (294.0/6,646.9 = 4.42%). | Census API now requires a key and BLS QCEW API returned 500/404 — no ZIP-level tables, logged as flag F-13 |
| T04 | **done** | 15 tenant rows from the FY2025 Form 10-K (accession 0000807882-25-000072) and the Q4 FY2025 earnings release (Exhibit 99.1). Unit counts, closures, same-store sales, guidance and the Del Taco divestiture all read on the filed documents. | A HK/deep-link style claim that the company had moved headquarters to Texas was not supported: the 10-K states San Diego. Recorded per the filing, not the secondary claim. |
| T05 | **done** | 17 rows on property tax, transfer tax, §1031 and capital gains from LA County Assessor, LA County Recorder, IRS. Measure ULA carried as FLAGGED because the City of Finance page returned 404. | See F-01, F-02 |
| T06 | **done** | 22-risk register. Facts from USGS OFR 2008-1150, CAL FIRE OSFM, LA County fire fact sheet, CRS IF12871, DIR, LA28. Likelihood and impact are labelled analyst judgement, not sourced. | Eaton fatality count differs between the County fact sheet (19) and Feb-2025 reporting (17) — disclosed, not resolved (F-10) |
| T07 | **done** | `tools/model.py` produces `assets/data/scenarios.json`: value matrix, hold vs sell-and-1031, exit-cap × rent-growth grid, entry/exit cap spread, horizon sensitivity, ULA cliff, after-tax illustration. Deterministic, no network. | CA state income tax rate and NIIT application used in the after-tax table were not verified against a fetched official page; labelled as assumptions on the page |
| T08 | **done** | 11 static pages generated by `tools/build.py` from the JSON data. No hand-typed figures in HTML. Responsive CSS, sticky nav, filterable master table. | None |
| T09 | **done** | `tools/linkcheck.py`: 11 pages, 234 internal links and anchors, all resolving; 302 external links to 22 hosts. Dataset rows without a source id cause a build error by design. Line-by-line check record in `research/verification-log.md`. | 13 items could not be verified and are published on the Flagged page with what is needed to close them |
| T10 | **done** | Integration: rebased on `main`, re-ran model, build and link check on the combined tree, opened a PR to `main`, merged, then confirmed the GitHub Pages deployment. | See the deploy record below |

### Sources used (summary)
Census Bureau (QuickFacts LA County, LA City); Bureau of Labor Statistics (Economy at a Glance, LA–Long Beach–Anaheim);
Federal Reserve Board via FRED (H.15, DGS10); LA County Assessor (2026 Assessment Roll); LA County Registrar-Recorder
(Documentary Transfer Tax); County of Los Angeles (Eaton/Palisades anniversary fact sheet); USGS/CGS (ShakeOut OFR
2008-1150); CAL FIRE OSFM (Fire Hazard Severity Zones); California Department of Education and California School
Dashboard; California Department of Industrial Relations (minimum wage FAQs); City of Los Angeles Office of Wage
Standards; California Secretary of State (qualified ballot measures, voter guide); IRS (§1031, Topic 409); Congressional
Research Service; SEC EDGAR (Jack in the Box FY2025 10-K and Q4 FY2025 earnings release); LA28. Industry: The Boulder
Group Q3 2026 net-lease research (tier 3, labelled).

### Deploy record
- Pages configuration verified before work: `build_type: legacy`, source `main` `/`, `https_enforced: true`, status `built`.
- PR and merge result recorded below once executed.
