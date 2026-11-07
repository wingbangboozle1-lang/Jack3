"""Verified data snapshot: the tenant -- Jack in the Box Inc. (NASDAQ: JACK).

Every figure below is taken from an SEC filing by the issuer (Form 10-K,
Form 10-Q, Form 8-K) or from the issuer's own investor-relations release.
SEC EDGAR CIK: 0000807882.  Nothing here is inferred or estimated.

Retrieved 2026-11-06 (UTC) by session arena-d989a5c6-jack3.
"""

SNAPSHOT_DATE = "2026-11-06"

EDGAR_HOME = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000807882&type=10-K&dateb=&owner=include&count=10"

SRC = {
    "10K_FY2025": {
        "label": "Form 10-K, FY ended 2025-09-28 (filed 2025-11-19)",
        "url": "https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm",
        "org": "U.S. Securities and Exchange Commission (EDGAR)",
    },
    "10Q_Q3FY2026": {
        "label": "Form 10-Q, period ended 2026-07-05 (filed 2026-08-12)",
        "url": "https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/jack-20260705.htm",
        "org": "U.S. Securities and Exchange Commission (EDGAR)",
    },
    "10Q_Q3FY2026_INDEX": {
        "label": "Form 10-Q filing index, acc-no 0000807882-26-000091",
        "url": "https://www.sec.gov/Archives/edgar/data/807882/000080788226000091/0000807882-26-000091-index.htm",
        "org": "U.S. Securities and Exchange Commission (EDGAR)",
    },
    "8K_Q3FY2026": {
        "label": "Form 8-K (Items 2.02, 9.01) filed 2026-08-12 - Q3 FY2026 results",
        "url": "https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/0000807882-26-000090-index.htm",
        "org": "U.S. Securities and Exchange Commission (EDGAR)",
    },
    "8K_REFI": {
        "label": "Form 8-K (Items 1.01, 1.02, 2.03, 8.01, 9.01) filed 2026-06-23",
        "url": "https://www.sec.gov/Archives/edgar/data/807882/000080788226000079/0000807882-26-000079-index.htm",
        "org": "U.S. Securities and Exchange Commission (EDGAR)",
    },
    "IR_Q3FY2026": {
        "label": "Jack in the Box Inc. Reports Third Quarter 2026 Earnings (2026-08-12)",
        "url": "https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Inc--Reports-Third-Quarter-2026-Earnings/default.aspx",
        "org": "Jack in the Box Inc. (issuer, Investor Relations)",
    },
}

# ------------------------------------------------------- issuer identity ----
ISSUER = [
    dict(field="Registrant", value="JACK IN THE BOX INC",
         source_key="10Q_Q3FY2026_INDEX", verified="VERIFIED"),
    dict(field="SEC CIK", value="0000807882",
         source_key="10Q_Q3FY2026_INDEX", verified="VERIFIED"),
    dict(field="Ticker / exchange", value="JACK / NASDAQ",
         source_key="IR_Q3FY2026", verified="VERIFIED"),
    dict(field="State of incorporation", value="Delaware",
         source_key="10Q_Q3FY2026_INDEX", verified="VERIFIED"),
    dict(field="SIC code", value="5812 - Retail Eating Places",
         source_key="10Q_Q3FY2026_INDEX", verified="VERIFIED"),
    dict(field="SEC file number", value="001-09390",
         source_key="10Q_Q3FY2026_INDEX", verified="VERIFIED"),
    dict(field="Fiscal year end", value="Late September / early October (52-53 week)",
         source_key="10Q_Q3FY2026_INDEX", verified="VERIFIED"),
    dict(field="Principal executive offices", value="San Diego, California",
         source_key="10Q_Q3FY2026_INDEX", verified="VERIFIED",
         note="Street address withheld - not relevant to the decision and excluded per the privacy directive."),
    dict(field="Credit rating, S&P", value=None, source_key="10K_FY2025",
         verified="UNVERIFIED",
         note="No rating-agency publication was consulted. Rating agencies are not official government sources; left blank rather than inferred."),
    dict(field="Credit rating, Moody's", value=None, source_key="10K_FY2025",
         verified="UNVERIFIED",
         note="No rating-agency publication was consulted; left blank rather than inferred."),
]

# ------------------------------------------------- restaurant real estate ---
# Form 10-K FY2025, Item 2 "Properties".  This is the single most important
# structural fact for a NNN landlord: it shows how the brand itself holds
# restaurant real estate, and therefore how it behaves at lease expiry.
PROPERTIES_FY2025 = [
    dict(category="Company-owned restaurant buildings - on company-owned land",
         company_operated="8", franchise="156", total="164", brand="Jack in the Box",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(category="Company-owned restaurant buildings - on leased land",
         company_operated="55", franchise="510", total="565", brand="Jack in the Box",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(category="Subtotal, company-owned restaurant buildings",
         company_operated="63", franchise="666", total="729", brand="Jack in the Box",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(category="Company-leased restaurant buildings on leased land",
         company_operated="87", franchise="933", total="1,020", brand="Jack in the Box",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(category="Franchise directly-owned or directly-leased restaurant buildings",
         company_operated="0", franchise="387", total="387", brand="Jack in the Box",
         source_key="10K_FY2025", verified="VERIFIED",
         note="This is the ownership pattern that matches an independent third-party NNN landlord."),
    dict(category="Total restaurant buildings", company_operated="150",
         franchise="1,986", total="2,136", brand="Jack in the Box",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(category="Total restaurant buildings", company_operated="132",
         franchise="444", total="576", brand="Del Taco",
         source_key="10K_FY2025", verified="VERIFIED",
         note="Del Taco divestiture announced October 2025."),
]

# --------------------------------------------------------- lease structure --
LEASE_STRUCTURE = [
    dict(term="Initial term of real estate leases",
         value="Generally 20 years, exclusive of options to renew",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(term="Renewal options",
         value="Generally exercisable at the company's sole discretion, 1 to 20 years",
         source_key="10K_FY2025", verified="VERIFIED",
         note="Material for a landlord: option exercise sits with the tenant, not the owner."),
    dict(term="Franchise agreement initial term",
         value="20 years; initial franchise fee $50,000 per restaurant",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(term="Rent formula",
         value="Fixed rental payments with cost-of-living index adjustments, plus real estate taxes, insurance and other expenses",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(term="Percentage rent",
         value="Approximately 13% of Jack in the Box leases provide contingent rent of 1% to 10% of the restaurant's gross sales",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(term="Escalations",
         value="Many restaurant leases have rent escalation clauses and require payment of property taxes, insurance and maintenance costs",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(term="Development cost, traditional restaurant (excluding land)",
         value="$1.3 million to $1.9 million",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(term="Off-premise prototype size",
         value="Approximately 1,372 square feet; supports a Y-Lane drive-thru configuration and a walk-up window",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(term="Disposition strategy",
         value="Company uses sales and sale-leaseback financing and offers franchisees the opportunity to purchase the property currently leased to them",
         source_key="10K_FY2025", verified="VERIFIED",
         note="The brand is a net SELLER of restaurant real estate - directly relevant to sale-side liquidity."),
    dict(term="Property sale proceeds, FY2025",
         value="$19.9 million", source_key="10K_FY2025", verified="VERIFIED"),
    dict(term="Sale-leaseback transactions, FY2025",
         value="None", source_key="10K_FY2025", verified="VERIFIED"),
    dict(term="Lessee-side closure risk (issuer risk factor)",
         value="If the company closes a restaurant in a leased location it may remain committed to the lease, including base rent for the balance of the term",
         source_key="10K_FY2025", verified="VERIFIED",
         note="Shows the brand understands lease obligations survive closure - relevant to negotiating any surrender or buy-out."),
]

# ------------------------------------------------------- operating trend ----
# Same-store sales, per SEC filings.
SAME_STORE_SALES = [
    dict(period="FY2024 (year ended 2024-09-29)", company="0.0%", franchise="(1.5)%",
         system="(1.3)%", source_key="10K_FY2025", verified="VERIFIED"),
    dict(period="FY2025 (year ended 2025-09-28)", company="(3.7)%", franchise="(4.3)%",
         system="(4.2)%", source_key="10K_FY2025", verified="VERIFIED"),
    dict(period="Q3 FY2025 (12 weeks ended 2025-07-06)", company="(6.4)%",
         franchise="(7.2)%", system="(7.1)%", source_key="IR_Q3FY2026",
         verified="VERIFIED"),
    dict(period="Q3 FY2026 (12 weeks ended 2026-07-05)", company="(0.9)%",
         franchise="(1.2)%", system="(1.1)%", source_key="IR_Q3FY2026",
         verified="VERIFIED",
         note="Decline driven by lower transactions, partially offset by menu price increases."),
]

RESTAURANT_COUNTS = [
    dict(as_of="2024-09-29 (FY2024 year end)", company="150", franchise="2,041",
         total="2,191", source_key="10K_FY2025", verified="VERIFIED"),
    dict(as_of="2025-04-13 (Q2 FY2025)", company="146", franchise="2,037",
         total="2,183", source_key="10K_FY2025", verified="VERIFIED"),
    dict(as_of="2025-09-28 (FY2025 year end)", company="150", franchise="1,986",
         total="2,136", source_key="10K_FY2025", verified="VERIFIED"),
    dict(as_of="2026-07-05 (Q3 FY2026)", company="149", franchise="1,966",
         total="2,115", source_key="IR_Q3FY2026", verified="VERIFIED",
         note="Split and total from the issuer's Q3 FY2026 earnings release (Business Wire, 2026-08-12), restaurant count table. Q2 FY2026 count 2,128 (149 company, 1,979 franchise). 40 restaurants closed in the first three quarters of FY2026; FY2025 openings 31, closures 86."),
]

Q3_FY2026 = [
    dict(metric="Total revenues", value="$257.7 million", prior_year="$262.4 million",
         change="-1.8%", source_key="IR_Q3FY2026", verified="VERIFIED"),
    dict(metric="Company-operated restaurant sales", value="$96,268 thousand",
         prior_year="$94,112 thousand", change="", source_key="IR_Q3FY2026",
         verified="VERIFIED"),
    dict(metric="Franchised restaurant sales", value="$847,842 thousand",
         prior_year="$863,706 thousand", change="", source_key="IR_Q3FY2026",
         verified="VERIFIED"),
    dict(metric="Systemwide sales", value="$944,110 thousand",
         prior_year="$957,818 thousand", change="-1.4%",
         source_key="IR_Q3FY2026", verified="VERIFIED"),
    dict(metric="Systemwide sales, year to date", value="$3,137,303 thousand",
         prior_year="$3,284,624 thousand", change="", source_key="IR_Q3FY2026",
         verified="VERIFIED"),
    dict(metric="Franchise-level margin (non-GAAP)", value="$60.3 million (37.4%)",
         prior_year="$66.2 million (39.3%)", change="", source_key="IR_Q3FY2026",
         verified="VERIFIED"),
    dict(metric="Earnings from operations (GAAP)", value="$52,797 thousand",
         prior_year="$48,365 thousand", change="", source_key="IR_Q3FY2026",
         verified="VERIFIED"),
    dict(metric="Net earnings from continuing operations", value="$21.0 million",
         prior_year="$22.8 million", change="", source_key="IR_Q3FY2026",
         verified="VERIFIED"),
    dict(metric="Diluted EPS, continuing operations", value="$1.08",
         prior_year="$1.19", change="", source_key="IR_Q3FY2026",
         verified="VERIFIED"),
    dict(metric="Adjusted EBITDA (non-GAAP)", value="$61.2 million",
         prior_year="$57.1 million", change="", source_key="IR_Q3FY2026",
         verified="VERIFIED"),
    dict(metric="Franchise occupancy expenses", value="$49,694 thousand",
         prior_year="$50,829 thousand", change="", source_key="IR_Q3FY2026",
         verified="VERIFIED"),
    dict(metric="Gains on the sale of real estate to franchisees, YTD",
         value="$9,491 thousand", prior_year="", change="",
         source_key="IR_Q3FY2026", verified="VERIFIED"),
]

# ------------------------------------------------- strategic risk program ---
JACK_ON_TRACK = [
    dict(item="Programme", value="'JACK on Track', announced 2025-04-23",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(item="Block closure programme",
         value="Approximately 150-200 underperforming restaurants projected to close; a majority have been in the system for over three decades",
         source_key="10K_FY2025", verified="VERIFIED",
         note="CRITICAL for this decision: a restaurant in the system 30+ years with a lease expiring 2030-2035 fits the stated closure profile."),
    dict(item="Closure timing mechanism",
         value="Remaining underperforming restaurants close thereafter based upon respective franchise agreement termination dates",
         source_key="10K_FY2025", verified="VERIFIED",
         note="The franchise-agreement expiry date is itself the closure trigger."),
    dict(item="Dividend", value="Discontinued as part of the plan",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(item="Real estate", value="Selective real estate sales to accelerate cash flow and prioritise debt paydown",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(item="Del Taco", value="Strategic alternatives process launched 2025-04-23; divestiture announced October 2025",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(item="Del Taco divestiture consideration", value="$115 million cash",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(item="Closures executed, FY2025", value="86 (Jack in the Box)",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(item="Openings executed, FY2025", value="31 (Jack in the Box)",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(item="Debt reduction since April 2025", value="$244 million cumulative",
         source_key="IR_Q3FY2026", verified="VERIFIED"),
    dict(item="FY2026 outlook - restaurant count", value="Approximately 2,100",
         source_key="IR_Q3FY2026", verified="VERIFIED"),
    dict(item="FY2026 outlook - Adjusted EBITDA", value="$225 million to $230 million",
         source_key="IR_Q3FY2026", verified="VERIFIED"),
    dict(item="Franchisee profitability (management commentary, Q3 FY2026)",
         value="Management stated franchisee profitability remains under pressure after multiple quarters of same-store sales decline and continued inflation",
         source_key="8K_Q3FY2026", verified="VERIFIED"),
    dict(item="Closure programme pace",
         value="Company acknowledged the closure programme is progressing more slowly than originally expected, partly because franchisees must evaluate lease obligations before closing",
         source_key="10Q_Q3FY2026", verified="VERIFIED",
         note="Directly links closure decisions to LEASE obligations - the same obligation that protects a landlord, and the same one that will be tested at renewal."),
]

# --------------------------------------------- cost structure pressure ------
COST_PRESSURE = [
    dict(metric="Food and packaging, % of company restaurant sales",
         value="29.3%", prior_year="28.6%", source_key="IR_Q3FY2026",
         verified="VERIFIED"),
    dict(metric="Labor, % of company restaurant sales", value="33.7%",
         prior_year="34.5%", source_key="IR_Q3FY2026", verified="VERIFIED"),
    dict(metric="Restaurant-level margin", value="17.6%", prior_year="17.9%",
         source_key="IR_Q3FY2026", verified="VERIFIED"),
    dict(metric="Franchised restaurant average unit volume, FY2025",
         value="$1,549 thousand", prior_year="$1,573 thousand",
         source_key="10K_FY2025", verified="VERIFIED"),
    dict(metric="Royalties as % of franchised restaurant sales, FY2025",
         value="4.6%", prior_year="4.7%", source_key="10K_FY2025",
         verified="VERIFIED"),
    dict(metric="Employees, system-wide", value="5,046 (both brands)",
         prior_year="", source_key="10K_FY2025", verified="VERIFIED"),
    dict(metric="Geographic concentration",
         value="Approximately 70% of system-wide restaurants located in California and Texas",
         prior_year="", source_key="10K_FY2025", verified="VERIFIED",
         note="California is the brand's core market - a reason it defends LA sites, and a reason LA weakness hits system results directly."),
]

ALL_TABLES = {
    "issuer": ISSUER,
    "properties": PROPERTIES_FY2025,
    "lease_structure": LEASE_STRUCTURE,
    "same_store_sales": SAME_STORE_SALES,
    "restaurant_counts": RESTAURANT_COUNTS,
    "q3_fy2026": Q3_FY2026,
    "jack_on_track": JACK_ON_TRACK,
    "cost_pressure": COST_PRESSURE,
}


def resolve(row):
    """Attach the concrete source label/url/org to a row keyed by source_key."""
    src = SRC[row["source_key"]]
    out = dict(row)
    out["source_label"] = src["label"]
    out["source_url"] = src["url"]
    out["source_org"] = src["org"]
    return out
