# Verification record — 2026-11-10 (session `e7bbac4b`, final integration)

Repo: `wingbangboozle1-lang/Jack3` · Branch: `arena/e7bbac4b-jack3`
Scope: shared outputs only (`data/evidence.json`, `scripts/`, root `*.html`). No other session's directory,
branch or PR was edited, merged or deleted.

This pass **re-read every headline figure from its publisher page**. It is not a re-statement of the 2026-11-08
record; where a value below says "matched", the publisher page was fetched and read again on 2026-11-10.

Status legend: **matched** = publisher page re-read, value identical · **closed** = previously blank, now verified
and published · **unchanged** = not re-read in this pass, carries its 2026-11-08 vintage.

---

## 1. Source-by-source re-read

| # | Value published on the site | Publisher page read 2026-11-10 | Result |
|---|---|---|---|
| 1 | LA city population 3,869,089 | [Census QuickFacts, LA city (V2025)](https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia/PST045225) | matched |
| 2 | LA city population change −0.8%, April 2020 base to July 2025 | same QuickFacts table | matched (estimates base 3,899,342) |
| 3 | LA city median household income $81,939 (2024 dollars) | same, Income & Poverty | matched |
| 4 | LA city poverty 16.5% | same | matched |
| 5 | LA city owner-occupied rate 36.0% | same, Housing | matched |
| 6 | LA city land area 469.49 sq mi; density 8,304.2/sq mi (2020) | same, Geography | matched |
| 7 | LA city households 1,439,097; persons per household 2.61 | same | matched |
| 8 | LA city under 18 = 19.2%; 65+ = 14.2% | same | matched |
| 9 | LA County population 9,694,934 | [Census QuickFacts, LA County (V2025)](https://www.census.gov/quickfacts/fact/table/losangelescountycalifornia/PST045225) | matched |
| 10 | LA County population change −3.2% | same QuickFacts table | matched (base 10,017,414) |
| 11 | LA County 65+ = 17.1% | same | matched |
| 12 | Metro unemployment 4.4% (Sep 2026), down from 5.5% | [BLS LA Area Economic Summary, updated 2026-11-04](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) | matched |
| 13 | LA city and LA County unemployment 4.5% | same BLS summary | matched |
| 14 | Nonfarm payrolls 6,282.1 thousand, +30.2 thousand, +0.5% YoY | same | matched |
| 15 | Information −5.7% (−11.4k); education & health +3.8% (+49.1k) | same | matched |
| 16 | CPI-U all items +3.7%; energy +20.3%; food +2.8% | same | matched |
| 17 | ECI, LA-Long Beach CSA, +3.9% YoY | same | matched |
| 18 | Average weekly wage, all industries, Q1 2026 = $1,704 | same | matched |
| 19 | 10-year Treasury | [FRED DGS10](https://fred.stlouisfed.org/series/DGS10) | 4.84% on 2026-11-05 confirmed; **refreshed to 4.86% on 2026-11-06**, the latest observation, carried forward from session 882bff85 and independently confirmed here |
| 20 | LAUSD enrollment 497,105 (2025-26) | [CDE Largest & Smallest Public School Districts](https://www.cde.ca.gov/ds/ad/ceflargesmalldist.asp) | matched, rank 1 |
| 21 | Statewide public enrollment 5,731,260 | same CDE page | matched |
| 22 | San Diego Unified 112,250 (comparison used in the rank row) | same CDE page | matched, rank 2 |
| 23 | System same-store sales −1.1%; franchise −1.2%, company −0.9% | [Jack in the Box Q3 FY2026 8-K Ex. 99.1](https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm) | matched |
| 24 | Systemwide sales −1.4% | same release | matched |
| 25 | 4 openings, 17 closures, 2,115 restaurants (149 company / 1,966 franchise) | same release, restaurant-count table | matched |
| 26 | Franchise-level margin 37.4% vs 39.3%; $60.3m vs $66.2m; higher bad-debt expense | same release | matched |
| 27 | Measure ULA $5,400,000 / $10,900,000; 4.00% / 5.50% for closings after 2026-06-30 | [City of LA Office of Finance, Measure ULA FAQ](https://finance.lacity.gov/faq/measure-ula) | matched |
| 28 | City base transfer tax $2.25 per $500 = 0.45% | same FAQ | matched |
| 29 | ULA thresholds indexed annually to Chained CPI | same FAQ | matched |
| 30 | ULA on gross value; base tax on value net of liens | same FAQ + [County Recorder](https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info) | matched |
| 31 | Prop 13: 1% general levy; 2% maximum annual assessed-value increase; reassessment on change of ownership or new construction; voter-approved debt and direct assessments are added | [LA County Assessor, Proposition 13](https://assessor.lacounty.gov/real-estate-toolkit/proposition-13) | matched |
| 32 | State minimum wage $16.90/hour from 2026-01-01 | [CA DIR Minimum Wage FAQ](https://www.dir.ca.gov/dlse/FAQ_MinimumWage.htm) | matched |
| 33 | **LA County documentary transfer tax $0.55 per $500 (= $1.10 per $1,000)** | [LA County Recorder, Documentary Transfer Tax](https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info) | **closed (was V-3)** |
| 34 | County rate inside the five cities levying their own tax, Los Angeles among them: "the full $1.10 per $1,000" | same Recorder page | **closed (new row)** |
| 35 | **LAUSD four-year graduation rate 84.6%** | [CA School Dashboard, LAUSD 2025 · Academic Engagement](https://www.caschooldashboard.org/reports/19647330000000/2025/academic-engagement) | **closed (was V-4), after a label correction — see IR-E6** |
| 36 | **LAUSD five-year graduation rate 86.5%** (Yellow, "Maintained -0.2%"; = 84.6% four-year + 1.8% fifth-year) | same Dashboard report | **published separately** |

Remaining rows on the site carry their 2026-11-08 vintage (unchanged). They are not claimed as re-read here.

## 2. Items deliberately left blank (unchanged, still flagged)

| Item | Why it stays blank | What would close it |
|---|---|---|
| Parcel identity, address, APN, census tract | never supplied; publishing it would breach the owner's privacy instruction | owner-supplied deed |
| Exact lease expiry, commencement, options, notice dates | "2030–2035" is a five-year range, not a date | executed lease and amendments |
| Rent, NOI, basis, debt, guaranty, estoppel | private; no public record | owner financials |
| Exit cap rate | no US government agency publishes commercial cap rates | an actual bid |
| Owner's marginal tax rates | private | owner's tax advisor |
| FEMA NRI county scores | portal reachable, values not readable; aggregator mirrors rejected | fema.gov value export |
| Parcel-level flood / fire / seismic zone | requires the parcel | FEMA MSC, CAL FIRE OSFM, CGS EQ Zapp |
| Campus assigned to any site; school-level performance | requires the parcel | LAUSD boundary lookup, CDE Dashboard |

## 3. Irregularities found in this pass

**IR-E1 — cross-layer contradiction, now resolved (was flagged as V-3 / V-4).**
The root site published *"LA County documentary transfer tax: not published — the County Recorder page could not be
retrieved"*, while the `dashboard/` layer published *$0.55 per $500* sourced to that same lavote.gov page. Both pages
are published on the same live site, so a reader could see two contradictory statements. The Recorder page **was**
retrievable on 2026-11-10 and states $0.55 per $500. Resolved in favour of the page actually read; both layers now
agree. A new build gate (`scripts/validate.py`, cross-layer check) fails if this class of contradiction reappears.

**IR-E2 — the same split affected the LAUSD graduation rate.** The root site carried it blank while the dashboard
layer published 86.5%. The Dashboard district report was read on 2026-11-10 and confirms 86.5%. Both layers now agree.

**IR-E3 — stale evidence-snapshot date.** Every root page displayed "Evidence snapshot · 08 Nov 2026" from a
hard-coded string while `data/evidence.json` carried a `reviewed` field. The stamp now renders from the data file, so
it cannot drift from the evidence it describes.

**IR-E4 — no guard against hand-edited HTML.** The generator is the only legitimate writer of the root pages, but
nothing failed the build if a generated page was edited by hand or left stale after a data change. Added a gate that
rebuilds in a scratch directory and requires byte-identical output. Verified by deliberately corrupting a page: the
build fails.

**IR-E6 — graduation-rate definition was mislabelled (caught and corrected before publication).**
The Dashboard's headline 86.5% is the **five-year** cohort rate. The report itself breaks it down: four-year 84.6% +
fifth-year 1.8% = 86.5%. This session's first pass published 86.5% as the "four-year graduation rate", and session
`882bff85` published "86.5% (5-year; 4-year 84.6%)". Both labels were wrong or ambiguous; the number was right. The
site now publishes **two separate rows** — four-year 84.6% and five-year 86.5% — each labelled with its definition, and
the review page records the correction rather than hiding it. Publishing 86.5% as the four-year rate would have
overstated the district outcome by 1.9 points.

**IR-E5 — the dashboard layer was reachable but not listed.** `dashboard/` was staged into the Pages artifact and
cross-linked from the sidebar of every root page, but the landing page itself never listed it among the pages. It is
now row 12 of the new Page directory.

**Carried forward, not fixed here (outside this session's file scope, recorded for the owner):**
- `K-IR-01` — 26 HTML files under `decision-file/` and 4 under `pages/` render the repository account handle. Neither
  directory is published (verified: `/Jack3/decision-file/` returns 404 on the live site), so nothing identifies the
  owner on the live site. Redaction belongs to those layers' owners.
- `K-IR-02` — `analysis/` cites a commercial brokerage domain and a private law firm. `analysis/` is not published.
- Five parallel layers (`advisory/`, `analysis/`, `brief/`, `decision-file/`, `pages/`, `docs/`) remain in the
  repository but outside the Pages artifact, each written under an older verification standard, and each carrying a
  differing headline recommendation. The root site states this plainly on the review page rather than deleting them.

## 4. Privacy re-scan (all layers, including unpublished)

| Check | Scope | Result |
|---|---|---|
| Email addresses | every `.html`, `.md`, `.json`, `.py` in the repo | 0 found |
| Telephone numbers | same | 0 found |
| Street address for the subject property | same | none; Asset A is a placeholder |
| Parcel / APN / taxpayer identifiers | same | none |
| Owner or officer names | same | none |
| Repository account handle | 26 files in `decision-file/`, 4 in `pages/`, 5 in `docs/`/`research/`, and repo metadata | present, but **only in non-published directories** |
| Third-party analytics, embeds, forms, external scripts | published artifact (`_pages_artifact`, 32 files) | 0 found (`tools/pii_scan.py` and the page-level checks) |

No personal information about the owner or any individual appears on the live site.

## 5. Checks run (all green before merge)

| Gate | Command | Result |
|---|---|---|
| Evidence-row schema, blank-value rule, no embeds | `python3 scripts/validate.py` | PASS — 143 rows, 12 pages |
| Cross-layer reconciliation (new) | same | PASS |
| Staged artifact: links resolve, every row sourced | `python3 scripts/stage_pages.py` | PASS — 32 entries |
| Committed pages match a fresh build (new) | same | PASS |
| Internal links and anchors (brief/) | `python3 tools/check_site.py` | PASS — 213 refs |
| Internal links and anchors (analysis/) | `python3 tools/linkcheck.py` | PASS — 256 refs, 0 broken |
| Official-domain rule for external links | `python3 tools/check_links.py` | PASS — 1,040 links, 30 hosts, 0 non-official |
| PII gate | `python3 tools/pii_scan.py` | PASS — 84 files, 0 findings |
| Advisory layer | `python3 _advisory_src/verify_advisory.py` | PASS — 227 rows |
| Dashboard layer | `python3 _dashboard_src/verify.py` | PASS — 185 facts, 148 body rows |

## 6. Merge with session `882bff85` (PR #35)

While PR #36 was open, session `882bff85` merged PR #35 to `main` having claimed the same shared-output scope. Both
branches therefore touched `data/evidence.json`, `scripts/build.py` and every generated page. **Nothing from either
session was discarded.**

| File | Resolution |
|---|---|
| `data/evidence.json` | Rebuilt on this branch, then every factual change from `882bff85` carried forward: the 4.84% → 4.86% Treasury refresh in the `model`, `risk` and `taxes` rows (3 cells). The graduation row was replaced by the two correctly labelled rows above. |
| `scripts/build.py` | This session's version kept — it contains `882bff85`'s snapshot-date change in a stronger form (rendered from `D['reviewed']`) plus the Page directory. |
| Root `*.html` | Regenerated with `scripts/build.py`. No HTML was hand-merged. |
| `COORDINATION.md` | Both sections preserved in full; collision and resolution logged. |
| Verification records | This one, plus `882bff85`'s preserved unchanged at `research/VERIFICATION-2026-11-10-882bff85.md`. A third file written by session `c70571c7` under the same name is also preserved in history. |

Both sessions independently closed the county transfer tax and the graduation rate from the same sources — duplicated
effort, but mutually corroborating. Cause: the shared-output scope was claimed twice because the board was not
re-read immediately before writing. Logged in `COORDINATION.md`.

## 7. Limits of this record

A publisher page can be revised after it is read; a "matched" result describes 2026-11-10, not permanence. No value on
the site is a forecast, an appraisal or a probability. The automated gates check structure — that a row has a source on
an approved domain, that blank means blank, that layers agree — and cannot prove that a publisher's page says what the
row claims; that was done by reading each page above and recording the link.

**Nothing on this site should be read as personalised legal, tax or investment advice.**
