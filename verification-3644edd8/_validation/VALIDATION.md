# Standalone audit validation

Review date: **2026-11-07 UTC**. All checks below ran locally against the generated page and reviewed model.

## PASS — Deterministic build

Model review and public page produced identical SHA-256 hashes on two consecutive runs.

## PASS — Reviewed model identity

model/projection.py SHA-256 e98d9575c6965e5f03fa00100c083731448b0a5d1d01d67c78117a14450f8924

## PASS — Evidence schema and statuses

45 unique rows; verified/projection/conflict rows nonblank; unconfirmed school row and all 12 private/property flags blank.

## PASS — Official-source allowlist

23 unique HTTPS government or issuer-primary sources; no commercial market-data host in the evidence register.

## PASS — HTML structure and links

One H1/main/title, unique IDs, all internal anchors resolve, all 68 table body rows carry an official source link, external links use safe HTTPS.

## PASS — Self-contained public page

No script, form, image, iframe, stylesheet link, external asset, tracker or manual-input feature.

## PASS — Privacy scan

No email, telephone, street-address or coordinate pattern in visible public text; property remains Asset A.

## PASS — Unconfirmed-input rendering

All 12 unconfirmed fields are named; their JSON values remain empty and render as em dashes.

## PASS — Public-file layout; Jekyll deferred

Exactly index.html is outside ignored underscore/dot directories. Jekyll is unavailable in this sandbox, so executable artifact validation is explicitly deferred to CI.

## PASS — Root integration boundary recorded

Root scripts/stage_pages.py does not yet stage this audit. Owner-side conditional staging remains required; this isolated session does not edit that shared script.

## Scope limit

These are structural, provenance, deterministic-build and privacy checks. They are not a live network monitor, appraisal, legal/tax opinion or proof that every inherited repository row is correct. Manual official-source readings are recorded in `_research/source-notes.md`.

## Reproduce

```sh
python verification-3644edd8/_model-review/review_model.py
python verification-3644edd8/_tools/build_audit.py
python verification-3644edd8/_tools/validate_audit.py
```

When Jekyll is available, isolated output is written under `_validation/jekyll-out`, which Jekyll itself ignores on subsequent builds. In this sandbox the executable was unavailable and the structural fallback is labelled above; CI must perform the real build.
