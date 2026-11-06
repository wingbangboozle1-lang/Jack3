# Jack / Property intelligence

Privacy-safe, static research dashboard for an unidentified Los Angeles-area net lease asset.
It is published in layers, all linked from the root landing page and from here.

**Live site:** https://wingbangboozle1-lang.github.io/Jack3/

## What is published

| Layer | Path | Built by | What it is |
|---|---|---|---|
| Evidence workspace | `/` (root) | `scripts/build.py` + `data/evidence.json` | Evidence-gated brief: known vs not-verifiable, decision pathways, flagged review |
| Research tables | `/docs/` | session `ff406d61` | Verified research dashboard, row-level official sources, flagged review |
| Deep-dive evidence dashboard | `/analysis/` | session `8d650ba0` | 11 pages generated from JSON; 113 sourced indicators; 22-row risk register; scenario model; decision framework |
| Deep-dive decision brief | `/brief/` | session `arena-796b983f-jack3` | 9 pages; interactive sell-vs-renew scenario model; scored risk register R-01…R-22; Measure ULA worked examples; flagged review |

## Evidence boundary
Official observations were manually checked on 2026-11-06. Property identity, lease, rent, debt and owner financial circumstances are absent. Regional context is not a parcel forecast. Missing numerical values stay blank; conditional analyst rules are not official recommendations. See `review.html` for nonblocking review flags and `sources.html` for methodology.

No personal information, addresses, parcel identifiers, owner research, analytics, forms or third-party executable assets are included. Do not commit private records, even in history.

## Build and check
```
python scripts/build.py
python scripts/validate.py
python tools/check_site.py   # checks the brief/ deep-dive site
python3 tools/linkcheck.py   # checks the analysis/ deep-dive site anchors
python -m http.server 8000 --bind 0.0.0.0
```

`data/evidence.json` is the public source of truth. Rebuild HTML after edits. Validation checks internal links and row provenance, not live external availability or semantic truth. Source checks are manual and the site is a dated snapshot, not an automatic data feed. GitHub Pages serves the repository root on main; PR validation checks deterministic output before integration.

---

## Deep-dive decision brief (`brief/`)

Added by session `arena-796b983f-jack3` as a companion to the main research workspace. It complements the `analysis/` deep-dive (above): same anonymization boundary, more emphasis on interactive decision support and a plain-language sell-vs-renew playbook. Opens at **https://wingbangboozle1-lang.github.io/Jack3/brief/**.

| Page | Content |
|---|---|
| `brief/index.html` | Dashboard — KPIs, headline recommendation, snapshot tables |
| `brief/executive-summary.html` | Verdict, findings F1–F10, decision scorecard, dated action plan |
| `brief/market-demographics.html` | Population, income, housing, jobs, LAUSD schools — row-sourced |
| `brief/economic-outlook.html` | SCAG/EDD forecasts, DTLA 2040, assessment roll, rates & cap rates |
| `brief/decision.html` | NNN mechanics, tenant credit, Measure ULA worked examples, 1031, triggers |
| `brief/risk-analysis.html` | Scored risk register R-01…R-22 (incl. wildfire, earthquake, unrest) |
| `brief/projection-model.html` | Interactive NOI → exit-value scenario model + sensitivity grid |
| `brief/sources.html` | Master source register S-01…S-38 |
| `brief/flagged.html` | All unverified values / owner-input blockers — nothing hidden |

Recommendation content in `brief/` is **analysis**, labeled as such — not official data and not personalized legal, tax, or investment advice. Mirror-sourced Census values are labeled; anything unconfirmable is blank or on `brief/flagged.html`.

`research/RESEARCH.md` holds this session's raw evidence log alongside `research/VERIFICATION.md` (root-workspace record), `research/demographics.md`, `research/economy.md` … (docs/ session) and `research/verification-log.md` (analysis/ session).

---

## Deep-dive evidence dashboard (`analysis/`)

A third, additive layer produced by session `sess-8d650ba0` sits in **`analysis/`** — 11 pages generated from JSON, with
113 sourced indicators, a 22-row risk register, a deterministic scenario model and a decision framework.

**Open it at:** `/analysis/index.html` (or the "Deep-dive evidence dashboard" link on the root landing page).

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

The two earlier dashboards (root, `docs/`) are unchanged apart from additive links to the deep dives.
Line-by-line check record: `research/verification-log.md`.

## Repository hygiene
`COORDINATION.md` is the shared multi-session task board — read it before editing anything; parallel sessions worked this repository simultaneously on 2026-11-06 and every session's scope is preserved there.

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
