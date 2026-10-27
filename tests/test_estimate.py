import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "estimate_benefit.py"


class EstimateBenefitTests(unittest.TestCase):
    def run_estimate(self, *values):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *(str(value) for value in values)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def assert_case(self, values, expected):
        result = self.run_estimate(*values)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        actual = {}
        for line in result.stdout.splitlines():
            label, separator, value = line.partition(": ")
            self.assertEqual(": ", separator, line)
            actual[label] = value
        self.assertEqual(expected, actual)
        self.assertEqual("", result.stderr)

    def test_deductible_not_met(self):
        self.assert_case(
            ("200", "120", "500", "70", "1000"),
            {
                "amount applied to deductible": "120.00",
                "plan expected payment": "0.00",
                "person expected cost": "200.00",
                "remaining deductible": "380.00",
                "remaining out-of-pocket": "880.00",
            },
        )

    def test_deductible_partly_met(self):
        self.assert_case(
            ("200", "120", "50", "70", "1000"),
            {
                "amount applied to deductible": "50.00",
                "plan expected payment": "49.00",
                "person expected cost": "151.00",
                "remaining deductible": "0.00",
                "remaining out-of-pocket": "929.00",
            },
        )

    def test_deductible_met(self):
        self.assert_case(
            ("200", "120", "0", "70", "1000"),
            {
                "amount applied to deductible": "0.00",
                "plan expected payment": "84.00",
                "person expected cost": "116.00",
                "remaining deductible": "0.00",
                "remaining out-of-pocket": "964.00",
            },
        )

    def test_out_of_pocket_limit_reached_mid_claim(self):
        self.assert_case(
            ("150", "120", "20", "60", "30"),
            {
                "amount applied to deductible": "20.00",
                "plan expected payment": "90.00",
                "person expected cost": "60.00",
                "remaining deductible": "0.00",
                "remaining out-of-pocket": "0.00",
            },
        )

    def test_coinsurance_zero(self):
        self.assert_case(
            ("100", "80", "0", "0", "200"),
            {
                "amount applied to deductible": "0.00",
                "plan expected payment": "0.00",
                "person expected cost": "100.00",
                "remaining deductible": "0.00",
                "remaining out-of-pocket": "120.00",
            },
        )

    def test_refuses_missing_number(self):
        result = self.run_estimate("100", "80", "0", "70")
        self.assertEqual(2, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertRegex(result.stderr, r"^error: .+\n$")
        self.assertNotIn("usage:", result.stderr.lower())

    def test_refuses_negative_number(self):
        result = self.run_estimate("100", "80", "-1", "70", "200")
        self.assertEqual(2, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertRegex(result.stderr, r"^error: .*negative.*\n$")

    def test_refuses_coinsurance_outside_range(self):
        result = self.run_estimate("100", "80", "0", "101", "200")
        self.assertEqual(2, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertRegex(result.stderr, r"^error: .*0 to 100.*\n$")


if __name__ == "__main__":
    unittest.main()
