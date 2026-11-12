"""Deterministic break-even framework for the sell-now versus hold-and-renew decision.

WHAT THIS IS
    Arithmetic. Every figure is expressed as a multiple of ONE YEAR OF CURRENT
    CONTRACTUAL BASE RENT ("1 R"). The owner has not supplied rent, price, basis,
    debt, cap rate or lease terms, and no official agency publishes a cap rate for
    this asset, so no dollar value is asserted anywhere in the output.

WHAT IT IS NOT
    Not a forecast, not a valuation, not a probability, not investment advice.
    It makes no claim about the future level of rents or cap rates. It answers one
    narrow question that the public record *can* answer:

        For a given discount rate, exit cap rate and rent growth, is the present
        value of holding to the lease horizon and renewing higher or lower than
        selling today at today's cap rate - and how much rent growth is needed
        just to break even?

    Because the answer is driven by the discount rate (the owner's required
    return, which is private) and by the exit cap rate (which no government body
    publishes), the tables are published as sensitivity ranges, not point
    estimates.

INPUTS (all disclosed, none measured for this asset)
    cap_now      cap rate at which the asset would sell today      swept 5.0-6.5%
    cap_exit     cap rate applied to rent at the end of the horizon swept 5.0-6.5%
    growth       annual growth in contractual base rent             swept 0-3%
    discount     owner's required return                            swept 4.88-9%
    horizon      years from now to the end of the lease            10 (2035, latest reported expiry)
    vacancy      months of rent loss at/after expiry                0 or 18

    The only externally sourced anchor is the discount-rate floor: the 10-year
    Treasury constant-maturity yield of 4.88% on 2026-11-09 (Federal Reserve H.15
    via FRED, series DGS10). It is a market rate, not the owner's required return.

EXCLUDED AND DISCLOSED
    Transaction costs, transfer taxes (0.45% city base tax and Measure ULA 4%/5.5%
    for City of Los Angeles closings), federal and California income tax on the
    gain, depreciation recapture at up to 25%, capital expenditure, insurance
    repricing, financing and the risk of tenant default before expiry. Each of
    those is a verified rule or a private fact, not something this module can
    assume. They are listed on the page so the reader can apply them.

DETERMINISM
    No network, no clock, no randomness, no floating-point accumulation across
    runs. Calling compute() twice returns equal output.
"""

from __future__ import annotations

HORIZON_YEARS = 10
TREASURY_ANCHOR = 0.0488          # 10-year constant maturity, 2026-11-09, FRED DGS10
TREASURY_ANCHOR_DATE = "2026-11-09"

CAP_RATES = (0.050, 0.055, 0.060, 0.065)
GROWTH_RATES = (0.000, 0.010, 0.020, 0.030)
DISCOUNT_RATES = (0.0488, 0.060, 0.070, 0.090)
BASE_CAP_NOW = 0.055
VACANCY_MONTHS = 18
RELEASE_RENT_FACTOR = 0.90        # re-letting at 90% of the prior rent


def _pv_rent_stream(growth: float, discount: float, years: int = HORIZON_YEARS) -> float:
    """Present value of years 1..N of rent, paid in arrears, growing annually."""
    return sum((1.0 + growth) ** (t - 1) / (1.0 + discount) ** t for t in range(1, years + 1))


def hold_pv(growth: float, discount: float, cap_exit: float,
            vacancy_months: int = 0) -> float:
    """Present value of holding, in multiples of one year's rent (1 R).

    Rent accrues for the full horizon; the asset is sold at the end of year N at
    `cap_exit` applied to the then-current rent. If `vacancy_months` > 0, the final
    years of rent are interrupted for that many months and the asset is re-let at
    RELEASE_RENT_FACTOR of the prior rent before the exit.
    """
    pv = _pv_rent_stream(growth, discount)
    exit_rent = (1.0 + growth) ** HORIZON_YEARS
    if vacancy_months:
        years_of_vacancy = vacancy_months / 12.0
        pv -= exit_rent / (1.0 + discount) ** HORIZON_YEARS * years_of_vacancy / (1.0 + growth)
        exit_rent *= RELEASE_RENT_FACTOR
    pv += exit_rent / cap_exit / (1.0 + discount) ** HORIZON_YEARS
    return pv


def sell_now_multiple(cap_now: float) -> float:
    """Proceeds of selling today, in multiples of one year's rent, before costs and tax."""
    return 1.0 / cap_now


def break_even_growth(cap_now: float, cap_exit: float, discount: float,
                      vacancy_months: int = 0) -> float | None:
    """Rent growth at which holding equals selling today.

    Bisection over a wide bracket; returns None when no positive finite root
    exists inside the bracket (i.e. the comparison cannot be closed by growth).
    """
    target = sell_now_multiple(cap_now)
    lo, hi = -0.50, 0.50
    f_lo = hold_pv(lo, discount, cap_exit, vacancy_months) - target
    f_hi = hold_pv(hi, discount, cap_exit, vacancy_months) - target
    if f_lo > 0 or f_hi < 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2.0
        f_mid = hold_pv(mid, discount, cap_exit, vacancy_months) - target
        if f_mid > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0


def ratio_grid() -> list[dict]:
    """PV(hold) / PV(sell today) for every cap x growth x discount combination."""
    rows = []
    for cap_exit in CAP_RATES:
        for growth in GROWTH_RATES:
            row = {"cap_exit": cap_exit, "growth": growth, "values": []}
            for discount in DISCOUNT_RATES:
                pv = hold_pv(growth, discount, cap_exit)
                row["values"].append({
                    "discount": discount,
                    "ratio": pv / sell_now_multiple(BASE_CAP_NOW),
                })
            rows.append(row)
    return rows


def break_even_table() -> list[dict]:
    """Break-even rent growth by exit cap and discount rate, at the base cap rate."""
    rows = []
    for discount in DISCOUNT_RATES:
        row = {"discount": discount, "values": []}
        for cap_exit in CAP_RATES:
            g = break_even_growth(BASE_CAP_NOW, cap_exit, discount)
            row["values"].append({"cap_exit": cap_exit, "growth": g})
        rows.append(row)
    return rows


def vacancy_scenario() -> dict:
    """What an 18-month void at expiry does to the same comparison."""
    out = []
    for cap_exit in CAP_RATES:
        base = hold_pv(0.01, TREASURY_ANCHOR, cap_exit)
        stressed = hold_pv(0.01, TREASURY_ANCHOR, cap_exit, VACANCY_MONTHS)
        out.append({
            "cap_exit": cap_exit,
            "with_rent": base,
            "with_vacancy": stressed,
            "loss_pct": (base - stressed) / base,
        })
    return {
        "vacancy_months": VACANCY_MONTHS,
        "release_rent_factor": RELEASE_RENT_FACTOR,
        "rows": out,
    }


def compute() -> dict:
    return {
        "horizon_years": HORIZON_YEARS,
        "base_cap_now": BASE_CAP_NOW,
        "treasury_anchor": TREASURY_ANCHOR,
        "treasury_anchor_date": TREASURY_ANCHOR_DATE,
        "ratio_grid": ratio_grid(),
        "break_even": break_even_table(),
        "vacancy": vacancy_scenario(),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(compute(), indent=2))
