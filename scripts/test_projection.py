#!/usr/bin/env python3
"""Unit tests for scripts/projection.py (dimensionless 1 R break-even framework).

Guards against:
  1. Regression of TREASURY_ANCHOR / DISCOUNT_RATES[0] away from the dated
     FRED DGS10 observation in data/canonical.json (see review flag F-32).
  2. Algebraic errors in _pv_rent_stream, hold_pv, sell_now_multiple, and
     break_even_growth (closed-form Gordon-growth identity: when cap_now ==
     cap_exit == c and discount == c + g with zero vacancy, hold_pv == 1/c
     and break_even_growth == r - c).
  3. Monotonicity violations with respect to rent growth, discount rate,
     exit cap rate, and expiry vacancy.
  4. Non-determinism or accidental emission of dollar amounts / PII in CLI output.

Run:  python3 scripts/test_projection.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import projection  # noqa: E402


class ProjectionFrameworkTests(unittest.TestCase):
    def test_treasury_anchor_matches_canonical_fred_observation(self) -> None:
        canonical = json.loads((ROOT / "data" / "canonical.json").read_text(encoding="utf-8"))
        matching = [
            row for row in canonical["rows"]
            if row.get("source") == "FRED"
            and projection.TREASURY_ANCHOR_DATE in row.get("scope", "")
            and row.get("status") == "Verified"
        ]
        self.assertTrue(
            matching,
            f"Expected a Verified FRED row for {projection.TREASURY_ANCHOR_DATE} in data/canonical.json",
        )
        m = re.search(r"(\d+\.\d+)%", matching[0]["value"])
        self.assertIsNotNone(m, f"Could not parse percentage from {matching[0]['value']!r}")
        expected_rate = round(float(m.group(1)) / 100.0, 6)
        self.assertAlmostEqual(projection.TREASURY_ANCHOR, expected_rate, places=6)
        self.assertAlmostEqual(projection.DISCOUNT_RATES[0], projection.TREASURY_ANCHOR, places=6)

    def test_closed_form_gordon_identity(self) -> None:
        # Exact identity: when cap_now == cap_exit == c and r - g == c (0 vacancy),
        # PV(rent stream) + PV(exit at (1+g)^N / c) == 1 / c == sell_now_multiple(c).
        for c in projection.CAP_RATES:
            for g in projection.GROWTH_RATES:
                r = c + g
                pv_hold = projection.hold_pv(growth=g, discount=r, cap_exit=c, vacancy_months=0)
                pv_sell = projection.sell_now_multiple(c)
                self.assertAlmostEqual(pv_hold, pv_sell, places=11)
                be_g = projection.break_even_growth(cap_now=c, cap_exit=c, discount=r, vacancy_months=0)
                self.assertIsNotNone(be_g)
                self.assertAlmostEqual(be_g, g, places=11)

    def test_break_even_table_roots_invert_hold_pv(self) -> None:
        target = projection.sell_now_multiple(projection.BASE_CAP_NOW)
        table = projection.break_even_table()
        self.assertEqual(len(table), len(projection.DISCOUNT_RATES))
        checked = 0
        for row in table:
            r = row["discount"]
            for cell in row["values"]:
                c_exit = cell["cap_exit"]
                g = cell["growth"]
                self.assertIsNotNone(g)
                pv = projection.hold_pv(g, r, c_exit, vacancy_months=0)
                self.assertAlmostEqual(pv, target, places=9)
                checked += 1
        self.assertEqual(checked, len(projection.DISCOUNT_RATES) * len(projection.CAP_RATES))

    def test_break_even_returns_none_outside_bracket(self) -> None:
        # Impossible target (e.g. cap_now = 0.001 => 1000x rent) exceeds max growth bracket.
        self.assertIsNone(projection.break_even_growth(0.001, 0.065, 0.09))

    def test_economic_monotonicity(self) -> None:
        # Higher growth -> strictly higher hold PV
        pvs_by_g = [projection.hold_pv(g, 0.06, 0.055) for g in projection.GROWTH_RATES]
        for a, b in zip(pvs_by_g, pvs_by_g[1:]):
            self.assertLess(a, b)

        # Higher discount rate -> strictly lower hold PV
        pvs_by_r = [projection.hold_pv(0.01, r, 0.055) for r in projection.DISCOUNT_RATES]
        for a, b in zip(pvs_by_r, pvs_by_r[1:]):
            self.assertGreater(a, b)

        # Higher exit cap rate -> strictly lower hold PV
        pvs_by_c = [projection.hold_pv(0.01, 0.06, c) for c in projection.CAP_RATES]
        for a, b in zip(pvs_by_c, pvs_by_c[1:]):
            self.assertGreater(a, b)

        # Expiry vacancy strictly reduces hold PV and produces 0 < loss_pct < 1
        vac = projection.vacancy_scenario()
        self.assertEqual(vac["vacancy_months"], projection.VACANCY_MONTHS)
        for row in vac["rows"]:
            self.assertLess(row["with_vacancy"], row["with_rent"])
            self.assertGreater(row["loss_pct"], 0.0)
            self.assertLess(row["loss_pct"], 1.0)

    def test_determinism_and_dimensionless_privacy_boundary(self) -> None:
        first = projection.compute()
        second = projection.compute()
        self.assertEqual(first, second)

        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "projection.py")],
            check=True,
            capture_output=True,
            text=True,
        )
        parsed = json.loads(proc.stdout)
        self.assertEqual(parsed, first)
        self.assertNotIn("$", proc.stdout)
        for forbidden in ("APN", "Lance Tucker", "Rachel Webb", "Mark King", "Andres Chait"):
            self.assertNotIn(forbidden, proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
