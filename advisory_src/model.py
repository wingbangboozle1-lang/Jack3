"""Deterministic Area Economic & NNN Property Projection System (2026–2035).

Session: e04af39b (arena/e04af39b-jack3)

DESIGN PRINCIPLES:
- Zero invented parcel numbers: because contractual rent, exact expiry year within
  2030–2035, lease guarantor, and tax basis are private/unsupplied, all property
  valuations are normalized to `1.00 R` (= 1 year of current contractual base rent),
  and exact parcel dollar forecasts are left strictly blank on Flagged/Profile rows.
- Symmetric present-value accounting: every strategy is evaluated at t=0 present
  value using a consistent discount rate anchored to the verified Nov 6, 2026
  10-Year U.S. Treasury par yield (4.86%, Source S11) plus an explicit real-estate
  risk premium. Sale pathways value net redeployed proceeds at par present value
  (zero artificial reinvestment alpha), isolating true economic drivers:
  (1) remaining-term cap-rate pricing, (2) renewal vs. dark-box vacancy/TI costs,
  (3) IRC §1031 deferral vs. taxable sale leakage, (4) Measure ULA cliffs, and
  (5) cumulative seismic/wildfire/insurance tail exposure while holding the parcel.
- Every generated row carries a valid official Source ID (`S01`..`S37`) and status
  `Analysis` (never `Verified`, which is reserved strictly for direct official facts).
"""

from __future__ import annotations

# Verified Nov 6, 2026 10-Yr U.S. Treasury Par Yield (Source S11)
UST_10Y_ANCHOR = 0.0486


def build_area_economic_projections() -> list[dict]:
    """Central LA / LA Basin 2026–2035 Macroeconomic Regime Projections (Sources S01, S02, S03, S08, S11, S31, S32, S35)."""
    # Compound 9-year changes (2026 -> 2035) from verified baselines
    regimes = [
        {
            "regime": "Downside / Out-Migration & Margin Stress",
            "pop_cagr": -0.0045,       # Closer to CA DOF county decline / V2025 county (-0.62%/yr)
            "jobs_cagr": -0.0010,      # Mild contraction (Information/Mfg drag outweighs healthcare)
            "qsr_cost_cagr": 0.0420,   # Sticky CPI/energy + post-2026 wage indexing
            "ust10_2030_35": "5.25% – 5.75%",
            "qsr_demand_idx_2035": "",
            "implication": " shrinking local headcount + 4.2%/yr cost inflation squeezes unit EBITDAR; high non-renewal risk at 2030–2035 expiry.",
            "source": "S35",
        },
        {
            "regime": "Measured-Trend Base Case (Anchored to V2025 & Sept 2026 BLS)",
            "pop_cagr": -0.0016,       # Exact LA City V2025 annualized pace (-0.8% over 5.25 yrs)
            "jobs_cagr": 0.0050,       # Exact Sept 2026 BLS LA Metro nonfarm YoY (+0.5%)
            "qsr_cost_cagr": 0.0350,   # Anchored to Sept 2026 LA CPI-U (+3.7%) & ECI (+3.9%) moderating slightly
            "ust10_2030_35": "4.50% – 5.00%",
            "qsr_demand_idx_2035": "",
            "implication": "Flat-to-slightly-lower resident count (-1.4% by 2035) offset by +4.6% cumulative payrolls; real QSR rent growth capped near 0%–1.5%/yr.",
            "source": "S03",
        },
        {
            "regime": "Transit / LA28 Olympic & DTLA 2040 Infill Upside",
            "pop_cagr": 0.0035,        # Central-core transit corridor capture (D Line opened May 2026 + DTLA 2040)
            "jobs_cagr": 0.0120,       # Hospitality/tourism + healthcare + Olympic infrastructure lift
            "qsr_cost_cagr": 0.0280,   # Disinflation toward Fed 2% target eases margin squeeze
            "ust10_2030_35": "3.75% – 4.25%",
            "qsr_demand_idx_2035": "",
            "implication": "Corridor densification (+3.2% pop, +11.3% jobs by 2035) lifts underlying mixed-use land value even more than drive-thru rent.",
            "source": "S32",
        },
    ]
    rows = []
    for r in regimes:
        pop_9y = (1.0 + r["pop_cagr"]) ** 9 - 1.0
        job_9y = (1.0 + r["jobs_cagr"]) ** 9 - 1.0
        cost_9y = (1.0 + r["qsr_cost_cagr"]) ** 9 - 1.0
        rows.append({
            "regime": r["regime"],
            "pop_2026_2035": f"{r['pop_cagr']*100:+.2f}%/yr ({pop_9y*100:+.1f}% cum.)",
            "jobs_2026_2035": f"{r['jobs_cagr']*100:+.2f}%/yr ({job_9y*100:+.1f}% cum.)",
            "cost_2026_2035": f"{r['qsr_cost_cagr']*100:+.2f}%/yr ({cost_9y*100:+.1f}% cum.)",
            "rate_env": r["ust10_2030_35"],
            "implication": r["implication"].strip(),
            "status": "Analysis",
            "source": r["source"],
        })
    return rows


def pv_growing_annuity(first_cf: float, g: float, k: float, n: int) -> float:
    """Present value of n annual end-of-year cash flows starting at first_cf growing at g."""
    if n <= 0:
        return 0.0
    total = 0.0
    for t in range(1, n + 1):
        cf = first_cf * ((1.0 + g) ** (t - 1))
        total += cf / ((1.0 + k) ** t)
    return total


def evaluate_pathways() -> list[dict]:
    """Symmetric Present-Value comparison (in multiples of current annual base rent `R`)
    across 5 owner decision pathways, 2 expiry bookends (2030 = 4 yrs; 2035 = 9 yrs),
    and 4 scenario regimes (Optimistic, Base, Downside, Black-Swan Tail Stress).
    """
    scenarios = {
        "opt": {
            "k": 0.0625,                  # 4.86% UST + 139 bps premium
            "g_in_place": 0.0175,         # ~1.75%/yr contractual bump
            "cap_long_ext": 0.0565,       # Fresh 12–15 yr extended NNN cap rate
            "cap_mid_term": 0.0600,       # 7–8 yr remaining NNN cap rate
            "cap_short_term": 0.0685,     # 3–4 yr short-fuse NNN cap rate
            "cap_relet": 0.0585,          # Re-let / repositioned NNN cap rate
            "p_renew": 0.85,              # Probability incumbent renews at expiry
            "renew_rent_mult": 1.08,      # Market rent ratio upon renewal
            "relet_rent_mult": 1.18,      # Stronger replacement tenant / land rent
            "vacant_carry_r": 0.22,       # Annual NNN carry (tax+ins+maint) when dark, in R
            "dark_years": 0.75,           # Downtime years if non-renewed
            "ti_lc_r": 1.10,              # TI + leasing commissions in multiples of R
            "sale_friction_1031": 0.0506, # 4.50% broker/closing + 0.56% transfer tax (sub-$5.4M)
            "tax_drag_cash": 0.24,        # Effective tax drag on gross value if sold taxable
            "annual_tail_loss_r": 0.02,   # Expected annual uninsured seismic/hazard drag
        },
        "base": {
            "k": 0.0700,                  # 4.86% UST + 214 bps NNN risk premium
            "g_in_place": 0.0150,         # 1.5%/yr contractual escalation
            "cap_long_ext": 0.0625,       # Fresh 12–15 yr extended NNN cap rate
            "cap_mid_term": 0.0665,       # ~7–8 yr remaining NNN cap rate (2035 expiry sold Yr 1)
            "cap_short_term": 0.0760,     # ~3–4 yr short-fuse NNN cap rate (2030 expiry sold Yr 1)
            "cap_relet": 0.0660,          # Post-re-tenanting exit cap rate
            "p_renew": 0.60,              # 60% renewal probability given -1.1%/-4.2% comps & closures
            "renew_rent_mult": 0.98,      # Flat-to-slight rent concession on renewal
            "relet_rent_mult": 1.05,      # Replacement QSR / medical / fast-casual market rent
            "vacant_carry_r": 0.28,       # Landlord pays NNN taxes + post-2025 insurance + security
            "dark_years": 1.25,           # 15 months downtime to permit & re-tenant in LA
            "ti_lc_r": 1.75,              # 1.75x annual rent TI + leasing commission
            "sale_friction_1031": 0.0556, # 5.00% broker/legal + 0.56% transfer tax (pre-ULA cliff)
            "tax_drag_cash": 0.27,        # Combined Fed LTCG/§1250/NIIT + CA ordinary tax on gain
            "annual_tail_loss_r": 0.05,   # Expected annual uninsured seismic/catastrophe drag
        },
        "down": {
            "k": 0.0800,                  # Higher rate / credit-spread regime
            "g_in_place": 0.0100,
            "cap_long_ext": 0.0700,
            "cap_mid_term": 0.0750,
            "cap_short_term": 0.0875,     # Financing dries up on <4 yr franchise/corporate term
            "cap_relet": 0.0760,
            "p_renew": 0.30,              # High 'JACK on Track' / margin-squeeze non-renewal
            "renew_rent_mult": 0.85,      # 15% rent roll-down demanded to stay open
            "relet_rent_mult": 0.90,      # Soft retail demand + drive-thru permitting friction
            "vacant_carry_r": 0.35,       # High vacant property tax + FAIR Plan insurance + security
            "dark_years": 2.00,           # 24 months dark-box carry in City of LA
            "ti_lc_r": 2.50,              # Heavy retrofit capex + broker commissions
            "sale_friction_1031": 0.0606, # Higher closing friction (or partial ULA price-cut allowance)
            "tax_drag_cash": 0.29,
            "annual_tail_loss_r": 0.09,
        },
        "swan": {
            "k": 0.0850,
            "g_in_place": 0.0100,
            "cap_long_ext": 0.0750,
            "cap_mid_term": 0.0800,
            "cap_short_term": 0.0950,
            "cap_relet": 0.0850,
            "p_renew": 0.15,              # Major seismic / insurer-exit / restructuring shock during hold
            "renew_rent_mult": 0.75,
            "relet_rent_mult": 0.80,
            "vacant_carry_r": 0.42,
            "dark_years": 2.50,
            "ti_lc_r": 3.50,              # Structural seismic/casualty deductible + rebuild capex
            "sale_friction_1031": 0.0650,
            "tax_drag_cash": 0.29,
            "annual_tail_loss_r": 0.28,   # Realized catastrophe / uninsured deductible shock while holding
        },
    }

    def calc_pathway(pid: str, rem_years: int, s: dict) -> float:
        k = s["k"]
        g = s["g_in_place"]
        # Year-1 sale strategies execute at end of Year 1 (collecting Year 1 net rent first)
        if pid == "P1":
            # Early Blend-and-Extend at t=1 (say 5% rent blend concession for fresh 12-15 yr term), then sell via §1031
            yr1_rent = (1.0 - s["annual_tail_loss_r"]) / (1.0 + k)
            blended_noi = 0.97 * (1.0 + g)
            gross_sale = blended_noi / s["cap_long_ext"]
            net_1031 = gross_sale * (1.0 - s["sale_friction_1031"])
            return yr1_rent + net_1031 / (1.0 + k)

        if pid == "P2":
            # Sell Before Expiry at t=1 via IRC §1031 (lease as-is: mid-term cap if 2035, short-term cap if 2030)
            yr1_rent = (1.0 - s["annual_tail_loss_r"]) / (1.0 + k)
            cap_exit = s["cap_mid_term"] if rem_years >= 7 else s["cap_short_term"]
            next_noi = 1.0 * (1.0 + g)
            gross_sale = next_noi / cap_exit
            net_1031 = gross_sale * (1.0 - s["sale_friction_1031"])
            return yr1_rent + net_1031 / (1.0 + k)

        if pid == "P3":
            # Sell Before Expiry Outright (Taxable Cash Sale at t=1, no §1031)
            yr1_rent = (1.0 - s["annual_tail_loss_r"]) / (1.0 + k)
            cap_exit = s["cap_mid_term"] if rem_years >= 7 else s["cap_short_term"]
            next_noi = 1.0 * (1.0 + g)
            gross_sale = next_noi / cap_exit
            net_cash = gross_sale * (1.0 - s["sale_friction_1031"] - s["tax_drag_cash"])
            return yr1_rent + net_cash / (1.0 + k)

        if pid == "P4":
            # Hold to Expiry (rem_years = 4 or 9) and Seek Incumbent Renewal; if non-renewed, incur dark-box cost & re-let
            pv_rent = pv_growing_annuity(1.0, g, k, rem_years)
            pv_tail = pv_growing_annuity(s["annual_tail_loss_r"], 0.0, k, rem_years)
            terminal_rent_base = (1.0 + g) ** rem_years
            # Branch A: Incumbent renews (prob p_renew)
            val_renew = (terminal_rent_base * s["renew_rent_mult"]) / s["cap_long_ext"]
            # Branch B: Incumbent vacates (prob 1 - p_renew)
            carry_cost = s["vacant_carry_r"] * s["dark_years"] + s["ti_lc_r"]
            stabilized_relet_val = (terminal_rent_base * s["relet_rent_mult"]) / s["cap_relet"]
            val_nonrenew = (stabilized_relet_val / ((1.0 + k) ** s["dark_years"])) - carry_cost
            expected_terminal = s["p_renew"] * val_renew + (1.0 - s["p_renew"]) * val_nonrenew
            return (pv_rent - pv_tail) + expected_terminal / ((1.0 + k) ** rem_years)

        if pid == "P5":
            # Hold to Expiry, Forgo Incumbent Options & Reposition / Ground-Lease / Transit Re-tenant
            pv_rent = pv_growing_annuity(1.0, g, k, rem_years)
            pv_tail = pv_growing_annuity(s["annual_tail_loss_r"], 0.0, k, rem_years)
            terminal_rent_base = (1.0 + g) ** rem_years
            carry_cost = s["vacant_carry_r"] * (s["dark_years"] + 0.25) + (s["ti_lc_r"] * 1.15)
            # Upside capture (+12% premium on transit/corner repositioning in opt/base, penalty in down/swan)
            upside_mult = 1.12 if k <= 0.0700 else 0.95
            reposition_val = (terminal_rent_base * s["relet_rent_mult"] * upside_mult) / s["cap_relet"]
            terminal_net = (reposition_val / ((1.0 + k) ** (s["dark_years"] + 0.25))) - carry_cost
            return (pv_rent - pv_tail) + terminal_net / ((1.0 + k) ** rem_years)

        raise ValueError(pid)

    defs = [
        ("P1", "Early Blend-and-Extend + Sell via §1031 (2027–2028)", "S21",
         "Highest overall risk-adjusted PV & upside if tenant signs ≥10-yr extension (<35 yrs total)."),
        ("P2", "Sell As-Is Before Expiry via §1031 Exchange (2027–2028)", "S21",
         "Strongest wealth-preservation floor if tenant declines early extension; exits tail & closure risk."),
        ("P3", "Sell As-Is Outright — Taxable Cash Exit (2027–2028)", "S22",
         "Full liquidity, but ~27% Fed+CA tax drag destroys ~3.5R–4.0R of wealth vs. §1031 exchange."),
        ("P4", "Passive Hold to Expiry & Attempt Incumbent Renewal", "S12",
         "Exposed to binary closure/roll-down cliff, dark-box carry, and multi-year LA seismic/insurance tail."),
        ("P5", "Hold to Expiry & Reposition / Transit Re-Tenant", "S31",
         "Viable growth play ONLY on high-tier transit/corner fee land with deep owner cash reserves."),
    ]

    results = []
    for expiry_yr, rem in [(2030, 4), (2035, 9)]:
        for pid, label, src, note in defs:
            vals = {sc: round(calc_pathway(pid, rem, params), 2) for sc, params in scenarios.items()}
            # Probability-weighted expected PV: 20% Opt, 50% Base, 20% Down, 10% Black-Swan Tail
            exp_pv = round(
                0.20 * vals["opt"] + 0.50 * vals["base"] + 0.20 * vals["down"] + 0.10 * vals["swan"],
                2,
            )
            results.append({
                "expiry_bookend": f"{expiry_yr} ({rem} yrs rem.)",
                "pathway_id": pid,
                "pathway": label,
                "opt_r": f"{vals['opt']:.2f} R",
                "base_r": f"{vals['base']:.2f} R",
                "down_r": f"{vals['down']:.2f} R",
                "swan_r": f"{vals['swan']:.2f} R",
                "expected_r": f"{exp_pv:.2f} R",
                "floor_r": f"{min(vals.values()):.2f} R",
                "note": note,
                "status": "Analysis",
                "source": src,
            })
    return results


def build_cap_rate_sensitivity() -> list[dict]:
    """Gross Valuation Multiple (in R = Annual NOI) & Implied Dollar Value per $100k NOI
    across Buyer Cap Rates (5.50% to 8.50%), showing Measure ULA cliff interaction (Sources S11, S17).
    """
    cap_rates = [0.0550, 0.0600, 0.0650, 0.0700, 0.0750, 0.0800, 0.0850]
    rows = []
    for cap in cap_rates:
        mult = 1.0 / cap
        # Illustrative scaling at $250k, $325k, $400k annual NNN rent (purely mathematical scaling of R, not asserted subject rent)
        v_250 = 250_000 / cap
        v_350 = 350_000 / cap
        ula_250 = "0.56% (Below $5.4M ULA)" if v_250 <= 5_400_000 else "4.56% (Triggers 4% ULA!)"
        ula_350 = "0.56% (Below $5.4M ULA)" if v_350 <= 5_400_000 else "4.56% (Triggers 4% ULA!)"
        spread_bps = round((cap - UST_10Y_ANCHOR) * 10000)
        rows.append({
            "cap_rate": f"{cap*100:.2f}%",
            "spread_vs_ust10": f"{spread_bps:+d} bps vs. 4.86% 10-Yr UST",
            "gross_multiple_r": f"{mult:.2f} × R",
            "scale_250k_noi": f"${v_250:,.0f} ({ula_250})",
            "scale_350k_noi": f"${v_350:,.0f} ({ula_350})",
            "lease_profile": (
                "12–15 yr corporate extension" if cap <= 0.0600 else
                "7–9 yr corporate NNN (2035)" if cap <= 0.0700 else
                "3–5 yr short-fuse (2030) or franchisee-only"
            ),
            "status": "Analysis",
            "source": "S17",
        })
    return rows


def build_ula_cliff_table() -> list[dict]:
    """Exact City of Los Angeles Measure ULA + County Transfer Tax Schedule Effective July 1, 2026 (Sources S17, S18)."""
    prices = [5_000_000, 5_399_500, 5_400_500, 5_650_000, 7_500_000, 10_899_500, 10_900_000]
    rows = []
    for p in prices:
        county = p * 0.0011
        city_base = p * 0.0045
        if p <= 5_400_000:
            ula_rate = 0.0
            bracket = "≤ $5,400,000 (Exempt from ULA)"
        elif p < 10_900_000:
            ula_rate = 0.04
            bracket = "> $5,400,000 to < $10,900,000 (4.0% ULA)"
        else:
            ula_rate = 0.055
            bracket = "≥ $10,900,000 (5.5% ULA)"
        ula_tax = p * ula_rate
        total_tax = county + city_base + ula_tax
        net_after_transfer = p - total_tax
        rows.append({
            "sale_price": f"${p:,.0f}",
            "bracket": bracket,
            "combined_rate": f"{(0.0056 + ula_rate)*100:.2f}%",
            "transfer_tax_usd": f"${total_tax:,.0f}",
            "net_before_broker_usd": f"${net_after_transfer:,.0f}",
            "takeaway": (
                "Optimal pre-cliff ceiling (saves ~$216k vs. $5.4005M)" if p == 5_399_500 else
                "TRAP ZONE: seller nets LESS than selling at $5,400,000 until ~$5,625,000!" if p in (5_400_500, 5_650_000) and net_after_transfer < (5_400_000 * (1 - 0.0056)) else
                "Second cliff: +1.5% jump ($163.5k instant step) at $10,900,000" if p == 10_900_000 else
                "Standard post-7/1/2026 statutory transfer tax calculation"
            ),
            "status": "Analysis",
            "source": "S17",
        })
    return rows


if __name__ == "__main__":
    print("=== AREA PROJECTIONS ===")
    for r in build_area_economic_projections():
        print(r["regime"], "->", r["pop_2026_2035"], "|", r["jobs_2026_2035"])
    print("\n=== PATHWAY PV (in R) ===")
    for r in evaluate_pathways():
        print(f"{r['expiry_bookend']:20s} {r['pathway_id']} | Opt {r['opt_r']:7s} | Base {r['base_r']:7s} | Down {r['down_r']:7s} | Swan {r['swan_r']:7s} | E[PV] {r['expected_r']:7s} | Floor {r['floor_r']}")
    print("\n=== ULA CLIFFS ===")
    for r in build_ula_cliff_table():
        print(r["sale_price"], r["combined_rate"], r["transfer_tax_usd"], "-> net", r["net_before_transfer_usd"] if "net_before_transfer_usd" in r else r["net_before_broker_usd"], "|", r["takeaway"])
