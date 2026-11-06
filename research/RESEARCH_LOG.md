# Research Log

The complete trail of what was queried, what was found, what was accepted and
what was rejected. This file exists so a reviewer can see the *search*, not just
the result — including the dead ends, because those bound what the analysis can
claim.

**Session:** `arena-d989a5c6-jack3` · **Conducted:** 2026-11-06 (UTC)

Data modules: [`../data/`](../data/) · Source register:
[`../decision-file/sources.html`](../decision-file/sources.html) · Verification report:
[`../VERIFY.md`](../VERIFY.md)

---

## Domain 1 — The tenant (Jack in the Box Inc.)

| Step | Route | Outcome |
|---|---|---|
| 1 | SEC EDGAR, CIK 0000807882 | Registrant identity confirmed: JACK IN THE BOX INC, Delaware, SIC 5812, file no. 001-09390, formerly FOODMAKER INC /DE/ |
| 2 | Form 10-K filing list | FY2025 10-K located, filed 2025-11-19, acc-no 0000807882-25-000072. **FY2026 10-K not yet filed** as of 2026-11-06 (expected mid/late November) |
| 3 | Form 10-Q filing list | Q3 FY2026 10-Q located, filed 2026-08-12, acc-no 0000807882-26-000091 |
| 4 | Form 8-K filing list | Q3 FY2026 earnings 8-K located, same day, acc-no 0000807882-26-000090. Also a June 2026 refinancing 8-K (Items 1.01, 1.02, 2.03, 8.01) |
| 5 | Read FY2025 10-K **Item 2 Properties** | **The most valuable single retrieval in the project.** Full real-estate ownership table for both brands. Initially mis-attributed between the Del Taco and Jack in the Box column pairs; re-read and corrected |
| 6 | Read FY2025 10-K lease and franchise disclosures | Initial term generally 20 years; options exercisable **at the company's sole discretion**; ~13% of leases carry contingent rent of 1–10% of gross sales; fixed rent with cost-of-living index adjustments plus taxes, insurance and other expenses; development cost $1.3M–$1.9M excluding land; prototype ~1,372 sq ft |
| 7 | Read FY2025 10-K risk factors | Issuer states that closing a leased restaurant may leave it committed to base rent for the balance of the term |
| 8 | Read FY2025 10-K real-estate strategy | $19.9M of property sale proceeds; **no sale-leasebacks in FY2025**; purchases of property intended for sale/leaseback fell $15.5M; franchisees are offered the chance to buy the property they occupy |
| 9 | Read Q3 FY2026 8-K / earnings release | Full quarterly financials; 2,115 restaurants; 40 closures in the first three quarters; $244M cumulative debt reduction since April 2025; interim CEO |
| 10 | Read Q3 FY2026 10-Q | **The decisive finding:** the closure programme is progressing more slowly than expected *because franchisees must evaluate lease obligations before closing* |
| 11 | Locate the "JACK on Track" 8-K (2025-04-23) | EDGAR `browse-edgar` **ignored the `dateb` parameter** and returned the ten most recent filings instead. Route changed: recovered via search and via the FY2025 10-K's own description of the programme |
| 12 | Programme terms | 150–200 restaurant block closure; *"a majority of which have been in the system for over three decades"*; 80–120 to close by 2025-12-31; **the remainder closing "based upon respective franchise agreement termination dates"**; dividend discontinued; Del Taco strategic alternatives launched |
| 13 | Credit ratings | **Rejected.** Rating agencies are private issuers, not official sources. No rating is published anywhere in this deliverable |

**The decisive analytical finding.** Steps 10 and 12 combine into the central
insight of the whole project: the 2030–2035 lease expiry coincides with the window
in which the block-closure programme terminates the remaining underperforming
restaurants *upon their respective franchise agreement termination dates*, and
those targets are disproportionately **30+ year-old sites**. A Jack in the Box
restaurant whose lease expires 2030–2035 sits squarely inside the closure
programme's own targeting logic. This anchors the risk register (`R-01`) and the
recommendation.

**Rejected in this domain:** net-lease aggregator tenant profiles (cap rates,
prices, franchisee entity names), analyst ratings and price targets, media
earnings summaries, transcript aggregators. All were consulted only to locate
primary sources. **No value from any of them is asserted anywhere.** The
aggregator cap rates were the reason `F-02` exists: they confirmed that private
data is plentiful and official data is absent.

---

## Domain 2 — Demographics and income

| Step | Route | Outcome |
|---|---|---|
| 1 | **Census Data API** `api.census.gov/data/2024/acs/acs5?...&for=county:037&in:state:06` | **FAILED — key required.** Both the county and place variants redirected to `missing_key.html`. No key obtainable in this environment. **Not retried.** |
| 2 | **Server-rendered QuickFacts** `census.gov/quickfacts/losangelescountycalifornia` | **Succeeded.** Four chunks; the full county variable set harvested |
| 3 | `census.gov/quickfacts/losangelescitycalifornia` | **Succeeded.** Four chunks; full city variable set harvested |
| 4 | `census.gov/quickfacts/losangeleslongbeachanaheimmsacalifornia` | Consulted for the MSA; the MSA QuickFacts set is thinner, so employment data was taken from BLS instead |
| 5 | City of LA EWDD Annual Plan PY2024-25 Tab 5 (LAEDC, May 2024) | **Succeeded**, 13 chunks. Provided 2022 ACS one-year characteristics for California, LA County and the City of LA side by side, plus the DOF decline forecast |

**Irregularities found in the source data itself.**

- **City race shares do not reconcile.** LA city: White alone 33.4 + Black 8.4 +
  American Indian/Alaska Native 1.3 + Asian 12.1 + Native Hawaiian/Pacific
  Islander 0.2 + Two or More 18.9 = **74.3%**. LA County equivalent sums to
  **99.8%**. One or more city values appear mis-extracted. **The city race
  breakdown is omitted entirely rather than published with a possibly wrong
  figure** (`F-12`). Decision-relevant variables are unaffected.
- **`[X]` markers.** LA city `Building Permits` and `Housing units` are not
  published at that geography. Left blank with the QuickFacts note reproduced;
  county values **never substituted** (`F-13`).
- **Vintage mixing.** Population is Vintage 2025 (July 2025); most other fields are
  ACS 2020–2024 five-year; spending data is the 2022 Economic Census. The Census
  Bureau's own guidance warns these are not comparable. Every row carries its own
  `as_of` (`F-14`).

---

## Domain 3 — Employment, wages and prices

| Step | Route | Outcome |
|---|---|---|
| 1 | `bls.gov/regions/west/ca_losangeles_msa.htm` | Located the regional hub and the current products |
| 2 | **`bls.gov/news.release/pdf/metro.pdf`** | **Succeeded.** USDL-26-1618, September 2026 data. Confirmed the MSA labour-force series directly rather than relying on a search snippet — which changed the figures from snippet-only to VERIFIED |
| 3 | **`bls.gov/regions/west/summary/blssummary_losangeles.pdf`** | **Succeeded**, single chunk. **The single richest LA source found in the whole project:** LAUS by area, CES sector payrolls Aug 2026, QCEW Q1-2026 wages, CPI-U Aug 2026, Consumer Expenditure 2023-24, OEWS May 2025, ECEC Jun 2026, ECI LA–Long Beach CSA |
| 4 | County Business Patterns via QuickFacts | Employer establishments, employment and annual payroll at county and city level |
| 5 | **FRED** `LOSA106UR` | **Rejected as a citation.** BLS-sourced and smoothed/seasonally adjusted, so a different series from the LAUS published figure. Cite BLS, never FRED |

**The finding that reframes the labour market.** Unemployment fell 5.5% → 4.4%
year on year, which reads as improvement. But the civilian labour force fell
6,768,502 → 6,646,903 over the same period — about 121,600 fewer people. A falling
rate caused by people leaving the labour force is not an expanding economy. Both
figures are published together, deliberately, so the reader cannot take the
favourable one alone.

---

## Domain 4 — Long-range projections

This domain produced the most important *negative* result in the project.

| Step | Route | Outcome |
|---|---|---|
| 1 | **`dof.ca.gov/forecasting/demographics/projections/`** | **Succeeded.** Confirmed the current official series: Baseline 2024; Vintage 2026 released 2026-03-13; county file `P2A_County_Total.xlsx`; also `P1A_State_Total.xlsx`, `PCC_Components_of_Change.xlsx`, `P4_HHProjections_B2024.xlsx`; methodology PDF; ArcGIS visualisation |
| 2 | Attempt to read the projected values | **FAILED.** DOF publishes county projections **only as `.xlsx`**. `fetch_page` cannot parse a spreadsheet, and the build environment has no network route to `dof.ca.gov` to download one. **The 2030, 2035 and 2040 county values are left blank** (`F-04`) |
| 3 | Third-party restatements of the DOF series | **Rejected.** They disagree by **more than 100,000 residents for the same year across vintages** (one gives 2030 = 9,727,305; another gives 9,867,515). Publishing either would have been a fabrication dressed as a citation |
| 4 | SCAG demographics table | **Succeeded.** Official MPO document; provided the earlier Connect SoCal projection to document the conflict |
| 5 | SCAG successive plan vintages | Recovered from the same official source family: 2024–2050 projected change of **+14.41%** (Connect SoCal 2020) → **+10.15%** (Connect SoCal 2024) → **negative** (preliminary Connect SoCal 2050). Every revision moved down |

**The conflict, and how it was handled.** SCAG's Connect SoCal 2020 plan projected
LA County to **grow 16.6%** to 11,674,000 by 2045. The California Department of
Finance projection cited in the City of Los Angeles 2024 workforce plan has the
county **falling** to about 9.3 million by 2040 and 8.3 million by 2060. Two
official bodies, opposite signs, same geography.

This was **not** resolved silently, averaged, or chosen between on convenience.
Both are published side by side, the observed Census measurement (−3.2% since the
2020 estimates base) is identified as the only line in the table that is
measurement rather than forecast, and **the analysis underwrites to the observed
trend** with growth treated as upside only.

---

## Domain 5 — Physical hazards

| Step | Route | Outcome |
|---|---|---|
| 1 | **USGS UCERF3 probability FAQ** | **Succeeded, official.** LA region 30-year probabilities: 60% M6.7+, 46% M7.0+, 31% M7.5+ |
| 2 | **County of Los Angeles Eaton/Palisades anniversary fact sheet** | **Succeeded, official.** The quantitative backbone of the black-swan analysis: acreage, structures, fatalities, and the $5.2–10.1B economic output loss, ~6,800 businesses and ~47,000 workers impacted, $2.2–4.2B labour income lost, $900M–$1.6B tax revenue lost |
| 3 | CAL FIRE incident pages, Eaton and Palisades | **Succeeded.** Jurisdictional agency, dates, and the flash-flood warning issued during the Palisades Fire |
| 4 | **CRS In Focus IF12871** | **Succeeded, official.** Ten wildfires began in LA and adjacent counties on 2025-01-07; >40,000 acres; >12,000 structures; ≥24 deaths as of 2025-01-16; FMAG declarations for Palisades, Eaton and Hurst |
| 5 | CAL FIRE OSFM Fire Hazard Severity Zone maps | **Succeeded.** Statutory basis Public Resources Code §§4201–4204; the Moderate/High/Very High scheme; LA County SRA map dates; the recommended LRA map still dated 2011 |
| 6 | CAL FIRE FRAP FHSZ project page | **Succeeded.** The official parcel-level lookup route |
| 7 | **LA County Open Data LRA FHSZ layer** | **Succeeded, and important.** LA County Local Responsibility Area zones were **established in 2025**, adding Moderate and High categories where the prior map showed only Very High. Any pre-2025 determination — including one in an old title report or insurance submission — is **stale** |
| 8 | **FEMA National Risk Index** | **Partially succeeded.** The official dataset-overview page and the RAPT page were both retrieved and confirm NRI v1.20 is published through RAPT. But the **county-level numeric scores were not readable on a `fema.gov` page** in this session; they circulated only in secondary aggregators. **Every NRI dollar figure and score is therefore left blank** (`F-03`) |

**Why the FEMA blank matters more than it looks.** Secondary sources gave a
county composite score and per-hazard Expected Annual Loss figures. They were not
used — and separately, one of them made the substantive point that a county
average is useless here: most LA County census tracts have effectively zero
wildfire expected loss while a small minority carry very large losses. The correct
action is a **tract-level** query in RAPT, which requires the address. So the
blank is not merely a retrieval failure; it records that the wrong granularity was
on offer.

---

## Domain 6 — Regulatory cost floor

| Step | Route | Outcome |
|---|---|---|
| 1 | Search for the California minimum wage | **Returned conflicting third-party figures** — $16.90 vs $17.00 for the state rate, and an unannounced future city rate |
| 2 | **Escalated to `dir.ca.gov/dlse/faq_minimumwage.htm`** | **Succeeded, official and decisive.** State rate **$16.90/hr effective 2026-01-01** (2024 $16.00, 2025 $16.50). Conflict resolved |
| 3 | **`dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm`** | **Succeeded, official.** AB 1228 = Labor Code §§1474–1476; **$20.00/hr from 2024-04-01**; three-part coverage test (limited-service + chain of ≥60 US establishments + primarily immediate-consumption food); **applies to franchisees as employers**; a city may not set a fast-food-specific rate but a higher *general* local rate then governs; the council may raise it annually through **2029** capped at the lesser of 3.5% or CPI-W |
| 4 | **City of LA Office of Wage Standards** | **Succeeded, official.** Full schedule: $16.04 (2022-07-01) → $16.78 → $17.28 → $17.87 → **$18.42 (2026-07-01)**; LAMC §187.02.B/C; indexed to LA-metro CPI-W; announced February 1 each year |
| 5 | Interaction | Since $20.00 > $18.42, the **fast-food floor governs** a Jack in the Box inside the City of Los Angeles. Established from the two official pages, not assumed |
| 6 | Unincorporated LA County rate | **Not verified** on an official county page; **not published** |

This domain established the general rule applied for the rest of the project:
**never accept an aggregator number — escalate to the agency page.**

---

## Domain 7 — Discount rate anchor

| Step | Route | Outcome |
|---|---|---|
| 1 | **`home.treasury.gov` Daily Treasury Par Yield Curve Rates, 2026** | **Succeeded, official.** January 2026 observations: 1 Yr 3.47%, 2 Yr 3.47%, 3 Yr 3.55%, 5 Yr 3.74%, 7 Yr 3.95%, **10 Yr 4.19%**, 20 Yr 4.81%, 30 Yr 4.86% |

The discount rate is built from this **verified** official rate plus an
**explicitly declared** risk premium swept from 2.0% to 5.5%. The verified and
judgement components are separated in the code and labelled differently in the
output, so no reader can mistake one for the other.

---

## Domain 8 — Tax and transaction

**This domain failed, and the failure is recorded rather than papered over.**

| Step | Route | Outcome |
|---|---|---|
| 1 | IRS Topic 418 | Retrieved successfully — but it is **Unemployment Compensation**, not like-kind exchanges. Wrong topic number |
| 2 | IRS like-kind exchanges page | **HTTP 404** |
| 3 | California FTB real-estate withholding page | **HTTP 404** |
| 4 | Third-party 1031 and California tax guides | Located, and they state a California top rate of 13.3% and a 3⅓% withholding. **All rejected.** None was read on an official page |

**Disposition:** the Tax Framework page describes the **mechanisms** — federal
gain, depreciation recapture, net investment income tax, IRC §1031 and its 45/180
day deadlines, California ordinary-income treatment of gain, real-estate
withholding, deferred-gain tracking after an out-of-state exchange, Article XIII A
reassessment on change of ownership, documentary transfer tax, and transaction
friction — each linked to its official publisher, with the specific questions the
owner must resolve. **Not one rate is asserted** (`F-05`).

Publishing an unverified tax rate on a site the owner will rely on for a
seven-figure decision is precisely the failure mode this project was told to
avoid. The gap is disclosed, the official routes are given, and the action plan
requires a written opinion from a California-licensed CPA before anything is
signed.

---

## Domain 9 — Infrastructure, land use and schools

| Step | Route | Outcome |
|---|---|---|
| 1 | Metro rail extension projects | Located in secondary sources only. **Not read on an official `metro.net` project page.** No date or cost is asserted (`F-11`) |
| 2 | Sepulveda Transit Corridor | Same disposition |
| 3 | City of LA zoning / ZIMAS / Community Plan Areas | **Not queried** — the parcel is unidentified, so no CPA-level statistic is assertable (`F-08`) |
| 4 | California School Dashboard / LAUSD | **Not queried** — school data is published at school and district level, not for an unidentified parcel (`F-09`) |
| 5 | Caltrans traffic census | **Not queried** — requires the nearest station, which requires the address (`F-10`). Broker marketing material quoting counts was **rejected** as non-official |

Rather than pad this domain with unverified values, the page publishes the
**official reference routes** with an explanation of why each matters to the
decision — plus the two infrastructure conclusions that *are* supportable from
verified regional data: LA County accommodation and food services sales of
**$44,016,586,000** in 2022 (City of LA **$17,366,966,000**, 39.5% of the county
total from 39.8% of its population), and **437,788** employer establishments with
**$550.7 billion** in annual payroll.

The second is the one that matters: it establishes, from verified official data,
that the *land* sits in one of the densest employer markets in the United States
even though the *building* is a specialised ~1,372 sq ft drive-thru box. That is
why the model gives the redevelopment strategy real weight, and why the zoning
lookup is worth paying for before dismissing it.

---

## Environmental constraints on the research

These bound what any reviewer should expect to be able to reproduce here.

- **No general network access.** Outbound traffic is restricted to `github.com`,
  `codeload.github.com`, `api.github.com`, `registry.npmjs.org`, `pypi.org` and
  `files.pythonhosted.org`. `curl`/`wget` to `census.gov`, `bls.gov`, `dof.ca.gov`,
  `fire.ca.gov`, `fema.gov`, `usgs.gov` and `home.treasury.gov` **will fail**. All
  official data was obtained through the page-retrieval tool, not the shell.
- **Consequence for the design.** No live API calls at build time are possible, so
  the site is generated from a **committed, reviewed data snapshot** in which every
  row records its own `as_of` date and `source_url`. This turned a limitation into
  a property: the published figures cannot drift silently after generation.
- **The Census Data API is key-gated** and no key is obtainable. Tract-level ACS
  data was therefore unreachable, which is the granularity a single drive-thru site
  actually trades on. Recorded as a residual limitation.
- **`.xlsx` cannot be parsed** by the retrieval tool, which is why the CA DOF
  projection values are blank.

---

## Rejected sources — the full list

Consulted during research, then rejected. **No value from any of these appears in
the data snapshot or on the site**, and every one of these domains is on
`tools/check_links.py`'s blocklist so it cannot appear even by accident.

**Commercial net-lease and broker sites** — tenant profiles publishing Jack in the
Box cap rates, average sale prices, average NOI, price per square foot, building
and lot sizes, lease terms and escalation patterns; individual listings in
California, Arizona and Texas. *Rejected because:* not official sources, and they
publish **franchisee entity names and addresses**, which is a direct privacy
conflict. *Used only to establish one fact:* that private cap-rate data is
plentiful and official cap-rate data is absent — which is why `F-02` exists.

**REIT press releases** — a 2021 acquisition of an Arizona Jack in the Box
property at a disclosed going-in cash cap rate with about five years of remaining
term. *Rejected as a citation* but the structural insight was retained and is
reproduced in the model instead: **short remaining term materially widens the cap
rate a buyer demands.** That is modelled as the difference between the "today" and
"exit" cap-rate assumptions, not quoted as a comparable.

**Hazard-data aggregators** — four separate sites restating FEMA National Risk
Index v1.20 for Los Angeles County with conflicting totals. *Rejected.* The
official FEMA pages were retrieved instead and the numeric values left blank.

**Media and commentary** — regional planning commentary, city-watch blogs,
demographic analysis sites, broadcast news coverage of transit projects, trade
press coverage of construction milestones. *Rejected.* Used only to locate
official documents, never as a source of a published value.

**Financial data aggregators and analyst opinion** — earnings-call transcripts,
analyst ratings, price targets and consensus estimates. *Rejected.* The Form 8-K
furnished to the SEC the same day was used instead, which is the primary document.

**FRED** — BLS-sourced but a different (smoothed, seasonally adjusted) series from
the published LAUS figures. *Rejected as a citation*; BLS cited directly.

---

*End of research log.*
