# Repository review — final integration

**Reviewed:** 2026-11-10  
**Reviewer session:** `1f62010a`

## Current public architecture

The repository contains several generations of parallel research. The final integration publishes one curated root dashboard: `index.html`, ten evidence/category pages, `sources.html`, and `assets/style.css`. `scripts/build.py` generates those pages from `data/evidence.json`; `scripts/stage_pages.py` creates the exact Pages artifact.

This removes conflicting live recommendations and prevents stale repository-only pages from being mistaken for the current analysis.

## Irregularities retained for review

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| J-IR-01 | High | `/advisory/` contains scenario weights and pathway rankings not established by its official citations. | Excluded from Pages; preserved for audit. |
| J-IR-02 | High | `/dashboard/` extrapolates population, employment and CPI-linked rent and contains qualitative claims beyond the cited evidence. | Excluded from Pages; preserved for audit. |
| J-IR-03 | High | Other historical layers include third-party commercial sources, stale figures, unsourced rows and conflicting recommendations. | Excluded from Pages; not represented as reverified. |
| J-IR-04 | Medium | Some historical HTML files render the repository account handle. | Not included in the curated public artifact. No owner identity or personal information was researched. |
| J-IR-05 | Medium | The LA County Assessment Roll official release says 4.42% in narrative but “42%” in a bullet. | Published 4.42%, flagged on `review.html`. |
| J-IR-06 | Medium | Earlier material labeled LAUSD’s combined graduation rate as a four-year rate. | Corrected to 86.2% four-year and 87.6% combined for 2026. |
| J-IR-07 | Medium | Earlier material cited mixed city/county values or two fire incidents with only one row-level source. | Split into single-source rows. |
| J-IR-08 | Low | The BLS Food category was labeled “food at home.” | Corrected to Food. |
| J-IR-09 | Low | FY2026 full-year tenant results are not yet available; issuer schedules them for 2026-12-09. | Q3 remains latest; future release flagged. |

## Verification boundary

A source link does not make an inference official. Government and issuer pages substantiate observations; they do not establish Asset A’s value, optimal sale date, tenant renewal intention, store closure probability or catastrophe loss. Those remain analytical gaps.

No historical directory was deleted. Excluding a directory from the Pages artifact is a publication-safety decision, not a claim that its repository history was erased.

## Final decision support

The only current public recommendation is the conditional dual track: confidential market testing plus written renewal negotiations, followed by an after-tax comparison of actual offers and enforceable terms. It is explicitly analyst judgment—not an appraisal or personalized financial, legal or tax opinion.

See [`research/VERIFICATION-2026-11-10-1f62010a.md`](research/VERIFICATION-2026-11-10-1f62010a.md) for all 155 row-level checks and [`review.html`](review.html) for the public Flagged for Review register.
