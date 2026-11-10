"""Deterministic 2026-2035 projection for Asset A.

No randomness, no network, no fitted parameters. Every constant is either read
from a verified source (SOURCE) or declared as an assumption and labelled
(ASSUMPTION).

Unit of account
---------------
R = one year of current contractual base rent. The rent itself was not
supplied and is not invented, so every strategy is valued in units of R. The
ranking therefore depends on term, tenant behaviour, cost and tax -- not on an
unknown rent level.

Consistency rules the model obeys
---------------------------------
1. Every strategy is marked to the same horizon (2036) at the same exit cap.
2. Strategies that sell early pay selling cost and the city transfer tax; the
   hold strategies are marked to market at the horizon *pre-tax* so the
   comparison is not silently biased by a zero-basis assumption.
3. The renewal probability swept in each scenario is actually used: strategy C
   blends the renewed cash-flow with the fallback re-let outcome.
4. Taxes on a realised sale are shown separately as a sensitivity, because the
   owner's basis was not supplied.
"""
from __future__ import annotations
import json
from pathlib import Path

SNAPSHOT = "2026-11-10"

# ---- verified input --------------------------------------------------------
TREASURY_10Y = 0.0486        # SOURCE fred_dgs10, observation 2026-11-06
PREMIUM_BASE = 0.0114        # ASSUMPTION: net-lease risk premium
DISCOUNT_BASE = round(TREASURY_10Y + PREMIUM_BASE, 4)   # 6.00% derived

# ---- declarable assumptions, swept -----------------------------------------
SCENARIOS = {
    "optimistic": dict(discount=0.0450, renewal_prob=0.85, relet_fraction=0.70,
                       downtime_years=1, exit_cap=0.055, rent_growth=0.030),
    "base":       dict(discount=0.0600, renewal_prob=0.60, relet_fraction=0.60,
                       downtime_years=2, exit_cap=0.065, rent_growth=0.020),
    "pessimistic": dict(discount=0.0750, renewal_prob=0.35, relet_fraction=0.50,
                        downtime_years=2, exit_cap=0.075, rent_growth=0.010),
}

SELLING_COST = 0.020         # ASSUMPTION: brokerage + closing
TRANSFER_TAX = 0.0445        # SOURCE ula: 0.45% city base + 4.00% ULA tier
CAPITAL_GAINS_DRAG = 0.323   # ASSUMPTION: 20% federal + 3.8% NIIT + 8.5% CA
TERM_PREMIUM = 0.10          # ASSUMPTION: +10% price for a 10-year-plus lease
RENEWAL_RESET = 0.90         # ASSUMPTION: renewal sets rent 10% below current
MARKET_RELET = 0.85          # ASSUMPTION: a re-tenant pays 15% below current
EXIT_YEAR = 2032             # ASSUMPTION: mid-point of the 2030-2035 window
VACANCY_COST = 0.5           # ASSUMPTION: taxes/insurance/security per downtime year
START_YEAR = 2026
HORIZON = 10                 # 2026 -> 2036

PATHWAYS = {
    "A": "A · Sell now",
    "B": "B · Hold to expiry, then re-let",
    "C": "C · Seek renewal at expiry",
    "D": "D · Extend first, then sell",
    "E": "E · Re-tenant at expiry",
}


def pv(cashflows, discount):
    return sum(cf / (1 + discount) ** (i + 1) for i, cf in enumerate(cashflows))


def rent(year, growth):
    return (1 + growth) ** (year - START_YEAR)


def build(scn):
    years = list(range(START_YEAR, START_YEAR + HORIZON))
    g = scn["rent_growth"]
    cap = scn["exit_cap"]
    dt = scn["downtime_years"]

    # A -- sell now: one year of rent plus net proceeds, then nothing.
    proceeds = (1.0 / cap) * (1 - SELLING_COST - TRANSFER_TAX)
    a = [1.0 + proceeds] + [0.0] * (HORIZON - 1)

    # B -- hold to expiry, then re-let at a discount after downtime.
    b = []
    for y in years:
        if y < EXIT_YEAR:
            b.append(rent(y, g))
        elif y == EXIT_YEAR:
            b.append(rent(y, g) - VACANCY_COST * dt)
        else:
            b.append(rent(y, g) * scn["relet_fraction"])
    b[-1] += b[-1] / cap          # mark to market at the horizon, pre-tax

    # C -- seek renewal at expiry; blend the renewed and fallback outcomes.
    renewed, fallback = [], []
    for y in years:
        if y < EXIT_YEAR:
            renewed.append(rent(y, g)); fallback.append(rent(y, g))
        elif y == EXIT_YEAR:
            renewed.append(rent(EXIT_YEAR, g) * RENEWAL_RESET)
            fallback.append(rent(y, g) - VACANCY_COST * dt)
        else:
            renewed.append(rent(EXIT_YEAR, g) * RENEWAL_RESET * (1 + g) ** (y - EXIT_YEAR))
            fallback.append(rent(y, g) * scn["relet_fraction"])
    renewed[-1] += renewed[-1] / cap
    fallback[-1] += fallback[-1] / cap
    p = scn["renewal_prob"]
    c = [p * r + (1 - p) * f for r, f in zip(renewed, fallback)]

    # D -- extend first (tenant commits), then sell the lengthened lease in 2028.
    price_d = (1.0 / cap) * (1 + TERM_PREMIUM)
    proceeds_d = price_d * (1 - SELLING_COST - TRANSFER_TAX)
    d = [1.0, rent(2027, g) + proceeds_d] + [0.0] * (HORIZON - 2)

    # E -- re-tenant at expiry, capturing market rent after downtime.
    e = []
    for y in years:
        if y < EXIT_YEAR:
            e.append(rent(y, g))
        elif y == EXIT_YEAR:
            e.append(-VACANCY_COST * dt)
        else:
            e.append(rent(y, g) * MARKET_RELET)
    e[-1] += e[-1] / cap

    return {"A": a, "B": b, "C": c, "D": d, "E": e}


def after_tax_sale(value, basis_fraction):
    """Illustrative after-tax proceeds if an R-valued asset is sold.

    `basis_fraction` is basis as a share of price; the owner's real basis was
    not supplied, so this is a sensitivity, not a finding.
    """
    gain = value * (1 - basis_fraction)
    return value * (1 - SELLING_COST - TRANSFER_TAX) - gain * CAPITAL_GAINS_DRAG


def run():
    out = {
        "snapshot": SNAPSHOT,
        "unit": "R = one year of current contractual base rent",
        "verified_inputs": {
            "treasury_10y": TREASURY_10Y,
            "treasury_date": "2026-11-06",
            "treasury_source": "FRED DGS10 (Federal Reserve H.15)",
            "discount_base": DISCOUNT_BASE,
        },
        "assumptions": {
            "premium_base": PREMIUM_BASE,
            "selling_cost": SELLING_COST,
            "transfer_tax": TRANSFER_TAX,
            "transfer_tax_source": "City of Los Angeles Measure ULA FAQ: 0.45% base + 4.00% tier",
            "capital_gains_drag": CAPITAL_GAINS_DRAG,
            "term_premium": TERM_PREMIUM,
            "renewal_reset": RENEWAL_RESET,
            "market_relet": MARKET_RELET,
            "exit_year": EXIT_YEAR,
            "expiry_window": "2030-2035 (owner-reported)",
            "horizon": "2026-2036",
        },
        "scenarios": {},
    }
    for name, scn in SCENARIOS.items():
        streams = build(scn)
        vals = {k: pv(v, scn["discount"]) for k, v in streams.items()}
        order = sorted(vals, key=lambda k: -vals[k])
        out["scenarios"][name] = {
            "discount": scn["discount"],
            "renewal_prob": scn["renewal_prob"],
            "relet_fraction": scn["relet_fraction"],
            "downtime_years": scn["downtime_years"],
            "exit_cap": scn["exit_cap"],
            "rent_growth": scn["rent_growth"],
            "pv": {k: round(v, 2) for k, v in vals.items()},
            "rank": {k: i for i, k in enumerate(order, start=1)},
        }

    keys = list(PATHWAYS)
    out["summary"] = {}
    for k in keys:
        vals = [out["scenarios"][s]["pv"][k] for s in SCENARIOS]
        ranks = [out["scenarios"][s]["rank"][k] for s in SCENARIOS]
        out["summary"][k] = {
            "name": PATHWAYS[k],
            "floor": round(min(vals), 2),
            "expected": round(sum(vals) / len(vals), 2),
            "ceiling": round(max(vals), 2),
            "mean_rank": round(sum(ranks) / len(ranks), 2),
        }
    floor_order = sorted(keys, key=lambda k: -out["summary"][k]["floor"])
    for i, k in enumerate(floor_order, start=1):
        out["summary"][k]["floor_rank"] = i
    out["floor_winner"] = PATHWAYS[floor_order[0]]
    out["expected_winner"] = max(out["summary"].values(), key=lambda x: x["expected"])["name"]

    # Tax sensitivity: what a realised sale is worth after tax at three bases.
    sale_value_now = 1.0 / SCENARIOS["base"]["exit_cap"]
    out["tax_sensitivity"] = {
        "asset_value_in_R_at_base_cap": round(sale_value_now, 2),
        "cases": {
            f"basis_{int(b*100)}pct": round(after_tax_sale(sale_value_now, b), 2)
            for b in (0.0, 0.5, 1.0)
        },
        "note": ("Illustrative only. The owner's basis was not supplied, so no "
                 "after-tax figure about the subject property is asserted."),
    }
    # §1031: the same sale with the gain deferred rather than taxed.
    out["section_1031"] = {
        "value_in_R": round(sale_value_now * (1 - SELLING_COST - TRANSFER_TAX), 2),
        "note": ("Deferral applies to the federal and state gain, not to the "
                 "transfer taxes or selling costs, which are still paid."),
    }
    return out


if __name__ == "__main__":
    result = run()
    dest = Path(__file__).resolve().parent.parent / "data" / "projection.json"
    dest.write_text(json.dumps(result, indent=2) + "\n")
    for k, v in result["summary"].items():
        print(f'{v["name"]:<34} floor {v["floor"]:>6}  expected {v["expected"]:>6}  '
              f'ceiling {v["ceiling"]:>6}  mean rank {v["mean_rank"]}')
    print("\nfloor winner:", result["floor_winner"])
    print("expected winner:", result["expected_winner"])
    print("tax sensitivity:", result["tax_sensitivity"]["cases"])
