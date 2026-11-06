# Verification log — line-by-line check record

Compiled 2026-11-06 by `sess-8d650ba0`. Every value in `assets/data/dataset.json` traces to one row in this log.
Rule applied throughout: **a value is recorded only if it was read on the page that is linked. If it was not read, it is
not recorded — it goes to `flagged.json`.**

---

## S01 — BLS, Economy at a Glance, Los Angeles–Long Beach–Anaheim MSA
URL: https://www.bls.gov/eag/eag.ca_losangeles_msa.htm · page states "Data extracted on: November 05, 2026"

Read directly from the table (columns Apr–Sep 2026, not seasonally adjusted):

| Series | Sep 2026 value | 12-month change | Recorded as |
|---|---|---|---|
| Civilian labor force | 6,646.9 thousand | — | LAB-01 |
| Employment | 6,352.9 thousand | — | LAB-02 |
| Unemployment | 294.0 thousand | — | LAB-03 |
| Unemployment rate | 4.4% (p) | — | LAB-04 |
| Total nonfarm | 6,282.1 thousand | +0.5% | LAB-05, LAB-06 |
| Leisure and hospitality | 782.0 thousand | +1.5% | LAB-07, LAB-08 |
| Education and health services | 1,340.7 thousand | +3.8% | LAB-09, LAB-10 |
| Professional and business services | 975.5 thousand | −0.5% | LAB-11, LAB-12 |
| Information | 187.0 thousand | −5.7% | LAB-13, LAB-14 |
| Manufacturing | 444.8 thousand | −1.2% | LAB-15, LAB-16 |
| Construction | 251.5 thousand | 0.0% | LAB-17, LAB-18 |
| Government | 734.8 thousand | −1.1% | LAB-19 |
| Trade, transport and utilities | 1,047.9 thousand | +0.3% | LAB-20 |
| CPI-U, all items | 358.725 index | +3.7% | RATE-02, RATE-03 |

Internal consistency check: 294.0 ÷ 6,646.9 = 4.42%, which is consistent with the published 4.4% rate. No discrepancy.
Note: the page labels the MSA "Los Angeles-Long Beach-Santa Ana" in the title and "Los Angeles-Long Beach-Anaheim" in the
CPI block. Both refer to the same BLS area (31080). Recorded as "LA–Long Beach–Anaheim MSA".

---

## S02 / S03 — Census QuickFacts, Los Angeles County and Los Angeles city
URLs: `.../losangelescountycalifornia/PST045224`, `.../losangelescitycalifornia/PST045224`

Read from the County table: population 9,694,934 (July 1 2025, V2025); change −3.2% from the April 1 2020 base of
10,017,414; Census 2020 count 10,014,009; median household income $90,112 (2020–2024, 2024 dollars); per capita income
$45,792; poverty 13.3%; median gross rent $1,954; median home value $834,200; owner-occupied 45.9%; building permits 2025
= 22,250; bachelor's+ 36.0%; HS+ 80.9%; language other than English 55.1%; mean travel time 30.4 min; establishments
304,988 (2023); employment 3,987,736 (2023); annual payroll $299,616,607 thousand; employment change 2022→2023 +2.3%;
retail sales $213,932,785 thousand (2022); retail sales per capita $22,010; accommodation and food services sales
$44,000,801 thousand (2022).

Read from the City table: median household income $81,939; per capita income $47,685; poverty 16.5%; retail sales
$81,351,523 thousand; retail sales per capita $21,281; mean travel time 30.7 min; population density 8,304.2/sq mi;
land area 469.49 sq mi.

**Deliberately not recorded:** the City's own 2025 population estimate. It was not read on a page in this session, so no
value is asserted for it.

---

## S04 — FRED, 10-Year Treasury constant maturity (DGS10)
URL: https://fred.stlouisfed.org/series/DGS10 · series source: Federal Reserve Board, H.15 release.
Read: 2026-11-04 = 4.90%. Also displayed: 11-03 = 4.95, 11-02 = 4.91, 10-30 = 4.94, 10-29 = 4.98. Recorded RATE-01.

---

## S05 / S06 — Los Angeles County Assessor, 2026 Assessment Roll
URL: https://lacounty.gov/2026/07/14/la-county-property-values-surpass-2-2-trillion/
Read: total net taxable value $2.272 trillion; increase of $96 billion or 4.42%; 16th consecutive year of growth;
2,399,978 taxable real property parcels (plus 157,195 business property assessments, 31,938 boats, 3,566 aircraft);
more than $27 billion of property tax revenue; median single-family home sales price $982,000; Proposition 13 caps most
parcels' annual increase at 2%.

Cross-check: an independent report of the same release states the May 2026 forecast was 3.9% and the final figure 4.42%.
Consistent.

---

## S07 — USGS / CGS, The ShakeOut Scenario (OFR 2008-1150)
URL: https://pubs.usgs.gov/of/2008/1150/
Read: M7.8 on the southern San Andreas; about 1,800 deaths and $213 billion of economic losses; property damage $112.7bn;
business interruption $96.2bn; losses in 2008 dollars. Recorded HAZ-01 to HAZ-04.
Not recorded: any probability of occurrence. The scenario report does not state a single annual probability and none is
asserted on the site.

---

## S08 — CAL FIRE / Office of the State Fire Marshal, Fire Hazard Severity Zones
URL: https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones
Read: FHSZ classes are Moderate, High, Very High; the 2023 SRA mapping took effect April 2024; Local Responsibility Area
maps were released to jurisdictions in phases during 2025 and CAL FIRE states that "contact your local jurisdiction for
information on a specific area that is located in the Local Responsibility Area".
**Consequence:** no FHSZ class is assigned to [PROPERTY-A]. Recorded HAZ-13, HAZ-14 and flag F-04.

---

## S09 / S10 — California Department of Education and California School Dashboard
URLs: https://www.cde.ca.gov/ds/cm/dqeoy25.asp · https://www.caschooldashboard.org/reports/19647330000000/2025/academic-engagement
Read: statewide four-year adjusted cohort graduation rate 87.5% in 2024–25 (up from 86.4%); Los Angeles Unified 86.5% for
2024–25 (the Dashboard's 2024 report shows 86.7%). Both recorded (EDU-01, EDU-02) with their own year labels; the two
LAUSD figures are for different years and are not a conflict.
Not recorded: per-school and neighbourhood school-quality metrics — not read in this session, so not asserted.

---

## S11 / S12 / S13 — minimum wage, official
- DIR Fast Food Minimum Wage FAQ: $20.00/hour for covered fast-food employees from April 1, 2024. Recorded REG-01.
- DIR Minimum Wage FAQ: $16.90/hour from January 1, 2026. Recorded REG-02.
- City of Los Angeles Office of Wage Standards: $18.42/hour effective July 1, 2026 (announcement block on the page).
  Recorded REG-03.
Discrepancy note: one secondary source quoted the state rate as $16.50 for 2026 in its headline while its own table said
$16.90. The DIR page is authoritative and says $16.90; the secondary source was not used.

---

## S14 — LA County Registrar-Recorder/County Clerk, Documentary Transfer Tax
URL: https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info
Read: county rate $0.55 per $500 (= $1.10 per $1,000); an additional City rate applies in five cities including Los
Angeles, at $4.50 per $1,000. Combined 0.56% is arithmetic and is marked Calculated (TAX-03).

---

## S15 / S16 — IRS
- §1031 (FS-2008-18): 45-day identification and 180-day completion; the page carries an IRS notice that it is archival and
  points to the current "Like-Kind Exchanges — Real Estate Tax Tips" page. Recorded TAX-06, TAX-07, with the archival
  status disclosed in the source registry.
- Topic 409: unrecaptured §1250 gain taxed at a maximum 25%; long-term capital gain at a maximum 20%; NIIT referenced.
  Recorded TAX-08, TAX-09.

---

## S17 / S18 — California Secretary of State
- Qualified ballot measures for November 3, 2026: 15 propositions (1–5, 37–45). **No measure capping transfer taxes
  appears on the certified list.** Recorded REG-04, REG-05. This is a documented absence, not an inference about intent.
- Proposition 40 voter guide: one-time 5% tax on taxpayers with assets over $1 billion. Recorded REG-06.

---

## S19 / S20 — January 2025 wildfires
- LA County anniversary fact sheet: Eaton 14,021 acres, 9,414 structures destroyed, 1,074 damaged, 19 confirmed
  fatalities; Palisades 23,448 acres, 6,837 structures destroyed, 973 damaged, 12 fatalities; economic output lost
  $5.2–10.1bn; ~6,800 businesses and ~47,000 workers affected; labour income lost $2.2–4.2bn; local tax revenue lost
  $0.9–1.6bn. Recorded HAZ-05 to HAZ-12.
- CRS IF12871: 10 named fires, over 40,000 acres as of 16 January 2025, one-year moratorium on insurance non-renewals and
  cancellations in affected areas, heavy FAIR Plan reliance before the fires. Recorded HAZ-15.

**Disclosed discrepancy (flag F-10):** contemporaneous reporting in February 2025 gave 17 Eaton fatalities; the County's
anniversary fact sheet gives 19. Recovery-period revision is the likely explanation, but it was not verified, so both
figures are disclosed and the discrepancy is not "resolved".

---

## S21 / S22 — Jack in the Box Inc.
- FY2025 Form 10-K (fiscal year ended 2025-09-28): 2,136 Jack in the Box restaurants across 22 states and 576 Del Taco
  restaurants across 18 states; Del Taco stock purchase agreement dated 2025-10-15 at $115 million cash; company
  "founded and headquartered in San Diego, California". Recorded TEN-01, TEN-02, TEN-03, TEN-15.
- Q4 FY2025 earnings release (Exhibit 99.1): FY2025 31 openings and 86 closures; Q4 same-store sales −7.4%, FY −4.2%;
  Q4 systemwide sales −7.2%; Q4 revenue $326.2m (−6.6%); adjusted EBITDA $45.6m; 38 of 47 Q4 closures under "JACK on
  Track"; FY2026 guidance 2,050–2,100 restaurants and same-store sales −1% to +1%. Recorded TEN-04 to TEN-14.

**Not recorded:** a corporate-vs-franchisee split for FY2025. The FY2025 release shows 150 company / 1,986 franchise at
Q4 end, which implies ~93% franchised; that ratio was not stated as a number on the page read, so no row asserts it.

---

## S23 — LA28
URL: https://tickets.la28.org/ — Olympic Games 14–30 July 2028; Paralympic Games 15–27 August 2028. Used in narrative.

---

## S24 / S25 / S26 — The Boulder Group (industry, tier 3)
- Q3 2026 research report landing page: overall net-lease cap rate 6.92% (+10 bp, highest in over a decade); retail 6.69%;
  office 8.00%; industrial 7.28%; bid-ask spread 25 bp; supply 5,754 properties (−0.7%); corporate QSR 5.90%; franchisee
  QSR 6.87%; financing costs generally exceed cap rates; Fed target range 3.75%–4.00% after a September 2026 increase.
  Recorded MKT-01 to MKT-08 and RATE-04.
- Tenant profiles report: McDonald's 15-year ground leases 4.35%–4.65%, Chick-fil-A 4.15%–4.45%, 7-Eleven 4.80%–5.15%.
  Used only as context; no row.
**Label:** these are industry figures, tagged "Industry data" in the dataset and never presented as official statistics.

---

## S27 / S28 — Measure ULA
- City of Los Angeles Office of Finance: the deep link attempted (`finance.lacity.gov/measure-ula`) returned HTTP 404.
  Only the domain root was reachable. The rates (4% above $5.4m and below $10.9m; 5.5% at $10.9m and above, for closings
  after 30 June 2026) were corroborated by three independent secondary sources that each cite the Office of Finance, and
  by the County Recorder's published tiers. **They are recorded as FLAGGED, not verified** (F-01).
- Seyfarth (Oct 2026) reports ULA remains in force with reform efforts shifting to narrower fixes. Used only in flag F-02.

---

## Failed retrievals (recorded so the gap is auditable)
1. Census data API — now requires a registered key. No ZIP-level ACS tables could be pulled. Consequence: flag F-13.
2. BLS QCEW API — `/cew/data/api/2024/a/area/06037.csv` returned HTTP 500/404. Consequence: sector data taken from S01
   instead of a county-industry table.
3. City of LA Office of Finance ULA page — HTTP 404. Consequence: flag F-01.
4. IRS 1031 "small-businesses-self-employed" URL — HTTP 404; the `newsroom` FS-2008-18 page was used instead.
5. Boulder Group PDF reports — the landing page and its executive summaries were read; the PDFs themselves were not
   parsed. Every Boulder figure recorded comes from the landing page text, which is why they are tiered as industry data.

---

## Counts at build time

- Dataset rows: 113 — 101 verified against an official, statutory or filed source, 1 calculated (transfer-tax arithmetic),
  9 industry (Boulder Group market data, labelled), 2 flagged (the two Measure ULA rows awaiting an official City page).
- Flagged items: 13 (see `flagged.html`).
- Risks: 22 (13 business-as-usual, 9 black swan).
- Internal links: 234, all resolving. External links: 302 to 22 hosts.
