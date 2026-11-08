# Repository Review & Multi-Layer Audit (`Jack3`)

**Review Date:** 2026-11-08 (UTC) · **Branch:** `arena/f47ec184-jack3` (rebased onto `origin/main` `febe6ea`)

---

## 1. Repository Origin & Evolution

1. **Initial state (`0c9e609`, 2026-11-06):** The repository started empty except for a 7-byte `README.md` (`# Jack3`). No property identity, lease document, tax basis, financial model, or application code existed.
2. **Parallel multi-session expansion (`PR #1`–`PR #28`):** Multiple concurrent sessions populated specialized directories alongside a shared root dashboard:
   - `/` (root 9 HTML pages + `assets/style.css` + `scripts/build.py` + `data/evidence.json`): Curated evidence-gated dashboard.
   - `/docs/`, `/analysis/`, `/brief/`, `/pages/`, `/decision-file/`, `/audit/`, `/advisory/` (`_advisory_src/`): Seven companion research/dashboard implementations retained in Git for audit history.
3. **Pages curation architecture (`PR #27` & `PR #28`, 2026-11-08):** GitHub Pages serves `/` from `main` using Jekyll with `_config.yml` excluding all companion folders (`docs`, `analysis`, `brief`, `pages`, `decision-file`, `audit`, `advisory`, `research`, `scripts`, `tools`, `model/`, `data/`). CI workflow `.github/workflows/validate.yml` enforces deterministic builds (`git diff --exit-code -- '*.html'`), provenance validation (`scripts/validate.py`), staged artifact parity against `jekyll build` (`scripts/stage_pages.py`), companion checks (`tools/check_site.py`, `tools/linkcheck.py`, `tools/check_links.py`, `_advisory_src/verify_advisory.py`), and privacy scanning (`tools/pii_scan.py`).

---

## 2. Line-by-Line Findings Across Inherited Layers (Resolved & Open)

| ID | Scope / Layer | Defect or Gap Identified | Resolution Applied in Root Integration |
|---|---|---|---|
| `F-17` | Root & `data/flags.py` | California 2027 minimum wage (`$17.40/hr`) was unverified because prior sessions failed to fetch the DIR FAQ URL (`faq_minimumwage.htm`). | **Resolved:** Directly verified CA DIR News Release `2026-66` (`https://www.dir.ca.gov/DIRNews/2026/2026-66.html`, certified 2026-07-31): `$17.40/hr` effective `2027-01-01` (`$72,384` exempt salary), while AB 1228 `$20.00/hr` remains binding on covered QSR chains. |
| `F-04` / `F-13` | `data/hazards.py`, `research/`, `_advisory_src/` | CA Dept. of Finance `P2A_County_Total.xlsx` was previously marked unreadable, and `_advisory_src` source `S36` (`demo30_table03.pdf`) served a 2019 USC/SCAG LAUSD enrollment deck rather than Connect SoCal tables. | **Resolved:** Parsed `P2A_County_Total.xlsx` directly (LA County FIPS `06037`: `9,811,358` in 2026 → `9,727,305` in 2030 → `9,708,647` in 2035 → `9,390,823` in 2050) and replaced `S36` with verified SCAG `appendix_i_updated_tables_508_final.pdf` + Jan 2026 Connect SoCal 2050 TWG packet. |
| `F-16` / `R-1`–`R-6` | Legacy `research/*.md`, `docs/`, `brief/`, `pages/`, `analysis/` | Historical companion layers cited August 2026 BLS payroll/CPI numbers against a November 4 BLS summary reporting September 2026 only, or listed unverified City/County/U.S. rates. | **Reconciled on Root & Root Docs:** Root `data/evidence.json`, `EXECUTIVE_SUMMARY.md`, and `VERIFY.md` use verified September 2026 BLS summary + `USDL-26-1618` Table 1 & Table 2 (including the `-121,599` MSA / `-94,312` County division labor-force drop). Excluded legacy folders remain unchanged in Git. |
| `IR-10` | `data/tenant.py`, old `EXECUTIVE_SUMMARY.md` | `$1,549k` FY2025 franchise AUV was misattributed to Jack in the Box; that figure was **Del Taco** (sold Dec 22, 2025). | **Resolved:** FY2025 Form 10-K Item 7 confirms Jack in the Box franchise AUV was **$1,874k** (FY2025) vs. **$1,949k** (FY2024), and Item 2 documents `1,585` corporate master-leased vs. `387` franchise-direct locations. |
| `M-01`–`M-09` & `e1bfd73b` | `model/projection.py`, `_advisory_src/model.py` | Prior projection models used unverified scenario probability weights (`20/50/20/10%`), guessed cap rates (`5.65%/6.25%/7.60%`), asymmetric `tenant_survival_adjust` penalties (`S3`), mixed `2030`/`2035` horizon logic (`R-05`), and stale `4.19%` Jan 2026 UST anchors. | **Replaced for Publication (`model/area_projection.py`):** Root `model.html` & `decisions.html` now publish purely official agency horizons, exact statutory City of LA Measure ULA dead-zone arithmetic (eff. `2026-07-01`), and unweighted algebraic `1.00 R` break-even identities anchored to Nov 6, 2026 `4.86%` 10-Yr UST—leaving private parcel outputs blank. |
| `IR-01`–`IR-09` | `brief/`, `analysis/`, `decision-file/`, `pages/` | Prior layers used expired `$5.3M/$10.6M` ULA thresholds (`brief/`), commercial broker/law-firm links (`analysis/`), broken LADBS `ladbs.org` redirects, or repo-handle footers (`IR-01`). | **Resolved on Root:** Updated to post-July 1, 2026 `$5.40M/$10.90M` ULA thresholds (`finance.lacity.gov` & `lavote.gov`), verified live `dbs.lacity.gov` Ord. 183893 retrofit URL, retained both LA County (`6,837/9,414`) and CAL FIRE (`6,845/9,419`) Jan 2025 fire counts, and kept 100% official/issuer links + zero PII/handles. |
| Open PRs `#4` & `#26` | Branch PRs (`28eacae6`, `3644edd8`) | Parallel unmerged PRs remain open on GitHub (`PR #4` stale branch build; `PR #26` standalone verification memo). | Left untouched in accordance with multi-session scope boundaries; substantiated model/evidence audit points (`M-01`–`M-09`) are addressed cleanly in the reconciled root outputs. |

---

## 3. Repository Architecture & Validation Summary

- **Curated Public Site (Pages Root):** `index.html`, `economy.html`, `tenant.html`, `risk.html`, `place.html`, `decisions.html`, `model.html`, `review.html`, `sources.html`, `assets/style.css` — built deterministically by `scripts/build.py` from `data/evidence.json` (`120` rows across `42` official/issuer sources, zero inline `<script>`, zero third-party CDNs, zero PII).
- **Deterministic Break-Even Engine:** `model/area_projection.py` verifies Measure ULA statutory math, CA DOF vs. SCAG horizon splits, and `1.00 R` algebraic extension/hold break-even identities via `--check`.
- **Unresolved Private Blockers:** Actual executed lease, tenant/guarantor entity, base rent `R`, store P&L, tax basis, debt terms, parcel APN/zoning, and insurance quotes remain intentionally absent and unresearched to preserve owner privacy.
