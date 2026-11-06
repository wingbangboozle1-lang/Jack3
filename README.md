# Jack in the Box NNN — Central Los Angeles · decision research

**Live site:** https://wingbangboozle1-lang.github.io/Jack3/

A verified, source-linked research package answering one question: for a Jack in the Box triple-net property in central
Los Angeles whose lease expires between 2030 and 2035, is it better to **sell before expiry** or **renew** — and what is
the best decision for the owner as an individual, balancing wealth preservation against growth and manageable risk?

## What is inside

| Page | What it answers |
|---|---|
| `index.html` | Dashboard: recommendation, executive summary, top risks, verification counts |
| `economy.html` | Population, income, housing, employment by sector, prices and rates |
| `tenant.html` | Jack in the Box Inc. unit counts, closures, same-store sales, guidance, Del Taco divestiture |
| `property.html` | Proposition 13, the 2026 assessment roll, transfer taxes, Measure ULA, value matrix, §1031 |
| `risk.html` | 22 risks: 13 business-as-usual and 9 black swan, with mitigations |
| `scenarios.html` | Deterministic hold-versus-sell model, sensitivity grids, after-tax illustration |
| `decision.html` | Five options scored, the recommendation, sell triggers, dated action plan |
| `data.html` | The full dataset — 113 rows, each with a source link and a verification status |
| `flagged.html` | 13 items that could not be verified, with what is needed to close each one |
| `sources.html` | 28 sources with tier, publisher, URL and access date |
| `methodology.html` | Verification standard, anonymisation rules, model method, limitations |

## Privacy

The property address, parcel number, owner identity, franchisee identity and all personal information are **not** in this
repository or on the site. The asset is `[PROPERTY-A]` and the owner `[OWNER-1]`. Every published statistic is
area-level (Los Angeles County, City of Los Angeles, or the LA–Long Beach–Anaheim metro) and available to the public.
See `methodology.html` for the full rule.

## The short answer

Hold, extend and prepare; sell only on a defined trigger. Under the disclosed base case an unlevered hold returns
**8.03%/yr** against **7.25%/yr** for selling now and deferring tax through a §1031 exchange, and holding only loses if the
exit cap rate widens to **7.22%** or more. The counterweight is tenant contraction (86 closures vs 31 openings in FY2025,
same-store sales −4.2%), which is why the recommendation is a *conditional* hold with a hard decision gate in 2029.
Full reasoning in `decision.html`; every assumption disclosed in `scenarios.html`.

## Repository layout

```
*.html                     built pages (GitHub Pages serves main /)
assets/css/style.css        styling
assets/js/app.js           table filtering on the master dataset page
assets/data/sources.json    28 sources, tiered, with URLs
assets/data/dataset.json    113 verified indicators
assets/data/risks.json      22-row risk register
assets/data/flagged.json    13 unverified items
assets/data/scenarios.json  model output (generated, not hand-edited)
tools/model.py             deterministic scenario model
tools/build.py             static site generator
tools/linkcheck.py         internal link and anchor checker
research/verification-log.md  line-by-line record of every check
COORDINATION.md            shared task board, claims and log
```

## Rebuild

```bash
python3 tools/model.py     # recompute scenarios.json
python3 tools/build.py     # regenerate all HTML
python3 tools/linkcheck.py # fail on any broken internal link or anchor
```

The build is deterministic: no network access, no hand-typed figures in the HTML.

## Sources

28 sources, tiered. Tier 1 is government, statute or court (Census, BLS, FRED/Federal Reserve, LA County Assessor and
Recorder, USGS/CGS, CAL FIRE, CDE, DIR, IRS, California Secretary of State). Tier 2 is filed or official issuer
disclosure (SEC EDGAR, LA28). Tier 3 is industry research (The Boulder Group) and is labelled as such everywhere it
appears.

## Not advice

Research for internal decision support only — not legal, tax or investment advice. Engage a California-licensed
appraiser, a CPA with real-estate tax experience and a land-use attorney before acting, and re-confirm every statutory
rate for the closing date.
