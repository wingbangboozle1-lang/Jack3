# Independent integration audit — 2026-11-07

Scope: targeted review, not certification of every row or external link. Public results: `audit-1a9deb2a.html`. No property identification or owner information was researched.

## Verification

- Census QuickFacts directly checked: city 2025 population 3,869,089, county 9,694,934; 2020 estimates-base-to-2025 change −0.8% and −3.2%, respectively. These describe different geographies and do not establish a parcel trade area. https://www.census.gov/quickfacts/fact/table/losangelescitycalifornia,losangelescountycalifornia/PST045225
- California FTB 2025 Form 593 instructions checked: exceptions require applicable conditions or certification; filing alone does not establish exemption. https://www.ftb.ca.gov/forms/2025/2025-593-instructions.html
- IRS capital gains page checked: adjusted basis and realized amount matter; rates vary. https://www.irs.gov/taxtopics/tc409
- The IRS like-kind exchange URL referenced in `pages/executive-summary.html` returned a page marked 404 in the page body. https://www.irs.gov/businesses/small-businesses-self-employed/like-kind-exchanges
- Inspection of `pages/executive-summary.html` found its subject lease no-renewal and franchisee rent-payer claims unsupported by the undisclosed subject lease, and a 1031/Form 593 recommendation that cannot be established for an unidentified owner's tax circumstances. Chain-wide disclosures do not establish the subject contract: https://www.sec.gov/Archives/edgar/data/807882/000080788225000072/jack-20250928.htm
- Inspection of `decision-file/executive-summary.html` found franchise agreement termination dates equated to the subject real estate lease expiry without evidence, model worst-case treated as a floor, and risk rows without source links. `model/projection.py` contains judgmental property-specific assumptions, not verified facts. https://home.treasury.gov/resource-center/data-chart-center/interest-rates
- `pages/lease-analysis.html` publishes third-party numerical cap-rate estimates, conflicting with the official-source-only requirement. Needs review, not treated as verified.
- `python scripts/validate.py`, `python tools/check_site.py`, `python tools/linkcheck.py`, `python tools/check_links.py`, and `python tools/pii_scan.py` passed on their respective stated scopes. These do not certify external URLs, facts, complete repository privacy, or cross-dashboard consistency.

The root dashboard's cautious conditional recommendation conflicts with the companion layers' categorical sell recommendations. A reliable property-specific forecast or individual recommendation cannot be established without private lease, property, tax, liquidity and valuation evidence; no property-specific values were supplied or invented. Remediation requests are recorded in COORDINATION.md, rather than editing another session's claimed files.
