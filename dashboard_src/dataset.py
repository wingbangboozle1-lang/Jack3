"""Verified evidence dataset for the /dashboard/ layer (session 27610006).

Rule enforced by this repo's publication standard:
  * every published value was read directly from the official source listed beside it
    during this session (2026-11-08), OR is explicitly marked 'unverified' (blank),
    OR is explicitly marked 'derived' with its arithmetic and inputs shown.
  * nothing about the subject property is invented. Lease, rent, address, parcel and
    owner-tax inputs were never supplied, so those cells stay blank and are flagged.

No personal information is collected or reproduced. The subject asset is referred to
only as "Asset A".
"""
from __future__ import annotations

import json
from pathlib import Path

SNAPSHOT = "2026-11-08"
SESSION = "27610006"

# ---------------------------------------------------------------------------
# 1. Source register. Every published row links to one of these.
# ---------------------------------------------------------------------------
SOURCES: dict[str, dict[str, str]] = {
    "S-01": {
        "name": "Census Bureau QuickFacts — Los Angeles city, California (V2025)",
        "publisher": "U.S. Census Bureau (census.gov)",
        "url": "https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225",
        "accessed": "2026-11-08",
    },
    "S-02": {
        "name": "Census Bureau QuickFacts — Los Angeles County, California (V2025)",
        "publisher": "U.S. Census Bureau (census.gov)",
        "url": "https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225",
        "accessed": "2026-11-08",
    },
    "S-03": {
        "name": "Los Angeles Area Economic Summary (updated November 04, 2026)",
        "publisher": "U.S. Bureau of Labor Statistics (bls.gov)",
        "url": "https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf",
        "accessed": "2026-11-08",
    },
    "S-04": {
        "name": "Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity (DGS10)",
        "publisher": "Federal Reserve Bank of St. Louis, FRED (fred.stlouisfed.org); underlying data: U.S. Department of the Treasury",
        "url": "https://fred.stlouisfed.org/series/DGS10",
        "accessed": "2026-11-08",
    },
    "S-05": {
        "name": "Daily Treasury Par Yield Curve Rates, 2026",
        "publisher": "U.S. Department of the Treasury (home.treasury.gov)",
        "url": "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026",
        "accessed": "2026-11-08",
    },
    "S-06": {
        "name": "Jack in the Box Inc. — Form 10-K, fiscal year ended September 28, 2025",
        "publisher": "U.S. Securities and Exchange Commission, EDGAR (sec.gov)",
        "url": "https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm",
        "accessed": "2026-11-08 (filing index verified; Item-level figures inherited — see flag K-F-16)",
    },
    "S-07": {
        "name": "Jack in the Box Inc. — Form 8-K Exhibit 99.1, Q3 FY2026 earnings release",
        "publisher": "U.S. Securities and Exchange Commission, EDGAR (sec.gov)",
        "url": "https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm",
        "accessed": "2026-11-08",
    },
    "S-08": {
        "name": "Minimum Wage Frequently Asked Questions",
        "publisher": "California Department of Industrial Relations (dir.ca.gov)",
        "url": "https://www.dir.ca.gov/dlse/faq_minimumwage.htm",
        "accessed": "2026-11-08",
    },
    "S-09": {
        "name": "Fast Food Minimum Wage Frequently Asked Questions (AB 1228)",
        "publisher": "California Department of Industrial Relations (dir.ca.gov)",
        "url": "https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm",
        "accessed": "2026-11-08",
    },
    "S-10": {
        "name": "UCERF3: A New Earthquake Forecast for California's Complex Fault System (Fact Sheet 2015-3009)",
        "publisher": "U.S. Geological Survey (usgs.gov)",
        "url": "https://pubs.usgs.gov/fs/2015/3009/pdf/fs2015-3009.pdf",
        "accessed": "2026-11-08",
    },
    "S-11": {
        "name": "Fire Hazard Severity Zones",
        "publisher": "CAL FIRE — Office of the State Fire Marshal (osfm.fire.ca.gov)",
        "url": "https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones",
        "accessed": "2026-11-08",
    },
    "S-12": {
        "name": "FEMA Flood Map Service Center",
        "publisher": "Federal Emergency Management Agency (msc.fema.gov)",
        "url": "https://msc.fema.gov/portal/home",
        "accessed": "2026-11-08 (portal reached; parcel-level values require the address — see flag K-F-13)",
    },
    "S-13": {
        "name": "2024–25 End-of-Year Reports (four-year adjusted cohort graduation rate)",
        "publisher": "California Department of Education (cde.ca.gov)",
        "url": "https://www.cde.ca.gov/ds/cm/dqeoy25.asp",
        "accessed": "2026-11-08",
    },
    "S-14": {
        "name": "California School Dashboard — Los Angeles Unified, Graduation Rate (2025)",
        "publisher": "California Department of Education (caschooldashboard.org)",
        "url": "https://www.caschooldashboard.org/reports/19647330000000/2025/academic-engagement",
        "accessed": "2026-11-08",
    },
    "S-15": {
        "name": "Real Property Transfer Tax and Measure ULA FAQ",
        "publisher": "City of Los Angeles, Office of Finance (finance.lacity.gov)",
        "url": "https://finance.lacity.gov/faq/measure-ula",
        "accessed": "2026-11-08",
    },
    "S-16": {
        "name": "Documentary Transfer Tax — General Information",
        "publisher": "Los Angeles County Registrar-Recorder/County Clerk (lavote.gov)",
        "url": "https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info",
        "accessed": "2026-11-08",
    },
    "S-17": {
        "name": "Like-kind exchanges — Real estate tax tips (IRC §1031)",
        "publisher": "Internal Revenue Service (irs.gov)",
        "url": "https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips",
        "accessed": "2026-11-08",
    },
    "S-18": {
        "name": "Publication 800-10 — How Property Is Assessed (Proposition 13)",
        "publisher": "California State Board of Equalization (boe.ca.gov)",
        "url": "https://boe.ca.gov/pdf/pub800-10.pdf",
        "accessed": "2026-11-08",
    },
    "S-19": {
        "name": "Property Tax Annotation 220.0345 — Leases (35-year leasehold change-in-ownership rule)",
        "publisher": "California State Board of Equalization (boe.ca.gov)",
        "url": "https://www.boe.ca.gov/proptaxes/pdf/220_0345.pdf",
        "accessed": "2026-11-08",
    },
    "S-20": {
        "name": "ZIMAS — Los Angeles City parcel and zoning lookup",
        "publisher": "City of Los Angeles (zimas.lacity.gov)",
        "url": "https://zimas.lacity.org/",
        "accessed": "2026-11-08 (lookup tool; requires the address — see flags K-F-01, K-F-02)",
    },
    "S-21": {
        "name": "FEMA National Risk Index",
        "publisher": "Federal Emergency Management Agency (hazards.fema.gov)",
        "url": "https://hazards.fema.gov/nri/",
        "accessed": "2026-11-08 (index reached; county score values were not readable this session — see flag K-F-13)",
    },
}

# ---------------------------------------------------------------------------
# 2. Facts. `status` is one of: verified | derived | unverified
# ---------------------------------------------------------------------------
def F(fid, category, indicator, geography, value, period, source, status="verified", note=""):
    return {
        "id": fid, "category": category, "indicator": indicator, "geography": geography,
        "value": value, "period": period, "source": source, "status": status, "note": note,
    }


FACTS: list[dict] = [
    # ---------------- Geography ----------------
    F("G-01", "geography", "Land area in square miles, 2020", "Los Angeles city", "469.49", "Census 2020", "S-01"),
    F("G-02", "geography", "Population per square mile, 2020", "Los Angeles city", "8,304.2", "Census 2020", "S-01"),
    F("G-03", "geography", "Population per square mile, 2010", "Los Angeles city", "8,092.3", "Census 2010", "S-01"),
    F("G-04", "geography", "Land area in square miles, 2020", "Los Angeles County", "4,059.28", "Census 2020", "S-02"),
    F("G-05", "geography", "Population per square mile, 2020", "Los Angeles County", "2,466.9", "Census 2020", "S-02"),
    F("G-06", "geography", "Mean travel time to work, workers 16+ (minutes)", "Los Angeles city", "30.7", "ACS 2020-2024", "S-01"),
    F("G-07", "geography", "Mean travel time to work, workers 16+ (minutes)", "Los Angeles County", "30.4", "ACS 2020-2024", "S-02"),
    F("G-08", "geography", "Building permits", "Los Angeles County", "22,250", "2025", "S-02"),
    F("G-09", "geography", "Building permits", "Los Angeles city", "(not published)", "2025", "S-01", "unverified",
      "QuickFacts reports this cell as not available for the city; left blank rather than substituted."),
    F("G-10", "geography", "Subject parcel address, APN and census tract", "Asset A (subject property)", "(not supplied)", "—", "S-20", "unverified",
      "No address or parcel identifier was provided. Every parcel-level determination (jurisdiction, flood zone, fire zone) is therefore blocked."),
    F("G-11", "geography", "Whether the site is inside the incorporated City of Los Angeles", "Asset A (subject property)", "(not supplied)", "—", "S-15", "unverified",
      "Decides whether Measure ULA applies on a sale. 'Central Los Angeles' is a planning colloquialism, not a legal boundary."),

    # ---------------- Demographics ----------------
    F("D-01", "demographics", "Population", "Los Angeles city", "3,869,089", "July 1, 2025 (V2025)", "S-01"),
    F("D-02", "demographics", "Population estimates base", "Los Angeles city", "3,899,342", "April 1, 2020 (V2025)", "S-01"),
    F("D-03", "demographics", "Population change, April 1 2020 base to July 1 2025", "Los Angeles city", "-0.8%", "2020-2025 (V2025)", "S-01"),
    F("D-04", "demographics", "Population", "Los Angeles city", "3,898,747", "Census April 1, 2020", "S-01"),
    F("D-05", "demographics", "Population", "Los Angeles city", "3,792,621", "Census April 1, 2010", "S-01"),
    F("D-06", "demographics", "Population", "Los Angeles County", "9,694,934", "July 1, 2025 (V2025)", "S-02"),
    F("D-07", "demographics", "Population estimates base", "Los Angeles County", "10,017,414", "April 1, 2020 (V2025)", "S-02"),
    F("D-08", "demographics", "Population change, April 1 2020 base to July 1 2025", "Los Angeles County", "-3.2%", "2020-2025 (V2025)", "S-02"),
    F("D-09", "demographics", "Population", "Los Angeles County", "10,014,009", "Census April 1, 2020", "S-02"),
    F("D-10", "demographics", "Population", "Los Angeles County", "9,818,605", "Census April 1, 2010", "S-02"),
    F("D-11", "demographics", "Median household income (in 2024 dollars)", "Los Angeles city", "$81,939", "ACS 2020-2024", "S-01"),
    F("D-12", "demographics", "Median household income (in 2024 dollars)", "Los Angeles County", "$90,112", "ACS 2020-2024", "S-02"),
    F("D-13", "demographics", "Per capita income (in 2024 dollars)", "Los Angeles city", "$47,685", "ACS 2020-2024", "S-01"),
    F("D-14", "demographics", "Per capita income (in 2024 dollars)", "Los Angeles County", "$45,792", "ACS 2020-2024", "S-02"),
    F("D-15", "demographics", "Persons in poverty, percent", "Los Angeles city", "16.5%", "2020-2024 (SAIPE)", "S-01"),
    F("D-16", "demographics", "Persons in poverty, percent", "Los Angeles County", "13.3%", "2020-2024 (SAIPE)", "S-02"),
    F("D-17", "demographics", "Households", "Los Angeles city", "1,439,097", "ACS 2020-2024", "S-01"),
    F("D-18", "demographics", "Households", "Los Angeles County", "3,416,449", "ACS 2020-2024", "S-02"),
    F("D-19", "demographics", "Persons per household", "Los Angeles city", "2.61", "ACS 2020-2024", "S-01"),
    F("D-20", "demographics", "Persons per household", "Los Angeles County", "2.81", "ACS 2020-2024", "S-02"),
    F("D-21", "demographics", "Owner-occupied housing unit rate", "Los Angeles city", "36.0%", "ACS 2020-2024", "S-01"),
    F("D-22", "demographics", "Owner-occupied housing unit rate", "Los Angeles County", "45.9%", "ACS 2020-2024", "S-02"),
    F("D-23", "demographics", "Median value of owner-occupied housing units", "Los Angeles city", "$921,200", "ACS 2020-2024", "S-01"),
    F("D-24", "demographics", "Median value of owner-occupied housing units", "Los Angeles County", "$834,200", "ACS 2020-2024", "S-02"),
    F("D-25", "demographics", "Median gross rent", "Los Angeles city", "$1,933", "ACS 2020-2024", "S-01"),
    F("D-26", "demographics", "Median gross rent", "Los Angeles County", "$1,954", "ACS 2020-2024", "S-02"),
    F("D-27", "demographics", "Foreign-born persons, percent", "Los Angeles city", "35.7%", "ACS 2020-2024", "S-01"),
    F("D-28", "demographics", "Foreign-born persons, percent", "Los Angeles County", "33.4%", "ACS 2020-2024", "S-02"),
    F("D-29", "demographics", "Persons under 18 years, percent", "Los Angeles city", "19.2%", "V2025", "S-01"),
    F("D-30", "demographics", "Persons 65 years and over, percent", "Los Angeles city", "14.2%", "V2025", "S-01"),
    F("D-31", "demographics", "Persons under 18 years, percent", "Los Angeles County", "19.2%", "V2025", "S-02"),
    F("D-32", "demographics", "Persons 65 years and over, percent", "Los Angeles County", "17.1%", "V2025", "S-02"),
    F("D-33", "demographics", "High school graduate or higher, percent of persons 25+", "Los Angeles city", "79.6%", "ACS 2020-2024", "S-01"),
    F("D-34", "demographics", "Bachelor's degree or higher, percent of persons 25+", "Los Angeles city", "38.5%", "ACS 2020-2024", "S-01"),
    F("D-35", "demographics", "High school graduate or higher, percent of persons 25+", "Los Angeles County", "80.9%", "ACS 2020-2024", "S-02"),
    F("D-36", "demographics", "Bachelor's degree or higher, percent of persons 25+", "Los Angeles County", "36.0%", "ACS 2020-2024", "S-02"),
    F("D-37", "demographics", "White alone, percent", "Los Angeles County", "62.9%", "V2025", "S-02"),
    F("D-38", "demographics", "Black alone, percent", "Los Angeles County", "8.9%", "V2025", "S-02"),
    F("D-39", "demographics", "Asian alone, percent", "Los Angeles County", "16.6%", "V2025", "S-02"),
    F("D-40", "demographics", "Two or More Races, percent", "Los Angeles County", "5.8%", "V2025", "S-02"),
    F("D-41", "demographics", "Hispanic or Latino, percent", "Los Angeles County", "49.3%", "V2025", "S-02"),
    F("D-42", "demographics", "White alone, not Hispanic or Latino, percent", "Los Angeles County", "24.6%", "V2025", "S-02"),
    F("D-43", "demographics", "Race-alone shares — city-level breakdown", "Los Angeles city", "(withheld — internally inconsistent)", "V2025", "S-01", "unverified",
      "The city page's race-alone percentages sum to 74.3% while the county page's sum to 99.8%. Until reconciled the city rows are not published."),

    # ---------------- Economy ----------------
    F("E-01", "economy", "Unemployment rate", "Los Angeles metro area", "4.4%", "September 2026", "S-03"),
    F("E-02", "economy", "Unemployment rate", "Los Angeles County", "4.5%", "September 2026", "S-03"),
    F("E-03", "economy", "Unemployment rate", "Los Angeles city", "4.5%", "September 2026", "S-03"),
    F("E-04", "economy", "Unemployment rate", "California", "5.1%", "September 2026", "S-03"),
    F("E-05", "economy", "Unemployment rate", "United States", "4.0%", "September 2026", "S-03"),
    F("E-06", "economy", "Unemployment rate, one year earlier", "Los Angeles metro area", "5.5%", "September 2025", "S-03"),
    F("E-07", "economy", "Unemployment rate, one year earlier", "Los Angeles County", "5.9%", "September 2025", "S-03"),
    F("E-08", "economy", "Unemployment rate, one year earlier", "Los Angeles city", "5.9%", "September 2025", "S-03"),
    F("E-09", "economy", "Total nonfarm employment (thousands)", "Los Angeles metro area", "6,282.1", "September 2026", "S-03"),
    F("E-10", "economy", "Total nonfarm employment, 12-month change (thousands)", "Los Angeles metro area", "+30.2", "Sep 2025 → Sep 2026", "S-03"),
    F("E-11", "economy", "Total nonfarm employment, 12-month percent change", "Los Angeles metro area", "+0.5%", "Sep 2025 → Sep 2026", "S-03"),
    F("E-12", "economy", "Leisure and hospitality employment (thousands)", "Los Angeles metro area", "782.0", "September 2026", "S-03"),
    F("E-13", "economy", "Leisure and hospitality employment, 12-month percent change", "Los Angeles metro area", "+1.5%", "Sep 2025 → Sep 2026", "S-03"),
    F("E-14", "economy", "Education and health services employment (thousands)", "Los Angeles metro area", "1,340.7", "September 2026", "S-03"),
    F("E-15", "economy", "Education and health services, 12-month percent change", "Los Angeles metro area", "+3.8%", "Sep 2025 → Sep 2026", "S-03"),
    F("E-16", "economy", "Information employment, 12-month percent change", "Los Angeles metro area", "-5.7%", "Sep 2025 → Sep 2026", "S-03"),
    F("E-17", "economy", "Manufacturing employment, 12-month percent change", "Los Angeles metro area", "-1.2%", "Sep 2025 → Sep 2026", "S-03"),
    F("E-18", "economy", "Financial activities employment, 12-month percent change", "Los Angeles metro area", "-1.7%", "Sep 2025 → Sep 2026", "S-03"),
    F("E-19", "economy", "Professional and business services, 12-month percent change", "Los Angeles metro area", "-0.5%", "Sep 2025 → Sep 2026", "S-03"),
    F("E-20", "economy", "Government employment, 12-month percent change", "Los Angeles metro area", "-1.1%", "Sep 2025 → Sep 2026", "S-03"),
    F("E-21", "economy", "Average weekly wages, all industries", "Los Angeles County", "$1,704", "Q1 2026", "S-03"),
    F("E-22", "economy", "Average hourly wage, all occupations (OES)", "Los Angeles metro area", "$37.15", "May 2025", "S-03"),
    F("E-23", "economy", "Employment Cost Index, 12-month percent change", "Los Angeles-Long Beach, CA CSA", "+3.9%", "September 2026", "S-03"),
    F("E-24", "economy", "CPI-U, all items, 12-month percent change", "Los Angeles metro area", "+3.7%", "September 2026", "S-03"),
    F("E-25", "economy", "CPI-U, food, 12-month percent change", "Los Angeles metro area", "+2.8%", "September 2026", "S-03"),
    F("E-26", "economy", "CPI-U, energy, 12-month percent change", "Los Angeles metro area", "+20.3%", "September 2026", "S-03"),
    F("E-27", "economy", "10-Year U.S. Treasury constant maturity yield", "United States", "4.84%", "2026-11-05", "S-04"),
    F("E-28", "economy", "10-Year U.S. Treasury constant maturity yield", "United States", "4.90%", "2026-11-04", "S-04"),
    F("E-29", "economy", "10-Year U.S. Treasury yield, observed range", "United States", "4.77% – 5.31%", "2026-09-01 to 2026-11-05", "S-04", "derived",
      "Minimum 4.77% (2026-09-03) and maximum 5.31% (2026-10-05) read from the daily DGS10 series."),
    F("E-30", "economy", "Total accommodation and food services sales ($1,000)", "Los Angeles city", "17,366,966", "2022 Economic Census", "S-01"),
    F("E-31", "economy", "Total accommodation and food services sales ($1,000)", "Los Angeles County", "44,000,801", "2022 Economic Census", "S-02"),
    F("E-32", "economy", "Total retail sales ($1,000)", "Los Angeles city", "81,351,523", "2022 Economic Census", "S-01"),
    F("E-33", "economy", "Total retail sales per capita", "Los Angeles city", "$21,281", "2022 Economic Census", "S-01"),
    F("E-34", "economy", "Total employer establishments", "Los Angeles County", "304,988", "2023", "S-02"),
    F("E-35", "economy", "Total employment", "Los Angeles County", "3,987,736", "2023", "S-02"),
    F("E-36", "economy", "Total employment, percent change 2022-2023", "Los Angeles County", "+2.3%", "2022-2023", "S-02"),
    F("E-37", "economy", "State minimum wage", "California", "$16.90 per hour", "From January 1, 2026", "S-08"),
    F("E-38", "economy", "Fast-food minimum wage (AB 1228)", "California", "$20.00 per hour", "From April 1, 2024", "S-09"),
    F("E-39", "economy", "AB 1228 applies to franchisees as well as the brand owner", "California", "Yes", "Per DIR FAQ", "S-09"),
    F("E-40", "economy", "City of Los Angeles general minimum wage", "Los Angeles city", "(not verified this session)", "2026", "S-08", "unverified",
      "The state fast-food floor of $20.00/hour governs covered limited-service chains of 60+ establishments unless a local general rate exceeds it. The city rate was not independently confirmed here."),
    F("E-41", "economy", "Market cap rate for single-tenant net-leased restaurants", "Asset A (subject property)", "(no official source)", "—", "S-05", "unverified",
      "No U.S. government agency publishes commercial cap rates or comparable-sale prices. This cell is left blank; it must come from private-market evidence that this project cannot verify."),

    # ---------------- Schools ----------------
    F("SC-01", "schools", "Four-year adjusted cohort graduation rate", "California (statewide)", "87.5%", "2024-25", "S-13"),
    F("SC-02", "schools", "Four-year adjusted cohort graduation rate, prior year", "California (statewide)", "86.4%", "2023-24", "S-13"),
    F("SC-03", "schools", "Graduation rate", "Los Angeles Unified", "86.5%", "2025", "S-14"),
    F("SC-04", "schools", "Graduation rate", "Los Angeles Unified", "86.7%", "2024", "S-14"),
    F("SC-05", "schools", "Graduation rate", "Los Angeles Unified", "83.6%", "2023", "S-14"),
    F("SC-06", "schools", "Graduation rate", "Los Angeles Unified", "86.0%", "2022", "S-14"),
    F("SC-07", "schools", "Graduation rate", "Los Angeles Unified", "82.1%", "2019", "S-14"),
    F("SC-08", "schools", "Five-year graduation rate", "Los Angeles Unified", "86.5%", "2025", "S-14"),
    F("SC-09", "schools", "Graduation rate, English Learners", "Los Angeles Unified", "64.1% (four-year)", "2025", "S-14"),
    F("SC-10", "schools", "Graduation rate, socioeconomically disadvantaged", "Los Angeles Unified", "(not published as a single figure)", "2025", "S-14", "unverified",
      "The Dashboard reports subgroup outcomes but the single composite figure was not captured this session; left blank."),
    F("SC-11", "schools", "Assigned public schools for the subject parcel", "Asset A (subject property)", "(not supplied)", "—", "S-14", "unverified",
      "School assignment is address-specific and the address was not provided."),

    # ---------------- Tenant & lease ----------------
    F("T-01", "tenant", "System same-store sales", "Jack in the Box (systemwide)", "-1.1%", "Q3 FY2026 (12 weeks ended 2026-07-05)", "S-07"),
    F("T-02", "tenant", "Franchise same-store sales", "Jack in the Box (systemwide)", "-1.2%", "Q3 FY2026", "S-07"),
    F("T-03", "tenant", "Company-operated same-store sales", "Jack in the Box (systemwide)", "-0.9%", "Q3 FY2026", "S-07"),
    F("T-04", "tenant", "System same-store sales, prior-year quarter", "Jack in the Box (systemwide)", "-7.1%", "Q3 FY2025", "S-07"),
    F("T-05", "tenant", "Systemwide sales", "Jack in the Box (systemwide)", "$944.110 million", "Q3 FY2026", "S-07"),
    F("T-06", "tenant", "Systemwide sales", "Jack in the Box (systemwide)", "$3,137.303 million", "40 weeks ended 2026-07-05", "S-07"),
    F("T-07", "tenant", "Systemwide sales, prior-year period", "Jack in the Box (systemwide)", "$3,284.624 million", "40 weeks ended 2025-07-06", "S-07"),
    F("T-08", "tenant", "Systemwide sales, year-over-year change", "Jack in the Box (systemwide)", "-4.5%", "40 weeks, FY2026 vs FY2025", "S-07", "derived",
      "3,137.303 / 3,284.624 - 1 = -4.48%, rounded to -4.5%."),
    F("T-09", "tenant", "Total revenues", "Jack in the Box Inc.", "$257.657 million", "Q3 FY2026", "S-07"),
    F("T-10", "tenant", "Total revenues, prior-year quarter", "Jack in the Box Inc.", "$262.401 million", "Q3 FY2025", "S-07"),
    F("T-11", "tenant", "Franchise rental revenues", "Jack in the Box Inc.", "$242.526 million", "40 weeks ended 2026-07-05", "S-07"),
    F("T-12", "tenant", "Franchise rental revenues, prior-year period", "Jack in the Box Inc.", "$260.254 million", "40 weeks ended 2025-07-06", "S-07"),
    F("T-13", "tenant", "Franchise rental revenues, year-over-year change", "Jack in the Box Inc.", "-6.8%", "40 weeks, FY2026 vs FY2025", "S-07", "derived",
      "242.526 / 260.254 - 1 = -6.81%, rounded to -6.8%. This is rent the company collects as intermediate lessor, and it is falling faster than revenue overall."),
    F("T-14", "tenant", "Franchise occupancy expenses (rent the company pays to landlords)", "Jack in the Box Inc.", "$166.043 million", "40 weeks ended 2026-07-05", "S-07"),
    F("T-15", "tenant", "Total restaurants at end of quarter", "Jack in the Box (systemwide)", "2,115", "Q3 FY2026", "S-07"),
    F("T-16", "tenant", "Company-operated restaurants at end of quarter", "Jack in the Box (systemwide)", "149", "Q3 FY2026", "S-07"),
    F("T-17", "tenant", "Franchised restaurants at end of quarter", "Jack in the Box (systemwide)", "1,966", "Q3 FY2026", "S-07"),
    F("T-18", "tenant", "Restaurant openings in the quarter", "Jack in the Box (systemwide)", "4", "Q3 FY2026", "S-07"),
    F("T-19", "tenant", "Restaurant closures in the quarter", "Jack in the Box (systemwide)", "17", "Q3 FY2026", "S-07"),
    F("T-20", "tenant", "Net restaurant change in the quarter", "Jack in the Box (systemwide)", "-13", "Q3 FY2026", "S-07"),
    F("T-21", "tenant", "Guidance: restaurant count", "Jack in the Box (systemwide)", "~2,100", "Fiscal year ending 2026-09-27", "S-07"),
    F("T-22", "tenant", "Guidance: restaurant closures", "Jack in the Box (systemwide)", "~50 to 60, most of them franchised", "Fiscal year 2026", "S-07"),
    F("T-23", "tenant", "Guidance: restaurant openings", "Jack in the Box (systemwide)", "~25", "Fiscal year 2026", "S-07"),
    F("T-24", "tenant", "Guidance: same-store sales", "Jack in the Box (systemwide)", "Low single-digit decline vs. FY2025", "Fiscal year 2026", "S-07"),
    F("T-25", "tenant", "Guidance: Adjusted EBITDA", "Jack in the Box Inc.", "$225 - $230 million", "Fiscal year 2026", "S-07"),
    F("T-26", "tenant", "Guidance: SG&A", "Jack in the Box Inc.", "$112 - $115 million", "Fiscal year 2026", "S-07"),
    F("T-27", "tenant", "Shareholder returns: dividend and repurchase programme", "Jack in the Box Inc.", "Discontinued", "Fiscal year 2026", "S-07"),
    F("T-28", "tenant", "'JACK on Track' plan components", "Jack in the Box Inc.", "Block closure programme and sale of real estate", "FY2026", "S-07"),
    F("T-29", "tenant", "Securitised refinancing completed", "Jack in the Box Inc.", "$500 million, Series 2026-1 Class A-2 Notes, anticipated repayment May 2031", "Q3 FY2026", "S-07"),
    F("T-30", "tenant", "Prepayment of existing securitised notes", "Jack in the Box Inc.", "$110.0 million, Series 2019-1 Class A-2-II", "Q3 FY2026", "S-07"),
    F("T-31", "tenant", "Del Taco divestiture", "Jack in the Box Inc.", "Completed December 22, 2025; reported as discontinued operations", "Q1 FY2026", "S-07"),
    F("T-32", "tenant", "Net earnings from continuing operations", "Jack in the Box Inc.", "$21.0 million", "Q3 FY2026", "S-07"),
    F("T-33", "tenant", "Adjusted EBITDA (non-GAAP)", "Jack in the Box Inc.", "$61.2 million", "Q3 FY2026", "S-07"),
    F("T-34", "tenant", "Cash and restricted cash at end of period", "Jack in the Box Inc.", "$71.771 million", "Q3 FY2026", "S-07"),
    F("T-35", "tenant", "Geographic footprint", "Jack in the Box (systemwide)", "25 states, Mexico and Guam", "Q3 FY2026", "S-07"),
    F("T-36", "tenant", "Units leased by the company from third-party landlords versus franchisee-direct sites", "Jack in the Box (systemwide)", "(inherited, not re-verified this session)", "FY2025 10-K Item 2", "S-06", "unverified",
      "An earlier session reported 1,585 company-leased units versus 387 franchisee-direct units from Item 2. The 10-K document is 2.66 MB and was not re-read line by line here, so the figures are not republished."),
    F("T-37", "tenant", "Jack in the Box franchise average unit volume", "Jack in the Box (franchise)", "(inherited, not re-verified this session)", "FY2025 10-K", "S-06", "unverified",
      "An earlier session reported $1,874k (FY25) and $1,949k (FY24). Not re-read here; not republished."),
    F("T-38", "tenant", "Lease commencement date, primary term and expiry date", "Asset A (subject property)", "(not supplied)", "—", "S-07", "unverified",
      "The brief states an expiry window of 2030-2035. That is a five-year range, not a date, and lease economics differ materially across it."),
    F("T-39", "tenant", "Contract rent, escalation and percentage-rent terms", "Asset A (subject property)", "(not supplied)", "—", "S-07", "unverified"),
    F("T-40", "tenant", "Whether the net lease is absolute (tenant bears roof, structure, insurance and tax) or modified", "Asset A (subject property)", "(not supplied)", "—", "S-07", "unverified"),
    F("T-41", "tenant", "Lease obligor: Jack in the Box Inc. corporate, or an individual franchisee", "Asset A (subject property)", "(not supplied)", "—", "S-07", "unverified",
      "This is the single most important unknown. Corporate credit and a single-unit franchisee's credit are different risks, and the issuer's closure programme acts through franchise agreements, not through your real-estate lease."),
    F("T-42", "tenant", "Renewal options, notice deadlines and remaining term including options", "Asset A (subject property)", "(not supplied)", "—", "S-19", "unverified",
      "Needed to test the California 35-year leasehold reassessment rule."),
    F("T-43", "tenant", "Subject restaurant's own unit-level sales versus the system average", "Asset A (subject property)", "(not supplied)", "—", "S-07", "unverified",
      "System same-store sales are not the subject restaurant's performance."),

    # ---------------- Property tax & transfer ----------------
    F("X-01", "tax", "Proposition 13 general levy ceiling", "California", "1% of assessed value, plus rates for voter-approved bonded indebtedness", "Current law", "S-18"),
    F("X-02", "tax", "Proposition 13 annual assessment growth limit", "California", "Lower of the California CPI change or 2% per year, applied to factored base year value", "Current law", "S-18"),
    F("X-03", "tax", "Event that resets base year value to market", "California", "Change in ownership or completion of new construction", "Current law", "S-18"),
    F("X-04", "tax", "Proposition 8 decline-in-value", "California", "Assessed value is temporarily reduced when market value falls below factored base year value", "Current law", "S-18"),
    F("X-05", "tax", "35-year leasehold change-in-ownership rule", "California", "Creating, terminating, or transferring a leasehold with a term of 35 years or more (including renewal options) is a change in ownership", "Revenue and Taxation Code § 61(c)(1)", "S-19"),
    F("X-06", "tax", "Transfer of a lessor's interest where the lease has 35+ years remaining", "California", "Not a change in ownership", "Revenue and Taxation Code § 62(g); BOE Rule 462(f)(2)(B)", "S-19"),
    F("X-07", "tax", "City of Los Angeles base documentary transfer tax", "City of Los Angeles", "$2.25 per $500 (0.45%)", "Current", "S-15"),
    F("X-08", "tax", "Measure ULA rate, tier 1", "City of Los Angeles", "4% of total transaction value above $5,400,000 and below $10,900,000", "Closings after 2026-06-30", "S-15"),
    F("X-09", "tax", "Measure ULA rate, tier 2", "City of Los Angeles", "5.5% of total transaction value at or above $10,900,000", "Closings after 2026-06-30", "S-15"),
    F("X-10", "tax", "Measure ULA effective date", "City of Los Angeles", "Conveyances on or after April 1, 2023", "Ordinance", "S-15"),
    F("X-11", "tax", "Measure ULA threshold indexation", "City of Los Angeles", "Thresholds are adjusted annually to the BLS Chained Consumer Price Index", "Ordinance", "S-15"),
    F("X-12", "tax", "Total City of Los Angeles transfer tax rate above the tier-1 threshold", "City of Los Angeles", "4.45% (0.45% base + 4.00% ULA)", "Closings after 2026-06-30", "S-15", "derived",
      "Sum of the two published City rates."),
    F("X-13", "tax", "Total City of Los Angeles transfer tax rate at or above the tier-2 threshold", "City of Los Angeles", "5.95% (0.45% base + 5.50% ULA)", "Closings after 2026-06-30", "S-15", "derived",
      "Sum of the two published City rates."),
    F("X-14", "tax", "Los Angeles County documentary transfer tax", "Los Angeles County", "$0.55 per $500 (0.11%)", "Current", "S-16"),
    F("X-15", "tax", "Measure ULA applies to the full consideration, not the excess over the threshold", "City of Los Angeles", "Yes — 4% or 5.5% of the total transaction value", "Per the published rate table", "S-15"),
    F("X-16", "tax", "Measure ULA exemptions", "City of Los Angeles", "Qualifying 501(c)(3) entities; the United States, states and their agencies; entities exempt from city taxation", "Ordinance", "S-15"),
    F("X-17", "tax", "Like-kind exchange (IRC § 1031) scope after the Tax Cuts and Jobs Act", "United States", "Real property only; personal and intangible property no longer qualify", "From January 1, 2018", "S-17"),
    F("X-18", "tax", "Like-kind test for real property", "United States", "Real properties are generally like-kind regardless of whether improved or unimproved; U.S. real property is not like-kind to foreign real property", "Current", "S-17"),
    F("X-19", "tax", "Form used to report a like-kind exchange", "United States", "Form 8824", "Current", "S-17"),
    F("X-20", "tax", "Owner's adjusted cost basis, depreciation taken and depreciation recapture exposure", "Asset A (subject property)", "(not supplied)", "—", "S-17", "unverified",
      "Determines the taxable gain on a sale and therefore whether a § 1031 exchange is worth pursuing."),

    # ---------------- Hazards ----------------
    F("H-01", "hazards", "30-year likelihood of one or more M≥6.7 earthquakes", "Los Angeles region", "60%", "UCERF3, 30 years from 2014", "S-10"),
    F("H-02", "hazards", "30-year likelihood of one or more M≥7.0 earthquakes", "Los Angeles region", "46%", "UCERF3, 30 years from 2014", "S-10"),
    F("H-03", "hazards", "30-year likelihood of one or more M≥7.5 earthquakes", "Los Angeles region", "31%", "UCERF3, 30 years from 2014", "S-10"),
    F("H-04", "hazards", "30-year likelihood of one or more M≥6.0 earthquakes", "Los Angeles region", "96%", "UCERF3, 30 years from 2014", "S-10"),
    F("H-05", "hazards", "30-year likelihood of one or more M≥8.0 earthquakes", "Los Angeles region", "7%", "UCERF3, 30 years from 2014", "S-10"),
    F("H-06", "hazards", "Average repeat time for M≥6.7 earthquakes", "Los Angeles region", "40 years", "UCERF3", "S-10"),
    F("H-07", "hazards", "30-year likelihood of one or more M≥6.7 earthquakes", "Southern California region", "93%", "UCERF3, 30 years from 2014", "S-10"),
    F("H-08", "hazards", "30-year likelihood of one or more M≥7.5 earthquakes", "Southern California region", "36%", "UCERF3, 30 years from 2014", "S-10"),
    F("H-09", "hazards", "Fire Hazard Severity Zone classifications", "California", "Moderate, High, Very High", "Current", "S-11"),
    F("H-10", "hazards", "State Responsibility Area FHSZ maps in effect", "California", "Effective April 1, 2024", "Current", "S-11"),
    F("H-11", "hazards", "Local Responsibility Area FHSZ maps released to jurisdictions", "California", "Phases 1-4: February 10, February 24, March 10 and March 24, 2025", "2025", "S-11"),
    F("H-12", "hazards", "FHSZ maps measure hazard, not risk", "California", "Hazard is the physical likelihood and expected fire behaviour over 30 to 50 years, before mitigation", "Per CAL FIRE", "S-11"),
    F("H-13", "hazards", "2026 State Responsibility Area FHSZ update", "California", "Public comment period open at the time of this snapshot", "2026", "S-11"),
    F("H-14", "hazards", "FEMA flood zone for the subject parcel", "Asset A (subject property)", "(not supplied)", "—", "S-12", "unverified",
      "Requires the address or parcel identifier in the FEMA Map Service Center."),
    F("H-15", "hazards", "FEMA National Risk Index scores for Los Angeles County", "Los Angeles County", "(not readable this session)", "—", "S-21", "unverified",
      "The index portal was reached but county-level score values could not be read from the official page during this session. Third-party mirrors were rejected under the no-aggregator rule."),
    F("H-16", "hazards", "CAL FIRE Fire Hazard Severity Zone for the subject parcel", "Asset A (subject property)", "(not supplied)", "—", "S-11", "unverified",
      "Requires the address in the CAL FIRE viewer."),
]

# ---------------------------------------------------------------------------
# 3. Derived projection system (analysis, not an official forecast)
# ---------------------------------------------------------------------------
# Inputs are all verified above. The arithmetic is printed on the page.
PROJECTION_INPUTS = [
    {"label": "Los Angeles County population, measured change, April 2020 base to July 2025",
     "value": "-3.2%", "source": "S-02", "span_years": 5.25},
    {"label": "Los Angeles city population, measured change, April 2020 base to July 2025",
     "value": "-0.8%", "source": "S-01", "span_years": 5.25},
    {"label": "Los Angeles metro nonfarm employment, 12-month change to September 2026",
     "value": "+0.5%", "source": "S-03", "span_years": 1.0},
    {"label": "Los Angeles metro CPI-U, all items, 12-month change to September 2026",
     "value": "+3.7%", "source": "S-03", "span_years": 1.0},
    {"label": "Los Angeles-Long Beach CSA Employment Cost Index, 12-month change to September 2026",
     "value": "+3.9%", "source": "S-03", "span_years": 1.0},
    {"label": "10-Year U.S. Treasury constant maturity yield, 2026-11-05",
     "value": "4.84%", "source": "S-04", "span_years": None},
]

# Scenario bands. Deliberately free of probability weights: no official source
# assigns probabilities to these outcomes, so none are asserted here.
SCENARIOS = [
    {"key": "low", "name": "Measured trend continues",
     "basis": "Applies the published Census population trend and the published BLS employment trend unchanged to 2030 and 2035.",
     "pop_annual": -0.0062, "emp_annual": 0.005, "rent_annual": 0.037},
    {"key": "base", "name": "Trend flattens",
     "basis": "Population stops declining and employment growth continues at the measured rate; rent is indexed at the published Los Angeles CPI-U rate of +3.7%.",
     "pop_annual": 0.0, "emp_annual": 0.005, "rent_annual": 0.037},
    {"key": "high", "name": "Partial recovery",
     "basis": "Population returns to its 2020 estimates base by 2035 and employment growth runs at twice the measured rate; rent is indexed at the published Los Angeles CPI-U rate of +3.7%.",
     "pop_annual": 0.0035, "emp_annual": 0.010, "rent_annual": 0.037},
]

# Present value of an annuity-due of 1.0 x current annual base rent, per year.
# Pure arithmetic; discount rate = verified 10-year Treasury yield + a declared premium.
RISK_FREE = 0.0484           # S-04, 2026-11-05
PREMIA = [0.010, 0.020, 0.030, 0.040, 0.050]
HORIZONS = [4, 5, 6, 7, 8, 9]   # expiry years 2030 .. 2035 measured from 2026


def pv_annuity_due(rate: float, years: int, growth: float = 0.0) -> float:
    """PV of 1.0 per year received at the start of each year for `years` years."""
    total = 0.0
    for t in range(years):
        total += ((1.0 + growth) / (1.0 + rate)) ** t
    return total


def build_grids() -> dict:
    grid_level, grid_growth = [], []
    for prem in PREMIA:
        rate = RISK_FREE + prem
        row_l = {"rate": rate, "premium": prem, "cells": [pv_annuity_due(rate, n) for n in HORIZONS]}
        row_g = {"rate": rate, "premium": prem, "cells": [pv_annuity_due(rate, n, 0.037) for n in HORIZONS]}
        grid_level.append(row_l)
        grid_growth.append(row_g)
    return {"level": grid_level, "growth": grid_growth}


def project(scenario: dict, year: int) -> dict:
    n = year - 2026
    return {
        "population_index": (1.0 + scenario["pop_annual"]) ** n,
        "employment_index": (1.0 + scenario["emp_annual"]) ** n,
        "rent_index": (1.0 + scenario["rent_annual"]) ** n,
    }


# ---------------------------------------------------------------------------
# 4. Flagged items (unverified / needs review)
# ---------------------------------------------------------------------------
FLAGS = [
    ("K-F-01", "Blocker", "Subject parcel address, APN and census tract were never supplied",
     "Every parcel-level determination — jurisdiction, flood zone, fire zone, school assignment, assessed value — is blocked.",
     "Owner-supplied deed, lease and tax bill", "S-20"),
    ("K-F-02", "Blocker", "Whether the site lies inside the incorporated City of Los Angeles is unknown",
     "Measure ULA adds 4.00% or 5.50% of gross consideration on a City of Los Angeles sale and 0% outside it. On a $6,000,000 sale that is the difference between roughly $0 and $240,000 of transfer tax.",
     "Owner confirmation of the taxing jurisdiction", "S-15"),
    ("K-F-03", "Blocker", "Lease commencement date, primary term and exact expiry date are unknown; '2030-2035' is a five-year range",
     "Remaining term drives value, financing and the Proposition 13 leasehold test. The two ends of the range produce materially different answers.",
     "Executed lease and all amendments", "S-07"),
    ("K-F-04", "Blocker", "Contract rent, escalations, percentage rent and option rents are unknown",
     "No income figure for this asset can be verified. All cash-flow work below is expressed in multiples of one year of base rent (R) instead.",
     "Executed lease and rent ledger", "S-07"),
    ("K-F-05", "High", "Whether the net lease is absolute or modified is unknown",
     "Under a modified gross or modified net lease the owner may carry roof, structure or insurance — a direct, unbudgeted capital call.",
     "Executed lease", "S-07"),
    ("K-F-06", "High", "The lease obligor is unknown: Jack in the Box Inc. corporate, or an individual franchisee",
     "The issuer's own filings describe shrinking franchise rental revenue and 50 to 60 closures in fiscal 2026, most of them franchised. Corporate credit and single-unit franchisee credit are not the same risk.",
     "Lease, estoppel certificate and guaranty", "S-07"),
    ("K-F-07", "High", "Existence and scope of a guaranty is unknown",
     "Determines whether a closure leaves the owner with a claim against a balance sheet or against a shell entity.",
     "Guaranty and estoppel certificate", "S-07"),
    ("K-F-08", "High", "Renewal options and total remaining term including options are unknown",
     "California reassesses a property when a leasehold of 35 years or more, counting options, is created or terminated. A renewal negotiated without checking this can trigger a reassessment.",
     "Executed lease and all amendments", "S-19"),
    ("K-F-09", "High", "Existing debt: balance, rate, maturity and recourse are unknown",
     "A refinance at today's 4.84% ten-year Treasury plus a spread may be materially above an expiring legacy rate, and a maturity inside the lease term is a hard constraint.",
     "Loan documents", "S-04"),
    ("K-F-10", "Medium", "Owner's adjusted cost basis, accumulated depreciation and other tax attributes are unknown",
     "Determines federal and California tax on a sale and whether a § 1031 exchange defers enough tax to justify its cost and timeline.",
     "Owner tax records", "S-17"),
    ("K-F-11", "Medium", "Market cap rate and comparable sales for single-tenant net-leased restaurants",
     "No U.S. government agency publishes commercial cap rates or private sale prices. The cell is left blank rather than filled from broker marketing material.",
     "Private market evidence (outside the official-source rule)", "S-05"),
    ("K-F-12", "Medium", "The subject restaurant's own unit-level sales versus the system average",
     "System same-store sales of -1.1% describe 2,115 restaurants, not this one. A site can outperform or underperform its system by a wide margin.",
     "Operator unit P&L", "S-07"),
    ("K-F-13", "Medium", "FEMA flood zone and National Risk Index values for the parcel and county",
     "The FEMA portal and index were reached, but parcel values need the address and county score values could not be read from the official page in this session. Third-party mirrors were rejected.",
     "FEMA Map Service Center lookup with the address", "S-21"),
    ("K-F-14", "Medium", "CAL FIRE Fire Hazard Severity Zone for the parcel",
     "Local Responsibility Area maps were issued to jurisdictions in early 2025 and the 2026 State Responsibility Area update is in public comment, so any pre-2025 determination is stale.",
     "CAL FIRE FHSZ viewer lookup with the address", "S-11"),
    ("K-F-15", "Low", "City of Los Angeles general minimum wage",
     "The state fast-food floor of $20.00 per hour governs covered limited-service chains of 60 or more establishments unless a local general rate exceeds it. The city rate was not independently confirmed in this session.",
     "City of Los Angeles Office of Wage Standards", "S-08"),
    ("K-F-16", "Medium", "FY2025 Form 10-K Item 2 lease structure (1,585 company-leased versus 387 franchisee-direct units)",
     "Reported by an earlier session. The filing is 2.66 MB and was not re-read line by line in this session, so the figures are not republished.",
     "Direct re-read of 10-K Item 2", "S-06"),
    ("K-F-17", "Low", "Jack in the Box franchise average unit volume ($1,874k FY25 / $1,949k FY24)",
     "Reported by an earlier session from 10-K pages 28-29. Not re-read in this session; not republished.",
     "Direct re-read of the FY2025 10-K", "S-06"),
]

# ---------------------------------------------------------------------------
# 5. Repo review irregularities found in this session's line-by-line pass
# ---------------------------------------------------------------------------
IRREGULARITIES = [
    ("K-IR-01", "High — privacy",
     "26 inherited HTML files render the repository account handle directly in footers or source tables.",
     "Internal scan of this working tree on 2026-11-08 (`grep -rl` across all tracked HTML).",
     "Out of scope for this layer and therefore not remediated here. The /dashboard/ layer reproduces no account handle, name, address or parcel identifier. Raised as cross-session request XR-K1.",
     "S-01"),
    ("K-IR-02", "High — sourcing",
     "Inherited layers cite non-official domains inside published table rows: bouldergroup.com (22 occurrences) and seyfarth.com (4) in analysis/, and datausa.io, point2homes.com, fool.com and similar in brief/ and pages/.",
     "Internal scan of `analysis/*.html` external hosts on 2026-11-08.",
     "Not republished here. Every external link in this layer resolves to a .gov, .ca.gov, municipal, Federal Reserve or SEC domain.",
     "S-01"),
    ("K-IR-03", "High — tax accuracy",
     "The inherited brief/ layer published expired Measure ULA thresholds of $5,300,000 and $10,600,000.",
     "Re-checked against the City of Los Angeles Office of Finance and the Los Angeles County Registrar-Recorder on 2026-11-08: for closings after 2026-06-30 the thresholds are $5,400,000 (4.00% ULA) and $10,900,000 (5.50% ULA).",
     "This layer publishes only the post-June-30-2026 thresholds.",
     "S-15"),
    ("K-IR-04", "Medium — stale input",
     "The inherited decision-file model anchors its discount rate to the 10-year Treasury yield of 4.19% observed on 2026-01-02.",
     "The same series now stands at 4.84% on 2026-11-05, a rise of about 65 basis points over the year.",
     "This layer anchors to 4.84% and sweeps a declared premium of 1.0% to 5.0% rather than a single point.",
     "S-04"),
    ("K-IR-05", "Medium — statistics",
     "Census QuickFacts race-alone percentages for Los Angeles city sum to 74.3% while the county equivalents sum to 99.8%. The two geographies are not internally consistent.",
     "Read directly from both QuickFacts tables on 2026-11-08.",
     "City-level race rows are withheld rather than published possibly wrong; county rows are published with the inconsistency disclosed.",
     "S-01"),
    ("K-IR-06", "Medium — row provenance",
     "Hundreds of inherited table rows carry no direct https source link (reported counts: decision-file 168, brief 91, analysis 83, docs 23, pages 20).",
     "Reported by earlier sessions and corroborated by this session's scan of `analysis/*.html`.",
     "This layer enforces in code that every body row carries a link from the source register.",
     "S-01"),
    ("K-IR-07", "Medium — lease semantics",
     "The inherited decision-file layer treats the issuer's franchise-agreement termination dates under 'JACK on Track' as if they were the real-estate lease expiry.",
     "The Q3 FY2026 earnings release describes a block closure programme and the sale of real estate; it does not set the expiry date of any landlord's lease, and the subject lease was never supplied.",
     "This layer states the distinction explicitly and does not infer a lease expiry from the closure programme.",
     "S-07"),
    ("K-IR-08", "Medium — freshness",
     "Earlier snapshots carried August 2026 BLS figures for Los Angeles.",
     "The current BLS Los Angeles Area Economic Summary, updated November 4, 2026, reports September 2026: unemployment 4.4% (metro) and 4.5% (city and county), nonfarm payrolls 6,282.1 thousand, CPI-U +3.7%.",
     "This layer publishes only the September 2026 observations.",
     "S-03"),
    ("K-IR-09", "Medium — conflicting conclusions",
     "Six inherited layers reach materially different headline recommendations, including one that ranks selling first and another that advises holding both options open.",
     "Read in the repository on 2026-11-08. No official source supports any of the rankings; they rest on assumptions about rent, cap rate and renewal probability that were never supplied.",
     "This layer refuses to rank the pathways numerically. It presents the decision drivers, the verified inputs and the risk balance, and leaves the ranking to the owner once the blocker documents are in hand.",
     "S-01"),
    ("K-IR-10", "Low — publication state",
     "The advisory/ layer was withheld from the published Pages artefact by another session after this session's base commit, on the grounds that its numerical scenario weights and pathway rankings are not established by the official sources it cites.",
     "Recorded in COORDINATION.md and in the merged PR #27 log.",
     "Noted. This layer therefore presents no scenario probabilities and no single-point pathway ranking.",
     "S-01"),
]

# ---------------------------------------------------------------------------
# 6. Decision pathway assessment (qualitative; analyst judgement, not official data)
# ---------------------------------------------------------------------------
PATHWAYS = [
    {
        "key": "A", "name": "Sell before expiry",
        "summary": "Convert an illiquid, single-tenant, single-site asset into cash or into a diversified position while a lease is still in place.",
        "drivers": [
            ("Sale proceeds are priced off the remaining lease term; the shorter the term at sale, the more the buyer discounts.", "S-07"),
            ("Measure ULA can take 4.00% or 5.50% of gross consideration if the site is inside the City of Los Angeles and the price clears the threshold.", "S-15"),
            ("System same-store sales fell 1.1% in Q3 FY2026 and the company guided to 50 to 60 closures in fiscal 2026.", "S-07"),
            ("A § 1031 exchange is available for real property and can defer the gain if the owner wants to stay in real estate.", "S-17"),
        ],
        "risks": [
            ("Sale certainty depends on a cap rate no government source publishes; the achievable price is unverifiable here.", "S-05"),
            ("Transfer tax, recapture and exchange deadlines make the execution path unforgiving.", "S-17"),
            ("Selling crystallises the tax today rather than at an unknown later date.", "S-17"),
        ],
    },
    {
        "key": "B", "name": "Renew with the incumbent tenant",
        "summary": "Extend the existing operator and keep the income stream, at a rent and term the tenant will actually sign.",
        "drivers": [
            ("Unemployment in the Los Angeles metro area fell to 4.4% in September 2026 from 5.5% a year earlier, and nonfarm payrolls rose 0.5%.", "S-03"),
            ("Education and health services grew 3.8% year over year and carry 1,340.7 thousand jobs, the largest sector in the metro.", "S-03"),
            ("The issuer's own filings describe a shrinking footprint and falling franchise rental revenue, which weakens the tenant's negotiating posture on rent.", "S-07"),
            ("Median household income in Los Angeles city is $81,939 and in the county $90,112, supporting local consumer demand.", "S-01"),
        ],
        "risks": [
            ("A renewal that pushes the total remaining term, counting options, to 35 years or more creates a change in ownership and a reassessment under California law.", "S-19"),
            ("The tenant is closing 50 to 60 restaurants in fiscal 2026 and has discontinued its dividend and buyback; credit is deteriorating, not improving.", "S-07"),
            ("Population in Los Angeles County is 3.2% below its 2020 estimates base, a demand headwind for marginal sites.", "S-02"),
            ("A renewal does not remove the concentration risk: one site, one operator, one intersection.", "S-07"),
        ],
    },
    {
        "key": "C", "name": "Short extension, then sell",
        "summary": "Buy time with a short, clean extension that preserves a marketable remaining term, then take the asset to market from a position of strength.",
        "drivers": [
            ("A sale is worth more with a signed term certain than with a looming expiry, so a short extension can be value-accretive even at a modest rent.", "S-07"),
            ("Keeping the total remaining term, including options, strictly under 35 years avoids the leasehold reassessment trigger.", "S-19"),
            ("The ten-year Treasury at 4.84% sets the risk-free anchor a buyer will use; the shorter the extension, the less duration risk the buyer takes.", "S-04"),
        ],
        "risks": [
            ("The tenant may decline a short extension or demand a rent concession that offsets the benefit.", "S-07"),
            ("Timing risk: if the market turns before the extension ends, the window closes.", "S-03"),
            ("Two transaction events mean two sets of legal and advisory costs.", "S-15"),
        ],
    },
    {
        "key": "D", "name": "Hold to expiry, then re-tenant or reposition",
        "summary": "Run the lease out, then lease to another operator or redevelop the site.",
        "drivers": [
            ("Fast-food sites are small-footprint, high-visibility parcels that can often be re-let to another limited-service or service-retail user.", "S-01"),
            ("Los Angeles city contains 8,304.2 people per square mile, among the densest urban footprints in the United States, which supports a range of alternative uses.", "S-01"),
            ("The county added 22,250 building permits in 2025, indicating continuing construction activity.", "S-02"),
        ],
        "risks": [
            ("Vacancy, tenant-improvement and leasing-commission costs are entirely the owner's during a dark period, and no official source can estimate them for this site.", "S-05"),
            ("The 60% thirty-year likelihood of an M≥6.7 earthquake in the Los Angeles region is an uninsured-balance-sheet risk that is worst when the site is vacant.", "S-10"),
            ("Re-tenanting a purpose-built restaurant box can require capital the owner may not want to commit at this stage.", "S-07"),
            ("Los Angeles County population is 3.2% below its 2020 base, so re-leasing demand assumptions should not be optimistic.", "S-02"),
        ],
    },
]

RISK_REGISTER = [
    ("R-01", "Business as usual", "Tenant credit deterioration",
     "Jack in the Box Inc. guided to 50 to 60 closures in fiscal 2026, reported a 6.8% decline in franchise rental revenue over 40 weeks, discontinued its dividend and buyback, and refinanced $500 million of securitised notes during fiscal 2026.",
     "High", "S-07"),
    ("R-02", "Business as usual", "Site-level closure at or before expiry",
     "The 'JACK on Track' plan is described as a block closure programme plus the sale of real estate. Whether this site is in the block cannot be determined without the lease and the operator's plan.",
     "High", "S-07"),
    ("R-03", "Business as usual", "Lease-obligor ambiguity",
     "If the obligor is a single-unit franchisee rather than the public company, the credit behind the rent is materially weaker and the closure programme runs through that franchise agreement.",
     "High", "S-07"),
    ("R-04", "Business as usual", "Renewal at a lower rent",
     "System same-store sales fell 1.1% in Q3 FY2026 on top of a 7.1% decline in the prior-year quarter, which supports a tenant asking for rent relief at renewal.",
     "High", "S-07"),
    ("R-05", "Business as usual", "Interest-rate and cap-rate repricing",
     "The ten-year Treasury moved between 4.77% and 5.31% between 2026-09-01 and 2026-11-05 and stood at 4.84% on 2026-11-05. Net-lease values are priced off this anchor.",
     "Medium", "S-04"),
    ("R-06", "Business as usual", "Property-tax reassessment on sale or on a long lease",
     "Proposition 13 resets base year value on a change in ownership, and a leasehold of 35 years or more including options is itself a change in ownership when created or terminated.",
     "Medium", "S-19"),
    ("R-07", "Business as usual", "Transfer-tax exposure on exit",
     "Inside the City of Los Angeles, a sale above $5,400,000 carries a total city transfer tax of 4.45% and a sale at or above $10,900,000 carries 5.95%, on the full consideration, plus 0.11% county tax.",
     "Medium", "S-15"),
    ("R-08", "Business as usual", "Labour-cost inflation at the operator",
     "California's fast-food minimum wage has been $20.00 per hour since April 1, 2024 and applies to franchisees; the state rate is $16.90 per hour from January 1, 2026. Unit economics, and therefore rent coverage, are compressed by the higher floor.",
     "Medium", "S-09"),
    ("R-09", "Business as usual", "Local demand headwind",
     "Los Angeles County population is 3.2% below its April 2020 estimates base and the city is 0.8% below; population is not growing into new restaurant supply.",
     "Medium", "S-02"),
    ("R-10", "Business as usual", "Consumer price pressure",
     "CPI-U in the Los Angeles metro area rose 3.7% year over year to September 2026, with energy up 20.3%, while the Employment Cost Index rose 3.9%. Real disposable income is being squeezed.",
     "Medium", "S-03"),
    ("R-11", "Business as usual", "Insurance availability and cost",
     "California's residential and commercial insurance market has been under stress following the January 2025 fires; no official source in this project quantifies the premium for this parcel.",
     "Medium", "S-11"),
    ("R-12", "Business as usual", "Sector concentration and single-asset risk",
     "One site, one operator, one intersection, in a system whose unit count fell by 13 net restaurants in a single quarter.",
     "Medium", "S-07"),
    ("R-13", "Business as usual", "1031 execution risk",
     "A like-kind exchange has statutory identification and closing deadlines and, since 2018, covers real property only. Missing a deadline defeats the deferral.",
     "Medium", "S-17"),
    ("R-14", "Black swan", "Major earthquake",
     "UCERF3 puts the 30-year likelihood of one or more M≥6.7 earthquakes in the Los Angeles region at 60%, of M≥7.0 at 46%, and of M≥7.5 at 31%. Earthquake is generally excluded from standard property policies.",
     "Severe", "S-10"),
    ("R-15", "Black swan", "Urban wildfire",
     "CAL FIRE issued Local Responsibility Area fire hazard severity zone maps to jurisdictions in early 2025 and has the 2026 State Responsibility Area update in public comment. Central Los Angeles is not immune: the January 2025 fires destroyed large parts of the county.",
     "Severe", "S-11"),
    ("R-16", "Black swan", "Flood",
     "FEMA's Map Service Center is the official determination point, but no flood zone could be established for this parcel without the address. Urban flooding is a documented Los Angeles County hazard.",
     "Moderate", "S-12"),
    ("R-17", "Black swan", "Civil unrest or a prolonged local shock",
     "No official source quantifies this probability for a specific parcel, so no number is asserted here. It is listed because a single-site retail asset has no internal diversification against a localised shutdown.",
     "Moderate", "S-01"),
    ("R-18", "Black swan", "Rapid policy shift on property or transfer tax",
     "Measure ULA thresholds are indexed annually and local tax measures are subject to the ballot. A change can alter after-tax proceeds between signing and closing.",
     "Moderate", "S-15"),
]

# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
def to_json() -> dict:
    return {
        "snapshot": SNAPSHOT,
        "session": SESSION,
        "sources": SOURCES,
        "facts": FACTS,
        "projection_inputs": PROJECTION_INPUTS,
        "scenarios": SCENARIOS,
        "horizons": HORIZONS,
        "risk_free": RISK_FREE,
        "premia": PREMIA,
        "grids": build_grids(),
        "projections": [{"key": s["key"], "years": {y: project(s, y) for y in (2030, 2035)}} for s in SCENARIOS],
        "flags": FLAGS,
        "irregularities": IRREGULARITIES,
        "pathways": PATHWAYS,
        "risks": RISK_REGISTER,
    }


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "dataset.json"
    out.write_text(json.dumps(to_json(), indent=1) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(FACTS)} facts, {len(SOURCES)} sources)")
