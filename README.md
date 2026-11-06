# SP-01 — Jack in the Box NNN decision file

**Live site:** https://wingbangboozle1-lang.github.io/Jack3/

A documented decision file for **SP-01**, a single-tenant Jack in the Box quick-service restaurant
on a triple-net lease in central Los Angeles, with a lease expiry inside the **2030–2035** window.

The question: **sell before expiry, or renew?**

---

## Recommendation

> **Renew if the tenant will commit. Never sell for cash. Route any exit through a §1031 exchange.**

Ranked on risk-adjusted after-tax wealth across 6,000 simulated macro paths, the order is stable:

1. Renew, then exchange out on a planned horizon (best risk-adjusted)
2. §1031 exchange now
3. Renew and hold long (best median, worst tail)
4. Sell before expiry
5. **Sell for cash — dominated in every scenario tested**

The cash sale loses because of tax, not the market. On a $6.5M asset with a 40% basis it nets
about $4.83M; the same-day §1031 exchange of the identical asset nets about $5.94M.

## What is in this repository

| Path | What it is |
|---|---|
| `index.html` … `flagged.html` | The published site (GitHub Pages serves the repo root) |
| `data/sources.json` | 30 source records: publisher, URL, as-of date, tier, and what each verifies |
| `data/datasets.json` | 179 table rows across 9 sections, each with a source id and a status |
| `data/model_assumptions.json` | 20 labelled assumptions, each with a range and a stated basis |
| `data/model_output.json` | Generated model results (do not hand-edit) |
| `data/flags.json` | 13 flagged items: unverified data, irregularities, conflicts |
| `tools/model.py` | Seeded Monte Carlo engine, Python standard library only |
| `tools/build_site.py` | Static site generator |
| `tools/verify.py` | Verification harness (structure, citation, prose traceability) |
| `research/NOTES.md` | Line-by-line verification log and worked findings |

## Reproducing everything

```bash
python3 tools/model.py       # regenerate data/model_output.json  (~8 s)
python3 tools/build_site.py  # regenerate the site + link audit
python3 tools/verify.py      # run all three verification layers
```

The model is seeded (`20261106`), so every number on the Projection page is exactly reproducible.
No third-party dependencies.

## Verification standard

Three tiers, enforced by `tools/verify.py`:

- **verified** — read on the publishing agency's own domain. Rendered green.
- **verified (secondary)** — an official statement read through a reproduction. Rendered amber,
  with the caveat recorded on the source record.
- **unverified** — could not be confirmed from an official source. **Value left blank**, rendered
  red, published on the Flagged for Review page with the URL to check by hand. Never estimated.

`tools/verify.py` also proves that every number quoted in the narrative prose appears in one of
the data files — the check that catches a fabricated figure before it reaches the page.

## Privacy

This repository contains **no** street address, parcel number (AIN), owner name, tenant-unit
identity, rent figure, lease date, contact detail or personal financial data. The asset is referred
to as `SP-01` throughout and all analysis is at county, city or metro granularity. The owner's tax
basis and bracket are exposed as *scenario parameters* rather than collected. See `method.html` on
the live site for the full protocol.

## Caveats

This is an analytical file prepared from public sources. It is **not** an appraisal, a legal
opinion or a tax opinion. Values labelled *assumption* are modelling choices, not observations.
See the Flagged for Review page for everything that could not be verified.

## Working on this repository in parallel

Read [`COORDINATION.md`](COORDINATION.md) first. It is the shared task board and records which
session owns which files.
