# Repository review — 2026-11-10 (session `203ae19e`)

Review of the repository as found at `main` = `4278c1a` (PR #33 merged), performed before any content
work in this session. Scope: what is published, what is only in the repository, whether the published
data reconciles, and what is irregular. This file is this session's record; the older
`REPO_REVIEW.md` and `dashboard/repo-review.html` belong to earlier sessions and are left untouched.

---

## 1. What the repository contains

| Directory | Pages | Published? | Dataset / generator | Verified by |
|---|---|---|---|---|
| root (`index.html`, 11 category pages, `assets/`) | 12 | **Yes** — the live site | `data/evidence.json` → `scripts/build.py` | `scripts/validate.py`, `scripts/stage_pages.py`, `tools/linkcheck.py` |
| `dashboard/` | 15 | **Yes** — reachable at `/dashboard/` and linked from the root nav | `_dashboard_src/dataset.json` → `_dashboard_src/build.py` | `_dashboard_src/verify.py` |
| `decision-file/` | 23 | No | `data/*.py` → `build_site.py` | `tools/check_links.py`, `tools/pii_scan.py` |
| `analysis/` | 11 | No | `analysis/data/*.json` → `tools/build.py` | `tools/linkcheck.py` (analysis set) |
| `brief/` | 10 | No | hand-written HTML | `tools/check_site.py` |
| `pages/` | 9 | No | hand-written HTML | none of its own |
| `docs/` | 9 + markdown | No | hand-written HTML + `research/*.md` | none of its own |
| `advisory/` | 12 | No | `_advisory_src/*.py` | `_advisory_src/verify_advisory.py` |
| `audit/`, `site/` | 2 + assets | No | loose HTML/CSS | none |

Tracked files: 208. GitHub Pages is served from `main` `/` with Jekyll (`build_type: legacy`), and
`scripts/stage_pages.py` reproduces the curated artifact that CI compares byte-for-byte against the
Jekyll output.

## 2. What reconciles

- **Root dataset after this session's pass:** 154 rows, 27 sources, 12 pages. Every published value was
  re-read from its publisher on 2026-11-10 (`research/VERIFICATION-2026-11-10-203ae19e.md`). No previously
  published verified value was found wrong.
- **Build gates pass on the combined tree:** `scripts/build.py` (deterministic — two consecutive builds
  are byte-identical), `scripts/validate.py` (154 rows, 12 pages, source links, blank-value status,
  prohibited-embed scan), `scripts/stage_pages.py` (32 staged entries; every staged row carries a
  registered source), `tools/check_site.py` (213 internal references), `tools/linkcheck.py` (no broken
  internal links or anchors), `tools/check_links.py` (official-domain allowlist), `tools/pii_scan.py`
  (0 findings), `_advisory_src/verify_advisory.py`, `_dashboard_src/verify.py`.
- **No personal information found in the published artifact.** An independent regex sweep of the 29
  published HTML/asset files (email, telephone, street address, APN patterns) returned zero hits.
  No address, parcel number, owner name, lease, rent roll or financial statement exists anywhere in the
  repository; the asset is published as *Asset A*.

## 3. Irregularities (flagged, with handling)

| ID | Severity | Finding | Handling in this session |
|---|---|---|---|
| **R-IR-01** | High | **Seven parallel layers** with overlapping datasets and, in places, different headline conclusions. Two of them are live at once: the root decision file and `/dashboard/` (15 pages, 185 rows, its own 21-source dataset). A reader can reach two different datasets from one site. | Not merged or deleted. The root decision file is the verified publication and states its evidence boundary. Flagged in `COORDINATION.md` for the next integration session; the `/dashboard/` layer is internally consistent and avoids asserting values, so it is not a false claim — it is a **duplication** risk. |
| **R-IR-02** | Medium | **Narrative numbers are hand-typed in `scripts/build.py`** (the landing hero, risk block and sources copy), while the tables are generated from `data/evidence.json`. A change in the dataset does not update the prose, so the two can drift. This session had to edit both to keep the Treasury anchor consistent at 4.86%. | Left as-is structurally; the drift was corrected for this pass. Recommendation: move narrative figures into the dataset in a later integration. |
| **R-IR-03** | Low | **README drift.** The README listed `report/` and `verification-3644edd8/` as repository layers; neither directory exists. It also claimed only the twelve root pages and one stylesheet are staged, while `scripts/stage_pages.py` also publishes `dashboard/`. | **Fixed** in this session (`README.md`). |
| **R-IR-04** | Low | **Two different school-enrollment counts for LAUSD** in official sources (CDE census-day 497,105; Dashboard 369,830). | Both published separately with definitions; new review-page flag. See N-IR-01 in the verification record. |
| **R-IR-05** | Medium | **26 HTML files still render the repository account handle** (`decision-file/` 23, `pages/` 3). None of them is published, and the handle is already public in the repository URL, but it is unnecessary surface. | **Not edited** — those files belong to other sessions, and the board's rule is to log a request rather than edit another session's scope. Logged as a cross-session request in `COORDINATION.md` (XR-N2). The published artifact contains zero occurrences. |
| **R-IR-06** | Medium | **Three stale open PRs** at the time of review: #26 (2026-11-07), #31 and #32 (2026-11-08). #32 is `CONFLICTING`, commits `_pages_artifact/` build output, and edits other sessions' directories (`brief/`, `decision-file/`). | Not merged or closed; they are not this session's branches. #32's substantive corrections (issuer AUV/royalty labels, ULA thresholds, BLS vintage) were independently re-checked against the official pages in this pass; the values published on the root site reconcile, so nothing verified is lost by leaving #32 open. |
| **R-IR-07** | Low | **`_pages_artifact/` is generated but present in the working tree**, and `.gitignore` covers it. It was committed in PR #32's branch and is therefore a merge hazard if that PR is ever merged. | Not tracked on `main` (0 tracked files under `_pages_artifact`). Noted. |
| **R-IR-08** | Low | **Rolling sources.** BLS, FRED, QuickFacts, the School Dashboard and CDE are re-vintaged on their own schedule; every published figure is a dated observation. | Every source now carries a `checked` date; the Treasury anchor is labelled with its observation date. |

## 4. Cross-session requests logged

| ID | To | Request |
|---|---|---|
| **XR-N1** | Next integration session | Decide whether `/dashboard/` remains published alongside the root decision file. If it stays, the root nav should label it as a separate dataset with its own snapshot date. |
| **XR-N2** | Owners of `decision-file/` and `pages/` | Redact the repository account handle from the 26 unpublished HTML files (R-IR-05). No functional change is required. |
| **XR-N3** | Next integration session | Move hand-typed narrative figures out of `scripts/build.py` into `data/evidence.json` so prose and tables cannot drift (R-IR-02). |

## 5. Verdict

The published site is internally consistent, every value is source-linked, the unverified material is
blank and disclosed, the privacy boundary holds, and the build is deterministic and gated. The
repository's outstanding risk is **structural, not factual**: too many parallel layers, one duplicated
live dataset, and prose figures that are not data-driven. None of that blocks publication.
