# Repository review — session `4f0b3fa2`, 10 November 2026

Line-by-line review of what is actually in `wingbangboozle1-lang/Jack3` before any change was made, followed by what
was changed and why. Findings are numbered `IR-nn`; the ones that are still open are also published on the site's
[Flagged for review](../review.html) page so they can be read without opening the repository.

## 1. What the repository contained at the start

`main` was at `4278c1a` (merge of PR #33). The working tree held **102 HTML pages** across nine separate dashboards,
produced by at least nine sessions between 2026-11-06 and 2026-11-08, plus three Python data pipelines, one
half-megabyte generator (`build_site.py`, 146 KB) and a shared coordination board of roughly 900 lines.

| Layer | Pages | Generator | Published? |
|---|---|---|---|
| root (`/*.html`) | 12 | `scripts/build.py`, `data/evidence.json` | **yes** |
| `decision-file/` | 23 | `build_site.py`, `data/*.py`, `model/` | no |
| `dashboard/` | 15 | `_dashboard_src/build.py` | no |
| `analysis/` | 11 | `tools/build.py`, `tools/model.py` | no |
| `brief/` | 9 | hand-written | no |
| `pages/` | 8 | hand-written | no |
| `docs/` | 9 | hand-written | no |
| `advisory/` | 12 | `_advisory_src/build_advisory.py` | no |
| `audit/` | 1 | hand-written | no |

Only the root layer is staged into the Pages artifact, which is the right decision: the layers disagree with each
other, and publishing all of them would present six different recommendations to the owner.

## 2. Findings

### IR-01 — Six dashboards, six answers (high)

`decision-file/` says **SELL**; `advisory/` ranks pathway options numerically; `dashboard/` publishes a weighted
decision matrix; `brief/` presents a scored risk register R-01…R-22; the root site presents a conditional dual-track
recommendation; `pages/` and `docs/` present a seventh variant. Several of these rank strategies using assumed inputs
(cap rates, renewal probabilities, scenario weights) that no official source publishes.

*Status:* reported, not overwritten. The curated root dashboard is the only published recommendation; the other layers
remain in the repository as an audit trail and are excluded from the artifact. The conflict is disclosed on the review
page (`F-16`).

### IR-02 — An unsourced school statistic (high)

`dashboard/` publishes an LAUSD four-year graduation rate of **86.5%** citing the California School Dashboard. On
2026-11-10 the CDE district-profile endpoint returned "No districts found" for the LAUSD CDS code and DataQuest
returned an error page; the cohort data exist only as a 16 MB text file. The figure is **not** republished anywhere in
the curated site and is flagged (`F-10`).

### IR-03 — The Employment Cost Index was mislabelled (medium)

Root economy rows labelled **3.9%** as the "Employment Cost Index change". On the BLS release of 2026-11-04, 3.9% is
*wages and salaries* for the LA–Long Beach CSA; *total compensation* is **4.2%**. Both figures now appear as separate
rows with the distinction stated (`E-22`, `E-23`, `F-12`).

### IR-04 — A stale discount rate in a live model (medium)

`decision-file/`'s projection model anchors its discount rate to the 10-year Treasury at **4.19%** (2026-01-02), nine
months before the snapshot of its own pages. The same series was **4.88%** on 2026-11-09. A 69 bp difference is
material to any present-value comparison. The curated site publishes the current observation and the date it was read.

### IR-05 — The live site dropped its own JavaScript (high, fixed)

`_config.yml` excluded `assets/app.js` from the Jekyll build while every root page loaded it. On the live site the
table filters and status chips would have silently failed. Fixed: `_config.yml` now excludes only the research layers,
the file set is verified by `scripts/stage_pages.py`, and CI builds with Jekyll and compares the output byte for byte.

### IR-06 — A generator that rewrote committed pages (medium, fixed)

`scripts/build.py` regenerated nine root pages from a 141-row dataset, while `place.html` was not in that dataset at
all, so the committed file could never be reproduced by the build. `IR-05` also meant CI ran `git diff --exit-code`
over files the build did not own.

*Fixed:* the builder now owns every root page. The empty `place.html` (six rows, all blank) is folded into a new
`geography.html` that carries real geography data, and the CI diff check names the exact files.

### IR-07 — Privacy gate did not cover the published site (high, fixed)

`tools/pii_scan.py` scanned `decision-file/`, `data/`, `model/`, `tools/`, `site/` and `research/` — but **not** the
root pages that are actually published, and not `assets/`. The gate was therefore silent about the only files that
matter.

*Fixed:* the scan now covers the curated artifact (`data/evidence.json`, the twelve pages, `assets/style.css`,
`assets/app.js`) plus the legacy data modules. The repository account handle found printed on 26 legacy pages is
reported as a repository irregularity (`F-14`) rather than as PII, because the GitHub Pages URL itself necessarily
contains the account name and that is repository metadata, not personal information.

### IR-08 — Provenance checks that could not fail (medium, fixed)

The old `stage_pages.py` asserted that every `<tbody>` row contained *any* registered source URL. Every page's sidebar
and footer contained such a link, so the assertion passed regardless of the table. The new checker only counts links
inside `<td>` cells of body rows, and fails on the specific row.

### IR-09 — Non-official sources inside published tables (medium)

`analysis/` cites a commercial brokerage domain (22 rows) and a private law firm (4 rows); `_advisory_src/` cites a
brokerage as a source for net-lease cap-rate context. Under this project's rule — official sources only — those are
not acceptable as the basis of a verified row. None of them is republished, and `tools/check_links.py` now fails the
build if any such host appears in the curated site.

### IR-10 — Seven open pull requests (low)

PRs #4, #12, #22, #26, #31, #32 and #34 remain open from earlier sessions; several are red on CI. They are not merged
or closed here. This session works only on its own branch and does not act on another session's pull request; the list
is recorded in `COORDINATION.md` (`F-17`).

### IR-11 — Rolling sources cited as if static (low)

The BLS economic summary is a rolling PDF and the Treasury table changes daily. Both were cited without an observation
date in earlier layers. Every row now carries a period and every page a snapshot date; the specific figures that moved
between 2026-11-06 and 2026-11-10 are listed in `research/VERIFICATION-2026-11-10.md` §4.

### IR-12 — Two figures resolved rather than flagged forever (info)

Two items left open by earlier sessions were closed by reading the source properly:

* **LA County documentary transfer tax.** `$0.55 per $500` under Rev. & Tax. Code §11911(a), with the Recorder's
  statement that the county rate is calculated at the full `$1.10 per $1,000` in five special cities including Los
  Angeles.
* **Eaton Fire fatalities.** The CAL FIRE incident page states **19**, resolving a 17-versus-19 discrepancy between
  two earlier layers.

## 3. What was changed in this session

| Area | Change |
|---|---|
| `data/evidence.json` | Rebuilt: 31 sources, 166 rows across 10 categories, each row carrying geography, period, source and status. All values re-read on 2026-11-10. |
| `scripts/build.py` | Rewritten: dashboard shell, 12 category pages, computed derivatives, filterable tables, no hand-typed figure. |
| `scripts/validate.py` | Rewritten: provenance, blank-when-unverified, derived arithmetic (recomputed), links, hygiene, privacy patterns, determinism. |
| `scripts/stage_pages.py` | Rewritten: stages the exact artifact, verifies rows inside cells, anchors, and compares Jekyll output byte for byte in CI. |
| `tools/check_links.py` | Rewritten: official/issuer host allowlist on every rendered link, blocked-host matching by host only (a path substring had previously produced false positives). |
| `tools/pii_scan.py` | Extended to the curated artifact; account handle reclassified as repository metadata and reported separately. |
| `_config.yml` | Fixed the `assets/app.js` exclusion; excluded every legacy layer. |
| `.github/workflows/validate.yml` | Build → validate → link audit → privacy → stage → committed-matches-build → Jekyll byte comparison. |
| Root pages | `place.html` removed and replaced by `geography.html`; all other pages regenerated. |
| Legacy layers | One additive link per page back to the curated dashboard, implemented once at the end of the session so that `_dashboard_src/verify.py`'s determinism check still passes. |
| `README.md`, `EXECUTIVE_SUMMARY.md`, this file, `research/VERIFICATION-2026-11-10.md` | Rewritten for the current state. |

## 4. Standing request to other sessions

`XR-4f0b3fa2-a` — the legacy layers should eventually be reduced to one archived folder. Six dashboards with six
different answers is a risk to the owner, not an asset: a reader who finds `decision-file/` will get a different
recommendation from a reader who finds the root site. Consolidating them is a change to files owned by other sessions,
so it is requested here rather than executed.
