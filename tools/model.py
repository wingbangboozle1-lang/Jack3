#!/usr/bin/env python3
"""Deterministic scenario model for [PROPERTY-A].

Every number produced here is arithmetic on *disclosed assumptions*. No input is a
verified fact about the property: rent, NOI, basis and tenant credit are private and
are listed as open items on the Flagged for Review page.

Run:  python3 tools/model.py   ->  writes assets/data/scenarios.json
"""
import json
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "analysis", "data", "scenarios.json")

# ----------------------------------------------------------------------------
# Disclosed assumptions (NOT facts about the property)
# ----------------------------------------------------------------------------
A = {
    "noi_levels": [120000, 180000, 240000, 400000, 700000],
    "cap_entry": 0.0650,          # central-LA QSR NNN, short-ish term; between franchisee QSR 6.87% and retail 6.69%
    "rent_growth": 0.025,         # typical 2-3% annual bumps or 10% every 5 years, amortised
    "hold_years": 7,              # 2026 -> 2033, inside the 2030-2035 expiry band
    "cap_exit": 0.0675,           # mild widening: shorter remaining term at exit
    "sale_cost": 0.045,           # 3.0% brokerage + 0.56% transfer + ~0.94% legal/closing (ULA excluded below $5.4M)
    "reserve": 0.02,              # landlord structural reserve even under NNN
    "reinvest_cap": 0.0687,       # Boulder Q3 2026 franchisee QSR average
    "reinvest_growth": 0.020,
    "reinvest_exit_cap": 0.0700,
    "ula_low_threshold": 5400000,
    "ula_high_threshold": 10900000,
    "ula_low_rate": 0.04,
    "ula_high_rate": 0.055,
    "transfer_tax_rate": 0.0056,  # 1.10 + 4.50 per 1,000
}


def irr(cfs, lo=-0.95, hi=1.5, tol=1e-9):
    """Bisection IRR on an annual cash-flow vector starting with a negative flow."""
    def npv(r):
        return sum(cf / (1 + r) ** i for i, cf in enumerate(cfs))
    for _ in range(300):
        mid = (lo + hi) / 2
        v = npv(mid)
        if abs(v) < tol:
            return mid
        if (npv(lo) > 0) == (v > 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def sale_costs(price):
    """Broker + transfer tax + ULA (if inside the City of LA and above threshold)."""
    base = A["sale_cost"]
    if price > A["ula_high_threshold"]:
        base += A["ula_high_rate"]
    elif price > A["ula_low_threshold"]:
        base += A["ula_low_rate"]
    return base


def hold_irr(noi0, g=None, exit_cap=None, n=None, entry_cap=None):
    g = A["rent_growth"] if g is None else g
    exit_cap = A["cap_exit"] if exit_cap is None else exit_cap
    n = A["hold_years"] if n is None else n
    entry_cap = A["cap_entry"] if entry_cap is None else entry_cap
    v0 = noi0 / entry_cap
    noi_n = noi0 * (1 + g) ** n
    price_n = noi_n / exit_cap
    net_exit = price_n * (1 - sale_costs(price_n))
    cfs = [-v0]
    for t in range(1, n + 1):
        cfs.append(noi0 * (1 + g) ** t * (1 - A["reserve"]))
    cfs[-1] += net_exit
    return {
        "value_today": v0,
        "exit_value": price_n,
        "net_exit": net_exit,
        "terminal_gross": net_exit + sum(cfs[1:-1]) + cfs[-1] - net_exit,
        "irr": irr(cfs),
        "multiple": sum(cfs[1:]) / v0,
        "cash_flows": cfs,
    }


def sell_and_reinvest(noi0, n=None):
    n = A["hold_years"] if n is None else n
    v0 = noi0 / A["cap_entry"]
    proceeds = v0 * (1 - sale_costs(v0))
    noi_r = proceeds * A["reinvest_cap"]
    price_n = noi_r * (1 + A["reinvest_growth"]) ** n / A["reinvest_exit_cap"]
    net_exit = price_n * (1 - sale_costs(price_n))
    cfs = [-v0]
    for t in range(1, n + 1):
        cfs.append(noi_r * (1 + A["reinvest_growth"]) ** t * (1 - A["reserve"]))
    cfs[-1] += net_exit
    return {
        "proceeds_after_costs": proceeds,
        "value_today": v0,
        "exit_value": price_n,
        "net_exit": net_exit,
        "irr": irr(cfs),
        "multiple": sum(cfs[1:]) / v0,
        "cash_flows": cfs,
        "terminal_wealth": sum(cfs[1:]),
    }


def breakeven_exit_cap(noi0, target_irr):
    """Exit cap at which holding equals the reinvest alternative's IRR."""
    lo, hi = 0.03, 0.20
    for _ in range(120):
        mid = (lo + hi) / 2
        if hold_irr(noi0, exit_cap=mid)["irr"] > target_irr:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    out = {"assumptions": A, "generated": "2026-11-06"}

    # 1. Value per unit of NOI
    caps = [round(0.055 + i * 0.0025, 4) for i in range(13)]  # 5.50% .. 8.50%
    out["value_matrix"] = {
        "caps": caps,
        "noi_levels": A["noi_levels"],
        "values": [[round(n / c) for c in caps] for n in A["noi_levels"]],
        "per_100k": [round(100000 / c) for c in caps],
    }

    # 2. Hold vs sell-and-1031, per NOI level
    comp = []
    for noi in A["noi_levels"]:
        h = hold_irr(noi)
        s = sell_and_reinvest(noi)
        comp.append({
            "noi": noi,
            "value_today": round(h["value_today"]),
            "hold": {
                "irr": h["irr"],
                "multiple": h["multiple"],
                "exit_value": round(h["exit_value"]),
                "net_exit": round(h["net_exit"]),
                "terminal_wealth": round(sum(h["cash_flows"][1:])),
            },
            "sell": {
                "proceeds_after_costs": round(s["proceeds_after_costs"]),
                "irr": s["irr"],
                "multiple": s["multiple"],
                "exit_value": round(s["exit_value"]),
                "net_exit": round(s["net_exit"]),
                "terminal_wealth": round(s["terminal_wealth"]),
            },
            "breakeven_exit_cap": breakeven_exit_cap(noi, s["irr"]),
            "irr_gap_pp": (h["irr"] - s["irr"]) * 100,
        })
    out["comparison"] = comp

    # 3. Sensitivity: exit cap x rent growth -> hold IRR (mid NOI)
    mid = A["noi_levels"][1]  # $180k used for the sensitivity grid
    exit_caps = [0.055, 0.060, 0.065, 0.0675, 0.070, 0.075, 0.080]
    growths = [0.010, 0.015, 0.020, 0.025, 0.030, 0.035]
    grid = []
    for g in growths:
        grid.append({
            "growth": g,
            "irr": [round(hold_irr(mid, g=g, exit_cap=c)["irr"], 6) for c in exit_caps],
        })
    out["sensitivity"] = {"exit_caps": exit_caps, "rows": grid, "noi": mid}

    # 4. Horizon sensitivity (lease expiry 2030-2035)
    horizons = []
    for n in (3, 5, 7, 9):
        h = hold_irr(mid, n=n)
        s = sell_and_reinvest(mid, n=n)
        horizons.append({"years": n, "hold_irr": h["irr"], "sell_irr": s["irr"],
                         "hold_terminal": round(sum(h["cash_flows"][1:])),
                         "sell_terminal": round(s["terminal_wealth"])})
    out["horizons"] = horizons

    # 5. Transaction-tax cliff (City of LA)
    prices = [4000000, 5000000, 5200000, 5390000, 5400000, 5500000, 6000000,
              8000000, 10500000, 10900000, 11000000, 15000000]
    cliff = []
    for p in prices:
        ula = 0.0
        if p > A["ula_high_threshold"]:
            ula = p * A["ula_high_rate"]
        elif p > A["ula_low_threshold"]:
            ula = p * A["ula_low_rate"]
        transfer = p * A["transfer_tax_rate"]
        cliff.append({
            "price": p,
            "transfer_tax": round(transfer),
            "ula": round(ula),
            "total_transfer": round(transfer + ula),
            "pct_of_price": round((transfer + ula) / p * 100, 3),
            "net_before_mortgage": round(p - transfer - ula),
        })
    out["tax_cliff"] = cliff

    # 6. Cost of selling, all-in (illustrative, mid NOI)
    v0 = mid / A["cap_entry"]
    out["all_in_exit_cost"] = {
        "price": round(v0),
        "brokerage_3pct": round(v0 * 0.03),
        "transfer_tax": round(v0 * A["transfer_tax_rate"]),
        "ula": 0,
        "legal_closing": round(v0 * 0.0094),
        "total": round(v0 * A["sale_cost"]),
        "pct": round(A["sale_cost"] * 100, 2),
    }

    # 6b. Entry-cap / exit-cap spread sensitivity (mid NOI)
    spread = []
    for ec in (0.0600, 0.0625, 0.0650, 0.0675, 0.0700, 0.0725):
        flat = hold_irr(mid, exit_cap=ec, entry_cap=ec)["irr"]
        widen25 = hold_irr(mid, exit_cap=ec + 0.0025, entry_cap=ec)["irr"]
        widen75 = hold_irr(mid, exit_cap=ec + 0.0075, entry_cap=ec)["irr"]
        spread.append({"entry_cap": ec, "flat": flat, "widen_25": widen25, "widen_75": widen75})
    out["cap_spread"] = spread

    # 7. After-tax illustration at several basis levels (flat, not an IRR)
    tax_rows = []
    for basis_pct in (0.35, 0.50, 0.65):
        for price in (2700000, 5400000, 8000000):
            basis = price * basis_pct
            gain = price - basis
            recapture = min(gain, basis * 0.35)  # illustrative share of gain treated as unrecaptured s.1250
            fed_cap = max(0, gain - recapture) * 0.20
            fed_recap = recapture * 0.25
            niit = max(0, gain - recapture) * 0.038
            ca = gain * 0.133
            tax = fed_cap + fed_recap + niit + ca
            tax_rows.append({
                "price": price, "basis_pct": basis_pct, "basis": round(basis),
                "gain": round(gain), "estimated_tax": round(tax),
                "effective_on_gain": round(tax / gain * 100, 1) if gain > 0 else 0,
                "net_after_tax": round(price - tax),
            })
    out["after_tax"] = tax_rows

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print("wrote", OUT)
    for c in comp:
        print(f"NOI {c['noi']:,}: hold IRR {c['hold']['irr']*100:.2f}% | "
              f"sell+1031 IRR {c['sell']['irr']*100:.2f}% | breakeven exit cap {c['breakeven_exit_cap']*100:.2f}%")


if __name__ == "__main__":
    main()
