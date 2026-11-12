# Asset A — Los Angeles net-lease decision file

Privacy-safe, source-linked research for an anonymized single-tenant Jack in the Box NNN property reported to expire between 2030 and 2035. The question is whether to sell before expiry or renew while balancing wealth preservation, growth and manageable risk.

**Live site:** https://wingbangboozle1-lang.github.io/Jack3/

> **Current canonical site (2026-11-11).** This repository now publishes **one** consolidated site, generated
> from a single verified register. The descriptions of earlier companion layers further down this README are
> historical audit trail; those directories are excluded from GitHub Pages and are not the live product.

## Start here

- [Executive summary](EXECUTIVE_SUMMARY.md) — conditional recommendation, decision matrix, key findings and risks.
- [Line-by-line verification](research/VERIFICATION-2026-11-11-d644184d.md) — all 223 canonical rows, with row-level dispositions and 36 official/issuer sources (audit dated 2026-11-11).
- [Verification summary](VERIFY.md) — build checks, corrections and privacy boundary.
- [Repository review](REPO_REVIEW.md) — irregularities and publication decisions.
- [Flagged for Review](review.html) — unresolved items and source irregularities.

## Recommendation

Verify lease dates and notice rights privately now; prepare sale and renewal tracks on a timeline the documents support. Compare documented after-tax offers with enforceable renewal terms and downside risks; no minimum renewal term or fixed marketing deadline is established. This is analyst judgment, not a valuation or personalized financial, legal or tax advice. Public sources cannot determine a personal optimum without the private lease and financial facts.

## Public pages

| Category | Contents |
|---|---|
| [Live dashboard](https://wingbangboozle1-lang.github.io/Jack3/) | Clean landing page, eight evidence categories, analysis pages and governance pages |
| [Executive summary](executive-summary.html) | Recommendation, decision matrix, six driving findings, risk balance, and what stays blank |
| [Suggestions to review](suggestions.html) | Proposed improvements and trade-offs for review before implementation |
| [All entries & findings](master.html) | Every published row in one source-linked table |
| [Flagged for Review](review.html) | Every unverified value, conflict and irregularity, published for manual review |
| [Repo review](repo-review.html) | Line-by-line findings on the inherited repository layers |
| [Line-by-line verification record](research/VERIFICATION-2026-11-11-d644184d.md) | 223-row canonical disposition register; independent official-source review dated 2026-11-11, plus corrections and gaps |
| [Sources & method](sources.html) | 36 official sources, verification standard and privacy boundary |

## Build and verify

22 static HTML pages (including the `flagged.html` alias) plus `assets/style.css`, for a 23-file Pages artifact. Every table body row carries an official source link; every
unconfirmed value is an **empty cell** and appears on *Flagged for Review*. No JavaScript, forms, analytics,
third-party assets, owner identifiers, addresses or parcel numbers.

| Page | Path | Contents |
|---|---|---|
| Overview / dashboard | `/` | Conditional recommendation, six verified anchors, risk balance, navigation |
| Executive summary | `/executive-summary.html` | Decision, findings, matrix, evidence gates, what stays blank |
| All entries & findings | `/master.html` | 223-row master register, grouped by category |
| Geography | `/geography.html` | City / county scale; every parcel-level gap flagged |
| People & income | `/demographics.html` | Population, households, income, poverty, education, spending capacity |
| Economy & jobs | `/economy.html` | Employment, wages, prices, output, rates, official long-range forecasts |
| Schools | `/schools.html` | LAUSD scale, graduation outcomes, attendance-boundary gap |
| Tenant & lease | `/tenant.html` | Issuer SEC filings, closure programme, missing executed lease |
| Taxes & transfer | `/taxes.html` | Prop 13, transfer taxes, Measure ULA, capital gains, §1031 |
| Hazards | `/hazards.html` | Earthquake, wildfire, flood: official observations and scenarios |
| Projection anchors | `/anchors.html` | Dated observations, official forecasts and withheld outputs |
| Risk register | `/risk.html` | 24 business-as-usual and black-swan risks, with context sources |
| Projection system | `/projections.html` | 13-step reproducible framework and the outputs deliberately withheld |
| Decision matrix | `/decisions.html` | Eight pathways, gates and the recommended sequence |
| Model & method | `/model.html` | Verification standard, published arithmetic, monitoring checklist |
| Evidence boundary | `/place.html` | What the site deliberately does not assert about Asset A |
| Flagged for Review | `/review.html` (alias `/flagged.html`) | Unverified values, conflicts and irregularities |
| Repo review | `/repo-review.html` | Line-by-line inherited-layer findings |
| Sources & method | `/sources.html` | Official source register, verification standard, privacy boundary |

## Build and verification

```
python3 scripts/build_canonical.py   # regenerate every published page + data/canonical.json + verification log
python3 scripts/validate.py          # row provenance, official hosts, blank values, links, PII, determinism
python3 scripts/stage_pages.py       # build the exact Pages artifact and check every row / link
```

`scripts/build.py` is a compatibility alias for the canonical generator. `.github/workflows/validate.yml` runs
the whole gate, rebuilds with Jekyll and asserts the published artifact byte-for-byte. The machine-readable
register is `data/canonical.json`; its source of truth is `data/canonical_rows.py`.

## Privacy boundary

Asset A and Owner A are placeholders. No property address, parcel number, owner name, account handle, contact
detail, financial account, tax basis, debt statement or private lease record is published. Official pages consulted
during research contain personal contact information; none of it is reproduced on the site.

## Repository-only layers (audit trail, not published)

The repository also preserves earlier parallel layers — `advisory/`, `analysis/`, `audit/`, `brief/`,
`dashboard/`, `decision-file/`, `docs/`, `pages/`, `research/`, `_advisory_src/`, `_dashboard_src/`, `site/`,
`model/`, `tools/` and `data/` sources. They are kept for audit and continuity, are **excluded from the live site**,
and are not claimed to be re-verified. `advisory/` in particular is withheld because its numerical scenario weights
and pathway rankings are not established by the official sources it cited. See `repo-review.html` and
`REPO_REVIEW.md`.

---

## Historical companion-layer documentation (audit trail)

The sections below were written by earlier parallel sessions and describe repository-only directories. They are
preserved verbatim; those directories are not published on the live site.

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

The Pages artifact contains only the curated root dashboard and its stylesheet. Historical companion layers (`advisory/`, `dashboard/`, `analysis/`, `brief/`, `decision-file/`, `docs/`, `pages/`, `report/`, and related sources) are preserved for audit but are not published or represented as reverified.

## Privacy and evidence rules

- **Asset A / Owner A are placeholders.** No personal, parcel or private financial information is collected or published.
- Every table row links to a government or issuer source.
- Unverified values are blank and flagged; values are never inferred to fill a gap.
- Official planning forecasts are identified as such. Break-even cap rates and growth rates are disclosed assumptions, not verified market facts. No sale price, renewal probability, disaster probability or calibrated 2030–2035 forecast is invented.
- The site has no forms, trackers, external scripts or third-party embeds.
