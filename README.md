# Jack / Property intelligence

Privacy-safe, static research dashboard for an unidentified Los Angeles-area net lease asset.

**Live site:** https://wingbangboozle1-lang.github.io/Jack3/

## Evidence boundary
Official observations were manually checked on 2026-11-06. Property identity, lease, rent, debt and owner financial circumstances are absent. Regional context is not a parcel forecast. Missing numerical values stay blank; conditional analyst rules are not official recommendations. See `review.html` for nonblocking review flags and `sources.html` for methodology.

No personal information, addresses, parcel identifiers, owner research, analytics, forms or third-party executable assets are included. Do not commit private records, even in history.

## Build and check
```
python scripts/build.py
python scripts/validate.py
python -m http.server 8000 --bind 0.0.0.0
```

`data/evidence.json` is the public source of truth. Rebuild HTML after edits. Validation checks internal links and row provenance, not live external availability or semantic truth. Source checks are manual and the site is a dated snapshot, not an automatic data feed. GitHub Pages serves the repository root on main; PR validation checks deterministic output before integration.

---

## Deep-dive evidence dashboard (`analysis/`)

A third, additive layer produced by session `sess-8d650ba0` sits in **`analysis/`** — 11 pages generated from JSON, with
113 sourced indicators, a 22-row risk register, a deterministic scenario model and a decision framework.

**Open it at:** `/analysis/index.html` (or the "Deep-dive evidence dashboard" link on the two landing pages).

| Page | What it answers |
|---|---|
| `analysis/index.html` | Dashboard: recommendation, executive summary, top risks, verification counts |
| `analysis/economy.html` | Population, income, housing, employment by sector, prices and rates |
| `analysis/tenant.html` | Jack in the Box Inc. unit counts, closures, same-store sales, guidance, Del Taco divestiture |
| `analysis/property.html` | Proposition 13, 2026 roll, transfer taxes, Measure ULA, value matrix, §1031 |
| `analysis/risk.html` | 22 risks: 13 business-as-usual and 9 black swan, with mitigations |
| `analysis/scenarios.html` | Hold-versus-sell model, sensitivity grids, after-tax illustration |
| `analysis/decision.html` | Five options scored, recommendation, sell triggers, dated action plan |
| `analysis/data.html` | 113-row master table, each row with a source link and status |
| `analysis/flagged.html` | 13 items that could not be verified, and what closes each one |
| `analysis/sources.html` | 28 sources with tier, publisher, URL and access date |
| `analysis/methodology.html` | Verification standard, anonymisation, model method, limitations |

Rebuild just this layer:

```
python3 tools/model.py       # recompute analysis/data/scenarios.json
python3 tools/build.py       # regenerate the 11 pages in analysis/
python3 tools/linkcheck.py   # fail on any broken internal link or anchor
```

The two earlier dashboards (root, `docs/`) are unchanged apart from one additive link to the deep dive. Line-by-line check
record: `research/verification-log.md`.

---

## Full sourced dashboard (`pages/`) — session `93f3087c`

A fourth, additive layer produced by session `93f3087c` sits in **`pages/`** — a self-contained static dashboard
(landing + 8 subpages: executive summary, market research, lease & tenant, risk analysis, projections, repo review,
sources, flagged-for-review) with its own assets. Every table row carries a source link; unverifiable values are blank
and listed on `pages/flagged.html`; all personal information is anonymized.

**Open it at:** `/pages/index.html` (also linked from the root landing page).

Research documents backing it live in `docs/*.md` (`docs/executive-summary.md`, `docs/research-economy.md`,
`docs/research-realestate.md`, `docs/risk-analysis.md`, `docs/repo-review.md`).

Headline recommendation (base case): **sell before the 2030–2035 lease expiry (target 2027–2029) via an IRS §1031
exchange**; hold only if a ≥10-year extension at/above current rent is signed now. See `pages/executive-summary.html`.
