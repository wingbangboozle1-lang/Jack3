# Asset A — net-lease decision file (central Los Angeles)

Privacy-safe, static, source-linked research into a single-tenant Jack in the Box net-leased property in central
Los Angeles, reported by the owner to expire between 2030 and 2035. The question: **sell before expiry, or renew?**

**Live dashboard:** https://wingbangboozle1-lang.github.io/Jack3/

## Start here

| Document | What it gives you |
|---|---|
| [Executive summary](EXECUTIVE_SUMMARY.md) | Recommendation, decision matrix, the six findings that drive it, risk balance, and what stays blank |
| [Live dashboard](https://wingbangboozle1-lang.github.io/Jack3/) | Twelve category pages, every table row carrying its official source |
| [Line-by-line verification record](research/VERIFICATION-2026-11-08.md) | Every published row re-read against its publisher page on 2026-11-08, plus gaps, link repairs and irregularities |
| [Re-verification addendum](research/VERIFICATION-2026-11-10.md) | Two flagged items closed on 2026-11-10 (V-3 county transfer tax, V-4 LAUSD graduation rate) with exact page evidence; combined-tree checks |
| [Flagged for Review](review.html) | Everything that could not be verified, published rather than hidden |

## What is published on the live site

| Page | Path | Contents |
|---|---|---|
| Executive summary / dashboard | `/` | Recommendation, evidence boundary, risk balance, category navigation |
| Area fundamentals | `/economy.html` | Population, income, payrolls, unemployment, wages, CPI, ECI |
| Trade area & demographics | `/demographics.html` | Households, age, poverty, tenure, spending capacity |
| Tenant & lease | `/tenant.html` | Issuer results, closures, capital structure, and the lease facts we do not have |
| Risk & resilience | `/risk.html` | Business-as-usual risks, black-swan events, mitigation tests |
| Neighborhood & land | `/place.html` | What cannot be asserted without a parcel |
| Schools & workforce | `/schools.html` | CDE enrollment and English-learner data; missing performance measures |
| Decision pathways | `/decisions.html` | Six routes, triggers, dominant risks, recommended sequence |
| Taxes & transaction costs | `/taxes.html` | Prop 13, transfer taxes, Measure ULA, §1031, capital-gain treatment |
| Projection framework | `/model.html` | Verified anchors and the forecasts deliberately withheld |
| Flagged for Review | `/review.html` | Unverified items with the official page that would close each one |
| Sources & methodology | `/sources.html` | 26-source register, verification standard, privacy boundary |
| Category dashboard | `/dashboard/` | 15-page deep-dive decision desk: verified dataset, risk register, projections, decision matrix (merged as PR #33) |

Only these files, `dashboard/` and `assets/style.css` are staged into the Pages artifact by `scripts/stage_pages.py`.

## Repository-only layers (audit trail, not published)

The repository also preserves earlier parallel layers — `advisory/`, `docs/`, `analysis/`, `brief/`, `pages/`,
`decision-file/`, `report/`, `verification-3644edd8/`, `audit/` and `_advisory_src/`. They are kept for audit and
continuity, are **excluded from the live site**, and are not claimed to be re-verified. `advisory/` in particular is
withheld because its numerical scenario weights and pathway rankings are not established by the official sources it
cited (see `review.html`).

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
---

## Verified decision file (`decision-file/`) — session `arena-d989a5c6-jack3`

A fifth, additive layer. Self-contained: 23 pages generated by `build_site.py` from a committed
Python data snapshot in `data/`, plus 23 CSV exports of the same snapshot. No hand-typed figures
in any HTML page, no runtime fetching, no CDN, no framework.

**Open it at:** https://wingbangboozle1-lang.github.io/Jack3/decision-file/

**Headline recommendation: SELL** — and if the tenant will commit to an early extension first, buy
the term and then sell the lengthened lease. Do not plan around renewing at expiry.

| Page group | Pages |
|---|---|
| Overview | `index.html` dashboard, `executive-summary.html`, `methodology.html`, `privacy.html` |
| The Asset | `property-profile.html` (20-field Input Register), `geography.html`, `lease-economics.html` |
| The Tenant | `tenant.html` (SEC filings only), `tenant-closures.html` |
| The Market | `demographics.html`, `employment.html`, `projections.html`, `infrastructure.html` |
| The Decision | `projection-model.html`, `valuation.html`, `decision.html`, `taxes.html` |
| Risk | `risk-register.html`, `hazards.html`, `black-swan.html` |
| Assurance | `sources.html`, `flagged-for-review.html`, `repo-review.html` |

### What this layer adds that the others do not

- **The model is normalised to `R` = one year of current contractual base rent**, so it produces a
  defensible strategy ranking without inventing a rent, basis or building size. Sell-versus-hold
  compares two streams from the same asset, so the rent level largely cancels out of the ranking.
- **Every assumption carries a favourability direction**, so the optimistic scenario takes the
  favourable extreme of *every* assumption and the pessimistic scenario the unfavourable extreme of
  every one. Without this, a sensitivity grid silently mixes the two.
- **Conclusions are reported by worst-case rank, not just expected value.** Selling now has the
  highest floor of any strategy (11.62 R pessimistic); renewing the incumbent ranks last in both the
  base and pessimistic scenarios (1.18 R).
- **The discount rate is anchored to a verified official rate** — the U.S. Treasury 10-year par yield
  of 4.19% at 2026-01-02 — plus a separately declared risk premium swept 2.0–5.5%.
- **Blanking of unverified values is enforced in code**, by `build_site.py:value_cell()`, not by
  convention. It is not possible for an unverified row to render a number.
- **`tools/pii_scan.py` is a hard privacy gate** that fails the build on any email address, telephone
  number, street address, parcel number, taxpayer identifier, identifying field value or tenant
  officer name across 64 files.

### Rebuild and check just this layer

```
python3 build_site.py        # data/ + model/ -> decision-file/
python3 tools/check_links.py # exit 0: 1,013 links, 30 hosts, 0 non-official
python3 tools/pii_scan.py    # exit 0: 64 files, 0 findings
python3 -m model.projection  # deterministic; no network, no randomness
```

`build_site.py` writes **only** to `decision-file/`. It never touches `docs/`, the root `index.html`,
`analysis/`, `brief/`, `pages/`, `scripts/` or `.github/workflows/`.

Written deliverables for this layer: `EXECUTIVE_SUMMARY.md`, `VERIFY.md`, `REPO_REVIEW.md`,
`research/RESEARCH_LOG.md`.

### Deliberately blank in this layer (also on `decision-file/flagged-for-review.html`)

`F-01` the property identity (never supplied) · `F-02` commercial cap rates (no US government agency
publishes them) · `F-04` CA DOF county projections for 2030/2035/2040 (`.xlsx` only) · `F-05` tax
rates on a sale (IRS and FTB pages returned 404) · `F-03` FEMA NRI values (not readable on fema.gov)
· `F-12` LA *city* QuickFacts race shares do not reconcile (sum ≈74% vs county 99.8%) — the city
breakdown is omitted rather than published possibly wrong.

None of these blocks the recommendation.
