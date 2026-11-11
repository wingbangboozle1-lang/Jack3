# Earlier final-integration review — session `1f62010a` (preserved verbatim)

# Repository review — final integration

**Reviewed:** 2026-11-10  
**Reviewer session:** `1f62010a`

## Current public architecture

The repository contains several generations of parallel research. The final integration publishes one curated root dashboard: `index.html`, ten evidence/category pages, `sources.html`, and `assets/style.css`. `scripts/build.py` generates those pages from `data/evidence.json`; `scripts/stage_pages.py` creates the exact Pages artifact.

This removes conflicting live recommendations and prevents stale repository-only pages from being mistaken for the current analysis.

## Irregularities retained for review

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| J-IR-01 | High | `/advisory/` contains scenario weights and pathway rankings not established by its official citations. | Excluded from Pages; preserved for audit. |
| J-IR-02 | High | `/dashboard/` extrapolates population, employment and CPI-linked rent and contains qualitative claims beyond the cited evidence. | Excluded from Pages; preserved for audit. |
| J-IR-03 | High | Other historical layers include third-party commercial sources, stale figures, unsourced rows and conflicting recommendations. | Excluded from Pages; not represented as reverified. |
| J-IR-04 | Medium | Some historical HTML files render the repository account handle. | Not included in the curated public artifact. No owner identity or personal information was researched. |
| J-IR-05 | Medium | The LA County Assessment Roll official release says 4.42% in narrative but “42%” in a bullet. | Published 4.42%, flagged on `review.html`. |
| J-IR-06 | Medium | Earlier material labeled LAUSD’s combined graduation rate as a four-year rate. | Corrected to 86.2% four-year and 87.6% combined for 2026. |
| J-IR-07 | Medium | Earlier material cited mixed city/county values or two fire incidents with only one row-level source. | Split into single-source rows. |
| J-IR-08 | Low | The BLS Food category was labeled “food at home.” | Corrected to Food. |
| J-IR-09 | Low | FY2026 full-year tenant results are not yet available; issuer schedules them for 2026-12-09. | Q3 remains latest; future release flagged. |

## Verification boundary

A source link does not make an inference official. Government and issuer pages substantiate observations; they do not establish Asset A’s value, optimal sale date, tenant renewal intention, store closure probability or catastrophe loss. Those remain analytical gaps.

No historical directory was deleted. Excluding a directory from the Pages artifact is a publication-safety decision, not a claim that its repository history was erased.

## Final decision support

The only current public recommendation is the conditional dual track: confidential market testing plus written renewal negotiations, followed by an after-tax comparison of actual offers and enforceable terms. It is explicitly analyst judgment—not an appraisal or personalized financial, legal or tax opinion.

See [`research/VERIFICATION-2026-11-10-1f62010a.md`](research/VERIFICATION-2026-11-10-1f62010a.md) for all 155 row-level checks and [`review.html`](review.html) for the public Flagged for Review register.

<!-- b98090a0 canonical repo review: start -->
# Repo review — line-by-line findings (2026-11-10, UTC)

Final-integration session `b98090a0`. This file is the repository-side companion to the published
[Repo review page](repo-review.html) and the row-level [verification log](research/VERIFICATION-2026-11-10-b98090a0.md).

The repository accumulated work from more than fifteen parallel sessions and eight overlapping
dashboard layers. This review does not delete any of that work. It records what was checked, what
was corrected in the canonical site, what remains unresolved, and which files are actually
published. **Every finding below carries an official source link for manual review.**

**Canonical site:** 20 static HTML pages · 223 evidence rows (189 verified, 4 derived with arithmetic shown, 1 analysis, 29 blank/unverified) · 36 official sources · 22 flagged items · 22 review findings.

## Line-by-line findings

| ID | Area | Finding | Disposition | Official source |
|---|---|---|---|---|
| R-01 | Repository structure | The repository contains eight overlapping dashboard layers (root, docs/, analysis/, brief/, pages/, decision-file/, advisory/, dashboard/) produced by earlier parallel sessions, with different recommendations and data vintages. | Consolidated into one canonical root site; the other directories are preserved as audit trail and excluded from GitHub Pages. | [Los Angeles Area Economic Summary · updated 2026-11-04](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) |
| R-02 | Publication boundary | _config.yml excluded most companion layers but not dashboard/, so two competing dashboards were live at the same time. | dashboard/ is now excluded from the Pages artifact; a single canonical navigation is published. | [Real Property Transfer Tax and Measure ULA FAQ](https://finance.lacity.gov/faq/measure-ula) |
| R-03 | Shared navigation | The root landing page linked to a second dashboard while a separate 15-page dashboard carried its own navigation. | One shared navigation block now drives every published page, generated from a single list. | [Census QuickFacts · Los Angeles city (V2025)](https://www.census.gov/quickfacts/losangelescitycalifornia) |
| R-04 | Table provenance | Both inherited datasets required an official source link on every table row; spot checks found rows whose links pointed to a portal rather than a value. | Qualitative portal statements are now labelled Analysis; unverified values are blank and flagged. | [EQ Zapp · earthquake hazard zone application](https://www.conservation.ca.gov/cgs/geohazards/eq-zapp) |
| R-05 | Blank-value rule | Earlier layers sometimes published text such as 'not verified this session' inside a value cell instead of leaving it empty. | Every unverified value cell is now empty with an explicit Flagged for Review entry. | [July 2025 population estimates · revised release 2026-02-04](https://dof.ca.gov/media/docs/forecasting/Demographics/estimates/July2025_Population_Estimates_Feb26_release.pdf) |
| R-06 | County documentary transfer tax | Root taxes.html left the county rate blank (V-3 / K-F-18) because the recorder page was reported unretrievable. | Re-read the official recorder page on 2026-11-10: $0.55 per $500 (0.11%). The gap is closed with a verified row. | [Documentary Transfer Tax · general information](https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info) |
| R-07 | LAUSD graduation rate | Root schools.html left the district graduation rate blank (V-4) because CDE files were not extracted. | Read CDE official records: 87.4% four-year ACGR for 2025-26 and 87.6% combined four-/five-year for 2026, with separate measures and direct sources. | [California School Dashboard · Los Angeles Unified 2025 academic engagement](https://www.caschooldashboard.org/reports/19647330000000/2025/academic-engagement) |
| R-08 | Interest-rate vintage | An inherited decision-file model anchors to 4.19% (2026-01-02); the root site used 4.84% (2026-11-05); FRED now shows 4.88% (2026-11-09). | All three are labelled by date on the Flagged page; the current site publishes the 2026-11-05 and 2026-11-09 observations. | [10-Year Treasury constant maturity yield (DGS10)](https://fred.stlouisfed.org/series/DGS10) |
| R-09 | BLS vintage | Some inherited rows were labelled August 2026 while citing a summary that reports September 2026 data. | The canonical dataset uses September 2026 observations from the 2026-11-04 summary only. | [Los Angeles Area Economic Summary · updated 2026-11-04](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) |
| R-10 | Franchise date conflation | An inherited report treated franchise agreement termination dates as property lease expiry dates. | Separated and flagged (F-14); the issuer plan establishes neither agreement for this site. | ['JACK on Track' plan announcement · 2025-04-23](https://investors.jackinthebox.com/news/news-details/2025/Jack-in-the-Box-Inc--Unveils-JACK-on-Track-Plan-to-Improve-Long-Term-Financial-Performance/default.aspx) |
| R-11 | Unsupported scenario weights | The advisory layer published numerical scenario weights and pathway rankings that its official citations do not establish. | Withheld from publication and flagged (F-19); no weights appear on the canonical site. | [10-Year Treasury constant maturity yield (DGS10)](https://fred.stlouisfed.org/series/DGS10) |
| R-12 | Non-official citations | An inherited analysis layer contains rows citing a commercial brokerage and a private law firm. | Repository-only and excluded; the published register contains government and issuer pages only. | [Los Angeles Area Economic Summary · updated 2026-11-04](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) |
| R-13 | Account identifier in repository-only files | 26 HTML files in decision-file/ render a repository account handle. | Excluded from Pages; the published site contains no account, owner or parcel identifier. Flagged (F-20). | [ZIMAS · planning and zoning information system](https://zimas.lacity.org/) |
| R-14 | Personal information encountered during research | Official filings and agency pages contain named contacts, emails, telephone numbers and street addresses (SEC exhibit, CDE district profile, CAL FIRE incident pages, county assessor offices). | None of it is reproduced on the website. Asset A / Owner A placeholders are used throughout; a PII build gate scans every published file. | [District Profile · Los Angeles Unified (2025-26)](https://www.cde.ca.gov/sdprofile/details.aspx?cds=19647330000000) |
| R-15 | Census race-share inconsistency | City race-alone percentages sum to 74.3% versus 99.8% for the county. | City breakdown withheld and flagged (F-10); the county Hispanic share is published with its definition. | [Census QuickFacts · Los Angeles city (V2025)](https://www.census.gov/quickfacts/losangelescitycalifornia) |
| R-16 | Population estimates disagree | Census V2025 and CA DOF February-2026 publish different LA County figures for 2025-07-01. | Both are published with agency and vintage labels; mixing them is prohibited (F-09). | [July 2025 population estimates · revised release 2026-02-04](https://dof.ca.gov/media/docs/forecasting/Demographics/estimates/July2025_Population_Estimates_Feb26_release.pdf) |
| R-17 | Minimum-wage 2027 figure | A 2027 rate appears in secondary commentary but not on the DIR page. | Left blank and flagged (F-11); only the official 2026 rate is published. | [Minimum Wage FAQ](https://www.dir.ca.gov/dlse/FAQ_MinimumWage.htm) |
| R-18 | USGS ShakeOut link repair | An earlier programme URL returned 404; the official report host serves the document. | The canonical source register uses the official report host; scenario figures were re-read there. | [The ShakeOut Scenario · USGS OFR 2008-1150](https://pubs.usgs.gov/of/2008/1150/) |
| R-19 | FEMA NRI values | County-level National Risk Index scores were not readable from the official portal. | Left blank and flagged (F-18); no third-party mirror used. | [National Risk Index](https://hazards.fema.gov/nri/) |
| R-20 | BEA measure mislabelling | Some inherited text treats $818.5bn as LA County GDP; the BEA release reports it as total personal income. | Corrected and flagged (F-17); the BEA metro-series discontinuation is published as a verified row. | [GDP by county and personal income by county, 2024 (BEA 26-08)](https://www.bea.gov/news/2026/gross-domestic-product-county-and-personal-income-county-2024) |
| R-21 | Build determinism | Generated HTML was committed by multiple sessions with different generators, so a rebuild could silently change published files. | One generator now produces every published page; CI rebuilds and asserts a byte-identical diff. | [Los Angeles Area Economic Summary · updated 2026-11-04](https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf) |
| R-22 | Coordination board | COORDINATION.md documents 15+ sessions, several conflicts and four stale open PRs. | This session appended its own claims, sources and verification record; no earlier text was removed. | [ZIMAS · planning and zoning information system](https://zimas.lacity.org/) |

## Layer map

| Path / scope | Role | Disposition |
|---|---|---|
| Root `*.html` + `assets/style.css` | Canonical published site | Generated by `scripts/build_canonical.py` |
| `data/canonical.json`, `data/canonical_rows.py` | Machine-readable register | Source of truth; excluded from Pages |
| `research/VERIFICATION-2026-11-10-b98090a0.md` | Row-by-row verification log | Excluded from Pages; internal audit |
| `docs/`, `analysis/`, `brief/`, `pages/`, `decision-file/`, `advisory/`, `dashboard/` | Repository-only companion layers | Excluded from Pages by `_config.yml` |
| `audit/`, `research/archive/`, `site/`, `model/`, `tools/`, `scripts/`, `_advisory_src/`, `_dashboard_src/` | Audit trail and generators | Excluded from Pages |

## Verification procedure

1. Read `COORDINATION.md` and the full file inventory before claiming a task.
2. Enumerated every published HTML file and every external host it links to.
3. Re-fetched each official publisher page and compared every published numeric value against the
   text of that page, including geography, period, unit and vintage.
4. Recorded disagreements between agencies and between inherited layers rather than silently
   choosing one.
5. Left unconfirmable values empty and published them on the Flagged for Review page.
6. Redacted all personal information encountered during research; no owner, contact, address,
   parcel or account identifier appears on the site.
7. Rebuilt the entire site from one dataset and asserted a byte-identical rebuild in CI.

## Published-source restriction

The canonical site links only to government agencies and issuer filings. Repository-only layers
that cite commercial brokerage or private law-firm domains are excluded (R-12); the inherited
account-handle rendering is also excluded (R-13).

## Build gates

- `scripts/validate.py` — row provenance, official hosts, blank-value rule, internal links, PII,
  deterministic rebuild.
- `scripts/stage_pages.py` — exact Pages artifact, source-linked rows, Jekyll byte comparison.
- `.github/workflows/validate.yml` — full CI, `git diff --exit-code -- '*.html'`, Jekyll build.

<!-- b98090a0 canonical repo review: end -->
