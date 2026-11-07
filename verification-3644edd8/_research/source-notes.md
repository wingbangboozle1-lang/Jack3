# Official-source inspection notes

Review date: **2026-11-07 (UTC)**. Asset remains **Asset A**, anonymized. These notes record only decision-relevant public aggregates and issuer disclosures. No address search, parcel search, owner search, tenant-entity search, rent roll, lease, personal name, or private financial record was collected.

This is a targeted source-and-model audit, not a certification of every inherited repository row.

## 1. Population, income, schools and official projections

### Census QuickFacts — county
Official URL: https://www.census.gov/quickfacts/losangelescountycalifornia

Directly read:
- Population estimates, July 1, 2025 (V2025): **9,694,934**.
- Population estimates base, April 1, 2020 (V2025): **10,017,414**.
- Percent change, estimates base to July 1, 2025: **−3.2%**.
- Median household income, 2020–2024, in 2024 dollars: **$90,112**.
- Per-capita income, 2020–2024, in 2024 dollars: **$45,792**.

Boundary: county values are not an unidentified central-LA trade area. The estimates base and the decennial Census count are different series and must not be interchanged.

### Census QuickFacts — city
Official URL: https://www.census.gov/quickfacts/losangelescitycalifornia

Directly read:
- Population estimates, July 1, 2025 (V2025): **3,869,089**.
- Population estimates base, April 1, 2020 (V2025): **3,899,342**.
- Percent change, estimates base to July 1, 2025: **−0.8%**.
- Median household income, 2020–2024, in 2024 dollars: **$81,939**.
- Per-capita income, 2020–2024, in 2024 dollars: **$47,685**.

Boundary: the site is only reported as “Central Los Angeles.” Municipal jurisdiction is unconfirmed; do not silently apply city figures to the asset.

### California Department of Finance P-2A
Official workbook: https://dof.ca.gov/media/docs/forecasting/Demographics/projections/P2A_County_Total.xlsx
Series notes: https://dof.ca.gov/forecasting/demographics/projections/

Workbook citation text identifies **Report P-2A: Total Population Projections, California Counties, 2020–2070 (Baseline 2024 Population Projections; Vintage 2026 Release), March 2026**. Release notes say the 2026-03-13 vintage updated published July 1 estimates without changing Baseline 2024 assumptions.

Direct Los Angeles (FIPS 6037; all ages, all sexes, all races) values:
- 2030: **9,727,305**.
- 2035: **9,708,647**.
- 2040: **9,637,524**.

Result: the inherited F-04 “XLSX unreachable / leave blank” limitation is no longer true in this review environment. The values can be published with vintage and projection status. They are not observations and do not establish store demand.

### Schools
Official CDE page: https://www.cde.ca.gov/ta/ac/cm/
Official Dashboard: https://www.caschooldashboard.org/

The CDE page fetched successfully in this audit and describes a multiple-measures accountability system for local educational agencies and schools. No subject campus or attendance area can be selected without an address. School/catchment values therefore remain blank. Adult educational attainment is not school performance.

## 2. Employment, inflation and wages

### BLS Los Angeles Area Economic Summary
Official URL: https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf

The live PDF states **“Updated November 04, 2026”** and warns that data are not seasonally adjusted, may be revised, and area definitions can differ.

Direct September 2026 readings:
- Unemployment: U.S. **4.0%**, California **5.1%**, LA metro **4.4%**, LA County **4.5%**, LA city **4.5%**. Prior-year September: **4.3%, 5.6%, 5.5%, 5.9%, 5.9%**, respectively.
- Metro total nonfarm: **6,282.1 thousand**, change **+30.2 thousand / +0.5%** year over year.
- Leisure and hospitality: **782.0 thousand**, change **+11.5 thousand / +1.5%**.
- CPI-U all items: **+3.7% LA / +3.7% U.S.** year over year.
- CPI-U food: **+2.8% LA / +2.5% U.S.**.
- CPI-U energy: **+20.3% LA / +20.4% U.S.**.
- ECI wages and salaries: **+3.9% LA–Long Beach CSA / +3.1% U.S.**.

Irregularity: inherited companion snapshots use August 6,289.1 thousand / +0.6%, CPI +3.6% / +3.4%, energy +17.6% / +16.3%, and June ECI +2.8%. Those may describe earlier snapshots but are not the current linked November 4 summary. Current-use rows must be updated or dated explicitly.

### BLS metropolitan labor-force table
Official URL: https://www.bls.gov/news.release/pdf/metro.pdf
Release: **USDL-26-1618**, released 2026-10-28, September 2026.

Los Angeles–Long Beach–Anaheim row:
- September 2025 civilian labor force **6,768,502**; September 2026 preliminary **6,646,903**.
- September 2025 unemployed **372,871**; September 2026 preliminary **294,000**.
- Unemployment rate **5.5% → 4.4%**.

Arithmetic implication: both labor force and unemployment counts fell. The table does **not** establish migration, why labor-force participation changed, or a causal claim that the rate improvement was “caused by people leaving the labor force.” Avoid that unsupported causal language.

### Wage rules
Official URLs:
- https://www.dir.ca.gov/dlse/faq_minimumwage.htm
- https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm
- https://wagesla.lacity.gov/

Direct readings:
- California general minimum wage **$16.90/hour effective 2026-01-01**, unless a higher industry/local standard applies.
- City of Los Angeles general minimum wage **$18.42/hour effective 2026-07-01**.
- AB 1228 covered fast-food employees: **$20.00/hour starting 2024-04-01**.

The fast-food FAQ says all coverage criteria must be met, exemptions exist, and franchisee employers can be covered. It also allows a higher general local wage to prevail. Do not call one rate “binding” for Asset A without city jurisdiction, employee coverage, exemptions, and a current industry-rate check. The September 2024 fast-food FAQ alone is not evidence of a later adjustment or site-specific applicability.

## 3. Tenant and real-estate contract distinctions

### FY2025 Form 10-K
Official SEC URL: https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm

Item 1 / Item 2:
- Jack in the Box at 2025-09-28: **2,136**, of which **1,986 (93%) franchised**; company-operated count in the Item 2 table is **150**.
- Del Taco at that date: **576**, of which **444 franchised**; this is a separate brand.
- Franchise agreement generally: initial fee **$50,000**, **20-year term**, royalty and marketing generally **5.0% of gross sales**, with legacy/variable exceptions.
- Item 2 reports approximately **13%** of Jack in the Box leases with contingent rent of **1%–10%** of gross sales above thresholds.
- Item 2 states: **“We have generally been able to renew our restaurant leases as they expire at then-current market rates.”** This is relevant counterevidence to a closure-only narrative, not a subject-site promise.

Item 7 has two separate franchise tables:
- **Jack in the Box:** franchised restaurant AUV **$1,874 thousand FY2025 / $1,949 thousand FY2024**; royalties **5.1% / 5.0%** of franchised restaurant sales.
- **Del Taco:** franchised restaurant AUV **$1,549 thousand / $1,573 thousand**; royalties **4.6% / 4.7%**.

Irregularity: inherited `data/tenant.py` labels the Del Taco values as generic cost-pressure metrics in a Jack in the Box asset analysis. This is a source-row brand mismatch, not a rounding difference.

### Q3 FY2026 Form 10-Q and issuer release
Official URLs:
- https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/jack-20260705.htm
- https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx

Direct readings:
- At 2026-07-05: **149 company-operated + 1,966 franchise-operated = 2,115** Jack in the Box restaurants.
- Q3 openings **4**, closures **17**.
- System same-store sales **−1.1%**, prior-year quarter **−7.1%**.
- Franchise-level margin **$60.3 million / 37.4%**, versus **$66.2 million / 39.3%**; non-GAAP.
- Del Taco sale completed **2025-12-22** and its results are discontinued operations.

Boundary: these are issuer-system observations, not the subject store’s sales, closure list membership, guaranty, or rent-paying entity.

### JACK on Track closure announcement
Official issuer URL: https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Unveils-JACK-on-Track-Plan-to-Improve-Long-Term-Financial-Performance/default.aspx

Direct wording:
- Approximately **150–200 underperforming restaurants**, a majority in the system over three decades.
- Approximately **80–120** closures planned through 2025-12-31.
- Remaining restaurants close thereafter **“based upon respective franchise agreement termination dates.”**

Decision-critical distinction: a franchise agreement and a real-estate lease are separate legal instruments. The announcement does not say that an independent landlord’s 2030–2035 real-estate expiry is the franchise termination date, nor that Asset A is in the programme. Any sentence equating the two must be removed or qualified.

## 4. Catastrophe sources and limits

### Earthquake
Official USGS URL: https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area

UCERF3 regional 30-year values: **60% M6.7+**, **46% M7.0+**, **31% M7.5+** in the Los Angeles region. Direct page fetch failed on a later retry, but the official USGS result and its extracted text were available through search in this review; an earlier direct fetch in the same session also confirmed the values.

These are regional earthquake occurrence probabilities, not Asset A damage, business-interruption, or uninsured-loss probabilities. No annual or hold-period conversion is officially established.

Official CGS EQ Zapp: https://www.conservation.ca.gov/cgs/geohazards/eq-zapp

CGS distinguishes fault rupture, liquefaction and earthquake-induced landslides, warns that maps may omit hazards, and says the application is not a substitute for site investigation. No parcel determination was attempted.

### Wildfire
Official sources:
- County fact sheet: https://file.lacounty.gov/SDSInter/lac/1199046_Eaton_Palisades_Fires_Anniversary_Fact_Sheet.pdf
- CAL FIRE Palisades incident: https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire
- CAL FIRE hazard-zone method: https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones

County fact sheet:
- Eaton: **14,021 acres; 9,414 structures destroyed; 1,074 damaged**.
- Palisades: **23,448 acres; 6,837 structures destroyed; 973 damaged**.

CAL FIRE incident page, last updated 2026-04-09:
- Palisades: **23,448 acres; 6,845 structures destroyed; 975 damaged**.

Irregularity: official snapshots differ by **8 destroyed** and **2 damaged** structures. Preserve both with source and vintage rather than choosing silently.

CAL FIRE explicitly distinguishes **hazard** from mitigated **risk**. No Asset A zone or loss likelihood can be inferred from county incidents.

### Flood
Official FEMA Map Service Center: https://msc.fema.gov/portal/home

FEMA describes this as the official source for NFIP flood-hazard products and warns effective information can change or be superseded. No address was entered and no Asset A flood zone is asserted.

## 5. Tax and rate context

Official IRS URLs:
- https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips
- https://www.irs.gov/instructions/i8824
- https://www.irs.gov/forms-pubs/about-form-8824

The IRS overview limits Section 1031 to qualifying real property held for business/investment, excludes real property held primarily for sale, and requires gain recognition to the extent of non-like-kind property or money. Form 8824 is the reporting form. The instructions describe **45-day identification** and **180-day receipt**, or the earlier tax-return due date including extensions. This does not establish eligibility or suitability for Asset A or its owner.

Official Treasury URL: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026

The **2026-01-02** row reports ten-year par yield **4.19%**, twenty-year **4.81%**, thirty-year **4.86%**. This verifies the inherited model’s historical ten-year anchor. The page also displayed 2026-11-06 as the latest date, but this audit does not extract or claim a current November ten-year value. The 4.19% historical observation is not itself a property discount rate.
