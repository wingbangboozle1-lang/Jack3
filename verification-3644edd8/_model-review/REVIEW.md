# Independent model-semantic review

Reviewed 2026-11-07. Read-only against `model/projection.py`; SHA-256 `e98d9575c6965e5f03fa00100c083731448b0a5d1d01d67c78117a14450f8924`.

> **Passing checks reproduce this audit's observations. They do not validate an appraisal, forecast, or recommendation.**

## M-01 — Inherited arithmetic reproduces

Status: **confirmed**

S1 is 15.28 R in base and 11.62 R in pessimistic; S3 2030 is 1.18 R in pessimistic. Reproduction is not appraisal validation.

## M-02 — R-05 mixes different expiry cases

Status: **issue**

The inherited 12.30 R to 2.51 R comparison pairs S4 base 2035 with S4 pessimistic 2030. Same-case pairs are 10.6433 to 2.5074 R (2030) and 12.3042 to 4.8219 R (2035).

## M-03 — Tenant-risk treatment is asymmetric

Status: **issue**

Only the three S3 results receive p_tenant_survives. The multiplier covers the whole PV, including pre-expiry rent also received by S2/S4/S6 and the terminal value.

## M-04 — The incumbent ranking is sensitive to that treatment

Status: **issue**

Removing only S3's extra tenant-survival multiplier changes S3 2035 ranks from 3/12/12 to 1/4/9 across optimistic/base/pessimistic. This isolates model dependence; it is not a corrected valuation.

## M-05 — The decision criterion changes the winner

Status: **context**

The inherited expected-value leader is S4 - Hold to expiry, re-let to another operator (+9y) at 2035 (17.15 R), while immediate sale leads only the selected pessimistic/maximin comparison.

## M-06 — Immediate sale is not preferred under base assumptions

Status: **issue**

Within the declared today-cap range and all other inputs at base, S5 extend-then-sell exceeds S1 at 5%, 6.25% and 8%. Immediate sale leads the selected pessimistic/maximin comparison, not every decision criterion inside the model.

## M-07 — S3 is not an early-renewal comparator

Status: **issue**

strategy_renew charges re-let downtime and capital at expiry. It may describe expiry/re-letting risk, but it is not a clean signed early extension with uninterrupted rent.

## M-08 — This is not an after-tax wealth model

Status: **limitation**

Immediate sale returns cap-rated proceeds less assumed friction. The code has no owner tax basis, debt payoff, income-tax calculation, replacement-asset return, or reinvestment-risk stream. R multiples cannot be presented as personal wealth outcomes.

## M-09 — Probability inputs are assumptions

Status: **limitation**

Tenant non-renewal, catastrophe probability and loss share, scenario weights, cap rates, downtime, capital costs and alternative-use value are declared assumptions. Regional hazard data do not calibrate parcel damage or closure probabilities.

## Same-horizon S4 comparisons

| Expiry | Base R | Pessimistic R |
|---|---:|---:|
| 2030 (4 years out) | 10.6433 | 2.5074 |
| 2035 (9 years out) | 12.3042 | 4.8219 |

## Counterfactual method

Mechanical sensitivity only; not a corrected model or recommendation.

For S3 only, use raw strategy PV followed by the existing catastrophe adjustment; omit tenant_survival_adjust. Leave every other strategy and every other input unchanged.

| Scenario | Expiry | Published R / rank | Counterfactual R / rank |
|---|---|---:|---:|
| optimistic | 2030 (4 years out) | 21.6027 / 7 | 28.8036 / 5 |
| optimistic | 2032 (mid-window) | 24.7185 / 5 | 32.9581 / 3 |
| optimistic | 2035 (9 years out) | 29.7942 / 3 | 39.7255 / 1 |
| base | 2030 (4 years out) | 6.4521 / 14 | 11.7311 / 12 |
| base | 2032 (mid-window) | 6.7800 / 13 | 12.3274 / 10 |
| base | 2035 (9 years out) | 7.1888 / 12 | 13.0706 / 4 |
| pessimistic | 2030 (4 years out) | 1.1821 / 14 | 3.9405 / 12 |
| pessimistic | 2032 (mid-window) | 1.4335 / 13 | 4.7785 / 11 |
| pessimistic | 2035 (9 years out) | 1.6984 / 12 | 5.6614 / 9 |

## Reproduce

From the repository root:

```sh
python verification-3644edd8/_model-review/review_model.py
```

The script writes `results.json` and this report deterministically. No network or private input is used.
