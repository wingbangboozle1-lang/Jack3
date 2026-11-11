# Verification — canonical publication

**Audit date:** 2026-11-11  
**Public scope:** 21 static HTML pages (20 shared-navigation pages plus the `flagged.html` alias), 223 evidence rows, 16 decision Q&A rows and 36 official/issuer sources. Historical companion layers are excluded.

## Evidence and corrections

- Load-bearing Census, BLS, issuer, FRED, wage, tax, hazard, CDE, SCAG, DOF and local-agency sources were independently re-read. The complete current row disposition register is [`research/VERIFICATION-2026-11-11-d644184d.md`](research/VERIFICATION-2026-11-11-d644184d.md).
- DGS10 is refreshed to **4.88% on 2026-11-09**. It remains a dated modeling anchor, not a forecast or the owner's required return.
- LAUSD is **87.4% four-year ACGR (2025–26 DataQuest)** and **87.6% combined four-/five-year (2026 Dashboard file)**. These are distinct measures and have separate direct CDE links.
- Every `Verified` observation retains its publisher, geography, period and measure. Every `Blank` value is empty and flagged. `Analysis` and `Derived` rows are not promoted to official observations.
- The 16-row Questions & Answers page states current answers, missing evidence, discovery routes and decision consequences. Private documents stay offline.

## Automated gates

```bash
python scripts/build_canonical.py
python scripts/validate.py
python scripts/projection.py
python scripts/stage_pages.py
python -m unittest discover -s scripts -p 'test_publication.py' -v
python tools/check_site.py
python tools/linkcheck.py
python tools/check_links.py
python tools/pii_scan.py
python _advisory_src/verify_advisory.py
python _dashboard_src/verify.py
git diff --exit-code -- '*.html'
```

The canonical build is deterministic and dependency-free. Validation checks row provenance, official hosts, blank-value handling, every table row, local links/fragments, shared navigation, prohibited embeds, privacy and deterministic regeneration. Staging validates the actual 22-file artifact (21 HTML pages plus CSS), and publication regression tests cover its exact inventory.

## Privacy and decision limits

Asset A and Owner A are placeholders. No owner identity, exact address, parcel identifier, personal contact information, private financial value, executed lease, tracker, form or third-party script is published. The privacy scan found zero findings.

The recommendation remains a conditional dual track: confidential market testing 24–36 months before the earliest verified expiry, in parallel with a written renewal request. No price, cap rate, rent, optimal sale year, renewal probability, disaster probability or calibrated parcel forecast is asserted. Missing lease, property, tax, insurance and owner facts remain blank rather than guessed.
