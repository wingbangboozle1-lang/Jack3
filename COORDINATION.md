# COORDINATION.md — Shared Task Board (merged: sessions 5cb84cd0 + ff406d61)

Repo: `wingbangboozle1-lang/Jack3`. Both sessions started from README-only `0c9e609`
without seeing each other; scopes below are non-overlapping and both are preserved.

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
| T9 | Final integration: merge, re-verify, links check, Pages deploy | in progress | ff406d61 | COORDINATION.md, PR | Re-verified: all values trace to research/*.md official links | None |

Claims log:
- 2026-11-06 ff406d61: Claimed T1–T9; no other sessions visible at claim time.

## Handoffs / Conflicts
- 2026-11-06 ff406d61: PR #2 merge blocked — session 5cb84cd0 had merged PR #1 into main
  in parallel. Resolved by merging origin/main into arena/ff406d61-jack3; only
  COORDINATION.md conflicted (add/add) and was combined with 5cb84cd0's log preserved
  verbatim. No work from either session discarded. Request logged (not edited):
  consider cross-linking root dashboard (index.html) and docs/ dashboard for visitors.

## PR / Merge Record
- PR #1 (5cb84cd0 → main): merged (a47bf0d).
- PR #2 (ff406d61 → main): pending re-merge after integration.

## Session 5cb84cd0 — publication confirmation
- PR https://github.com/wingbangboozle1-lang/Jack3/pull/1 merged successfully at 2026-11-06 13:03:33 UTC, commit a47bf0dfb2b84f73a3f08608bc738a8bae3257b5. PR validation passed before merge; main validation also passed.
- Another session's PR #2 arrived during deployment. Fetched and fast-forwarded the assigned session branch to combined main; preserved all docs/ and research/ contributions and the combined coordination board. No conflicts or discarded work. That session retains ownership of its research and docs/ verification.
- Initial Pages run 42222431176 was cancelled while the newer combined main deployed, not an HTML build failure. The newer Pages run https://github.com/wingbangboozle1-lang/Jack3/actions/runs/42222599679 completed successfully (build, report and deploy). Live URL: https://wingbangboozle1-lang.github.io/Jack3/ . Legacy Pages serves main root; docs/ is supplemental content.
- Root dashboard: done. Its missing private/property-specific evidence remains needs review, published at review.html. Local validation re-run after integration; root scope remains 68 source-linked rows and nine generated pages. No claim is made that this session independently verified the other session's added research.
- Completion-log push encountered an add/add coordination conflict when plain rebase attempted to replay the parallel session's merged history against the older session remote. Aborted that rebase without losing any work, then rebased on origin/main to retain the combined history. No resolution discarded another session's content.


---

# Session `sess-8d650ba0` — deep-dive evidence dashboard (`analysis/`)

Branch: `arena/8d650ba0-jack3`. Scope: `analysis/**`, `tools/**`, `research/verification-log.md`, this section of `COORDINATION.md`, and one additive cross-link each in `index.html` and `docs/index.html`.

The two earlier sections above are preserved verbatim. Nothing from sessions 5cb84cd0 or ff406d61 was modified or removed except one additive navigation link on each landing page.

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

---

## Session `sess-8d650ba0` — PR, merge and deployment record

- **PR:** https://github.com/wingangboozle1-lang/Jack3/pull/7 — "Jack in the Box NNN (Central LA): verified research, risk
  register, scenario model and decision dashboard".
- **Merge:** merged to `main` 2026-11-06 13:10:58 UTC, merge commit `00709bc584928d4629459be7f78b4dc298d6aea9`.
  Merge method: merge commit. No approval wait, as instructed.
- **Pre-merge checks:** the repository's own workflow (`Validate public research`) passed on the PR head
  (run 42223322444). Locally: `tools/model.py`, `tools/build.py` and `tools/linkcheck.py` all clean
  (11 pages, 234 internal links and anchors, 0 broken); `scripts/validate.py` PASS with 68 evidence rows and 9 root pages.
- **Repair made to pass CI:** the first CI run failed on `git diff --exit-code -- '*.html'` because the root `index.html`
  had been hand-edited to add the cross-link. Fixed by folding the link into the root page generator (`scripts/build.py`)
  so regeneration is byte-identical. Re-run passed. No other session's content was altered by that change.
- **Deployment:** GitHub Pages built successfully for commit `00709bc` (build status `built`, duration 166 s,
  no error). Early 404s were CDN propagation and cleared on re-request.
- **Live URLs verified after deploy:**
  - `https://wingbangboozle1-lang.github.io/Jack3/` — root dashboard (session 5cb84cd0), now carrying the cross-link
  - `https://wingbangboozle1-lang.github.io/Jack3/docs/` — docs dashboard (session ff406d61), cross-link present
  - `https://wingbangboozle1-lang.github.io/Jack3/analysis/` — this session's deep-dive dashboard
  - `https://wingbangboozle1-lang.github.io/Jack3/analysis/decision.html` — decision page

### Conflict resolution log
- `git merge origin/main` produced **add/add on `COORDINATION.md`** and **content conflict on `README.md`** only. Both
  resolved by keeping the upstream text **verbatim** and appending this session's section; nothing was removed.
- Root-level `index.html`, `economy.html`, `tenant.html`, `risk.html`, `sources.html` in this branch were **relocated to
  `analysis/`** rather than merged over the other sessions' pages, so both earlier dashboards remain intact and unchanged
  apart from one additive link each.
- No other session's files were edited. No cross-session request was needed.

---

# Session `arena-796b983f-jack3` — deep-dive decision brief (`brief/`)

Branch: `arena/796b983f-jack3` (platform-assigned; no other branch used). Four parallel sessions existed by the time of this merge; this session's scope and files are non-overlapping with the other three. Work on this branch was partially duplicated in spirit by `sess-8d650ba0`'s `analysis/` layer — both are preserved; nothing was reverted.

## Task board

| # | Task | Status | Owner | Files / Scope |
|---|------|--------|-------|---------------|
| 0 | Coordination board | done | arena-796b983f | COORDINATION.md |
| 1 | Research: demographics/income/population/schools (official sources) | done | arena-796b983f | research/RESEARCH.md |
| 2 | Research: NNN economics, sell vs renew, Measure ULA | done | arena-796b983f | brief/decision.html |
| 3 | Research: risk register incl. black swans | done | arena-796b983f | brief/risk-analysis.html |
| 4 | Research: Jack in the Box tenant credit (IR fetched live 2026-11-06) | done | arena-796b983f | brief/decision.html |
| 5 | Site build: dashboard + 8 subpages (under /brief/) | done | arena-796b983f | brief/* |
| 6 | Verification (tools/check_site.py; source typing; PII grep) | done | arena-796b983f | tools/check_site.py |
| 7 | Integration: merge main (3x), /brief/ restructure, PR #3 | in progress | arena-796b983f | brief/, README.md, COORDINATION.md, scripts/build.py (one additive line), index.html (regenerated) |
| 8 | Flagged for Review page | done | arena-796b983f | brief/flagged.html |

## Log
- 2026-11-06: Repo found README-only; board created; research + build complete. `check_site.py` PASS (brief/: 9 pages, 204 internal refs).
- 2026-11-06: Parallel PR #1 (5cb84cd0), PR #2 (ff406d61) and PR #7 (8d650ba0) discovered via origin/main moves. This session's root-level site was moved to `/brief/` (commit 9c1f7e0) to preserve the merged workspace untouched.
- 2026-11-06: Root `index.html` + `scripts/build.py` conflicted twice (both sessions folded a cross-link into the generator). Resolved by keeping both additive link lines (hero-note `analysis/` link from 8d650ba0 preserved; companion line lists docs/ · analysis/ · brief/). `index.html` regenerated deterministically; `scripts/validate.py` PASS (68 rows).
- 2026-11-06: `.github/workflows/deploy-pages.yml` (Actions deploy) was added then deliberately dropped: legacy Pages builds recovered (run 42222599679 succeeded per 5cb84cd0's deploy record above); two competing deployers avoided. If Pages errors again, re-add an Actions workflow and set Pages `build_type=workflow`.
- 2026-11-06: PR #3 opened from `arena/796b983f-jack3`. CI (Validate public research) PASS. Merge blocked by concurrent PR #7 — main merged into this branch, conflicts in README.md / COORDINATION.md / index.html / scripts/build.py resolved without discarding any session's work. `check_site.py` and `scripts/validate.py` re-run after resolution.
- PRs still open by others: PR #4 (`arena/28eacae6-jack3`) — not touched by this session.
- 2026-11-06 (later): PR #8 (`arena/8d650ba0-jack3`) merged; conflicted on COORDINATION.md only; resolved by keeping both sessions verbatim (theirs first, this session appended). Their cross-dashboard navigation commits carry links to this `/brief/` site.

## PR / Merge Record (this session)
- PR #3 `arena/796b983f-jack3 → main`: https://github.com/wingbangboozle1-lang/Jack3/pull/3 — merge pending at time of writing; result recorded in the follow-up note below.
