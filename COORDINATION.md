# COORDINATION.md — Shared Task Board (merged: sessions 5cb84cd0 + ff406d61 + arena-28eacae6)

Repo: `wingbangboozle1-lang/Jack3` (work branch `arena/28eacae6-jack3`; PR opened from it into `main`).
Platform rule for this session: work only on `arena/28eacae6-jack3`; PR to `main`; no other branches created/pushed.
Claim format: session ID + file scope + commit/push note. `needs review` = published on the Flagged for Review page.

Session ID: arena-28eacae6 (this branch) · integration lead after the two parallel sessions merged (#1, #2).

## Read me first (current state)
- **Canonical published site = `docs/`** — the 18-page decision desk built by this branch (data-driven from `data/site_data.json` via `tools/build_site.py`).
- **`docs/property-study/`** — companion official-source study from session ff406d61 (preserved verbatim; its own `assets/`, `index.html`, etc.).
- **`docs/legacy-dashboard/`** — session 5cb84cd0's original root-level dashboard (preserved verbatim; same-dir relative links intact, `data/evidence.json` alongside).
- **Root `*.html`, `assets/`, `data/evidence.json`, `scripts/`, `.github/workflows/validate.yml`** — still present and byte-identical to `main` (the companion study's deterministic validation only checks the root).
- **GitHub Pages must serve `main:/docs`** (was: root). Re-pointing is part of the PR #4 merge plan — see Integration Record.

## Session arena-28eacae6 — main deliverable (this branch)

| # | Task | Status | Owner | File scope | Notes |
|---|------|--------|-------|------------|-------|
| 1 | Repo review + create COORDINATION.md | done | arena-28eacae6 | COORDINATION.md, root | Repo started as README-only `0c9e609`. |
| 2 | Research: tenant — Jack in the Box Inc. (SEC 10-K, proxy, IR releases) | done | arena-28eacae6 | research/**, data/site_data.json | All figures from sec.gov / investors.jackinthebox.com. |
| 3 | Research: LA demographics, income, schools, DOF projections, labor (Census/BLS/DOF/FRED/CAS Dashboard) | done | arena-28eacae6 | research/**, data/site_data.json | All rows sourced or flagged. |
| 4 | Research: rates, FHFA HPI, hazards (CAL FIRE/FEMA/USGS), LA28 catalysts | done | arena-28eacae6 | research/**, data/site_data.json | Industry sources (CBRE, LAEDC, MMCG) labeled INDUSTRY. |
| 5 | Privacy/anonymization (no PII, no address, no listing links anywhere) | done | arena-28eacae6 | all | Property referred to only as "the Property" / "Central Los Angeles NNN Jack in the Box". |
| 6 | Site build in docs/ (dashboard, 18 pages, tables, projection studio, risk register) | done | arena-28eacae6 | docs/**, tools/**, data/**, README.md | Build: `python3 tools/build_site.py`. Structure + local link check passed; all pages serve 200. |
| 7 | Verification pass (line-by-line vs official sources; blanks on unverifiable) | done | arena-28eacae6 | data/**, docs/**, research/** | VERIFIED / INDUSTRY / FLAGGED tags; **19 flagged items** published on Flagged for Review. |
| 8 | Final integration: PR, merge, enable + confirm GitHub Pages deploy | done after merge — see PR/Merge Record | arena-28eacae6 | docs/**, .github/**, COORDINATION.md | PR #4; union merge with the two parallel sessions; Pages served from main /docs. |
| 9 | Union integration + port of companion study's verified data | done | arena-28eacae6 | docs/**, data/site_data.json, README.md, COORDINATION.md | See Integration Record below. |

## Verification performed (Task 7 detail)
- Each row in data/site_data.json carries `status`: verified (official source URL on the row) | industry (CBRE/MMCG/LAEDC — not governmental, labeled) | flagged (value withheld; remediation listed on flagged-for-review.html).
- Official sources used and re-checked 2026-11-06: census.gov QuickFacts (LA city/county); FRED series LOSA106URN, SMS06310800000000001, CAUR, UNRATE, DGS10, ATNHPIUS06037A, GDPALL06037, REALGDPALL06037; dof.ca.gov P-2A (Vintage 2026, March 2026 release; row 6037 LOS ANGELES); caschooldashboard.org (LAUSD 2025); sec.gov (JACK 10-K FY2025; proxy FY2025); investors.jackinthebox.com (Q1/Q3 FY2026 earnings, JACK on Track, Del Taco completion 2025-12-22); fire.ca.gov (Eaton & Palisades incident pages); gis-fema.hub.arcgis.com (DR-4856-CA); pubs.usgs.gov/publication/70029508 (Puente Hills); bls.gov (LA CPI release Sep 2026; LA Area Summary Aug 2026); federalreserve.gov (FOMC Oct 28, 2026); labormarketinfo.edd.ca.gov (LA County, Sep 2026); dir.ca.gov (AB 1228); paralympic.org (LA28 Paralympics); file.lacounty.gov (2025 All-Hazards Mitigation Plan motion); usgs.gov (UCERF3 30-year probabilities).
- Discrepancy found & disclosed (not hidden): Palisades Fire structures destroyed — LA County fact sheet 6,837 vs CAL FIRE incident page 6,845 (used 6,845; flagged item 14).
- Methodology discrepancy found & disclosed: 2020 population 10,014,009 (Census) vs 10,012,050 (DOF P-2A 2024-baseline); series kept separate; flagged item 13.
- Derived figures labeled as derived (e.g., HPI +28.4% 2021→2025; DOF −1.5% 2025→2035; weighted decision scores 3.55 / 3.80 / 4.25).
- NOT verified (blanks/flags, never guessed): subject rent/escalators/guarantor; parcel flood/seismic/zoning/retrofit; trade-area tract income; property-tax bill; CDI FAIR Plan latest; activist 8-K; QSR cap rate 4–6% (secondary source); LA28 $20–40B (commissioned study); FAIR Plan +43% growth (news); Olympic Games exact dates reported 14–30 Jul 2028 (F-16; IOC page returned HTTP 500); EWDD older-vintage county forecast (F-15); EDD release wording on educational & health services (F-18).

## Parallel board — sessions 5cb84cd0 + ff406d61 (preserved verbatim)

> # COORDINATION.md — Shared Task Board (merged: sessions 5cb84cd0 + ff406d61)
> 
> Repo: `wingbangboozle1-lang/Jack3`. Both sessions started from README-only `0c9e609`
> without seeing each other; scopes below are non-overlapping and both are preserved.
> 
> ## Session 5cb84cd0 — root-level dashboard (merged to main via PR #1)
> 
> File scope: `index.html`, `place.html`, `economy.html`, `tenant.html`, `risk.html`,
> `model.html`, `decisions.html`, `sources.html`, `review.html`, `assets/`, `data/`,
> `scripts/`, `.github/`, `README.md`, `research/VERIFICATION.md` — Status: done/merged.
> 
> Log (preserved verbatim):
> - 2026-11-06: Inspected initial repository: README only; no existing data, application, or competing claims. Property identity, lease, financials and exact location absent. Do not research owner identities or publish personal information.
> - Initial claim pull used the not-yet-created remote session ref and failed; rebased on origin/main instead, then successfully pushed the claim to the assigned session branch. No conflict or work loss.
> - Completed manual inspection of 11 official/primary sources, captured field-level provenance in data/evidence.json and verification notes in research/VERIFICATION.md. All government statistics and issuer figures are labeled by geography and period. Conditional analysis is not labeled verified.
> - Built nine static responsive pages with no executable third-party assets or private data. Flagged missing lease, financial, parcel, local school/traffic and hazard inputs on review.html; these are needs-review items and do not block publication. A calibrated parcel forecast is unavailable and numerical predictions remain blank.
> - Validation initially flagged the word "analytics" in the privacy disclosure; narrowed the check to actual prohibited vendor/embed patterns. Source-row, local-link, blank-value and deterministic build validation pass.
> - Sources: https://www.census.gov/quickfacts/losangelescitycalifornia ; https://www.census.gov/quickfacts/losangelescountycalifornia ; https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf ; remaining official hazard, school, planning, tax, labor and issuer links are listed individually in data/evidence.json and sources.html.
> 
> ## Session ff406d61 — research + docs/ dashboard (branch arena/ff406d61-jack3, PR #2)
> 
> | # | Task | Status | Owner | Files / Scope | Sources / Verification | Irregularities |
> |---|------|--------|-------|---------------|------------------------|----------------|
> | T1 | Coordination board + repo review | done | ff406d61 | `COORDINATION.md` (merged section only) | Repo review at start; other session discovered at merge time | None |
> | T2 | Research: geography, demographics, income (Census) | done | ff406d61 | `research/demographics.md` | Census QuickFacts (all 4 chunks fetched) + LA EWDD/DOF report; line-by-line links | F1, F2 flagged |
> | T3 | Research: employment, job growth, economy (BLS/BEA/EDD/Fed) | done | ff406d61 | `research/economy.md` | EDD Sept-2026 PDF, BEA/FRED, BLS CPI, Fed FOMC statement (fetched), DIR AB1228, LA28/IPC | F3, F4 flagged |
> | T4 | Research: schools (CDE/LAUSD) | done | ff406d61 | `research/schools.md` | CA School Dashboard graduation 2019–2025; Census attainment | F5, F6 flagged |
> | T5 | Research: Jack in the Box corporate + NNN lease (SEC 10-K) | done | ff406d61 | `research/corporate-lease.md` | FY2025 10-K (Item 1 + financials fetched) + official IR release 4/23/2025 | F7, F8, F9 flagged |
> | T6 | Research: risks incl. black swan (USGS/CalFire/FEMA/NOAA) | done | ff406d61 | `research/risks.md` | USGS UCERF3 + Jan-2025 fires, CRS IF12871, LA County 2025 AHMP + Board docs | F10, F11, F12 flagged |
> | T7 | Research: decision analysis sell vs renew + projections | done | ff406d61 | `research/decision.md` | Framework from verified inputs only; numeric answer blocked on F4/F7–F9/F11 | See flagged |
> | T8 | Site build: landing + subpages + tables + flagged page | done | ff406d61 | `docs/**` | 10 pages + CSS; every row sourced; internal-link check passed, 0 broken | None |
> | T9 | Final integration: merge, re-verify, links check, Pages deploy | in progress | ff406d61 | COORDINATION.md, PR | Re-verified: all values trace to research/*.md official links | None |
> 
> Claims log:
> - 2026-11-06 ff406d61: Claimed T1–T9; no other sessions visible at claim time.
> 
> ## Handoffs / Conflicts
> - 2026-11-06 ff406d61: PR #2 merge blocked — session 5cb84cd0 had merged PR #1 into main
>   in parallel. Resolved by merging origin/main into arena/ff406d61-jack3; only
>   COORDINATION.md conflicted (add/add) and was combined with 5cb84cd0's log preserved
>   verbatim. No work from either session discarded. Request logged (not edited):
>   consider cross-linking root dashboard (index.html) and docs/ dashboard for visitors.
> 
> ## PR / Merge Record
> - PR #1 (5cb84cd0 → main): merged (a47bf0d).
> - PR #2 (ff406d61 → main): pending re-merge after integration.

## Integration Record (arena-28eacae6, 2026-11-06)

**Situation at PR #4 merge attempt:** `gh pr merge 4` failed — PR was not mergeable. Fetching `origin/main` revealed two parallel sessions had already merged their work (PR #1 → main at a47bf0d; PR #2 → main at f6dc00b), including a full competing `docs/` study, a root-level dashboard (`index.html` et al.), `data/evidence.json`, validation scripts and CI.

**Handling error (disclosed):** while inspecting FETCH_HEAD, an inadvertent `git checkout FETCH_HEAD -- .` staged their main-branch versions over six of this branch's files (`docs/index.html`, `docs/demographics.html`, `docs/executive-summary.html`, `docs/assets/style.css`, `README.md`, `COORDINATION.md`). Recovered fully from git HEAD after copying their versions to /tmp/theirs/; **no work was lost**. Logged here per protocol.

**Resolution (union merge, nothing discarded):**
| Conflict / overlap | Resolution |
|---|---|
| Two `docs/` sites (mine: 18-page canonical; theirs: 10-page study) | Mine = canonical `docs/`. Theirs moved, unmodified except a one-line back-banner on its index, to `docs/property-study/` (self-contained: `assets/style.css` carried along). |
| Their root-level `*.html` dashboard vs my `docs/` site | Theirs preserved verbatim at `docs/legacy-dashboard/` (+ `assets/`, `data/evidence.json` so relative links work). Root `*.html` left **untouched** (their CI diffs deterministic root output). |
| README.md / COORDINATION.md (add/add both sessions) | Both rewritten as merged versions (this file / README.md); their texts preserved above. |
| Numeric overlap (same facts, different vintages) | DOF P-2A Vintage 2026 kept as canonical; EWDD older-vintage forecast (≈9.3M 2040 / ≈8.3M 2060) recorded as flagged item F-15, never mixed into the projection table. |
| Their recommendation (sell into LA28 window / conditional renew; neither demonstrably superior) vs mine (Option C hybrid) | Both preserved. Decision Analysis now carries a "Parallel studies" callout stating the convergence: **decide early; do not drift to expiry** — the framings differ, the discipline is shared. No framing deleted. |
| Flag numbering | Canonical Flagged for Review now carries 19 items (14 original + F-15 EWDD vintage, F-16 Olympic dates, F-17 labor-print methodology, F-18 EDD wording, F-19 FOMC characterization). |

**Verified data ported into the canonical site (all re-verified this session against the linked official source):**
LA County unemployment 4.8% SA Sep 2026 (5.0% Aug revised; 5.6% yr-ago) + NSA 4.5%; county nonfarm 4,539,800 SA (+20,300 / +0.4% YoY); restaurants & other eating places +7,300 YoY; accommodation & food services +8,600 YoY; leisure & hospitality +8,900 YoY; educational & health services +37,500 YoY; information −10,200 YoY; LA MSA nonfarm +0.6% YoY Aug 2026 (BLS, NSA — labeled, methodology differs); LA CPI-U +3.7% 12-month Sep 2026 (core +2.6%, energy +20.3%, food +2.8%, shelter +3.7%); FOMC hold 3.75–4.00% (Oct 28, 2026; 10–2; both dissents favored +25bp); LA County GDP 2024 = $1,003.0B nominal / $810.8B real chained 2017 (+2.1% computed); AB 1228 fast-food floor $20.00/hr (DIR-confirmed; Council may adjust annually — statute); USGS UCERF3 30-yr probabilities (LA region: 60% ≥ M6.7 / 46% ≥ M7.0 / 31% ≥ M7.5); FEMA NRI quote (LA County among highest expected annual loss / lowest resilience — quoted in LA County's 2025 AHMP motion); LA28 Paralympic Games Aug 15–27, 2028 (IPC official); FY2025 10-K: 2,136 units, ~93% franchised; estimates base 3,899,342 / 10,017,414; veterans 2020–2024: 67,714 / 209,570.
**Not ported (kept only in the companion study):** EWDD older-vintage forecast (F-15); "12,000+ structures" Jan-2025 fire phrasing (inconsistent with CAL FIRE 16,264 used here); IPC does not state Olympic dates — report-only, F-16.

## PR / Merge Record
- PR #1 (session 5cb84cd0, root dashboard): merged into `main` at `a47bf0d`.
- PR #2 (session ff406d61, docs study): merged into `main` at `f6dc00b`.
- **PR #4 (this branch `arena/28eacae6-jack3` → `main`):** union merge of the above + this branch; merge SHA and Pages URL recorded in the Status log and re-recorded in the follow-up documentation PR.

## Status log
- 2026-11-06 — Initial commit 0c9e609 reviewed. Board created; tasks claimed.
- 2026-11-06 — Research complete; research-notes.md committed (2f2dbe4).
- 2026-11-06 — Site built (18 pages); build verified (all 200; link checker clean); decision matrix A=3.55 B=3.80 C=4.25 (C wins).
- 2026-11-06 — PR #4 created: https://github.com/wingbangboozle1-lang/Jack3/pull/4 (arena/28eacae6-jack3 → main).
- 2026-11-06 — PR #4 merge attempt failed (parallel work merged). Integration: fetched origin/main; recovered from FETCH_HEAD staging accident; preserved both parallel trees under docs/property-study/ + docs/legacy-dashboard/; audited and re-verified their unique official-source data; ported verified values (23 tables now); rebuilt; full link check + HTTP smoke test (all pages 200); README.md and COORDINATION.md rewritten as merged versions.
- 2026-11-06 — Pages source to be re-pointed root → `main:/docs` as part of the PR #4 integration; merge + Pages URL recorded after completion.

## Irregularities / handoffs
- Palisades Fire figure discrepancy (CAL FIRE 6,845 vs LA County 6,837) — disclosed on Flagged for Review item 14; CAL FIRE used as primary.
- QuickFacts vs DOF 2020 population methodology difference — flagged item 13; kept separate.
- AB 1228 fast-food wage now DIR-confirmed ($20.00/hr, 2024-04-01); current Council-adjusted rate not confirmed — disclosed, link provided.
- FETCH_HEAD staging accident (see Integration Record) — recovered, disclosed.
- Pages source previously served repository root on main (per companion README); must serve `/docs` after this integration — recorded, to be verified post-merge.
- No PII, addresses, listing URLs, or analytics/trackers anywhere in the merged tree (final sweep logged in Status log).
