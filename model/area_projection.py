#!/usr/bin/env python3
"""Deterministic, assumption-explicit horizon and break-even analytics for Jack3.

Strictly excludes unverified market cap rates, guessed renewal probabilities,
fabricated property financials, or personal tax brackets. All numerical outputs
are either:
  1. Direct official agency observations / projections (CA DOF P-2A, SCAG, BLS,
     Census, U.S. Treasury, City of Los Angeles Measure ULA & County DTT), or
  2. Exact algebraic break-even / sensitivity identities normalized to 1.00 R
     (= one year of verified current contract NOI / base rent).

Run `python3 model/area_projection.py --check` to verify all arithmetic and
print summary tables.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Verified primary-source constants (as of 2026-11-08 UTC)
# ---------------------------------------------------------------------------
UST_10Y_2026_11_06 = 0.0486          # U.S. Treasury 10Y par yield, 2026-11-06
UST_30Y_2026_11_06 = 0.0526          # U.S. Treasury 30Y par yield, 2026-11-06
FOMC_LOW = 0.0375                    # Oct 28, 2026 FOMC target lower bound
FOMC_HIGH = 0.0400                   # Oct 28, 2026 FOMC target upper bound

CENSUS_LA_CITY_2020_BASE = 3_899_342
CENSUS_LA_CITY_2025 = 3_869_089      # V2025 July 1, 2025 (-0.8% vs Apr 2020)
CENSUS_LA_COUNTY_2025 = 9_694_934    # V2025 July 1, 2025 (-3.2% vs Apr 2020)

# CA Dept. of Finance P-2A Baseline 2024 (Vintage March 2026), FIPS 06037
DOF_LA_COUNTY = {
    2025: 9_853_435,
    2026: 9_811_358,
    2030: 9_727_305,
    2035: 9_708_647,
    2040: 9_637_524,
    2050: 9_390_823,
}

# SCAG Connect SoCal 2024 Final PEIR Appendix I (LA County, in thousands)
SCAG_2024_LA_COUNTY_K = {
    "population": {2019: 10_046, 2030: 10_214, 2050: 10_793},
    "households": {2019: 3_393, 2030: 3_784, 2050: 4_155},
    "employment": {2019: 5_031, 2030: 5_277, 2050: 5_461},
}

# City of Los Angeles Transfer Taxes (effective after June 30, 2026)
CITY_BASE_PER_500 = 2.25             # $2.25 per $500 or fractional part (0.45%)
COUNTY_DTT_PER_500 = 0.55            # $0.55 per $500 or fractional part (0.11%)
ULA_T1_THRESHOLD = 5_400_000         # > $5,400,000 and < $10,900,000 -> 4.0%
ULA_T1_RATE = 0.04
ULA_T2_THRESHOLD = 10_900_000        # >= $10,900,000 -> 5.5%
ULA_T2_RATE = 0.055


@dataclass(frozen=True)
class TransferTaxRow:
    gross_price: int
    base_city_county: float
    ula_tax: float
    total_transfer_tax: float
    effective_rate: float
    net_before_brokerage: float


def compute_la_transfer_tax(price: int) -> TransferTaxRow:
    """Compute statutory City of LA + LA County transfer taxes (eff. 2026-07-01)."""
    if price <= 100:
        return TransferTaxRow(price, 0.0, 0.0, 0.0, 0.0, float(price))
    blocks = math.ceil(price / 500.0)
    base_tax = blocks * (CITY_BASE_PER_500 + COUNTY_DTT_PER_500)
    if price >= ULA_T2_THRESHOLD:
        ula_tax = price * ULA_T2_RATE
    elif price > ULA_T1_THRESHOLD:
        ula_tax = price * ULA_T1_RATE
    else:
        ula_tax = 0.0
    total = round(base_tax + ula_tax, 2)
    net = round(price - total, 2)
    return TransferTaxRow(
        gross_price=price,
        base_city_county=round(base_tax, 2),
        ula_tax=round(ula_tax, 2),
        total_transfer_tax=total,
        effective_rate=total / price,
        net_before_brokerage=net,
    )


def annuity_pv_factor(rate: float, years: int) -> float:
    """Present value of 1.00 R/yr end-of-year annuity over `years` at `rate`."""
    if rate <= 0:
        return float(years)
    return (1.0 - (1.0 + rate) ** (-years)) / rate


def breakeven_extension_cap_compression_bps(cap_rate: float, rent_cut_pct: float) -> float:
    """Exact exit cap-rate change (bps) needed to preserve gross value after rent cut.

    Identity: R / c_0 = (1 - cut) * R / (c_0 + dc) => dc = -cut * c_0.
    Reported before transaction, concession, or tax friction.
    """
    return round(-rent_cut_pct * cap_rate * 10_000, 1)


def breakeven_hold_terminal_r(net_sale_r: float, rate: float, years: int) -> float:
    """Undiscounted Year-T terminal value (in R) required for hold PV to equal net sale.

    Identity: net_sale_r = annuity_pv(rate, T) + terminal_R / (1 + rate)^T.
    """
    pv_rent = annuity_pv_factor(rate, years)
    return round((net_sale_r - pv_rent) * ((1.0 + rate) ** years), 2)


def ula_cliff_summary() -> list[TransferTaxRow]:
    """Return statutory transfer tax cliff checkpoints (effective 2026-07-01)."""
    prices = [
        5_000_000,
        5_400_000,
        5_400_500,
        5_500_000,
        5_626_500,   # lowest $500-rounded gross price recovering $5,400,000 net
        7_500_000,
        10_899_500,
        10_900_000,
        11_074_000,  # lowest $500-rounded gross price recovering $10,899,500 net
    ]
    return [compute_la_transfer_tax(p) for p in prices]


def dof_vs_scag_summary() -> dict[str, dict[str, float]]:
    """Compare official 2026->2030 and 2026->2035 LA County demographic tracks."""
    p26 = DOF_LA_COUNTY[2026]
    p30 = DOF_LA_COUNTY[2030]
    p35 = DOF_LA_COUNTY[2035]
    p50 = DOF_LA_COUNTY[2050]
    # Annualized Census V2025 LA City pace (5.25 yrs Apr 2020 -> Jul 2025)
    city_cagr = (CENSUS_LA_CITY_2025 / CENSUS_LA_CITY_2020_BASE) ** (1 / 5.25) - 1.0
    return {
        "dof_p2a": {
            "2026": p26,
            "2030": p30,
            "2035": p35,
            "2050": p50,
            "pct_2026_2030": round((p30 / p26 - 1.0) * 100, 2),
            "pct_2026_2035": round((p35 / p26 - 1.0) * 100, 2),
            "pct_2026_2050": round((p50 / p26 - 1.0) * 100, 2),
        },
        "census_city_pace": {
            "annual_pct": round(city_cagr * 100, 3),
            "extrap_4yr_pct": round(((1 + city_cagr) ** 4 - 1.0) * 100, 2),
            "extrap_9yr_pct": round(((1 + city_cagr) ** 9 - 1.0) * 100, 2),
        },
        "scag_peir_2024": {
            "pop_2019_2030_pct": round(
                (SCAG_2024_LA_COUNTY_K["population"][2030]
                 / SCAG_2024_LA_COUNTY_K["population"][2019] - 1.0) * 100, 2
            ),
            "hh_2019_2030_pct": round(
                (SCAG_2024_LA_COUNTY_K["households"][2030]
                 / SCAG_2024_LA_COUNTY_K["households"][2019] - 1.0) * 100, 2
            ),
            "jobs_2019_2030_pct": round(
                (SCAG_2024_LA_COUNTY_K["employment"][2030]
                 / SCAG_2024_LA_COUNTY_K["employment"][2019] - 1.0) * 100, 2
            ),
        },
    }


def run_checks() -> None:
    """Assert mathematical identities, monotonicity, and cliff arithmetic."""
    # 1. Measure ULA dead zones
    r_5400 = compute_la_transfer_tax(5_400_000)
    r_5400_5 = compute_la_transfer_tax(5_400_500)
    r_5626_5 = compute_la_transfer_tax(5_626_500)
    assert math.isclose(r_5400.net_before_brokerage, 5_369_760.00)
    assert r_5400_5.net_before_brokerage < r_5400.net_before_brokerage
    assert r_5626_5.net_before_brokerage >= r_5400.net_before_brokerage

    r_10899_5 = compute_la_transfer_tax(10_899_500)
    r_10900 = compute_la_transfer_tax(10_900_000)
    r_11074 = compute_la_transfer_tax(11_074_000)
    assert r_10900.net_before_brokerage < r_10899_5.net_before_brokerage
    assert r_11074.net_before_brokerage >= r_10899_5.net_before_brokerage

    # 2. Algebraic cap-rate & extension break-even identities
    for cap in (0.060, 0.070, 0.075, 0.080):
        for cut in (0.05, 0.10):
            dc_bps = breakeven_extension_cap_compression_bps(cap, cut)
            new_cap = cap + dc_bps / 10_000.0
            assert math.isclose(1.0 / cap, (1.0 - cut) / new_cap, rel_tol=1e-3)

    # 3. Discounted hold break-even identity
    r_low = UST_10Y_2026_11_06 + 0.0200   # 6.86%
    r_high = UST_10Y_2026_11_06 + 0.0300  # 7.86%
    for T in (4, 9):
        pv_low = annuity_pv_factor(r_low, T)
        pv_high = annuity_pv_factor(r_high, T)
        assert pv_high < pv_low < T
        term_r = breakeven_hold_terminal_r(14.0, r_low, T)
        pv_reconstruct = pv_low + term_r / ((1 + r_low) ** T)
        assert math.isclose(pv_reconstruct, 14.0, abs_tol=0.02)

    # 4. DOF directional decline vs SCAG 2024 PEIR growth
    s = dof_vs_scag_summary()
    assert s["dof_p2a"]["pct_2026_2030"] < 0
    assert s["dof_p2a"]["pct_2026_2035"] < 0
    assert s["scag_peir_2024"]["pop_2019_2030_pct"] > 0


def print_summary() -> None:
    s = dof_vs_scag_summary()
    print("=== Official Horizon Comparison (LA County / City) ===")
    print(f"CA DOF P-2A (2026->2030 / 2035 / 2050): "
          f"{s['dof_p2a']['pct_2026_2030']}% / {s['dof_p2a']['pct_2026_2035']}% / {s['dof_p2a']['pct_2026_2050']}%")
    print(f"SCAG Connect SoCal 2024 PEIR (2019->2030): "
          f"pop +{s['scag_peir_2024']['pop_2019_2030_pct']}%, "
          f"HH +{s['scag_peir_2024']['hh_2019_2030_pct']}%, "
          f"jobs +{s['scag_peir_2024']['jobs_2019_2030_pct']}%")
    print("\n=== City of LA Transfer Tax + Measure ULA Cliff (Eff. 2026-07-01) ===")
    for row in ula_cliff_summary():
        print(f"  ${row.gross_price:>10,d} | tax ${row.total_transfer_tax:>10,.2f} ({row.effective_rate*100:5.3f}%) | net ${row.net_before_brokerage:>11,.2f}")
    print("\n=== Algebraic Cap-Rate & Break-Even Sweep (1.00 R Unit-Rent Basis) ===")
    for cap in (0.055, 0.060, 0.065, 0.070, 0.075, 0.080, 0.085):
        mult = 1.0 / cap
        sp = (cap - UST_10Y_2026_11_06) * 10_000
        dc5 = breakeven_extension_cap_compression_bps(cap, 0.05)
        dc10 = breakeven_extension_cap_compression_bps(cap, 0.10)
        print(f"  Cap {cap*100:4.2f}% (+{sp:3.0f} bps vs UST) | Multiple {mult:5.2f} R | "
              f"BE compress (-5%/-10% rent): {dc5:+.0f} / {dc10:+.0f} bps")
    print("\n=== Hold-to-Expiry Break-Even Terminal Value (Illustrative 14.00 R Net Sale Today) ===")
    for name, r in (("UST+200 bps (6.86%)", 0.0686), ("UST+300 bps (7.86%)", 0.0786)):
        for T, yr in ((4, 2030), (9, 2035)):
            pv_r = annuity_pv_factor(r, T)
            term = breakeven_hold_terminal_r(14.0, r, T)
            print(f"  {yr} ({T} yr) @ {name}: PV(rent) = {pv_r:5.2f} R -> Required Year-{T} value = {term:5.2f} R")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Run arithmetic integrity assertions")
    args = parser.parse_args()
    if args.check:
        run_checks()
        print("AREA PROJECTION CHECKS PASSED.")
    print_summary()
