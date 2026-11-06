# Jack / Property intelligence

Privacy-safe, static research dashboard for an unidentified Los Angeles-area net lease asset, **plus** a deep-dive decision brief at `brief/` (see below).

**Live site:** https://wingbangboozle1-lang.github.io/Jack3/

## Evidence boundary
Official observations were manually checked on 2026-11-06. Property identity, lease, rent, debt and owner financial circumstances are absent. Regional context is not a parcel forecast. Missing numerical values stay blank; conditional analyst rules are not official recommendations. See `review.html` for nonblocking review flags and `sources.html` for methodology.

No personal information, addresses, parcel identifiers, owner research, analytics, forms or third-party executable assets are included. Do not commit private records, even in history.

## Build and check
```
python scripts/build.py
python scripts/validate.py
python tools/check_site.py   # checks the brief/ deep-dive site
python -m http.server 8000 --bind 0.0.0.0
```

`data/evidence.json` is the public source of truth. Rebuild HTML after edits. Validation checks internal links and row provenance, not live external availability or semantic truth. Source checks are manual and the site is a dated snapshot, not an automatic data feed. GitHub Pages serves the repository root on main; PR validation checks deterministic output before integration.

## Deep-dive decision brief (`brief/`)

Added by session `arena-796b983f-jack3` as a companion to the main research workspace. Opens at **https://wingbangboozle1-lang.github.io/Jack3/brief/** and includes:

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

The brief layer adds decision analysis and an interactive model on top of the main workspace's evidence register. Recommendation content is **analysis**, labeled as such — not official data and not personalized legal, tax, or investment advice. Mirror-sourced Census values are labeled; anything unconfirmable is blank or on `brief/flagged.html`.

`research/RESEARCH.md` holds this session's raw evidence log alongside `research/VERIFICATION.md` (the main workspace record).
