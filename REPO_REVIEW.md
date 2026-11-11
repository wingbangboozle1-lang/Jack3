# Repository review — final integration

**Reviewed:** 2026-11-11 (repository-wide review originally written 2026-11-10 for session `1f62010a`; refresh below by session `c350ccea`)

## Current public architecture

The repository contains several generations of parallel research. The final integration publishes one curated root dashboard: `index.html`, nine evidence/category pages, a `questions.html` discovery register, `review.html`, `sources.html`, and `assets/style.css` — thirteen HTML pages in all. `scripts/build.py` generates those pages from `data/evidence.json`; `scripts/stage_pages.py` creates the exact Pages artifact.

This removes conflicting live recommendations and prevents stale repository-only pages from being mistaken for the current analysis.

## Irregularities retained for review

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| J-IR-01 | High | `/advisory/` contains scenario weights and pathway rankings not established by its official citations. | Excluded from Pages; preserved for audit. |
| J-IR-02 | High | `/dashboard/` extrapolates population, employment and CPI-linked rent and contains qualitative claims beyond the cited evidence. | Excluded from Pages; preserved for audit. |
| J-IR-03 | High | Other historical layers include third-party commercial sources, stale figures, unsourced rows and conflicting recommendations. | Excluded from Pages; not represented as reverified. |
| J-IR-04 | Medium | Some historical HTML files render the repository account handle. | Not included in the curated public artifact. No owner identity or personal information was researched. |
| J-IR-05 | Medium | The LA County Assessment Roll official release says 4.42% in narrative but “42%” in a bullet. | Published 4.42%, flagged on `review.html`. |
| J-IR-06 | Medium | Earlier material labeled LAUSD’s combined graduation rate as a four-year rate. | Corrected on 2026-11-10 to 86.2% four-year and 87.6% combined; both later withdrawn as unverified on 2026-11-11 (see C-IR-01). |
| J-IR-07 | Medium | Earlier material cited mixed city/county values or two fire incidents with only one row-level source. | Split into single-source rows. |
| J-IR-08 | Low | The BLS Food category was labeled “food at home.” | Corrected to Food. |
| J-IR-09 | Low | FY2026 full-year tenant results are not yet available; issuer schedules them for 2026-12-09. | Q3 remains latest; future release flagged. |

### Irregularities added 2026-11-11 (`c350ccea`)

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| C-IR-01 | **High** | Two LAUSD graduation rows marked Verified could not be re-read from their cited page: the 2026 School Dashboard serves its tables client-side and returned no values. | Rows set to Unverified with blank values; prior figures preserved only in the explanation. Server-rendered CDE DataQuest (87.4%) and CDE release 26-44 (87.9%) added as separately labelled Verified rows. |
| C-IR-02 | Medium | The 10-year Treasury anchor advanced from 4.86% (2026-11-06) to 4.88% (2026-11-09) between publication and this pass. | Both dated observations published; the projection module keeps 4.86% with its date and discloses it. |
| C-IR-03 | Medium | Ten open pull requests from earlier sessions propose competing data contracts for the same pages (#42 a 222-row canonical site, #43 publication-integrity tests, #31/#32/#36/#40/#26/#22/#12/#4 older branches). Several are `CONFLICTING`. | None merged in this pass: each would replace the verified dataset without a line-by-line re-check. Reported for the owner. |
| C-IR-04 | Low | The repository's own gates did not test the published artifact for PII, non-official hosts or unused sources. `tools/check_site.py` and `tools/linkcheck.py` still point at legacy `brief/` and `analysis/` trees. | New `tools/check_public.py` tests the artifact and runs in CI; the legacy scripts are left untouched (they cover layers that are not published). |
| C-IR-05 | Low | Generated site text contained stale counts ("nine pages", "twelve pages") and the snapshot stamp read 10 Nov. | Corrected in the generator; pages regenerated. |
| C-IR-06 | Low | The Assessment Roll release still prints "42%" in a highlights bullet against a 4.42% narrative. | Unchanged and unresolved upstream; 4.42% published, typo flagged on `review.html`. |

## Verification boundary

A source link does not make an inference official. Government and issuer pages substantiate observations; they do not establish Asset A’s value, optimal sale date, tenant renewal intention, store closure probability or catastrophe loss. Those remain analytical gaps.

No historical directory was deleted. Excluding a directory from the Pages artifact is a publication-safety decision, not a claim that its repository history was erased.

## Final decision support

The only current public recommendation is the conditional dual track: confidential market testing plus written renewal negotiations, followed by an after-tax comparison of actual offers and enforceable terms. It is explicitly analyst judgment—not an appraisal or personalized financial, legal or tax opinion.

See [`research/VERIFICATION-2026-11-10-1f62010a.md`](research/VERIFICATION-2026-11-10-1f62010a.md) for all 155 row-level checks and [`review.html`](review.html) for the public Flagged for Review register.
