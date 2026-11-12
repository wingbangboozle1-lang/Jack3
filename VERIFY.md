# Verification — canonical publication

**Audit date:** 2026-11-12  
**Public scope:** 22 static HTML pages (21 shared-navigation pages including `suggestions.html` and `questions.html`, plus the `flagged.html` alias), 230 evidence rows (199 verified, 4 derived, 1 analysis, 26 blank), 16 decision Q&A rows, 24 risks, 25 review flags (`F-01`–`F-25`), 24 repo-review findings, and 40 official/issuer sources. Historical companion layers are excluded.

## Evidence and corrections

- Every canonical row and all 40 official/issuer sources were independently re-read on 2026-11-12. The complete row disposition register is [`research/VERIFICATION-2026-11-12-f0b78eb6.md`](research/VERIFICATION-2026-11-12-f0b78eb6.md) (superseding the 2026-11-11 review in [`research/VERIFICATION-2026-11-11-d644184d.md`](research/VERIFICATION-2026-11-11-d644184d.md) and complementing the generated register [`research/VERIFICATION-2026-11-10-b98090a0.md`](research/VERIFICATION-2026-11-10-b98090a0.md)).
- Closed gaps and factual fixes verified on 2026-11-12:
  - Fixed Census QuickFacts V2025 population vintage date typos (`2026-07-01` → `2025-07-01`).
  - Closed `F-12` via City of Los Angeles Wages LA: general minimum wage is **$18.42/hour effective 2026-07-01** (AB 1228 $20.00/hour fast-food floor still governs covered chains).
  - Verified FY2025 Form 10-K Item 2 (`941` California units of `2,136`; property tenure split `164`/`565`/`1,020`/`387`; `~13%` percentage-rent leases), Item 7 (`$1,874k` FY2025 Franchise AUV vs `$1,949k` FY2024), Note 8 (`11.2`-year weighted-average remaining operating lease term at `6.1%`), and the issuer's **2026-12-09** Q4/FY2026 earnings webcast notice (`2,115` systemwide stores).
  - Verified finalized 2026 federal LTCG taxable-income thresholds under **IRS Rev. Proc. 2025-32 § 4.03** (`$98,900` / `$613,700` MFJ), while flagging that IRS Topic 409 still displays 2025 numbers and draft 2027 guidance (`rp-26-35.pdf`) carries `[Release Date, 2026]` placeholders (`F-16`).
  - Confirmed `hazards.fema.gov/nri/` returned HTTP 500 on 2026-11-12 (`F-18` live portal remains blank) while publishing archived March 2023 NRI v1.19.0 LA County context (`$3.9B` EAL / `$5.3B` Risk Value) from official FEMA PrepToolkit with explicit vintage caveats.
  - Closed `F-25` in `scripts/projection.py` by aligning `TREASURY_ANCHOR` and `DISCOUNT_RATES[0]` (`0.0486` → `0.0488`) with the 2026-11-09 DGS10 observation.
- DGS10 is **4.88% on 2026-11-09**. It remains a dated market reference, not a forecast or mandatory discount-rate floor.
- LAUSD is **87.4% four-year ACGR (2025–26 DataQuest)** and **87.6% combined four-/five-year (2026 Dashboard file)**. These are distinct measures and carry separate direct CDE links.
- Every `Verified` observation retains its publisher, geography, period and measure. Every `Blank` value is empty and flagged. `Analysis` and `Derived` rows are not promoted to official observations.

## Automated gates

```bash
python3 scripts/build_canonical.py
python3 scripts/validate.py
python3 scripts/projection.py
python3 scripts/stage_pages.py
python3 -m unittest discover -s scripts -p 'test_publication.py' -v
python3 tools/check_site.py
python3 tools/linkcheck.py
python3 tools/check_links.py
python3 tools/pii_scan.py
python3 _advisory_src/verify_advisory.py
python3 _dashboard_src/verify.py
git diff --exit-code -- '*.html'
```

The canonical build is deterministic and dependency-free. Validation checks row provenance, official hosts, blank-value handling, every table row, local links/fragments, shared navigation, prohibited embeds, privacy and deterministic regeneration. Staging validates the actual **23-file artifact** (`22` HTML pages plus `assets/style.css`), and publication regression tests assert its exact inventory and parser contracts.

## Privacy and decision limits

Asset A and Owner A are placeholders. No owner identity, exact address, parcel identifier, personal contact information, tenant officer/IR contact name, private financial value, executed lease, tracker, form or third-party script is published. The privacy scan found zero findings.

The recommendation remains a conditional dual track: privately verify lease dates and notice rights now, and explore confidential sale interest alongside a written renewal request on a timeline consistent with those lease documents. No fixed marketing window (`24–36 months` is illustrative only), minimum renewal length (`no minimum term is established`), price, cap rate, rent, optimal sale year, renewal probability, disaster probability or calibrated parcel forecast is asserted. Missing lease, property, tax, insurance and owner facts remain blank rather than guessed.
