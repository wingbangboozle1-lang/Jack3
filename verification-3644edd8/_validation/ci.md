# CI integration record

## 2026-11-07 — PR #26, run 42413180245

Run: https://github.com/wingbangboozle1-lang/Jack3/actions/runs/42413180245
Job: `validate` / job `128525481381`
Reviewed head: `17975a6041a0a30c98ba97212726988dd180873c`

Result: **expected integration failure; not merged.**

GitHub's failed-step record identifies only step 16, `python scripts/stage_pages.py _jekyll_test`. The check-run annotation says:

> unexpected Jekyll files: ['verification-3644edd8/index.html']; missing: []

Interpretation: the actual GitHub Actions Jekyll build emitted the intended one public audit page, and every workflow step before the curated-artifact comparison passed. The shared allowlist did not yet include that page. This confirms the anticipated owner-side staging dependency; it is not a semantic, source-link, privacy or deterministic-build failure.

Coordination:
- Conditional one-file staging and canonical-link request posted on open PR #22.
- Same staging follow-up requested from the most recent merged staging owner on PR #25.
- PR #26 must remain unmerged until the allowlist includes the file and the full real Jekyll/artifact comparison passes.

No shared script or workflow was edited by this session.
