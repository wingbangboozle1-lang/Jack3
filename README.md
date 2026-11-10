# Asset A — a Jack in the Box NNN property decision file

A privacy-safe, source-linked research file on one single-tenant Jack in the Box net-leased restaurant property in
central Los Angeles, reported by the owner to expire between 2030 and 2035. The question is whether to sell before
expiry or renew.

**Live dashboard:** https://wingbangboozle1-lang.github.io/Jack3/

| Document | What it gives you |
|---|---|
| [Executive summary](EXECUTIVE_SUMMARY.md) | The recommendation, the six findings behind it, the decision matrix, the risk balance, the projection system and what is deliberately missing |
| [Live dashboard](https://wingbangboozle1-lang.github.io/Jack3/) | Twelve category pages; every table row carries its official source; filter and status chips work with no network |
| [Line-by-line verification record](research/VERIFICATION-2026-11-10.md) | Every published value re-read on its publisher's page on 2026-11-10, with corrections, failed attempts and rollovers |
| [Repository review](REPO_REVIEW.md) | Line-by-line review of what was in this repository, twelve findings (IR-01…IR-12), and what was changed |
| [Flagged for review](https://wingbangboozle1-lang.github.io/Jack3/review.html) | Everything that could not be verified, published rather than hidden, with the check that would close each item |

## The recommendation in one paragraph

Run a dual track now: take the asset to market confidentially 24–36 months before the earliest possible expiry, and in
the same quarter demand renewal terms in writing — rent, escalators, options, expense caps and a guaranty. Then act on
whichever the documents support: a verified after-tax bid, or an enforceable extension of ten years or more at market
rent with acceptable credit. At expiry the landlord has no income and the tenant has no obligation, so waiting is the
one route that hands the leverage to the other side. This is analyst judgement on public evidence, not a valuation and
not advice.

## What is published

| Page | Contents |
|---|---|
| `/` | Recommendation, six headline indicators, the risk balance, category navigation |
| `/economy.html` | Unemployment, payrolls by sector, CPI, ECI, wages, consumer spending |
| `/demographics.html` | Population, households, income, poverty, tenure, labour participation |
| `/geography.html` | Land area, density, commute, housing stock, permits, economic-census sales |
| `/schools.html` | District scale and enrollment; the measures that need a parcel |
| `/tenant.html` | Issuer results, unit counts, closures, margins, capital structure |
| `/risk.html` | 19 rows: business-as-usual risks, then black-swan events, each with a mitigation test |
| `/taxes.html` | Prop 13, city and county transfer taxes, Measure ULA, §1031, capital gains, NIIT |
| `/decisions.html` | Six decision routes, the triggers that switch between them, and the limits |
| `/model.html` | The projection framework: verified anchors, reproducible arithmetic, explicit refusals |
| `/review.html` | Nineteen flagged items, each with the source and the check that closes it |
| `/sources.html` | 31 official sources, the verification standard, the privacy boundary, reproducibility |

## Numbers at a glance

| | |
|---|---|
| Official sources re-read on 2026-11-10 | 31 |
| Evidence rows | 166 |
| Verified, plus derived arithmetic recomputed by the validator | 109 + 6 |
| Analysis rows, labelled as judgement | 12 |
| Rows left blank because no official source supplies them | 32 |
| Flagged irregularities | 7 |
| Pages built from the dataset, zero hand-typed figures | 13 |

## How the file is built and checked

```
python3 scripts/build.py        # data/evidence.json -> 13 static pages + assets
python3 scripts/validate.py     # provenance, blanks, arithmetic, links, hygiene, privacy, determinism
python3 tools/check_links.py    # every external link https and on an approved official/issuer host
python3 tools/pii_scan.py       # personal-information gate over the published artifact
python3 scripts/stage_pages.py  # build and verify the exact Pages artifact
```

The same five commands run in CI (`.github/workflows/validate.yml`), followed by a check that the committed HTML
matches a fresh build, then a real Jekyll build compared byte for byte against the curated artifact. If a page drifts
from the dataset, or a Jekyll exclusion drops a file, the build fails rather than publishing.

Design rules enforced in code rather than by convention:

* A table row without a registered official source fails the build.
* A row marked unverified cannot render a value — `build.py:value_cell()` returns the placeholder, and the validator
  independently asserts that no unverified row in the dataset carries one.
* Every derived figure is recomputed from its stated components on every build.
* No third-party script, font, iframe or analytics tag; one first-party stylesheet and one first-party script.

## Privacy

Asset A and Owner A are placeholders. No street address, parcel or assessor number, owner name, contact detail, rent,
net operating income, tax basis, debt term or lease document is collected, stored, published or committed here. The
site is static: no analytics, no forms, no cookies, no third-party requests. `tools/pii_scan.py` is the mechanical
enforcement, and it fails the build on any hit.

Anything private that would close an open item belongs in a private file system outside this repository — never in a
commit, a branch or a pull request.

## Repository layout

| Path | Role |
|---|---|
| `data/evidence.json` | The single hand-edited dataset: sources, categories, rows |
| `scripts/`, `tools/` | Build, validation, staging, privacy and link gates |
| Root `*.html`, `assets/` | The published dashboard, generated |
| `research/VERIFICATION-2026-11-10.md` | The line-by-line verification record |
| `COORDINATION.md` | Multi-session task board; read before editing shared files |

Earlier sessions left further layers in the repository — `analysis/`, `advisory/`, `audit/`, `brief/`, `dashboard/`,
`decision-file/`, `docs/`, `pages/`, `_advisory_src/`, `_dashboard_src/`, `build_site.py`. They are retained as an
audit trail and **excluded from the published site**, because they disagree with each other and several rest on
non-official sources or assumed inputs. See `REPO_REVIEW.md` and the review page. Each of their pages carries one
additive link back to the curated dashboard.

## Scope and limits

This is decision support built on public data. It is not an appraisal, not a legal or tax opinion, and not a
personalised investment recommendation. No value, cap rate, sale price, rent projection or renewal probability is
asserted anywhere, because no official source publishes one for this property and inventing one would be worse than
leaving it blank.
