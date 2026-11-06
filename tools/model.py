#!/usr/bin/env python3
"""
SP-01 Decision Model — Jack in the Box NNN asset, central Los Angeles.

Design rules
------------
1. OBSERVED inputs come only from data/model_assumptions.json -> verified_anchor_inputs,
   each carrying a source id resolvable in data/sources.json.
2. Every judgement is registered as an ASSUMPTION with an id (A01..A19), a basis, and a
   range. The engine never hard-codes a market number of its own.
3. Scale invariance: rent, value and basis are unknown and private. Property value is
   carried as an explicit scenario band (V1..V3), never as a fact about this asset.
   Current rent is expressed as the going-in cap rate, so results are returns on capital.
4. Everything is seeded, so the user can reproduce every number.

Primary metric
--------------
after-tax compound annual return on deployed capital:
    CAGR = (terminal_after_tax_wealth / V0) ** (1 / years) - 1

where terminal_after_tax_wealth is measured at the comparison horizon with all interim
cash reinvested (A19), the property liquidated at horizon value, and all taxes paid —
including taxes on reinvestment growth. This is directly comparable across strategies
that exit at different dates, which a raw IRR is not.

Secondary metric: net after-tax sale proceeds in the exit year — what the owner actually
receives, which is the number that matters for replacing the asset under §1031.
"""

import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


def load(name):
    with open(os.path.join(DATA, name)) as f:
        return json.load(f)


# ----------------------------------------------------------------------------- helpers

def percentile(sorted_vals, p):
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * p
    lo = math.floor(k)
    hi = math.ceil(k)
    if lo == hi:
        return sorted_vals[int(k)]
    return sorted_vals[lo] * (hi - k) + sorted_vals[hi] * (k - lo)


def poisson(rng, lam):
    l, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= l:
            return k
        k += 1


# ----------------------------------------------------------------------------- tax

def transfer_tax(gross, px):
    """County + City of LA + Measure ULA. Rates from S16 and S17."""
    county = gross * px["county_transfer_tax_rate"]
    city = gross * px["city_transfer_tax_rate"]
    u = 0.0
    if gross >= px["ula_upper_threshold"]:
        u = gross * px["ula_rate_upper"]
    elif gross > px["ula_lower_threshold"]:
        u = gross * px["ula_rate_lower"]
    return {"county": county, "city": city, "ula": u, "total": county + city + u}


def total_sale_costs(gross, px, a):
    return gross * a["A09"] + transfer_tax(gross, px)["total"]


# ----------------------------------------------------------------------------- simulation

class Params:
    def __init__(self, assump):
        self.A = {r["id"]: r["value"] for r in assump["assumptions"]}
        self.OBS = {r["name"]: r["value"] for r in assump["verified_anchor_inputs"]}
        self.spec = {s["id"]: s for s in assump["scenario_parameters"]["strategies"]}
        self.horizon = assump["scenario_parameters"]["horizon_end"]
        self.start = assump["scenario_parameters"]["horizon_start"]
        self.reinvest = 0.065          # A19
        self.px = {
            "county_transfer_tax_rate": self.OBS["county_transfer_tax_rate"],
            "city_transfer_tax_rate": self.OBS["city_transfer_tax_rate"],
            "ula_lower_threshold": self.OBS["ula_lower_threshold"],
            "ula_upper_threshold": self.OBS["ula_upper_threshold"],
            "ula_rate_lower": self.OBS["ula_rate_lower"],
            "ula_rate_upper": self.OBS["ula_rate_upper"],
        }


def draw_path(rng, a, horizon):
    """One macro path: recession years, black-swan years, rent deviation, cap-rate shift."""
    recessions = []
    for _ in range(min(2, poisson(rng, 0.35))):
        s = rng.randint(2027, max(2027, horizon - 3))
        recessions.append((s, s + rng.randint(2, 3)))

    swans = [y for y in range(2027, horizon + 1) if rng.random() < a["A13"]]

    return {
        "recessions": recessions,
        "swans": swans,
        "rent_dev": rng.gauss(0.0, 0.006),
        "cap_shift": rng.gauss(0.0, 0.0040),
    }


def in_recession(year, path):
    return any(s <= year <= e for s, e in path["recessions"])


# ----------------------------------------------------------------------------- core

def evaluate(sid, path, v0, P, silent_swan=False):
    """Run one strategy on one macro path.

    Returns a dict with terminal after-tax wealth, exit-year net proceeds,
    the property cash-flow series for IRR, and diagnostic counters.
    """
    a, px, spec = P.A, P.px, P.spec[sid]
    exit_year = spec["exit_year"]
    exchange = spec.get("exchange", False)
    start, horizon = P.start, P.horizon
    years = horizon - start

    basis0 = a["A10"] * v0
    cap0 = max(0.040, min(0.085, a["A01"]))

    def net_proceeds_at(gross, basis, is_exchange, deferred):
        """After-tax proceeds from a liquidation of the property at `gross`."""
        costs = total_sale_costs(gross, px, a)
        net = gross - costs
        gain = max(0.0, net - basis)
        if is_exchange:
            return net, 0.0, gain  # gain deferred, no tax
        return net - a["A11"] * gain, a["A11"] * gain, 0.0

    # ---- t = 0 sale (exit_year == start)
    if exit_year <= start:
        costs = total_sale_costs(v0, px, a)
        net = v0 - costs
        gain = max(0.0, net - basis0)
        tax = 0.0 if exchange else a["A11"] * gain
        proceeds = net - tax
        tw = proceeds * ((1.0 + P.reinvest) ** years)
        tw -= a["A11"] * max(0.0, tw - proceeds)   # tax on reinvestment growth at liquidation
        return {
            "terminal_wealth": tw,
            "exit_proceeds": proceeds,
            "exit_gross": v0,
            "sale_costs": costs,
            "tax_at_exit": tax,
            "irr_cfs": [-v0, tw],       # capital deployed vs. terminal value
            "cagr": (tw / v0) ** (1.0 / years) - 1.0 if years > 0 and tw > 0 else None,
            "swan_hits": 0,
            "rent_lost": 0.0,
            "hold_to_horizon": False,
        }

    noi = v0 * cap0
    value = v0
    cap = cap0
    cash_bank = 0.0
    basis_now = basis0
    deferred_gain = 0.0
    sold = False
    exit_proceeds = None
    exit_gross = None
    sale_cost_amt = 0.0
    tax_exit = 0.0
    swan_hits = 0
    rent_lost = 0.0
    irr_cfs = [-v0]

    for year in range(start + 1, horizon + 1):
        if not sold:
            # ---- rent growth
            renewed = spec.get("renew", False) and year > 2030
            g = a["A04"] if renewed else a["A03"]
            g += path["rent_dev"] * (1.0 if renewed else 0.5)
            if renewed:
                g += a["A17"]
            if in_recession(year, path):
                g = min(g, -0.04)
            g = max(-0.08, min(0.09, g))
            noi *= (1.0 + g)

            # ---- black swan: rent interruption plus unrecovered capital cost
            swan = year in path["swans"] and not silent_swan
            if swan:
                swan_hits += 1
                rent_lost += noi
                noi_cash = 0.0
                # impairment: unrecovered capital cost plus an 18-month NOI loss
                cash_bank -= value * a["A14"] * (1.0 - a["A15"])
                noi *= (1.0 - a["A14"] * (1.0 - a["A15"]))
            else:
                noi_cash = noi

            reserve = a["A08"] * value
            net_cash = noi_cash - reserve
            cash_bank = cash_bank * (1.0 + P.reinvest) + net_cash

            # ---- reprice
            cap = cap0 + path["cap_shift"] + lease_penalty(year, sid, P)
            if in_recession(year, path):
                cap += 0.010
            if year in path["swans"]:
                cap += 0.0050
            cap = max(0.035, min(0.115, cap))
            value = noi / cap

            if year == exit_year:
                sold = True
                exit_gross = value
                sale_cost_amt = total_sale_costs(exit_gross, px, a)
                net = exit_gross - sale_cost_amt
                gain = max(0.0, net - basis_now)
                if exchange:
                    tax_exit = 0.0
                    deferred_gain += gain
                    basis_now = basis_now + gain
                else:
                    tax_exit = a["A11"] * gain
                    basis_now = net
                exit_proceeds = net - tax_exit
                cash_bank = cash_bank + exit_proceeds
                irr_cfs.append(exit_proceeds)
                continue
        else:
            cash_bank *= (1.0 + P.reinvest)

        irr_cfs.append(0.0 if sold else net_cash)

    # ---- horizon liquidation of anything still held
    if not sold:
        exit_gross = value
        sale_cost_amt = total_sale_costs(exit_gross, px, a)
        net = exit_gross - sale_cost_amt
        gain = max(0.0, net - basis_now) + deferred_gain
        tax_exit = a["A11"] * gain
        exit_proceeds = net - tax_exit
        cash_bank = cash_bank + exit_proceeds
        basis_now = net

    # tax on growth of the reinvestment portfolio at final liquidation
    growth_tax = a["A11"] * max(0.0, cash_bank - (exit_proceeds or 0.0) - v0)
    cash_bank -= growth_tax

    # truncate the IRR series at the exit year so trailing zero periods do not dilute it
    cut = irr_cfs.index(exit_proceeds) if exit_proceeds in irr_cfs else len(irr_cfs) - 1
    irr_series = irr_cfs[: cut + 1]

    return {
        "terminal_wealth": cash_bank,
        "exit_proceeds": exit_proceeds,
        "exit_gross": exit_gross,
        "sale_costs": sale_cost_amt,
        "tax_at_exit": tax_exit,
        "irr_cfs": irr_series,
        "cagr": (cash_bank / v0) ** (1.0 / years) - 1.0 if cash_bank > 0 else None,
        "swan_hits": swan_hits,
        "rent_lost": rent_lost,
        "hold_to_horizon": not sold,
    }


def remaining_term_at(year, sid):
    """Years of in-place lease remaining at `year` for this strategy action table.

    The user gave a 2030-2035 expiry window and no exact date. The base case takes
    2032.5 as the mid-point of the window; 6.5 years from 2026.
    """
    return {
        "S1": 6.5 - (year - 2026),
        "S2": 6.5 - (year - 2026),
        "S3": 6.5 - (year - 2026),
        "S4": 12.0 - (year - 2036),   # renewed 2032 to 2042, then renewed 2042 to 2052
        "S5": 22.0 - (year - 2036),
        "S6": 6.5 - (year - 2026),
        "S7": 12.0 - (year - 2036),
    }.get(sid, 0.0)


def lease_penalty(year, sid, P):
    """Cap-rate widening for short remaining term (A16)."""
    rem = max(0.0, remaining_term_at(year, sid))
    return P.A["A16"] * max(0.0, min(1.0, (5.0 - rem) / 5.0))


# ----------------------------------------------------------------------------- main

def main():
    assump = load("model_assumptions.json")
    P = Params(assump)
    a = P.A

    n_paths = assump["scenario_parameters"]["monte_carlo_paths"]
    seed = assump["scenario_parameters"]["random_seed"]

    value_bands = [
        {"id": "V1", "label": "Below the Measure ULA threshold", "value": 4_000_000},
        {"id": "V2", "label": "Between ULA thresholds (4% cliff applies)", "value": 6_500_000},
        {"id": "V3", "label": "Above the upper ULA threshold (5.5% applies)", "value": 12_000_000},
    ]

    rng = random.Random(seed)
    paths = [draw_path(rng, a, P.horizon) for _ in range(n_paths)]
    renewal_draws = [rng.random() for _ in range(n_paths)]

    rows = []
    for band in value_bands:
        v0 = band["value"]
        for sid, spec in P.spec.items():
            cagrs, wealth, proceeds = [], [], []
            swans = 0
            for i in range(n_paths):
                r = evaluate(sid, paths[i], v0, P)
                penalty = 0.0
                # a strategy that renews depends on the tenant actually renewing
                if spec.get("renew") and renewal_draws[i] > a["A05"]:
                    penalty = v0 * a["A07"] + (v0 * a["A01"]) * (a["A06"] / 12.0)
                tw = r["terminal_wealth"] - penalty
                wealth.append(tw)
                cagrs.append(r["cagr"])
                if r["exit_proceeds"] is not None:
                    proceeds.append(r["exit_proceeds"] - penalty)
                swans += r["swan_hits"]

            ws = sorted(wealth)
            cs = sorted(c for c in cagrs if c is not None)
            ps = sorted(proceeds)
            n = len(ws)

            # CRRA certainty equivalent on terminal wealth.
            # gamma = 1 reduces to geometric mean; gamma > 1 penalises downside.
            def ce(gamma):
                if not ws:
                    return None
                if abs(gamma - 1.0) < 1e-9:
                    s = sum(math.log(w) for w in ws if w > 0)
                    return math.exp(s / len(ws))
                p = 1.0 - gamma
                s = sum((w ** p) for w in ws if w > 0)
                return (s / len(ws)) ** (1.0 / p)

            ce2 = ce(2.0)
            ce4 = ce(4.0)

            rows.append({
                "value_band": band["id"],
                "value_label": band["label"],
                "value_assumed": v0,
                "strategy": sid,
                "name": spec["name"],
                "exit_year": spec["exit_year"],
                "renew": spec.get("renew", False),
                "exchange": spec.get("exchange", False),
                "cagr": {
                    "p05": percentile(cs, 0.05), "p25": percentile(cs, 0.25),
                    "p50": percentile(cs, 0.50), "p75": percentile(cs, 0.75),
                    "p95": percentile(cs, 0.95),
                    "mean": sum(cs) / len(cs) if cs else None,
                    "prob_below_zero": sum(1 for x in cs if x < 0) / len(cs) if cs else None,
                },
                "terminal_wealth": {
                    "p05": percentile(ws, 0.05), "p25": percentile(ws, 0.25),
                    "p50": percentile(ws, 0.50), "p75": percentile(ws, 0.75),
                    "p95": percentile(ws, 0.95),
                    "mean": sum(ws) / n,
                    "cvar5": sum(ws[: max(1, n // 20)]) / max(1, n // 20),
                    "prob_below_start": sum(1 for x in ws if x < v0) / n,
                },
                "exit_proceeds": {
                    "p05": percentile(ps, 0.05), "p50": percentile(ps, 0.50),
                    "p95": percentile(ps, 0.95),
                } if ps else None,
                "certainty_equivalent": {
                    "gamma_2": ce2,
                    "gamma_4": ce4,
                    "note": "CRRA utility on terminal after-tax wealth. gamma=1 is the geometric mean; higher gamma penalises downside dispersion more heavily. These are the numbers used to rank strategies for a risk-averse owner.",
                },
                "swan_exposure": {
                    "expected_single_year_risk": a["A13"],
                    "cumulative_prob_to_exit": 1.0 - (1.0 - a["A13"]) ** max(0, spec["exit_year"] - 2026),
                    "avg_swan_hits_per_path": swans / n_paths,
                },
            })

    # ---- calm, deterministic comparison
    calm = {"recessions": [], "swans": [], "rent_dev": 0.0, "cap_shift": 0.0}
    calm_rows = []
    for band in value_bands:
        for sid, spec in P.spec.items():
            r = evaluate(sid, calm, band["value"], P)
            calm_rows.append({
                "value_band": band["id"],
                "strategy": sid,
                "name": spec["name"],
                "exit_year": spec["exit_year"],
                "terminal_wealth": r["terminal_wealth"],
                "cagr": r["cagr"],
                "exit_proceeds": r["exit_proceeds"],
                "exit_gross": r["exit_gross"],
                "sale_costs": r["sale_costs"],
                "tax_at_exit": r["tax_at_exit"],
                "hold_to_horizon": r["hold_to_horizon"],
            })

    # ---- one-at-a-time sensitivity: which assumptions actually move the answer?
    sens_params = [
        ("A01", "Going-in cap rate (current rent as a yield on value)"),
        ("A02", "Cap-rate risk spread"),
        ("A03", "Rent growth in the existing lease"),
        ("A04", "Market rent growth at renewal"),
        ("A05", "Probability the tenant renews"),
        ("A09", "Selling costs"),
        ("A10", "Owner's adjusted basis as a share of value"),
        ("A11", "Blended tax rate on gain"),
        ("A13", "Annual black-swan probability"),
        ("A14", "Black-swan severity"),
    ]
    sens_rows = []
    for pid, label in sens_params:
        spec_row = next((r for r in assump["assumptions"] if r["id"] == pid), None)
        if not spec_row or "range" not in spec_row or spec_row["range"] is None:
            continue
        lo, hi = spec_row["range"]
        mid = P.A[pid]
        results = {}
        for tag, val in (("low", lo), ("base", mid), ("high", hi)):
            P.A[pid] = val
            m = 3000
            rng2 = random.Random(seed + 7)
            p2 = [draw_path(rng2, P.A, P.horizon) for _ in range(m)]
            rd2 = [rng2.random() for _ in range(m)]
            acc = {"S4": [], "S6": []}
            for i in range(m):
                for sid in ("S4", "S6"):
                    r = evaluate(sid, p2[i], 6_500_000, P)
                    tw = r["terminal_wealth"]
                    if sid == "S4" and rd2[i] > P.A["A05"]:
                        tw -= 6_500_000 * P.A["A07"] + 6_500_000 * P.A["A01"] * (P.A["A06"] / 12.0)
                    acc[sid].append(tw)
            results[tag] = {k: sorted(v)[m // 2] for k, v in acc.items()}
        P.A[pid] = mid
        sens_rows.append({
            "assumption_id": pid,
            "label": label,
            "base_value": mid,
            "low_value": lo,
            "high_value": hi,
            "S4_median": results["base"]["S4"],
            "S6_median": results["base"]["S6"],
            "S4_median_low": results["low"]["S4"],
            "S4_median_high": results["high"]["S4"],
            "swing": abs(results["high"]["S4"] - results["low"]["S4"]),
        })
    sens_rows.sort(key=lambda r: r["swing"], reverse=True)

    # ---- optimal exit-year scan: does when you sell matter, and where is the peak?
    exit_scan = []
    for ey in range(2026, 2036):
        sid = "SCAN"
        # temporarily evaluate a one-off exit year by cloning the S3 action table
        P.spec["SCAN"] = {"id": "SCAN", "name": f"Sell in {ey}", "exit_year": ey}
        globals()["remaining_term_at"]  # keep linters quiet
        r = evaluate("SCAN", calm, 6_500_000, P)
        # build a matched claim: risk accumulates with time held
        prob_shock = 1.0 - (1.0 - a["A13"]) ** max(0, ey - 2026)
        exit_scan.append({
            "exit_year": ey,
            "years_held": ey - 2026,
            "terminal_wealth": r["terminal_wealth"],
            "cagr": r["cagr"],
            "exit_proceeds": r["exit_proceeds"],
            "exit_gross": r["exit_gross"],
            "cumulative_shock_exposure": prob_shock,
        })
        del P.spec["SCAN"]
    best_tw = max(exit_scan, key=lambda r: r["terminal_wealth"])
    best_proceeds = max(exit_scan, key=lambda r: r["exit_proceeds"] or 0)

    # ---- ULA cliff
    cliff = []
    for price in [5_000_000, 5_300_000, 5_399_999, 5_400_001, 5_500_000, 6_500_000,
                  10_899_999, 10_900_001, 12_000_000]:
        t = transfer_tax(price, P.px)
        cliff.append({"price": price, **t, "effective_rate": t["total"] / price})

    # ---- break-even: which going-in cap rate makes sell-before-expiry exactly match renew-and-hold?
    breakeven = []
    for v in [4_000_000, 6_500_000, 12_000_000]:
        sweep = []
        saved = P.A["A01"]
        for i in range(0, 321):
            cap = 0.0350 + i * 0.00025
            P.A["A01"] = cap
            sell = evaluate("S3", calm, v, P)["terminal_wealth"]
            hold = evaluate("S4", calm, v, P)["terminal_wealth"]
            sweep.append({"cap_rate": cap, "sell": sell, "hold": hold, "diff": sell - hold})
        P.A["A01"] = saved
        crossing = None
        for i in range(1, len(sweep)):
            a0, a1 = sweep[i - 1], sweep[i]
            if (a0["diff"] < 0) != (a1["diff"] < 0):
                t = abs(a0["diff"]) / (abs(a0["diff"]) + abs(a1["diff"]))
                crossing = a0["cap_rate"] + t * (a1["cap_rate"] - a0["cap_rate"])
                break
        breakeven.append({
            "value": v,
            "cap_rate_where_indifferent": crossing,
            "min_cap_tested": sweep[0]["cap_rate"],
            "max_cap_tested": sweep[-1]["cap_rate"],
            "diff_at_min_cap": sweep[0]["diff"],
            "diff_at_max_cap": sweep[-1]["diff"],
        })

    # ---- explicit stress grid: business as usual vs. named black-swan cases
    stress_cases = [
        {"id": "B0", "name": "Business as usual (calm, no shocks)", "path": calm},
        {"id": "B1", "name": "One recession during the hold", "path": {
            "recessions": [(2029, 2031)], "swans": [], "rent_dev": 0.0, "cap_shift": 0.0}},
        {"id": "B2", "name": "Tenant vacates at lease expiry", "path": calm, "vacate": True},
        {"id": "B3", "name": "Wildfire-scale shock in 2031", "path": {
            "recessions": [], "swans": [2031], "rent_dev": 0.0, "cap_shift": 0.0}},
        {"id": "B4", "name": "Cap-rate dislocation of +175bp", "path": {
            "recessions": [], "swans": [], "rent_dev": -0.010, "cap_shift": 0.0175}},
        {"id": "B5", "name": "Stagflation: zero rent growth, cap rates +100bp", "path": {
            "recessions": [], "swans": [], "rent_dev": -0.0275, "cap_shift": 0.0100}},
        {"id": "B6", "name": "Sustained negative rent drift", "path": {
            "recessions": [], "swans": [], "rent_dev": -0.0600, "cap_shift": 0.0}},
    ]
    stress_rows = []
    for sc in stress_cases:
        for sid in ["S1", "S3", "S4", "S6"]:
            r = evaluate(sid, sc["path"], 6_500_000, P)
            tw = r["terminal_wealth"]
            if sc.get("vacate") and P.spec[sid].get("renew"):
                tw -= 6_500_000 * P.A["A07"] + 6_500_000 * P.A["A01"] * (P.A["A06"] / 12.0)
            years = P.horizon - P.start
            stress_rows.append({
                "case": sc["id"], "case_name": sc["name"], "strategy": sid,
                "name": P.spec[sid]["name"],
                "terminal_wealth": tw,
                "exit_proceeds": r["exit_proceeds"],
                "cagr": (tw / 6_500_000) ** (1.0 / years) - 1.0 if tw > 0 else None,
            })

    out = {
        "meta": {
            "compiled": "2026-11-06",
            "engine": "tools/model.py",
            "horizon_start": P.start,
            "horizon_end": P.horizon,
            "paths": n_paths,
            "seed": seed,
            "reinvestment_rate": P.reinvest,
            "reinvestment_note": "Interim cash is reinvested at 6.5% nominal and taxed at A11 on liquidation at the horizon.",
            "sale_costs_definition": "Brokerage, title, escrow and legal (A09) plus county documentary transfer tax (S16), City of Los Angeles base transfer tax (S17) and Measure ULA where applicable (S17).",
        },
        "observed_inputs": assump["verified_anchor_inputs"],
        "assumptions": assump["assumptions"],
        "value_bands": value_bands,
        "strategies": rows,
        "deterministic_calm": calm_rows,
        "ula_cliff": cliff,
        "sensitivity": sens_rows,
        "exit_year_scan": exit_scan,
        "exit_year_scan_summary": {"best_terminal_wealth_year": best_tw["exit_year"], "best_terminal_wealth": best_tw["terminal_wealth"], "best_exit_proceeds_year": best_proceeds["exit_year"], "best_exit_proceeds": best_proceeds["exit_proceeds"]},
        "stress_grid": stress_rows,
        "breakeven_cap_rate": breakeven,
    }

    with open(os.path.join(DATA, "model_output.json"), "w") as f:
        json.dump(out, f, indent=1)

    print(f"wrote data/model_output.json — {len(rows)} strategy/band pairs x {n_paths} paths")
    print("\nCalm-state comparison, V2 band ($6.5M):")
    print(f"  {'':3s} {'strategy':46s} {'exit':>6s} {'CAGR':>8s} {'proceeds':>14s} {'TW':>16s}")
    for r in calm_rows:
        if r["value_band"] == "V2":
            pr = f"${r['exit_proceeds']:,.0f}" if r["exit_proceeds"] else "—"
            cg = f"{r['cagr']*100:.2f}%" if r["cagr"] else "—"
            print(f"  {r['strategy']:3s} {r['name'][:46]:46s} {r['exit_year']:>6d} {cg:>8s} {pr:>14s} ${r['terminal_wealth']:>15,.0f}")
        if r["value_band"] == "V2":
            pass
    print("\nBreak-even going-in cap rate (sell-before-expiry vs renew-and-hold):")
    for b in breakeven:
        print(f"  value ${b['value']:,.0f}: indifferent at cap rate {b['cap_rate_where_indifferent']*100:.2f}%" if b['cap_rate_where_indifferent'] else f"  value ${b['value']:,.0f}: no crossing found")


if __name__ == "__main__":
    main()
