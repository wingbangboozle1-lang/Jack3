# Jack3 — Central Los Angeles NNN Property Decision File

A complete analysis and published website for a **single-tenant Jack in the Box
NNN (triple-net) lease property in Central Los Angeles**, with the primary lease
term **expiring between 2030 and 2035**.

The question answered: **sell before the lease expires, or renew?**

> **Live site:** <https://wingbangboozle1-lang.github.io/Jack3/>
> Served by GitHub Pages from `/docs`. Plain static HTML — no build step, no
> runtime API calls, no CDN, no framework.

---

## The recommendation

**Sell — and if the tenant will commit to an early extension first, buy the term
and then sell the lengthened lease. Do not plan around renewing at expiry.**

Selling now carries the **highest worst-case present value of every strategy
modelled** (11.62 R in the pessimistic scenario, against 9.88 R for the
next-best and 1.18 R for renewing the Jack in the Box lease to a 2030 expiry).
Renewing ranks **last in both the base and the pessimistic scenario**, because it
is the only strategy whose entire value depends on a counterparty that is
publicly contracting — and that has tied its closure decisions to exactly the
dates in question.

`R` = one year of the property's current contractual base rent. See
[Why the model is normalised to R](#why-the-model-is-normalised-to-r).

---

## What is in this repository

| Path | Contents |
|---|---|
| `docs/` | **The published site.** 23 pages + 23 CSV exports of the data snapshot. |
| `data/` | The verified data snapshot. Six modules; every row carries value, unit, geography, as-of date, source organisation, source URL and a verification status. |
| `model/projection.py` | The projection and decision model. Deterministic, no network, no randomness. |
| `build_site.py` | Static site generator: `data/` + `model/` → `docs/`. |
| `site/` | Stylesheet and client-side behaviour. |
| `tools/check_links.py` | Validates every emitted URL; fails on a non-official domain in a verified column. |
| `tools/pii_scan.py` | Fails the build if any personal or property-identifying value appears. |
| `research/` | Working research notes behind the data modules. |
| `EXECUTIVE_SUMMARY.md` | The decision, the evidence, the conditions, the risks. |
| `VERIFY.md` | Verification protocol, results and the reproduction commands. |
| `REPO_REVIEW.md` | Line-by-line audit of the repository as found, and its irregularities. |
| `COORDINATION.md` | Shared task board, session registry, ownership map and change log. |

### The site

Landing dashboard, then six categories:

- **Overview** — dashboard, executive summary, methodology, privacy
- **The Asset** — property profile and input register, geography, NNN lease economics
- **The Tenant** — tenant credit from SEC filings, the closure programme
- **The Market** — population and income, employment and wages, official forecasts, infrastructure and schools
- **The Decision** — projection model, valuation and sensitivity, decision framework, tax framework
- **Risk** — risk register, physical hazards, black swan register
- **Assurance** — source register, **flagged for review**, repository review

Every table row carries a link to the official source it came from. Rows that
could not be confirmed from an official source are **published blank** and
appear on the [Flagged for Review](https://wingbangboozle1-lang.github.io/Jack3/flagged-for-review.html) page.

---

## Verification stance

Every figure is classified:

| Label | Meaning |
|---|---|
| `VERIFIED` | Read directly on an official `.gov` page, or in a filing the issuer made with the SEC, during this session. URL given. |
| `MODELLED` | Arithmetic output of `model/projection.py` from declared assumptions. Reproducible, not an observation. |
| `JUDGEMENT` | Qualitative assessment. Reasoning traceable to cited facts; the rating itself is opinion. |
| `UNVERIFIED` | Appeared only in a secondary source, or the official page could not be retrieved. **Published blank.** |
| `NO OFFICIAL SOURCE` | No government body publishes it. **Never asserted.** |
| `INPUT REQUIRED` | Property-specific or personal. Withheld by design. |

Commercial brokerage listings, net-lease aggregators, analyst opinions,
rating-agency reports and media restatements of government data were **consulted
and then rejected**. No value from any of them is asserted anywhere.

**1,013 links** are emitted into the site across **30 distinct hosts, all
official or primary**. `tools/check_links.py` and `tools/pii_scan.py` both pass.

---

## Privacy

No owner name, entity name, street address, Assessor Parcel Number, telephone
number, email address, transaction price, rent figure or purchase basis appears
in the published site, the data snapshot, or the repository deliverables. Fields
that would need one are left blank and labelled `INPUT REQUIRED`, or replaced
with the placeholders `PROPERTY-01` and `OWNER-01`.

This is enforced mechanically by `tools/pii_scan.py`, which fails the build.
Every page also carries `<meta name="robots" content="noindex,nofollow">`.

See [`docs/privacy.html`](docs/privacy.html) for the full disposition of what was
found during research and how each item was handled.

---

## Why the model is normalised to R

The owner's actual lease economics were never supplied, and under the privacy
directive no property-specific figure is invented. Rather than fabricate a rent,
a basis or a building size, the model is written in units of

> **R = one year of the property's current contractual base rent**

This is not a workaround — it is the right form for this decision. Sell-versus-hold
compares two cash-flow streams from the *same* asset, so the rent level largely
cancels out of the ranking. The owner reads "strategy X returns 15.28 R versus
strategy Y at 6.78 R" and multiplies by their own actual rent in private. No
private figure has to be published for the analysis to work.

---

## Reproduce

```bash
python3 -m model.projection      # every strategy, every scenario, ranked
python3 build_site.py            # regenerate docs/ from data/ and model/
python3 tools/check_links.py     # validate all 1,013 emitted links
python3 tools/pii_scan.py        # enforce the privacy guarantee
```

The model is deterministic: same inputs, same outputs, no randomness, no network
calls. Every assumption is declared in `model/projection.py` with a low, base and
high value **and a favourability direction**, so the optimistic scenario takes
the favourable extreme of *every* assumption and the pessimistic scenario takes
the unfavourable extreme of every one.

---

## The four things this analysis refuses to invent

1. **The property itself** — no address, APN, lot size, building size, rent,
   escalation schedule, basis or guaranty status was supplied (`F-01`).
2. **Commercial cap rates and comparable sales** — no United States government
   agency publishes these (`F-02`). Valuation is a sensitivity range, never a
   point estimate.
3. **Los Angeles County population projections for 2030, 2035 and 2040** —
   published only as spreadsheets on a domain this environment cannot reach, and
   third-party restatements disagree by more than 100,000 residents (`F-04`).
4. **Tax rates on a sale** — the relevant IRS and California Franchise Tax Board
   pages returned HTTP 404 when retrieved, so the mechanisms are described and
   linked but **no rate is asserted** (`F-05`).

Each is documented on the Flagged for Review page with the official route to
resolve it. None blocks the decision.

---

*Data snapshot 2026-11-06. Built and verified by session
`arena-d989a5c6-jack3`.*
