# Jack3 — Central LA NNN Jack in the Box: Decision Desk

**Live site:** https://wingbangboozle1-lang.github.io/Jack3/ (GitHub Pages, serves `docs/` from `main`)

An anonymized, official-source analytical dashboard for one question: **sell a single-tenant NNN-leased
Jack in the Box restaurant in Central Los Angeles before its lease expires (2030–2035), or renew.**

Contents: executive summary · weighted sell-vs-renew decision matrix · interactive present-value
"Projection Studio" · area demographics, economy, income, schools, population projections · tenant
(Jack in the Box Inc.) fundamentals from SEC filings · hazard/black-swan analysis (Puente Hills
earthquake, Jan 2025 wildfires) · 14-item scored risk register · flagged-for-review list.

Every table row carries a source link to an official (.gov / SEC / State of California) source or is
explicitly labeled industry or flagged unverified — nothing is invented. No owner identity, street
address, parcel, listing, or personal financial data appears anywhere on the site, per the privacy mandate.

- Build: `python3 tools/build_site.py` (regenerates `docs/` from `data/site_data.json` + `tools/content_part*.py`)
- Shared task board: `COORDINATION.md`
- Not legal, tax, appraisal, or investment advice.
