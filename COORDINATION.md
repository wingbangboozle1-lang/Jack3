# COORDINATION.md — Shared Task Board

Repo: wingbangboozle1-lang/Jack3 (work branch `arena/28eacae6-jack3`; PR opened from it into `main`)
Platform rule for this session: work only on `arena/28eacae6-jack3`; PR to `main`; no other branches created/pushed.
Claim format: session ID + file scope + commit/push note. `needs review` = published on the Flagged for Review page.

Session ID: arena-28eacae6

## Task Board

| # | Task | Status | Owner | File scope | Notes |
|---|------|--------|-------|------------|-------|
| 1 | Repo review + create COORDINATION.md | done | arena-28eacae6 | COORDINATION.md, root | Repo = initial commit `0c9e609` with only README.md ("# Jack3"). Nothing to code-audit; no credentials; no PII. |
| 2 | Research: tenant — Jack in the Box Inc. (SEC 10-K, proxy, IR releases) | done | arena-28eacae6 | research/**, data/site_data.json | All figures from sec.gov / investors.jackinthebox.com; see research/research-notes.md. |
| 3 | Research: LA demographics, income, schools, DOF projections, labor (Census/BLS/DOF/FRED/CAS Dashboard) | done | arena-28eacae6 | research/**, data/site_data.json | See rows in data/site_data.json; all rows sourced or flagged. |
| 4 | Research: rates, FHFA HPI, hazards (CAL FIRE/FEMA/USGS), LA28 catalysts | done | arena-28eacae6 | research/**, data/site_data.json | Industry sources (CBRE, LAEDC, MMCG) labeled INDUSTRY, never as official. |
| 5 | Privacy/anonymization (no PII, no address, no listing links anywhere) | done | arena-28eacae6 | all | Property referred to only as "the Property" / "Central Los Angeles NNN Jack in the Box". |
| 6 | Site build in docs/ (dashboard, 18 pages, tables, projection studio, risk register) | done | arena-28eacae6 | docs/**, tools/**, data/**, README.md | Build: `python3 tools/build_site.py`. Structure + local link check passed; all pages serve 200; projection math sanity-checked. |
| 7 | Verification pass (line-by-line vs official sources; blanks on unverifiable) | done | arena-28eacae6 | data/**, docs/**, research/** | Every row tagged VERIFIED (official) / INDUSTRY / FLAGGED; 14 flagged items published on Flagged for Review page. |
| 8 | Final integration: PR, merge, enable + confirm GitHub Pages deploy | done after merge — see log | arena-28eacae6 | docs/**, .github/**, COORDINATION.md | PR from arena/28eacae6-jack3 → main; merge without waiting; Pages served from main /docs. |

## Verification performed (Task 7 detail)
- Each row in data/site_data.json carries `status`: verified (official source URL on the row) | industry (CBRE/MMCG/LAEDC — not governmental, labeled) | flagged (value withheld; remediation listed on flagged-for-review.html).
- Official sources used and re-checked 2026-11-06: census.gov QuickFacts (LA city/county); FRED series LOSA106URN, SMS06310800000000001, CAUR, UNRATE, DGS10, ATNHPIUS06037A; dof.ca.gov P-2A (row 6037 LOS ANGELES verified from the xlsx itself, Vintage 2026, released 2026-03-13); caschooldashboard.org (LAUSD 2025); sec.gov (JACK 10-K FY2025 filed Nov 2025; proxy FY2025); investors.jackinthebox.com (Q1/Q3 FY2026 earnings, JACK on Track, Del Taco completion 2025-12-22); fire.ca.gov (Eaton & Palisades incident pages); gis-fema.hub.arcgis.com (DR-4856-CA); pubs.usgs.gov/publication/70029508 (Puente Hills $82–252B).
- Discrepancy found & disclosed (not hidden): Palisades Fire structures destroyed — LA County fact sheet 6,837 vs CAL FIRE incident page 6,845 (used 6,845; flagged).
- Methodology discrepancy found & disclosed: 2020 population 10,014,009 (Census) vs 10,012,050 (DOF P-2A 2024-baseline); series kept separate; flagged.
- Derived figures labeled as derived (e.g., HPI +28.4% 2021→2025; DOF −1.5% 2025→2035; weighted decision scores 3.55 / 3.80 / 4.25).
- NOT verified (blanks/flags, never guessed): subject rent/escalators/guarantor; parcel flood/seismic/zoning/retrofit; trade-area tract income; property-tax bill; CDI FAIR Plan latest; activist 8-K; QSR cap rate 4–6% (secondary source); LA28 $20–40B (commissioned study); FAIR Plan +43% growth (news).

## Status log
- 2026-11-06 — Initial commit 0c9e609 reviewed (README only). Board created; tasks claimed.
- 2026-11-06 — Research complete; research/research-notes.md committed (commit 2f2dbe4).
- 2026-11-06 — Site built (18 pages); build verified (all 200; link checker clean); decision matrix A=3.55 B=3.80 C=4.25 (C wins).
- 2026-11-06 — PR #4 created: https://github.com/wingbangboozle1-lang/Jack3/pull/4 (arena/28eacae6-jack3 → main). Merge pending; deploy + merge result recorded below after completion.

## Irregularities / handoffs
- Palisades Fire figure discrepancy (CAL FIRE 6,845 vs LA County 6,837) — disclosed on Flagged for Review #15; CAL FIRE used as primary.
- QuickFacts vs DOF 2020 population methodology difference — disclosed on Flagged for Review; not reconcilable without mixing series (kept separate).
- AB 1228 fast-food wage referenced only with "verify at DIR" flag; no unverified wage number asserted.
- No handoffs taken over; no other session claimed tasks during this window.
