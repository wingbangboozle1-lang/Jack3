# Fresh official-source re-verification pass — 2026-11-16 (session 7f1087ce)

**Scope.** A full liveness and line-by-line value re-check of the canonical evidence
register (`data/canonical_rows.py`, 255 rows / 48 official sources) as of the current
main head (`a68b55e`, merge of PR #107). Every dynamic official source was re-read
live through its published URL on 2026-11-16 (UTC). Static archived publications
last verified in the full 2026-11-12 audit were re-checked for liveness where
fetched and were not altered by their publishers.

**Result.** Every re-read value matched the register exactly. **No evidence value
was changed.** The only content updates in this pass are:

1. `SNAPSHOT` bumped 2026-11-13 → **2026-11-16** (re-verification date; values unchanged).
2. Row "FEMA National Risk Index county scores" and flag **F-18**: the legacy portal
   `hazards.fema.gov/nri/` returned HTTP 500 on 2026-11-12; on re-check today it now
   **redirects to FEMA's Resilience Analysis and Planning Tool (RAPT)**, which hosts
   the National Risk Index **v1.20** dataset update. Los Angeles County figures were
   still not extracted from the official app, so the value remains **blank** (no
   third-party mirror is used). Action recorded: extract from RAPT or the v1.20
   official download if post-2023 county values are needed.
3. Suggestions **SG-01** (option B) and **SG-12** (option A) and **Path 2** marked
   adopted: the owner's standing brief requires "a private calculator that runs in
   the reader's browser," which selects the already-documented Path 2. Implemented
   as `calculator.html` (inline, network-free JS) plus a text filter on
   `master.html`; the no-script rule in `scripts/validate.py` was relaxed only for
   inline JS on those two disclosed pages, with every other rule unchanged
   (external-resource, tracking, PII, provenance, determinism and host-allowlist
   rules all preserved and re-tested).

## Sources re-read live on 2026-11-16 (all values confirmed identical)

| Source | URL | Rows covered | Result |
|---|---|---|---|
| BLS LA Area Economic Summary (updated 2026-11-04) | https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf | 65–86, 247–248 | Unemployment (US 4.0 / CA 5.1 / metro 4.4 / county 4.5 / city 4.5; Sep-25 priors), nonfarm 6,282.1k +0.5%, industry changes, QCEW $1,704, OEWS $37.15, CPI-U 3.7/2.8/20.3, ECI +3.9%, CE West spending — all match |
| FRED DGS10 | https://fred.stlouisfed.org/series/DGS10 | 92–96 | Latest observation still 2026-11-12: 5.10%; 11-10 4.98; 11-09 4.88 — match (11-11 holiday, no print) |
| Census QuickFacts LA city (V2025) | https://www.census.gov/quickfacts/losangelescitycalifornia | 0–1, 4, 7, 15–18, 26–35, 37–43, 45–46, 49–51, 53–54, 56–58 | Every cited cell matches; city building-permits/business cells still displayed as not available |
| Census QuickFacts LA county (V2025) | https://www.census.gov/quickfacts/losangelescountycalifornia | 2–3, 5–6, 19–22, 27–35, 38–42, 44, 47–48, 50–52, 55, 59–62 | Every cited cell matches; permits 22,250; CBP 2023 establishments/employment/+2.3% match |
| IRS Topic 409 | https://www.irs.gov/taxtopics/tc409 | 205, 207 | 0/15/20% rates; §1250 max 25% — match |
| IRS Rev. Proc. 2025-32 §4.03 | https://www.irs.gov/pub/irs-drop/rp-25-32.pdf | 206 | 2026 max-zero/15% amounts: MFJ $98,900/$613,700; MFS $49,450/$306,850; HoH $66,200/$579,600; other $49,450/$545,500; E/T $3,300/$16,250 — exact match |
| IRS Topic 559 | https://www.irs.gov/taxtopics/tc559 | 208–209 | 3.8% NIIT; 2025 E/T threshold $15,650 — match |
| IRS like-kind exchanges | https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges-real-estate-tax-tips | 211–212 | Real property only; Form 8824 — match |
| CA FTB capital gains | https://www.ftb.ca.gov/file/personal/income-types/capital-gains-and-losses.html | 210 | "California does not have a lower rate…taxed as ordinary income" — match |
| LA City Finance, Measure ULA FAQ | https://finance.lacity.gov/faq/measure-ula | 195–201 | Base 0.45%; ULA 4% > $5.4M < $10.9M; 5.5% ≥ $10.9M; effective 2023-04-01; annual chained-CPI indexation; page note confirms $5.4M/$10.9M for closings after 2026-06-30 — match |
| LA County RR/CC transfer taxes | https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info | 202–204 | County $0.55/$500; full $1.10 per $1,000 for the five special cities; LA city rates effective 7/1/26 — match |
| CA DIR minimum-wage FAQ | https://www.dir.ca.gov/dlse/FAQ_MinimumWage.htm | 87–88 | $16.90 from 2026-01-01; no 2027 rate published yet (row stays blank) — match |
| CA DIR fast-food FAQ | https://www.dir.ca.gov/dlse/Fast-Food-Minimum-Wage-FAQ.htm | 89–90 | $20.00 from 2024-04-01; applies to franchisees — match |
| LA City Wages LA | https://wagesla.lacity.gov/ | 91 | July 1, 2026 → $18.42 — match |
| LA County Assessor, Proposition 13 | https://assessor.lacounty.gov/real-estate-toolkit/proposition-13 | 187–192 | 1% general levy; 2% cap; reassessment on change of ownership/new construction; add-ons; Prop 8 — match |
| BOE Publication 800-10 (7-25) | https://boe.ca.gov/pdf/pub800-10.pdf | 189, 192 | California-CPI inflation factor capped at 2%; Prop 8 temporary reduction — match |
| CAL FIRE Palisades Fire incident page | https://www.fire.ca.gov/incidents/2025/1/7/palisades-fire | 224–227 | 23,448 acres; 6,845 structures destroyed; 12 civilian fatalities; contained 2025-01-31 (24 days) — match |
| CAL FIRE Eaton Fire incident page | https://www.fire.ca.gov/incidents/2025/1/7/eaton-fire | 228–230 | 14,021 acres; 9,419 structures destroyed; 19 fatalities — match; derived combined 16,264 re-confirmed |
| CAL FIRE/OSFM Fire Hazard Severity Zones | https://osfm.fire.ca.gov/what-we-do/community-wildfire-preparedness-and-mitigation/fire-hazard-severity-zones | 232–236 | Moderate/High/Very High; SRA effective 2024-04-01; LRA phases 2025-02-10/02-24/03-10/03-24; hazard vs risk; 2026 SRA public comment open — match |
| CGS EQ Zapp | https://www.conservation.ca.gov/cgs/geohazards/eq-zapp | 237–238 | Three ground-failure zone types; explicit not-a-substitute note — match |
| FEMA Flood Maps | https://www.fema.gov/flood-maps | 239 | MSC is the official NFIP mapping location — match |
| FEMA NRI (redirect) | https://hazards.fema.gov/nri/ | 243 | Now redirects to the Resilience Analysis and Planning Tool; NRI v1.20 update announced; county values still not extracted — row remains blank; F-18 refreshed |
| CA DOF July 2025 estimates (Feb 2026 release) | https://dof.ca.gov/media/docs/forecasting/Demographics/estimates/July2025_Population_Estimates_Feb26_release.pdf | 23–25 | LA County 9,853,435; −44,822 (−0.45%); CA 39,528,899; release dated 2026-02-04 — match |
| BEA county GDP & personal income 2024 (BEA 26-08) | https://www.bea.gov/news/2026/gross-domestic-product-county-and-personal-income-county-2024 | 97–98 | LA County personal income $818.5bn (2024); metro-area publication discontinued — match |
| SCAG Connect SoCal 2024 Demographics & Growth Forecast | https://www.scag.ca.gov/sites/default/files/2024-05/23-2987-tr-demographics-growth-forecast-final-040424.pdf | 99–103 | Document live; adopted 2024-04-04; table values verified in the 2026-11-12 full audit (static publication) |
| CDE District Profile (LAUSD) | https://www.cde.ca.gov/sdprofile/details.aspx?cds=19647330000000 | 105–106 | Enrollment 497,105; EL 81,328 (16.4%), 2025-26 — match |
| CDE Largest & Smallest Districts | https://www.cde.ca.gov/ds/ad/ceflargesmalldist.asp | 107–109 | LAUSD 1st (497,105); San Diego 2nd (112,250); statewide 5,731,260 — match |
| California School Dashboard 2026 (LAUSD) | https://www.caschooldashboard.org/reports/19647330000000/2026/academic-engagement | 110, 112, 114 | Graduation 87.6% (+1.1%); by-year 82.1 (2019) / 86.0 (2022) / 83.6 (2023); chronic absenteeism 21.3% — match |
| CDE 2024–25 End-of-Year reports | https://www.cde.ca.gov/ds/cm/dqeoy25.asp | 116–119 | Statewide ACGR 87.5%; five-year 88.7%; absenteeism 19.4%; suspension 2.9% — match |
| CDE DataQuest ACGR 2025-26 (LAUSD) | https://dq.cde.ca.gov/dataquest/dqcensus/CohRate.aspx?agglevel=District&cds=1964733&year=2025-26 | 111 | Report live (2025-26 four-year ACGR); the 87.4% value is verified in the 2026-11-12 full audit; the rate value sits deep in the paginated report |
| CDE GRAD download 2026 | https://www3.cde.ca.gov/researchfiles/cadashboard/graddownload2026.txt | 110 | File live (540 chunks); LAUSD row verified in the 2026-11-12 full audit; file unchanged |
| SEC 8-K Ex-99.1 Q3 FY2026 (filed 2026-08-12) | https://www.sec.gov/Archives/edgar/data/807882/000080788226000090/ex991-q326earningsrelease.htm | 122–125, 139–161, 167–168 | SSS −1.1% system / −1.2% franchise / −0.9% company; prior-year −7.1%; systemwide sales −1.4%; counts 2,115/149/1,966; +4/−17/−13; revenues $257.657M (−1.8%); margins 17.6% / 37.4% (from 39.3%); rental revenues $242,526 vs $260,254 (40 wks; derived −6.8% re-confirmed); occupancy expenses $166,043; higher bad debt; $110.0M 2019-1 prepayment; $500M 2026-1 notes; guidance ~2,100 units, 50–60 closures, ~25 openings, EBITDA $225–230M, SG&A $112–115M; dividend/repurchase discontinued; Del Taco sale completed 2025-12-22; 25 states + Mexico + Guam — all match |
| SEC 8-K Ex-99.1 Q2 FY2026 | https://www.sec.gov/Archives/edgar/data/807882/000080788226000066/ex991-q226earningsrelease.htm | 127, 130, 132, 135, 138 | Q2 FY2026 SSS −3.8% (prior-year −4.4%); count 2,128; closures 9 — match |
| SEC 8-K Ex-99.1 Q1 FY2026 | https://www.sec.gov/Archives/edgar/data/807882/000080788226000039/ex991-q126earningsrelease.htm | 126, 129, 134, 137 | Q1 FY2026 SSS −6.7% (prior-year +0.4%); count 2,128; closures 14 — match |
| SEC 8-K Ex-99.1 Q4/FY2025 | https://www.sec.gov/Archives/edgar/data/807882/000080788225000070/ex991-q425earningsrelease.htm | 128, 133, 136, 180 | Q4 FY2025 SSS −7.4%; count 2,136; 47 closures; FY2025 86 closures / 31 openings — match |
| SEC FY2025 Form 10-K | https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm | 173–181 | Filing live (53 parsed chunks); Item 1 cover matches 2,136 restaurants / 22 states + Del Taco; the Item 2 / Item 7 / Notes values (941 CA restaurants, tenure split, ~13% percentage rent, AUV $1,874k, 11.2-year weighted lease term, 20-year initial terms, lessor income $245,062/$16,859) were verified line by line in the 2026-11-12 full audit and the immutable filing is unchanged |
| SEC EDGAR 8-K index (JACK, CIK 807882) | https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000807882&type=8-K&dateb=&owner=include&count=10 | 183 | Most recent 8-K remains 2026-09-21 (items 1.01/5.02/7.01/9.01); earnings 8-K 2026-08-12 confirmed — match |
| SEC 8-K Ex-99.1 2026-09-21 | https://www.sec.gov/Archives/edgar/data/807882/000080788226000098/ex991-pressreleasexbodanno.htm | 184–185 | Interim CEO arrangement (Executive Chairman & Interim CEO; successor expected within 12 months); GreenWood cooperation agreement extended with standstill/voting provisions — match |
| JACK on Track release (2025-04-23) | https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Unveils-JACK-on-Track-Plan-to-Improve-Long-Term-Financial-Performance/default.aspx | 162–166 | 150–200 closures; ~80–120 by 2025-12-31; remainder tied to franchise-agreement termination dates; ~1% ongoing closure rate from FY2026; sell select owned real estate — match |
| Q4/FY2026 earnings webcast notice | https://investors.jackinthebox.com/news/news-details/2026/Jack-in-the-Box-Announces-Fourth-Quarter-and-Full-Year-2026-Earnings-Webcast/default.aspx | 182 | Release dated 2026-10-26; results after market close on 2026-12-09 — match |
| ZIMAS (research route) | https://zimas.lacity.org/ | 8, 11–12, 14 | Application live (JS app); remains a research route, not a parcel fact |

**Not re-fetched on 2026-11-16 (static archived publications; values rest on the
full line-by-line audit of 2026-11-12 recorded in
`research/VERIFICATION-2026-11-12-c56c569e.md` and successors):** BOE Publication
220-0345 (35-year leasehold change-in-ownership quote), the FEMA PrepToolkit NRI
v1.19.0 briefing deck (NRIDECK), USGS Open-File Report 2008-1150 (ShakeOut) and
USGS Fact Sheet 2015-3009 (UCERF3) PDFs, and the 2025-vintage California School
Dashboard page. None of these is a mutable statistics feed.

## Irregularities and flags

- **No data irregularity found.** No re-read value differed from the register;
  nothing was inferred or back-filled.
- **F-18 status refresh** (portal redirect to RAPT; v1.20 available): recorded in
  the flag and the row note; the blank value policy is unchanged.
- **Palisades Fire cause** is now displayed by CAL FIRE as "Arson" (updated
  2026-04-09); the register does not cite a cause, so no row change was needed.
- **2027 California minimum wage** is not yet published on the DIR FAQ (checked
  2026-11-16); row 88 stays blank rather than projecting the CPI-W adjustment.
- **City race-alone shares** remain deliberately blank (flagged): the city's
  QuickFacts race-alone percentages total 74.3% against the county's 99.8% and are
  not reconciled; re-confirmed unchanged on 2026-11-16.

## Verification of the calculator change (S7-04)

- `calculator.html` (SG-01B) and the `master.html` filter (SG-12A) use inline,
  network-free JavaScript only: no `<script src=…>`, no fetch/XHR/sendBeacon, no
  storage, no imports, no websockets, no forms, no iframes, no external resources,
  no inline event-handler attributes — asserted by new regression tests
  (`test_calculator_is_inline_and_network_free`,
  `test_master_register_filter_is_inline_and_local`,
  `test_no_script_on_any_other_published_page`, plus the tightened
  `test_no_active_collection_or_remote_resources`).
- Every `<tbody>` row on the new page carries an official source link
  (`scripts/stage_pages.py` and `scripts/validate.py` re-verify this on every run).
- The tax arithmetic mirrors the rows cited above: base city transfer tax 0.45%,
  ULA 4%/5.5% tiers ($5.4M/$10.9M), county 0.11%, §1250 recapture at the owner's
  entered rate (25% statutory maximum, shown), NIIT 3.8% optional, California
  ordinary-income treatment, §1031 disclosed as not modelled. Owner inputs are
  never persisted or transmitted; reloading clears them.
- Full gate set on the final tree: build (24 pages, 255 rows, 48 sources),
  validate, stage, 22 unit tests, check_site, linkcheck, check_links, PII scan,
  advisory and dashboard verifiers — all PASS; `git diff --check` clean.
