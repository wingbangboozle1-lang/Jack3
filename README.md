# Jack / Property intelligence

Privacy-safe, static research dashboard for an unidentified Los Angeles-area net lease asset.

**Live site:** https://wingbangboozle1-lang.github.io/Jack3/

## Evidence boundary
Official observations were manually checked on 2026-11-06. Property identity, lease, rent, debt and owner financial circumstances are absent. Regional context is not a parcel forecast. Missing numerical values stay blank; conditional analyst rules are not official recommendations. See `review.html` for nonblocking review flags and `sources.html` for methodology.

No personal information, addresses, parcel identifiers, owner research, analytics, forms or third-party executable assets are included. Do not commit private records, even in history.

## Build and check
```
python scripts/build.py
python scripts/validate.py
python -m http.server 8000 --bind 0.0.0.0
```

`data/evidence.json` is the public source of truth. Rebuild HTML after edits. Validation checks internal links and row provenance, not live external availability or semantic truth. Source checks are manual and the site is a dated snapshot, not an automatic data feed. GitHub Pages serves the repository root on main; PR validation checks deterministic output before integration.
