# Verification — final integration

**Audit date:** 2026-11-10  
**Public scope:** the 12-page curated root dashboard only. Historical companion layers remain in the repository for audit and are not represented as verified.

## Evidence verification

- **155 category rows** were reviewed against direct government or issuer pages.
- **30 official/issuer sources** are registered in `data/evidence.json`.
- The complete row-by-row record, including corrections and source links, is [`research/VERIFICATION-2026-11-10-1f62010a.md`](research/VERIFICATION-2026-11-10-1f62010a.md).
- Every `Verified` observation was matched to its publisher, geography, period and measure.
- Every `Unverified` value cell is blank. No sale price, cap rate, rent, owner tax rate, renewal probability or parcel-level forecast was inferred.
- `Analysis` rows are conditional judgments; their links support context, not the conclusion.

## Material findings

1. Closed the county documentary-transfer-tax gap: **$0.55 per $500 (0.11%)** from the LA County Registrar-Recorder.
2. Closed the district graduation gap with exact 2026 measures: **86.2% four-year; 87.6% combined four/five-year** for LAUSD.
3. Corrected the BLS category from “food at home” to **Food**, split mixed-geography and mixed-incident rows, and updated DGS10 to **4.86% on 2026-11-06**.
4. Added SCAG’s adopted 2030 planning outputs without extrapolating them or calling them a property forecast.
5. Flagged the official Assessment Roll page’s internal **4.42% / “42%”** inconsistency; published 4.42%, consistent with its narrative and $96 billion change.
6. Excluded `/advisory/` and `/dashboard/` from Pages because their numerical extrapolations/rankings are not established by official citations.

## Automated checks

Run from the repository root:

```bash
python scripts/build.py
python scripts/validate.py
python scripts/stage_pages.py
python tools/check_site.py
python tools/linkcheck.py
python tools/check_links.py
python tools/pii_scan.py
python _advisory_src/verify_advisory.py
python _dashboard_src/verify.py
git diff --exit-code -- '*.html'
```

The build is deterministic and dependency-free. `scripts/stage_pages.py` validates links and row provenance in the actual artifact. GitHub Actions additionally performs a Jekyll build and byte-for-byte artifact comparison.

## Privacy

The subject is **Asset A** and the owner is **Owner A**. No owner identity, exact address, parcel identifier, personal contact information, personal financial value, private lease, tracker, form or third-party script is included in the public site. Public agency pages reached through source links have their own privacy practices; GitHub may retain standard hosting logs.

## Decision limitation

The recommendation is deliberately conditional: run a sale track and a written-renewal track, then select the documented after-tax outcome. Public data cannot determine the owner's personal optimal choice without the executed lease, exact term, rent, guaranty, tax basis, debt, insurance and store economics. Those remain blank and flagged rather than guessed.
