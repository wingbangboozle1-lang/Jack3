# COORDINATION.md — Shared Task Board

Repo: `wingbangboozle1-lang/Jack3` — Project: "Jack in the Box" NNN-leased property decision research (Central Los Angeles), repo review, and GitHub Pages site.

## Session registry

| Session ID | Branch | Status | Notes |
|---|---|---|---|
| `93f3087c` | `arena/93f3087c-jack3` | active | Only active session at board creation (2026-11-06). Session is fixed to branch `arena/93f3087c-jack3` per Arena session rules; the "final integration" PR merges that branch into `main`. |

## Task board

| Task ID | Task | Status | Owning session | Files touched |
|---|---|---|---|---|
| T1 | Repo review — verify every existing file line by line, flag irregularities, list official source links | claimed (in progress) | `93f3087c` | `README.md`, `COORDINATION.md`, `docs/repo-review.md`, `site/pages/repo-review.html` |
| T2 | Research — Central LA economic fundamentals (population, income, jobs, schools, geography/climate) from official sources | claimed (in progress) | `93f3087c` | `docs/research-economy.md`, `site/pages/market-research.html` |
| T3 | Research — real estate market, NNN net-lease market, cap rates, Jack in the Box corporate/lease facts (SEC) | claimed (in progress) | `93f3087c` | `docs/research-realestate.md`, `site/pages/lease-analysis.html` |
| T4 | Risk analysis & decision framework — sell vs. renew, scenario matrix incl. black swans (wildfire, earthquake, flood, recession) | claimed (in progress) | `93f3087c` | `docs/risk-analysis.md`, `site/pages/risk-analysis.html` |
| T5 | Executive summary — decision, rationale, key numbers, privacy note | claimed (in progress) | `93f3087c` | `docs/executive-summary.md`, `site/pages/executive-summary.html` |
| T6 | Site build — static GitHub Pages site (dashboard landing + category subpages + tables + Flagged for Review page), no PII | claimed (in progress) | `93f3087c` | `index.html`, `site/**`, `assets/**` |
| T7 | Integration — PR to main, merge, verify Pages deploy, record PR link + deploy result here | unclaimed | (final integration session) | `COORDINATION.md`, repo root |

## Rules (from task brief)

- Claim by writing session ID + file scope above, commit and push the claim immediately. Done at board creation.
- Never start a task another session has claimed. If a claim is >60 min old with no commits, another session may take over and must log the handoff here.
- Never mark anything verified without checking against an official source, and link that source.
- Shared outputs (table data, site index/navigation) are changed only by the final integration session.
- Privacy: no personal information anywhere in the published site; placeholders only (e.g. `[OWNER NAME REDACTED]`, `[PROPERTY ADDRESS REDACTED]`).
- Every table row on the site must carry a source link to an official site; unconfirmable values stay blank and are flagged on the "Flagged for Review" page.

## Log

- 2026-11-06 — Board created by session `93f3087c`. Repo contained only `README.md` (`# Jack3`). GitHub Pages already enabled: source = branch `main`, path `/`, legacy build, public at `https://wingbangboozle1-lang.github.io/Jack3/`. No other sessions/branches/PRs found. Session `93f3087c` claims T1–T6; T7 reserved for final integration.
