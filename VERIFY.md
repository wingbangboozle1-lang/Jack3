# Verification — canonical publication

**Audit date:** 2026-11-12  
**Public scope:** 22 static HTML pages (21 shared-navigation pages including `suggestions.html` and `questions.html`, plus the `flagged.html` alias), 240 evidence rows (211 verified, 2 derived, 1 analysis, 26 blank), 20 information-register questions, 16 decision Q&A rows, 24 risks, 8 pathway-risk rows, 31 review flags (`F-01`–`F-31`), 36 repo-review findings, and 45 official/issuer sources. Historical companion layers are excluded.

## Evidence and corrections

- Three separate verification passes were completed on 2026-11-12:
  - Session `7b04b8ee` independently fetched and verified all **45** official/issuer sources and all **240** canonical rows line by line ([`research/VERIFICATION-2026-11-12-7b04b8ee.md`](research/VERIFICATION-2026-11-12-7b04b8ee.md)), audited the repository line by line ([`research/REPO-REVIEW-2026-11-12-7b04b8ee.md`](research/REPO-REVIEW-2026-11-12-7b04b8ee.md)), published a companion anonymized decision dossier ([`research/DECISION-DOSSIER-2026-11-12-7b04b8ee.md`](research/DECISION-DOSSIER-2026-11-12-7b04b8ee.md)), and added 6 automated unit tests in `scripts/test_projection.py` locking `scripts/projection.py`'s `0.0488` FRED `DGS10` anchor against `data/canonical.json`.
  - Session `c56c569e` re-read the publisher page behind every `Verified` and `Derived` row, including the rows added that day by session `f0b78eb6`; its generated register, [`research/VERIFICATION-2026-11-12-c56c569e.md`](research/VERIFICATION-2026-11-12-c56c569e.md), lists the documents read only in part and the three items it did not confirm (the graduate count in the 2026 CDE data file, the prior-year city wage in a row note, and the reported FEMA portal error and draft 2027 revenue procedure).
- Session `f0b78eb6` reported re-reading every canonical row and all 40 sources then in the register. Its row disposition register is [`research/VERIFICATION-2026-11-12-f0b78eb6.md`](research/VERIFICATION-2026-11-12-f0b78eb6.md) (superseding the 2026-11-11 review in [`research/VERIFICATION-2026-11-11-d644184d.md`](research/VERIFICATION-2026-11-11-d644184d.md) and the earlier generated register [`research/VERIFICATION-2026-11-10-b98090a0.md`](research/VERIFICATION-2026-11-10-b98090a0.md), which the build no longer rewrites).
- Further corrections by session `c56c569e` on 2026-11-12: city poverty relabelled ACS 5-year and county SAIPE 1-year from the Census source note; LAUSD chronic absenteeism refreshed to **21.3%** and the English-learner four-year rate to **67.7%** from the 2026 Dashboard; combined city transfer-tax rates **4.45%** / **5.95%** relabelled `Verified`; the **3.8%** net investment income tax added from IRS Topic 559; the archived FEMA row label corrected to Community Risk Factor; three FY2025 Form 10-K rows added (typical 20-year initial lease term, the issuer's statement on renewals, 86 restaurants closed in fiscal 2025); and issuer governance rows added from EDGAR without naming any individual.
- Closed gaps and factual fixes verified on 2026-11-12:
  - Fixed Census QuickFacts V2025 population vintage date typos (`2026-07-01` → `2025-07-01`).
  - Closed `F-12` via City of Los Angeles Wages LA: general minimum wage is **$18.42/hour effective 2026-07-01** (AB 1228 $20.00/hour fast-food floor still governs covered chains).
  - Verified FY2025 Form 10-K Item 2 (`941` California units of `2,136`; property tenure split `164`/`565`/`1,020`/`387`; `~13%` percentage-rent leases), Item 7 (`$1,874k` FY2025 Franchise AUV vs `$1,949k` FY2024), Note 8 (`11.2`-year weighted-average remaining operating lease term at `6.1%`), and the issuer's **2026-12-09** Q4/FY2026 earnings webcast notice (`2,115` systemwide stores).
  - Verified finalized 2026 federal LTCG taxable-income thresholds under **IRS Rev. Proc. 2025-32 § 4.03** (`$98,900` / `$613,700` MFJ), while flagging that IRS Topic 409 still displays 2025 numbers and draft 2027 guidance (`rp-26-35.pdf`) carries `[Release Date, 2026]` placeholders (`F-16`).
  - Confirmed `hazards.fema.gov/nri/` returned HTTP 500 on 2026-11-12 (`F-18` live portal remains blank) while publishing archived March 2023 NRI v1.19.0 LA County context (`$3.9B` EAL / `$5.3B` Risk Value) from official FEMA PrepToolkit with explicit vintage caveats.
  - Closed `F-25` in `scripts/projection.py` by aligning `TREASURY_ANCHOR` and `DISCOUNT_RATES[0]` (`0.0486` → `0.0488`) with the 2026-11-09 DGS10 observation; later refreshed to `0.0510` for the 2026-11-12 observation (see session `arena/c155a72c-jack3`).
- DGS10 is **5.10% on 2026-11-12** (read 2026-11-13; prior print 4.88% on 2026-11-09). It remains a dated market reference, not a forecast or mandatory discount-rate floor.
- LAUSD is **87.4% four-year ACGR (2025–26 DataQuest)** and **87.6% combined four-/five-year (2026 Dashboard file)**. These are distinct measures and carry separate direct CDE links.
- Every `Verified` observation retains its publisher, geography, period and measure. Every `Blank` value is empty and flagged. `Analysis` and `Derived` rows are not promoted to official observations.

## Automated gates

```bash
python3 scripts/build_canonical.py
python3 scripts/validate.py
python3 scripts/projection.py
python3 scripts/stage_pages.py
python3 -m unittest discover -s scripts -p 'test_*.py' -v
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
