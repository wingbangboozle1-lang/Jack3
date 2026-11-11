#!/usr/bin/env python3
"""Deterministic 2026-2035 scenario engine for Asset A (anonymised NNN restaurant asset).

WHAT THIS MODULE IS
    Arithmetic with every assumption printed.  It answers "which route leaves the owner
    better off after tax and transaction cost, and by how much", expressed ONLY as a
    multiple of ONE YEAR OF CURRENT CONTRACTUAL BASE RENT (1 R).  One year of rent is the
    only scale that can be carried without knowing the rent, because every other quantity
    in the model is driven by it.

WHAT THIS MODULE IS NOT
    * Not a valuation, appraisal or price estimate.
    * Not a forecast of rent, cap rates, interest rates or population.
    * Not a probability of renewal, closure or catastrophe.
    * Not investment, tax or legal advice.

    No official agency publishes a cap rate, a rent level or a discount rate for this
    parcel, and the executed lease was never supplied.  Any dollar figure produced here
    would therefore be an artefact of an invented input.  So the module deliberately
    publishes *ratios and break-evens* (for example "holding must out-earn selling unless
    the exit cap widens by more than X basis points") under explicitly disclosed
    assumption sets, and never a dollar value of the asset.

THE ONE EXTERNALLY SOURCED NUMBER
    The discount-rate grid is anchored on the 10-year Treasury constant-maturity yield,
    4.88% on 2026-11-09 (Federal Reserve H.15 via FRED, series DGS10).  It is a market
    rate, not the owner's required return, so the grid sweeps above it.

DETERMINISM
    Pure stdlib.  No network, no clock, no randomness, no floating-point accumulation
    across calls.  ``compute()`` is idempotent and ``self_test()`` proves the closed-form
    maths against brute-force year-by-year loops before any table is published.
"""

from __future__ import annotations

import math

# --------------------------------------------------------------------------- anchors
TREASURY_ANCHOR = 0.0488          # FRED DGS10, observation for 2026-11-09
TREASURY_ANCHOR_DATE = "2026-11-09"
CPI_ANCHOR = 0.037               # BLS CPI-U, LA metro, 12-month change, Sep 2026 (BLS summary)
ECI_ANCHOR = 0.039               # BLS ECI, LA-Long Beach CSA, 12-month change, Sep 2026
PAYROLL_GROWTH_ANCHOR = 0.005    # BLS LA metro total nonfarm, 12-month change, Sep 2026

# --------------------------------------------------------------------------- grids
HORIZON_YEARS = (5, 6, 7, 8, 9)          # 2026 -> 2031..2035
CAP_NOW = (0.050, 0.055, 0.060, 0.065)   # cap rate if sold today  (ASSUMPTION)
CAP_EXIT = (0.050, 0.055, 0.060, 0.065)  # cap rate at exit        (ASSUMPTION)
RENT_GROWTH = (0.000, 0.010, 0.020, 0.030)   # contractual escalator   (ASSUMPTION)
DISCOUNT = (0.0488, 0.060, 0.070, 0.080)     # owner's required return (ASSUMPTION)
TRANSFER_COST = (0.0045, 0.020)          # city base 0.45% / city base + 4% ULA  (VERIFIED rules)
SELL_COST = 0.020                        # brokerage + due diligence    (ASSUMPTION)
TAX_RATE = 0.35                          # combined federal+CA marginal (ASSUMPTION)

# Base case used for the headline tables (all disclosed on the page).
# Base case: entry cap 5.75%, exit cap 50 bp wider (the standard conservative
# underwriting convention for a lease with rolling term), rent growth 1.50% (between the
# flat-escalator case and the 3.7% CPI observation), required return 7.50% = the 4.88%
# Treasury anchor plus a 262 bp risk premium.  Every one of these is an ASSUMPTION and is
# printed as such on the published page; none is a market observation for this parcel.
BASE = dict(cap_now=0.0575, cap_exit=0.0625, growth=0.015, discount=0.075,
            transfer=0.0045, horizon=9, vacancy_months=18,
            release_rent_factor=0.90, sell_cost=SELL_COST, tax_rate=TAX_RATE)


# --------------------------------------------------------------------------- maths
def pv_annuity(growth: float, discount: float, years: int) -> float:
    """PV of 1 unit of rent received at the end of years 1..N, growing at ``growth``.

    Closed form of  sum_{t=1..N} (1+g)^(t-1) / (1+d)^t .  When g == d the sum
    collapses to N/(1+d); the closed form handles that case without dividing by zero.
    """
    if years <= 0:
        return 0.0
    if abs(growth - discount) < 1e-12:
        return years / (1.0 + discount)
    q = (1.0 + growth) / (1.0 + discount)
    return (1.0 - q ** years) / (discount - growth)


def pv_annuity_loop(growth: float, discount: float, years: int) -> float:
    """Brute-force reference implementation used only by self_test()."""
    return sum((1.0 + growth) ** (t - 1) / (1.0 + discount) ** t for t in range(1, years + 1))


def hold_pv(cap_exit: float, growth: float, discount: float, horizon: int,
            vacancy_months: int = 0, release_factor: float = 0.90) -> float:
    """PV of holding for ``horizon`` years then selling, in multiples of 1 R.

    Rent accrues at the end of each year, growing at ``growth``; at the end of year N
    the asset is sold for  (rent in year N) * (1+growth) / cap_exit  before costs.
    ``vacancy_months`` removes that fraction of a year's rent at the end of the horizon
    and re-lets at ``release_factor`` of the prior rent (0 disables the stress).
    """
    pv = pv_annuity(growth, discount, horizon)
    exit_rent = (1.0 + growth) ** horizon
    if vacancy_months:
        loss_years = vacancy_months / 12.0
        pv -= exit_rent * loss_years / (1.0 + discount) ** horizon
        exit_rent *= release_factor
    pv += exit_rent / cap_exit / (1.0 + discount) ** horizon
    return pv


def sell_now_net(cap_now: float, transfer: float = 0.0045, sell_cost: float = SELL_COST,
                 tax_rate: float = 0.0) -> float:
    """Net proceeds of selling today, in multiples of 1 R, before income tax by default.

    Gross price = 1 R / cap_now.  Transfer taxes and selling costs are deducted.  The
    tax term is optional and is NOT applied unless a basis multiple is supplied, because
    the owner's basis is private and unknowable here.
    """
    gross = 1.0 / cap_now
    return gross * (1.0 - transfer - sell_cost)


def sell_now_net_after_tax(cap_now: float, basis_multiple: float | None = None,
                           transfer: float = 0.0045, sell_cost: float = SELL_COST,
                           tax_rate: float = TAX_RATE) -> float | None:
    """After-tax sale proceeds in multiples of 1 R.

    ``basis_multiple`` is the owner's adjusted basis expressed in the same units (so
    basis_multiple=4.0 means the basis equals four years of current rent).  When it is
    None the function returns None: the site does not invent a basis.
    """
    if basis_multiple is None:
        return None
    gross = 1.0 / cap_now
    net_before_tax = gross * (1.0 - transfer - sell_cost)
    gain = net_before_tax - basis_multiple
    return net_before_tax - max(gain, 0.0) * tax_rate


def required_growth(cap_now: float, cap_exit: float, discount: float, horizon: int,
                    transfer: float = 0.0045, sell_cost: float = SELL_COST,
                    vacancy_months: int = 0, release_factor: float = 0.90) -> float | None:
    """Rent growth at which holding equals selling today after costs.

    Monotone bisection on a wide bracket.  Returns None when the bracket does not
    contain a root, i.e. the comparison cannot be closed by rent growth alone.
    """
    target = sell_now_net(cap_now, transfer, sell_cost)
    lo, hi = -0.20, 0.25
    f_lo = hold_pv(cap_exit, lo, discount, horizon, vacancy_months, release_factor) - target
    f_hi = hold_pv(cap_exit, hi, discount, horizon, vacancy_months, release_factor) - target
    if f_lo > 0 or f_hi < 0:
        return None
    for _ in range(120):
        mid = (lo + hi) / 2.0
        if hold_pv(cap_exit, mid, discount, horizon, vacancy_months, release_factor) > target:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0


def breakeven_exit_cap(cap_now: float, growth: float, discount: float, horizon: int,
                       transfer: float = 0.0045, sell_cost: float = SELL_COST) -> float | None:
    """Exit cap at which holding equals selling today after costs (monotone in cap)."""
    target = sell_now_net(cap_now, transfer, sell_cost)
    lo, hi = 0.02, 0.20
    # hold_pv falls as cap_exit rises
    if hold_pv(lo, growth, discount, horizon) < target:
        return None
    if hold_pv(hi, growth, discount, horizon) > target:
        return None
    for _ in range(120):
        mid = (lo + hi) / 2.0
        if hold_pv(mid, growth, discount, horizon) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


# --------------------------------------------------------------------------- tables
def table_horizon() -> list[dict]:
    """Hold vs sell for each possible expiry year, at the base assumptions."""
    out = []
    for h in HORIZON_YEARS:
        pv = hold_pv(BASE["cap_exit"], BASE["growth"], BASE["discount"], h)
        pv_vac = hold_pv(BASE["cap_exit"], BASE["growth"], BASE["discount"], h,
                         BASE["vacancy_months"], BASE["release_rent_factor"])
        sell = sell_now_net(BASE["cap_now"], BASE["transfer"])
        out.append({
            "horizon": h, "expiry_year": 2026 + h,
            "hold_pv": pv, "hold_pv_vacancy": pv_vac, "sell_net": sell,
            "ratio": pv / sell, "ratio_vacancy": pv_vac / sell,
            "delta": pv - sell, "delta_vacancy": pv_vac - sell,
        })
    return out


def table_exit_cap() -> list[dict]:
    """Hold/sell ratio across exit cap x discount, at the base rent growth."""
    out = []
    for cap_exit in CAP_EXIT:
        row = {"cap_exit": cap_exit, "values": []}
        for d in DISCOUNT:
            pv = hold_pv(cap_exit, BASE["growth"], d, BASE["horizon"])
            row["values"].append({"discount": d,
                                  "ratio": pv / sell_now_net(BASE["cap_now"], BASE["transfer"])})
        out.append(row)
    return out


def table_growth() -> list[dict]:
    """Hold/sell ratio across rent growth x discount, at the base exit cap."""
    out = []
    for g in RENT_GROWTH:
        row = {"growth": g, "values": []}
        for d in DISCOUNT:
            pv = hold_pv(BASE["cap_exit"], g, d, BASE["horizon"])
            row["values"].append({"discount": d,
                                  "ratio": pv / sell_now_net(BASE["cap_now"], BASE["transfer"])})
        out.append(row)
    return out


def table_breakeven() -> list[dict]:
    """Required rent growth and required exit cap for each discount rate."""
    out = []
    for d in DISCOUNT:
        g_req = required_growth(BASE["cap_now"], BASE["cap_exit"], d, BASE["horizon"],
                                BASE["transfer"])
        g_req_vac = required_growth(BASE["cap_now"], BASE["cap_exit"], d, BASE["horizon"],
                                    BASE["transfer"], vacancy_months=BASE["vacancy_months"],
                                    release_factor=BASE["release_rent_factor"])
        cap_req = breakeven_exit_cap(BASE["cap_now"], BASE["growth"], d, BASE["horizon"],
                                     BASE["transfer"])
        out.append({"discount": d, "growth_required": g_req,
                    "growth_required_vacancy": g_req_vac, "exit_cap_required": cap_req})
    return out


def table_transfer_cost() -> list[dict]:
    """What each transfer-tax regime costs, in rent multiples, at each cap rate."""
    out = []
    for cap_now in CAP_NOW:
        gross = 1.0 / cap_now
        out.append({
            "cap_now": cap_now, "gross": gross,
            "statutory": gross * 0.0056,          # 0.45% city base + 0.11% county documentary
            "sell_cost": gross * SELL_COST,       # disclosed 2.0% assumption
            "with_ula": gross * 0.0445,           # statutory + 4% Measure ULA tier
            "net_base": gross * (1 - 0.0056 - SELL_COST),
        })
    return out


def table_vacancy() -> list[dict]:
    """Cost of an 18-month void at expiry, by exit cap, in rent multiples and %."""
    out = []
    for cap_exit in CAP_EXIT:
        base = hold_pv(cap_exit, BASE["growth"], BASE["discount"], BASE["horizon"])
        stressed = hold_pv(cap_exit, BASE["growth"], BASE["discount"], BASE["horizon"],
                           BASE["vacancy_months"], BASE["release_rent_factor"])
        out.append({"cap_exit": cap_exit, "with_rent": base, "with_vacancy": stressed,
                    "loss": base - stressed, "loss_pct": (base - stressed) / base})
    return out


# --------------------------------------------------------------------------- stress
def stress_cases() -> list[dict]:
    """Black-swan and business-as-usual stress cases, each against the base case.

    Severity inputs are disclosed assumptions chosen from *observed* official events
    (the 2025 Los Angeles County fires, the USGS ShakeOut scenario, an 18-month
    re-letting period).  No cell is a probability.
    """
    base_pv = hold_pv(BASE["cap_exit"], BASE["growth"], BASE["discount"], BASE["horizon"])
    base_sell = sell_now_net(BASE["cap_now"], BASE["transfer"])

    cases = []

    def add(cid, name, kind, shock, pv, note):
        cases.append({
            "id": cid, "name": name, "kind": kind, "shock": shock,
            "pv": pv, "sell": base_sell, "ratio": pv / base_sell,
            "loss_vs_base": pv - base_pv,
            "loss_pct": (base_pv - pv) / base_pv if base_pv else None,
            "note": note,
        })

    # 1 business as usual: 18-month void at expiry, re-let at 90%
    add("S-01", "Expiry vacancy: 18 months void, re-let at 90% of prior rent", "Business as usual",
        "-18 months rent; -10% re-let rent",
        hold_pv(BASE["cap_exit"], BASE["growth"], BASE["discount"], BASE["horizon"],
                BASE["vacancy_months"], BASE["release_rent_factor"]),
        "Uses the only vacancy assumption disclosed: 18 months, 90% re-let. Not a measured figure.")
    # 2 tenant default one year before expiry, no recovery
    pv = (hold_pv(BASE["cap_exit"], BASE["growth"], BASE["discount"], BASE["horizon"])
          - (1.0 + BASE["growth"]) ** (BASE["horizon"] - 1) / (1.0 + BASE["discount"]) ** (BASE["horizon"] - 1))
    add("S-02", "Tenant default one year before expiry with no recovery", "Business as usual",
        "-1 year of rent", pv,
        "Arithmetic removal of the final rent year. Whether a guaranty exists is unknown (Flagged F-05).")
    # 3 exit cap widens 100 bp from base
    add("S-03", "Exit cap widens 100 bp above the base exit cap", "Business as usual",
        f"exit cap {BASE['cap_exit']:.1%} to {BASE['cap_exit'] + 0.01:.1%}",
        hold_pv(BASE["cap_exit"] + 0.01, BASE["growth"], BASE["discount"], BASE["horizon"]),
        "Rate-driven repricing stress; not a forecast of cap rates.")
    # 4 costs exceed escalator: growth 0, discount +100bp
    add("S-04", "No rent growth and a higher required return (+100 bp)", "Business as usual",
        "growth 0.0%; discount +1.00%",
        hold_pv(BASE["cap_exit"], 0.0, BASE["discount"] + 0.01, BASE["horizon"]),
        "CPI-U 3.7% / ECI 3.9% against a flat escalator erode real rent.")
    # 5 earthquake: 12 months closure + 15% of a year's rent in unrecovered cost
    pv = (hold_pv(BASE["cap_exit"], BASE["growth"], BASE["discount"], BASE["horizon"])
          - (1.0 + BASE["growth"]) ** BASE["horizon"] / (1.0 + BASE["discount"]) ** BASE["horizon"]
          - 0.15 / (1.0 + BASE["discount"]) ** (BASE["horizon"] // 2))
    add("S-05", "Earthquake: 12-month business interruption plus unrecovered cost", "Black swan",
        "-1 year rent; -0.15 R unrecovered cost", pv,
        "Severity scaled from the USGS ShakeOut scenario (M7.8: ~1,800 deaths, ~$213bn losses). "
        "No parcel ground-failure result exists (Flagged F-06).")
    # 6 wildfire: 18-month closure, re-let at 85%
    add("S-06", "Wildfire: 18-month closure, re-let at 85% of prior rent", "Black swan",
        "-18 months rent; -15% re-let rent",
        hold_pv(BASE["cap_exit"], BASE["growth"], BASE["discount"], BASE["horizon"],
                18, 0.85),
        "Scaled from the January 2025 Los Angeles County fires: 16,264 structures destroyed in 24 days "
        "(6,845 Palisades + 9,419 Eaton). Regional insurance repricing is the correlated channel.")
    # 7 correlated catastrophe: rent stops and exit cap widens 150bp
    add("S-07", "Correlated catastrophe: rent interruption plus a 150 bp exit-cap widening", "Black swan",
        "-18 months rent; exit cap +1.50%",
        hold_pv(BASE["cap_exit"] + 0.015, BASE["growth"], BASE["discount"], BASE["horizon"],
                BASE["vacancy_months"], BASE["release_rent_factor"]),
        "Models the simultaneous loss of income and liquidity that makes forced sales expensive.")
    # 8 forced sale: 10% discount to the base exit assumption plus full transfer cost
    forced = ((1.0 + BASE["growth"]) ** BASE["horizon"] / BASE["cap_exit"] * 0.90
              * (1.0 - 0.02 - SELL_COST) / (1.0 + BASE["discount"]) ** BASE["horizon"]
              + pv_annuity(BASE["growth"], BASE["discount"], BASE["horizon"]))
    add("S-08", "Forced sale at a 10% discount with 2% transfer cost and 2% selling cost",
        "Black swan", "-10% price; -2% transfer; -2% selling", forced,
        "Liquidity event at the worst moment; the owner cannot time the market.")
    return cases


def table_basis() -> list[dict]:
    """After-tax sale proceeds by assumed adjusted basis (the real basis is unknown).

    basis_multiple is expressed in years of current rent so it stays scale-free.  This is
    arithmetic on a disclosed assumption set, not a statement about Owner A's position.
    """
    out = []
    for basis in (0.0, 4.0, 8.0, 12.0):
        net = sell_now_net_after_tax(BASE["cap_now"], basis, BASE["transfer"],
                                     BASE["sell_cost"], BASE["tax_rate"])
        gross_net = sell_now_net(BASE["cap_now"], BASE["transfer"], BASE["sell_cost"])
        out.append({
            "basis": basis, "net_before_tax": gross_net, "net_after_tax": net,
            "tax": gross_net - net,
            "tax_pct_of_gross": (gross_net - net) / (1.0 / BASE["cap_now"]),
        })
    return out


def compute() -> dict:
    return {
        "treasury_anchor": TREASURY_ANCHOR,
        "treasury_anchor_date": TREASURY_ANCHOR_DATE,
        "cpi_anchor": CPI_ANCHOR,
        "eci_anchor": ECI_ANCHOR,
        "payroll_anchor": PAYROLL_GROWTH_ANCHOR,
        "base": BASE,
        "horizon": table_horizon(),
        "exit_cap": table_exit_cap(),
        "growth": table_growth(),
        "breakeven": table_breakeven(),
        "transfer": table_transfer_cost(),
        "vacancy": table_vacancy(),
        "basis": table_basis(),
        "stress": stress_cases(),
    }


# --------------------------------------------------------------------------- tests
def self_test() -> None:
    """Prove the closed forms against brute force before anything is published."""
    for g in (-0.05, 0.0, 0.01, 0.037, 0.07):
        for d in (0.0488, 0.07, 0.09):
            for n in (1, 5, 9, 30):
                a = pv_annuity(g, d, n)
                b = pv_annuity_loop(g, d, n)
                assert math.isclose(a, b, rel_tol=1e-12), (g, d, n, a, b)
    # growth == discount must not divide by zero
    assert math.isclose(pv_annuity(0.05, 0.05, 9), 9 / 1.05, rel_tol=1e-12)
    # zero horizon is zero
    assert pv_annuity(0.01, 0.07, 0) == 0.0
    # required_growth must reproduce the target when fed back in
    target = sell_now_net(0.055, 0.0045)
    g = required_growth(0.055, 0.06, 0.07, 9, 0.0045)
    if g is not None:
        assert math.isclose(hold_pv(0.06, g, 0.07, 9), target, rel_tol=1e-6), g
    # breakeven_exit_cap must reproduce the target when fed back in
    c = breakeven_exit_cap(0.055, 0.01, 0.07, 9, 0.0045)
    if c is not None:
        assert math.isclose(hold_pv(c, 0.01, 0.07, 9), target, rel_tol=1e-6), c
    # selling must be worth more than 1 R whenever costs are positive
    assert sell_now_net(0.10) < 1.0 / 0.10
    # compute() is idempotent
    assert compute() == compute()


if __name__ == "__main__":
    self_test()
    import json
    result = compute()
    print(json.dumps(result, indent=2))
    print("\nSELF-TEST PASS: closed-form annuity matches brute force; break-evens invert exactly.")
