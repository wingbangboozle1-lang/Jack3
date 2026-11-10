# Asset A — Los Angeles net-lease decision file

Privacy-safe, source-linked research for an anonymized single-tenant Jack in the Box NNN property reported to expire between 2030 and 2035. The question is whether to sell before expiry or renew while balancing wealth preservation, growth and manageable risk.

**Live site:** https://wingbangboozle1-lang.github.io/Jack3/  
**Evidence snapshot:** 2026-11-10

## Start here

- [Executive summary](EXECUTIVE_SUMMARY.md) — conditional recommendation, decision matrix, key findings and risks.
- [Line-by-line verification](research/VERIFICATION-2026-11-10-1f62010a.md) — all 155 rows and 30 official/issuer sources.
- [Verification summary](VERIFY.md) — build checks, corrections and privacy boundary.
- [Repository review](REPO_REVIEW.md) — irregularities and publication decisions.
- [Flagged for Review](review.html) — unresolved items and source irregularities.

## Recommendation

Run two tracks now: confidential sale market testing 24–36 months before the earliest contractual expiry, and a written renewal request. Choose only after comparing a documented after-tax offer with an enforceable, credit-supported extension. This is analyst judgment, not a valuation or personalized financial, legal or tax advice. Public sources cannot determine a personal optimum without the private lease and financial facts.

## Public pages

| Category | Contents |
|---|---|
| Executive summary | Recommendation, evidence and risk balance |
| Area fundamentals | Population, income, jobs, wages, CPI, assessment roll, transport funding |
| Demographics | Households, age, poverty, tenure and spending context |
| Tenant & lease | Latest issuer results, closure plan and missing lease facts |
| Risk & resilience | Business-as-usual and catastrophe risks |
| Neighborhood & land | Parcel-dependent evidence left blank |
| Schools & workforce | LAUSD enrollment and exact 2026 graduation measures |
| Decision pathways | Sell, renew, hold, extend-then-sell, re-tenant, redevelop, exchange |
| Taxes & transaction costs | Prop 13, city/county transfer taxes, ULA, §1031 and capital gains |
| Projection framework | Official SCAG/DOF projections plus a clearly labeled break-even sensitivity model; no calibrated parcel forecast |
| Flagged for Review | Unverified fields and irregularities |
| Sources & methodology | Source register, definitions, limitations and privacy |

## Build and verify

```bash
python scripts/build.py
python scripts/validate.py
python scripts/stage_pages.py
python tools/check_site.py
python tools/linkcheck.py
python tools/check_links.py
python tools/pii_scan.py
```

The Pages artifact contains only the curated root dashboard and its stylesheet. Historical companion layers (`advisory/`, `dashboard/`, `analysis/`, `brief/`, `decision-file/`, `docs/`, `pages/`, `report/`, and related sources) are preserved for audit but are not published or represented as reverified.

## Privacy and evidence rules

- **Asset A / Owner A are placeholders.** No personal, parcel or private financial information is collected or published.
- Every table row links to a government or issuer source.
- Unverified values are blank and flagged; values are never inferred to fill a gap.
- Official planning forecasts are identified as such. Break-even cap rates and growth rates are disclosed assumptions, not verified market facts. No sale price, renewal probability, disaster probability or calibrated 2030–2035 forecast is invented.
- The site has no forms, trackers, external scripts or third-party embeds.
