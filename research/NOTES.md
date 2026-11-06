# Verification log

Line-by-line record of what was checked, where, and what it turned up. Every entry corresponds to a
source record in `data/sources.json`. This file exists so the retrieval work is auditable without
re-running it.

Access note: direct `curl`/HTTP egress from the build sandbox to `api.bls.gov`, `census.gov`,
`fred.stlouisfed.org` and `home.treasury.gov` is blocked (`SSL_ERROR_SYSCALL` / no route). All
retrieval was performed through the agent's web retrieval layer. Machine-readable endpoints are
recorded below so any reader can re-run them from an unblocked network.

---

## 1. Macro & rates

**S01 — Federal Reserve FOMC statement, 28 October 2026**
`https://www.federalreserve.gov/newsevents/pressreleases/monetary20261028a.htm`
Read in full. Target range held at 3.75–4.00% on a **10–2 vote**; dissents from Cook and Hammack
preferred a 25bp *increase*. Text states activity "is expanding at a strong pace" and inflation
"remains elevated". Note for the record: the search layer also surfaced a **29 July 2026** statement
at 3.50–3.75% and a September 2026 hike; the October statement is the current one and is the only
FOMC text cited. **Irregularity avoided:** early search results described a 3.50–3.75% range; that
figure is superseded. Only the retrieved primary text is used.

**S02 — Treasury Daily Par Yield Curve, November 2026**
`https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202611`
Table read directly. 11/05/2026: 1M 4.03, 1Y 4.28, 2Y 4.46, 3Y 4.53, 5Y 4.59, 7Y 4.70, 10Y 4.84,
20Y 5.27, 30Y 5.25. The curve is **inverted at the front and positively sloped at the long end** —
10Y is 97bp above the fed funds midpoint of 3.875%. That positive term premium is what makes the
cap-rate risk real and is the reason assumption A02 is a spread over the 10Y rather than over a
policy expectation.

**S03 — BLS CPI-U, U.S. city average** (series `CUUR0000SA0`, Public API v1, no key required)
`https://api.bls.gov/publicAPI/v1/timeseries/data/CUUR0000SA0`
336.940 (Sep 2026) against 324.800 (Sep 2025) = **+3.74% y/y**. Annual 2025 321.943 vs 2024 313.689
= +2.63%. **Irregularity I-01 found here:** October 2025 returns `"-"` with footnote code `X`,
"Data unavailable due to the 2025 lapse in appropriations". No interpolation performed; the model
uses September-anchored y/y comparisons throughout.

**S04 — BLS CPI-U, Los Angeles-Long Beach-Anaheim** (series `CUURS49ASA0`)
358.725 (Sep 2026) vs 345.865 (Sep 2025) = **+3.72% y/y**. Annual 2025 +3.16%.
**Finding:** local inflation is within 2bp of national. The landlord's operating-cost exposure is
therefore not a local-inflation story — it is a contract-escalation story.

## 2. Labour market

**S05 — EDD, Los Angeles-Long Beach-Glendale MD, released 16 October 2026**
`https://labormarketinfo.edd.ca.gov/file/lfmonth/la$pds.pdf`
Read across three chunks. Key verified facts: SA unemployment **4.8%** (Sep 2026), 5.0% (Aug rev),
5.6% (Sep 2025); unadjusted 4.5%. CA 5.1%, U.S. 4.2%. Nonfarm employment 4,539,800 SA / 4,593,800 NSA.
Year over year **+20,300 (+0.4%)**.
Sector detail, y/y: education & health **+37,500**; leisure & hospitality +8,900; restaurants and
other eating places **+7,300**; information **−10,200** (motion picture & sound recording −7,300,
declines in 20 of the last 22 months); government −7,800; manufacturing −4,100; financial
activities −4,000; professional & business services −3,500.
**Finding that shaped the recommendation:** the restaurant sub-sector is *adding* jobs (+7,300) in
the same year the tenant closed 86 units. That is a share-shift story, not a demand collapse, and it
is why the tenant's own problem is treated as company-specific rather than market-wide.

Note: a BLS series attempt `LAUCT06037000000000003` and `LSUR060370000000003` both returned
"series does not exist". EDD is used instead as the official LA-specific source.

## 3. Demographics

**S06 / S07 — Census QuickFacts, LA County and City of LA**, vintage 2025 population and ACS 2020–2024.
County population **9,694,934** at 1 Jul 2025 against a **10,014,009** 2020 Census base = **−3.2%**.
City **3,869,089**, −0.8%. Median household income $90,112 county / $81,939 city. Poverty 13.3% /
16.5%. Density 2,466.9 /sq mi county vs **8,304.2** city.
**Finding:** the city is declining materially more slowly than the county and is 3.4× denser. For a
drive-through that is the favourable half of a deteriorating region.

**S08 — CA Department of Finance population projections, Baseline 2024, Vintage 2026 (13 Mar 2026)**
`https://dof.ca.gov/forecasting/demographics/projections/`
Product page verified: P-1/P-2/P-3/P-4/P-CC all published. **The P-2A workbook was not parsed**, so
county 2030 and 2035 single-year values are **blank** and carried as flag **F-02**. Two secondary
sources conflict (9,727,305 vs 9,867,515) and neither was accepted.

**S09 — DOF Public K-12 Graded Enrollment Projections, 2026 Series (August 2026)**
`https://dof.ca.gov/forecasting/demographics/public-k-12-graded-enrollment/`
State enrollment 5,731,300 in 2025-26, the **ninth consecutive annual decline** (−75,000 in the
year); projected 5,020,800 by 2035-36 (−710,500). **Los Angeles County is the largest projected
county decline in the state: −240,800 students.** This is the single hardest official number in the
file and it is why assumption A17 applies a negative structural drag to market rent.

**S10 — City of Los Angeles EWDD economic forecast (quoting DOF)**
Secondary: gives direction and the 2040 (9.3M) and 2060 (8.3M) endpoints, not single-year values.
Tiered `official-secondary` and labelled as such.

## 4. Tenant credit

**S11 — Jack in the Box Inc. Form 10-K, FY ended 28 Sept 2025**, accession 0000807882-25-000072,
filed 19 Nov 2025. Index page read; the 10-K body is 2.6 MB and was not fully parsed. Confirmed from
the summary and search extracts: 2,136 JITB units at year end (3 in Mexico, 2 in Guam), 576 Del Taco
units, occupancy cost at **18.7%** of company restaurant sales up from 17.3% "due to sales
deleverage, higher costs for rent, utilities", menu pricing of approximately **5.5%** in FY2025.

**S12 — 8-K Item 2.02 Ex-99.1, Q4 and FY2025 earnings, filed 19 Nov 2025**
`https://www.sec.gov/Archives/edgar/data/807882/000080788225000070/ex991-q425earningsrelease.htm`
FY2025 same-store sales **−4.2%** (company −3.7%, franchise −4.3%); Q4 **−7.4%**. 31 openings and
**86 closures** in FY2025; 38 of the 47 Q4 closures were the "JACK on Track" block closure program.
Q4 revenue $326.2M (−6.6%), net earnings $5.8M, EPS $0.30, Adjusted EBITDA $45.6M vs $65.5M.
FY2026 guidance: 2,050–2,100 units (≈20 openings, **≈50–100 closures**), SSS −1% to +1%, Adj. EBITDA
$225–240M. Dividend discontinued. Explicit statement that JACK on Track "includes a block closure
program and **selling real estate**".

**S13 — 8-K Item 2.02 Ex-99.1, Q3 FY2026, filed 12 Aug 2026**
Same-store sales **−1.1%** (franchise −1.2%, company −0.9%) — a 6.0pp improvement on −7.1% a year
earlier. Units 2,115 (149 company, 1,966 franchise). Revenue $257.7M (−1.8%). Net earnings from
continuing operations $21.0M. Adjusted EBITDA $61.2M vs $57.1M. Franchise-Level Margin **37.4%**
from 39.3%, with "**Bad debt expense was also higher** versus the prior year quarter". Real-estate
gains cited as the driver of other operating income. Del Taco sold, completed **22 Dec 2025**, now in
discontinued operations. Effective tax rate 36.9% vs 20.9%. Interim CEO Mark King.

**S14 — 8-K Item 1.01/2.03 Ex-99.1, securitized refinancing, filed 23 June 2026**
$500M Series 2026-1 Class A-2 at **7.624%** fixed, retiring Series 2019-1 at 4.476% and part of
Series 2022-1 at 3.445%. "**Next anticipated repayment date in 2029**". Plus $150M Class A-1 VFN.
**Finding:** the tenant's cost of debt has risen by more than 300bp, and its next
anticipated repayment date precedes the 2030–2035 lease expiry window.

**S30 — EDGAR filing index**
Ten consecutive 10-K filings FY2016–FY2025 and eight 8-Ks between 13 Apr and 21 Sept 2026. No
reporting delinquency.

## 5. Tax & regulatory

**S15 — BOE Publication 29**, `https://www.boe.ca.gov/proptaxes/pdf/pub29.pdf`
Prop 13: 1% ad valorem plus locally approved bonded indebtedness; reassessment only on change in
ownership or new construction; annual base-year increase capped at 2% or CA CPI if lower; Prop 8
decline-in-value permits a temporary reduction; assessed value is the lower of market or factored
base year.

**S16 — RTC §11911**, `https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=11911`
Verified verbatim: $0.55 per $500 or fractional part above $100; a city may impose one-half that
amount; a credit against the county tax is allowed for the city tax.
**Irregularity I-02:** the City of Los Angeles imposes **$2.25 per $500 (0.45%)**, roughly eight
times the §11911(b) ceiling. Consistent with charter-city authority, but the statute alone does not
explain it. Both the statute and the City's own FAQ are cited.

**S17 — City of Los Angeles Office of Finance, Real Property Transfer Tax and Measure ULA FAQ**
`https://finance.lacity.gov/faq/measure-ula`
Base tax 0.45% at $2.25/$500. ULA adds **4%** over $5,400,000 and **5.5%** at $10,900,000 or more,
effective for closings after 30 June 2026, thresholds indexed to BLS Chained CPI. The City's own
table gives 0.45% / 4.45% / **5.95%**. Exemptions limited to qualifying 501(c)(3), government
entities and constitutionally exempt transferees.
**Note on a computed difference:** the model reports 4.56% and 6.06% effective for specific
prices, against the City's stated 4.45% and 5.95%. The difference is the $2.25-per-$500 rounding
over a finite consideration and is disclosed in the row notes rather than smoothed away.
*URL note:* `https://finance.lacity.gov/tax/real-property-transfer-tax` returned a 404; the `/faq/measure-ula`
path is the live one.

**S18 — IRS, like-kind exchanges**, `https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips`
§1031 applies only to real property since 2018; gain recognised only to the extent of boot; losses
not recognisable; U.S. real property is not like-kind to foreign real property.

**S19 — DIR minimum wage FAQ** — $16.90/hour from 1 Jan 2026, CPI-W indexed, capped at 3.5%/yr, no
tip credit.
**S20 — DIR fast food minimum wage FAQ (AB 1228)** — $20.00/hour from 1 Apr 2024; covers
limited-service chains of 60+ U.S. establishments **including franchisees**; a Fast Food Council can
raise it; a city may not set a fast-food-specific higher rate but a higher general local minimum
does apply.

## 6. Hazard

**S21 — CAL FIRE, Palisades Fire**
23,448 acres; 6,845 structures destroyed; 975 damaged; 12 civilian fatalities; cause **arson**; LAFD
jurisdiction; 100% of structures in footprint inspected.
**S22 — CAL FIRE, Eaton Fire update 27 Jan 2025**
14,021 acres; 9,418 destroyed; 1,073 damaged; **17** civilian fatalities.
**Combined: 16,263 structures destroyed in one week.**
**Irregularity I-03:** later secondary reporting gives 19 Eaton fatalities. The official update read
for this study says 17. The verified figure is used and the discrepancy is published.

**S23 — FEMA National Risk Index v1.20**
Product page verified: 18 hazards; EAL, social vulnerability and community resilience at tract or
county level; v1.20 added pluvial flooding, USGS landslide data and USGS probabilistic seismic data;
the standalone NRI application has been retired in favour of RAPT.
**Retrieval failures (F-03):** `hazards.fema.gov/nri/api/county/06037` and
`fema.gov/api/open/v2/NriCountyDetails?...` both returned 404; an OpenFEMA
`DisasterDeclarationsSummaries` filter on `designatedArea eq 'Los Angeles County'` returned an empty
set, which is a query artefact rather than evidence of zero declarations. The widely quoted composite
of 100.0 is therefore **not used**.

**F-04 — USGS seismic probabilities.** A usgs.gov page carrying the UCERF3 figures returned 404. The
widely quoted 60% (LA region, M6.7+, 2014–2043) is **not used**.

## 7. Property market

**S24 / S25 — LA County Assessor 2026 roll**
Official page verified: 2026 Roll memorandum dated 13 July 2026, 2026 Roll Forecast dated 15 May
2026, historical forecasts 2012–2025. The PDF was not parsed, so roll totals are quoted from
reputable reproductions of the Assessor's own statement and tiered `official-secondary`:
net taxable value **$2.272 trillion**, gross **$2.367 trillion**, **+4.42%** / +$96bn, 16th
consecutive year of growth; Prop 13 inflation adjustment **+$43bn** (the 2% cap was binding because
CA CPI exceeded it); transfers +$49bn; new construction +$12bn; personal property +$11bn;
**wildfire relief −$9bn**; median home price $982,000; 2,399,978 taxable parcels; City of LA
$926.1bn.
**Irregularity I-04:** the distributed text says both "4.42%" and "42%". The 4.42% and $96bn are
mutually consistent with $2.272tn; "42%" is a typographical error.

**F-05 — cap rates.** No official government series publishes net-lease cap rates. NCREIF and CoStar
are subscription products and are excluded by the source rules. The cap rate is therefore declared
as assumption A01 (5.75%, range 5.00–6.50%) built from the verified 10Y Treasury plus a stated
spread — never presented as an observation.

---

## Things deliberately not done

- No address, parcel number or owner identity was sought, recorded or inferred.
- No figure was interpolated, back-filled or estimated into a "verified" slot.
- No third-party cap-rate or index figure was used, even where it would have been convenient.
- The two conflicting population projections were **left blank** rather than split or averaged.
