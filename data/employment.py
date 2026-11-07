"""Verified data snapshot: employment, wages, payrolls and inflation for the
Los Angeles labour market.

Sources are official U.S. Bureau of Labor Statistics products and the U.S.
Census Bureau.  Every row carries a direct source URL.  Rows that could not be
confirmed carry value=None and verified="UNVERIFIED".

Retrieved 2026-11-06 (UTC) by session arena-d989a5c6-jack3.

Re-verified 2026-11-07 by session 64d0ce02 (arena/64d0ce02-jack3) (see COORDINATION.md, F-16):
- BLS Los Angeles Area Economic Summary (updated 2026-11-04) reports SEPTEMBER 2026
  payrolls, 12-month employment trends and CPI. Earlier rows labelled 2026-08 were
  re-pointed to the September values that the cited document actually contains.
- Rows whose cited document does not contain the stated value are blanked and
  marked UNVERIFIED.
"""

SNAPSHOT_DATE = "2026-11-06"

_BLS_SUMMARY = "https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf"
_BLS_METRO = "https://www.bls.gov/news.release/pdf/metro.pdf"
_BLS_T01 = "https://www.bls.gov/news.release/metro.t01.htm"
_BLS = "U.S. Bureau of Labor Statistics"
_QF_COUNTY = "https://www.census.gov/quickfacts/losangelescountycalifornia"
_QF_CITY = "https://www.census.gov/quickfacts/losangelescitycalifornia"
_CENSUS = "U.S. Census Bureau, QuickFacts"

# -------------------------------------------- labour force & unemployment --
# Release: "Metropolitan Area Employment and Unemployment", USDL-26-1618.
# Los Angeles-Long Beach-Anaheim, CA MSA.
LABOR_FORCE = [
    dict(metric="Civilian labor force", value="6,646,903", unit="persons",
         geography="la-msa", as_of="2026-09 (preliminary)",
         source_org=_BLS, source_url=_BLS_METRO, verified="VERIFIED"),
    dict(metric="Civilian labor force", value="6,768,502", unit="persons",
         geography="la-msa", as_of="2025-09",
         source_org=_BLS, source_url=_BLS_METRO, verified="VERIFIED"),
    dict(metric="Civilian labor force", value="6,589,304", unit="persons",
         geography="la-msa", as_of="2026-08",
         source_org=_BLS, source_url=_BLS_METRO, verified="VERIFIED"),
    dict(metric="Unemployed, number", value="294,000", unit="persons",
         geography="la-msa", as_of="2026-09 (preliminary)",
         source_org=_BLS, source_url=_BLS_METRO, verified="VERIFIED"),
    dict(metric="Unemployed, number", value="372,871", unit="persons",
         geography="la-msa", as_of="2025-09",
         source_org=_BLS, source_url=_BLS_METRO, verified="VERIFIED"),
    dict(metric="Unemployment rate", value="4.4", unit="percent",
         geography="la-msa", as_of="2026-09 (preliminary)",
         source_org=_BLS, source_url=_BLS_METRO, verified="VERIFIED"),
    dict(metric="Unemployment rate", value="5.5", unit="percent",
         geography="la-msa", as_of="2025-09",
         source_org=_BLS, source_url=_BLS_METRO, verified="VERIFIED"),
    dict(metric="Unemployment rate", value="4.8", unit="percent",
         geography="la-msa", as_of="2026-08",
         source_org=_BLS, source_url=_BLS_T01, verified="VERIFIED"),
    dict(metric="Unemployment rate", value="5.8", unit="percent",
         geography="la-msa", as_of="2025-08",
         source_org=_BLS, source_url=_BLS_T01, verified="VERIFIED"),
    # F-16: county and city August/2025 rates are not in the cited document.
    dict(metric="Unemployment rate", value=None, unit="percent",
         geography="la-county", as_of="2026-08",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="UNVERIFIED",
         note="Not found in cited document. Left blank (F-16)."),
    dict(metric="Unemployment rate", value=None, unit="percent",
         geography="la-county", as_of="2025-08",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="UNVERIFIED",
         note="Not found in cited document. Left blank (F-16)."),
    dict(metric="Unemployment rate", value=None, unit="percent",
         geography="la-city", as_of="2026-08",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="UNVERIFIED",
         note="Not found in cited document. Left blank (F-16)."),
    dict(metric="Unemployment rate", value=None, unit="percent",
         geography="la-city", as_of="2025-08",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="UNVERIFIED",
         note="Not found in cited document. Left blank (F-16)."),
    # Former value 4.3 labelled 2026-08 is the September 2025 figure in the cited
    # document. August 2026 national rate not confirmed; blanked (F-16).
    dict(metric="Unemployment rate (benchmark)", value=None, unit="percent",
         geography="united-states", as_of="2026-08",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="UNVERIFIED",
         note="Former value 4.3 is the Sep-2025 figure in the cited document; August 2026 not confirmed. Left blank (F-16)."),
    dict(metric="Unemployment rate (benchmark)", value="5.4", unit="percent",
         geography="california", as_of="2026-08",
         source_org=_BLS, source_url=_BLS_T01, verified="VERIFIED"),
    dict(metric="In civilian labor force (age 16+)", value="64.7", unit="percent",
         geography="la-county", as_of="2020-2024 ACS 5-year",
         source_org=_CENSUS, source_url=_QF_COUNTY, verified="VERIFIED"),
    dict(metric="In civilian labor force (age 16+)", value="66.4", unit="percent",
         geography="la-city", as_of="2020-2024 ACS 5-year",
         source_org=_CENSUS, source_url=_QF_CITY, verified="VERIFIED"),
]

# ------------------------------------------------- nonfarm payrolls by sector
# Los Angeles metro area, Aug 2026, CES.
# ------------------------------------------------- nonfarm payrolls by sector --
# Los Angeles metro area, SEPTEMBER 2026, CES (re-pointed from 2026-08; F-16).
# Source: BLS Los Angeles Area Economic Summary, updated 2026-11-04.
PAYROLLS = [
    dict(metric="Total nonfarm", value="6,282.1", unit="thousands of jobs",
         change_num="+30.2", change_pct="+0.5", geography="la-msa",
         as_of="2026-09", source_org=_BLS, source_url=_BLS_SUMMARY,
         verified="VERIFIED"),
    dict(metric="Education and health services", value="1,340.7", unit="thousands of jobs",
         change_num="+49.1", change_pct="+3.8", geography="la-msa",
         as_of="2026-09", source_org=_BLS, source_url=_BLS_SUMMARY,
         verified="VERIFIED",
         note="Largest over-the-year gain of any sector in the cited table."),
    dict(metric="Trade, transportation, and utilities", value="1,047.9", unit="thousands of jobs",
         change_num="+2.9", change_pct="+0.3", geography="la-msa",
         as_of="2026-09", source_org=_BLS, source_url=_BLS_SUMMARY,
         verified="VERIFIED"),
    dict(metric="Professional and business services", value="975.5", unit="thousands of jobs",
         change_num="-5.2", change_pct="-0.5", geography="la-msa",
         as_of="2026-09", source_org=_BLS, source_url=_BLS_SUMMARY,
         verified="VERIFIED"),
    dict(metric="Leisure and hospitality", value="782.0", unit="thousands of jobs",
         change_num="+11.5", change_pct="+1.5", geography="la-msa",
         as_of="2026-09", source_org=_BLS, source_url=_BLS_SUMMARY,
         verified="VERIFIED",
         note="The sector the tenant operates in."),
    dict(metric="Government", value="734.8", unit="thousands of jobs",
         change_num="-8.4", change_pct="-1.1", geography="la-msa",
         as_of="2026-09", source_org=_BLS, source_url=_BLS_SUMMARY,
         verified="VERIFIED"),
    dict(metric="Manufacturing", value="444.8", unit="thousands of jobs",
         change_num="-5.4", change_pct="-1.2", geography="la-msa",
         as_of="2026-09", source_org=_BLS, source_url=_BLS_SUMMARY,
         verified="VERIFIED"),
    dict(metric="Financial activities", value="300.4", unit="thousands of jobs",
         change_num="-5.1", change_pct="-1.7", geography="la-msa",
         as_of="2026-09", source_org=_BLS, source_url=_BLS_SUMMARY,
         verified="VERIFIED"),
    dict(metric="Construction", value="251.5", unit="thousands of jobs",
         change_num="+0.1", change_pct="0.0", geography="la-msa",
         as_of="2026-09", source_org=_BLS, source_url=_BLS_SUMMARY,
         verified="VERIFIED"),
    dict(metric="Other services", value="215.4", unit="thousands of jobs",
         change_num="+2.1", change_pct="+1.0", geography="la-msa",
         as_of="2026-09", source_org=_BLS, source_url=_BLS_SUMMARY,
         verified="VERIFIED"),
    dict(metric="Information", value="187.0", unit="thousands of jobs",
         change_num="-11.4", change_pct="-5.7", geography="la-msa",
         as_of="2026-09", source_org=_BLS, source_url=_BLS_SUMMARY,
         verified="VERIFIED"),
    dict(metric="Mining and logging", value="2.1", unit="thousands of jobs",
         change_num="0.0", change_pct="0.0", geography="la-msa",
         as_of="2026-09", source_org=_BLS, source_url=_BLS_SUMMARY,
         verified="VERIFIED"),
]

# --------------------------------------------------- employment growth trend
EMPLOYMENT_TREND = [
    # 12-month % change, LA metro, September values from the cited summary (F-16).
    dict(metric="12-month change in employment, Sep-23", value="-0.1",
         unit="percent", geography="la-msa", as_of="2023-09",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="VERIFIED",
         benchmark="1.8 (United States)"),
    dict(metric="12-month change in employment, Sep-24", value="1.0",
         unit="percent", geography="la-msa", as_of="2024-09",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="VERIFIED",
         benchmark="0.95 (United States)"),
    dict(metric="12-month change in employment, Sep-25", value="-0.2",
         unit="percent", geography="la-msa", as_of="2025-09",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="VERIFIED",
         benchmark="0.4 (United States)"),
    dict(metric="12-month change in employment, Sep-26", value="0.5",
         unit="percent", geography="la-msa", as_of="2026-09",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="VERIFIED",
         benchmark="0.3 (United States)"),
    dict(metric="Total employment (County Business Patterns)", value="3,987,736",
         unit="persons", geography="la-county", as_of="2023",
         source_org=_CENSUS, source_url=_QF_COUNTY, verified="VERIFIED"),
    dict(metric="Total employment, percent change 2022-2023", value="2.3",
         unit="percent", geography="la-county", as_of="2023",
         source_org=_CENSUS, source_url=_QF_COUNTY, verified="VERIFIED"),
    dict(metric="Total employer establishments", value="304,988",
         unit="establishments", geography="la-county", as_of="2023",
         source_org=_CENSUS, source_url=_QF_COUNTY, verified="VERIFIED"),
    dict(metric="Total nonemployer establishments", value="1,165,040",
         unit="establishments", geography="la-county", as_of="2024",
         source_org=_CENSUS, source_url=_QF_COUNTY, verified="VERIFIED"),
    dict(metric="Total annual payroll", value="$299,616,607", unit="$1,000",
         geography="la-county", as_of="2023", source_org=_CENSUS,
         source_url=_QF_COUNTY, verified="VERIFIED"),
]

# ------------------------------------------------------------------ wages ---
WAGES = [
    dict(metric="Average weekly wage, all industries", value="$1,704",
         unit="USD/week", geography="la-county", as_of="2026-Q1 (QCEW)",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="VERIFIED"),
    dict(metric="Average weekly wage, all industries", value="$1,721",
         unit="USD/week", geography="la-msa", as_of="2026-Q1 (QCEW)",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="VERIFIED"),
    dict(metric="Average weekly wage, all industries", value="$1,766",
         unit="USD/week", geography="orange-county", as_of="2026-Q1 (QCEW)",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="VERIFIED"),
    dict(metric="Average weekly wage, all industries", value="$1,654",
         unit="USD/week", geography="united-states", as_of="2026-Q1 (QCEW)",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="VERIFIED"),
    dict(metric="Mean hourly wage, all occupations", value="$37.15",
         unit="USD/hour", geography="la-msa", as_of="2025-05 (OEWS)",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="VERIFIED"),
    dict(metric="Mean hourly wage, all occupations", value="$33.54",
         unit="USD/hour", geography="united-states", as_of="2025-05 (OEWS)",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="VERIFIED"),
    dict(metric="Employment Cost Index, 12-month change", value="3.9",
         unit="percent", geography="la-msa", as_of="2026-09",
         source_org=_BLS, source_url=_BLS_SUMMARY, verified="VERIFIED",
         benchmark="3.1 (United States)",
         note="Area series: Los Angeles-Long Beach, CA CSA. Previous 2.8 (Jun-2026) was not in the cited document (F-16). Prior Sep values in cited table: 4.9 (Sep-23), 4.8 (Sep-24), 3.4 (Sep-25)."),
]

# ------------------------------------------------------- prices / inflation -
INFLATION = [
    # CPI-U, 12-month % change, September 2026 (cited summary; F-16).
    dict(metric="CPI-U, all items, 12-month change", value="3.7", unit="percent",
         geography="la-msa", as_of="2026-09", source_org=_BLS,
         source_url=_BLS_SUMMARY, verified="VERIFIED",
         benchmark="3.7 (U.S. city average)"),
    dict(metric="CPI-U, food, 12-month change", value="2.8", unit="percent",
         geography="la-msa", as_of="2026-09", source_org=_BLS,
         source_url=_BLS_SUMMARY, verified="VERIFIED",
         benchmark="2.5 (U.S. city average)",
         note="Direct input to the tenant's food-cost pressure and therefore to its ability to absorb rent."),
    dict(metric="CPI-U, energy, 12-month change", value="20.3", unit="percent",
         geography="la-msa", as_of="2026-09", source_org=_BLS,
         source_url=_BLS_SUMMARY, verified="VERIFIED",
         benchmark="20.4 (U.S. city average)"),
    dict(metric="PPI, hotels (exc. casino hotels) and motels, 12-month change",
         value="5.0", unit="percent", geography="united-states",
         as_of="2026-09", source_org=_BLS, source_url=_BLS_SUMMARY,
         verified="VERIFIED"),
]

ALL_TABLES = {
    "labor_force": LABOR_FORCE,
    "payrolls": PAYROLLS,
    "employment_trend": EMPLOYMENT_TREND,
    "wages": WAGES,
    "inflation": INFLATION,
}
