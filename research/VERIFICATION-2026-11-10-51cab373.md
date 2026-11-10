# Line-by-line verification record — 2026-11-10 (session `51cab373`)

**Session:** `arena/51cab373-jack3` · **Branch:** `arena/51cab373-jack3` · **Date:** 2026-11-10 (UTC)
**Reconciliation note (post-rebase):** concurrent sessions `c70571c7` (PR #34) and `882bff85` (PR #35, merged
as `5fc524d`) independently closed the same two flagged items on the same day, from the same official pages, with
the same values. `main` already publishes those closures (source ids `lavote` and `dashboard`; Treasury anchor
refreshed to 4.86% on 2026-11-06; review-page V-3/V-4 rows carry "Closed 2026-11-10" notes). On rebase this
session's duplicate edits to `data/evidence.json`, `scripts/build.py` and the generated root pages were dropped in
favour of main's, kept verbatim. This file preserves this session's independent reading as corroboration. Source id
names differ (`recorder`/`casdash` here vs. `lavote`/`dashboard` on main) — same publisher pages, same figures.

**Scope of this pass:** the two open flagged items in the root workspace that an official page could close —
V-3 (LA County documentary transfer tax) and V-4 (LAUSD graduation rate) — plus combined-tree integrity checks.
Every other published row was **not** re-read this pass; the standing line-by-line record remains
`research/VERIFICATION-2026-11-08.md`. No value was copied from another layer without re-reading the official page here.

## V-3 — LA County documentary transfer tax — VERIFIED

**Official source:** Los Angeles County Registrar-Recorder/County Clerk — "Documentary Transfer Tax" general information
(`https://www.lavote.gov/home/recorder/property-document-recording/documentary-transfer-taxes/general-info`),
fetched directly 2026-11-10. (`lavote.gov` is the County's official site; the page is maintained by the Recorder's Office.)

What the page states, verbatim substance:

- "A Documentary Transfer Tax is imposed on all documents that convey real property within the cities of Los Angeles
  County (Per Revenue & Taxation Code Sections 11911-11933)."
- General rate: "**fifty-five cents ($0.55) for each five hundred dollars ($500), or fractional part thereof**", computed on
  the consideration or value of the interest conveyed, **exclusive of the value of any lien or encumbrance remaining
  thereon at the time of sale**, once consideration exceeds $100. "The Recorder's Office collects the tax on behalf of the
  Cities at the time the document is recorded."
- "Special rates apply to the following 5 cities: Culver City, Los Angeles, Pomona, Redondo Beach and Santa Monica";
  "**The County rate for these 5 special Cities is calculated at the full $1.10 per $1000.**"
- Los Angeles row (Effective 7/1/26): "$2.25 for each $500 or fraction thereof; AND EITHER 4 Percent of the total
  transaction value of sales above **$5,400,000** but less than **$10,900,000**; OR 5.5 Percent of the total transaction
  value of sales at or above **$10,900,000**."
- The worked example confirms the computation method (round up to the next $500; divide by $500; multiply by $0.55), and
  that County and City amounts must be listed separately on the declaration.

**Cross-check:** the City of LA 7/1/26 schedule on `lavote.gov` matches the City of LA Office of Finance Measure ULA FAQ
already verified 2026-11-08 (`finance.lacity.gov/faq/measure-ula`: 4% above $5,400,000; 5.5% at or above $10,900,000;
thresholds indexed to Chained CPI). The previously "secondary-sources only" $1.10 per $1,000 figure is confirmed here for
the five special cities (including Los Angeles) only; the general county rate outside those cities is $0.55 per $500.

**Published on main as:** `taxes.html` — "LA County documentary transfer tax" row, status Verified, source `lavote`
("$0.55 per $500 ($1.10 per $1,000)"), and the `review.html` V-3 row carries "Closed 2026-11-10". Independent agreement
recorded here.

## V-4 — LAUSD graduation rate — VERIFIED

**Official source:** California School Dashboard (caschooldashboard.org — operated by the California Department of
Education), Los Angeles Unified — 2025, Academic Engagement report
(`https://www.caschooldashboard.org/reports/19647330000000/2025/academic-engagement`), fetched directly 2026-11-10.

What the page states, verbatim substance:

- "**Los Angeles Unified**" … Academic Engagement … Graduation Rate — All Students: Medium (yellow) performance level,
  "**86.5% graduated** … Maintained -0.2% … Number of Students: **29,899**".
- "Percentage of students who received a high school diploma within four or five years of entering ninth grade":
  2019 **82.1%** · 2022 **86.0%** · 2023 **83.6%** · 2024 **86.7%** · 2025 **86.5%**.
- 5-Year Graduation Rate breakdown (2025): "Four Year = **84.6%**", "Five Year = 1.8%", "Did Not Graduate = 13.5%".
- Performance level detail: one student group (English Learners) at Red, "66.8% graduated … Declined 4.7%", N=5,806.

**Cross-check:** the series is consistent with the values read 2026-11-08 by the dashboard layer session (86.5% for 2025)
and with the closure published on main via PR #35. Statewide context: CDE 2024–25 four-year statewide ACGR 87.5% is recorded
in the dashboard layer; the root site does not assert it and it is not restated here as a root-workspace row.

**Published on main as:** `schools.html` — "District graduation rate" row, status Verified, source `dashboard`
("86.5% (5-year; 4-year 84.6%)"), and the `review.html` V-4 row carries "Closed 2026-11-10". Independent agreement recorded here.

## Combined-tree checks (2026-11-10)

Run on the pre-rebase tree, and re-run after the rebase onto `origin/main`:

| Check | Result |
|---|---|
| `scripts/build.py` + `git diff -- '*.html'` after rebase | committed HTML byte-identical to generator output (re-run on the rebased tree) |
| `scripts/validate.py` | PASS — 141 evidence rows; 12 pages; source links, local links, blank fields, prohibited embeds |
| `scripts/stage_pages.py` | PASS — staged artifact link/source-provenance check (32 entries) |
| `tools/check_site.py` | PASS — brief/ 9 pages, 213 internal references |
| `tools/linkcheck.py` | OK — no broken internal links or anchors |
| `tools/check_links.py` | OK — every verified-source link on an official/primary domain |
| `tools/pii_scan.py` | OK — 0 findings |
| `_advisory_src/verify_advisory.py` / `_dashboard_src/verify.py` | PASS (companion layers untouched by this session) |

`curl` to the Pages host is network-blocked from this sandbox (HTTP 000); live-site verification after merge uses the
`fetch_page` reader, as prior sessions did.

## Irregularities noted this pass

- None new. Two pre-existing items are now closed on main (V-3, V-4). The general county rate ($0.55/$500) vs the five
  special cities' full $1.10 per $1,000 distinction should be read carefully by anyone using the taxes page for a
  City of Los Angeles transaction — the page publishes both, and a City of LA sale pays the city base tax ($2.25/$500)
  plus Measure ULA on top.
- `caschooldashboard.org` is the California Department of Education's official Dashboard but is not a `.gov` domain;
  it is registered on main as Government (CDE-operated) and must not be treated as a third-party mirror.

## Not re-verified this pass

Everything not listed above, including all BLS/Census/issuer rows (last read 2026-11-08 by their verifiers; main's
2026-11-10 record `VERIFICATION-2026-11-10-882bff85.md` re-read them and found all match), hazard rows, and all companion
layers, which remain in the repository but **excluded from the Pages artifact** and are not claimed re-verified.
