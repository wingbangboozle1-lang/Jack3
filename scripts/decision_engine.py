"""Fail-closed, offline equity-cash-flow arithmetic for future private analysis.

No inputs are collected, fetched, or persisted by this module.  A cash-flow
comparison is not a forecast, appraisal, tax opinion, or a verification service.
The caller must substantiate every input and independently check the lease,
tax treatment, sale expenses and debt.  Financial inputs and results must never
be copied into the public Pages artifact.

Both paths must be stated on the same after-tax *equity* basis.  For holding,
include each operating cash flow net of unreimbursed expenses, debt service,
capital spending and applicable tax; supply exactly one terminal cash flow net
of selling costs, taxes and debt payoff.  No default dates, growth, cap rates,
terminal values, disaster probabilities, or required returns are invented.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence


@dataclass(frozen=True)
class CashFlow:
    """One after-tax equity cash flow at a stated time after the decision date.

    ``terminal`` marks the final sale/reversion, not a rent payment.  An assumed
    scenario is never evidence that the cash flow will occur.
    """

    years: float
    amount: float
    terminal: bool = False


def _finite(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{label} must be a finite number")
    return result


def compare_after_tax(
    *,
    sale_offer: float | None,
    sale_costs: float | None,
    sale_tax: float | None,
    debt_payoff: float | None,
    annual_required_return: float | None,
    hold_cash_flows: Sequence[CashFlow] | None,
) -> dict:
    """Compare immediate sale proceeds with a dated, after-tax hold stream.

    Missing critical fields return only a blocked status and generic field
    names; no result or substituted estimate is produced.  A completed result
    is arithmetic on supplied inputs, not an assurance those inputs are true or
    appropriate.  The caller is responsible for verifying source and vintage.
    """
    fields = {
        "sale offer": sale_offer,
        "sale costs": sale_costs,
        "sale tax": sale_tax,
        "debt payoff": debt_payoff,
        "annual required return": annual_required_return,
        "hold cash flows": hold_cash_flows,
    }
    missing = [name for name, value in fields.items() if value is None]
    if missing:
        return {"status": "blocked", "missing": missing}

    offer = _finite(sale_offer, "sale offer")
    costs = _finite(sale_costs, "sale costs")
    tax = _finite(sale_tax, "sale tax")
    payoff = _finite(debt_payoff, "debt payoff")
    rate = _finite(annual_required_return, "annual required return")
    if offer < 0 or costs < 0 or payoff < 0:
        raise ValueError("offer, costs and debt payoff must not be negative")
    # Tax may be negative where a substantiated tax benefit applies.
    if rate <= -1:
        raise ValueError("annual required return must be greater than -100%")
    if isinstance(hold_cash_flows, (str, bytes)) or not isinstance(hold_cash_flows, Sequence):
        raise ValueError("hold cash flows must be a sequence")
    if not hold_cash_flows:
        return {"status": "blocked", "missing": ["hold cash flows"]}

    validated = []
    for flow in hold_cash_flows:
        if not isinstance(flow, CashFlow) or not isinstance(flow.terminal, bool):
            raise ValueError("each cash flow must be a CashFlow with a boolean terminal marker")
        year = _finite(flow.years, "cash-flow timing")
        amount = _finite(flow.amount, "cash-flow amount")
        if year < 0:
            raise ValueError("cash-flow timing cannot precede the decision date")
        validated.append((year, amount, flow.terminal))
    terminals = [year for year, _, terminal in validated if terminal]
    if not terminals:
        return {"status": "blocked", "missing": ["terminal cash flow"]}
    if len(terminals) != 1 or terminals[0] <= 0:
        raise ValueError("supply exactly one terminal cash flow after the decision date")
    if any(year > terminals[0] for year, _, _ in validated):
        raise ValueError("no hold cash flow may occur after the terminal sale")

    try:
        discounted = [amount / (1.0 + rate) ** year for year, amount, _ in validated]
        hold_pv = math.fsum(discounted)
        sale_net = offer - costs - tax - payoff
    except (OverflowError, ZeroDivisionError) as exc:
        raise ValueError("discounting produced an invalid result") from exc
    if not math.isfinite(hold_pv) or not math.isfinite(sale_net):
        raise ValueError("cash-flow calculation produced a non-finite result")
    return {
        "status": "analysis",
        "sale_after_tax_equity": sale_net,
        "hold_after_tax_equity_pv": hold_pv,
        "difference_hold_minus_sale": hold_pv - sale_net,
    }


def public_input_status() -> dict:
    """Current public snapshot has no subject-specific financial inputs."""
    return compare_after_tax(
        sale_offer=None, sale_costs=None, sale_tax=None, debt_payoff=None,
        annual_required_return=None, hold_cash_flows=None,
    )
