"""Projection and decision model.

DESIGN PRINCIPLE -- WHY EVERYTHING IS NORMALISED TO "R"
=======================================================
The owner's actual lease economics (current base rent, escalation schedule,
building size, lot size, basis, remaining term) were never supplied to this
project, and under the privacy directive no property-specific figures are
invented.  Rather than fabricate inputs, the model is written in units of

        R  =  one year of the property's CURRENT contractual base rent

Every output is therefore a dimensionless multiple of R (or of the property's
current capitalised value).  That has three consequences:

  1. Nothing is fabricated.  No rent level, price, basis or NOI is asserted.
  2. The model is still fully decision-useful.  Because sell-vs-hold is a
     comparison of two cash-flow streams from the SAME asset, the rent level
     cancels out of the ranking in most cases.  The owner reads the answer as
     "Strategy X returns 14.8 R versus Strategy Y at 12.1 R" and can multiply
     by their own actual rent in private.
  3. Every assumption is explicit, named and adjustable, and the outputs are
     reported as sensitivity grids rather than single point estimates.

Rates that ARE anchored to official published data are cited.  Rates that are
pure analytical judgement are labelled "ASSUMPTION" and are swept across a
range so the conclusion does not rest on any one of them.

Run:  python3 -m model.projection
"""

from __future__ import annotations

# --------------------------------------------------------------------------
# 1. OFFICIAL ANCHORS (verified values, with sources)
# --------------------------------------------------------------------------

# U.S. Department of the Treasury, Daily Treasury Par Yield Curve Rates,
# January 2026 observations read directly from treasury.gov.
# https://home.treasury.gov/resource-center/data-chart-center/interest-rates/
#   TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026
TREASURY_PAR_YIELD_JAN_2026 = {
    "1 Yr": 3.47, "2 Yr": 3.47, "3 Yr": 3.55, "5 Yr": 3.74, "7 Yr": 3.95,
    "10 Yr": 4.19, "20 Yr": 4.81, "30 Yr": 4.86,
    "_date_read": "2026-01-02",
    "_source": "U.S. Department of the Treasury",
    "_url": ("https://home.treasury.gov/resource-center/data-chart-center/"
             "interest-rates/TextView?type=daily_treasury_yield_curve"
             "&field_tdr_date_value=2026"),
}
TREASURY_10Y_JAN_2026 = TREASURY_PAR_YIELD_JAN_2026["10 Yr"]
TREASURY_20Y_JAN_2026 = TREASURY_PAR_YIELD_JAN_2026["20 Yr"]

# U.S. BLS, Los Angeles Area Economic Summary, updated 2026-10-05.
# https://www.bls.gov/regions/west/summary/blssummary_losangeles.pdf
BLS_LA_CPI_ALL_ITEMS_AUG2026 = 3.6      # 12-month % change, LA metro
BLS_LA_CPI_FOOD_AUG2026 = 2.8           # 12-month % change, LA metro
BLS_LA_ECI_JUN2026 = 2.8                # 12-month % change, LA-Long Beach CSA
BLS_LA_NONFARM_YOY_AUG2026 = 0.6        # %
BLS_LA_LEISURE_HOSP_YOY_AUG2026 = 2.2   # %
BLS_LA_UNEMPLOY_AUG2026 = 4.8           # LA metro, %
BLS_LA_COUNTY_UNEMPLOY_AUG2026 = 4.9    # LA County, %
BLS_LA_CITY_UNEMPLOY_AUG2026 = 5.0      # LA City, %

# U.S. Census Bureau QuickFacts (V2025 population estimates; ACS 2020-2024).
CENSUS_LA_COUNTY_POP_2025 = 9_694_934
CENSUS_LA_COUNTY_POP_2020_BASE = 10_017_414
CENSUS_LA_COUNTY_POP_CHANGE_PCT = -3.2
CENSUS_LA_CITY_POP_2025 = 3_869_089
CENSUS_LA_CITY_POP_CHANGE_PCT = -0.8

# SEC filings, Jack in the Box Inc.
JIB_SSS_SYSTEM_FY2025 = -4.2            # FY2025 system same-store sales, %
JIB_SSS_SYSTEM_Q3FY2026 = -1.1          # Q3 FY2026 system same-store sales, %
JIB_UNITS_FY2025_END = 2_136
JIB_UNITS_Q3FY2026 = 2_115
JIB_CLOSURES_TARGET_LOW = 150
JIB_CLOSURES_TARGET_HIGH = 200

# --------------------------------------------------------------------------
# 2. ASSUMPTIONS (analytical judgement -- explicitly NOT verified data)
# --------------------------------------------------------------------------
# Each assumption carries a low / base / high value.  Conclusions are reported
# across the whole range so nothing rests on a single guessed number.

# `fav` states which extreme is FAVOURABLE to the owner:
#   "high" -> the high value is the good outcome (e.g. replacement rent ratio)
#   "low"  -> the low value is the good outcome  (e.g. exit cap rate)
# Without this, an "optimistic" scenario would silently mix optimistic and
# pessimistic inputs, which is the most common way a sensitivity grid lies.
ASSUMPTIONS = {
    # Capitalisation rate for a single-tenant NNN Jack in the Box in an urban
    # California infill location.  NO U.S. GOVERNMENT AGENCY PUBLISHES
    # COMMERCIAL CAP RATES.  Private-transaction pricing is not official data.
    # The range below is therefore an explicit modelling input, swept wide,
    # and flagged on the Flagged for Review page.
    "exit_cap_rate": dict(low=0.050, base=0.065, high=0.085, unit="decimal",
                          fav="low", status="ASSUMPTION - NO OFFICIAL SOURCE"),
    "today_cap_rate": dict(low=0.050, base=0.0625, high=0.080, unit="decimal",
                           fav="low", status="ASSUMPTION - NO OFFICIAL SOURCE"),
    # Vacancy / downtime between the tenant leaving and a replacement occupier
    # paying rent.  Single-tenant restaurant boxes are slow to re-let.
    "relet_downtime_years": dict(low=0.5, base=1.5, high=3.0, unit="years",
                                 fav="low", status="ASSUMPTION"),
    # Re-tenanting capital: demolition or adaptation of a drive-thru box,
    # plus leasing commissions and tenant improvements, expressed in years of
    # current base rent (keeps the model dimensionless).
    "relet_capex_in_R": dict(low=0.5, base=1.5, high=3.0, unit="R",
                             fav="low", status="ASSUMPTION"),
    # Rent achieved by a replacement occupier relative to the current JIB rent.
    "relet_rent_ratio": dict(low=0.70, base=0.95, high=1.15, unit="ratio",
                             fav="high", status="ASSUMPTION"),
    # Value of the land plus box repurposed to a non-Jack-in-the-Box use,
    # net of all conversion cost, in units of R.  Highly site-specific.
    "alternative_use_value_in_R": dict(low=8.0, base=13.0, high=20.0,
                                       unit="R", fav="high",
                                       status="ASSUMPTION"),
    # Transaction friction on a sale: broker commission, legal, transfer tax,
    # and any lender exit costs.
    "sale_friction_pct": dict(low=0.02, base=0.045, high=0.07, unit="decimal",
                              fav="low", status="ASSUMPTION"),
    # Probability the tenant does NOT renew / does NOT extend at expiry, given
    # the disclosed closure programme.  Derived qualitatively from the SEC
    # filings (see risk register) but the number itself is judgement.
    "p_non_renewal": dict(low=0.25, base=0.45, high=0.70, unit="probability",
                          fav="low",
                          status="ASSUMPTION - judgement anchored to SEC disclosures"),
    # Probability of a value-destroying local catastrophe inside the hold
    # window.  Anchored to USGS 30-year probabilities (see below) but the
    # per-window figure is a modelling conversion.
    "p_black_swan_10y": dict(low=0.02, base=0.06, high=0.15, unit="probability",
                             fav="low",
                             status="ASSUMPTION - anchored to USGS/CAL FIRE data"),
    # Loss given a black-swan event: share of asset value lost net of
    # insurance recovery.
    "black_swan_loss_share": dict(low=0.15, base=0.40, high=0.90, unit="decimal",
                                  fav="low", status="ASSUMPTION"),
    # Discount rate.  Built from the VERIFIED official Treasury curve plus a
    # risk premium that is itself an assumption.
    "risk_premium_pct": dict(low=0.020, base=0.035, high=0.055, unit="decimal",
                             fav="low",
                             status="ASSUMPTION - premium over the official Treasury rate"),
    # Contractual rent escalation inside the remaining term.
    "rent_escalation_pct": dict(low=0.00, base=0.02, high=0.10, unit="decimal",
                                fav="high",
                                status="ASSUMPTION - INPUT REQUIRED from the lease"),
    # Rent concession given to the tenant to purchase an early extension.
    "extension_concession_pct": dict(low=0.00, base=0.06, high=0.15,
                                     unit="decimal", fav="low",
                                     status="ASSUMPTION"),
    # Cap-rate compression achieved by lengthening the remaining term.
    "extension_cap_compression": dict(low=0.00, base=0.08, high=0.15,
                                      unit="decimal of cap rate", fav="high",
                                      status="ASSUMPTION"),
}

# Scenario names used everywhere on the site.
SCENARIOS = ["optimistic", "base", "pessimistic"]


def A(name: str, scenario: str = "base") -> float:
    """Resolve an assumption for a scenario, respecting its favourable side."""
    a = ASSUMPTIONS[name]
    if scenario == "base":
        return a["base"]
    if scenario == "optimistic":
        return a["high"] if a["fav"] == "high" else a["low"]
    if scenario == "pessimistic":
        return a["low"] if a["fav"] == "high" else a["high"]
    raise ValueError(scenario)


def discount_rate(scenario: str = "base") -> float:
    """Official Treasury 10-year par yield + assumed risk premium."""
    return TREASURY_10Y_JAN_2026 / 100.0 + A("risk_premium_pct", scenario)


# --------------------------------------------------------------------------
# 3. STRATEGY CASH-FLOW ENGINE  (all values in units of R)
# --------------------------------------------------------------------------

QUARTER = 0.25


def _vacancy_loss(t, downtime_years, ratio, rate):
    """PV of rent foregone while the box stands empty, in units of R.

    Charged in quarters at the replacement rent level (ratio * QUARTER per
    quarter), so total nominal loss equals ratio * downtime_years exactly.
    """
    quarters = max(0, int(round(downtime_years / QUARTER)))
    return -sum((ratio * QUARTER) / (1.0 + rate) ** (t + (i + 1) * QUARTER)
                for i in range(quarters))

def _pv(stream, rate):
    """Present value of [(year, amount_in_R), ...] discounted at `rate`."""
    return sum(amt / (1.0 + rate) ** yr for yr, amt in stream)


def strategy_sell_now(hold_years=0, scenario="base"):
    """Sell the asset today, with the Jack in the Box lease in place.

    Buyer prices it off in-place NOI.  A short remaining term widens the cap
    rate a buyer demands, so the model prices today's sale at the "today" cap
    rate and a sale at expiry at the "exit" cap rate.
    """
    cap = A("today_cap_rate", scenario)
    friction = A("sale_friction_pct", scenario)
    gross = 1.0 / cap                      # one year of rent capitalised
    net = gross * (1.0 - friction)
    return dict(name="S1 - Sell now, lease in place",
                pv_R=net, gross_R=gross, notes="Immediate liquidity; no re-letting or rollover risk.")


def strategy_sell_at_expiry(expiry_years, scenario="base"):
    """Hold to lease expiry collecting rent, then sell with the box vacant."""
    rate = discount_rate(scenario)
    esc = A("rent_escalation_pct", scenario)
    friction = A("sale_friction_pct", scenario)
    cap = A("exit_cap_rate", scenario)
    alt = A("alternative_use_value_in_R", scenario)
    stream = [(y, (1.0 + esc) ** (y - 1)) for y in range(1, expiry_years + 1)]
    rent_pv = _pv(stream, rate)
    # Terminal: sold as a vacant box / land.  Value is the lower of a
    # capitalised replacement rent and the alternative-use value.
    terminal = min(1.0 / cap, alt) * (1.0 - friction)
    terminal_pv = terminal / (1.0 + rate) ** expiry_years
    return dict(name=f"S2 - Hold to expiry (+{expiry_years}y), then sell vacant",
                pv_R=rent_pv + terminal_pv,
                rent_pv_R=rent_pv, terminal_pv_R=terminal_pv,
                notes="Full rent to expiry; terminal value carries all the location risk.")


def strategy_renew(expiry_years, scenario="base"):
    """Hold to expiry, then re-let to Jack in the Box on a new long term."""
    rate = discount_rate(scenario)
    esc = A("rent_escalation_pct", scenario)
    downtime = A("relet_downtime_years", scenario)
    capex = A("relet_capex_in_R", scenario)
    ratio = A("relet_rent_ratio", scenario)
    cap = A("exit_cap_rate", scenario)
    stream = [(y, (1.0 + esc) ** (y - 1)) for y in range(1, expiry_years + 1)]
    rent_pv = _pv(stream, rate)
    t = expiry_years
    # Capital cost of making the box re-lettable (remodel / reimage).
    capex_pv = capex / (1.0 + rate) ** t
    # Vacancy during re-letting.
    vacancy_pv = _vacancy_loss(t, downtime, ratio, rate)
    # Re-let income, valued in perpetuity at the exit cap rate, discounted back.
    new_noi = ratio * (1.0 + esc) ** t
    perpetuity = new_noi / cap
    perpv = perpetuity / (1.0 + rate) ** (t + downtime)
    return dict(name=f"S3 - Renew / re-let to Jack in the Box (+{expiry_years}y)",
                pv_R=rent_pv - capex_pv + vacancy_pv + perpv,
                rent_pv_R=rent_pv, capex_pv_R=capex_pv,
                vacancy_pv_R=vacancy_pv, relet_pv_R=perpv,
                notes="Keeps the income stream; requires tenant credit to survive to expiry.")


def strategy_replacement_tenant(expiry_years, scenario="base"):
    """Hold to expiry, then re-let the box to a DIFFERENT operator."""
    rate = discount_rate(scenario)
    esc = A("rent_escalation_pct", scenario)
    downtime = A("relet_downtime_years", scenario) * 1.3   # non-branded box is harder
    capex = A("relet_capex_in_R", scenario) * 1.4          # more adaptation work
    ratio = A("relet_rent_ratio", scenario)
    cap = A("exit_cap_rate", scenario)
    stream = [(y, (1.0 + esc) ** (y - 1)) for y in range(1, expiry_years + 1)]
    rent_pv = _pv(stream, rate)
    t = expiry_years
    capex_pv = capex / (1.0 + rate) ** t
    vacancy_pv = _vacancy_loss(t, downtime, ratio, rate)
    new_noi = ratio * (1.0 + esc) ** t
    perpv = (new_noi / cap) / (1.0 + rate) ** (t + downtime)
    return dict(name=f"S4 - Hold to expiry, re-let to another operator (+{expiry_years}y)",
                pv_R=rent_pv - capex_pv + vacancy_pv + perpv,
                notes="Removes Jack in the Box credit risk; adds re-tenanting risk.")


def strategy_sale_leaseback_now(scenario="base"):
    """Negotiate an early lease extension with the tenant, then sell.

    A longer remaining term compresses the cap rate a buyer demands.  Modelled
    as a sale priced between S1 and a fully-extended asset, with the tenant
    taking a rent concession to secure the extension.
    """
    compression = A("extension_cap_compression", scenario)
    cap = A("today_cap_rate", scenario) * (1.0 - compression)  # longer term -> tighter cap
    friction = A("sale_friction_pct", scenario)
    concession = A("extension_concession_pct", scenario)
    gross = (1.0 - concession) / cap
    return dict(name="S5 - Extend early, then sell the lengthened lease",
                pv_R=gross * (1.0 - friction), gross_R=gross,
                notes="Buys term before selling; costs a rent concession; depends entirely on tenant willingness.")


def strategy_redevelop(expiry_years, scenario="base"):
    """Hold to expiry, then clear the site for a higher-and-better use."""
    rate = discount_rate(scenario)
    esc = A("rent_escalation_pct", scenario)
    alt = A("alternative_use_value_in_R", scenario)
    stream = [(y, (1.0 + esc) ** (y - 1)) for y in range(1, expiry_years + 1)]
    rent_pv = _pv(stream, rate)
    t = expiry_years
    terminal_pv = alt / (1.0 + rate) ** t
    return dict(name=f"S6 - Hold to expiry, then redevelop the site (+{expiry_years}y)",
                pv_R=rent_pv + terminal_pv,
                notes="Maximum upside, maximum entitlement/execution risk; needs the land to support a better use.")


# --------------------------------------------------------------------------
# 4. RISK ADJUSTMENT
# --------------------------------------------------------------------------

def apply_black_swan(pv_R, years, scenario="base"):
    """Subtract the expected loss from a value-destroying local catastrophe."""
    p10 = A("p_black_swan_10y", scenario)
    p = 1.0 - (1.0 - p10) ** (years / 10.0)
    loss = A("black_swan_loss_share", scenario)
    return pv_R - p * loss * pv_R, p


def tenant_survival_adjust(pv_R, scenario="base"):
    """Weight the renewal-dependent strategies by the probability the tenant
    is still trading and still wants the site at expiry."""
    p = 1.0 - A("p_non_renewal", scenario)
    return pv_R * p, p


# --------------------------------------------------------------------------
# 5. RUNNER
# --------------------------------------------------------------------------

EXPIRY_CASES = {"2030 (4 years out)": 4, "2032 (mid-window)": 6, "2035 (9 years out)": 9}
CASES = [SCENARIOS]


def run(scenario="base"):
    rate = discount_rate(scenario)
    out = []
    out.append(strategy_sell_now(scenario=scenario))
    out.append(strategy_sale_leaseback_now(scenario=scenario))
    for label, yrs in EXPIRY_CASES.items():
        s = strategy_renew(yrs, scenario=scenario)
        adj, p = tenant_survival_adjust(s["pv_R"], scenario=scenario)
        bs, pb = apply_black_swan(adj, yrs, scenario=scenario)
        s["label"] = label
        s["risk_adjusted_pv_R"] = bs
        s["p_tenant_survives"] = p
        s["p_black_swan"] = pb
        out.append(s)
    for label, yrs in EXPIRY_CASES.items():
        s = strategy_sell_at_expiry(yrs, scenario=scenario)
        bs, pb = apply_black_swan(s["pv_R"], yrs, scenario=scenario)
        s["label"] = label
        s["risk_adjusted_pv_R"] = bs
        s["p_black_swan"] = pb
        out.append(s)
    for label, yrs in EXPIRY_CASES.items():
        s = strategy_replacement_tenant(yrs, scenario=scenario)
        bs, pb = apply_black_swan(s["pv_R"], yrs, scenario=scenario)
        s["label"] = label
        s["risk_adjusted_pv_R"] = bs
        s["p_black_swan"] = pb
        out.append(s)
    for label, yrs in EXPIRY_CASES.items():
        s = strategy_redevelop(yrs, scenario=scenario)
        bs, pb = apply_black_swan(s["pv_R"], yrs, scenario=scenario)
        s["label"] = label
        s["risk_adjusted_pv_R"] = bs
        s["p_black_swan"] = pb
        out.append(s)
    return rate, out


def summary_table():
    rows = []
    for scenario in SCENARIOS:
        rate, results = run(scenario)
        for r in results:
            rows.append(dict(
                scenario=scenario,
                discount_rate=round(rate * 100, 2),
                strategy=r["name"],
                expiry=r.get("label", "n/a"),
                pv_R=round(r["pv_R"], 2),
                risk_adjusted_pv_R=round(r.get("risk_adjusted_pv_R", r["pv_R"]), 2),
            ))
    return rows


if __name__ == "__main__":
    print("Discount rate anchor: U.S. Treasury 10-yr par yield 2026-01-02 = "
          f"{TREASURY_10Y_JAN_2026}%  (official)")
    for scenario in SCENARIOS:
        rate, results = run(scenario)
        print(f"\n=== {scenario.upper()} ===  |  discount rate {rate*100:.2f}% ===")
        for r in sorted(results, key=lambda x: -x.get("risk_adjusted_pv_R", x["pv_R"])):
            ra = r.get("risk_adjusted_pv_R", r["pv_R"])
            print(f"  {ra:8.2f} R   {r['name']}"
                  + (f"   [{r.get('label')}]" if r.get("label") else ""))


# --------------------------------------------------------------------------
# 6. ROBUSTNESS: does the ranking survive the assumptions?
# --------------------------------------------------------------------------
# A recommendation that only holds under one set of guesses is not a
# recommendation.  Two tests are reported on the site:
#   (a) rank stability - where does each strategy place in each scenario?
#   (b) worst-case rank  - the single most important number: the worst place
#       a strategy can finish.  This is what "manageable level of risk" means
#       operationally.

def ranked(scenario):
    _, results = run(scenario)
    ordered = sorted(results,
                     key=lambda x: -x.get("risk_adjusted_pv_R", x["pv_R"]))
    return [(i + 1, r) for i, r in enumerate(ordered)]


def key_for(r):
    """Stable identity for a strategy across scenarios."""
    return r["name"]


def rank_stability():
    table = {}
    for sc in SCENARIOS:
        for rank, r in ranked(sc):
            k = key_for(r)
            table.setdefault(k, {})[sc] = dict(
                rank=rank,
                risk_adjusted_pv_R=round(r.get("risk_adjusted_pv_R", r["pv_R"]), 2),
                expiry=r.get("label", "-"),
            )
    rows = []
    for k, per in table.items():
        ranks = [per[sc]["rank"] for sc in SCENARIOS]
        pv = [per[sc]["risk_adjusted_pv_R"] for sc in SCENARIOS]
        rows.append(dict(
            strategy=k,
            expiry=per["base"]["expiry"],
            rank_optimistic=per["optimistic"]["rank"],
            rank_base=per["base"]["rank"],
            rank_pessimistic=per["pessimistic"]["rank"],
            worst_rank=max(ranks),
            best_rank=min(ranks),
            mean_rank=round(sum(ranks) / len(ranks), 1),
            pv_optimistic=per["optimistic"]["risk_adjusted_pv_R"],
            pv_base=per["base"]["risk_adjusted_pv_R"],
            pv_pessimistic=per["pessimistic"]["risk_adjusted_pv_R"],
            pv_min=min(pv),
            pv_spread=round(max(pv) - min(pv), 2),
        ))
    rows.sort(key=lambda r: (r["worst_rank"], r["mean_rank"]))
    return rows


# Scenario weights are an ASSUMPTION, not a verified figure.  They are stated
# openly so the reader can change them; the conclusion is also reported
# unweighted (via worst-case rank) so it never depends on the weights alone.
SCENARIO_WEIGHTS = dict(optimistic=0.25, base=0.50, pessimistic=0.25)


def expected_value():
    rows = []
    for k, per in ((r["strategy"], r) for r in rank_stability()):
        ev = sum(SCENARIO_WEIGHTS[sc] * per[f"pv_{sc}"] for sc in SCENARIOS)
        rows.append(dict(strategy=k, expiry=per["expiry"],
                         expected_pv_R=round(ev, 2),
                         worst_pv_R=per["pv_min"],
                         spread_R=per["pv_spread"]))
    rows.sort(key=lambda r: -r["expected_pv_R"])
    return rows
