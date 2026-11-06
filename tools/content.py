"""Long-form content for the SP-01 site.

Every figure quoted in this file is either (a) a verified value that also appears in
data/datasets.json with a source id, or (b) an explicitly labelled model output or
assumption. Prose never introduces a number that is not traceable.
"""

EXEC_SUMMARY = {
    "title": "Executive Summary",
    "standfirst": (
        "SP-01 is a single-tenant Jack in the Box quick-service restaurant on a triple-net "
        "lease in central Los Angeles, with a lease expiry inside the 2030&#8211;2035 window. "
        "This study asks one question: sell before expiry, or renew? It answers that question "
        "from official data, states plainly what it could not verify, and quantifies every "
        "decision it recommends."
    ),
}

VERDICT = {
    "headline": "Renew if the tenant will commit. Never sell for cash. Route any exit through a &#167;1031 exchange.",
    "one_line": (
        "On risk-adjusted after-tax wealth the ranking is stable across 6,000 simulated macro paths: "
        "renew-and-hold-with-a-deferred-exit first, a &#167;1031 exchange executed now second, and an "
        "outright cash sale last. The outright cash sale is dominated in <em>every</em> scenario tested, "
        "and the reason is tax, not the market."
    ),
}

KEY_FINDINGS = [
    {
        "n": 1,
        "title": "The tenant is stabilising, but it is also shrinking &#8212; on purpose",
        "body": (
            "Jack in the Box same-store sales went from <strong>&#8722;7.4%</strong> in Q4 fiscal 2025 "
            "to <strong>&#8722;1.1%</strong> in Q3 fiscal 2026, a 6.0 point improvement (S12, S13). "
            "That is the strongest single positive datapoint in this study. Against it, the company has "
            "guided to closing <strong>50 to 100 restaurants</strong> in fiscal 2026 after closing 86 in "
            "fiscal 2025, and its system is down to 2,115 units from 2,191 (S12, S13). The tenant is "
            "recovering its P&amp;L by removing its weakest boxes. Whether SP-01 is one of them is not "
            "publicly knowable."
        ),
        "flag": "F-01",
    },
    {
        "n": 2,
        "title": "The local economy is stable but not growing, and the population is shrinking",
        "body": (
            "Los Angeles County unemployment fell to <strong>4.8%</strong>, below both California (5.1%) "
            "and its own 5.6% a year earlier (S05). But total nonfarm employment grew only "
            "<strong>0.4%</strong> over the year, and five of eleven industry sectors are shrinking &#8212; "
            "information lost 10,200 jobs and has declined in 20 of the last 22 months (S05). The county "
            "has lost <strong>3.2%</strong> of its population since 2020 (S06) and is projected to lose "
            "<strong>240,800</strong> public school students over the next decade, the largest county "
            "decline in the state (S09). Health care is the only real growth engine."
        ),
        "flag": None,
    },
    {
        "n": 3,
        "title": "Density is the asset. Central LA holds 3.4&#215; the county's population density",
        "body": (
            "The City of Los Angeles carries <strong>8,304</strong> people per square mile against "
            "<strong>2,467</strong> for the county (S06, S07), and the city is declining more slowly than "
            "the county (&#8722;0.8% versus &#8722;3.2% since 2020). Its population is younger (14.2% aged "
            "65+ versus 17.1%) and the restaurant sub-sector is still adding jobs (+7,300 year over year, "
            "S05). An urban infill drive-through is therefore in the better half of a deteriorating county."
        ),
        "flag": None,
    },
    {
        "n": 4,
        "title": "The tax code, not the market, decides this question",
        "body": (
            "A cash sale in the City of Los Angeles carries <strong>0.56%</strong> in county and city "
            "transfer tax below the Measure ULA threshold, and <strong>4.56%</strong> above $5.4 million "
            "or <strong>6.06%</strong> above $10.9 million because ULA is a cliff applied to the whole "
            "price (S16, S17). Stack a blended <strong>33.4%</strong> capital gains rate on the gain and an "
            "outright sale surrenders roughly a third of all accumulated appreciation. A &#167;1031 "
            "exchange defers that entire amount (S18). Stack that on selling costs and the arithmetic is brutal: on a $6.5 million "
            "asset with a 40% basis, a cash sale delivers <strong>$4.83 million</strong> of net proceeds "
            "&#8212; a 25.7% haircut taken before a dollar is reinvested. The same-day &#167;1031 "
            "exchange of the identical asset delivers <strong>$5.94 million</strong>. Nothing about the "
            "property changed between those two figures; only the structure did."
        ),
        "flag": None,
    },
    {
        "n": 5,
        "title": "A short lease is priced. That is why waiting is not free",
        "body": (
            "Once a single-tenant net-lease asset has under about five years of term left, buyers stop "
            "pricing a bond and start pricing a re-leasing story. The model applies a cap-rate penalty "
            "that widens to 75bp as remaining term goes to zero (A16). This is the mechanism by which "
            "'hold to expiry' loses to 'sell before expiry' even in a rising-rent market &#8212; and it is "
            "the single reason a renewal is worth more than the rent it captures."
        ),
        "flag": None,
    },
    {
        "n": 6,
        "title": "The hazard record is recent, large, and already inside the tax base",
        "body": (
            "In one week of January 2025, two urban wildfires destroyed <strong>16,263</strong> structures "
            "in Los Angeles County &#8212; 6,845 in the Palisades Fire and 9,418 in the Eaton Fire &#8212; "
            "with 29 confirmed civilian deaths between them (S21, S22). The fiscal consequence is visible: "
            "wildfire assessment relief removed more than <strong>$9 billion</strong> from the 2026 "
            "assessment roll, more than new construction added (S25). A central-LA infill site is far less "
            "exposed than the wildland interface, but the event class is not hypothetical."
        ),
        "flag": None,
    },
    {
        "n": 7,
        "title": "The tenant's cost of capital has more than doubled, and it matures before the lease does",
        "body": (
            "Jack in the Box refinanced in June 2026 by issuing $500 million of <strong>7.624%</strong> "
            "secured notes to retire paper carrying 4.476% and 3.445% (S14). Its next anticipated "
            "repayment date is <strong>2029</strong> &#8212; earlier than the 2030&#8211;2035 expiry window. "
            "The tenant therefore faces a refinancing decision before the landlord faces a renewal "
            "decision, and a tenant under refinancing pressure is a tenant that renegotiates rent."
        ),
        "flag": None,
    },
]

DECISION_MATRIX_INTRO = (
    "Seven strategies were evaluated on 6,000 simulated macro paths each, across three assumed "
    "property values. Each path draws recessions, black-swan events, rent-growth deviations and "
    "cap-rate shifts, and every path is shared across strategies so the comparison is like-for-like. "
    "Results are after all taxes and after Los Angeles transfer tax and Measure ULA."
)

RECOMMENDATION_STEPS = [
    {
        "step": "1",
        "title": "Do not sell for cash. In this fact pattern it is dominated.",
        "body": (
            "On a $6.5 million asset with a 40% adjusted basis, a cash sale nets about "
            "<strong>$4.83 million</strong> after brokerage, Los Angeles transfer tax and capital gains "
            "&#8212; a 25.7% haircut. A &#167;1031 exchange of the identical asset on the identical day "
            "nets about <strong>$5.94 million</strong>, because the capital gains tax of roughly $1.12 "
            "million is deferred rather than paid. Roughly <strong>17% of asset value</strong> is destroyed "
            "for no economic reason other than liquidity. If a sale happens, it must be structured."
        ),
    },
    {
        "step": "2",
        "title": "Separate the exit decision from the structure decision.",
        "body": (
            "These are two different decisions and they are routinely conflated. <em>Should I exit?</em> is "
            "a question about the tenant, the lease term and concentration risk. <em>How do I exit?</em> is a "
            "question about tax. The model says the second decision is worth more than the first: on the base "
            "case, changing only the structure of a sale changes terminal after-tax wealth by more than the "
            "entire difference between selling in 2026 and selling in 2035."
        ),
    },
    {
        "step": "3",
        "title": "Open renewal discussions now, while the tenant is improving.",
        "body": (
            "A renewal is worth more than the exit it precedes, because it removes the short-lease cap-rate "
            "penalty (A16) and converts a decaying asset back into a long-dated income stream. Approach the "
            "tenant's real-estate group while same-store sales are recovering &#8212; from &#8722;7.4% to "
            "&#8722;1.1% (S12, S13) &#8212; because that is when a franchisee will commit capital and a "
            "landlord has leverage. Do it well before any contractual renewal notice deadline, which is "
            "currently unknown (F-01)."
        ),
    },
    {
        "step": "4",
        "title": "If the tenant commits: renew, then exchange out on a planned horizon.",
        "body": (
            "This is the highest risk-adjusted outcome in the model (strategy S7, and the best strategy at "
            "risk aversion &#947;=4). The point of renewing is not to hold forever. It is to be holding a "
            "<em>long-lease, low-friction</em> asset at the moment you choose to exchange it, because a box "
            "with ten years of term trades to a different buyer pool at a tighter cap rate than the same box "
            "with four years left."
        ),
    },
    {
        "step": "5",
        "title": "If the tenant will not commit: exchange out before the term erodes.",
        "body": (
            "If renewal is refused, the asset is on a clock and the clock is priced. Sell into a &#167;1031 "
            "while four to six years of term remain, not after. The cost of waiting is visible in the exit "
            "scan: cumulative exposure to at least one shock rises from 11.4% at a 2032 exit to 16.6% at "
            "2035, and the cap-rate penalty widens every year in between. Do not wait for certainty. The "
            "market charges for it."
        ),
    },
    {
        "step": "6",
        "title": "Use the exchange to fix the concentration, not to replicate it.",
        "body": (
            "The real risk in this file is not the tenant, the cap rate or the wildfires. It is that one "
            "individual's wealth is concentrated in one box, in one county, whose population is projected to "
            "fall by 240,800 school students over ten years (S09) and which has just absorbed the largest "
            "urban fire loss in its history (S21, S22). A &#167;1031 into a diversified set of net-lease "
            "assets, or into a professionally managed Delaware Statutory Trust, keeps the deferral and "
            "removes the single-asset, single-metro bet. If the owner will not diversify, the case for "
            "exiting earlier gets materially stronger."
        ),
    },
]

RISK_BY_DECISION = [
    {
        "decision": "Sell now, for cash",
        "upside": "Certainty. Liquidity. Removes tenant, wildfire, seismic and regulatory exposure in one transaction.",
        "downside": (
            "Surrenders roughly a third of accumulated appreciation to tax. Pays Measure ULA if the price "
            "exceeds $5.4 million &#8212; a cliff, so a $5.45 million sale nets less than a $5.39 million "
            "sale. Gives up the income stream with no replacement asset, so the proceeds must be redeployed "
            "into a fully taxed environment."
        ),
        "verdict": "Dominated. Ranked last or near-last on risk-adjusted wealth in every scenario tested.",
        "severity": "high",
    },
    {
        "decision": "Sell now, via &#167;1031 exchange",
        "upside": (
            "Defers the entire capital gain, removes single-asset and single-metro concentration, and has "
            "the lowest dispersion of outcomes of any strategy modelled. Certainty of execution is high."
        ),
        "downside": (
            "Requires identifying replacement property inside tight statutory deadlines, and the replacement "
            "must be bought competitively in the same market. Deferral is not elimination &#8212; the tax "
            "follows the replacement asset. Transaction costs are paid twice."
        ),
        "verdict": "Strong. Best outcome at high risk aversion among the immediate-exit strategies.",
        "severity": "low",
    },
    {
        "decision": "Hold to lease expiry and decide then",
        "upside": "Keeps every option open and pays nothing today.",
        "downside": (
            "The worst of both worlds: the cap-rate penalty (A16) widens as term runs down, so the asset "
            "is worth less each year for a reason unrelated to the market. Risk of a shock accumulates "
            "with time held &#8212; 11.4% cumulative by 2032 and 16.6% by 2035 on assumption A13. Deciding "
            "late means deciding with less leverage."
        ),
        "verdict": "Avoid. Dominated by deciding now in either direction.",
        "severity": "high",
    },
    {
        "decision": "Renew, then hold long",
        "upside": (
            "Highest median outcome. Captures rent growth above contract escalation (A04 versus A03), "
            "removes the short-lease cap-rate penalty, and defers all tax for as long as the asset is held."
        ),
        "downside": (
            "Concentrates wealth further into one asset in a county losing population. Extends exposure to "
            "a hazard class that produced two catastrophic events in one week in 2025. Liquidity falls to "
            "zero for the hold period. Requires the tenant to remain solvent for fifteen-plus years."
        ),
        "verdict": "Best on median and at low risk aversion. Best overall once paired with a deferred exit.",
        "severity": "medium",
    },
    {
        "decision": "Renew, then exchange out on a planned horizon",
        "upside": (
            "Takes the renewal gain and the deferral gain together. Highest risk-adjusted outcome in the "
            "model (strategy S7, best at risk aversion &#947;=4). Converts a decaying short-lease asset "
            "into a saleable long-lease asset before selling it."
        ),
        "downside": (
            "Depends on the tenant actually renewing (A05 = 62%). Requires active management of both the "
            "lease negotiation and the exchange calendar. Two things must go right instead of one."
        ),
        "verdict": "Recommended, conditional on a tenant renewal commitment.",
        "severity": "medium",
    },
]

BLACK_SWANS = [
    {
        "name": "Wildfire reaching the urban core",
        "evidence": (
            "January 2025: 16,263 structures destroyed across the Palisades and Eaton fires; 29 confirmed "
            "civilian deaths; $9 billion removed from the 2026 assessment roll for wildfire relief "
            "(S21, S22, S25)."
        ),
        "transmission": (
            "Rent interruption while the site is closed, smoke and ash remediation, utility outage, "
            "insurance repricing across the whole county, and a post-event cap-rate widening that hits "
            "every asset in the region regardless of whether it burned."
        ),
        "modelled": "Case B3 applies a single-event shock in 2031. It costs the hold strategy about $6.8 million of terminal wealth on a $6.5 million asset.",
        "mitigation": "Verify the parcel's fire hazard severity zone and brush-clearance obligation. Confirm the tenant's insurance is replacement-cost and that rent abatement is covered by business-interruption cover, not by the landlord.",
    },
    {
        "name": "Major seismic event",
        "evidence": (
            "Los Angeles County sits astride the southern San Andreas and a dense network of thrust faults. "
            "The specific 30-year probabilities could not be confirmed from a USGS endpoint during this "
            "session and are therefore published as unverified (F-04) rather than asserted."
        ),
        "transmission": (
            "Physical damage, mandatory retrofit, months of closure, and &#8212; critically &#8212; a "
            "county-wide insurance market shock. A quick-service box is a light-frame structure; the "
            "greater risk is the site's parking and canopy, and the tenant's ability to reopen."
        ),
        "modelled": "Not separately modelled. Its economics resemble case B3 with a lower recovery ratio, because seismic damage is less uniformly insured than fire.",
        "mitigation": "Obtain a seismic assessment. Establish whether the building is non-ductile concrete or soft-story, which would create a mandatory capital event.",
    },
    {
        "name": "Cap-rate dislocation",
        "evidence": (
            "Long-end Treasury yields are 4.84% at 10 years while the policy rate is 3.75&#8211;4.00%, and "
            "two FOMC members dissented in favour of <em>raising</em> rates (S01, S02). The term premium is "
            "positive and rising."
        ),
        "transmission": (
            "Net-lease cap rates are priced off the long end. A 175bp widening compresses asset value by "
            "roughly a quarter with no change in rent."
        ),
        "modelled": "Case B4 applies +175bp. It costs the 10-year hold about $3.6 million of terminal wealth and makes the immediate &#167;1031 exit the better choice.",
        "mitigation": "This is the strongest argument for selling into strength. It is also the reason not to sell for cash &#8212; a dislocation is precisely when you want deferral, not a tax bill.",
    },
    {
        "name": "Tenant insolvency or strategic exit from the market",
        "evidence": (
            "The tenant closed 86 units in fiscal 2025 and guided to 50&#8211;100 more in fiscal 2026; it "
            "sold Del Taco; it discontinued its dividend; its CEO is interim; and its franchise-level margin "
            "fell to 37.4% with bad-debt expense rising (S12, S13)."
        ),
        "transmission": (
            "Rejection of a renewal option, followed by dark rent for 9&#8211;36 months, tenant "
            "improvements, and a leasing commission &#8212; about 7.5% of value plus lost rent (A06, A07). "
            "A dark box also invites vandalism and municipal nuisance enforcement."
        ),
        "modelled": "Case B2 assumes vacancy at expiry. It costs the hold strategy about $1.0 million. That is modest only because the site has strong residual land value; the real cost is the re-leasing calendar, which the model cannot observe.",
        "mitigation": "Confirm the guarantor structure before renewal. A franchisee guarantee is not a corporate guarantee, and the model treats the difference as invisible.",
    },
    {
        "name": "Regulatory shock to the tenant's cost base",
        "evidence": (
            "California's fast-food minimum wage has been $20.00 per hour since April 2024, applying to any "
            "limited-service chain of 60 or more establishments nationwide, including franchisees. A "
            "standing Fast Food Council can raise it again at any time, and the general state minimum "
            "rose to $16.90 on 1 January 2026 with no tip credit permitted (S19, S20)."
        ),
        "transmission": (
            "A wage floor that rises faster than menu prices compresses franchisee margin above the rent "
            "line. Margin compression is what precedes renewal refusal, not sales decline."
        ),
        "modelled": "Not a discrete case; it enters through assumption A05 (renewal probability) and A12 (pricing-power offset).",
        "mitigation": "Structure any renewal with fixed, contractually certain escalators rather than CPI linkage, so the landlord's income does not depend on the tenant's ability to pass through wage costs.",
    },
    {
        "name": "Fiscal and tax-base erosion",
        "evidence": (
            "Downtown office value declines and wildfire relief both subtracted from the 2026 roll, and the "
            "county applied the maximum 2% Proposition 13 inflation factor only because state CPI exceeded "
            "the cap (S15, S25). Los Angeles city assessed value is $926.1 billion of a $2.367 trillion "
            "county roll."
        ),
        "transmission": (
            "A weaker commercial tax base pushes the county and city toward higher rates, parcel taxes and "
            "fees &#8212; and toward Measure ULA-style instruments. Every incremental transfer tax lands "
            "directly on the owner's exit proceeds."
        ),
        "modelled": "Not modelled as a discrete case, because the transfer-tax rates are statutory today. It is the reason to assume exit costs will be higher, not lower, in future.",
        "mitigation": "Model exit on today's rates and treat the 2026 ULA thresholds as a floor. They are indexed to Chained CPI and will be higher in 2030.",
    },
]

METHODOLOGY_NOTES = [
    {
        "title": "What 'verified' means here",
        "body": (
            "A value is marked <strong>verified</strong> only if it was read on the publishing agency's own "
            "domain &#8212; federalreserve.gov, home.treasury.gov, sec.gov, bls.gov, edd.ca.gov, census.gov, "
            "dof.ca.gov, dir.ca.gov, leginfo.legislature.ca.gov, fire.ca.gov or irs.gov. Values that come "
            "from a government body but were read through a reproduction are marked "
            "<strong>verified (secondary)</strong> and carry the caveat on the source record. Values that "
            "only appear in commercial or media sources are marked <strong>unverified</strong>, are blanked "
            "out of the tables, and are published on the Flagged for Review page with their links."
        ),
    },
    {
        "title": "Why the model is scale-invariant",
        "body": (
            "The property's price, rent, basis and lease terms are private and were never supplied. Rather "
            "than invent them, the engine expresses current rent as a going-in cap rate on value and reports "
            "every result as a return on the capital employed. Three property-value bands are run "
            "($4.0M, $6.5M, $12.0M) specifically because they straddle the two Measure ULA thresholds, so the "
            "tax cliff is visible rather than averaged away. The ranking of strategies is stable across all "
            "three bands, which is the point: the conclusion does not depend on knowing the property's price."
        ),
    },
    {
        "title": "Why terminal wealth rather than IRR",
        "body": (
            "A raw IRR cannot compare a 2026 exit with a 2052 exit &#8212; it ignores what happens to the "
            "cash in between. The primary metric is therefore the compound annual return on deployed capital "
            "measured at a common horizon, with all interim cash reinvested, the property eventually "
            "liquidated, and all taxes paid including tax on reinvestment growth. A secondary metric reports "
            "net after-tax sale proceeds in the exit year, because that is the figure that determines "
            "whether a replacement asset can be bought."
        ),
    },
    {
        "title": "Risk adjustment",
        "body": (
            "Outcomes are ranked on three measures: the 5th-percentile terminal wealth, the mean of the worst "
            "5% of outcomes (conditional value at risk), and a CRRA certainty equivalent at risk aversion "
            "2 and 4. The certainty equivalent is the guaranteed amount a risk-averse owner would accept "
            "instead of the gamble, so it answers the user's actual brief &#8212; a manageable level of risk "
            "in exchange for growth &#8212; rather than simply maximising the median."
        ),
    },
    {
        "title": "Reproducibility",
        "body": (
            "The Monte Carlo is seeded (seed 20261106) and drawn entirely from the Python standard library. "
            "Re-running <code>python3 tools/model.py</code> reproduces every figure on the Projection page "
            "exactly. That is deliberate: the model's job is to be checkable, not impressive."
        ),
    },
]

PRIVACY_POINTS = [
    {
        "title": "Placeholders only",
        "body": (
            "The property is referred to as <strong>SP-01</strong> throughout. No street address, parcel "
            "number (AIN), owner name, tenant-unit identity, rent figure, lease date beyond the supplied "
            "window, or contact detail appears anywhere in this repository, its data files, its build "
            "scripts, its commit history, or this site."
        ),
    },
    {
        "title": "Analysis at submarket granularity",
        "body": (
            "Every dataset is county, city or metro level. The decision was deliberately built at that "
            "granularity so that the analysis carries no parcel-level information that could be used to "
            "re-identify the asset. The trade-off is real and is disclosed: trade-area demand, traffic "
            "counts, school catchment and zoning cannot be evaluated without the address, and those rows are "
            "blank and flagged rather than guessed."
        ),
    },
    {
        "title": "Personal financial data was never requested",
        "body": (
            "The owner's basis, capital gains bracket, ownership structure and debt position are unknown. "
            "Rather than ask for them, the model exposes each as a stated scenario parameter with a range, "
            "and reports results across that range. The sensitivity table shows which of these actually "
            "change the answer."
        ),
    },
    {
        "title": "What would change if the address were supplied",
        "body": (
            "Parcel size and zoning would fix redevelopment yield; the fire hazard severity zone and FEMA "
            "flood zone would fix hazard exposure; traffic counts and trade-area population would fix demand; "
            "the school catchment would fix the family-formation signal. Each of these is listed in the "
            "Site-Specific Variables table with a blank value and a review flag. None of them changes the "
            "ranking of the seven strategies, because that ranking is driven by tax and lease term rather "
            "than by site characteristics."
        ),
    },
]
