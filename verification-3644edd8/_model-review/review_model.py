#!/usr/bin/env python3
"""Reproduce and audit the inherited model without modifying it.

The assertions test this review's observations. A passing run means the review
is reproducible; it does NOT validate the model as a property appraisal.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from model import projection as m  # noqa: E402

YEARS = {"2030 (4 years out)": 4, "2032 (mid-window)": 6, "2035 (9 years out)": 9}


def value(result: dict) -> float:
    return result.get("risk_adjusted_pv_R", result["pv_R"])


def identity(result: dict) -> str:
    return f"{result['name']}|{result.get('label', '-')}"


def find(results: list[dict], prefix: str, label: str | None = None) -> dict:
    for result in results:
        if result["name"].startswith(prefix) and (label is None or result.get("label") == label):
            return result
    raise KeyError((prefix, label))


def ranks(results: list[dict], field: str = "risk_adjusted_pv_R") -> dict[str, int]:
    ordered = sorted(results, key=lambda r: -value(r) if field == "risk_adjusted_pv_R" else -r[field])
    return {identity(r): rank for rank, r in enumerate(ordered, 1)}


baseline: dict[str, list[dict]] = {}
by_scenario: dict[str, list[dict]] = {}
for scenario in m.SCENARIOS:
    _, results = m.run(scenario)
    by_scenario[scenario] = results
    rank_map = ranks(results)
    baseline[scenario] = [
        {
            "strategy": r["name"],
            "expiry": r.get("label", "-"),
            "raw_pv_R": round(r["pv_R"], 4),
            "published_adjusted_R": round(value(r), 4),
            "rank": rank_map[identity(r)],
            "tenant_survival_factor": round(r["p_tenant_survives"], 4) if "p_tenant_survives" in r else None,
            "black_swan_probability": round(r["p_black_swan"], 6) if "p_black_swan" in r else None,
        }
        for r in results
    ]

# Reproduce the exact inherited headline outputs before examining semantics.
s1_base = find(by_scenario["base"], "S1")
s1_pess = find(by_scenario["pessimistic"], "S1")
s3_pess_4 = find(by_scenario["pessimistic"], "S3", "2030 (4 years out)")
assert round(value(s1_base), 2) == 15.28
assert round(value(s1_pess), 2) == 11.62
assert round(value(s3_pess_4), 2) == 1.18

same_horizon = []
for label in ("2030 (4 years out)", "2035 (9 years out)"):
    base = find(by_scenario["base"], "S4", label)
    pess = find(by_scenario["pessimistic"], "S4", label)
    same_horizon.append({
        "strategy": base["name"],
        "expiry": label,
        "base_R": round(value(base), 4),
        "pessimistic_R": round(value(pess), 4),
    })
assert same_horizon[0]["base_R"] == 10.6433
assert same_horizon[0]["pessimistic_R"] == 2.5074
assert same_horizon[1]["base_R"] == 12.3042
assert same_horizon[1]["pessimistic_R"] == 4.8219

# Confirm that only S3 receives the tenant survival/renewal multiplier.
survival_recipients = {
    scenario: [r["name"] for r in results if "p_tenant_survives" in r]
    for scenario, results in by_scenario.items()
}
assert all(names and all(name.startswith("S3") for name in names) for names in survival_recipients.values())
assert all(len(names) == 3 for names in survival_recipients.values())

# Mechanical counterfactual: remove only S3's additional tenant-survival factor.
# Keep every other input and the catastrophe adjustment exactly as published.
# This is a sensitivity test, NOT a proposed replacement forecast.
counterfactual_rows = []
counterfactual_all = {}
for scenario, original in by_scenario.items():
    changed = []
    for original_result in original:
        result = dict(original_result)
        if result["name"].startswith("S3"):
            result["counterfactual_R"] = m.apply_black_swan(
                result["pv_R"], YEARS[result["label"]], scenario
            )[0]
        else:
            result["counterfactual_R"] = value(result)
        changed.append(result)
    counterfactual_all[scenario] = changed
    original_ranks = ranks(original)
    changed_ranks = ranks(changed, "counterfactual_R")
    for result in changed:
        if result["name"].startswith("S3"):
            counterfactual_rows.append({
                "scenario": scenario,
                "strategy": result["name"],
                "expiry": result["label"],
                "published_adjusted_R": round(value(result), 4),
                "published_rank": original_ranks[identity(result)],
                "counterfactual_R": round(result["counterfactual_R"], 4),
                "counterfactual_rank": changed_ranks[identity(result)],
                "change": "Only S3 tenant-survival multiplier removed; catastrophe adjustment retained",
            })

s3_9 = [r for r in counterfactual_rows if r["expiry"] == "2035 (9 years out)"]
assert [(r["published_rank"], r["counterfactual_rank"]) for r in s3_9] == [(3, 1), (12, 4), (12, 9)]

# One-way sale-cap sensitivity inside the model's declared 5% / 6.25% / 8% range.
# All other assumptions stay at base. This isolates price uncertainty from the
# inherited correlated optimistic/pessimistic scenario bundles.
original_assumptions = copy.deepcopy(m.ASSUMPTIONS)
cap_sensitivity = []
try:
    for key, cap in (("low", 0.050), ("base", 0.0625), ("high", 0.080)):
        m.ASSUMPTIONS["today_cap_rate"]["base"] = cap
        sell = m.strategy_sell_now(scenario="base")
        extend = m.strategy_sale_leaseback_now(scenario="base")
        cap_sensitivity.append({
            "declared_today_cap_case": key,
            "today_cap_rate_pct": round(cap * 100, 2),
            "sell_now_R": round(sell["pv_R"], 4),
            "extend_then_sell_R": round(extend["pv_R"], 4),
            "higher_mechanical_pv": "S1" if sell["pv_R"] > extend["pv_R"] else "S5",
        })
finally:
    m.ASSUMPTIONS = original_assumptions
assert all(row["higher_mechanical_pv"] == "S5" for row in cap_sensitivity)

expected = m.expected_value()
assert expected[0]["strategy"].startswith("S4")
assert expected[0]["expiry"] == "2035 (9 years out)"
assert round(expected[0]["expected_pv_R"], 2) == 17.15

checks = [
    {
        "id": "M-01",
        "status": "confirmed",
        "title": "Inherited arithmetic reproduces",
        "finding": "S1 is 15.2800 R in base and 11.6250 R in pessimistic; S3 2030 is 1.1821 R in pessimistic. Reproduction is not appraisal validation.",
    },
    {
        "id": "M-02",
        "status": "issue",
        "title": "R-05 mixes different expiry cases",
        "finding": "The inherited 12.30 R to 2.51 R comparison pairs S4 base 2035 with S4 pessimistic 2030. Same-case pairs are 10.6433 to 2.5074 R (2030) and 12.3042 to 4.8219 R (2035).",
    },
    {
        "id": "M-03",
        "status": "issue",
        "title": "Tenant-risk treatment is asymmetric",
        "finding": "Only the three S3 results receive p_tenant_survives. The multiplier covers the whole PV, including pre-expiry rent also received by S2/S4/S6 and the terminal value.",
    },
    {
        "id": "M-04",
        "status": "issue",
        "title": "The incumbent ranking is sensitive to that treatment",
        "finding": "Removing only S3's extra tenant-survival multiplier changes S3 2035 ranks from 3/12/12 to 1/4/9 across optimistic/base/pessimistic. This isolates model dependence; it is not a corrected valuation.",
    },
    {
        "id": "M-05",
        "status": "context",
        "title": "The decision criterion changes the winner",
        "finding": f"The inherited expected-value leader is {expected[0]['strategy']} at 2035 ({expected[0]['expected_pv_R']:.2f} R), while immediate sale leads only the selected pessimistic/maximin comparison.",
    },
    {
        "id": "M-06",
        "status": "issue",
        "title": "Immediate sale is not preferred under base assumptions",
        "finding": "Within the declared today-cap range and all other inputs at base, S5 extend-then-sell exceeds S1 at 5%, 6.25% and 8%. Immediate sale leads the selected pessimistic/maximin comparison, not every decision criterion inside the model.",
    },
    {
        "id": "M-07",
        "status": "issue",
        "title": "S3 is not an early-renewal comparator",
        "finding": "strategy_renew charges re-let downtime and capital at expiry. It may describe expiry/re-letting risk, but it is not a clean signed early extension with uninterrupted rent.",
    },
    {
        "id": "M-08",
        "status": "limitation",
        "title": "This is not an after-tax wealth model",
        "finding": "Immediate sale returns cap-rated proceeds less assumed friction. The code has no owner tax basis, debt payoff, income-tax calculation, replacement-asset return, or reinvestment-risk stream. R multiples cannot be presented as personal wealth outcomes.",
    },
    {
        "id": "M-09",
        "status": "limitation",
        "title": "Probability inputs are assumptions",
        "finding": "Tenant non-renewal, catastrophe probability and loss share, scenario weights, cap rates, downtime, capital costs and alternative-use value are declared assumptions. Regional hazard data do not calibrate parcel damage or closure probabilities.",
    },
]

output = {
    "reviewed": "2026-11-07",
    "model_file": "model/projection.py",
    "model_sha256": hashlib.sha256((ROOT / "model/projection.py").read_bytes()).hexdigest(),
    "interpretation": "PASS means this audit reproduced its observations, not that the inherited model is suitable for a property decision.",
    "checks": checks,
    "same_horizon_comparisons": same_horizon,
    "tenant_survival_recipients": survival_recipients,
    "counterfactual": {
        "warning": "Mechanical sensitivity only; not a corrected model or recommendation.",
        "method": "For S3 only, use raw strategy PV followed by the existing catastrophe adjustment; omit tenant_survival_adjust. Leave every other strategy and every other input unchanged.",
        "rows": counterfactual_rows,
    },
    "cap_sensitivity": cap_sensitivity,
    "expected_value_leaders": expected[:3],
    "baseline": baseline,
}
(HERE / "results.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")

lines = [
    "# Independent model-semantic review",
    "",
    "Reviewed 2026-11-07. Read-only against `model/projection.py`; SHA-256 `" + output["model_sha256"] + "`.",
    "",
    "> **Passing checks reproduce this audit's observations. They do not validate an appraisal, forecast, or recommendation.**",
    "",
]
for check in checks:
    lines.extend([f"## {check['id']} — {check['title']}", "", f"Status: **{check['status']}**", "", check["finding"], ""])
lines.extend([
    "## Same-horizon S4 comparisons",
    "",
    "| Expiry | Base R | Pessimistic R |",
    "|---|---:|---:|",
])
for row in same_horizon:
    lines.append(f"| {row['expiry']} | {row['base_R']:.4f} | {row['pessimistic_R']:.4f} |")
lines.extend([
    "",
    "## Counterfactual method",
    "",
    output["counterfactual"]["warning"],
    "",
    output["counterfactual"]["method"],
    "",
    "| Scenario | Expiry | Published R / rank | Counterfactual R / rank |",
    "|---|---|---:|---:|",
])
for row in counterfactual_rows:
    lines.append(
        f"| {row['scenario']} | {row['expiry']} | {row['published_adjusted_R']:.4f} / {row['published_rank']} "
        f"| {row['counterfactual_R']:.4f} / {row['counterfactual_rank']} |"
    )
lines.extend([
    "",
    "## Reproduce",
    "",
    "From the repository root:",
    "",
    "```sh",
    "python verification-3644edd8/_model-review/review_model.py",
    "```",
    "",
    "The script writes `results.json` and this report deterministically. No network or private input is used.",
    "",
])
(HERE / "REVIEW.md").write_text("\n".join(lines))
print(f"PASS: reproduced {len(checks)} review observations; results in {HERE}")
