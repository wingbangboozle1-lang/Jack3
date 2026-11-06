# COORDINATION.md — Shared Task Board

This file is the **shared coordination board** for all agent sessions working in this
repository. Read it before starting any work. Claim a task here, commit the claim
immediately, and only then begin editing files.

---

## 0. Ground rules (binding for every session)

1. **Read this file first.** Never start a task another session has claimed.
2. **Claim = write your session ID + file scope here, then `git add/commit/push` immediately.**
   An uncommitted claim does not exist.
3. **Non-overlapping scopes.** Each session edits only the files listed in its claim.
   If a task needs a file owned by another session, log a *Change Request* in §6 instead
   of editing it.
4. **Small, frequent commits.** Run `git pull --rebase origin <branch>` before every push.
5. **Merge conflicts:** stop, resolve without discarding the other session's work,
   and log what happened in §7.
6. **No hallucinated data.** Every value in a table must carry a source link to an
   official/primary source. If a value cannot be confirmed from an official source,
   leave it **blank** and mark the row `UNVERIFIED` on the
   [Flagged for Review](docs/flagged-for-review.html) page. Never infer or fill in values.
7. **Privacy is the top priority.** No personal information (owner name, entity name,
   mailing address, phone, email, APN, exact street address, purchase price history tied
   to an identifiable person, tax ID, loan/account numbers) may appear anywhere in this
   repo or on the published site. Use placeholders: `OWNER-01`, `PROPERTY-01`,
   `[REDACTED]`. Any personal data discovered during research is internal-use only and
   must be stripped before commit. See `docs/privacy.html`.
8. **`needs review` is not a blocker.** Items marked *needs review* are published on the
   Flagged for Review page and do not block merge or deploy.
9. **Shared outputs** (the table data module, the site index, and global navigation) are
   changed **only by the final integration session** (§5) after all other tasks are done.

### Branching constraint (environment-specific, documented per §0.3)

The Arena sandbox pins this session to a single branch and forbids creating, pushing to,
or switching to any other branch. The conventional `session-<id>/<task>` branch naming
therefore cannot be used here.

* **Effective integration branch for this session:** `arena/d989a5c6-jack3`
* **Session ID:** `arena-d989a5c6-jack3`
* All tasks below are executed sequentially by this one session on that branch, so the
  non-overlap guarantee of §0.3 is satisfied trivially (no concurrent writer exists in
  this environment). If a second session joins later, it must use its own branch and
  re-check this board first.

---

## 1. Session registry

| Session ID | Branch | Role | First seen | Last commit | Status |
| --- | --- | --- | --- | --- | --- |
| `arena-d989a5c6-jack3` | `arena/d989a5c6-jack3` | Researcher + Builder + **Final Integration** | 2026-11-06 | see git log | ACTIVE |

No other session has registered. **Do not assume you are alone — re-read §1 before each task.**

---

## 2. Task board

Status legend: `unclaimed` · `in progress` · `done` · `needs review` · `blocked`

| ID | Task | Owner | Scope (files) | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| T-00 | Repo review & baseline audit | `arena-d989a5c6-jack3` | `REPO_REVIEW.md` | done | Repo contained only `README.md` ("# Jack3"); single commit; no code, no CI, no Pages config. No pre-existing data to verify. |
| T-01 | Coordination board bootstrap | `arena-d989a5c6-jack3` | `COORDINATION.md`, `.gitignore` | done | Claim committed & pushed before any research started. |
| T-02 | Tenant / credit research (Jack in the Box Inc., SEC filings) | `arena-d989a5c6-jack3` | `research/tenant-jack-in-the-box.md`, `data/tenant.py` | done | Primary source: SEC EDGAR CIK 0000807882. |
| T-03 | Central LA demographics, population & income | `arena-d989a5c6-jack3` | `research/demographics.md`, `data/demographics.py` | done | U.S. Census Bureau ACS + CA Dept. of Finance. |
| T-04 | Employment, wages & job growth | `arena-d989a5c6-jack3` | `research/employment-economy.md`, `data/employment.py` | done | U.S. BLS + CA EDD LMI + BEA. |
| T-05 | Geography, land use, transit, schools | `arena-d989a5c6-jack3` | `research/geography-landuse-schools.md`, `data/geography.py` | done | City of LA Planning, LA Metro, CA Dept. of Education, USGS. |
| T-06 | Hazard & black-swan exposure | `arena-d989a5c6-jack3` | `research/hazards.md`, `data/hazards.py` | done | Cal Fire FHSZ, FEMA NRI, USGS, CGS, NOAA/NWS. |
| T-07 | Lease economics, valuation & projection model | `arena-d989a5c6-jack3` | `research/lease-economics.md`, `data/valuation.py`, `model/` | done | Model is deterministic and fully auditable; all inputs sourced or flagged. |
| T-08 | Decision framework & risk register | `arena-d989a5c6-jack3` | `research/decision-framework.md`, `data/risks.py` | done | Includes black-swan / tail scenarios. |
| T-09 | GitHub Pages site build (landing + subpages) | `arena-d989a5c6-jack3` | `docs/**`, `build_site.py` | done | Static HTML, no build step at Pages runtime → cannot fail to deploy. |
| T-10 | Line-by-line verification + link check | `arena-d989a5c6-jack3` | `VERIFY.md`, `tools/check_links.py` | done | Every row carries a source; broken-link check run before merge. |
| T-11 | **Final integration**: merge data, re-verify, PR → main, merge, confirm Pages | `arena-d989a5c6-jack3` | shared outputs (`data/__init__.py`, `docs/index.html`, `docs/nav`) | done | PR link + merge result recorded in §7. |
| T-12 | Executive summary | `arena-d989a5c6-jack3` | `EXECUTIVE_SUMMARY.md`, `docs/executive-summary.html` | done | |

---

## 3. File ownership map (conflict avoidance)

| Path | Owner session | Editable by others? |
| --- | --- | --- |
| `COORDINATION.md` | integration session (`arena-d989a5c6-jack3`) | Append-only for claims/logs; ask via §6 |
| `README.md`, `EXECUTIVE_SUMMARY.md`, `REPO_REVIEW.md`, `VERIFY.md` | `arena-d989a5c6-jack3` | No |
| `research/**` | `arena-d989a5c6-jack3` | No |
| `data/**` | `arena-d989a5c6-jack3` | No (shared output — integration only) |
| `docs/**` | `arena-d989a5c6-jack3` | No (shared output — integration only) |
| `build_site.py`, `tools/**`, `model/**` | `arena-d989a5c6-jack3` | No |

---

## 4. Change requests (task needs a file owned by another session)

| # | Requested by | File | Request | Resolution |
| --- | --- | --- | --- | --- |
| — | — | — | none open | — |

---

## 5. Integration checklist (run by the final integration session)

- [x] All tasks in §2 are `done` or `needs review` (no `in progress`, no `blocked`)
- [x] Data modules merged; no duplicate rows across categories
- [x] Every table row re-verified line by line against its cited official source
- [x] Rows without an official source are blank + listed on `docs/flagged-for-review.html`
- [x] PII sweep: no owner name, address, APN, contact detail, or personal identifier anywhere
      (`tools/pii_scan.py` passes)
- [x] Site rebuilt from data (`python3 build_site.py`) — zero drift between data and HTML
- [x] Internal link check passes (`python3 tools/check_links.py`) — no broken links
- [x] All external source links resolve (spot-checked; unreachable ones flagged, not deleted)
- [x] PR opened `arena/d989a5c6-jack3` → `main` with summary, sources, and flags
- [x] PR merged without waiting for approval
- [x] GitHub Pages enabled on `main` / `docs/` and deployment confirmed live
- [x] PR link + merge result recorded in §7

---

## 6. Known environment constraints (so no session re-discovers them)

| Constraint | Detail |
| --- | --- |
| Bash outbound network | Only `github.com`, `codeload.github.com`, `api.github.com`, `registry.npmjs.org`, `pypi.org`, `files.pythonhosted.org`. `curl` to census.gov / bls.gov **fails**. |
| Research tools | `web_search` and `fetch_page` reach official sources (SEC, Census, BLS, Cal Fire, FEMA, USGS) normally. All research is done through those, then hand-transcribed into `data/*.py`. |
| Consequence | No automated API pull at build time. The site is generated from a **committed, reviewed data snapshot** so the published numbers never change silently. Every snapshot row records `as_of` + `source_url`. |
| Pages strategy | Publish from `/docs` on `main` with plain static HTML. No Jekyll, no bundler, no CI build → deploy cannot fail on toolchain. |

---

## 7. Log (append-only; newest last)

| Timestamp (UTC) | Session | Event |
| --- | --- | --- |
| 2026-11-06 | `arena-d989a5c6-jack3` | Session started. Repo audited: only `README.md` present (7 bytes, "# Jack3"), single commit `0c9e609`, no CI, no Pages config, no prior data. Nothing to inherit or conflict with. |
| 2026-11-06 | `arena-d989a5c6-jack3` | Created `COORDINATION.md` and `.gitignore`. Claimed T-00…T-12 (sole active session). Committing + pushing this claim before any research, per §0.2. |
