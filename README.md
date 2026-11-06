# Jack3 — Central LA Jack in the Box NNN Lease: Sell vs Renew Decision Brief

A private, anonymized decision-analysis microsite for the owner of one quick-service
Jack in the Box asset in Central Los Angeles on a triple-net (NNN) lease expiring
**2030–2035**. It answers: **sell before expiry, or renew at expiry?**

Live site: GitHub Pages (see repo **Settings → Pages**).

## What’s inside

| Page | Content |
|---|---|
| `index.html` | Dashboard — KPIs, recommendation, snapshot tables |
| `executive-summary.html` | One-page verdict, findings F1–F10, action plan |
| `market-demographics.html` | Population, income, housing, jobs, LAUSD schools — all sourced |
| `economic-outlook.html` | SCAG/EDD forecasts, DTLA 2040, assessment roll, rates |
| `decision.html` | NNN mechanics, tenant credit, Measure ULA worked examples, 1031, triggers |
| `risk-analysis.html` | Scored risk register R-01…R-22 (incl. wildfire, earthquake, unrest) |
| `projection-model.html` | Interactive scenario model (NOI → exit value, ULA drag, sensitivity) |
| `sources.html` | Master source register S-01…S-38 with links |
| `flagged.html` | Everything unverified / requiring owner input — nothing hidden |
| `research/RESEARCH.md` | Raw evidence log |
| `COORDINATION.md` | Multi-session task board & audit log |

## Integrity rules

- Every table row carries a source link; official sources preferred.
- Unverifiable values are **blank or flagged**, never estimated silently.
- **No personal information anywhere.** The property is "The Property"; the tenant is "The Tenant".
- Not legal, tax, or investment advice. Confidential.

## Local preview

No build step — static HTML/CSS/JS. Serve the repo root:

```bash
python3 -m http.server 8080
# open http://localhost:8080/
```

## Verification

Run the built-in checker from the repo root (stdlib only):

```bash
python3 tools/check_site.py
```

It validates that every internal href/src resolves to a file, that no page references
localhost/127.0.0.1, and that external links carry `rel="noopener"`.
