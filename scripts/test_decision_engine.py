"""Regression tests use synthetic numbers, never property data or forecasts."""
import math
import unittest

from decision_engine import CashFlow, compare_after_tax, public_input_status


class DecisionEngineTests(unittest.TestCase):
    def setUp(self):
        # Synthetic test fixture only; no example figures appear on the site.
        self.inputs = dict(sale_offer=100.0, sale_costs=5.0, sale_tax=7.0,
                           debt_payoff=20.0, annual_required_return=0.1,
                           hold_cash_flows=[CashFlow(1, 11), CashFlow(2, 121, True)])

    def test_public_snapshot_is_blocked_and_contains_no_result(self):
        result = public_input_status()
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(len(result["missing"]), 6)
        self.assertNotIn("sale_after_tax_equity", result)
        self.assertNotIn("hold_after_tax_equity_pv", result)

    def test_each_missing_critical_input_blocks(self):
        for key in self.inputs:
            with self.subTest(key=key):
                fields = self.inputs | {key: None}
                self.assertEqual(compare_after_tax(**fields)["status"], "blocked")
        self.assertEqual(compare_after_tax(**(self.inputs | {"hold_cash_flows": []}))["status"], "blocked")

    def test_after_tax_equity_discounting(self):
        result = compare_after_tax(**self.inputs)
        self.assertEqual(result["status"], "analysis")
        self.assertAlmostEqual(result["sale_after_tax_equity"], 68)
        self.assertAlmostEqual(result["hold_after_tax_equity_pv"], 110)
        self.assertAlmostEqual(result["difference_hold_minus_sale"], 42)

    def test_vacancy_does_not_retroactively_remove_contractual_rent(self):
        # With the same pre-expiry cash flow and terminal amount, a later sale
        # is worth less at a positive discount rate; the earlier rent remains.
        on_time = compare_after_tax(**(self.inputs | {"hold_cash_flows": [CashFlow(1, 11), CashFlow(2, 121, True)]}))
        delayed = compare_after_tax(**(self.inputs | {"hold_cash_flows": [CashFlow(1, 11), CashFlow(3.5, 121, True)]}))
        self.assertGreater(on_time["hold_after_tax_equity_pv"], delayed["hold_after_tax_equity_pv"])
        self.assertAlmostEqual(delayed["hold_after_tax_equity_pv"], 10 + 121 / 1.1 ** 3.5)

    def test_missing_terminal_is_blocked(self):
        result = compare_after_tax(**(self.inputs | {"hold_cash_flows": [CashFlow(1, 11)]}))
        self.assertEqual(result, {"status": "blocked", "missing": ["terminal cash flow"]})

    def test_invalid_numbers_and_time_order_rejected(self):
        cases = [
            {"annual_required_return": -1}, {"annual_required_return": math.nan},
            {"sale_offer": math.inf}, {"sale_costs": -1},
            {"hold_cash_flows": [CashFlow(-1, 10), CashFlow(2, 10, True)]},
            {"hold_cash_flows": [CashFlow(2, 10, True), CashFlow(3, 10)]},
            {"hold_cash_flows": [CashFlow(2, 10, True), CashFlow(3, 10, True)]},
            {"hold_cash_flows": [CashFlow(0, 10, True)]},
        ]
        for patch in cases:
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                compare_after_tax(**(self.inputs | patch))


if __name__ == "__main__":
    unittest.main()
