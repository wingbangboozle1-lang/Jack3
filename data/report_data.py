"""Canonical dataset for the integrated dashboard (session arena/0ed6d83e-jack3).

This module assembles ONE reconciled view of the project for the published site in
``report/``.  It does not invent values.  Every numerical row either

  * was re-read on the official publisher's page during this session
    (``verified-now``, with the reading date and what was seen), or
  * carries an official or primary source link and was read when the row was first
    captured (``source-linked``), or
  * is explicitly analytical output of the committed model (``analysis``), or
  * is industry (non-government) market data, kept out of the official evidence
    table and labelled as non-official (``industry``), or
  * could not be confirmed from an official source and is therefore BLANK and
    published on the Flagged for Review page (``unverified`` / ``input``).

No personal information is stored here, and none may be added.
"""

from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
READ_DATE = "2026-11-07"

# ---------------------------------------------------------------------------
# 1. SOURCE REGISTER
#    kind: official (government/statutory) | issuer (SEC filing) | industry
# ---------------------------------------------------------------------------
SOURCES = {
    "S_CENSUS_CO": dict(
        label="QuickFacts: Los Angeles County, California",
        publisher="U.S. Census Bureau",
        url="https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045224",
        kind="official", accessed="2026-11-06 / re-read 2026-11-07",
        used="Population, income, housing, education, economic-census counts"),
    "S_CENSUS_CITY": dict(
        label="QuickFacts: Los Angeles city, California",
        publisher="U.S. Census Bureau",
        url="https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045224",
        kind="official", accessed="2026-11-06 / re-read 2026-11-07",
        used="City population, population change, race shares"),
    "S_BLS_EAG": dict(
        label="Economy at a Glance: Los Angeles-Long Beach-Santa Ana, CA (MSA)",
        publisher="U.S. Bureau of Labor Statistics",
        url="https://www.bls.gov/eag/eag.ca_losangeles_msa.htm",
        kind="official", accessed="2026-11-07",
        used="Labor force, employment, unemployment, nonfarm payrolls by sector"),
    "S_BLS_METRO": dict(
        label="Metropolitan Area Employment and Unemployment (USDL-26-1618)",
        publisher="U.S. Bureau of Labor Statistics",
        url="https://www.bls.gov/news.release/pdf/metro.pdf",
        kind="official", accessed="2026-11-06",
        used="Metro area employment and unemployment comparison"),
    "S_BLS_SUMMARY": dict(
        label="Los Angeles Area Economic Summary",
        publisher="U.S. Bureau of Labor Statistics, Western Information Office",
        url="https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf",
        kind="official", accessed="2026-11-06",
        used="Wages, CPI, 12-month employment change"),
    "S_BLS_CPI": dict(
        label="Consumer Price Index, Los Angeles area",
        publisher="U.S. Bureau of Labor Statistics",
        url="https://www.bls.gov/regions/west/news-release/consumerpriceindex_losangeles.htm",
        kind="official", accessed="2026-11-06",
        used="Local CPI-U 12-month change"),
    "S_FRED_DGS10": dict(
        label="10-Year Treasury Constant Maturity (DGS10)",
        publisher="Federal Reserve Board via FRED, Federal Reserve Bank of St. Louis",
        url="https://fred.stlouisfed.org/series/DGS10",
        kind="official", accessed="2026-11-07",
        used="Daily 10-year Treasury constant-maturity yield"),
    "S_TREASURY_YIELD": dict(
        label="Daily Treasury Par Yield Curve Rates, calendar year 2026",
        publisher="U.S. Department of the Treasury",
        url=("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
             "TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026"),
        kind="official", accessed="2026-11-06",
        used="Model discount-rate anchor (10-year par yield, 2026-01-02)"),
    "S_FED_STATEMENT": dict(
        label="FOMC statement, 28 October 2026",
        publisher="Board of Governors of the Federal Reserve System",
        url="https://www.federalreserve.gov/newsevents/pressreleases/monetary20261028a.htm",
        kind="official", accessed="2026-11-07",
        used="Federal funds target range and the vote"),
    "S_ASSESSOR_ROLL": dict(
        label="LA County property values surpass $2.2 trillion (2026 Assessment Roll)",
        publisher="County of Los Angeles / Office of the Assessor",
        url="https://lacounty.gov/2026/07/14/la-county-property-values-surpass-2-2-trillion/",
        kind="official", accessed="2026-11-07",
        used="Assessment roll total, growth, parcel count, median home price, Prop 13 factor"),
    "S_ASSESSOR": dict(
        label="Assessment Roll portal",
        publisher="Los Angeles County Office of the Assessor",
        url="https://assessor.lacounty.gov/news-information/assessmentroll",
        kind="official", accessed="2026-11-06",
        used="Roll documentation"),
    "S_DIR_FF": dict(
        label="Fast Food Minimum Wage Frequently Asked Questions (AB 1228)",
        publisher="California Department of Industrial Relations",
        url="https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm",
        kind="official", accessed="2026-11-07",
        used="Fast-food wage floor, coverage tests, franchisee applicability"),
    "S_DIR_MW": dict(
        label="Minimum Wage Frequently Asked Questions",
        publisher="California Department of Industrial Relations",
        url="https://www.dir.ca.gov/dlse/faq_minimumwage.htm",
        kind="official", accessed="2026-11-07",
        used="State minimum wage schedule 2017-2026"),
    "S_LA_WAGES": dict(
        label="Office of Wage Standards - minimum wage announcements",
        publisher="City of Los Angeles",
        url="https://wagesla.lacity.gov/",
        kind="official", accessed="2026-11-07",
        used="City minimum wage effective 2026-07-01"),
    "S_ULA": dict(
        label="Real Property Transfer Tax and Measure ULA FAQ",
        publisher="City of Los Angeles Office of Finance",
        url="https://finance.lacity.gov/faq/measure-ula",
        kind="official", accessed="2026-11-07",
        used="Measure ULA rates and thresholds, city base transfer tax rate"),
    "S_LAC_RR": dict(
        label="Documentary transfer taxes - general information",
        publisher="LA County Registrar-Recorder/County Clerk",
        url=("https://www.lavote.gov/home/recorder/property-document-recording/"
             "documentary-transfer-taxes/general-info"),
        kind="official", accessed="2026-11-06",
        used="County documentary transfer tax rate"),
    "S_IRS_1031": dict(
        label="Like-kind exchanges under IRC §1031",
        publisher="Internal Revenue Service",
        url="https://www.irs.gov/newsroom/like-kind-exchanges-under-irc-code-section-1031",
        kind="official", accessed="2026-11-06",
        used="45-day identification and 180-day completion periods"),
    "S_IRS_409": dict(
        label="Topic no. 409, Capital gains and losses",
        publisher="Internal Revenue Service",
        url="https://www.irs.gov/taxtopics/tc409",
        kind="official", accessed="2026-11-06",
        used="Long-term capital gains and unrecaptured §1250 rates"),
    "S_SOS_MEASURES": dict(
        label="Qualified Statewide Ballot Measures (November 3, 2026)",
        publisher="California Secretary of State",
        url="https://www.sos.ca.gov/elections/ballot-measures/qualified-ballot-measures",
        kind="official", accessed="2026-11-07",
        used="Certified proposition list and titles"),
    "S_SOS_PROP40": dict(
        label="Proposition 40 - official voter guide",
        publisher="California Secretary of State",
        url="https://voterguide.sos.ca.gov/propositions/40/index.htm",
        kind="official", accessed="2026-11-07",
        used="One-time 5% tax on taxpayers with assets over $1 billion"),
    "S_USGS_FAQ": dict(
        label="What is the probability that an earthquake will occur in the Los Angeles area?",
        publisher="U.S. Geological Survey",
        url=("https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-"
             "los-angeles-area-san-francisco-bay-area"),
        kind="official", accessed="2026-11-06",
        used="30-year earthquake probabilities (UCERF3)"),
    "S_USGS_SHAKEOUT": dict(
        label="The ShakeOut earthquake scenario (Open-File Report 2008-1150)",
        publisher="U.S. Geological Survey",
        url="https://pubs.usgs.gov/of/2008/1150/",
        kind="official", accessed="2026-11-06",
        used="Modelled losses for a M7.8 southern San Andreas event"),
    "S_LA_FIRES": dict(
        label="Key facts about the Eaton and Palisades Fires (anniversary fact sheet)",
        publisher="County of Los Angeles",
        url=("https://file.lacounty.gov/SDSInter/lac/"
             "1199046_Eaton_Palisades_Fires_Anniversary_Fact_Sheet.pdf"),
        kind="official", accessed="2026-11-06",
        used="Acreage, structures, economic output, business and worker impacts"),
    "S_CALFIRE_FHSZ": dict(
        label="Fire Hazard Severity Zones",
        publisher="CAL FIRE - Office of the State Fire Marshal",
        url=("https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-"
             "mitigation/fire-hazard-severity-zones"),
        kind="official", accessed="2026-11-06",
        used="State Responsibility Area zone classes"),
    "S_CRS": dict(
        label="In Focus IF12871: January 2025 Los Angeles County wildfires",
        publisher="Congressional Research Service (via congress.gov)",
        url="https://www.congress.gov/crs-product/IF12871",
        kind="official", accessed="2026-11-06",
        used="Post-fire insurance moratorium, federal context"),
    "S_CDE": dict(
        label="Four-year adjusted cohort graduation rate, 2024-25",
        publisher="California Department of Education",
        url="https://www.cde.ca.gov/ds/cm/dqeoy25.asp",
        kind="official", accessed="2026-11-06",
        used="Statewide graduation rate"),
    "S_DASHBOARD": dict(
        label="California School Dashboard - Los Angeles Unified",
        publisher="California Department of Education",
        url="https://www.caschooldashboard.org/reports/19647330000000/2025/academic-engagement",
        kind="official", accessed="2026-11-06",
        used="District graduation rate"),
    "S_JIB_10K": dict(
        label="Jack in the Box Inc., Form 10-K for the fiscal year ended 2025-09-28",
        publisher="Jack in the Box Inc. (SEC EDGAR)",
        url="https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm",
        kind="issuer", accessed="2026-11-07",
        used="Restaurant counts, lease terms, closure programme, prototype, geography"),
    "S_JIB_Q4": dict(
        label="Jack in the Box Inc., Q4 and full-year 2025 earnings release (Exhibit 99.1)",
        publisher="Jack in the Box Inc. (SEC EDGAR)",
        url=("https://www.sec.gov/Archives/edgar/data/807882/000080788225000070/"
             "ex991-q425earningsrelease.htm"),
        kind="issuer", accessed="2026-11-07",
        used="Same-store sales, openings, closures, JACK on Track closures, unit counts"),
    "S_JIB_10Q": dict(
        label="Jack in the Box Inc., Form 10-Q for the period ended 2026-07-05",
        publisher="Jack in the Box Inc. (SEC EDGAR)",
        url="https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/jack-20260705.htm",
        kind="issuer", accessed="2026-11-06 (index re-checked 2026-11-07)",
        used="Q3 FY2026 restaurant counts, same-store sales"),
    "S_BOULDER": dict(
        label="Net Lease Research Report, Q3 2026",
        publisher="The Boulder Group (private research firm)",
        url="https://www.bouldergroup.com/media/pdf/2026-Q3-Net-Lease-Research-Report.pdf",
        kind="industry", accessed="2026-11-06",
        used="Net-lease cap rates - NON-OFFICIAL, shown separately and never scored as verified"),
}

# ---------------------------------------------------------------------------
# 2. ROW OVERRIDES
#    Corrections applied during the line-by-line integration review.  Each entry
#    states what changed and why; nothing is silently rewritten.
# ---------------------------------------------------------------------------
OVERRIDES = {
    # Value corrected: the official certified list carries 14 propositions, not 15.
    "REG-04": dict(
        value="14", metric="Statewide measures certified for the November 3, 2026 ballot",
        status="verified-now", src="S_SOS_MEASURES",
        note="CORRECTED during integration: the previous layer published 15. "
             "Counting the certified list (1-5 and 37-45) gives 14."),
    # Revision drift: BLS revised the August 2026 nonfarm level.
    "LAB-05": dict(
        value="6,282.6", period="Aug 2026 (prelim.)", status="verified-now", src="S_BLS_EAG",
        note="REVISED during integration: 6,289.1 (decision-file layer) and 6,282.1 "
             "(analysis layer) both precede the current published value of 6,282.6."),
    # Source attribution corrected: the federal funds rate is not published by a
    # private research firm, and the October decision was a hold, not an increase.
    "RATE-04": dict(
        value="3.75-4.00", period="28 Oct 2026 (FOMC decision)", status="verified-now",
        src="S_FED_STATEMENT",
        note="CORRECTED during integration: source re-attributed to the FOMC statement "
             "and the label changed from 'after September 2026 increase' to 'hold, 10-2 vote'."),
    # Measure ULA: flagged in the previous layer because a deep link 404'd.  The
    # official FAQ is live and states both rates and thresholds.
    "TAX-04": dict(
        value="4", status="verified-now", src="S_ULA",
        note="UPGRADED from flagged to verified: read on the City of Los Angeles Office "
             "of Finance Measure ULA FAQ. Applies to conveyances over $5,400,000 and "
             "under $10,900,000."),
    "TAX-05": dict(
        value="5.5", status="verified-now", src="S_ULA",
        note="UPGRADED from flagged to verified: reads 5.5% for conveyances of "
             "$10,900,000 or more on the official Measure ULA FAQ."),
    "TAX-01": dict(status="source-linked"),
    "TAX-03": dict(status="analysis", note="Arithmetic: city base 0.45% + county 0.11%."),
    "RATE-02": dict(src="S_BLS_CPI", status="source-linked"),
    "RATE-03": dict(src="S_BLS_CPI", status="source-linked"),
    "DEM-01": dict(src="S_CENSUS_CO", status="source-linked"),
    "DEM-02": dict(src="S_CENSUS_CO", status="source-linked"),
    "DEM-03": dict(src="S_CENSUS_CO", status="source-linked"),
    "INC-01": dict(src="S_CENSUS_CO", status="source-linked"),
    "INC-03": dict(src="S_CENSUS_CO", status="source-linked"),
    "INC-05": dict(src="S_CENSUS_CO", status="source-linked"),
    "INC-06": dict(src="S_CENSUS_CITY", status="source-linked"),
    "LAB-21": dict(src="S_CENSUS_CO", status="source-linked"),
    "LAB-22": dict(src="S_CENSUS_CO", status="source-linked"),
    "LAB-23": dict(src="S_CENSUS_CO", status="source-linked"),
    "LAB-24": dict(src="S_CENSUS_CO", status="source-linked"),
    "LAB-25": dict(src="S_CENSUS_CO", status="source-linked"),
    "LAB-26": dict(src="S_CENSUS_CO", status="source-linked"),
    "LAB-27": dict(src="S_CENSUS_CO", status="source-linked"),
    "LAB-01": dict(status="verified-now", src="S_BLS_EAG"),
    "LAB-02": dict(status="verified-now", src="S_BLS_EAG"),
    "LAB-03": dict(status="verified-now", src="S_BLS_EAG"),
    "LAB-04": dict(status="verified-now", src="S_BLS_EAG"),
    "RATE-01": dict(status="verified-now", src="S_FRED_DGS10"),
    "INC-07": dict(status="verified-now", src="S_CENSUS_CO"),
    "INC-08": dict(status="verified-now", src="S_CENSUS_CO"),
    "INC-09": dict(status="verified-now", src="S_CENSUS_CO"),
    "INC-10": dict(status="verified-now", src="S_CENSUS_CO"),
    "INC-11": dict(status="verified-now", src="S_CENSUS_CO"),
    "INC-12": dict(status="verified-now", src="S_CENSUS_CO"),
    "INC-13": dict(status="verified-now", src="S_CENSUS_CO"),
    "PROP-01": dict(status="verified-now", src="S_ASSESSOR_ROLL", value="2.272",
                     note="Read as '$2.272 trillion in total net taxable value'."),
    "PROP-02": dict(status="verified-now", src="S_ASSESSOR_ROLL"),
    "PROP-03": dict(status="verified-now", src="S_ASSESSOR_ROLL"),
    "PROP-04": dict(status="verified-now", src="S_ASSESSOR_ROLL"),
    "PROP-05": dict(status="verified-now", src="S_ASSESSOR_ROLL"),
    "PROP-06": dict(status="verified-now", src="S_ASSESSOR_ROLL"),
    "PROP-07": dict(status="verified-now", src="S_ASSESSOR_ROLL"),
    "PROP-08": dict(status="verified-now", src="S_ASSESSOR_ROLL"),
    "REG-01": dict(status="verified-now", src="S_DIR_FF"),
    "REG-02": dict(status="verified-now", src="S_DIR_MW"),
    "REG-03": dict(status="verified-now", src="S_LA_WAGES"),
    "REG-05": dict(status="verified-now", src="S_SOS_MEASURES"),
    "REG-06": dict(status="verified-now", src="S_SOS_PROP40"),
    "TEN-01": dict(status="verified-now", src="S_JIB_Q4"),
    "TEN-04": dict(status="verified-now", src="S_JIB_Q4"),
    "TEN-05": dict(status="verified-now", src="S_JIB_Q4"),
    "TEN-06": dict(status="verified-now", src="S_JIB_Q4"),
    "TEN-07": dict(status="verified-now", src="S_JIB_Q4"),
    "TEN-12": dict(status="verified-now", src="S_JIB_Q4"),
    "TEN-08": dict(status="verified-now", src="S_JIB_Q4"),
}

SRC_MAP = {
    "S01": "S_BLS_EAG", "S02": "S_CENSUS_CO", "S03": "S_CENSUS_CITY",
    "S04": "S_FRED_DGS10", "S05": "S_ASSESSOR_ROLL", "S06": "S_ASSESSOR",
    "S07": "S_USGS_SHAKEOUT", "S08": "S_CALFIRE_FHSZ", "S09": "S_CDE",
    "S10": "S_DASHBOARD", "S11": "S_DIR_FF", "S12": "S_DIR_MW", "S13": "S_LA_WAGES",
    "S14": "S_LAC_RR", "S15": "S_IRS_1031", "S16": "S_IRS_409",
    "S17": "S_SOS_MEASURES", "S18": "S_SOS_PROP40", "S19": "S_LA_FIRES",
    "S20": "S_CRS", "S21": "S_JIB_10K", "S22": "S_JIB_Q4", "S24": "S_BOULDER",
    "S25": "S_BOULDER", "S26": "S_BOULDER", "S28": "S_ULA",
}

# Rows whose source is a private research firm are reclassified as industry data
# and kept out of the official evidence table.
INDUSTRY_OVERRIDE = {"MKT-01", "MKT-02", "MKT-03", "MKT-04", "MKT-05", "MKT-06",
                     "MKT-07", "MKT-08", "RATE-04_OLD"}

VERIFIED_NOTES = {
    "LAB-01": "BLS table read 2026-11-07: Sept 2026 preliminary 6,646.9 thousand.",
    "LAB-02": "BLS table read 2026-11-07: Sept 2026 preliminary 6,352.9 thousand.",
    "LAB-03": "BLS table read 2026-11-07: Sept 2026 preliminary 294.0 thousand.",
    "LAB-04": "BLS table read 2026-11-07: Sept 2026 preliminary 4.4%.",
    "INC-07": "QuickFacts county read 2026-11-07: median gross rent $1,954.",
    "INC-08": "QuickFacts county read 2026-11-07: median value $834,200.",
    "INC-09": "QuickFacts county read 2026-11-07: 45.9%.",
    "INC-10": "QuickFacts county read 2026-11-07: 22,250 permits (2025).",
    "INC-11": "QuickFacts county read 2026-11-07: 36.0%.",
    "INC-12": "QuickFacts county read 2026-11-07: 80.9%.",
    "INC-13": "QuickFacts county read 2026-11-07: 55.1%.",
    "RATE-01": "FRED DGS10 read 2026-11-07: 4.90 on 2026-11-04.",
    "PROP-01": "Assessor release read 2026-11-07: $2.272 trillion.",
    "PROP-02": "Assessor release read 2026-11-07: 4.42%.",
    "PROP-04": "Assessor release read 2026-11-07: 2,399,978 parcels.",
    "PROP-05": "Assessor release read 2026-11-07: $982,000.",
    "PROP-06": "Assessor release read 2026-11-07: 16th consecutive year.",
    "PROP-07": "Assessor release read 2026-11-07: more than $27 billion.",
    "PROP-08": "Assessor release read 2026-11-07: 2% maximum inflation factor applied.",
    "REG-01": "DIR FAQ read 2026-11-07: $20.00/hour from 2024-04-01, applies to franchisees.",
    "REG-02": "DIR FAQ read 2026-11-07: $16.90/hour from 2026-01-01.",
    "REG-03": "City of LA read 2026-11-07: $18.42 effective 2026-07-01.",
    "REG-04": "SOS list read 2026-11-07: 14 propositions (1-5 and 37-45).",
    "REG-06": "SOS voter guide read 2026-11-07: 5% one-time tax above $1 billion of assets.",
    "TAX-04": "City Office of Finance FAQ read 2026-11-07.",
    "TAX-05": "City Office of Finance FAQ read 2026-11-07.",
    "TEN-01": "Q4 FY2025 release read 2026-11-07: 2,136 restaurants at FY2025 year end.",
    "TEN-04": "Q4 FY2025 release read 2026-11-07: 31 openings in fiscal 2025.",
    "TEN-05": "Q4 FY2025 release read 2026-11-07: 86 closures in fiscal 2025.",
    "TEN-06": "Q4 FY2025 release read 2026-11-07: system (7.4)% in Q4.",
    "TEN-07": "Q4 FY2025 release read 2026-11-07: system (4.2)% for FY2025.",
    "TEN-08": "Q4 FY2025 release read 2026-11-07: systemwide sales (7.2)% in Q4.",
    "TEN-12": "Q4 FY2025 release read 2026-11-07: 38 of 47 closures were JACK on Track.",
}

# Rows added by this integration because they are decision-critical and were
# verified here (or are new authoritative observations).
EXTRA_ROWS = [
    dict(id="POP-CITY-01", cat="Demographics",
         metric="Population, July 1, 2025 (V2025)", value="3,869,089", unit="persons",
         period="2025-07-01", geo="Los Angeles city", src="S_CENSUS_CITY",
         status="verified-now", note="QuickFacts city read 2026-11-07."),
    dict(id="POP-CITY-02", cat="Demographics",
         metric="Population change, 2020 estimates base to 2025", value="-0.8", unit="%",
         period="2020-2025", geo="Los Angeles city", src="S_CENSUS_CITY",
         status="verified-now", note="QuickFacts city read 2026-11-07."),
    dict(id="POP-CITY-03", cat="Demographics",
         metric="Population estimates base, April 1, 2020", value="3,899,342", unit="persons",
         period="2020-04-01", geo="Los Angeles city", src="S_CENSUS_CITY",
         status="verified-now", note="QuickFacts city read 2026-11-07."),
    dict(id="RATE-05", cat="Prices & Rates",
         metric="10-Year Treasury constant maturity yield, latest observation",
         value="4.84", unit="%", period="2026-11-05", geo="United States",
         src="S_FRED_DGS10", status="verified-now",
         note="FRED DGS10 read 2026-11-07: 4.84 (2026-11-05), 4.90 (2026-11-04)."),
    dict(id="TAX-10", cat="Transaction Costs & Tax",
         metric="Measure ULA threshold, lower tier", value="5,400,000", unit="USD",
         period="closings after 2026-06-30", geo="Los Angeles city", src="S_ULA",
         status="verified-now", note="Read on the official Measure ULA FAQ 2026-11-07."),
    dict(id="TAX-11", cat="Transaction Costs & Tax",
         metric="Measure ULA threshold, upper tier", value="10,900,000", unit="USD",
         period="closings after 2026-06-30", geo="Los Angeles city", src="S_ULA",
         status="verified-now", note="Read on the official Measure ULA FAQ 2026-11-07."),
    dict(id="TAX-12", cat="Transaction Costs & Tax",
         metric="Combined city base + ULA rate at $5.4M-$10.9M", value="4.45", unit="% of price",
         period="closings after 2026-06-30", geo="Los Angeles city", src="S_ULA",
         status="verified-now",
         note="Official FAQ publishes the combined 4.45% rate; 5.95% at $10.9M or more."),
    dict(id="TEN-16", cat="Tenant",
         metric="Jack in the Box same-store sales, Q3 FY2026 (system)", value="-1.1", unit="%",
         period="Q3 FY2026 (12 weeks to 2026-07-05)", geo="System", src="S_JIB_10Q",
         status="source-linked",
         note="Read from the Q3 FY2026 10-Q/earnings exhibit by the originating session; "
              "filing index confirmed present on EDGAR 2026-11-07. Not re-read line by line here."),
    dict(id="TEN-17", cat="Tenant",
         metric="Jack in the Box restaurants at 2026-07-05", value="2,115", unit="restaurants",
         period="Q3 FY2026", geo="System", src="S_JIB_10Q", status="source-linked",
         note="Filing index confirmed 2026-11-07; value read by the originating session."),
    dict(id="TEN-18", cat="Tenant",
         metric="Disclosed block-closure programme ('JACK on Track')", value="150-200",
         unit="restaurants", period="announced 2025-04-23", geo="System", src="S_JIB_10K",
         status="source-linked",
         note="The 10-K states remaining closures occur based on respective franchise "
              "agreement termination dates; target sites are largely in the system over "
              "three decades. Quoted, not paraphrased, in the tenant page."),
    dict(id="LEASE-01", cat="Lease & tenant disclosures",
         metric="Initial lease term, the company's restaurant leases",
         value="generally 20 years", unit="term", period="FY2025 10-K", geo="Company leases",
         src="S_JIB_10K", status="source-linked",
         note="Excludes renewal options. The owner's own lease was not supplied."),
    dict(id="LEASE-02", cat="Lease & tenant disclosures",
         metric="Renewal options", value="1-20 years, generally at the company's sole discretion",
         unit="option", period="FY2025 10-K", geo="Company leases", src="S_JIB_10K",
         status="source-linked",
         note="If the owner's lease mirrors this, renewal is the tenant's choice, not the owner's."),
    dict(id="LEASE-03", cat="Lease & tenant disclosures",
         metric="Leases carrying contingent (percentage) rent", value="about 13", unit="% of leases",
         period="FY2025 10-K", geo="Company leases", src="S_JIB_10K", status="source-linked",
         note="Contingent rent disclosed at 1% to 10% of gross sales."),
    dict(id="LEASE-04", cat="Lease & tenant disclosures",
         metric="Development cost per new restaurant, excluding land",
         value="1.3-1.9", unit="USD million", period="FY2025 10-K", geo="Company",
         src="S_JIB_10K", status="source-linked",
         note="Replacement-cost context for insurance adequacy."),
    dict(id="HAZ-16", cat="Hazard & Risk",
         metric="Probability of M6.7 or greater, Los Angeles region, next 30 years",
         value="60", unit="% probability", period="30-year window", geo="Los Angeles region",
         src="S_USGS_FAQ", status="source-linked",
         note="USGS (UCERF3) FAQ. M6.7 is roughly the 1994 Northridge magnitude."),
    dict(id="HAZ-17", cat="Hazard & Risk",
         metric="Probability of M7.0 or greater, Los Angeles region, next 30 years",
         value="46", unit="% probability", period="30-year window", geo="Los Angeles region",
         src="S_USGS_FAQ", status="source-linked", note="USGS (UCERF3) FAQ."),
    dict(id="HAZ-18", cat="Hazard & Risk",
         metric="Probability of M7.5 or greater, Los Angeles region, next 30 years",
         value="31", unit="% probability", period="30-year window", geo="Los Angeles region",
         src="S_USGS_FAQ", status="source-linked", note="USGS (UCERF3) FAQ."),
    dict(id="LAB-28", cat="Labor Market",
         metric="Civilian labour force, September 2025 (year-earlier comparison)",
         value="6,768,502", unit="persons", period="Sept 2025", geo="LA-Long Beach-Anaheim MSA",
         src="S_BLS_EAG", status="source-linked",
         note="Year-earlier level used for the comparison; read by the originating session from BLS "
              "series LAUMT063108000000006. The public page shows the latest six months only."),
    dict(id="LAB-29", cat="Labor Market",
         metric="Unemployment rate, September 2025 (year-earlier comparison)", value="5.5",
         unit="%", period="Sept 2025", geo="LA-Long Beach-Anaheim MSA", src="S_BLS_EAG",
         status="source-linked",
         note="Year-earlier rate. The fall from 5.5% to 4.4% coincided with a shrinking labour force."),
]

# Values that cannot be confirmed from an official source.  They are BLANK on the
# site and published on the Flagged for Review page.
# (analysis dataset rows with status 'flagged' that were not upgraded are blanked
# automatically by the loader.)

INPUT_ROWS = [
    dict(id="I-01", field="Street address", why="Identifies the parcel; withheld by the privacy directive."),
    dict(id="I-02", field="Assessor Parcel Number (APN)", why="Needed for zoning, hazard-zone and tax lookups."),
    dict(id="I-03", field="Community plan area / council district", why="Determines permitted uses after vacancy."),
    dict(id="I-04", field="Lot size and building size (sq ft)", why="Replacement cost, re-letting and redevelopment."),
    dict(id="I-05", field="Year built / year renovated", why="Capital-reserve and insurance underwriting."),
    dict(id="I-06", field="Current base rent and escalation schedule", why="Converts the R-normalised model into dollars."),
    dict(id="I-07", field="Lease commencement and exact expiry date", why="The 2030-2035 window is a 5-year range, not a date."),
    dict(id="I-08", field="Renewal option terms and notice deadlines", why="Establishes whether renewal is the owner's or the tenant's choice."),
    dict(id="I-09", field="Guaranty (corporate or franchisee only)", why="Determines what survives a tenant failure."),
    dict(id="I-10", field="Percentage-rent clause, if any", why="Would share sales downside with the owner."),
    dict(id="I-11", field="Purchase price, date and adjusted cost basis", why="Required for after-tax sale proceeds and recapture."),
    dict(id="I-12", field="Existing debt, rate, maturity and prepayment terms", why="A sale may trigger defeasance or yield maintenance."),
    dict(id="I-13", field="Entity type and state residency", why="Determines the tax rate applied to a sale."),
    dict(id="I-14", field="Current insurance: carrier, limit, deductible", why="The dominant black-swan exposure under NNN."),
    dict(id="I-15", field="Whether the site is inside the tenant's closure programme", why="The single highest-value, zero-cost question."),
]

CATEGORY_ORDER = [
    "Demographics", "Income & Housing", "Labor Market", "Prices & Rates",
    "Property Tax & Valuation", "Transaction Costs & Tax", "Lease & tenant disclosures",
    "Tenant", "Hazard & Risk", "Regulation", "Education",
]

STATUS_LABELS = {
    "verified-now": ("Verified", "Re-read on the official source during integration on " + READ_DATE),
    "source-linked": ("Source-linked", "Official or primary source linked; read when first captured, not re-read today"),
    "analysis": ("Analysis", "Arithmetic or judgement built on the cited evidence"),
    "industry": ("Industry - not official", "Private research firm; NOT an official source and never scored as verified"),
    "unverified": ("Unverified - blank", "No official source could be confirmed; value withheld"),
    "input": ("Input required", "Owner must supply; cannot be researched from public sources"),
}


# ---------------------------------------------------------------------------
# 3. LOADER
# ---------------------------------------------------------------------------
def _load_base_rows():
    path = os.path.join(ROOT, "analysis", "data", "dataset.json")
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    rows = []
    for r in data["rows"]:
        status = r["status"]
        if status == "verified":
            status = "source-linked"
        elif status == "verified-industry":
            status = "industry"
        elif status == "calculated":
            status = "analysis"
        elif status == "flagged":
            status = "unverified"
        row = dict(id=r["id"], cat=r["cat"], metric=r["metric"], value=r["value"],
                   unit=r.get("unit", ""), period=r.get("period", ""), geo=r.get("geo", ""),
                   src=SRC_MAP.get(r.get("src", ""), r.get("src", "")), status=status, note="")
        if r["id"] in INDUSTRY_OVERRIDE:
            row["status"] = "industry"
            row["src"] = "S_BOULDER"
        if r["id"] in OVERRIDES:
            row.update(OVERRIDES[r["id"]])
        if r["id"] in VERIFIED_NOTES and not row.get("note"):
            row["note"] = VERIFIED_NOTES[r["id"]]
        rows.append(row)
    return rows


def _merge_extra(rows):
    have = {r["id"] for r in rows}
    for r in EXTRA_ROWS:
        if r["id"] not in have:
            rows.append(dict(r))
    return rows


def all_rows():
    rows = _merge_extra(_load_base_rows())
    order = {c: i for i, c in enumerate(CATEGORY_ORDER)}
    rows.sort(key=lambda r: (order.get(r["cat"], 99), r["id"]))
    for r in rows:
        if r["status"] in ("unverified", "input"):
            r["display_value"] = ""
        else:
            r["display_value"] = _format(r)
    return rows


DISPLAY_OVERRIDES = {
    "REG-05": "None on the certified list",
    "MKT-08": "Financing costs generally exceed cap rates",
    "TEN-12": "38 of 47",
    "PROP-01": "$2.272 trillion",
    "PROP-03": "$96 billion",
    "PROP-07": "more than $27 billion",
    "INC-07": "$1,954/month",
}

THOUSAND_UNITS = {"thousands": "thousand", "thousands of jobs": "thousand jobs"}


def _format(r):
    rid = r.get("id")
    if rid in DISPLAY_OVERRIDES:
        return DISPLAY_OVERRIDES[rid]
    v = str(r["value"]).strip()
    if v in ("None", "", "None on the certified list"):
        return ""
    unit = str(r.get("unit", "")).strip()
    if not unit:
        return v
    if unit == "%":
        return f"{v}%"
    if unit.startswith("%"):
        return f"{v}{unit}"
    if unit.startswith("USD"):
        rest = unit[3:]
        return f"${v}{rest}"
    if unit in THOUSAND_UNITS:
        return f"{v} {THOUSAND_UNITS[unit]}"
    return f"{v} {unit}"


def rows_for(cat):
    return [r for r in all_rows() if r["cat"] == cat]


def official_rows():
    return [r for r in all_rows() if r["status"] in ("verified-now", "source-linked")]


def industry_rows():
    return [r for r in all_rows() if r["status"] == "industry"]


def counts():
    rows = all_rows()
    return {
        "total": len(rows),
        "verified-now": sum(1 for r in rows if r["status"] == "verified-now"),
        "source-linked": sum(1 for r in rows if r["status"] == "source-linked"),
        "analysis": sum(1 for r in rows if r["status"] == "analysis"),
        "industry": sum(1 for r in rows if r["status"] == "industry"),
        "unverified": sum(1 for r in rows if r["status"] == "unverified"),
        "sources": len(SOURCES),
        "official_sources": sum(1 for s in SOURCES.values() if s["kind"] in ("official", "issuer")),
    }


# ---------------------------------------------------------------------------
# 4. RISK REGISTER (analysis; each row cites the evidence it rests on)
# ---------------------------------------------------------------------------
RISKS = [
    dict(id="R-01", kind="Business as usual", cat="Tenant continuity",
         risk="The tenant's brand operator is running a disclosed 150-200 restaurant closure "
              "programme whose remaining closures are timed to franchise-agreement termination dates.",
         l=4, i=5, evidence="10-K FY2025; Q4 FY2025 release; Q3 FY2026 10-Q", src="S_JIB_Q4",
         mitigation="Ask the tenant in writing whether the site is inside the programme before "
                    "spending anything on renewal capital."),
    dict(id="R-02", kind="Business as usual", cat="Tenant credit",
         risk="System same-store sales have declined in every recent reporting period "
              "(-4.2% FY2025, -1.1% Q3 FY2026), driven by lower transactions.",
         l=5, i=4, evidence="Q4 FY2025 release; Q3 FY2026 10-Q", src="S_JIB_Q4",
         mitigation="Underwrite renewal on transactions, not menu price. Assume rent concessions "
                    "are requested."),
    dict(id="R-03", kind="Business as usual", cat="Tenant credit",
         risk="Franchisee-level margin pressure (food and packaging costs rising) reduces the "
              "operator's ability and willingness to pay rent at renewal.",
         l=4, i=4, evidence="10-K FY2025", src="S_JIB_10K",
         mitigation="Confirm whether the lease is guaranteed by the corporate parent."),
    dict(id="R-04", kind="Business as usual", cat="Operating cost",
         risk="A statutory wage floor of $20.00/hour for fast-food employees applies to "
              "franchisees as well as the brand owner, and the City general minimum wage is $18.42.",
         l=5, i=3, evidence="DIR FAQs; City of Los Angeles", src="S_DIR_FF",
         mitigation="Cannot be mitigated by the owner; it is a fixed cost on the tenant. Treat "
                    "as a permanent margin headwind at renewal."),
    dict(id="R-05", kind="Business as usual", cat="Rollover / vacancy",
         risk="If the tenant vacates at expiry, a specialised single-tenant drive-thru box may "
              "take a year or more to re-let, at re-tenanting capital.",
         l=3, i=5, evidence="Lease disclosures; model assumptions", src="S_JIB_10K",
         mitigation="Start marketing or re-leasing early; price the downtime into any hold decision."),
    dict(id="R-06", kind="Business as usual", cat="Market / demand",
         risk="Los Angeles County population is below its 2020 estimates base (-3.2%), and the "
              "city is -0.8%.",
         l=5, i=3, evidence="Census QuickFacts V2025", src="S_CENSUS_CO",
         mitigation="Underwrite to measurement, not to forecast growth. Test trade-area data "
                    "before assuming local growth."),
    dict(id="R-07", kind="Business as usual", cat="Market / demand",
         risk="Official long-range projections disagree on the direction of travel for the same "
              "county (SCAG growth vs Department of Finance decline).",
         l=5, i=4, evidence="SCAG; CA DOF; City of LA plan", src="S_CENSUS_CO",
         mitigation="Do not capitalise a growth forecast into the decision. Treat growth as upside."),
    dict(id="R-08", kind="Business as usual", cat="Employment",
         risk="Metro employment growth is weak (+0.6% y/y) and unevenly distributed; information "
              "and manufacturing are contracting.",
         l=4, i=3, evidence="BLS Economy at a Glance", src="S_BLS_EAG",
         mitigation="Monitor the leisure and hospitality sector, which is the tenant's own sector."),
    dict(id="R-09", kind="Business as usual", cat="Employment",
         risk="The labour force is shrinking while the unemployment rate falls; a falling rate "
              "is not, on its own, an expanding economy.",
         l=4, i=3, evidence="BLS Economy at a Glance", src="S_BLS_EAG",
         mitigation="Publish the rate and the labour force together; never cite the rate alone."),
    dict(id="R-10", kind="Business as usual", cat="Inflation",
         risk="Local CPI is running at 3.7% and energy costs are rising faster, squeezing "
              "discretionary drive-thru spending.",
         l=4, i=3, evidence="BLS CPI, Los Angeles", src="S_BLS_CPI",
         mitigation="Check that the lease escalation actually offsets inflation."),
    dict(id="R-11", kind="Business as usual", cat="Valuation",
         risk="No U.S. government agency publishes commercial cap rates or single-tenant "
              "comparables, so value cannot be officially verified.",
         l=5, i=4, evidence="Absence of an official publisher (documented)", src="S_BOULDER",
         mitigation="Negotiate from a sensitivity band, not a point cap rate; obtain two "
                    "independent broker opinions before pricing."),
    dict(id="R-12", kind="Business as usual", cat="Tax / transaction",
         risk="A sale crystallises capital-gains and depreciation-recapture tax plus transfer "
              "taxes and Measure ULA where applicable.",
         l=5, i=3, evidence="IRS; City of Los Angeles", src="S_IRS_409",
         mitigation="Model a §1031 exchange; confirm eligibility and timing before listing."),
    dict(id="R-13", kind="Business as usual", cat="Governance",
         risk="Tenant leadership turnover and strategic repositioning can change site-level "
              "commitment.",
         l=3, i=2, evidence="SEC filings", src="S_JIB_10K",
         mitigation="Monitor filings; do not rely on verbal assurances."),
    dict(id="R-14", kind="Business as usual", cat="Analysis integrity",
         risk="The subject property was never identified, so every site-specific conclusion is "
              "conditional.",
         l=5, i=5, evidence="Anonymisation boundary (privacy directive)", src="S_CENSUS_CO",
         mitigation="Complete the Input Register before committing capital to any strategy."),
    dict(id="R-15", kind="Business as usual", cat="Opportunity cost",
         risk="Holding concentrates wealth in one illiquid single-tenant, single-county asset.",
         l=4, i=4, evidence="Portfolio reasoning (analysis)", src="S_FRED_DGS10",
         mitigation="Size the position against total net worth; consider partial diversification "
                    "via a §1031 exchange."),
    dict(id="B-01", kind="Black swan", cat="Wildfire",
         risk="A wind-driven wildfire destroys the trade area. The January 2025 Eaton and "
              "Palisades fires burned 14,021 and 23,448 acres and destroyed 9,414 and 6,837 "
              "structures, removing an estimated $5.2-10.1 billion of output.",
         l=2, i=5, evidence="County of Los Angeles fact sheet; CRS IF12871", src="S_LA_FIRES",
         mitigation="Confirm the tenant maintains full replacement-cost insurance and that the "
                    "owner is named; check the parcel's Fire Hazard Severity Zone."),
    dict(id="B-02", kind="Black swan", cat="Earthquake",
         risk="A major earthquake. USGS puts 30-year probabilities for the Los Angeles region at "
              "60% (M6.7+), 46% (M7.0+) and 31% (M7.5+).",
         l=3, i=5, evidence="USGS UCERF3; ShakeOut scenario", src="S_USGS_FAQ",
         mitigation="Verify seismic insurance and deductibles; a long hold adds exposure that no "
                    "rent escalation compensates."),
    dict(id="B-03", kind="Black swan", cat="Tenant failure",
         risk="A brand-level failure or accelerated closure wave; the system has already shrunk "
              "from 2,191 units (FY2024) to 2,136 (FY2025) and 2,115 (Q3 FY2026).",
         l=2, i=5, evidence="10-K FY2025; Q4 FY2025 release; Q3 FY2026 10-Q", src="S_JIB_Q4",
         mitigation="Corporate guaranty, security deposit, and early-warning lease covenants."),
    dict(id="B-04", kind="Black swan", cat="Flood / debris flow",
         risk="Post-fire debris flow or riverine flooding; insurance availability and cost change "
              "sharply after a wildfire season.",
         l=2, i=4, evidence="CRS IF12871 (post-fire insurance moratorium)", src="S_CRS",
         mitigation="Check FEMA flood zone and the post-fire moratorium status before renewal."),
    dict(id="B-05", kind="Black swan", cat="Extreme heat",
         risk="Sustained extreme heat suppresses drive-thru and dine-in traffic and raises "
              "refrigeration energy cost.",
         l=3, i=3, evidence="Seasonal consumption pattern (analysis)", src="S_BLS_CPI",
         mitigation="Diversify tenant mix; ensure HVAC and refrigeration capital obligations are "
                    "assigned to the tenant."),
    dict(id="B-06", kind="Black swan", cat="Out-migration",
         risk="Out-migration accelerates beyond official projections, compounding the measured "
              "-3.2% county decline.",
         l=2, i=4, evidence="Census V2025; CA DOF", src="S_CENSUS_CO",
         mitigation="Monitor annual Census estimates; set a review trigger at a further 1% decline."),
    dict(id="B-07", kind="Black swan", cat="Insurance",
         risk="Insurer withdrawal from California commercial property makes coverage unavailable "
              "or unaffordable, transferring the risk to the owner under NNN.",
         l=3, i=5, evidence="CRS IF12871; California insurance market conditions", src="S_CRS",
         mitigation="Require proof of insurance annually; negotiate a lease covenant that makes "
                    "non-renewal a default."),
]

# ---------------------------------------------------------------------------
# 5. FLAGGED FOR REVIEW (merged from every prior layer, de-duplicated)
# ---------------------------------------------------------------------------
FLAGS = [
    dict(id="F-01", sev="High", status="Input required",
         item="Property identity and lease economics",
         detail="No address, parcel number, community plan area, lot or building size, year built, "
                "purchase price, cost basis, current base rent, escalation schedule, option terms, "
                "guaranty or debt terms were supplied. They are not publicly researchable without "
                "identifying the property, which the privacy directive forbids.",
         action="Owner supplies the lease and closing statement privately. Until then all "
                "site-specific figures stay blank and the model runs in rent units (R)."),
    dict(id="F-02", sev="High", status="No official source",
         item="Commercial cap rates and single-tenant comparables",
         detail="No U.S. government agency publishes commercial capitalisation rates or net-lease "
                "comparables. The only figures available come from private research firms and are "
                "labelled industry data on this site, never verified.",
         action="Obtain two independent broker opinions and a lender appraisal; treat the cap "
                "rate as a sensitivity band."),
    dict(id="F-03", sev="Medium", status="Unverified",
         item="FEMA National Risk Index values for Los Angeles County",
         detail="Expected Annual Loss and composite risk scores circulate in secondary aggregators "
                "but were not read on fema.gov.",
         action="Read the parcel-level values in FEMA's Resilience Analysis and Planning Tool."),
    dict(id="F-04", sev="Medium", status="Unverified",
         item="California Department of Finance county projections for 2030, 2035 and 2040",
         detail="DOF publishes these only as .xlsx workbooks; the numeric cells were not read, so "
                "no value is asserted. This is the single most decision-relevant forecast year.",
         action="Download P-2A_County_Total.xlsx from dof.ca.gov and read the county row."),
    dict(id="F-05", sev="Medium", status="Unverified",
         item="Tax rates applied to a sale at the owner's own marginal position",
         detail="Federal and state pages on capital-gains and depreciation-recapture rates were "
                "linked but not all were re-read; the owner's basis, holding period, entity type "
                "and state residency are unknown.",
         action="A CPA computes after-tax proceeds for the actual basis and entity."),
    dict(id="F-06", sev="Low", status="Unverified",
         item="Tenant credit rating",
         detail="Rating agencies are private issuers; no rating publication was consulted, so no "
                "rating is asserted.",
         action="Read the current rating directly from the agency, or obtain it from the broker."),
    dict(id="F-07", sev="Medium", status="Unverified",
         item="Parcel Fire Hazard Severity Zone and flood zone",
         detail="Los Angeles County Local Responsibility Area zones were re-mapped in 2025, so any "
                "pre-2025 determination is stale. The parcel is unidentified.",
         action="Look up the parcel on CAL FIRE's 2025 LRA map and FEMA's flood map."),
    dict(id="F-08", sev="High", status="Unverified",
         item="Zoning, community plan and alternative-use entitlement",
         detail="The permitted uses after a restaurant box is vacated, and the uplift from "
                "redevelopment, depend on the parcel's zoning and the applicable community plan. "
                "Neither is known.",
         action="ZIMAS lookup plus a planning consultation; this is the gate on strategy S6."),
    dict(id="F-09", sev="Low", status="Unverified",
         item="School-level performance and district enrolment trend",
         detail="CDE and LAUSD publish at school and district level. District graduation rates are "
                "cited, but school assignment and enrolment trend for the parcel are not known.",
         action="Assign schools from the address; read the CDE Dashboard for those schools."),
    dict(id="F-10", sev="Medium", status="Unverified",
         item="Traffic counts on the frontage road",
         detail="Caltrans and local agencies publish counts at specific post-miles; the relevant "
                "station cannot be identified without the address. Broker-quoted counts were "
                "deliberately not used.",
         action="Pull the Caltrans count for the nearest station."),
    dict(id="F-11", sev="Low", status="Unverified",
         item="Transit project dates and costs",
         detail="Metro project pages were located but not read, so no date or cost is asserted.",
         action="Read metro.net project pages for the relevant corridor."),
    dict(id="F-12", sev="Low", status="Data conflict (source)",
         item="Los Angeles city race shares do not reconcile",
         detail="QuickFacts city race shares sum to about 74% while the county shares sum to 99.8%. "
                "The city breakdown is therefore omitted rather than published possibly wrong.",
         action="Recheck QuickFacts or use the ACS table directly."),
    dict(id="F-13", sev="Low", status="Not available",
         item="Housing units for Los Angeles city",
         detail="QuickFacts displays [X] (not available) for this field at city level.",
         action="Use the ACS table if the figure is needed."),
    dict(id="F-14", sev="Medium", status="Vintage mismatch",
         item="Mixed data vintages across the evidence table",
         detail="The table mixes V2025 population estimates, ACS 2020-2024 five-year estimates, the "
                "2022 Economic Census, 2023 County Business Patterns, 2026 monthly labour data and "
                "2025-2026 SEC filings. Every row states its own period and geography.",
         action="Never compare rows across vintages without reading the period column."),
    dict(id="F-15", sev="Medium", status="Judgement",
         item="Model assumptions, probabilities and risk scores",
         detail="Cap rates, downtime, re-tenanting capital, tenant-survival and catastrophe "
                "probabilities, the risk premium and all likelihood/impact scores are analytical "
                "judgement. They are swept across ranges and label-marked.",
         action="Replace each assumption with the owner's actual lease and market data."),
    dict(id="F-16", sev="High", status="Data conflict (layer)",
         item="Employer-establishment and payroll figures in one prior layer could not be reproduced",
         detail="The decision-file narrative cites 437,788 employer establishments, $550.7 billion "
                "of annual payroll, 1,184,030 establishments in the city and densities of 172.8 and "
                "464.6 per square mile. The official QuickFacts figure re-read for this integration "
                "is 304,988 employer establishments with $299.6 billion of annual payroll. The "
                "narrative figures are NOT carried into this dashboard.",
         action="Re-derive from County Business Patterns directly before using any of these numbers."),
    dict(id="F-17", sev="Medium", status="Data conflict (layer)",
         item="Building size asserted as a brand prototype",
         detail="One prior layer describes 'the improvement' as a specialised 1,372 sq ft drive-thru "
                "box. 1,372 sq ft is the brand's disclosed prototype, not a verified attribute of "
                "this property; the owner never supplied building size.",
         action="Read the building size from the lease or an appraisal."),
    dict(id="F-18", sev="Low", status="Source typo",
         item="Official assessment-roll release contains an internal typo",
         detail="The County release states '42% increase over 2025 or an increase of $96 billion' "
                "while the same page states 4.42%. The 4.42% figure is used here because it is "
                "consistent with $2.272 trillion versus the prior roll.",
         action="None required for this analysis; recorded so the discrepancy is not mistaken for ours."),
    dict(id="F-19", sev="Low", status="Naming inconsistency",
         item="Metro area name differs between BLS and prior layers",
         detail="BLS titles the MSA 'Los Angeles-Long Beach-Santa Ana, CA'; several prior layers use "
                "'Los Angeles-Long Beach-Anaheim'. Figures are the same series.",
         action="None; label follows the publisher."),
    dict(id="F-20", sev="Critical", status="Privacy",
         item="Repository commit metadata contains a personal name and email",
         detail="Git commit author metadata on the base commit contains a personal name and a "
                "personal email address. It is repository infrastructure, not project data, and it "
                "is deliberately not reproduced on the site, in any table, or in this file.",
         action="If the repository will be shared, rewrite history or set a neutral author identity. "
                "No personal data was collected about any owner, tenant officer or third party."),
    dict(id="F-21", sev="High", status="Judgement boundary",
         item="Whether a recommendation should be published at all",
         detail="One parallel audit layer concluded that no verified sell/renew ranking is available and "
                "withheld one; this file publishes a conditional, model-based recommendation labelled as "
                "analysis. Both positions are defensible: the ranking rests on declared assumptions, not on "
                "official data about this parcel.",
         action="Read the recommendation as conditional and replace every assumption with the lease, "
                "guaranty, zoning and appraisal facts before acting. If the assumptions cannot be "
                "populated, treat the ranking as illustrative only."),
]

# ---------------------------------------------------------------------------
# 6. CROSS-LAYER RECONCILIATION (this integration session's own audit trail)
# ---------------------------------------------------------------------------
RECONCILIATIONS = [
    dict(id="X-01", topic="Headline recommendation",
         conflict="The root landing page said no strategy was 'demonstrably superior'; four other "
                  "layers recommended selling.",
         resolution="One canonical recommendation is published: sell, with a documented "
                    "extend-then-sell alternative if the tenant will commit. The reasoning and the "
                    "conditions are on the decision page.",
         verdict="Resolved"),
    dict(id="X-02", topic="Employer establishments and payroll",
         conflict="437,788 establishments / $550.7bn payroll in one layer versus 304,988 / $299.6bn "
                  "in the official QuickFacts source.",
         resolution="The official values are published. The unreproducible narrative figures are "
                    "excluded and flagged (F-16).",
         verdict="Resolved - prior figure withdrawn"),
    dict(id="X-03", topic="Nonfarm employment, August 2026",
         conflict="6,289.1k (decision-file), 6,282.1k (analysis), 6,282.6k (BLS live read today).",
         resolution="Published value is the current BLS figure, 6,282.6k, with the revision noted. "
                    "The differences are ordinary BLS revisions, not errors.",
         verdict="Resolved - revision drift"),
    dict(id="X-04", topic="Federal funds target range",
         conflict="One layer described 3.75-4.00% as following a 'September 2026 increase' and "
                  "sourced it to a private research firm; another layer said the 28 October "
                  "decision was a hold.",
         resolution="The FOMC statement of 28 October 2026 was read directly: the Committee "
                    "maintained 3-3/4 to 4 percent on a 10-2 vote. Source re-attributed.",
         verdict="Resolved - source and wording corrected"),
    dict(id="X-05", topic="10-year Treasury yield",
         conflict="4.19% (2026-01-02) used as the model anchor; 4.90% (2026-11-04) in another layer.",
         resolution="Both are correct for their dates. The site shows 4.90% (4 Nov) and 4.84% "
                    "(5 Nov) as current observations, and keeps 4.19% explicitly as the date-stamped "
                    "model anchor.",
         verdict="Resolved - both retained, dates labelled"),
    dict(id="X-06", topic="Unemployment rate",
         conflict="4.8% was labelled 'September 2026, seasonally adjusted' in one layer; BLS "
                  "reports 4.4% for September 2026 (preliminary, not seasonally adjusted).",
         resolution="The BLS series is the only rate published here: 4.4% for September 2026, "
                    "preliminary, MSA geography, not seasonally adjusted. Definition and geography "
                    "are stated in every row.",
         verdict="Resolved - definition mismatch"),
    dict(id="X-07", topic="Number of certified ballot propositions",
         conflict="One layer published 15 propositions for the November 3, 2026 ballot.",
         resolution="The Secretary of State's certified list contains 14 (1-5 and 37-45). Corrected.",
         verdict="Resolved - corrected"),
    dict(id="X-08", topic="Measure ULA rates",
         conflict="Flagged as unverified in one layer because a deep link returned 404.",
         resolution="The official City of Los Angeles Office of Finance FAQ was read on 2026-11-07. "
                    "Rates are 4% above $5.4M and 5.5% at $10.9M or more. Upgraded to verified.",
         verdict="Resolved - upgraded to verified"),
    dict(id="X-09", topic="Cap rates labelled 'verified'",
         conflict="Eight net-lease cap-rate rows carried a 'verified-industry' status sourced to a "
                  "private research firm.",
         resolution="Reclassified as industry data and moved out of the official evidence table. "
                    "They are shown in a separate, clearly-labelled table.",
         verdict="Resolved - reclassified"),
    dict(id="X-10", topic="Prototype versus subject building",
         conflict="The brand's 1,372 sq ft prototype was described as 'the improvement'.",
         resolution="Prototype and subject are separated. Subject building size is blank (F-17).",
         verdict="Resolved - flagged"),
    dict(id="X-11", topic="Six parallel site layers",
         conflict="Root, docs/, analysis/, brief/, pages/ and decision-file/ duplicated and "
                  "occasionally contradicted each other, and each claimed a different recommendation "
                  "or evidence standard.",
         resolution="This dashboard is the single canonical site. The prior layers remain published "
                    "and are listed as archive on the landing page, clearly marked as superseded "
                    "where they conflict with the reconciled findings.",
         verdict="Resolved - consolidated"),
    dict(id="X-12", topic="Source-level errors and typos",
         conflict="The County assessment-roll release prints '42% increase' next to '4.42%'; BLS "
                  "and prior layers use different MSA names.",
         resolution="Recorded as F-18 and F-19 so they are not mistaken for our errors. Values "
                    "taken from the internally consistent figures.",
         verdict="Recorded"),
    dict(id="X-13", topic="What is published on the Pages site",
         conflict="A parallel audit session moved Pages to a curated artifact with Jekyll exclusions, "
                  "withholding the five legacy companion layers pending row-level re-verification. This "
                  "integration adds a new canonical layer.",
         resolution="The curated artifact now publishes the nine root pages plus the canonical report/ "
                    "layer. The legacy layers remain in the repository and are linked to GitHub rather "
                    "than published, so no dead links exist on the live site. The curation decision is "
                    "preserved, not overridden.",
         verdict="Resolved - merged"),
]

# ---------------------------------------------------------------------------
# 7. MODEL OUTPUT (analysis - produced by the committed model, not data)
# ---------------------------------------------------------------------------
def model_output():
    from model import projection as p

    scenarios = {}
    for sc in p.SCENARIOS:
        rate, _ = p.run(sc)
        scenarios[sc] = dict(discount_rate=round(rate * 100, 2),
                             ranked=[(rank, r["name"], round(r.get("risk_adjusted_pv_R", r["pv_R"]), 2),
                                      r.get("label", "-"))
                                     for rank, r in p.ranked(sc)])
    ev = p.expected_value()
    assumptions = []
    for name, a in p.ASSUMPTIONS.items():
        assumptions.append(dict(name=name, low=a["low"], base=a["base"], high=a["high"],
                                unit=a["unit"], status=a["status"]))
    return dict(scenarios=scenarios, expected=ev, assumptions=assumptions,
                anchor=dict(value=p.TREASURY_10Y_JAN_2026,
                            date=p.TREASURY_PAR_YIELD_JAN_2026["_date_read"],
                            url=p.TREASURY_PAR_YIELD_JAN_2026["_url"]))


if __name__ == "__main__":
    c = counts()
    print(c)
    for r in all_rows():
        print(f"{r['id']:12} {r['cat'][:26]:26} {r['status']:14} {r['display_value']}")
