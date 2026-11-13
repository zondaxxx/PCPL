"""Проверки математических случаев, ввода и консольных программ."""

from decimal import Decimal
from pathlib import Path
import subprocess
import sys
import unittest

import functional
import oop
import procedural
from common import coefficient, read_coefficients


SOLVERS = (procedural.solve, oop.solve, functional.solve)
ROOT = Path(__file__).resolve().parent


class EquationTests(unittest.TestCase):
    def test_real_roots_and_degenerate_cases(self):
        cases = [
            ((1, -5, 4), (-2, -1, 1, 2)),
            ((1, -2, 1), (-1, 1)),
            ((1, 0, -16), (-2, 2)),
            ((1, 0, 1), ()),
            ((1, 5, 4), ()),
            ((1, 2, 1), ()),
            ((1, -4, 0), (-2, 0, 2)),
            ((1, 0, 0), (0,)),
            ((0, 2, -8), (-2, 2)),
            ((0, -2, 8), (-2, 2)),
            ((0, 2, 8), ()),
            ((0, 2, 0), (0,)),
            ((0, 0, 7), ()),
            ((0, 0, 0), None),
            ((-1, 5, -4), (-2, -1, 1, 2)),
        ]
        for solver in SOLVERS:
            for coefficients, expected in cases:
                with self.subTest(solver=solver.__module__, coefficients=coefficients):
                    self.assertEqual(solver(*coefficients), expected)

    def test_irrational_roots_satisfy_equation(self):
        for solver in SOLVERS:
            with self.subTest(solver=solver.__module__):
                roots = solver(1, -3, 2)
                self.assertEqual(len(roots), 4)
                for root in roots:
                    self.assertLess(abs(root ** 4 - 3 * root ** 2 + 2), Decimal("1e-24"))

    def test_large_coefficients_do_not_overflow(self):
        for solver in SOLVERS:
            with self.subTest(solver=solver.__module__):
                self.assertEqual(solver(1e300, -5e300, 4e300), (-2, -1, 1, 2))

    def test_small_root_is_not_lost_to_cancellation(self):
        for solver in SOLVERS:
            with self.subTest(solver=solver.__module__):
                roots = solver(1, -1e100, 1)
                self.assertEqual(len(roots), 4)
                self.assertGreater(roots[2], 0)
                self.assertLess(abs(roots[2] - Decimal("1e-50")), Decimal("1e-75"))

    def test_invalid_coefficient_rejected_by_all_solvers(self):
        for solver in SOLVERS:
            for value in (float("nan"), float("inf"), "oops"):
                with self.subTest(solver=solver.__module__, value=value):
                    with self.assertRaises(ValueError):
                        solver(value, 1, 1)

    def test_oop_discriminant(self):
        self.assertEqual(oop.BiquadraticEquation(1, -5, 4).discriminant, 9)


class InputTests(unittest.TestCase):
    def test_correct_argv_does_not_request_input(self):
        def unexpected_input(prompt):
            self.fail("Неожиданный интерактивный ввод")
        self.assertEqual(read_coefficients(["1", "-5", "4"], unexpected_input), (1, -5, 4))

    def test_missing_coefficients_are_requested(self):
        values = iter(("-5", "4"))
        self.assertEqual(read_coefficients(["1"], lambda _: next(values)), (1, -5, 4))

    def test_invalid_argument_retried_until_finite(self):
        values = iter(("nan", "inf", "abc", "1"))
        messages = []
        result = read_coefficients(["bad", "-5", "4"], lambda _: next(values), messages.append)
        self.assertEqual(result, (1, -5, 4))
        self.assertEqual(len(messages), 4)

    def test_extra_arguments_are_rejected(self):
        with self.assertRaises(ValueError):
            read_coefficients(["1", "2", "3", "4"])

    def test_nonfinite_and_overflow_values_are_rejected(self):
        for value in ("NaN", "Infinity", "-inf", "1e999", "", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                coefficient(value)


class CommandLineTests(unittest.TestCase):
    def test_every_program_handles_correct_and_invalid_arguments(self):
        for filename in ("procedural.py", "oop.py", "functional.py"):
            for first, stdin in (("1", ""), ("bad", "nan\n1\n")):
                with self.subTest(filename=filename, first=first):
                    result = subprocess.run(
                        [sys.executable, str(ROOT / filename), first, "-5", "4"],
                        input=stdin, text=True, capture_output=True, timeout=5,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("Дискриминант: 9", result.stdout)
                    self.assertIn("Действительные корни: -2, -1, 1, 2", result.stdout)

    def test_eof_is_handled_without_traceback(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "procedural.py")],
            input="", text=True, capture_output=True, timeout=5,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Ввод прерван", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
