# Verification — final integration

**Audit date:** 2026-11-11 (supersedes the 2026-11-10 pass)  
**Public scope:** the 12-page curated root dashboard only. Historical companion layers remain in the repository for audit and are not represented as verified.

## Evidence verification

- **163 category rows** are verified against direct government or issuer pages; **20 open questions** and 4 answered questions are registered separately.
- **33 official/issuer sources** are registered in `data/evidence.json`.
- The current row-by-row record is [`research/VERIFICATION-2026-11-11-c350ccea.md`](research/VERIFICATION-2026-11-11-c350ccea.md); the 2026-11-10 record is retained as history.
- Every `Verified` observation was matched to its publisher, geography, period and measure.
- Every `Unverified` value cell is blank. No sale price, cap rate, rent, owner tax rate, renewal probability or parcel-level forecast was inferred.
- `Analysis` rows are conditional judgments; their links support context, not the conclusion.

## Material findings

1. Closed the county documentary-transfer-tax gap: **$0.55 per $500 (0.11%)** from the LA County Registrar-Recorder.
2. **Reversed** the district graduation claim on 2026-11-11. The 2026 Dashboard page renders its tables in
   the browser and served no values, so 86.2% (four-year) and 87.6% (combined) are now **withheld as
   unverified and blank**. Server-rendered CDE sources now supply a Verified **87.4%** LAUSD four-year rate
   (charter schools excluded) and a Verified **87.9%** statewide rate.
3. Corrected the BLS category from “food at home” to **Food**, split mixed-geography and mixed-incident rows, and dated the Treasury anchor: **4.86% on 2026-11-06**, plus **4.88% on 2026-11-09** at the 2026-11-11 re-read.
4. Added SCAG’s adopted 2030 planning outputs without extrapolating them or calling them a property forecast.
5. Flagged the official Assessment Roll page’s internal **4.42% / “42%”** inconsistency; published 4.42%, consistent with its narrative and $96 billion change.
6. Excluded `/advisory/` and `/dashboard/` from Pages because their numerical extrapolations/rankings are not established by official citations.

## Automated checks

Run from the repository root:

```bash
python scripts/build.py
python scripts/validate.py
python scripts/stage_pages.py
python tools/check_public.py
python tools/check_site.py
python tools/linkcheck.py
python tools/check_links.py
python tools/pii_scan.py
python _advisory_src/verify_advisory.py
python _dashboard_src/verify.py
git diff --exit-code -- '*.html'
```

`tools/check_public.py` is the strict gate: it tests the published artifact for its exact file set, broken
internal links, non-official hosts, rows without a registered source, an Unverified row that carries a value,
personal-information patterns, embedded scripts/forms/trackers, and unused sources. Current result: 13 pages,
244 body rows, 236 internal and 249 external links, all passing.

The build is deterministic and dependency-free. `scripts/stage_pages.py` validates links and row provenance in the actual artifact. GitHub Actions additionally performs a Jekyll build and byte-for-byte artifact comparison.

## Privacy

The subject is **Asset A** and the owner is **Owner A**. No owner identity, exact address, parcel identifier, personal contact information, personal financial value, private lease, tracker, form or third-party script is included in the public site. Public agency pages reached through source links have their own privacy practices; GitHub may retain standard hosting logs.

## Decision limitation

The recommendation is deliberately conditional: run a sale track and a written-renewal track, then select the documented after-tax outcome. Public data cannot determine the owner's personal optimal choice without the executed lease, exact term, rent, guaranty, tax basis, debt, insurance and store economics. Those remain blank and flagged rather than guessed.
