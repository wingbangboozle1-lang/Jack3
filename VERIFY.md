# Verification — canonical publication

- **Current register snapshot:** 2026-11-16 (targeted re-reads plus the private calculator and private-workflow pages; see the 2026-11-16 section below).
- **Last full line-by-line source audit:** 2026-11-12 (240 rows / 45 sources).
- **Current public scope:** 24 static HTML pages (23 shared-navigation pages plus the `flagged.html` alias), 260 evidence rows (230 verified, 3 derived, 1 analysis, 26 blank), 20 information-register questions, 16 decision Q&A rows, 24 risks, 8 pathway-risk rows, 32 review flags (`F-01`–`F-32` plus `F-33`–`F-35` added 2026-11-15), 36 repo-review findings, and 53 official/issuer sources. Historical companion layers are excluded.

## Evidence and corrections

- Three separate verification passes were completed on 2026-11-12:
  - Session `7b04b8ee` independently fetched and verified all **45** official/issuer sources and all **240** canonical rows line by line ([`research/VERIFICATION-2026-11-12-7b04b8ee.md`](research/VERIFICATION-2026-11-12-7b04b8ee.md)), audited the repository line by line ([`research/REPO-REVIEW-2026-11-12-7b04b8ee.md`](research/REPO-REVIEW-2026-11-12-7b04b8ee.md)), published a companion anonymized decision dossier ([`research/DECISION-DOSSIER-2026-11-12-7b04b8ee.md`](research/DECISION-DOSSIER-2026-11-12-7b04b8ee.md)), and added 6 automated unit tests in `scripts/test_projection.py` locking `scripts/projection.py`'s then-current `0.0488` FRED `DGS10` anchor against `data/canonical.json` (subsequently refreshed in the 2026-11-13 supplement below).
  - Session `c56c569e` re-read the publisher page behind every `Verified` and `Derived` row, including the rows added that day by session `f0b78eb6`; its generated register, [`research/VERIFICATION-2026-11-12-c56c569e.md`](research/VERIFICATION-2026-11-12-c56c569e.md), lists the documents read only in part and the three items it did not confirm (the graduate count in the 2026 CDE data file, the prior-year city wage in a row note, and the reported FEMA portal error and draft 2027 revenue procedure).
- Session `f0b78eb6` reported re-reading every canonical row and all 40 sources then in the register. Its row disposition register is [`research/VERIFICATION-2026-11-12-f0b78eb6.md`](research/VERIFICATION-2026-11-12-f0b78eb6.md) (superseding the 2026-11-11 review in [`research/VERIFICATION-2026-11-11-d644184d.md`](research/VERIFICATION-2026-11-11-d644184d.md) and the earlier generated register [`research/VERIFICATION-2026-11-10-b98090a0.md`](research/VERIFICATION-2026-11-10-b98090a0.md), which the build no longer rewrites).
- Further corrections by session `c56c569e` on 2026-11-12: city poverty relabelled ACS 5-year and county SAIPE 1-year from the Census source note; LAUSD chronic absenteeism refreshed to **21.3%** and the English-learner four-year rate to **67.7%** from the 2026 Dashboard; combined city transfer-tax rates **4.45%** / **5.95%** relabelled `Verified`; the **3.8%** net investment income tax added from IRS Topic 559; the archived FEMA row label corrected to Community Risk Factor; three FY2025 Form 10-K rows added (typical 20-year initial lease term, the issuer's statement on renewals, 86 restaurants closed in fiscal 2025); and issuer governance rows added from EDGAR without naming any individual.
- Closed gaps and factual fixes verified on 2026-11-12:
  - Fixed Census QuickFacts V2025 population vintage date typos (`2026-07-01` → `2025-07-01`).
  - Closed `F-12` via City of Los Angeles Wages LA: general minimum wage is **$18.42/hour effective 2026-07-01** (AB 1228 $20.00/hour fast-food floor still governs covered chains).
  - Verified FY2025 Form 10-K Item 2 (`941` California units of `2,136`; property tenure split `164`/`565`/`1,020`/`387`; `~13%` percentage-rent leases), Item 7 (`$1,874k` FY2025 Franchise AUV vs `$1,949k` FY2024), Note 8 (`11.2`-year weighted-average remaining operating lease term at `6.1%`), and the issuer's **2026-12-09** Q4/FY2026 earnings webcast notice (`2,115` systemwide stores).
  - Verified finalized 2026 federal LTCG taxable-income thresholds under **IRS Rev. Proc. 2025-32 § 4.03** (`$98,900` / `$613,700` MFJ), while flagging that IRS Topic 409 still displays 2025 numbers and draft 2027 guidance (`rp-26-35.pdf`) carries `[Release Date, 2026]` placeholders (`F-16`).
  - Confirmed `hazards.fema.gov/nri/` returned HTTP 500 on 2026-11-12 (`F-18` live portal remains blank) while publishing archived March 2023 NRI v1.19.0 LA County context (`$3.9B` EAL / `$5.3B` Risk Value) from official FEMA PrepToolkit with explicit vintage caveats.
  - Closed `F-25` in `scripts/projection.py` by aligning `TREASURY_ANCHOR` and `DISCOUNT_RATES[0]` (`0.0486` → `0.0488`) with the 2026-11-09 DGS10 observation.
- Dated DGS10 observations: **4.98% on 2026-11-10** and **5.10% on 2026-11-12** (latest shown on 2026-11-13); no observation was displayed for 2026-11-11. **4.88% on 2026-11-09** is retained as historical. These are market references, not a property forecast, cap rate or mandatory discount-rate floor.
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

The canonical build is deterministic and dependency-free. Validation checks row provenance, official hosts, blank-value handling, every table row, local links/fragments, shared navigation, prohibited embeds, privacy and deterministic regeneration. Staging validates the actual **25-file artifact** (`24` HTML pages plus `assets/style.css`), and publication regression tests assert its exact inventory and parser contracts.

Two disclosed exceptions to the historical no-JavaScript rule (2026-11-16): `calculator.html` (sell-versus-hold after-tax worksheet plus short-lease-discount pricer) and the `master.html` register filter embed inline engines. `scripts/validate.py` and `scripts/test_publication.py` prove that the engine is inline (no `src`), makes no network request (`fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `sendBeacon`, `import(`, any `http(s)://` reference), stores nothing (`localStorage`, `sessionStorage`, `indexedDB`, `document.cookie`), executes nothing dynamically (`eval`, `new Function`), does not navigate or message out (`location`, `postMessage`), and that every other published page remains completely script-free. The calculators' arithmetic is tested line by line by `node tools/calculator_engine_test.js` against an independent re-implementation of the verified rules (per-$500 rounding-up, ULA tiers and boundaries, §1250 recapture, LTCG/NIIT/California treatment, discounted hold case with after-tax exit, short-lease discount per remaining year, blank-input honesty, loss case with zero taxes) — 31 checks, all passing.

## Privacy and decision limits

Asset A and Owner A are placeholders. No owner identity, exact address, parcel identifier, personal contact information, tenant officer/IR contact name, private financial value, executed lease, tracker, form or third-party script is published. The privacy scan found zero findings.

The recommendation remains a conditional dual track: privately verify lease dates and notice rights now, and explore confidential sale interest alongside a written renewal request on a timeline consistent with those lease documents. No fixed marketing window (`24–36 months` is illustrative only), minimum renewal length (`no minimum term is established`), price, cap rate, rent, optimal sale year, renewal probability, disaster probability or calibrated parcel forecast is asserted. Missing lease, property, tax, insurance and owner facts remain blank rather than guessed.

## Targeted freshness update — 2026-11-13

The [Federal Reserve Bank of St. Louis FRED DGS10](https://fred.stlouisfed.org/series/DGS10) page read on 2026-11-13 showed **5.10% for 2026-11-12**, no observation for 2026-11-11, **4.98% for 2026-11-10**, and **4.88% for 2026-11-09**. PR #76 refreshed the current anchor and dimensionless sensitivity input to 5.10%; this follow-up retains 4.88% as history, adds the 4.98% dated row and regenerates the 242-row current register. The 2026-11-12 240-row / 45-source audit remains unchanged. See [`research/AUDIT-2026-11-13-02fb510c.md`](research/AUDIT-2026-11-13-02fb510c.md) and the [`current generated register`](research/VERIFICATION-2026-11-13-406ca5a9.md). This is still a targeted DGS10 update, not a new line-by-line verification of all current rows.

## Targeted update — 2026-11-16 (session `arena/87ca5536-jack3`)

Scope of this update (no full-register re-audit claimed; the 2026-11-12 audit remains the last complete pass):

- **FRED DGS10 re-read (no value change):** the official page fetched 2026-11-16 still showed **5.10% for 2026-11-12** as the latest observation (page updated 2026-11-13 3:16 PM CST; no observation for 2026-11-11 or 2026-11-13; next release 2026-11-16). The register rows were updated to record the re-read; no value changed.
- **Rule constants re-read (unchanged):** [Measure ULA FAQ](https://finance.lacity.gov/faq/measure-ula) — base 0.45% ($2.25 per $500, base value rounded up to the nearest $500), ULA 4% above $5,400,000 / 5.5% at or above $10,900,000 effective for transactions closing after 2026-06-30, annual Chained-CPI indexation; [IRS Topic 409](https://www.irs.gov/taxtopics/tc409) — 0/15/20% structure, unrecaptured §1250 gain at a 25% maximum rate, NIIT via Topic 559. Both matched the register exactly and are now encoded (with links) in the private calculator.
- **Five official data-tool sources added after live fetch on 2026-11-16:** [Census Geocoder](https://geocoding.geo.census.gov/geocoder/), [data.census.gov](https://data.census.gov/), [LEHD OnTheMap](https://onthemap.ces.census.gov/) (2024 data notice dated 2026-11-05), [LADOT Traffic Counts on the City GeoHub](https://geohub.lacity.org/maps/a27ad0d462f74efb92bfa230e5f64239) (dataset updated 2020-08-26), and the [California School Directory](https://sd.cde.ca.gov/SchoolDirectory/). Each backs one new Geography/Schools workflow row; the rows describe the tools, not any parcel.
- **Checked and deliberately not cited:** the FEMA Flood Map Service Center returned HTTP 500 on 2026-11-16 (same failure mode as open flag F-18); the registered fema.gov/flood-maps source remains in use.
- **New pages/sections:** `calculator.html` (private after-tax calculator and short-lease-discount pricer, SG-01B, mandated by the owner brief), the decision-gate progress board on `decisions.html`, the parcel hazard screening sheet on `hazards.html`, and the private trade-area workflow on `geography.html`. No owner figure, address, parcel identifier or tract identifier is published anywhere; all new "status" cells honestly read Open / Not performed here.
- **Engine arithmetic verification:** `node tools/calculator_engine_test.js` — 31 checks against an independent re-implementation, all passing (per-$500 rounding, ULA tier boundary at exactly $10,900,000, county-only jurisdiction, recapture/LTCG/NIIT/CA ordering, discounted hold case with terminal sale, short-lease discount per remaining year, blank-input honesty, loss case with zero taxes).
- **Privacy scan:** 0 findings across all published files; the calculator page stores and transmits nothing.
