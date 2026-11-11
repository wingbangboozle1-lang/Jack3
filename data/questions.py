"""Open questions and missing-information register for Asset A.

PURPOSE
    The published evidence tables say what is known. This module says what is
    *not* known, in the order it blocks a decision, and — for each gap — exactly
    who or what can close it and how. It exists because a decision cannot be made
    "reasonably" on regional averages: the facts that decide between selling and
    renewing are private property documents and store-level operating data.

RULES APPLIED TO EVERY ROW
    * No invented value. Column "Value now" is blank unless an official source
      establishes it; a blank cell is the honest answer, not an oversight.
    * Every row carries a source link. Where the row records an absence, the link
      is to the official register that would hold the fact (Assessor, Recorder,
      zoning, FEMA, county fire, SEC EDGAR) and the row's own text says the value
      was not retrieved. That distinction is enforced by tools/check_public.py.
    * No personal data. Nothing here asks for, stores or publishes an owner name,
      address, parcel number, account, contact detail or private financial value.
      Where a private document is required, the row names the *class* of document
      and the party that holds it, never a person.

COLUMNS
    ID    stable question identifier (Q-01 ...)
    Question    what must be answered before a decision
    Why it blocks    the specific decision that cannot be made without it
    How to close it    the concrete discovery step (document, register, requester)
    Owner of the answer    who holds the information (role, never a name)
    Status    Missing - private | Partially answered | Unverified official | Answered

Status is a fixed vocabulary so the page can be filtered and audited.
"""

COLUMNS = ["ID", "Question", "Why it blocks the decision", "How to close it",
           "Owner of the answer", "Status"]

# Each row: (id, question, why_it_blocks, how_to_close, holder, status, source_key)
ROWS = [
    ("Q-01",
     "What is the exact lease commencement date, expiration date, and every renewal-option "
     "term, notice window and deadline?",
     "The sell-versus-renew clock cannot be set from a reported 2030-2035 range. Notice "
     "deadlines can fall 12-24 months before expiry, which moves the marketing window "
     "into the past.",
     "Request the executed lease, all amendments, side letters and the estoppel. Read the "
     "renewal clause line by line and diary every notice date.",
     "Owner A / property manager (private file)", "Missing - private", "jack"),

    ("Q-02",
     "Who is the legal tenant, and is there a corporate guaranty, franchisee guaranty or "
     "letter of credit behind the rent?",
     "Investment value depends on the credit behind the lease, not on the brand on the "
     "sign. A franchisee obligor and a Jack in the Box Inc. guaranty are different risks "
     "and price at different cap rates.",
     "Read the tenant entity name and guaranty in the lease; obtain the guarantor's "
     "financial statements if a guaranty exists; confirm the store's franchisee of record "
     "with the issuer in writing.",
     "Owner A (lease); Jack in the Box Inc. franchise records (private)", "Missing - private", "jack"),

    ("Q-03",
     "What are the contractual base rent, escalation schedule, percentage-rent or reporting "
     "clauses, and reimbursable versus unreimbursed expenses?",
     "Every after-tax comparison in this file is expressed as a multiple of one year of "
     "base rent. Without the actual rent, no sale price, yield or tax figure can be "
     "computed by anyone.",
     "Pull the rent schedule and the last 12 months of rent invoices, CAM/insurance/tax "
     "reconciliations and any percentage-rent statements.",
     "Owner A (lease and rent roll)", "Missing - private", "jack"),

    ("Q-04",
     "What is the store-level operating performance: sales, rent coverage, arrears, "
     "remodel status and franchise-agreement term?",
     "The issuer's chain results (same-store sales -1.1%, 17 closures) say nothing about "
     "this restaurant. Renewal willingness is driven by the store's four-wall economics.",
     "Request the franchisee's store P&L or, at minimum, rent-coverage evidence; obtain a "
     "tenant estoppel and, if offered, a renewal letter of intent.",
     "Franchisee operator (private); issuer disclosure is chain-level only", "Missing - private", "jack"),

    ("Q-05",
     "What is the owner's tax basis, accumulated depreciation, debt, entity structure and "
     "marginal federal and California rates?",
     "Capital-gains and section 1250 recapture tax can exceed the difference between the "
     "two sale paths. The optimal route cannot be chosen before the after-tax number is "
     "known.",
     "Assemble the depreciation schedule, closing statement from acquisition, loan "
     "documents and the last two tax returns; compute after-tax proceeds per route with a "
     "CPA.",
     "Owner A / CPA (private)", "Missing - private", "irs409"),

    ("Q-06",
     "Can the owner tolerate a failed marketing period or an 18-month vacancy without "
     "forced selling?",
     "The 18-month-void stress case on the projection page removes roughly a tenth of "
     "holding value at the least convenient moment. Liquidity is private information and "
     "sets the maximum defensible risk.",
     "Document committed reserves and other income outside this asset; set a minimum "
     "acceptable net-proceeds floor and a walk-away vacancy horizon.",
     "Owner A (private)", "Missing - private", "fred"),

    ("Q-07",
     "What precise location and jurisdiction is the parcel in - City of Los Angeles, or "
     "another incorporated city or unincorporated county area inside 'central Los Angeles'?",
     "The 0.45% city transfer tax and Measure ULA (4% above $5.4m, 5.5% at $10.9m) apply "
     "only inside the city; a county-island parcel pays neither. The whole after-tax "
     "comparison changes with jurisdiction.",
     "One parcel lookup resolves it: the county Assessor parcel report and the Registrar-"
     "Recorder grant deed show the taxing jurisdiction, then the city zoning portal "
     "confirms it. The result is retained privately; it is not published.",
     "LA County Assessor / Recorder (official, private retrieval)", "Unverified official", "countytax"),

    ("Q-08",
     "What is the current zoning, general plan land use, and the legal status of the "
     "drive-through (conforming or legally non-conforming)?",
     "If the drive-through is non-conforming, a lapse or rebuild can lose it permanently - "
     "which destroys the residual value a buyer is underwriting, and closes the "
     "re-tenanting route.",
     "Run the parcel through the city zoning information system and request a zoning "
     "verification letter or certificate of occupancy history from the Department of "
     "Building and Safety.",
     "City of Los Angeles Planning / LADBS (official, private retrieval)", "Unverified official", "zoning"),

    ("Q-09",
     "What are the parcel's effective hazard designations: FEMA flood zone, CAL FIRE fire "
     "hazard severity zone and CGS seismic/liquefaction zone?",
     "Regional hazard records (2025 fires, USGS ShakeOut) are not parcel risk. Insurance "
     "pricing, deductibles and lender requirements key off the parcel designations.",
     "Pull the effective FEMA Flood Insurance Rate Map panel, the adopted CAL FIRE FHSZ "
     "map for the parcel and the CGS seismic-hazard zone report; order a geotechnical "
     "screen if the parcel sits in a mapped zone.",
     "FEMA / CAL FIRE OSFM / California Geological Survey (official, private retrieval)",
     "Unverified official", "flood"),

    ("Q-10",
     "What insurance is actually in force - limits, deductibles, exclusions, rent-loss "
     "period and replacement-cost basis?",
     "Post-catastrophe repricing and non-renewal are regional, so the policy, not the "
     "hazard map, determines the transferable risk. An uninsured loss is the one event "
     "that can end the plan.",
     "Obtain the current policy, declarations page, loss runs and the insurer's wildfire "
     "and earthquake endorsements; ask a broker for a 2030-2035 renewability view in "
     "writing.",
     "Owner A / insurance broker (private)", "Missing - private", "fire"),

    ("Q-11",
     "How large is the site, and what does an independent residual-land-value analysis say "
     "the land is worth for its best permitted alternative use?",
     "Redevelopment and ground-lease options in this file are unranked because residual "
     "value was never established. Without it, 'sell versus hold' ignores the land option.",
     "Obtain the parcel area and dimensions from the assessor record, then commission a "
     "residual-value analysis using permitted density and current construction cost.",
     "Owner A / appraiser (private), fed by official parcel data", "Missing - private", "zoning"),

    ("Q-12",
     "Which comparables have actually sold - net-lease QSR assets in central Los Angeles, "
     "with price, cap rate, remaining term and tenant credit?",
     "No government agency publishes cap rates. The base 5.5% and the 5.0-6.5% sweep on "
     "the projection page are disclosed assumptions, not market evidence, so the sale "
     "price remains unknown to this file.",
     "Request a broker opinion of value with closed comparable sales; verify each "
     "comparable against public records (grant deed, transfer-tax declaration) before "
     "relying on it.",
     "Licensed broker / appraiser (private market evidence)", "Missing - private", "irs"),

    ("Q-13",
     "Which school attendance areas serve the site, and how do those campuses perform on the "
     "state indicators?",
     "School quality is a stated decision factor and is currently unanswerable: district "
     "aggregates cannot be attributed to a parcel, and no campus has been identified.",
     "From the confirmed address, use the district's school-locator, then read each "
     "campus on the California School Dashboard and DataQuest.",
     "LAUSD (official), CDE Dashboard (official)", "Unverified official", "dashboard2026"),

    ("Q-14",
     "What is the block-level trade area - population, households, daytime workers and "
     "income within a 1-3 mile or 10-minute drive?",
     "City and county totals cannot show whether *this* trade area is growing. Every "
     "demand statement in this file is regional context, not site demand.",
     "Draw the catchment from the confirmed address and pull ACS 5-year estimates for the "
     "intersecting tracts or block groups, keeping margins of error.",
     "U.S. Census Bureau (official, private retrieval)", "Unverified official", "city"),

    ("Q-15",
     "Who are the direct competitors within the catchment, and what development or "
     "redevelopment is approved or pending nearby?",
     "Competitive supply and pipeline change store sales, which drive renewal willingness. "
     "No authenticated competitor or pipeline dataset was obtained.",
     "Combine a field survey with the city's permit and planning-case search for the "
     "surrounding area, and the assessor's new-construction roll additions.",
     "City of Los Angeles (official), field survey (private)", "Missing - private", "zoning"),

    ("Q-16",
     "Is the reported 2030-2035 expiry a lease expiration, a renewal-option window, or a "
     "franchise-agreement date?",
     "These are different events with different consequences. An earlier companion report "
     "in this repository equated a franchise termination date with the lease expiry, which "
     "the issuer does not establish.",
     "Compare the lease dates with the franchise agreement dates in the private file; they "
     "are separate contracts and neither is public.",
     "Owner A (lease); franchisee (franchise agreement)", "Missing - private", "closure"),

    ("Q-17",
     "What are the LAUSD graduation rates for the 2025-26 cohort on a charter-inclusive "
     "basis, matching the Dashboard's district-wide measure?",
     "The published 86.2% four-year and 87.6% combined figures could only be read from the "
     "2026 Dashboard, whose tables load in the browser and are not present in the served "
     "page. The server-rendered CDE DataQuest report for the same year returns 87.4% for "
     "LAUSD with charter schools excluded by default (2025-26 school year).",
     "Re-read the 2026 Dashboard in a browser, or the Graduation Rate Additional Report "
     "once CDE updates it (CDE states the Additional Reports will carry 2026 data by "
     "2026-12-15), and record the exact filter set used.",
     "California Department of Education (official)", "Unverified official", "dashboard2026"),

    ("Q-18",
     "Is the 2026 Assessment Roll growth 4.42% or 42%?",
     "The official county release states 4.42% in its narrative ($96bn on $2.272tn) but "
     "prints '42%' in its highlights bullet. This file publishes 4.42% because the dollar "
     "change and the narrative agree; the page is internally inconsistent.",
     "Treat 4.42% as the operative figure; ask the Assessor's public information office to "
     "correct the bullet. No decision should rest on the typo.",
     "LA County Assessor (official)", "Partially answered", "roll"),

    ("Q-19",
     "What will the issuer's full-year FY2026 results show when released on 2026-12-09?",
     "The tenant evidence here is Q3 FY2026 (quarter ended 2026-07-05). A closing trend - "
     "fewer closures, better franchise margin - would weaken the argument for selling "
     "early.",
     "Re-read the Q4/FY2026 release and the FY2026 Form 10-K from SEC EDGAR after "
     "2026-12-09 and refresh the tenant rows.",
     "Jack in the Box Inc. (issuer)", "Unverified official", "q4"),

    ("Q-20",
     "Does the sale contract permit assignment, and does the tenant hold any right of first "
     "refusal, recapture or consent over a sale?",
     "A right of first refusal or consent requirement can delay or defeat the sale track, "
     "and an assignment restriction can bar a section 1031 exchange structure.",
     "Read the assignment/transfer clause, subordination and SNDA in the lease; confirm "
     "lender consent requirements if debt is assumed.",
     "Owner A (lease and loan documents)", "Missing - private", "irs"),
]

# Questions that are fully answered by an official source in this file, recorded so
# the register is complete rather than one-sided. Each must name the answer and link
# the page that establishes it.
ANSWERED = [
    ("A-01", "What are the state and local transfer-tax rates that apply to a sale?",
     "City of Los Angeles base tax 0.45% ($2.25 per $500) plus county documentary "
     "transfer tax 0.11% ($0.55 per $500); Measure ULA adds 4% above $5,400,000 and "
     "5.5% at or above $10,900,000 for closings after 2026-06-30.",
     "City of Los Angeles Office of Finance; LA County Registrar-Recorder", "ula"),
    ("A-02", "What is the California property-tax framework that a hold preserves?",
     "1% general levy on assessed value, with a 2% maximum annual increase and "
     "reassessment on change of ownership or completed new construction.",
     "LA County Assessor (Proposition 13)", "assessor"),
    ("A-03", "How is a sale gain taxed, and can it be deferred?",
     "California has no preferential capital-gains rate (taxed as ordinary income); "
     "federal long-term rates are 0/15/20%, unrecaptured section 1250 gain is capped at "
     "25%, and a section 1031 exchange defers the gain on qualifying real property.",
     "IRS Topic 409; California FTB; IRS like-kind exchange guidance", "irs409"),
    ("A-04", "What minimum wage applies to a covered fast-food restaurant?",
     "$20.00 per hour for covered fast-food employees from 2024-04-01 (AB 1228); the "
     "state minimum is $16.90 per hour from 2026-01-01. The DIR page does not state a "
     "2027 rate.",
     "California Department of Industrial Relations", "wage"),
]
