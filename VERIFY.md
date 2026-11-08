# Verification & Reproducibility Ledger (`VERIFY.md`)

**Verification Date:** 2026-11-08 (UTC) · **Curated Root Snapshot:** `data/evidence.json` (`42` sources · `120` rows · `9` root HTML pages)

---

## 1. Evidence Classification Rules

1. **`Verified`**: Direct, single-hop match to a fetched primary government, municipal, court/tax, or SEC/issuer document inspected on `2026-11-08` (UTC). No aggregator or broker cap-rate figures are promoted to `Verified`.
2. **`Analysis`**: Deterministic statutory math (Measure ULA brackets), algebraic `1.00 R` break-even identities (`model/area_projection.py`), or conditional strategic logic explicitly tagged as analyst interpretation rather than an official forecast.
3. **`Unverified` / `Needs review`**: Private parcel, lease, tax-basis, store P&L, or insurance facts absent from public records, or cross-agency / vintage divergences (`CA DOF P-2A` vs. `SCAG 2024 PEIR`, `LA County Anniversary Fact Sheet` vs. `CAL FIRE 2026` structure counts). Blank cells (`""`) are enforced in code whenever a parcel-specific figure cannot be verified.

---

## 2. Primary Sources Directly Checked (`2026-11-08`)

- **Demographics & Projections:** U.S. Census QuickFacts LA City (`V2025`, `2020–2024 ACS`, `2022 Economic Census`) and LA County; **CA Dept. of Finance `P2A_County_Total.xlsx`** (`Baseline 2024 / Mar 2026`, FIPS `06037` parsed directly: `2030: 9,727,305`, `2035: 9,708,647`, `2050: 9,390,823`); **SCAG Connect SoCal 2024 Final PEIR Appendix I**; **SCAG Jan 2026 Connect SoCal 2050 TWG Agenda Packet**.
- **Labor, Inflation & Capital Markets:** **BLS Los Angeles Area Economic Summary** (`2026-11-04`, September 2026 preliminary NSA); **BLS `USDL-26-1618` Table 1 & Table 2** (September 2026 MSA & County Division labor-force drop); **Federal Reserve FOMC Statement** (`2026-10-28`, `3.75%–4.00%` 10–2 vote); **U.S. Treasury Daily Par Yield Curve** (`2026-11-06`, 10-Yr `4.86%`, 30-Yr `5.26%`).
- **Tenant & SEC Filings:** **Jack in the Box Inc. FY2025 Form 10-K** (`0000807882-25-000072`, Items 2 & 7: `1,585` Co. master-leased / `387` franchise-direct, `$1,874k` JIB vs. `$1,549k` Del Taco AUV); **Q3 FY2026 Form 10-Q** (`0000807882-26-000091`, Note 5: `$1,492.0M` total debt, `$432.25M` 2029 ARD wall, `$500M` `7.624%` Series 2026-1, `$23.3M` sweep, `$11.0M` franchisee deferrals, `$18.9M` property-sale gains); official JIB investor releases (`Q3 FY26`, `$500M` refi, `JACK-on-Track`).
- **Wages, Property Taxes & Transfer Taxes:** **CA DIR AB 1228 FAQ** (`$20.00/hr`); **CA DIR News Release `2026-66`** (`$17.40/hr` eff. `2027-01-01`, `$72,384` exempt salary — resolving `F-17`); **LA Office of Wage Standards** (`$18.42/hr` eff. `2026-07-01`); **LA County Assessor 2026 Roll Portal & Memo** (`$2.272T` County / `$926.1B` City); **LA Office of Finance Measure ULA FAQ** & **LA County Recorder DTT** (`0.56% / 4.56% / 6.06%` eff. `2026-07-01`); **CA BOE Annotation `220.0345`** (`Prop 13` 35-year rule); **IRS §1031 Tips**, **IRS Topic 409**, and **CA FTB Capital Gains Guidance**.
- **Hazards, Schools & Catalysts:** **USGS UCERF3**, **CGS EQ Zapp**, **LADBS Mandatory Retrofit Programs (`dbs.lacity.gov` Ord. `183893`)**, **CAL FIRE OSFM FHSZ**, **LA County Anniversary Fact Sheet** & **CAL FIRE Palisades / Eaton Incident Pages**, **CRS `IF12871`**, **CA Dept. of Insurance `release052-2025`** (`2028` commercial FAIR Plan sunset), **FEMA MSC**, **CDE District Enrollment (`497,105`)** & **CA School Dashboard (`86.5%` grad / `21.9%` chronic abs.)**, **LA Metro D Line Westside (`Section 1` opened `2026-05-08`)**, **LA City Planning CHIP Year-1 Report (`242` projects / `28,526` homes)**, **DTLA 2040**, **ZIMAS**, and **Caltrans Traffic Census**.

---

## 3. Automated Integrity & Privacy Checks

Run from `/home/user/Jack3`:
```bash
python3 model/area_projection.py --check
python3 scripts/build.py
python3 scripts/validate.py
python3 scripts/stage_pages.py
python3 tools/check_site.py
python3 tools/linkcheck.py
python3 tools/check_links.py
python3 tools/pii_scan.py
python3 _advisory_src/verify_advisory.py
git diff --exit-code -- '*.html'
```

All checks enforce:
- Every `<tbody>` row across all 9 root Pages HTML files carries a registered `https://` official/issuer link from `data/evidence.json`.
- Zero blank-cell rows marked `Verified`; zero `<script>`, `<iframe>`, `localhost`, or tracking embeds.
- Zero email addresses, phone numbers, street addresses, APNs, SSNs, or prohibited officer/owner identifiers (`tools/pii_scan.py`).
- Exact Jekyll staging curation (`_config.yml` + `scripts/stage_pages.py`) excluding unverified legacy/companion directories from GitHub Pages.
