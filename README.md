# Jack3 — Central LA NNN Jack in the Box: Decision Desk

**Live site:** https://wingbangboozle1-lang.github.io/Jack3/ (GitHub Pages · source: `main` / `docs`)

An anonymized, official-source analytical dashboard for one question: **sell a single-tenant NNN-leased
Jack in the Box restaurant in Central Los Angeles before its lease expires (2030–2035), or renew.**

Contents: executive summary · weighted sell-vs-renew decision matrix · interactive present-value
"Projection Studio" · area demographics, economy, income, schools, population projections · tenant
(Jack in the Box Inc.) fundamentals from SEC filings · hazard/black-swan analysis (Puente Hills
earthquake, Jan 2025 wildfires) · 14-item scored risk register · 19-item flagged-for-review list.

Every table row carries a source link to an official (.gov / SEC / State of California) source or is
explicitly labeled **industry** (brokerage/commissioned studies, never presented as official) or
**flagged unverified** (value withheld, remediation listed) — nothing is invented. No owner identity,
street address, parcel, listing, or personal financial data appears anywhere in the site.

## Repository layout (post-integration, 2026-11-06)

| Path | What it is |
|---|---|
| `docs/` | **Canonical published site** (this dashboard, 18 pages). Built by `tools/build_site.py` from `data/site_data.json` + `tools/content_part*.py`. GitHub Pages serves `main:/docs`. |
| `docs/property-study/` | Companion official-source study (preserved verbatim): decision framing, economy, schools, risks, flagged review, sources. Build: `scripts/build.py` + `scripts/validate.py` (root-level, for that study). |
| `docs/legacy-dashboard/` | Original consolidated evidence dashboard (preserved verbatim) — place / economy / model / risk / review / tenant / decisions / sources; backed by `data/evidence.json` and `assets/`. |
| Root `*.html`, `assets/`, `data/evidence.json`, `scripts/`, `.github/workflows/validate.yml` | Files owned by the companion study (session ff406d61). Leave them byte-identical — the workflow deterministically rebuilds and diffs them on every push. |
| `research/` | Working notes and per-topic research files from both sessions. |
| `COORDINATION.md` | Parallel-session coordination board: task ledgers, PR log (#1, #2, #4), integration record. |

## Evidence boundary

Official observations were manually checked on 2026-11-06. Property identity, lease, rent, debt and owner
financial circumstances are absent. Regional context is not a parcel forecast. Missing numerical values
stay blank; conditional analyst rules are not official recommendations. See the
**Flagged for Review** page for nonblocking review flags and **Methodology** for the verification protocol.

No personal information, addresses, parcel identifiers, owner research, analytics, forms or third-party
executable assets are included. Do not commit private records, even in history.

## Build and check

```
# canonical site (docs/)
python3 tools/build_site.py

# companion study (root-level, deterministic)
python3 scripts/build.py
python3 scripts/validate.py

# local preview
python3 -m http.server 8000 --bind 0.0.0.0 --directory docs
```

`data/site_data.json` (canonical) and `data/evidence.json` (companion study) are the public sources of
truth. Rebuild HTML after edits. Validation checks provenance and internal links, not live external
availability or semantic truth. Source checks are manual — the sites are dated snapshots (2026-11-06),
not automatic data feeds.

**GitHub Pages serves `main:/docs`.** The companion study's workflow determinism check applies to the
repository **root** only and does not touch `docs/`.

Not legal, tax, appraisal, or investment advice.
