# Official-source re-check — session 3c0dd247 (2026-11-15)

Internal record. Not published on GitHub Pages (`research/` is excluded by `_config.yml`).
Asset A and Owner A are placeholders. No personal names, contact details, addresses or parcel
identifiers are recorded here; officer names and contact lines visible on official pages were
deliberately not copied.

## Scope

This pass re-read the official page behind each value below on 2026-11-15 (UTC) and compared it
with the published register row. It is **not** a full re-read of all 242 rows. The last full
line-by-line pass remains the 2026-11-12 audit. Rows not listed here were not re-read today.

## Results

| # | Published row(s) in `data/canonical_rows.py` | Official page re-read | Published value | Official value on that page | Result |
|---|---|---|---|---|---|
| 1 | Hazards · UCERF3 30-yr M≥6.7 (LA region) · M≥6.0 · M≥7.0 · M≥7.5 · M≥8.0 · average repeat 40 yr; Southern California M≥6.7 | [USGS Fact Sheet 2015-3009 (UCERF3), Table 1](https://pubs.usgs.gov/fs/2015/3009/pdf/fs2015-3009.pdf) | 60% · 96% · 46% · 31% · 7% · 40 yr · 93% | LA region: 60% (M6.7), 96% (M6), 46% (M7), 31% (M7.5), 7% (M8), repeat 40 yr; Southern California: 93% (M6.7) | Match |
| 2 | Taxes · Measure ULA thresholds and rates; effective date; base tax on net value, ULA on gross value | [City of LA Office of Finance · Measure ULA FAQ](https://finance.lacity.gov/faq/measure-ula) | $5,400,000 / $10,900,000 (closings after 2026-06-30); 4% / 5.5%; on or after 2023-04-01; base tax net, ULA gross | Same | Match |
| 3 | Hazards · Palisades Fire structures destroyed 6,845; civilian fatalities 12; area 23,448 acres; duration 24 days | [CAL FIRE · Palisades Fire incident page](https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire) | 6,845 · 12 · 23,448 · active 24 days | 6,845 destroyed; 12 confirmed civilian fatalities; 23,448 acres; active 24 days. Page says "Not a CAL FIRE Incident" (see F-34) | Match; scope note added (F-34) |
| 4 | Hazards · Eaton Fire structures destroyed 9,419; combined 16,264 (derived) | [CAL FIRE · Eaton Fire incident page](https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire) | 9,419; 6,845 + 9,419 = 16,264 | 9,419 destroyed | Match; sum arithmetic checked |
| 5 | Hazards · ShakeOut scenario M7.8; about 1,800 deaths; about $213 billion | [USGS OFR 2008-1150, The ShakeOut Scenario](https://pubs.usgs.gov/of/2008/1150/) | M7.8 southern San Andreas; about 1800 deaths; $213 billion | Same, dated 2008 | Match; present-tense landing wording corrected (F-33) |
| 6 | Hazards · FEMA National Risk Index, Los Angeles County (archived v1.19.0) · rank 1; EAL $3.9B; CRF 1.36; risk value $5.3B | [FEMA NRI overview presentation, March 2023 (PrepToolkit)](https://www.preptoolkit.fema.gov/documents/d/caes/1d_national-risk-index-_sheehan?download) · live portal [hazards.fema.gov/nri](https://hazards.fema.gov/nri/) | rank 1; $3.9B; 1.36; $5.3B | Slide "Updated Top 20 Highest Risk Counties": Los Angeles, CA #1, EAL $3.9B, CRF 1.36, Risk Value $5.3B | Match to the archived deck. Live portal returned HTTP 500 twice today (already F-18 / R-36) |
| 7 | Tenant · Q3 FY2026 closures 17; system same-store sales −1.1%; restaurant counts 149 company / 1,966 franchise / 2,115 total | [SEC · Jack in the Box Form 8-K Ex. 99.1, Q3 FY2026 release](https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm) | 17 · −1.1% · 149 / 1,966 / 2,115 | Page 2: 4 openings, 17 closures; system SSS (1.1%); counts 149 / 1,966 / 2,115 | Match |
| 8 | Tenant · franchise rental revenues 40 weeks $242.526m vs $260.254m (−6.8%) | Same 8-K, consolidated statement of earnings | 242,526 vs 260,254 (thousands) | 242,526 vs 260,254 (40 weeks); Q3 73,017 vs 76,538 | Match; −6.8% recomputed |
| 9 | Tenant · FY2026 guidance: about 2,100 restaurants; about 25 openings; 50–60 closures; Adjusted EBITDA $225–230m; SG&A $112–115m | Same 8-K, "Guidance Updates" | Same | ~2,100; ~25 openings; ~50 to 60 closures (mostly franchise); Adjusted EBITDA $225–230m; SG&A $112–115m | Match |
| 10 | Economy · covered fast-food minimum wage $20.00/hour from 2024-04-01 | [California DIR · Fast Food Minimum Wage FAQ](https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm) | $20.00 from 2024-04-01 | "Starting April 1, 2024 … at least $20.00 per hour" | Match |
| 11 | People · Los Angeles city population 3,869,089; estimates base 3,899,342; change −0.8%; median household income $81,939; poverty 16.5%; density 8,304.2 per sq mi; land area 469.49 sq mi | [Census QuickFacts · Los Angeles city](https://www.census.gov/quickfacts/losangelescitycalifornia) | As listed | 3,869,089; 3,899,342; −0.8%; $81,939 (2024 dollars, 2020–2024); 16.5%; 8,304.2; 469.49 | Match. Per-capita income $47,685 is on the page and not in the register |
| 12 | Economy · LA metro unemployment 4.4% (Sep-26, from 5.5%); LA County 4.5%; LA city 4.5%; nonfarm 6,282.1k (+0.5%); education & health 1,340.7k (+3.8%); CPI-U +3.7%; ECI +3.9% (LA-Long Beach CSA); average weekly wage LA County Q1-26 $1,704; average hourly wage LA metro (May-25) $37.15 | [BLS · Los Angeles Area Economic Summary, updated 2026-11-04](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | As listed | Same values; ECI table labelled "Los Angeles-Long Beach, CA CSA" | Match (ECI scope note added, F-35) |
| 13 | Economy · 10-year Treasury (DGS10): 5.10% on 2026-11-12; no observation 2026-11-11; 4.98% on 2026-11-10; 4.88% on 2026-11-09 | [FRED · DGS10 (Federal Reserve H.15)](https://fred.stlouisfed.org/series/DGS10) | As listed | 2026-11-12: 5.10; 2026-11-11: "."; 2026-11-10: 4.98; 2026-11-09: 4.88; page updated Nov 13, 2026; no later observation on the page read 2026-11-15 | Match; rate anchor remains current (F-32) |

Totals: 13 official pages re-read; about 55 individual values compared; 0 mismatches.

## Irregularities and changes made

- **F-33 (Low, closed).** The overview and risk-summary text described the 2008 ShakeOut scenario in the present tense. Wording corrected in `scripts/build_canonical.py` to "A 2008 USGS ShakeOut scenario modelled …". No figure changed.
- **F-34 (Low, open).** The Palisades Fire CAL FIRE page says "Not a CAL FIRE Incident" and lists the Los Angeles City Fire Department as agency having jurisdiction. The figures are official and are kept, with a scope note.
- **F-35 (Low, open).** The +3.9% Employment Cost Index is an LA-Long Beach CSA figure. The overview, risk and decision text repeat it without that scope. Scope note added; no value changed.
- **F-18 / R-36 (already open).** The live FEMA NRI portal returned HTTP 500 again on 2026-11-15. The archived 2023 deck still supports the published values.

## Open items carried forward (not blocking)

- Only 13 pages were re-read today. Full row re-verification of the register (255 rows after merging `main` at 1920c85) is due on the next scheduled audit.
- Pull requests from earlier sessions remain open for owner decision: #4, #12, #22, #26, #31, #32, #36, #40, #44, #48, #51 and #87. This session did not close or edit them.
- `COORDINATION.md` has grown past 2,100 lines across more than 30 sessions. Archiving older sections would make it easier to read; this is a repository-maintenance suggestion for owner review.
