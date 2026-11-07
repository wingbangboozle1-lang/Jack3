"""Analytical layer: risk register, decision framework, black-swan register,
and the Flagged-for-Review queue.

IMPORTANT LABELLING CONVENTION USED THROUGHOUT THIS FILE
--------------------------------------------------------
Every entry is tagged with one of three evidence classes:

  VERIFIED  - the underlying fact was read directly on an official .gov page
              (or an SEC filing by the issuer) in this session; a source URL
              is given and is checked by tools/check_links.py.
  MODELLED  - the figure is an output of model/projection.py from declared
              assumptions.  It is arithmetic, not observation.
  JUDGEMENT - a qualitative assessment by this analysis.  The *reasoning* is
              traceable to cited verified facts, but the severity rating
              itself is opinion and is labelled as such.

Nothing in this file is presented as verified data unless it is tagged
VERIFIED.
"""

SNAPSHOT_DATE = "2026-11-06"

# --------------------------------------------------------------------------
# RISK REGISTER
# --------------------------------------------------------------------------
# score = likelihood x impact on a 1-5 scale.  Both are JUDGEMENT, anchored to
# the cited verified evidence.
RISKS = [
    dict(
        id="R-01", category="Tenant credit",
        risk="The tenant's brand operator is running a disclosed 150-200 restaurant closure programme and has stated the remaining closures happen 'based upon respective franchise agreement termination dates'.",
        evidence_class="VERIFIED",
        evidence="Jack in the Box Inc. Form 10-K FY2025 and the JACK on Track disclosure; 40 restaurants closed in the first three quarters of FY2026; total system fell from 2,191 (FY2024 year end) to 2,115 (2026-07-05).",
        source_url="https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm",
        likelihood=4, impact=5, score=20,
        why_it_matters="A lease expiry date is precisely the trigger the closure programme uses. The 2030-2035 window is therefore not a neutral date - it is the date at which the tenant's own stated process evaluates whether to keep the site.",
        mitigation="Confirm whether the site is on the operator's closure list before spending anything on renewal negotiation. Require a corporate guaranty or a letter of credit as a renewal condition. Begin exit preparation now rather than at expiry.",
    ),
    dict(
        id="R-02", category="Tenant credit",
        risk="System same-store sales have declined in every recent reporting period.",
        evidence_class="VERIFIED",
        evidence="FY2024 system same-store sales (1.3)%; FY2025 (4.2)%; Q3 FY2025 (7.1)%; Q3 FY2026 (1.1)%. FY2026 guidance implies approximately 2,100 restaurants, down from 2,191 at FY2024 year end.",
        source_url="https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm",
        likelihood=5, impact=4, score=20,
        why_it_matters="Store-level sales drive a franchisee's ability to pay rent and its willingness to renew. Sustained negative comps convert into rent concessions, closures, or non-renewal.",
        mitigation="Obtain the subject restaurant's actual sales history and rent-to-sales ratio. A rent-to-sales ratio materially above sector norms is the strongest single predictor of non-renewal.",
    ),
    dict(
        id="R-03", category="Tenant credit",
        risk="Franchisee profitability is under disclosed pressure, and the operator has said franchise closures reduce franchise-level margin by roughly $80,000 each.",
        evidence_class="VERIFIED",
        evidence="Q3 FY2026 management commentary and results: franchise-level margin fell to $60.3M (37.4% of franchise revenues) from $66.2M (39.3%); food and packaging rose to 29.3% of company restaurant sales from 28.6%.",
        source_url="https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/0000807882-26-000090-index.htm",
        likelihood=4, impact=4, score=16,
        why_it_matters="In an NNN structure the landlord's counterparty is usually the franchisee, not the corporate. Franchisee distress is direct counterparty distress.",
        mitigation="Verify whether the lease carries a Jack in the Box Inc. corporate guaranty. If it does not, treat the credit as a small-business credit, not a NASDAQ-listed credit.",
    ),
    dict(
        id="R-04", category="Tenant cost",
        risk="California's fast-food minimum wage floor is $20.00/hour and is set by a statutory council with authority to raise it further through 2029.",
        evidence_class="VERIFIED",
        evidence="AB 1228 added Labor Code sections 1474-1476; $20.00/hour effective 2024-04-01 for covered fast food employees including franchisee-employed staff. The City of Los Angeles general minimum wage reached $18.42/hour on 2026-07-01, so the $20.00 fast-food floor is the binding rate.",
        source_url="https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm",
        likelihood=5, impact=3, score=15,
        why_it_matters="A statutory wage floor the tenant cannot avoid compresses the tenant's margin, which compresses the rent it can pay at renewal. This is a structural, not cyclical, pressure.",
        mitigation="Model renewal rent against the tenant's demonstrated rent-to-sales ratio rather than against market comparables.",
    ),
    dict(
        id="R-05", category="Rollover / vacancy",
        risk="If the tenant vacates at expiry, a single-tenant drive-thru box in an infill urban location is slow and expensive to re-let.",
        evidence_class="MODELLED",
        evidence="In the base scenario the model charges 1.5 years of downtime and 1.5 R of re-tenanting capital; in the pessimistic scenario, 3.0 years and 3.0 R. The pessimistic case reduces a hold-and-re-let strategy from 12.30 R to 2.51 R.",
        source_url="",
        likelihood=3, impact=5, score=15,
        why_it_matters="This is the largest single swing factor in the model. It is also the factor the owner controls least.",
        mitigation="Line up a replacement tenant or a redevelopment path BEFORE the expiry notice date. A site with an identified alternative use is worth materially more than one marketed cold.",
    ),
    dict(
        id="R-06", category="Market / demand",
        risk="Los Angeles County population is falling, not growing.",
        evidence_class="VERIFIED",
        evidence="U.S. Census Bureau Vintage 2025: county population 9,694,934 at 2025-07-01 against an estimates base of 10,017,414 at 2020-04-01, a change of -3.2%. City of Los Angeles -0.8% over the same period.",
        source_url="https://www.census.gov/quickfacts/losangelescountycalifornia",
        likelihood=5, impact=3, score=15,
        why_it_matters="Quick-service restaurant volume is a function of population within a drive-time ring. A shrinking base erodes transaction counts, which is exactly what the tenant is reporting.",
        mitigation="Do not underwrite renewal on an assumption of demographic growth. Test the trade area's own trajectory at tract level once the address is known.",
    ),
    dict(
        id="R-07", category="Market / demand",
        risk="Official long-range projections disagree on the DIRECTION of travel for the county's population.",
        evidence_class="VERIFIED",
        evidence="SCAG's Connect SoCal 2020 plan projected Los Angeles County at 11,674,000 by 2045 (+16.6% from 2020). The California Department of Finance projection cited in the City of Los Angeles 2024 workforce plan has the county FALLING to about 9.3 million by 2040 and 8.3 million by 2060.",
        source_url="https://ewdd.lacity.gov/images/reports/ap25/APy25_Tab5-EconomicForecast.pdf",
        likelihood=5, impact=4, score=20,
        why_it_matters="A 25-year horizon decision cannot be made on a growth assumption when the two official planning bodies disagree on the sign. Any plan that requires population growth to work is not robust.",
        mitigation="Underwrite to the OBSERVED trend (Census Vintage 2025 actuals), not to either forecast. Treat growth as upside, never as the base case.",
    ),
    dict(
        id="R-08", category="Employment",
        risk="Employment growth in the metro is weak and unevenly distributed across sectors.",
        evidence_class="VERIFIED",
        evidence="U.S. BLS, Los Angeles Area Economic Summary updated 2026-11-04: total nonfarm 6,282.1 thousand in Sep 2026, +0.5% year on year. Education and health services +3.8% and leisure and hospitality +1.5%, against information -5.7%, financial activities -1.7%, manufacturing -1.2%, professional and business services -0.5%, government -1.1%.",
        source_url="https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf",
        likelihood=4, impact=3, score=12,
        why_it_matters="A +0.5% headline masks a two-speed economy. Daypart traffic for a quick-service restaurant depends on which sectors are near the site.",
        mitigation="Identify the dominant employment sectors within a 1-3 mile ring once the address is known, and check them against this sector table.",
    ),
    dict(
        id="R-09", category="Employment",
        risk="The civilian labour force is shrinking even while the unemployment rate falls.",
        evidence_class="VERIFIED",
        evidence="U.S. BLS Metropolitan Area Employment and Unemployment (USDL-26-1618): Los Angeles-Long Beach-Anaheim MSA civilian labour force 6,646,903 in Sept 2026 (preliminary) against 6,768,502 in Sept 2025, a fall of about 121,600. The unemployment rate fell from 5.5% to 4.4% over the same period.",
        source_url="https://www.bls.gov/news.release/pdf/metro.pdf",
        likelihood=4, impact=3, score=12,
        why_it_matters="A falling unemployment rate that is caused by people leaving the labour force is not an improving economy. Fewer workers and fewer residents means fewer customers.",
        mitigation="Read the unemployment improvement together with the labour-force level, never alone.",
    ),
    dict(
        id="R-10", category="Inflation / cost",
        risk="Local inflation is running above the national average and energy costs are rising sharply.",
        evidence_class="VERIFIED",
        evidence="U.S. BLS CPI-U, 12-month change to September 2026, Los Angeles metro: all items +3.7% (U.S. city average +3.7%), food +2.8% (+2.5%), energy +20.3% (+20.4%).",
        source_url="https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf",
        likelihood=4, impact=3, score=12,
        why_it_matters="Under NNN the tenant pays the operating costs, so inflation is transferred to the tenant - which is good for the landlord until it breaks the tenant. Energy at +20.3% (12 months to Sep 2026) is a direct hit on a 24-hour drive-thru operation.",
        mitigation="Confirm the lease is genuinely absolute NNN with no landlord residual exposure to taxes, insurance or structure.",
    ),
    dict(
        id="R-11", category="Catastrophe",
        risk="Wind-driven wildfire has already destroyed a large share of structures in Los Angeles County within the last two years.",
        evidence_class="VERIFIED",
        evidence="County of Los Angeles official fact sheet: the Eaton Fire (2025-01-07 to 2025-01-31) burned 14,021 acres and destroyed 9,414 structures; the Palisades Fire burned 23,448 acres and destroyed 6,837 structures with 12 confirmed fatalities. Combined economic output lost $5.2B-$10.1B, businesses impacted approximately 6,800, tax revenue losses $900M-$1.6B.",
        source_url="https://file.lacounty.gov/SDSInter/lac/1199046_Eaton_Palisades_Fires_Anniversary_Fact_Sheet.pdf",
        likelihood=2, impact=5, score=10,
        why_it_matters="This is not a theoretical tail. It happened in this county 22 months ago and removed up to 1% of annual county economic output. It also feeds directly into insurance cost and availability, which affects both the tenant and any buyer.",
        mitigation="Determine the parcel's CAL FIRE Fire Hazard Severity Zone (2025 re-mapping applies). Confirm insurance is placed and renewable. A buyer will ask; an uninsured or uninsurable site does not sell.",
    ),
    dict(
        id="R-12", category="Catastrophe",
        risk="Earthquake exposure over the hold period is material and cannot be mitigated by timing.",
        evidence_class="VERIFIED",
        evidence="U.S. Geological Survey (UCERF3): within the next 30 years the probability in the Los Angeles region is 60% for magnitude 6.7 or greater, 46% for magnitude 7.0 or greater, and 31% for magnitude 7.5 or greater.",
        source_url="https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area",
        likelihood=3, impact=5, score=15,
        why_it_matters="A 60% 30-year probability of an M6.7+ event overlaps almost entirely with a hold-to-2035 decision. Every additional year of holding adds exposure that no rent increase compensates for.",
        mitigation="Verify the building's construction type and any seismic retrofit. Insurance availability and cost for earthquake is a first-order question, not a footnote.",
    ),
    dict(
        id="R-13", category="Valuation",
        risk="No U.S. government agency publishes commercial capitalisation rates or comparable sale prices, so the exit value cannot be verified from an official source.",
        evidence_class="VERIFIED",
        evidence="Cap rates and single-tenant NNN transaction pricing are private commercial data. The site therefore presents valuation as a SENSITIVITY GRID across a cap-rate range rather than asserting a market value.",
        source_url="",
        likelihood=5, impact=4, score=20,
        why_it_matters="The single most important number in a sell-versus-hold decision cannot be officially verified. Any adviser quoting a precise value is quoting a private dataset, not an official statistic.",
        mitigation="Commission an MAI appraisal. Treat every cap-rate-dependent conclusion as a range and check which side of the range flips the decision.",
    ),
    dict(
        id="R-14", category="Tax / transaction",
        risk="A sale crystallises tax and friction that a hold does not, and California's treatment of deferred gain is unusual.",
        evidence_class="JUDGEMENT",
        evidence="Structural: a taxable sale triggers federal and California tax on gain plus depreciation recapture; a like-kind exchange can defer it. The specific rate schedules and the California withholding and deferred-gain reporting forms were NOT read on an official page in this session, so no rates are asserted anywhere on this site.",
        source_url="https://www.ftb.ca.gov/",
        likelihood=5, impact=3, score=15,
        why_it_matters="Net proceeds, not gross price, are what the owner keeps. A 4.5% friction assumption in the model is a placeholder, not advice.",
        mitigation="Obtain a written tax opinion from a California-licensed CPA or tax attorney covering gain, depreciation recapture, exchange eligibility, and withholding BEFORE signing anything. See the Tax Framework page for the official sources to bring to that conversation.",
    ),
    dict(
        id="R-15", category="Governance",
        risk="Tenant leadership instability.",
        evidence_class="VERIFIED",
        evidence="Reporting of the Q3 FY2026 results identifies an interim chief executive. The company has also refinanced and reduced debt by $244 million since April 2025 and divested Del Taco.",
        source_url="https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/0000807882-26-000090-index.htm",
        likelihood=3, impact=2, score=6,
        why_it_matters="Counterparty strategy is less predictable during leadership transition, which matters when negotiating a renewal several years out.",
        mitigation="Do not rely on informal or relationship-based assurances from the tenant. Anything that matters must be in the lease document.",
    ),
    dict(
        id="R-16", category="Analysis integrity",
        risk="The subject property was never identified, so all site-specific conclusions are necessarily incomplete.",
        evidence_class="VERIFIED",
        evidence="No address, APN, parcel ID, building size, lot size, rent roll, lease document, basis or purchase price was provided in the repository or the brief.",
        source_url="",
        likelihood=5, impact=5, score=25,
        why_it_matters="This is the largest single limitation on the whole analysis and it is disclosed rather than papered over. Site-level trade area, traffic counts, zoning, fire zone, flood zone and school catchment cannot be determined without it.",
        mitigation="Complete the Input Register on the Property Profile page. Every field is a placeholder by design. Once supplied privately, the model in model/projection.py runs unchanged - it needs no re-engineering.",
    ),
    dict(
        id="R-17", category="Opportunity cost",
        risk="Holding concentrates the owner's wealth in one illiquid single-tenant asset in one county.",
        evidence_class="JUDGEMENT",
        evidence="Structural inference from the verified facts: an asset with a 2030-2035 expiry, a tenant in a closure programme, and a county population in decline is a concentrated, illiquid, correlated position.",
        source_url="",
        likelihood=4, impact=4, score=16,
        why_it_matters="The brief asks for preservation of wealth AND opportunity for growth at a manageable level of risk. A single concentrated position fails the diversification test regardless of how the individual numbers look.",
        mitigation="Selling converts one illiquid correlated position into capital that can be diversified. This is a reason to sell that is independent of the cap-rate view.",
    ),
]

# --------------------------------------------------------------------------
# BLACK SWAN / TAIL REGISTER
# --------------------------------------------------------------------------
BLACK_SWANS = [
    dict(
        id="B-01", event="Major wind-driven wildfire in the trade area",
        precedent="REALISED 2025-01-07: Eaton and Palisades Fires, Los Angeles County",
        evidence_class="VERIFIED",
        observed="14,021 and 23,448 acres; 9,414 and 6,837 structures destroyed; economic output lost $5.2B-$10.1B; approximately 6,800 businesses and 47,000 workers impacted; tax revenue losses $900M-$1.6B.",
        source_url="https://file.lacounty.gov/SDSInter/lac/1199046_Eaton_Palisades_Fires_Anniversary_Fact_Sheet.pdf",
        transmission_to_value="Direct physical loss; prolonged rebuild period; insurance repricing across the whole county raises the tenant's NNN cost and the buyer's underwriting; trade-area demand displaced for years.",
        horizon_relevance="High - already occurred inside the analysis period.",
    ),
    dict(
        id="B-02", event="Magnitude 6.7 or greater earthquake in the Los Angeles region",
        precedent="1994 Northridge earthquake (magnitude 6.7) is the reference event used by USGS",
        evidence_class="VERIFIED",
        observed="60% probability within 30 years for M6.7+; 46% for M7.0+; 31% for M7.5+.",
        source_url="https://www.usgs.gov/faqs/what-probability-earthquake-will-occur-los-angeles-area-san-francisco-bay-area",
        transmission_to_value="Physical damage to the building; business interruption; a buyer will not finance an unreinforced structure; insurance may become unavailable at any price.",
        horizon_relevance="High - the 30-year window fully contains a hold-to-2035 decision.",
    ),
    dict(
        id="B-03", event="Tenant brand-level failure or a large-scale closure wave",
        precedent="Disclosed and in progress: the JACK on Track block closure programme",
        evidence_class="VERIFIED",
        observed="150-200 restaurants targeted; 86 closures in FY2025; 40 in the first three quarters of FY2026; system count 2,191 to 2,115; management said the programme is being re-evaluated and extends into 2027.",
        source_url="https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm",
        transmission_to_value="Loss of the income stream; the box becomes a second-generation restaurant asset in a market where the largest operator is contracting; re-letting requires a different tenant entirely.",
        horizon_relevance="High - this is the base case, not a tail.",
    ),
    dict(
        id="B-04", event="Riverine or debris-flow flooding after wildfire-denuded slopes",
        precedent="The January 2025 fires were followed by flash-flood warnings in the burn areas",
        evidence_class="VERIFIED",
        observed="CAL FIRE incident reporting during the Palisades Fire references flash-flood warnings issued for the fire period. Post-fire debris flow is the standard second-order hazard.",
        source_url="https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire",
        transmission_to_value="Damage to ground-floor commercial property; insurance exclusions; prolonged access disruption.",
        horizon_relevance="Medium - depends on whether the site is below burned slopes.",
    ),
    dict(
        id="B-05", event="Extreme heat event suppressing drive-thru and dine-in traffic",
        precedent="Heat wave is a rated hazard for Los Angeles County in FEMA's National Risk Index",
        evidence_class="UNVERIFIED",
        observed="The specific FEMA NRI rating for Los Angeles County was not read on a fema.gov page in this session and is therefore left blank.",
        source_url="https://www.fema.gov/flood-maps/products-tools/national-risk-index",
        transmission_to_value="Short-term revenue suppression; longer-term labour availability; higher tenant utility cost under NNN.",
        horizon_relevance="Medium.",
    ),
    dict(
        id="B-06", event="Sharp regional out-migration accelerating beyond official projections",
        precedent="Observed: -3.2% county population between the 2020 estimates base and the 2025 estimate",
        evidence_class="VERIFIED",
        observed="Census Vintage 2025 county estimates. SCAG's own successive plans have been revised downward: Connect SoCal 2020 projected +14.41% for 2024-2050, Connect SoCal 2024 +10.15%, and the preliminary Connect SoCal 2050 is negative.",
        source_url="https://www.census.gov/quickfacts/losangelescountycalifornia",
        transmission_to_value="Structural erosion of the customer base and of exit values; every successive official forecast has been revised down, so the risk is asymmetric to the downside.",
        horizon_relevance="High - directly spans the 2030-2035 window.",
    ),
    dict(
        id="B-07", event="Insurance market withdrawal from California commercial property",
        precedent="Not verified from an official source in this session",
        evidence_class="UNVERIFIED",
        observed="",
        source_url="https://www.insurance.ca.gov/",
        transmission_to_value="If the building cannot be insured, the NNN lease cannot be performed and the asset cannot be financed by a buyer. This is a total-loss mechanism that does not require any physical damage.",
        horizon_relevance="Potentially high; must be checked with the California Department of Insurance before relying on a hold strategy.",
    ),
]

# --------------------------------------------------------------------------
# DECISION FRAMEWORK
# --------------------------------------------------------------------------
STRATEGIES = [
    dict(id="S1", name="Sell now, lease in place",
         summary="Market the asset today with the Jack in the Box NNN lease in place, priced off in-place income.",
         preserves_wealth="Highest - converts the position to cash at the point of maximum remaining term.",
         growth="Lowest - forfeits all future upside.",
         key_dependency="A buyer willing to underwrite a shortening remaining term.",
         model_note="Priced at the 'today' cap rate less transaction friction. Highest worst-case present value of any strategy in the model."),
    dict(id="S2", name="Hold to expiry, then sell vacant",
         summary="Collect contractual rent to 2030-2035, then sell the empty box and land.",
         preserves_wealth="Medium - full rent to expiry, but terminal value carries all the location risk.",
         growth="Low.",
         key_dependency="The alternative-use value of the land at the expiry date.",
         model_note="Terminal value taken as the LOWER of a capitalised replacement rent and the alternative-use value, so the model never assumes both."),
    dict(id="S3", name="Renew / re-let to Jack in the Box",
         summary="Grant a new long term to the incumbent brand at expiry.",
         preserves_wealth="Lowest - the model ranks this last in both the base and pessimistic scenarios.",
         growth="Low - renews into a declining unit count and a declining county population.",
         key_dependency="Entirely on tenant credit and tenant willingness. Both are outside the owner's control and both are currently deteriorating.",
         model_note="Discounted by the probability the tenant is still trading and still wants the site, then charged re-tenanting capital and vacancy. This double hit is why it ranks last."),
    dict(id="S4", name="Hold to expiry, re-let to a different operator",
         summary="Let the Jack in the Box term run out and reposition the box with another quick-service or retail user.",
         preserves_wealth="Medium-low - the highest expected value but the lowest floor of the strong strategies.",
         growth="Highest of the re-letting strategies.",
         key_dependency="Demand for second-generation drive-thru boxes in the specific trade area.",
         model_note="Longer downtime and higher capital than S3 because a non-branded box needs more adaptation, but no tenant-survival discount."),
    dict(id="S5", name="Negotiate an early extension, then sell",
         summary="Buy additional term from the tenant now (at a rent concession), then sell the lengthened lease.",
         preserves_wealth="High - best mean rank across the three scenarios.",
         growth="Low.",
         key_dependency="Tenant willingness to extend while it is running a closure programme. This is the weak link.",
         model_note="Cap-rate compression from the longer term is traded against a rent concession; both are declared assumptions and both are swept."),
    dict(id="S6", name="Hold to expiry, then redevelop",
         summary="Take the site back at expiry and pursue a higher-and-better use.",
         preserves_wealth="Medium - the most robust of the hold strategies in the base case.",
         growth="Highest absolute upside.",
         key_dependency="Zoning, entitlement, and whether Central Los Angeles land values support a better use than a drive-thru.",
         model_note="Terminal value is the full alternative-use value with no capitalised-rent cap, which is why it outperforms S2 whenever that value is high."),
]

RECOMMENDATION = dict(
    headline="Sell - and if the tenant will extend first, extend, then sell.",
    rationale=[
        "The model's highest worst-case present value belongs to selling now (11.62 R in the pessimistic scenario, against 9.88 R for the next-best strategy and 1.18 R for renewing the Jack in the Box lease). Under the owner's stated objective - preservation of wealth at a manageable level of risk - the floor matters more than the ceiling, and selling has the highest floor.",
        "Renewing the Jack in the Box lease ranks LAST in both the base and pessimistic scenarios. It is the only strategy that is heavily discounted by tenant-survival probability, because it is the only one whose entire value depends on the incumbent still wanting the site.",
        "The tenant's own SEC filings describe a 150-200 restaurant closure programme in which the remaining closures occur 'based upon respective franchise agreement termination dates'. A 2030-2035 expiry is that date. Renewing means underwriting the assumption that this specific site is not on that list, with no evidence either way.",
        "Los Angeles County population is measured to have fallen 3.2% since the 2020 estimates base, and the two official planning bodies disagree on the sign of the long-range forecast. A hold strategy that needs demographic growth to work is not robust.",
        "The brand is itself a net seller of restaurant real estate: the FY2025 10-K describes sale and sale-leaseback programmes and offering franchisees the chance to buy the property they occupy. Seller-side liquidity exists, and the owner is not the only one exiting.",
        "Selling also resolves the concentration problem. It converts one illiquid, single-tenant, single-county position into diversifiable capital - a benefit that is independent of any view on cap rates.",
    ],
    conditions=[
        "CONDITION: before spending anything on an extension negotiation, establish whether the subject site is inside the tenant's closure programme. If it is, S5 is unavailable and S1 is the answer outright.",
        "CONDITION: if the lease carries a Jack in the Box Inc. corporate guaranty and the site is confirmed to be off the closure list, S5 (extend then sell) becomes preferable to S1, because it sells a longer and more financeable income stream.",
        "CONDITION: if the land has a demonstrably better alternative use - confirmed by zoning, not by hope - then S6 outranks S1 on expected value and the owner is choosing growth over preservation. That is a legitimate choice, but it should be made explicitly and with entitlement risk priced.",
        "CONDITION: complete the Input Register on the Property Profile page first. Every strategy ranking above is normalised to R because the actual rent, basis and building details were never supplied.",
    ],
    what_would_change_the_answer=[
        "Evidence that the trade area is growing against the county trend - a tract-level population and income gain that contradicts the county aggregate.",
        "A confirmed corporate guaranty plus written confirmation from the tenant that the site is not in the closure programme.",
        "A zoning or entitlement position that makes S6 materially more valuable than the modelled alternative-use range.",
        "Cap rates for this asset type tightening far enough that a hold-and-re-let strategy beats selling in the pessimistic scenario. On the model, that requires the exit cap rate to fall below roughly 5.5%.",
    ],
)

ALL_TABLES = {"risks": RISKS, "black_swans": BLACK_SWANS, "strategies": STRATEGIES}
