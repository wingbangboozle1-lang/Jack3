# Independent targeted publication audit — 2026-11-12

Scope: targeted sample and automated checks, **not** a line-by-line re-verification of the full repository. Earlier sessions' verification claims were not independently repeated here. No owner, parcel, address, lease or personal information was researched or recorded.

## Direct checks

| Check | Result | Source |
|---|---|---|
| City population | 3,869,089, July 2025; −0.8% from the 2020 estimates base. Citywide context, not a trade-area estimate. | [Census QuickFacts](https://www.census.gov/quickfacts/losangelescitycalifornia) |
| City transfer tax | For closings after June 30, 2026, the City states a 4% ULA rate above $5.4m and below $10.9m; 5.5% at or above $10.9m. Thresholds are adjusted annually. Applicability to Asset A is unverified. | [LA Office of Finance](https://finance.lacity.gov/faq/measure-ula) |
| District graduation | The 2026 Dashboard page displays 87.6% graduated for Los Angeles Unified; this is district context and does not establish the property's school attendance zone. | [California School Dashboard](https://www.caschooldashboard.org/reports/19647330000000/2026) |
| County jobs, separate historical series | BLS reports Los Angeles County covered employment fell 0.5% March 2024–March 2025. This is not comparable as the same geography or period to the landing page's September 2026 metro figure. | [BLS](https://www.bls.gov/opub/ted/2025/employment-up-over-the-year-in-221-of-the-372-largest-u-s-counties-march-2025.htm) |

## Items requiring review

- The landing page recommends an extension of at least ten years and a 24–36 month marketing window. These are analytical heuristics, not official-source facts or established optima for the unknown property. Notice deadlines, negotiated terms, credit, pricing and personal circumstances could justify a different timetable or term. The decision should not be taken solely on these thresholds.
- The site has a decision matrix, questions and review pages, but no clearly titled dedicated **site-improvement suggestions** page. Request to the integration session: add a source-linked suggestions register distinguishing proposed improvements from implemented changes, with priority, rationale, tradeoffs, dependencies and review status. Do not present a proposal as approved.
- README's build section says 20 pages / 222 rows, while the current generator reports 21 pages / 223 rows; it also retains historical companion URLs that are explicitly excluded from the deployed artifact. Request to README owner: reconcile current counts and clearly identify old URLs as non-live.
- Public asset-specific outputs cannot be validated without the underlying private records. The lease expiry, options and notice windows, rent, tenant and guarantor obligations, parcel location, operating performance, offer, basis, debt, insurance and individual goals remain unknown. Geographic, hazard and school data for a large region do not establish conditions at this parcel. A tailored forecast or sell-versus-renew answer would be speculative.
- Automated link checks establish local target/fragment integrity and source-host formatting, **not** availability or factual support of every external link. A regex PII scan reduces risk but cannot prove absence of all personal information. Official sources may change after a snapshot.

## Local and deployment checks

On the branch based on `6b1979d`, `scripts/build.py`, `scripts/validate.py`, `scripts/stage_pages.py`, all eight `test_publication.py` tests, `tools/check_site.py`, `tools/linkcheck.py`, `tools/check_links.py`, `tools/pii_scan.py`, `_advisory_src/verify_advisory.py`, `_dashboard_src/verify.py`, and generated HTML diff check passed. Legacy `check_site.py` and `linkcheck.py` check companion directories; the staging and publication tests check the actual staged site. Scans are not a substitute for manual factual verification.

GitHub reported the Pages build at `6b1979d` built; the Pages deployment, research-validation and artifact-regression Actions runs on that commit were successful. The landing page was fetched successfully at https://wingbangboozle1-lang.github.io/Jack3/ on 2026-11-12. This is evidence of the existing deployment, not a guarantee of future availability.
