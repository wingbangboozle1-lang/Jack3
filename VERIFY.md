# Verification Report

**Project:** Jack3 — Central Los Angeles NNN property decision file
**Session:** `arena-d989a5c6-jack3`
**Data snapshot:** 2026-11-06 (UTC)
**Repository:** `wingbangboozle1-lang/Jack3`
**Live site:** <https://wingbangboozle1-lang.github.io/Jack3/>

This document records how every figure in the deliverable was obtained, what was
accepted as evidence, what was rejected, what could not be verified, and how any
reviewer can reproduce or check the result.

---

## 1. Results

| Check | Result |
|---|---|
| Pages generated | **23** |
| Total HTML emitted | **487,407 bytes** |
| CSV exports of the data snapshot | **23** |
| External and internal links emitted | **1,013** |
| Distinct link hosts | **30** |
| **Non-official hosts** | **0** |
| `tools/check_links.py` | **PASS** (exit 0) |
| `tools/pii_scan.py` — files scanned | **64** |
| `tools/pii_scan.py` — findings | **0** |
| `tools/pii_scan.py` | **PASS** (exit 0) |
| Data rows carrying an official source link | see `docs/index.html` (computed at build time) |
| Data rows published blank because unconfirmable | see `docs/index.html` (computed at build time) |
| Items on the Flagged for Review page | **15** |
| Items blocking publication | **0** |
| Site builds without network access | **YES** — no runtime fetches of any kind |

### Reproduce

```bash
python3 -m model.projection      # deterministic; no network, no randomness
python3 build_site.py            # data/ + model/ -> docs/
python3 tools/check_links.py     # must exit 0
python3 tools/pii_scan.py        # must exit 0
```

---

## 2. Evidence classes

Every figure in `data/*.py` and every claim on the site carries one of six
labels. The label determines how it is rendered.

| Label | Meaning | Rendering rule enforced by `build_site.py` |
|---|---|---|
| `VERIFIED` | Read directly on an official `.gov` page, or in a filing the issuer made with the SEC, during this session | Value printed; source link printed; green badge |
| `MODELLED` | Arithmetic output of `model/projection.py` from declared assumptions | Value printed; labelled as model output, never as observation |
| `JUDGEMENT` | Qualitative assessment by this analysis | Value printed; reasoning traceable to cited facts; rating labelled as opinion |
| `UNVERIFIED` | Appeared only in a secondary source, or the official page could not be retrieved | **Value forced blank**; `[ blank — unverified ]` printed; amber badge; row highlighted |
| `NO OFFICIAL SOURCE` | No government body publishes this figure at all | **Value forced blank**; amber badge; explained inline |
| `INPUT REQUIRED` | Property-specific or personal | **Value forced blank**; placeholder token printed; collected in the Input Register |

The blanking is enforced in code, not by care. `build_site.py:value_cell()`
returns the blank marker whenever `value` is `None` or empty, and
`table()` applies `class="unverified"` to any row whose status is not
`VERIFIED`. It is not possible for an unverified row to render a number.

---

## 3. Source hierarchy applied

**Tier 1 — primary federal and state agencies.**
U.S. Securities and Exchange Commission (EDGAR) · U.S. Census Bureau · U.S.
Bureau of Labor Statistics · U.S. Geological Survey · U.S. Department of the
Treasury · Federal Emergency Management Agency · CAL FIRE (including the Office
of the State Fire Marshal and the Fire and Resource Assessment Program) ·
California Department of Industrial Relations · California Department of Finance
· Congressional Research Service.

**Tier 2 — county and municipal governments.**
County of Los Angeles · Los Angeles County Fire Department open data · City of
Los Angeles Office of Wage Standards · City of Los Angeles Economic and Workforce
Development Department.

**Tier 3 — the issuer itself.**
Jack in the Box Inc. earnings release. Accepted *only* because the same figures
were furnished to the SEC on Form 8-K (Items 2.02 and 9.01) the same day.

**Tier 4 — official host, third-party author.**
The City of Los Angeles EWDD Annual Plan PY2024-25, Tab 5 Economic Forecast.
Published on `ewdd.lacity.gov` but written by the LAEDC Institute for Applied
Economics under commission to the City of Los Angeles Workforce Development
Board. **Authorship is disclosed wherever this document is cited**, both in the
Source Register and inline on the Official Forecasts page.

**Rejected outright.**
Commercial brokerage listings · net-lease aggregator sites · investor forums ·
media restatements of government data · analyst ratings and price targets ·
rating-agency credit opinions · any third-party restatement of a figure that
could be read at source.

Where a third-party figure was the *only* one obtainable, the value is left blank
and the official route is given instead. This happened four times: FEMA National
Risk Index values (`F-03`), CA DOF county projections (`F-04`), tax rates
(`F-05`), and transit project dates (`F-11`).

---

## 4. Sources used

The complete register — 27 entries with publisher, filing date, accession number,
evidence tier and exactly what was taken from each — is on
[`docs/sources.html`](docs/sources.html). Principal sources:

| Publisher | Document | Used for |
|---|---|---|
| SEC EDGAR | Form 10-K, FY ended 2025-09-28, acc-no 0000807882-25-000072 | Item 2 Properties real-estate table; lease and franchise terms; same-store sales; restaurant counts; JACK on Track; Del Taco divestiture; cost structure |
| SEC EDGAR | Form 10-Q, period ended 2026-07-05, acc-no 0000807882-26-000091 | System restaurant count 2,115; closure-programme pace and its interaction with lease obligations |
| SEC EDGAR | Form 8-K filed 2026-08-12, acc-no 0000807882-26-000090 | Quarterly results and management commentary |
| U.S. Census Bureau | QuickFacts, Los Angeles County (FIPS 06037) | Full demographic, housing, income, education, labour-force, density and 2022 Economic Census variable set |
| U.S. Census Bureau | QuickFacts, Los Angeles city (FIPS 0644000) | Same set at city level; `[X]` fields recorded as not available |
| U.S. BLS | Los Angeles Area Economic Summary, updated 2026-10-05 | Unemployment by area; average weekly wages; payrolls by sector; employment trend; CPI-U; consumer expenditure; OEWS; ECI |
| U.S. BLS | Metropolitan Area Employment and Unemployment, USDL-26-1618 | MSA labour force, unemployed and rate, Sept 2026 preliminary |
| U.S. Treasury | Daily Par Yield Curve Rates, 2026 | The risk-free anchor for the discount rate |
| USGS | UCERF3 earthquake probability FAQ | 30-year M6.7+ / M7.0+ / M7.5+ probabilities |
| County of Los Angeles | Eaton and Palisades Fires anniversary fact sheet | Acreage, structures, fatalities, and the $5.2–10.1B economic impact |
| CRS | In Focus IF12871 | Count and names of the ten January 2025 wildfires; FMAG declarations |
| California DIR | Minimum Wage FAQ; Fast Food Minimum Wage FAQ | State rate $16.90 from 2026-01-01; AB 1228 $20.00 fast-food floor and franchisee applicability |
| City of Los Angeles | Office of Wage Standards schedule | City rate $18.42 from 2026-07-01 and the full historical schedule |
| CAL FIRE / OSFM / FRAP | Fire Hazard Severity Zone maps and project page | Statutory basis (Public Resources Code §§4201–4204); classification scheme; parcel lookup route |
| LA County Fire Dept | LRA Fire Hazard Severity Zones open data | Confirmation that LA County LRA zones were **established in 2025** |
| CA Dept of Finance | Population Projections, Baseline 2024, Vintage 2026 | Current official projection series, vintage and file structure |
| City of LA EWDD | Annual Plan PY2024-25 Tab 5 (LAEDC, May 2024) | 2022 ACS one-year characteristics; the DOF decline forecast |
| SCAG | Demographics table | The earlier regional projection, to document the conflict |

---

## 5. Irregularities found in official sources

These are defects in the *source data*, not in this analysis. All are disclosed
rather than silently corrected.

### 5.1 Los Angeles city race and ethnicity shares do not reconcile (`F-12`)

The QuickFacts race-category shares returned for **Los Angeles city** sum to
roughly **74%**, while the equivalent **Los Angeles County** shares sum to
**99.8%**. One or more city values appear to have been mis-extracted during
retrieval.

**Disposition:** the city race-composition breakdown is **omitted entirely** from
the Demographics page rather than published with a possibly incorrect figure.
County shares are published because they reconcile. Hispanic or Latino share is
published for both geographies. None of the decision-relevant variables —
population, income, poverty, density, foreign-born share, age structure — is
affected.

### 5.2 Los Angeles city building permits and housing units show `[X]` (`F-13`)

QuickFacts marks these as not available at place level.

**Disposition:** rendered blank with the QuickFacts note reproduced. County
values are **never substituted** for city values.

### 5.3 Two official forecasters disagree on the sign of population change

SCAG's Connect SoCal 2020 plan projected Los Angeles County to **grow 16.6%** to
11,674,000 by 2045. The California Department of Finance projection cited in the
City of Los Angeles 2024 workforce plan has the county **falling** to about 9.3
million by 2040 and 8.3 million by 2060. Successive SCAG plans have been revised
down every time: +14.41% → +10.15% → negative for 2024–2050.

**Disposition:** both are published side by side on the Official Forecasts page.
Neither is averaged and neither is silently preferred. The analysis underwrites
to the **measured** Census Bureau trend (−3.2% since the 2020 estimates base) and
treats growth as upside, never as the base case.

### 5.4 Mixed reference periods across the snapshot (`F-14`)

The snapshot mixes Census Vintage 2025 population estimates (July 2025), ACS
2020–2024 five-year estimates, the 2022 Economic Census, BLS August and September
2026 data, and SEC filings for periods ending September 2025 and July 2026. The
Census Bureau itself warns that estimates from different sources and vintages are
not comparable.

**Disposition:** every row carries its own `as_of` date. The site never compares
across vintages without saying so.

### 5.5 Minimum wage figures from third parties were wrong

Secondary sources gave **$17.00** for the California minimum wage. The California
Department of Industrial Relations gives **$16.90** effective 2026-01-01. Others
gave an unannounced future city rate.

**Disposition:** the official figure was used and the conflict recorded. This
established the general rule applied throughout: **never accept an aggregator
number — escalate to the agency page.**

### 5.6 SEC EDGAR search ignores date filters

The EDGAR browse interface returned the most recent filings regardless of the
requested date range.

**Disposition:** filing history was assembled from the filing index pages
directly. Recorded so a reviewer reproducing the work does not assume a
date-filtered query succeeded.

---

## 6. What could not be verified

Fifteen items are on the [Flagged for Review](docs/flagged-for-review.html) page.
The four that materially limit the decision:

| # | Item | Root cause | Route to resolve |
|---|---|---|---|
| **F-01** | The subject property identity | Never supplied; not in the repository; withheld under the privacy directive | Input Register — 20 fields, on the Property Profile page |
| **F-02** | Cap rates and comparable sales | **No US government agency publishes commercial cap rates.** Private data. | MAI appraisal plus broker comparables |
| **F-04** | LA County projections for 2030 / 2035 / 2040 | DOF publishes only `.xlsx`; no network route to `dof.ca.gov` from this environment; third-party restatements disagree by >100,000 residents | Download `P2A_County_Total.xlsx` from the official DOF page |
| **F-05** | Tax rates on a sale | One IRS URL and one FTB URL returned HTTP 404 when retrieved | Written opinion from a California-licensed CPA |

**F-04 is the most consequential.** The 2035 projection is the mid-point of the
stated expiry window and is the single most useful forecast number for this
decision. It is left blank rather than approximated.

Also unverified and left blank: FEMA National Risk Index values for LA County
(`F-03`), the parcel's Fire Hazard Severity Zone (`F-07`), zoning and
highest-and-best-use (`F-08`), school catchment data (`F-09`), traffic counts
(`F-10`), transit project dates (`F-11`), and tenant credit ratings (`F-06`).

---

## 7. Privacy verification

**Directive:** personal information privacy is the highest-priority constraint.
All personal information anonymised; placeholders used; nothing personal appears
in the final website product.

| What was found | Disposition |
|---|---|
| **P-1** — the base commit's git author identity includes a personal email address | History **not** rewritten (out of scope, and the branch is tracked). The address is never read into, generated into, or rendered by any deliverable. `tools/pii_scan.py` scans all generated output for email patterns and fails the build if one appears. The published site contains no repository metadata at all. |
| **P-2** — commercial net-lease sites publish franchisee entity names, addresses and prices | Consulted only to establish that no official cap-rate source exists. **No name, address or price recorded in the data snapshot or rendered on any page.** These domains are also on `check_links.py`'s blocklist, so they cannot appear in the site even by accident. |
| **P-3** — property address, APN, rent, basis | Never supplied. Nothing inferred. The model is normalised to R so it produces a valid ranking without them. |
| **P-4** — tenant executive names in SEC filings | Public corporate disclosure, not personal information about the owner. **None reproduced.** Leadership status described generically ("an interim chief executive") with a link to the filing. `pii_scan.py` actively checks that these names do not appear. |
| **P-5** — issuer principal office street address | Omitted from the Tenant page. Irrelevant to the decision; the row records city and state only, with a note explaining the omission. |

**Mechanical enforcement.** `tools/pii_scan.py` scans 64 files — every generated
HTML page and CSV, every data module, the model, the tools, the stylesheet, the
research notes and the root Markdown deliverables — for email addresses, North
American telephone numbers, street-address patterns, APN patterns, taxpayer
identifier patterns, identifying field labels carrying a value, and the tenant's
officer names. **Result: 0 findings.**

The repository's `.gitignore` excludes `scratch/`, `private/` and `pii/` so that
any working material containing identifying detail can never be committed or
published by accident. Those directories were never created, because no
identifying material was ever supplied.

Every page carries `<meta name="robots" content="noindex,nofollow">`.

---

## 8. Link verification

`tools/check_links.py` performs three checks on all 1,013 emitted links:

1. **Well formed** — the URL parses, uses HTTPS, and has a host. Internal links
   must resolve to a file that exists in `docs/`.
2. **Official** — any URL in a column that claims to be a verified source must sit
   on an official or primary domain. A broker or aggregator URL in a verified
   column is a **hard failure**.
3. **Not blocked** — 30 named non-official domains, including every net-lease
   aggregator and every media source consulted during research, are blocklisted.
   Their appearance anywhere in the published site is a hard failure.

**Result: 1,013 links, 30 distinct hosts, 0 non-official hosts, 0 errors.**

Top hosts by link count: `www.census.gov` 83 · `www.sec.gov` 62 ·
`www.bls.gov` 54 · `investors.jackinthebox.com` 22 · `file.lacounty.gov` 16 ·
`www.fema.gov` 11 · `www.irs.gov` 7 · `home.treasury.gov` 7 · `www.usgs.gov` 6 ·
`frap.fire.ca.gov` 6.

The four hosts that are official but not on a `.gov` domain are explicitly
allowlisted with their operating agency recorded: `www.cadedash.net` (California
Department of Education), `www.metro.net` (LA County Metropolitan Transportation
Authority), `www.lausd.org` (Los Angeles Unified School District), and
`zimas.lacity.org` (City of Los Angeles).

**The checker deliberately does not make HTTP requests.** The build environment
has no network route to `census.gov`, `bls.gov` or `sec.gov`, so an HTTP check
here would report failures that are properties of the sandbox rather than of the
link. What is checked is that every link is syntactically valid, correctly
attributed, and on an approved domain — the failure mode that actually matters
for a verification claim.

---

## 9. Model verification

`model/projection.py` is deterministic: no randomness, no network calls, no
hidden state. Two defects were found and fixed during verification, and are
recorded here because a model that has never been wrong is a model that has never
been checked.

**Defect 1 — scenario semantics mixed favourable and unfavourable extremes.**
The original `low / base / high` parameters were swept directly, so the "high"
scenario simultaneously took the *favourable* extreme of replacement rent and the
*unfavourable* extreme of the exit cap rate and re-tenanting capital. It produced
nonsense — including negative present values for a strategy that collects rent.
**Fix:** every assumption now carries a `fav` field stating which extreme is good
for the owner, and `A(name, scenario)` resolves optimistic → favourable extreme of
every assumption, pessimistic → unfavourable extreme of every assumption.

**Defect 2 — vacancy loss was over-charged several-fold.**
The vacancy stream charged `ratio × f` for each quarter offset `f`, so the total
nominal loss grew quadratically instead of equalling `ratio × downtime`.
**Fix:** replaced with `_vacancy_loss()`, which charges `ratio × QUARTER` per
quarter so the total nominal loss equals `ratio × downtime_years` exactly.

**Post-fix behaviour confirms the model is sound:** all fourteen
strategy-by-expiry combinations produce positive present values in the optimistic
and base scenarios, and only the two weakest strategies go marginally negative in
the pessimistic scenario — which is the correct outcome for a strategy that spends
capital to re-let into a vacancy.

**Anchor integrity.** The discount rate is built from a *verified official* rate
(the U.S. Treasury 10-year par yield of 4.19% at 2026-01-02) plus an *explicitly
declared* risk premium that is itself swept from 2.0% to 5.5%. The verified
component and the judgement component are separated in the code and labelled
differently in the output.

---

## 10. Publication integrity

- The site is **static HTML served by GitHub Pages from `/docs`** with no build
  step, so deployment cannot fail because of a toolchain.
- **No runtime API calls.** The published figures cannot change silently after
  generation; what a reviewer reads is what was verified.
- No CDN, no framework, no external stylesheet or script. The only two assets are
  `assets/style.css` and `assets/app.js`, both committed.
- Client-side JavaScript does three things only: filter table rows, export a
  table to CSV, and mark the active navigation entry. It fetches nothing.
- The build regenerates `docs/` from scratch on every run (`shutil.rmtree`), so no
  stale page can survive a data change.

---

## 11. Residual limitations

Stated plainly, because a verification report that claims completeness is not
worth reading.

1. The **U.S. Census Bureau Data API requires a key**, unavailable here, so
   demographic data was read from server-rendered QuickFacts pages. This limits
   the analysis to the QuickFacts variable set; **tract-level ACS tables were not
   reachable**, which is the granularity a single drive-thru site actually trades
   on.
2. **County and metropolitan aggregates are the wrong granularity** for this
   decision. They establish direction and context, not site-level demand. A county
   decline of −3.2% is entirely compatible with a specific trade area growing.
3. **No property-level conclusion is possible** without the Input Register. This
   is a market and submarket analysis with a parameterised model, not an appraisal.
4. **No cap rate is verified anywhere**, so no market value is asserted. Every
   valuation statement is a range.
5. **No tax rate is asserted**, so net proceeds cannot be computed. The tax page
   describes mechanisms and links official sources only.
6. All scenario weights, likelihood and impact ratings, and model assumptions are
   **judgement** (`F-15`). They are anchored to cited verified facts, declared
   openly with a favourability direction, and swept across their full range so no
   conclusion rests on any single one.

---

*Verification performed by session `arena-d989a5c6-jack3`, 2026-11-06.*
