"""Canonical, verification-gated dataset for the Asset A decision site.

Session 2aaf237e · every value was read from the publisher page on 2026-11-10.

Row contract (uniform, enforced by scripts/validate.py):
    _row(cells, status, source, note="")

  * cells   -- list of strings; a value inside HTML is escaped by the builder
  * status  -- "Verified" | "Derived" | "Analysis" | "Unverified"
  * source  -- key in SOURCES
  * note    -- optional qualifier shown under the source link

Rules:
  * "Verified" needs a source key that exists, and the row must contain at
    least one non-empty value.
  * "Unverified" rows have every value cell blank. Nothing is estimated.
  * "Derived" rows state their arithmetic in the note.
  * "Analysis" rows are this session's reasoning, never official data.

No personal data, address, parcel number, owner identity or account handle is
collected in this file, by design.
"""

SNAPSHOT = "2026-11-10"

# --------------------------------------------------------------------------
# Source register.  Every URL below was opened and read during this session.
# `observed` is a short verbatim capture used by the mechanical drift check.
# --------------------------------------------------------------------------
SOURCES = {
    "census_city": {
        "label": "QuickFacts — Los Angeles city, California (V2025)",
        "publisher": "U.S. Census Bureau",
        "host": "census.gov",
        "url": "https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225",
        "tier": "1 · U.S. federal statistical agency",
        "observed": "Population estimates, July 1, 2025, (V2025) 3,869,089 | Population estimates base, April 1, 2020, (V2025) 3,899,342 | Population, percent change -0.8% | Persons under 5 years 5.0% | Persons under 18 years 19.2% | Persons 65 years and over 14.2% | Female persons 50.2% | White alone 33.4% | Black alone 8.4% | American Indian and Alaska Native alone 1.3% | Asian alone 12.1% | Native Hawaiian and Other Pacific Islander alone 0.2% | Two or More Races 18.9% | Hispanic or Latino 47.2% | White alone, not Hispanic or Latino 28.1% | Veterans 67,714 | Foreign-born persons 35.7% | Owner-occupied housing unit rate 36.0% | Median value of owner-occupied housing units $921,200 | Median selected monthly owner costs with a mortgage $3,497 | without a mortage $1,001 | Median gross rent $1,933 | Households 1,439,097 | Persons per household 2.61 | Living in the same house 1 year ago 89.3% | Language other than English spoken at home 56.4% | Households with a computer 96.4% | broadband 92.6% | High school graduate or higher 79.6% | Bachelor's degree or higher 38.5% | With a disability 7.5% | without health insurance 10.7% | In civilian labor force total 66.4% | female 61.1% | Total accommodation and food services sales 17,366,966 | Total health care 46,297,839 | Total transportation and warehousing 25,410,257 | Total retail sales 81,351,523 | Total retail sales per capita $21,281 | Mean travel time to work 30.7 | Median households income $81,939 | Per capita income $47,685 | Persons in poverty 16.5% | Population per square mile 2020 8,304.2 | 2010 8,092.3 | Land area in square miles 2020 469.49 | 2010 468.67 | Building Permits 2025 [X]",
        "checked": "2026-11-10",
    },
    "census_county": {
        "label": "QuickFacts — Los Angeles County, California (V2025)",
        "publisher": "U.S. Census Bureau",
        "host": "census.gov",
        "url": "https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225",
        "tier": "1 · U.S. federal statistical agency",
        "observed": "Population estimates, July 1, 2025, (V2025) 9,694,934 | Population estimates base, April 1, 2020, (V2025) 10,017,414 | Population, percent change -3.2% | Persons under 18 years 19.2% | Persons 65 years and over 17.1% | White alone 62.9% | Black alone 8.9% | Asian alone 16.6% | Two or More Races 5.8% | Hispanic or Latino 49.3% | White alone, not Hispanic 24.6% | Foreign-born persons 33.4% | Owner-occupied housing unit rate 45.9% | Median value of owner-occupied housing units $834,200 | Median gross rent $1,954 | Building Permits 2025 22,250 | Households 3,416,449 | Persons per household 2.81 | High school graduate or higher 80.9% | Bachelor's degree or higher 36.0% | In civilian labor force total 64.7% | Language other than English 55.1% | Mean travel time to work 30.4 | Median households income $90,112 | Per capita income $45,792 | Persons in poverty 13.3% | Population per square mile 2020 2,466.9 | Land area in square miles 2020 4,059.28",
        "checked": "2026-11-10",
    },
    "bls_la": {
        "label": "Los Angeles Area Economic Summary (updated November 04, 2026)",
        "publisher": "U.S. Bureau of Labor Statistics",
        "host": "bls.gov",
        "url": "https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf",
        "tier": "1 · U.S. federal statistical agency",
        "observed": "Los Angeles metro area 5.5 4.4 | Los Angeles County 5.9 4.5 | Los Angeles city 5.9 4.5 | California 5.6 5.1 | United States 4.3 4.0 | Average weekly wages Q1 2026 Los Angeles 1704 Orange 1766 | Total nonfarm 6,282.1 30.2 0.5 | Mining and logging 2.1 | Construction 251.5 0.1 0.0 | Manufacturing 444.8 -5.4 -1.2 | Trade transportation and utilities 1,047.9 2.9 0.3 | Information 187.0 -11.4 -5.7 | Financial activities 300.4 -5.1 -1.7 | Professional and business services 975.5 -5.2 -0.5 | Education and health services 1,340.7 49.1 3.8 | Leisure and hospitality 782.0 11.5 1.5 | Other services 215.4 2.1 1.0 | Government 734.8 -8.4 -1.1 | Sep-26 0.5 0.3 | All items 3.7 3.7 | Food 2.8 2.5 | Energy 20.3 20.4 | West 33016 14110 12447 6713 26447 | United States 27790 13492 10633 6470 23520 | All occupations $37.15 $33.54 | Sep-26 3.9 3.1 | Total compensation $55.49 $46.89",
        "checked": "2026-11-10",
    },
    "fred_dgs10": {
        "label": "10-Year Treasury constant-maturity yield (DGS10), daily",
        "publisher": "Federal Reserve Board via FRED, Federal Reserve Bank of St. Louis",
        "host": "fred.stlouisfed.org",
        "url": "https://fred.stlouisfed.org/series/DGS10",
        "tier": "1 · Federal Reserve statistical release H.15",
        "observed": "2026-11-06: 4.86",
        "checked": "2026-11-10",
    },
    "sec_q3fy26": {
        "label": "Jack in the Box Inc. Form 8-K, Exhibit 99.1 — Q3 FY2026 earnings release (2026-08-12)",
        "publisher": "U.S. Securities and Exchange Commission, EDGAR",
        "host": "sec.gov",
        "url": "https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm",
        "tier": "1 · SEC-filed issuer disclosure",
        "observed": "Jack in the Box same-store sales of (1.1%)",
        "checked": "2026-11-10",
    },
    "sec_10k": {
        "label": "Jack in the Box Inc. Form 10-K for fiscal year ended 2025-09-28 (filed 2025-11-19)",
        "publisher": "U.S. Securities and Exchange Commission, EDGAR",
        "host": "sec.gov",
        "url": "https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/0000807882-25-000072-index.htm",
        "tier": "1 · SEC-filed issuer disclosure",
        "observed": "Period of Report 2025-09-28",
        "checked": "2026-11-10",
    },
    "sec_edgar_index": {
        "label": "EDGAR filing index — Jack in the Box Inc., CIK 0000807882",
        "publisher": "U.S. Securities and Exchange Commission, EDGAR",
        "host": "sec.gov",
        "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000807882&type=10-K&dateb=&owner=include&count=10",
        "tier": "1 · SEC filing register",
        "observed": "JACK IN THE BOX INC CIK#: 0000807882",
        "checked": "2026-11-10",
    },
    "jack_on_track": {
        "label": "\u201cJACK on Track\u201d plan announcement (2025-04-23)",
        "publisher": "Jack in the Box Inc. investor relations",
        "host": "investors.jackinthebox.com",
        "url": "https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Unveils-JACK-on-Track-Plan-to-Improve-Long-Term-Financial-Performance/default.aspx",
        "tier": "2 · issuer's own corporate release (not an SEC filing)",
        "observed": "approximately 150-200 underperforming restaurants",
        "checked": "2026-11-10",
    },
    "sec_board": {
        "label": "Form 8-K, Exhibit 99.1 — board appointment and GreenWood agreement (2026-09-21)",
        "publisher": "U.S. Securities and Exchange Commission, EDGAR",
        "host": "sec.gov",
        "url": "https://www.sec.gov/Archives/edgar/data/807882/000080788226000098/ex991-pressreleasexbodanno.htm",
        "tier": "1 · SEC-filed issuer disclosure",
        "observed": "approximately 2,115 restaurants across 25 states, Mexico and Guam",
        "checked": "2026-11-10",
    },
    "assessor_prop13": {
        "label": "Proposition 13 — assessment and 1% general levy",
        "publisher": "Los Angeles County Assessor",
        "host": "assessor.lacounty.gov",
        "url": "https://assessor.lacounty.gov/real-estate-toolkit/proposition-13",
        "tier": "1 · county assessing authority",
        "observed": "limits a property owner\u2019s general levy tax to 1 percent of the assessed value",
        "checked": "2026-11-10",
    },
    "assessor_home": {
        "label": "Los Angeles County Assessor — disaster relief, decline-in-value, 2026-27 filing window",
        "publisher": "Los Angeles County Assessor",
        "host": "assessor.lacounty.gov",
        "url": "https://assessor.lacounty.gov/",
        "tier": "1 · county assessing authority",
        "observed": "deadline to file is November 30, 2026",
        "checked": "2026-11-10",
    },
    "ula": {
        "label": "Real Property Transfer Tax and Measure ULA FAQ",
        "publisher": "City of Los Angeles Office of Finance",
        "host": "finance.lacity.gov",
        "url": "https://finance.lacity.gov/faq/measure-ula",
        "tier": "1 · city taxing authority",
        "observed": "Effective for transactions closing after June 30, 2026, the new ULA thresholds will be $5,400,000 and $10,900,000 | 4% tax | 5.5% tax | Base Tax rate of $2.25 per $500 | 4% for properties conveyed over $5,400,000 | 5.5% for properties conveyed at $10,900,000 | 0.45% | 4.45% | 5.95% | April 1, 2023 | adjusted annually based on the Bureau of Labor Statistics Chained Consumer Price Index",
        "checked": "2026-11-10",
    },
    "rtc11911": {
        "label": "California Revenue & Taxation Code \u00a711911 — Documentary Transfer Tax Act",
        "publisher": "California Legislative Information",
        "host": "leginfo.legislature.ca.gov",
        "url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=RTC&sectionNum=11911",
        "tier": "1 · statute text",
        "observed": "fifty-five cents ($0.55) for each five hundred dollars ($500)",
        "checked": "2026-11-10",
    },
    "dir_wage": {
        "label": "Minimum Wage Frequently Asked Questions (state rate)",
        "publisher": "California Department of Industrial Relations",
        "host": "dir.ca.gov",
        "url": "https://www.dir.ca.gov/dlse/FAQ_MinimumWage.htm",
        "tier": "1 · state labor agency",
        "observed": "Effective January 1, 2026, the minimum wage is $16.90 per hour",
        "checked": "2026-11-10",
    },
    "dir_fastfood": {
        "label": "Fast Food Minimum Wage Frequently Asked Questions (AB 1228)",
        "publisher": "California Department of Industrial Relations",
        "host": "dir.ca.gov",
        "url": "https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm",
        "tier": "1 · state labor agency",
        "observed": "must be paid at least $20.00 per hour",
        "checked": "2026-11-10",
    },
    "wagesla": {
        "label": "Office of Wage Standards — city minimum wage",
        "publisher": "City of Los Angeles Office of Wage Standards",
        "host": "wagesla.lacity.gov",
        "url": "https://wagesla.lacity.gov/",
        "tier": "1 · city labor standards agency",
        "observed": "July 1, 2026 $18.42",
        "checked": "2026-11-10",
    },
    "irs_1031": {
        "label": "Like-kind exchanges — real estate tax tips (\u00a71031)",
        "publisher": "Internal Revenue Service",
        "host": "irs.gov",
        "url": "https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips",
        "tier": "1 · federal tax authority",
        "observed": "you are not required to recognize a gain or loss under Internal Revenue Code Section 1031",
        "checked": "2026-11-10",
    },
    "irs_409": {
        "label": "Topic no. 409 — capital gains and losses",
        "publisher": "Internal Revenue Service",
        "host": "irs.gov",
        "url": "https://www.irs.gov/taxtopics/tc409",
        "tier": "1 · federal tax authority",
        "observed": "no higher than 15% for most individuals",
        "checked": "2026-11-10",
    },
    "ftb": {
        "label": "Capital gains and losses — California treatment",
        "publisher": "California Franchise Tax Board",
        "host": "ftb.ca.gov",
        "url": "https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html",
        "tier": "1 · state tax authority",
        "observed": "California does not have a lower rate for capital gains",
        "checked": "2026-11-10",
    },
    "cde_lausd": {
        "label": "District Profile — Los Angeles Unified (CDS 19 64733 0000000)",
        "publisher": "California Department of Education",
        "host": "cde.ca.gov",
        "url": "https://www.cde.ca.gov/sdprofile/details.aspx?cds=19647330000000",
        "tier": "1 · state education agency",
        "observed": "497,105",
        "checked": "2026-11-10",
    },
    "dashboard_lausd": {
        "label": "California School Dashboard — Los Angeles Unified, 2025 report",
        "publisher": "California Department of Education",
        "host": "caschooldashboard.org",
        "url": "https://www.caschooldashboard.org/reports/19647330000000/2025",
        "tier": "1 · state accountability system",
        "observed": "Enrollment 369,830 | Socioeconomically Disadvantaged 86.1% | English Learners 19.5% | Foster Youth 0.6% | English Language Arts 17.8 points below standard Increased 10.4 Points | Mathematics 48.9 points below standard Increased 11.5 Points | English Learner Progress 51.5% making progress | College/Career Prepared 54.9% Increased 3.8% | Chronic Absenteeism 21.9% chronically absent Declined 1.5% | Graduation Rate 86.5% graduated Maintained -0.2% | Suspension Rate 0.3% suspended at least one day | Teacher Assignments 83.2% Clear Above the State Average",
        "checked": "2026-11-10",
    },
    "usgs_shakeout": {
        "label": "The ShakeOut Scenario — USGS Open-File Report 2008-1150",
        "publisher": "U.S. Geological Survey / California Geological Survey",
        "host": "pubs.usgs.gov",
        "url": "https://pubs.usgs.gov/of/2008/1150/",
        "tier": "1 · federal science agency",
        "observed": "about 1800 deaths and $213 billion of economic losses",
        "checked": "2026-11-10",
    },
    "usgs_ucerf3": {
        "label": "UCERF3: A New Earthquake Forecast for California's Complex Fault System (FS 2015-3009)",
        "publisher": "U.S. Geological Survey",
        "host": "pubs.usgs.gov",
        "url": "https://pubs.usgs.gov/fs/2015/3009/pdf/fs2015-3009.pdf",
        "tier": "1 · federal science agency",
        "observed": "Los Angeles region",
        "checked": "2026-11-10",
    },
    "cgs_eqzapp": {
        "label": "EQ Zapp — California Earthquake Hazards Zone Application",
        "publisher": "California Geological Survey, Department of Conservation",
        "host": "conservation.ca.gov",
        "url": "https://www.conservation.ca.gov/cgs/geohazards/eq-zapp",
        "tier": "1 · state geological agency",
        "observed": "fault rupture, where the surface of the earth breaks along a fault",
        "checked": "2026-11-10",
    },
    "calfire_fhsz": {
        "label": "Fire Hazard Severity Zones (hazard vs. risk; LRA maps)",
        "publisher": "CAL FIRE — Office of the State Fire Marshal",
        "host": "osfm.fire.ca.gov",
        "url": "https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones",
        "tier": "1 · state fire agency",
        "observed": "Moderate High Very High | hazard not risk | They are like flood zone maps | Maps Released: Phase1 - February 10, 2025, Phase 2- February 24,2025, Phase 3 - March 10, 2025, and Phase 4 - March 24, 2025",
        "checked": "2026-11-10",
    },
    "calfire_palisades": {
        "label": "Palisades Fire incident record (started 2025-01-07)",
        "publisher": "CAL FIRE",
        "host": "fire.ca.gov",
        "url": "https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire",
        "tier": "1 · state fire agency incident record",
        "observed": "6,845",
        "checked": "2026-11-10",
    },
    "calfire_eaton": {
        "label": "Eaton Fire incident record (started 2025-01-07)",
        "publisher": "CAL FIRE",
        "host": "fire.ca.gov",
        "url": "https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire",
        "tier": "1 · state fire agency incident record",
        "observed": "9,419",
        "checked": "2026-11-10",
    },
    "fema_msc": {
        "label": "FEMA Flood Map Service Center — official NFIP flood hazard maps",
        "publisher": "Federal Emergency Management Agency",
        "host": "msc.fema.gov",
        "url": "https://msc.fema.gov/portal/home",
        "tier": "1 · federal agency",
        "observed": "the official public source for flood hazard information",
        "checked": "2026-11-10",
    },
    "dof_p2a": {
        "label": "Report P-2A: Total Population Projections, California Counties, 2020-2070 (Baseline 2024, Vintage 2026)",
        "publisher": "California Department of Finance, Demographic Research Unit",
        "host": "dof.ca.gov",
        "url": "https://dof.ca.gov/media/docs/forecasting/Demographics/projections/P2A_County_Total.xlsx",
        "tier": "1 · state demographic unit (projection, not an observation)",
        "observed": "6037 LOS ANGELES ALL AGES ALL SEXES ALL RACES 10,012,050 9,914,219 9,860,931 9,855,630 9,898,257 9,853,435 9,811,358 9,778,629 9,754,806 9,733,907 9,727,305 9,723,118 9,721,552 9,720,980 9,716,390 9,708,647 9,698,123 9,684,997 9,670,356 9,654,459 9,637,524 9,620,202 9,601,589 9,580,933",
        "checked": "2026-11-10",
    },
    "zimas": {
        "label": "ZIMAS — Los Angeles Zone Information and Map Access System",
        "publisher": "Los Angeles City Planning",
        "host": "zimas.lacity.org",
        "url": "https://zimas.lacity.org/",
        "tier": "1 · city planning department (parcel-query tool; no parcel supplied)",
        "observed": "ZIMAS",
        "checked": "2026-11-10",
    },
}

# DOF P-2A Los Angeles County row (FIPS 6037), calendar years 2020-2070.
# Parsed from the official .xlsx above, which the fetcher rendered as text.
P2A_LA = {
    2020: 10012050, 2021: 9914219, 2022: 9860931, 2023: 9855630, 2024: 9898257,
    2025: 9853435, 2026: 9811358, 2027: 9778629, 2028: 9754806, 2029: 9733907,
    2030: 9727305, 2031: 9723118, 2032: 9721552, 2033: 9720980, 2034: 9716390,
    2035: 9708647, 2036: 9698123, 2037: 9684997, 2038: 9670356, 2039: 9654459,
    2040: 9637524, 2041: 9620202, 2042: 9601589, 2043: 9580933, 2044: 9559513,
    2045: 9536756, 2046: 9511469, 2047: 9484569, 2048: 9454638, 2049: 9423404,
    2050: 9390823,
}




INTERNAL_SOURCE_KEY = "internal"

INTERNAL_SOURCE = {
    "label": "This decision file — method and scope",
    "publisher": "Asset A decision file (internal)",
    "host": "internal",
    "url": "methodology.html",
    "tier": "Internal · project policy, method or a declared model assumption",
    "observed": "",
    "checked": "2026-11-10",
}


def _row(cells, status, source, note=""):
    return {"cells": list(cells), "status": status, "source": source, "note": note}


def _v(cells, source, note=""):
    return _row(cells, "Verified", source, note)


def _d(cells, source, note=""):
    return _row(cells, "Derived", source, note)


def _a(cells, source, note=""):
    return _row(cells, "Analysis", source, note)


def _i(cells, note=""):
    """An internal row: project policy, method or a declared model assumption.

    It makes no factual claim about the property or the market, so no official
    source can exist. It is rendered with an Internal badge and links to the
    method page rather than borrowing a citation it does not have.
    """
    return _row(cells, "Internal", INTERNAL_SOURCE_KEY, note)


def _u(cells, source, note=""):
    """An unverified row: every value cell blank by construction."""
    return _row([c if i == 0 else "" for i, c in enumerate(cells)], "Unverified", source, note)


def _page(pid, nav, group, title, kicker, description, columns, rows):
    return {"id": pid, "nav": nav, "group": group, "title": title, "kicker": kicker,
            "description": description, "columns": columns, "rows": rows}


PAGES = []

# ------------------------------------------------------------------ Decision
PAGES.append(_page(
    "executive-summary", "Executive summary", "Decision", "Executive summary",
    "The answer, the reasoning, and the limits",
    "What can be proved from official sources, what only the owner can supply, and the sequence of decisions that follows.",
    ["Item", "Finding", "Basis"],
    [
        _a(["Headline recommendation",
            "Open renewal negotiations now. If the tenant commits to ten years or more at market rent, sell the lengthened lease. "
            "If it will not, sell before the 2030-2035 expiry, preferably through a §1031 exchange.",
            "Analyst judgement"],
           "analysis",
           "Not a valuation, appraisal or personalised financial advice. It is the conclusion drawn from the verified "
           "evidence on this site and the model on the Valuation model page."),
        _a(["Why not simply hold to expiry",
            "At expiry the owner holds a building with no contractual income, and the tenant has published a closure "
            "programme that runs to agreement termination dates.",
            "Terminal vacancy risk"],
           "jack_on_track",
           "The tenant's own 2025 announcement ties the remaining closures to franchise-agreement termination dates."),
        _a(["Why not simply sell now",
            "A sale crystallises tax: a 4.45% city transfer tax above $5.4 million plus federal and California capital-gains tax.",
            "Realised tax drag"],
           "ula",
           "Measure ULA is 4.00% of gross consideration plus the 0.45% city base for closings after 2026-06-30."),
        _a(["Sequencing that dominates both",
            "Extend first if the tenant will pay market rent for ten years or more, then sell the lengthened lease; "
            "if it will not extend, sell into the expiry window rather than through it.",
            "Term is the product"],
           "analysis",
           "A net-lease buyer is buying remaining contractual term. Extending is the only lever the owner controls."),
        _a(["What the model says",
            "Extend-then-sell has the highest worst case (13.68 R) and the highest expected value (16.22 R) of the five pathways.",
            "Deterministic model"],
           "analysis",
           "Every model input is a declared assumption. Read the Valuation model page before relying on the ranking."),
        _a(["Evidence boundary",
            "No address, parcel, rent, basis, debt or executed lease was supplied, and none is invented. No dollar value "
            "for the subject property is asserted anywhere in this file.",
            "Publication rule"],
           "analysis",
           "Every property-specific field is published blank on the Flagged for review page."),
        _a(["What would change the answer",
            "A signed extension at market rent; a verified after-tax bid above the hold case; block-level evidence of "
            "trade-area growth; or a change in the owner's liquidity needs.",
            "Decision triggers"],
           "analysis",
            "Thresholds are on the Decision page."),
        _a(["Confidence",
            "Moderate on direction (do not let the option clock run out), low on timing (2027-2029 versus 2029-2031).",
            "Analyst judgement"],
           "analysis",
           "Direction rests on structural facts about lease expiry and the tenant's closure plan, not on a price forecast."),
    ]))

# ------------------------------------------------------------------ The asset
PAGES.append(_page(
    "property-profile", "Property profile", "The asset", "Property profile & input register",
    "What is known, and what is missing",
    "Twenty fields determine the value of a net-leased restaurant. The public ones are read from official sources; "
    "the private ones are blank because they were never supplied.",
    ["Field", "Value", "Status"],
    [
        _a(["Asset class", "Single-tenant net-leased quick-service restaurant", "Owner statement"],
           "analysis", "Description supplied in the brief, not an official record."),
        _v(["Tenant brand", "Jack in the Box", "Issuer filings"], "jack_on_track",
           "Brand confirmed as an operating chain in the issuer's own releases."),
        _v(["General location", "Central Los Angeles", "Owner statement"], "census_city",
           "Only the broad area is published. No address, parcel or cross-street is stored in this repository."),
        _a(["Lease expiry window", "2030 to 2035", "Owner statement"],
           "analysis", "A five-year window, not a date. The exact expiry is in the executed lease and is not public."),
        _a(["Lease structure", "NNN — tenant pays taxes, insurance and maintenance", "Owner statement"],
           "analysis", "Triple-net is the standard structure for this asset class; the executed document was not supplied."),
        _u(["Street address", "Withheld for privacy"], "zimas",
           "Deliberately never collected. Privacy is the highest-priority requirement of this project."),
        _u(["Assessor parcel number (AIN)", "Withheld for privacy"], "assessor_home",
           "A parcel number is identifying information and is excluded by design."),
        _u(["Year built / building area / land area", "Not supplied"], "zimas",
           "ZIMAS answers this only for an address, which is deliberately not collected."),
        _u(["Current annual base rent", "Not supplied"],
           "Not public. Without it no dollar valuation is possible; the model is normalised to rent instead."),
        _u(["Rent escalation schedule", "In the lease"],
           "The most important driver of the hold case. Not supplied."),
        _u(["Option terms and notice dates", "In the lease"],
           "Notice deadlines decide whether the owner can still act. First documents to pull."),
        _u(["Tenant guarantor and credit support", "In the lease"],
           "Whether Jack in the Box Inc. or a franchisee is the obligor changes the credit entirely."),
        _u(["Original purchase price and adjusted basis", "Owner records"], "irs_409",
           "Basis sets the taxable gain, which sets the after-tax comparison."),
        _u(["Outstanding debt, rate and maturity", "Owner records"], "fred_dgs10",
           "A maturing loan can force a sale regardless of the real-estate case."),
        _u(["Property tax assessed value (Prop 13 base)", "County roll"], "assessor_prop13",
           "Public but parcel-keyed, and the parcel is deliberately not collected."),
        _u(["Zoning and general plan designation", "Parcel-keyed"], "zimas",
           "Determines re-use and redevelopment value at expiry."),
        _u(["Flood zone (FEMA FIRM panel)", "Parcel-keyed"], "fema_msc",
           "FEMA is the official source; a panel is identified by address or coordinates."),
        _u(["Fire Hazard Severity Zone", "Parcel-keyed"], "calfire_fhsz",
           "CAL FIRE maps hazard, not risk. A zone cannot be assigned without the parcel."),
        _u(["Liquefaction / landslide zone", "Parcel-keyed"], "cgs_eqzapp",
           "CGS maps three ground-failure hazards; the parcel lookup was not performed."),
        _u(["Store-level sales and rent coverage", "Not public"],
           "Franchisee unit economics are not disclosed by the issuer."),
    ]))

PAGES.append(_page(
    "geography", "Geography", "The asset", "Geography, land and access",
    "Location evidence that does not identify the parcel",
    "Central Los Angeles is a dense, built-out, car-oriented market. What geography can and cannot tell an owner here.",
    ["Indicator", "Value", "Geography / period"],
    [
        _v(["Land area", "469.49 square miles", "Los Angeles city, 2020"], "census_city"),
        _v(["Population density", "8,304.2 per square mile", "Los Angeles city, 2020"], "census_city"),
        _v(["County land area", "4,059.28 square miles", "Los Angeles County, 2020"], "census_county"),
        _v(["County population density", "2,466.9 per square mile", "Los Angeles County, 2020"], "census_county"),
        _v(["Mean travel time to work", "30.7 minutes", "Los Angeles city, 2020-2024"], "census_city"),
        _v(["County mean travel time to work", "30.4 minutes", "Los Angeles County, 2020-2024"], "census_county"),
        _v(["Households", "1,439,097", "Los Angeles city, 2020-2024"], "census_city",
           "QuickFacts publishes households; the city housing-unit count carries a suppressed flag."),
        _v(["Owner-occupied rate", "36.0%", "Los Angeles city, 2020-2024"], "census_city",
           "A renter-majority city, which matters for trade-area income stability."),
        _v(["Median value, owner-occupied unit", "$921,200", "Los Angeles city, 2020-2024"], "census_city"),
        _v(["Median gross rent", "$1,933", "Los Angeles city, 2020-2024"], "census_city"),
        _v(["County median value, owner-occupied unit", "$834,200", "Los Angeles County, 2020-2024"], "census_county"),
        _v(["County building permits, 2025", "22,250", "Los Angeles County, 2025"], "census_county",
           "The city figure is suppressed by QuickFacts, so only the county value is published."),
        _u(["Trade-area drive time, traffic counts, access, parking", "Parcel-keyed"], "zimas",
           "Requires the address, which is deliberately not collected. No proxy is substituted."),
    ]))

# ------------------------------------------------------------------ The market
PAGES.append(_page(
    "demographics", "People & income", "The market", "People, income and the trade area",
    "Who lives near the site, and what they can spend",
    "Population, households, income, poverty and education from Census QuickFacts for the city and county that contain the property.",
    ["Indicator", "Los Angeles city", "Los Angeles County", "Period"],
    [
        _v(["Population", "3,869,089", "9,694,934", "July 1, 2025 (V2025)"], "census_city",
           "County value read from the county table."),
        _v(["Population, 2020 estimates base", "3,899,342", "10,017,414", "April 1, 2020 (V2025)"], "census_city"),
        _v(["Population change since 2020 base", "-0.8%", "-3.2%", "2020-2025 (V2025)"], "census_city",
           "Both geographies shrank. The county decline is the larger one."),
        _v(["Median household income (2024 dollars)", "$81,939", "$90,112", "2020-2024"], "census_city"),
        _v(["Per capita income (2024 dollars)", "$47,685", "$45,792", "2020-2024"], "census_city"),
        _v(["Persons in poverty", "16.5%", "13.3%", "2025 (V2025)"], "census_city"),
        _v(["Households", "1,439,097", "3,416,449", "2020-2024"], "census_city"),
        _v(["Persons per household", "2.61", "2.81", "2020-2024"], "census_city"),
        _v(["Persons under 18", "19.2%", "19.2%", "2025 (V2025)"], "census_city"),
        _v(["Persons 65 and over", "14.2%", "17.1%", "2025 (V2025)"], "census_city"),
        _v(["Foreign-born persons", "35.7%", "33.4%", "2020-2024"], "census_city"),
        _v(["Language other than English at home (age 5+)", "56.4%", "55.1%", "2020-2024"], "census_city"),
        _v(["High school graduate or higher (age 25+)", "79.6%", "80.9%", "2020-2024"], "census_city"),
        _v(["Bachelor's degree or higher (age 25+)", "38.5%", "36.0%", "2020-2024"], "census_city"),
        _v(["Civilian labour force participation (age 16+)", "66.4%", "64.7%", "2020-2024"], "census_city"),
        _v(["Hispanic or Latino (any race)", "47.2%", "49.3%", "2025 (V2025)"], "census_city"),
        _v(["White alone, not Hispanic or Latino", "28.1%", "24.6%", "2025 (V2025)"], "census_city"),
        _v(["Asian alone", "12.1%", "16.6%", "2025 (V2025)"], "census_city"),
        _v(["Black alone", "8.4%", "8.9%", "2025 (V2025)"], "census_city"),
        _u(["Race shares, Los Angeles city, all seven published categories", "Withheld — see F-12"], "census_city",
           "The published city race-alone shares do not reconcile arithmetically with the county table, so the "
           "individual city shares above are shown but the aggregate is not used for any analysis."),
        _u(["Census-tract income and spending inside the actual trade area", "Parcel-keyed"], "census_city",
           "A trade area cannot be drawn without the address. City and county averages are context only."),
    ]))

PAGES.append(_page(
    "economy", "Economy & jobs", "The market", "Economy, jobs and prices",
    "The regional engine behind the trade area",
    "Unemployment, payrolls by sector, wages, inflation and the risk-free rate for the Los Angeles metro area, from BLS and the Federal Reserve.",
    ["Indicator", "Value", "Comparison", "Period"],
    [
        _v(["Unemployment rate — Los Angeles metro", "4.4%", "5.5% in Sep-2025; U.S. 4.0%", "Sep 2026"], "bls_la"),
        _v(["Unemployment rate — Los Angeles County", "4.5%", "5.9% in Sep-2025", "Sep 2026"], "bls_la"),
        _v(["Unemployment rate — Los Angeles city", "4.5%", "5.9% in Sep-2025", "Sep 2026"], "bls_la"),
        _v(["Unemployment rate — California", "5.1%", "5.6% in Sep-2025", "Sep 2026"], "bls_la"),
        _v(["Total nonfarm employment, metro", "6,282.1 thousand", "+30.2 thousand (+0.5%) year over year", "Sep 2026"], "bls_la"),
        _v(["12-month employment change, metro", "+0.5%", "U.S. +0.3%", "Sep 2026"], "bls_la"),
        _v(["Education and health services", "1,340.7 thousand", "+49.1 thousand (+3.8%)", "Sep 2026"], "bls_la",
           "Largest sector and fastest grower."),
        _v(["Trade, transportation and utilities", "1,047.9 thousand", "+2.9 thousand (+0.3%)", "Sep 2026"], "bls_la"),
        _v(["Professional and business services", "975.5 thousand", "-5.2 thousand (-0.5%)", "Sep 2026"], "bls_la"),
        _v(["Leisure and hospitality", "782.0 thousand", "+11.5 thousand (+1.5%)", "Sep 2026"], "bls_la",
           "The sector that contains restaurants."),
        _v(["Government", "734.8 thousand", "-8.4 thousand (-1.1%)", "Sep 2026"], "bls_la"),
        _v(["Manufacturing", "444.8 thousand", "-5.4 thousand (-1.2%)", "Sep 2026"], "bls_la"),
        _v(["Financial activities", "300.4 thousand", "-5.1 thousand (-1.7%)", "Sep 2026"], "bls_la"),
        _v(["Construction", "251.5 thousand", "+0.1 thousand (0.0%)", "Sep 2026"], "bls_la"),
        _v(["Information", "187.0 thousand", "-11.4 thousand (-5.7%)", "Sep 2026"], "bls_la",
           "Sharpest decline of any sector."),
        _v(["Average weekly wage, all industries", "$1,704", "Orange County $1,766", "Q1 2026"], "bls_la"),
        _v(["CPI-U, all items, 12-month change", "3.7%", "U.S. 3.7%", "Sep 2026"], "bls_la"),
        _v(["CPI-U, energy, 12-month change", "20.3%", "U.S. 20.4%", "Sep 2026"], "bls_la"),
        _v(["CPI-U, food, 12-month change", "2.8%", "U.S. 2.5%", "Sep 2026"], "bls_la"),
        _v(["Employment Cost Index, 12-month change", "3.9%", "U.S. 3.1%", "Sep 2026"], "bls_la",
           "Local wage costs are rising faster than national ones."),
        _v(["Average hourly wage, all occupations", "$37.15", "U.S. $33.54", "May 2025 OEWS"], "bls_la"),
        _v(["Average annual consumer spending, West region", "$33,016 housing; $12,447 food",
            "U.S. $27,790 housing; $10,633 food", "2025"], "bls_la"),
        _v(["10-year Treasury constant-maturity yield", "4.86%", "4.84% on 2026-11-05; 4.95% on 2026-11-03", "2026-11-06"],
           "fred_dgs10", "The risk-free anchor a net-lease buyer prices against."),
        _u(["Sub-market vacancy, rents and absorption for this trade area", "No official publisher"],
           "No federal or state agency publishes commercial sub-market data, and broker research is excluded by the "
           "official-sources rule."),
    ]))

PAGES.append(_page(
    "projections", "Projections 2026-2035", "The market", "Projection system, 2026-2035",
    "Official projections first, then a transparent model",
    "The State of California's county population projection is used exactly as published. The property model is "
    "normalised to rent and discloses every assumption on the page.",
    ["Projection", "Value", "Basis"],
    [
        _v(["LA County population, 2025 (DOF)", "9,853,435", "Official projection, Baseline 2024, Vintage 2026"], "dof_p2a",
           "DOF projects from its own estimate base, which differs from the Census base above. Both are published; "
           "neither is adjusted."),
        _v(["LA County population, 2030 (DOF)", "9,727,305", "Official projection"], "dof_p2a"),
        _v(["LA County population, 2035 (DOF)", "9,708,647", "Official projection"], "dof_p2a"),
        _v(["LA County population, 2040 (DOF)", "9,637,524", "Official projection"], "dof_p2a"),
        _d(["Change 2025-2035 (DOF)", "-1.5%", "9,708,647 ÷ 9,853,435 − 1"], "dof_p2a",
           "A slow contraction, not a collapse."),
        _d(["Change 2025-2030 (DOF)", "-1.3%", "9,727,305 ÷ 9,853,435 − 1"], "dof_p2a", "Formula shown in the Basis column."),
        _d(["Change 2030-2035 (DOF)", "-0.2%", "9,708,647 ÷ 9,727,305 − 1"], "dof_p2a",
           "The decline flattens: most of it is in the next five years."),
        _a(["Consistency check against the measured trend",
            "Same direction",
            "Census: -3.2% from the 2020 base to 2025. DOF: -2.2% from its own 2020 base to 2025."],
           "census_county",
           "Two different vintages, reported together rather than reconciled into one number."),
        _u(["Metro employment projection to 2035", "Not extracted"], "bls_la",
           "EDD publishes industry projections only through an interactive Tableau application. Nothing was extracted "
           "and nothing is estimated; see F-09."),
        _a(["Property cash-flow model", "See the Valuation model page", "Normalised to R = one year of base rent"],
           "analysis", "Deterministic arithmetic with declared inputs. Not an official forecast."),
        _u(["Rent or cap-rate forecast specific to this parcel", "None published"],
           "No federal or state body publishes a cap-rate series for single-tenant restaurant assets."),
    ]))

# ------------------------------------------------------------------ The tenant
PAGES.append(_page(
    "tenant", "Tenant & lease", "The tenant", "Tenant credit and lease risk",
    "Jack in the Box Inc., from its own filings",
    "Same-store sales, units, closures, capital allocation and guidance, read from SEC-filed documents. This is the counterparty behind the rent.",
    ["Item", "Value", "Period"],
    [
        _v(["Legal entity", "Jack in the Box Inc., CIK 0000807882, Delaware, fiscal year ends late September",
            "Current"], "sec_edgar_index", "Address of record is in San Diego, California, per the filings."),
        _v(["Ticker", "NASDAQ: JACK", "Current"], "sec_board"),
        _v(["System same-store sales", "-1.1%", "Q3 FY2026, 12 weeks to 2026-07-05"], "sec_q3fy26",
           "Franchise -1.2%, company-owned -0.9%."),
        _v(["Prior-year system same-store sales", "-7.1%", "Q3 FY2025"], "sec_q3fy26"),
        _v(["Systemwide sales change", "-1.4%", "Q3 FY2026"], "sec_q3fy26"),
        _v(["Restaurant count, total", "2,115", "End of Q3 FY2026"], "sec_q3fy26",
           "Franchise 1,966; company-owned 149."),
        _v(["Restaurant count, prior year", "2,168", "End of Q3 FY2025"], "sec_q3fy26",
           "Negative net unit growth year over year."),
        _v(["Quarterly unit change", "-13 net", "Q3 FY2026"], "sec_q3fy26", "4 openings, 17 closures."),
        _v(["Total revenues", "$257.7 million, -1.8%", "Q3 FY2026"], "sec_q3fy26"),
        _v(["Franchise rental revenues", "$73.0 million", "Q3 FY2026"], "sec_q3fy26",
           "Down from $76.5 million. The issuer is itself a landlord to its franchisees."),
        _v(["Franchise-Level Margin", "$60.3 million, 37.4%", "Q3 FY2026"], "sec_q3fy26",
           "Down from $66.2 million, 39.3%."),
        _v(["Restaurant-Level Margin", "$17.0 million, 17.6%", "Q3 FY2026"], "sec_q3fy26"),
        _v(["Adjusted EBITDA", "$61.2 million", "Q3 FY2026"], "sec_q3fy26", "Prior-year quarter $57.1 million."),
        _v(["Diluted EPS, continuing operations", "$1.08", "Q3 FY2026"], "sec_q3fy26", "Operating EPS $0.96."),
        _v(["Effective tax rate", "36.9%", "Q3 FY2026"], "sec_q3fy26", "Prior year 20.9%."),
        _v(["FY2026 restaurant-count guidance", "About 2,100", "Fiscal year to 2026-09-27"], "sec_q3fy26",
           "About 25 openings and 50 to 60 closures."),
        _v(["FY2026 same-store sales guidance", "Low single digit decline", "Fiscal year to 2026-09-27"], "sec_q3fy26"),
        _v(["FY2026 Adjusted EBITDA guidance", "$225-230 million", "Fiscal year to 2026-09-27"], "sec_q3fy26"),
        _v(["Dividend and buyback", "Dividend discontinued; no repurchases in the quarter", "Q3 FY2026"], "sec_q3fy26",
           "$175.0 million remains authorised under the buyback programme."),
        _v(["Securitised debt refinancing", "$500 million 2026-1 Class A-2 notes", "Q3 FY2026"], "sec_q3fy26",
           "Anticipated repayment date May 2031."),
        _v(["Prepayment of 2019-1 Class A-2-II notes", "$110.0 million", "Q3 FY2026"], "sec_q3fy26"),
        _v(["Del Taco divestiture", "Completed 2025-12-22", "Q3 FY2026 disclosure"], "sec_q3fy26",
           "Reported in discontinued operations."),
        _v(["Closure programme size", "150-200 restaurants", "Announced 2025-04-23"], "jack_on_track",
           "A majority had been in the system for over three decades."),
        _v(["Closure programme phasing",
            "80-120 by 2025-12-31; the remainder at franchise-agreement termination dates",
            "Announced 2025-04-23"], "jack_on_track",
           "The most decision-relevant sentence in the evidence set: it ties store exits to agreement or lease dates."),
        _v(["Real-estate strategy", "Sell a select number of owned properties; proceeds to debt paydown",
            "Announced 2025-04-23"], "jack_on_track",
           "Signals that the issuer prefers liquidity to owning real estate."),
        _v(["Latest annual report on file", "Form 10-K for the period ended 2025-09-28, filed 2025-11-19", "2025"],
           "sec_10k", "No later 10-K was on file at the snapshot date."),
        _v(["Leadership", "Mark King, Executive Chairman and Interim CEO; Taylor Montgomery expected to become CEO within 12 months",
            "2026-09-21"], "sec_board"),
        _u(["Subject property rent, term, options and guarantor", "In the executed lease"],
           "Not public. This is the largest single unknown in the file."),
    ]))

# ------------------------------------------------------------------ Money
PAGES.append(_page(
    "taxes", "Taxes & transfer costs", "Money", "Taxes, transfer costs and the after-tax question",
    "What a sale actually costs",
    "Property tax, the documentary transfer tax, the City of Los Angeles surcharge, federal and California capital-gains treatment, and §1031 deferral.",
    ["Item", "Value", "Application"],
    [
        _v(["Proposition 13 general levy", "1% of assessed value", "Annual property tax"], "assessor_prop13",
           "Plus voter-approved debt and direct assessments."),
        _v(["Annual assessed-value increase cap", "2%", "Prop 13 base-year value"], "assessor_prop13",
           "Except on change of ownership or new construction."),
        _v(["Assessment on sale", "Change of ownership reassesses to market value", "At the sale"], "assessor_prop13",
           "A buyer underwrites the post-sale tax bill, not the seller's."),
        _v(["Decline-in-value filing window", "2026-07-02 to 2026-11-30", "2026-2027 tax year"], "assessor_home",
           "Relevant if market value falls below the assessed value."),
        _v(["County documentary transfer tax", "$0.55 per $500 of consideration", "On the deed"], "rtc11911",
           "Rate set by California Revenue & Taxation Code §11911."),
        _v(["City documentary transfer tax, base", "0.45% ($2.25 per $500)", "On the deed"], "ula",
           "In addition to the county tax."),
        _v(["Measure ULA surcharge, lower tier", "4.00% of gross consideration above $5,400,000", "Closings after 2026-06-30"],
           "ula"),
        _v(["Measure ULA surcharge, upper tier", "5.50% at $10,900,000 or more", "Closings after 2026-06-30"], "ula"),
        _d(["Combined city rate above $5.4m", "4.45%", "0.45% city base + 4.00% ULA"], "ula",
           "Both component rates are published on the same official page."),
        _d(["Combined city rate at or above $10.9m", "5.95%", "0.45% city base + 5.50% ULA"], "ula",
           "Both component rates are published on the same official page."),
        _v(["Measure ULA threshold indexing", "Adjusted annually by the BLS Chained CPI", "Annual"], "ula"),
        _v(["Measure ULA effective date", "2023-04-01", "History"], "ula"),
        _v(["Federal long-term capital-gains rate", "0%, 15% or 20% depending on taxable income", "Federal return"], "irs_409",
           "A 3.8% net investment income tax can apply on top of the applicable rate."),
        _v(["Unrecaptured §1250 gain", "Maximum 25% rate", "Depreciated real property"], "irs_409",
           "This is the part that surprises sellers who depreciated the building."),
        _v(["California capital-gains treatment", "No preferential rate; taxed as ordinary income", "California return"], "ftb"),
        _v(["§1031 like-kind exchange",
            "Gain not recognised when real property is exchanged for like-kind real property", "At the sale, if executed"],
           "irs_1031", "Since 2018 §1031 applies to real property only. It defers tax; it does not eliminate it."),
        _v(["§1031 and a personal residence", "Not available", "At the sale"], "irs_1031",
           "Matters if the owner intends to roll into housing rather than another investment property."),
        _u(["Owner's adjusted basis and holding period", "Owner records"], "irs_409",
           "Not supplied. Without it no after-tax figure about this property can be computed."),
        _u(["Owner's filing status and taxable income", "Owner records"], "irs_409",
           "Determines whether the federal rate is 15%, 20% or 23.8% with the net investment income tax."),
        _u(["Owner's state of residence", "Owner records"], "ftb",
           "California taxes the gain on California real property sold by a California resident."),
    ]))

PAGES.append(_page(
    "model", "Valuation model", "Money", "The model, in one unit of rent",
    "No invented rent, no invented value",
    "No rent was supplied, so every strategy is valued in units of R — one year of current contractual base rent. "
    "The ranking then depends on term, tenant behaviour, cost and tax rather than on an unknown rent level.",
    ["Line", "Value", "How it is computed"],
    [
        _v(["Risk-free anchor", "4.86%", "10-year Treasury, 2026-11-06"], "fred_dgs10"),
        _i(["Risk premium", "1.14%", "Declared assumption"],
           "Added to the Treasury yield to give a 6.00% base discount rate. The premium is an assumption, not a sourced figure."),
        _i(["Discount rate", "6.00% base; 4.50% optimistic; 7.50% pessimistic", "Treasury plus premium, swept"]),
        _i(["Horizon", "2026 to 2036", "Ten years, which spans the expiry window"]),
        _i(["Assumed exit year", "2032", "Mid-point of the owner-reported 2030-2035 window"],
           "A single assumed year; the full window is not separately modelled."),
        _i(["Renewal probability", "60% base; 85% optimistic; 35% pessimistic", "Swept assumption"],
           "Not sourced. The tenant has not disclosed an intention for any specific site."),
        _i(["Exit capitalisation rate", "6.50% base; 5.50% optimistic; 7.50% pessimistic", "Swept assumption"],
           "No official cap-rate series exists. The value of one unit of R at the base case is 1 ÷ 6.50% = 15.38 R."),
        _i(["Rent growth", "2.0% base; 3.0% optimistic; 1.0% pessimistic", "Swept assumption"]),
        _i(["Re-let rent after vacancy", "60% of passing rent, base case", "Swept assumption"]),
        _i(["Downtime after vacancy", "2 years base; 1 optimistic; 2 pessimistic", "Assumption"]),
        _i(["Vacancy carrying cost", "0.5 R per downtime year", "Assumption for taxes, insurance and security"]),
        _i(["Renewal rent reset", "90% of passing rent", "Assumption"],
           "A renewal is modelled as a negotiation, not as an automatic roll at the current rent."),
        _i(["Market re-let rent", "85% of passing rent", "Assumption"]),
        _i(["Term premium for a long lease", "+10% on sale price", "Assumption"],
           "Applied only to the extend-then-sell pathway."),
        _i(["Selling cost", "2.00% of gross price", "Brokerage and closing, assumed"],
           "An assumption, not a sourced figure. No official publisher states a typical brokerage rate."),
        _d(["City transfer tax on exit", "4.45% of price", "0.45% base plus 4.00% ULA tier"], "ula",
           "Assumed to apply, which requires a price above the $5.4 million threshold."),
        _a(["Capital-gains drag", "32.3% of gain", "20% federal plus 3.8% NIIT plus 8.5% California"], "irs_409",
           "An owner-specific estimate. Actual liability depends on basis, income and filing status, none of which were supplied."),
        _a(["§1031 exchange", "Tax deferred, not eliminated", "Reinvestment into like-kind real property"], "irs_1031",
           "Carried as a separate consideration, never as a free lunch."),
        _u(["Value of the subject property in dollars", "Requires rent, area, basis and a market cap rate"],
           "Deliberately blank. A dollar value would have to be invented."),
    ]))

# ------------------------------------------------------------------ Risk
PAGES.append(_page(
    "hazards", "Hazards", "Risk", "Natural hazards and black-swan exposure",
    "What the agencies actually publish",
    "Earthquake, wildfire and flood exposure for the region, with the distinction between hazard mapping, risk and a specific parcel kept explicit.",
    ["Hazard / measure", "Value", "Geography / basis"],
    [
        _v(["Earthquake, M≥6.7 in 30 years", "60%", "Los Angeles region, UCERF3 Table 1, from 2014"], "usgs_ucerf3"),
        _v(["Earthquake, M≥7.0 in 30 years", "46%", "Los Angeles region"], "usgs_ucerf3"),
        _v(["Earthquake, M≥7.5 in 30 years", "31%", "Los Angeles region"], "usgs_ucerf3"),
        _v(["Average repeat time, M≥6.7", "40 years", "Los Angeles region"], "usgs_ucerf3"),
        _v(["Modelled M7.8 San Andreas scenario, deaths", "About 1,800", "Eight-county southern California"], "usgs_shakeout"),
        _v(["Modelled M7.8 scenario, economic losses", "$213 billion", "Eight-county southern California"], "usgs_shakeout"),
        _v(["Ground-failure hazards mapped by the state",
            "Fault rupture, liquefaction, earthquake-induced landslide", "Statewide"], "cgs_eqzapp",
           "Whether this parcel sits in one of those zones is undetermined; the state tool is parcel-keyed."),
        _v(["Fire Hazard Severity Zone classes", "Moderate, High, Very High", "State and Local Responsibility Areas"],
           "calfire_fhsz", "The state maps hazard, not risk. No zone is asserted for this parcel."),
        _v(["2025 Local Responsibility Area maps", "Released in four phases, February to March 2025", "All counties"],
           "calfire_fhsz", "Phase dates are listed on the OSFM page."),
        _v(["Palisades Fire", "23,448 acres; 6,845 structures destroyed; 12 civilian fatalities",
            "Los Angeles County, January 2025"], "calfire_palisades", "Cause recorded as arson."),
        _v(["Eaton Fire", "14,021 acres; 9,419 structures destroyed; 19 civilian fatalities",
            "Los Angeles County, January 2025"], "calfire_eaton", "Cause recorded as electrical."),
        _d(["Structures destroyed in the two fires", "16,264", "6,845 + 9,419"], "calfire_eaton",
           "Each component is sourced separately on its own incident page."),
        _u(["Flood zone for this parcel", "Parcel-keyed"], "fema_msc",
           "FEMA is the official source and its lookup is address- or coordinate-keyed. Nothing is inferred."),
        _u(["Wildfire probability for this parcel", "Not published in parcel form"], "calfire_fhsz",
           "No annual probability is invented. The state maps hazard classes, not annual likelihoods."),
        _u(["Insurance availability and premium", "Not published"],
           "California's post-2025 wildfire insurance market cannot be assessed without the parcel and a quote."),
    ]))

PAGES.append(_page(
    "risk-register", "Risk register", "Risk", "Risk register",
    "Business as usual, then the tail",
    "Each risk is paired with the verified evidence that makes it live and the mitigation available to the owner. "
    "Likelihood and severity are this session's judgement and are labelled as such.",
    ["ID", "Risk", "Verified evidence", "Judgement", "Mitigation"],
    [
        _a(["R-01", "Tenant vacates at expiry and the building goes dark",
            "Lease expiry 2030-2035; 50-60 closures guided for FY2026; block closure programme",
            "High likelihood · High severity", "Start renewal talks now and market the asset while income is contractual."],
           "jack_on_track"),
        _a(["R-02", "Issuer credit deteriorates before expiry",
            "Same-store sales negative two years running; dividend discontinued; securitised refinancing",
            "Medium · High", "Read each 10-Q and 8-K; hold six months of debt service in reserve."],
           "sec_q3fy26"),
        _a(["R-03", "Re-letting at a lower rent after vacancy",
            "Metro employment growth of 0.5%; a purpose-built restaurant box has few alternative users",
            "Medium · High", "Negotiate a renewal option with a rent floor rather than gambling on the market."],
           "bls_la"),
        _a(["R-04", "Exit yield expands as Treasury yields rise",
            "10-year Treasury 4.86% on 2026-11-06",
            "Medium · High", "Model the value at +100 bp and do not underwrite to today's yield."],
           "fred_dgs10"),
        _a(["R-05", "Wage-floor inflation compresses franchisee margins",
            "Fast-food minimum $20.00/hour; city minimum $18.42 from 2026-07-01; state $16.90",
            "High · Medium", "Ask for unit-level profit and loss in diligence; rent coverage is unknown."],
           "dir_fastfood"),
        _a(["R-06", "Property tax step-up on sale reduces a buyer's bid",
            "Change of ownership reassesses to market value; 1% levy plus assessments",
            "High · Medium", "Price the post-sale tax bill into the ask and into buyer outreach."],
           "assessor_prop13"),
        _a(["R-07", "Transaction tax on a city sale",
            "4.00% ULA above $5.4 million plus 0.45% base plus $0.55 per $500 county",
            "High · Medium", "Model the net proceeds and consider the $5.4 million threshold before setting a price."],
           "ula"),
        _a(["R-08", "Capital-gains tax on exit",
            "Federal 15% or 20% plus 3.8% NIIT; California gives gains no preferential rate",
            "High · Medium", "Establish basis now and evaluate a §1031 exchange before listing."],
           "irs_409"),
        _a(["R-09", "Debt maturity forces a sale at a bad moment",
            "Owner-specific and not supplied",
            "Unknown · High", "Refinance or extend before listing if a maturity falls inside the sale window."],
           "analysis"),
        _a(["R-10", "Trade-area demand erosion",
            "City population -0.8%, county -3.2% since 2020; DOF projects continued county decline to 2035",
            "Medium · Medium", "Do not assume traffic growth in the underwriting."],
           "census_county"),
        _a(["R-11", "Operating cost inflation on a NNN asset",
            "CPI-U +3.7%; energy +20.3%; employment cost index +3.9%",
            "Medium · Low", "Confirm the lease's expense pass-throughs and any caps."],
           "bls_la"),
        _a(["R-12", "Zoning or entitlement blocks re-use at expiry",
            "Parcel-keyed; ZIMAS is the official city tool",
            "Unknown · Medium", "Pull the zoning and general plan designation before expiry, not after."],
           "zimas"),
        _a(["R-13", "Earthquake damage",
            "60% chance of M≥6.7 in the region within 30 years; a modelled M7.8 event at about 1,800 deaths and $213 billion",
            "Low frequency · Severe", "Commission a seismic assessment and carry adequate insurance, including business interruption."],
           "usgs_ucerf3"),
        _a(["R-14", "Wildfire",
            "16,264 structures destroyed in two Los Angeles County fires in January 2025",
            "Regional · Severe", "Defensible space is not the issue on an urban pad; insurance availability is."],
           "calfire_eaton"),
        _a(["R-15", "Flood",
            "FEMA is the official mapping authority; the parcel zone is unknown",
            "Unknown · Medium", "Pull the FIRM panel before purchase or expiry."],
           "fema_msc"),
        _a(["R-16", "Insurance market withdrawal",
            "Post-2025 California wildfire market; no official parcel-level data",
            "Medium · High", "Obtain quotes early. A non-renewal can force a sale regardless of the real-estate case."],
           "analysis"),
        _a(["R-17", "Municipal fiscal stress raising transfer or property taxes",
            "Measure ULA is the live example of a city-level transfer tax",
            "Medium · Low", "Track city council actions; ULA thresholds are indexed annually."],
           "ula"),
        _a(["R-18", "Pandemic or civil disruption closing dining rooms",
            "2020-2021 precedent; no current official signal",
            "Low frequency · High", "Lease language on abatement and force majeure matters more than any forecast."],
           "analysis"),
    ]))

PAGES.append(_page(
    "decision", "Decision", "Decision", "Decision pathways, risks and triggers",
    "Five routes, scored on the downside",
    "Sell now, hold to expiry, seek renewal, extend-then-sell, or re-tenant. Each is scored on its worst case as well as "
    "its expected value, because preserving wealth is a floor problem before it is an optimisation problem.",
    ["Pathway", "Mechanics", "Dominant risk", "Why it loses"],
    [
        _i(["A · Sell now", "Market the asset today with a 2030-2035 expiry",
            "Exit yield expansion during the marketing period",
            "Leaves value on the table if the tenant would have extended cheaply."]),
        _a(["B · Hold to expiry, do nothing", "Collect rent to expiry, then decide",
            "Vacancy with no income and no plan",
            "Hands the timing decision to the tenant, whose own plan is to close stores at agreement dates."], "jack_on_track"),
        _a(["C · Seek renewal at expiry", "Negotiate a new term when the lease comes up",
            "Rent reset into a softer market",
            "A single-counterparty negotiation conducted while the income stream is expiring."], "sec_q3fy26"),
        _i(["D · Extend first, then sell", "Negotiate ten years or more at market rent, then market the lengthened lease",
            "Extension talks leak and weaken the sale position",
            "Costs time and optionality, and depends entirely on the tenant agreeing."]),
        _i(["E · Re-tenant at expiry", "Let the building to another operator",
            "Downtime, re-fixture cost and lower rent",
            "Worst downside of the operating routes; only rational with parcel-level evidence of demand."]),
    ]))

# ------------------------------------------------------------------ Assurance
PAGES.append(_page(
    "sources", "Sources & method", "Assurance", "Source register",
    "Every page this file was read from",
    "Thirty official publishers, each opened in this session on the same date. Every table row on the site links to one of these pages.",
    ["Source", "Publisher", "Tier", "Read on"],
    [{"cells": [s["label"], s["publisher"], s["tier"], s["checked"]],
      "status": "Verified", "source": k, "url": s["url"],
      "note": "Read directly from this page in this session."}
     for k, s in SOURCES.items()]))

PAGES.append(_page(
    "flagged", "Flagged for review", "Assurance", "Flagged for review",
    "Everything that is blank, and why",
    "Nothing on this site was estimated. Every item below is withheld for privacy, unobtainable from an official source, "
    "or in conflict between sources. Each names the page or document that would close it.",
    ["ID", "Item", "Why it is unresolved", "What closes it"],
    [
        _a(["F-01", "Property identity: address, parcel, AIN",
            "Withheld deliberately. Privacy is the highest-priority requirement of this project.",
            "Owner supplies it privately to their adviser. It is never published."], "zimas"),
        _i(["F-02", "Current rent, escalations, options and term",
            "Not public. Contained in the executed lease.",
            "Executed lease, rent roll and any amendments."]),
        _a(["F-03", "Owner basis, holding period, debt and filing status",
            "Owner records only.",
            "Closing statement, depreciation schedule and loan statements."], "irs_409"),
        _i(["F-04", "Commercial capitalisation rates for this asset class",
            "No federal or state agency publishes cap rates. Broker surveys are excluded by the official-sources rule.",
            "Two independent arm's-length appraisals."]),
        _i(["F-05", "Sub-market vacancy, rents and absorption",
            "No official publisher at this geography.",
            "An appraisal or third-party survey, labelled as non-official if used."]),
        _a(["F-06", "FEMA flood zone for this parcel",
            "The FEMA lookup is address- or coordinate-keyed.",
            "Pull the FIRM panel using the parcel."], "fema_msc"),
        _a(["F-07", "Fire Hazard Severity Zone for this parcel",
            "The state tool is parcel-keyed.",
            "Look the parcel up in the CAL FIRE viewer."], "calfire_fhsz"),
        _a(["F-08", "Liquefaction or landslide zone",
            "The state tool is parcel-keyed.",
            "Look the parcel up in EQ Zapp."], "cgs_eqzapp"),
        _a(["F-09", "Metro employment projection to 2035",
            "EDD publishes projections only through an interactive Tableau application; nothing readable was extracted.",
            "A downloadable EDD projection file, or the Tableau view read manually and recorded with its vintage."], "bls_la"),
        _a(["F-10", "City of Los Angeles building permits, 2025",
            "QuickFacts suppresses the city value with an [X] flag; the county value is published and is used instead.",
            "The underlying Census Building Permits Survey place-level file."], "census_city"),
        _a(["F-11", "County documentary transfer tax as stated by the county",
            "The Los Angeles County Registrar-Recorder pages returned 'resource removed' when fetched on 2026-11-10.",
            "Closed from statute instead: Revenue & Taxation Code §11911 sets $0.55 per $500, and the statutory rate "
            "is published on the Taxes page. The county page itself remains unread."], "rtc11911"),
        _a(["F-12", "Census race shares for Los Angeles city, aggregated",
            "The published city shares (White 33.4, Black 8.4, AIAN 1.3, Asian 12.1, NHPI 0.2, two-or-more 18.9) sum to "
            "about 74%, which cannot be reconciled mechanically with the county table's 99.8%. The individual rows are "
            "published because each was read directly; the aggregate is not used in any analysis.",
            "Re-read the QuickFacts race table in full, including any 'some other race' line the renderer dropped."], "census_city"),
        _a(["F-13", "Store-level sales and rent coverage for the subject restaurant",
            "Not disclosed by the issuer for individual units.",
            "Franchisee unit profit and loss in diligence."], "sec_q3fy26"),
        _a(["F-14", "Assigned school attendance area",
            "Parcel-keyed.",
            "Address lookup in the district's boundary tool."], "cde_lausd"),
        _i(["F-15", "Insurance availability and premium",
            "Requires a quote on the actual building and occupancy.",
            "Broker quotes."]),
        _a(["F-16", "Zoning and general plan designation",
            "Parcel-keyed.",
            "ZIMAS lookup with the parcel."], "zimas"),
        _i(["F-17", "Whether the 2030-2035 window is an initial term or an option",
            "Determines whether the rent can be extended unilaterally or has to be negotiated.",
            "Executed lease."]),
        _a(["F-18", "The tenant's intention for this specific site",
            "Not disclosed. The closure programme explains the mechanism, not the list of sites.",
            "A written renewal proposal request to the tenant's real-estate group."], "jack_on_track"),
        _a(["F-19", "Annual probability of a black-swan event at this parcel",
            "No agency publishes an annual parcel-level probability for earthquake, fire or flood.",
            "Regional probabilities only; a parcel study would be non-official."], "usgs_ucerf3"),
        _i(["F-20", "Owner's liquidity needs and time horizon",
            "Personal circumstances were not supplied and are deliberately not collected.",
            "The owner's own statement, which is not recorded in this repository."]),
        _i(["F-21", "Any published dollar value for this property",
            "Requires rent, area, basis and a market capitalisation rate, none of which were supplied.",
            "An appraisal instructed by the owner."]),
    ]))

PAGES.append(_page(
    "schools", "Schools & workforce", "The market", "Schools and human capital",
    "The district that contains the site",
    "Los Angeles Unified is the district covering central Los Angeles. Enrollment, graduation and subgroup outcomes "
    "are read from the state's own systems.",
    ["Indicator", "Value", "Period"],
    [
        _v(["District", "Los Angeles Unified, CDS 19 64733 0000000", "Current"], "cde_lausd"),
        _v(["District enrollment", "497,105", "2025-26"], "cde_lausd"),
        _v(["English language learners", "81,328, or 16.4%", "2025-26"], "cde_lausd"),
        _v(["Four-year cohort graduation rate", "86.5%", "2025 Dashboard"], "dashboard_lausd"),
        _v(["Change in graduation rate", "-0.2 points, reported as maintained", "2025 Dashboard"], "dashboard_lausd"),
        _v(["Chronic absenteeism", "21.9%, down 1.5 points", "2025 Dashboard"], "dashboard_lausd"),
        _v(["Socioeconomically disadvantaged", "86.1%", "2025 Dashboard"], "dashboard_lausd"),
        _v(["College or career prepared", "54.9%, up 3.8 points", "2025 Dashboard"], "dashboard_lausd"),
        _v(["English language arts, all students", "17.8 points below standard, up 10.4 points", "2025 Dashboard"], "dashboard_lausd"),
        _v(["Mathematics, all students", "48.9 points below standard, up 11.5 points", "2025 Dashboard"], "dashboard_lausd"),
        _v(["Suspension rate", "0.3%", "2025 Dashboard"], "dashboard_lausd"),
        _v(["Teacher assignment, clear credentials", "83.2%, above the state average", "2025 Dashboard"], "dashboard_lausd"),
        _u(["Assigned school for the subject property", "Parcel-keyed"], "cde_lausd",
           "An attendance boundary cannot be assigned without the address. LAUSD is the district; the specific school is blank."),
    ]))

# ------------------------------------------------------------------ Assurance
PAGES.append(_page(
    "repo-review", "Repo review", "Assurance", "Repository review",
    "What the inherited layers got right and wrong",
    "Line-by-line review of the seven parallel document sets this repository accumulated, and the irregularity log.",
    ["Finding", "Detail", "Action taken"],
    [
        _i(["Layer inventory",
            "advisory/, analysis/, brief/, dashboard/, decision-file/, docs/ and pages/ were produced by separate sessions.",
            "Each was inspected. Only the root set generated from this dataset is published."]),
        _i(["IR-01 · conflicting headline recommendations",
            "Six layers carry recommendations ranging from hold to sell. None can be true at once without stating its assumptions.",
            "This session states one recommendation, marks it Analysis, and publishes its assumptions."]),
        _i(["IR-02 · non-official sources inside 'all-official' claims",
            "analysis/ cites a commercial brokerage for 22 rows and a private law firm for 4, while claiming an all-official standard.",
            "Those rows are not republished. Only government and SEC-filed pages appear in this dataset."]),
        _i(["IR-03 · repository account handle in rendered pages",
            "26 inherited HTML files render the repository owner's account handle in visible text.",
            "The published artifact is regenerated from scratch, so the handle does not appear. The repository-only "
            "files were left untouched and are not published."]),
        _a(["IR-04 · stale market anchor",
            "decision-file/ anchors its model to a 4.19% 10-year Treasury from 2026-01-02; the rate read today is 4.86%.",
            "This session uses 4.86% from 2026-11-06 and discloses the premium separately."], "fred_dgs10"),
        _i(["IR-05 · broken internal navigation",
            "/brief/ returns 404 on the live site because _config.yml excludes brief/ from the Pages build, yet the README links to it.",
            "Root navigation is rebuilt and README corrected; no published link points at an unpublished layer."]),
        _a(["IR-06 · duplicated research with different vintages",
            "The same Census and BLS figures are re-derived in several layers, sometimes with different vintages.",
            "One dataset now feeds every published page."], "census_county"),
        _a(["IR-07 · flags that are already closed",
            "Several layers report the county transfer tax and the LAUSD graduation rate as unverifiable; both were readable today.",
            "Both are published with sources. The county page itself still failed, so the rate is published from statute; see F-11."], "rtc11911"),
        _i(["IR-08 · unverified values rendered as numbers",
            "At least one layer published model outputs that could be mistaken for official forecasts.",
            "Blanking is enforced in the validator, not by convention."]),
        _i(["IR-09 · build determinism",
            "Hand-edited HTML previously broke CI on a byte-identical rebuild check.",
            "Every published page is generated, and the determinism check is retained in CI."]),
        _i(["IR-10 · open pull requests",
            "Six stale pull requests (#4, #12, #22, #26, #31, #32) are open against main, several with red CI.",
            "Not merged. Recorded in COORDINATION.md as superseded by this integration; nothing was deleted."]),
        _i(["Privacy check",
            "No address, parcel, owner, contact detail, account handle or executed lease appears in the generated output.",
            "Checked by scripts/validate.py on every build."]),
    ]))

PAGES.append(_page(
    "privacy", "Privacy", "Assurance", "Privacy and anonymisation",
    "Highest priority, enforced in code",
    "What is collected, what is never collected, and how the build fails if identifying information appears.",
    ["Rule", "Implementation"],
    [
        _i(["Placeholders only", "'Asset A' and 'Owner A' replace every identifying name. No real name appears anywhere on the site."]),
        _i(["No address or parcel", "The property is described only as central Los Angeles. No street, cross-street or AIN is stored in this repository."]),
        _i(["No owner research", "No person, trust, entity or ownership chain connected to the property was researched or recorded."]),
        _i(["No contact data", "No phone numbers, email addresses or account handles of the owner or of the tenant's officers are collected."]),
        _i(["No third-party scripts", "No analytics, web fonts, CDNs, iframes or forms. Every page is static HTML plus one local stylesheet."]),
        _i(["Enforced at build time", "scripts/validate.py fails the build on any email, telephone number, street address, parcel pattern or repository handle in the output."]),
        _i(["Public sources only", "Every published figure comes from a government or SEC page open to the public. Nothing private was obtained."]),
    ]))

PAGES.append(_page(
    "methodology", "Methodology", "Assurance", "Methodology and limitations",
    "What a verified badge means, and does not mean",
    "The verification standard, how the model works, and the limitations a reader must carry into any decision.",
    ["Topic", "Statement"],
    [
        _i(["Verified", "The value was read on the publisher page named in the row, on the date in the source register, and is stored verbatim."]),
        _i(["Derived", "Arithmetic on verified values, with the operation shown in the note."]),
        _i(["Analysis", "This file's reasoning. Sources on the row support background only and do not endorse the conclusion."]),
        _i(["Unverified", "The cell is blank. No value is inferred, interpolated or borrowed from a similar property."]),
        _i(["Model", "Deterministic arithmetic on declared assumptions. No randomness, no fitted parameters, no back-test."]),
        _i(["A link is not a verification", "A URL proves nothing on its own; the value has to have been read. Every row here was opened in this session, and the source register records a verbatim capture used by an automated drift check."]),
        _i(["Not an appraisal", "Nothing here is an appraisal, a broker opinion of value, legal advice, or personalised investment advice."]),
        _i(["Regional data is not parcel data", "City and county averages cannot tell an owner what this restaurant earns or what this parcel is worth."]),
        _i(["Snapshot, not a feed", "Values are fixed at 2026-11-10. Rolling sources such as FRED and BLS will change; re-read them before acting."]),
        _a(["Projection limits", "The only multi-year official projection used is the California DOF county series. No official rent or cap-rate forecast exists at parcel level."], "dof_p2a"),
        _i(["Right to be wrong", "Every recommendation here is a judgement that could be wrong. The worst case is published beside the expected case for exactly that reason."]),
    ]))

# A short, explicit ordering for the navigation groups.
GROUP_ORDER = ["Decision", "The asset", "The market", "The tenant", "Money", "Risk", "Assurance"]


# ---------------------------------------------------------------------------
# Normalisation.  An "Unverified" row may be written with just its label; the
# remaining value cells are padded blank, which is the only padding allowed.
# Every other row must match the page's column count exactly, so a verified or
# derived value can never silently slide into the wrong column.
for _p in PAGES:
    _n = len(_p["columns"])
    for _r in _p["rows"]:
        if len(_r["cells"]) < _n:
            if _r["status"] != "Unverified":
                raise ValueError(f'{_p["id"]}: non-unverified row has too few cells: {_r["cells"][0]}')
            _r["cells"] = _r["cells"] + [""] * (_n - len(_r["cells"]))
        if len(_r["cells"]) > _n:
            raise ValueError(f'{_p["id"]}: row has too many cells: {_r["cells"][0]}')


# ---------------------------------------------------------------------------
# Final reconciliation.  Two shapes are tolerated and made explicit here, so
# that no row can end up pointing at a source key that does not exist:
#   * a row whose "source" is actually prose is an internal row -- the prose
#     becomes its note and the source becomes the internal method page;
#   * the retired "analysis" key becomes the same internal source.
for _p in PAGES:
    for _r in _p["rows"]:
        _src = _r["source"]
        if _src in SOURCES or _src == INTERNAL_SOURCE_KEY:
            continue
        if _src == "analysis":
            _r["source"] = INTERNAL_SOURCE_KEY
            continue
        if len(_src) > 25:
            _r["note"] = (_src + " " + _r["note"]).strip()
            _r["source"] = INTERNAL_SOURCE_KEY
            continue
        raise ValueError(f'{_p["id"]}: unresolved source key {_src!r} on row {_r["cells"][0]}')

_ORDER = {p["id"]: i for i, p in enumerate(PAGES)}
PAGES.sort(key=lambda p: (GROUP_ORDER.index(p["group"]), _ORDER[p["id"]]))
