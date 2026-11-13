"""Проверки поведения по условиям лабораторной работы."""

from contextlib import redirect_stdout
from io import StringIO
import subprocess
import sys
import unittest
from unittest.mock import patch

from lab_python_fp.field import field
from lab_python_fp.gen_random import gen_random
from lab_python_fp.unique import Unique
from lab_python_fp.print_result import print_result
from lab_python_fp.cm_timer import cm_timer_1, cm_timer_2
from lab_python_fp.process_data import f1, f2, f3, f4


class FieldTests(unittest.TestCase):
    def test_single_field_skips_missing_and_none_but_keeps_falsy(self):
        self.assertEqual(list(field([{}, {"x": None}, {"x": 0}, {"x": False}, {"x": ""}], "x")), [0, False, ""])

    def test_multiple_fields_and_source_unchanged(self):
        rows = [{"x": 2, "y": None, "z": 3}, {"y": 4}, {}, {"x": None}]
        self.assertEqual(list(field(rows, "x", "y")), [{"x": 2}, {"y": 4}])
        self.assertEqual(rows[0], {"x": 2, "y": None, "z": 3})

    def test_no_fields(self):
        with self.assertRaises(ValueError):
            list(field([],))

    def test_lazy_consumption(self):
        consumed = []
        def rows():
            for value in range(3):
                consumed.append(value)
                yield {"x": value}
        values = field(rows(), "x")
        self.assertEqual(consumed, [])
        self.assertEqual(next(values), 0)
        self.assertEqual(consumed, [0])


class RandomTests(unittest.TestCase):
    def test_count_and_bounds(self):
        values = list(gen_random(100, -2, 3))
        self.assertEqual(len(values), 100)
        self.assertTrue(all(-2 <= value <= 3 for value in values))

    def test_inclusive_equal_endpoints(self):
        self.assertEqual(list(gen_random(3, 5, 5)), [5, 5, 5])
        self.assertEqual(list(gen_random(0, 0, 1)), [])

    def test_invalid_bounds_and_count(self):
        for args in [(-1, 0, 2), (1, 2, 0)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                list(gen_random(*args))

    def test_random_calls_are_lazy(self):
        with patch("lab_python_fp.gen_random.random.randint", return_value=2) as randint:
            values = gen_random(2, 1, 3)
            randint.assert_not_called()
            self.assertEqual(next(values), 2)
            randint.assert_called_once_with(1, 3)


class UniqueTests(unittest.TestCase):
    def test_order_and_case_modes(self):
        values = ["a", "A", "b", "B", "a", "b"]
        self.assertEqual(list(Unique(values)), ["a", "A", "b", "B"])
        self.assertEqual(list(Unique(values, ignore_case=True)), ["a", "b"])

    def test_original_string_is_returned(self):
        self.assertEqual(list(Unique(["ПРОГРАММИСТ", "программист"], ignore_case=True)), ["ПРОГРАММИСТ"])

    def test_generator_and_iterator_protocol(self):
        values = Unique(value % 2 for value in range(4))
        self.assertIs(iter(values), values)
        self.assertEqual(next(values), 0)
        self.assertEqual(next(values), 1)
        with self.assertRaises(StopIteration):
            next(values)
        with self.assertRaises(StopIteration):
            next(values)

    def test_lazy_input(self):
        consumed = []
        def source():
            for value in [1, 1, 2]:
                consumed.append(value)
                yield value
        values = Unique(source())
        self.assertEqual(consumed, [])
        self.assertEqual(next(values), 1)
        self.assertEqual(consumed, [1])
        self.assertEqual(next(values), 2)
        self.assertEqual(consumed, [1, 1, 2])

    def test_bool_option_validation(self):
        with self.assertRaises(TypeError):
            Unique([], ignore_case="yes")


class PrintingTests(unittest.TestCase):
    def test_print_return_metadata_arguments(self):
        @print_result
        def sample(value, *, suffix):
            """A documented function."""
            return {"answer": value + suffix}
        output = StringIO()
        with redirect_stdout(output):
            result = sample("hello", suffix="!")
        self.assertEqual(result, {"answer": "hello!"})
        self.assertEqual(output.getvalue(), "sample\nanswer = hello!\n")
        self.assertEqual(sample.__name__, "sample")
        self.assertEqual(sample.__doc__, "A documented function.")

    def test_list_is_printed_in_column_and_not_copied(self):
        values = [1, 2]
        @print_result
        def sample():
            return values
        output = StringIO()
        with redirect_stdout(output):
            self.assertIs(sample(), values)
        self.assertEqual(output.getvalue(), "sample\n1\n2\n")

    def test_scalar_and_none(self):
        for value in [1, "iu5", None]:
            with self.subTest(value=value):
                @print_result
                def sample():
                    return value
                output = StringIO()
                with redirect_stdout(output):
                    self.assertEqual(sample(), value)
                self.assertEqual(output.getvalue(), f"sample\n{value}\n")


class TimerTests(unittest.TestCase):
    def test_both_timers_measure_interval(self):
        for timer in (cm_timer_1, cm_timer_2):
            with self.subTest(timer=timer), patch("lab_python_fp.cm_timer.perf_counter", side_effect=[10, 15.5]):
                output = StringIO()
                with redirect_stdout(output), timer():
                    pass
                self.assertEqual(output.getvalue(), "time: 5.500000\n")

    def test_exceptions_propagate_and_elapsed_time_is_printed(self):
        for timer in (cm_timer_1, cm_timer_2):
            with self.subTest(timer=timer), patch("lab_python_fp.cm_timer.perf_counter", side_effect=[10, 11]):
                output = StringIO()
                with self.assertRaisesRegex(RuntimeError, "failure"), redirect_stdout(output), timer():
                    raise RuntimeError("failure")
                self.assertEqual(output.getvalue(), "time: 1.000000\n")


class ProcessingTests(unittest.TestCase):
    def test_pipeline_preserves_first_case_and_transforms(self):
        data = [
            {"job-name": "Экономист"}, {"job-name": "Программист C#"},
            {"job-name": "программист c#"}, {"job-name": "ПРОГРАММИСТ Python"},
            {"job-name": None}, {},
        ]
        with redirect_stdout(StringIO()), patch("lab_python_fp.gen_random.random.randint", side_effect=[100000, 200000]):
            first = f1(data)
            self.assertEqual(first, ["Программист C#", "ПРОГРАММИСТ Python", "Экономист"])
            result = f4(f3(f2(first)))
        self.assertEqual(result, [
            "Программист C# с опытом Python, зарплата 100000 руб.",
            "ПРОГРАММИСТ Python с опытом Python, зарплата 200000 руб.",
        ])

    def test_empty_pipeline(self):
        with redirect_stdout(StringIO()):
            self.assertEqual(f4(f3(f2(f1([])))), [])

    def test_sort_demo_both_versions(self):
        result = subprocess.run([sys.executable, "-m", "lab_python_fp.sort"], capture_output=True, text=True, check=True)
        expected = "[123, 100, -100, -30, 30, 4, -4, 1, -1, 0]"
        self.assertEqual(result.stdout.splitlines(), [expected, expected])


if __name__ == "__main__":
    unittest.main()
