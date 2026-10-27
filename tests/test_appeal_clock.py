import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "appeal_clock.py"
FIXTURES = ROOT / "tests" / "fixtures" / "denials"
CASES = (
    ("missing-attachment", "2026-01-10", "employer", "2026-07-09", "2026-05-10"),
    ("provider-information", "2026-02-15", "employer", "2026-08-14", "2026-06-15"),
    ("employer-benefit-denial", "2026-03-31", "employer", "2026-09-27", "2026-07-31"),
    ("individual-benefit-denial", "2026-04-30", "individual", "2026-10-27", "2026-08-30"),
)


class AppealClockTests(unittest.TestCase):
    def run_clock(self, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_first_four_fixture_dates(self):
        for case, notice, plan_type, appeal_by, external_by in CASES:
            with self.subTest(case=case):
                fixture = (FIXTURES / f"{case}.txt").read_text(encoding="utf-8")
                expected = (FIXTURES / f"expected-{case}.md").read_text(
                    encoding="utf-8"
                )
                self.assertIn(f"Denial notice date: {notice}", fixture)
                self.assertIn(f"Plan type: {plan_type}", fixture)
                self.assertIn(f"Appeal-by date: {appeal_by}", expected)
                self.assertIn(
                    f"External review request-by date: {external_by}", expected
                )

                result = self.run_clock(notice, plan_type)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn(f"appeal-by date: {appeal_by}", result.stdout)
                self.assertIn(
                    f"external review request-by date: {external_by}", result.stdout
                )
                self.assertIn(
                    "The insurer's letter controls where it states a different deadline.",
                    result.stdout,
                )

    def test_government_plan_refuses(self):
        result = self.run_clock("2026-05-20", "government")
        self.assertEqual(2, result.returncode)
        self.assertIn("government", result.stderr.lower())

    def test_missing_date_refuses(self):
        result = self.run_clock()
        self.assertEqual(2, result.returncode)

    def test_received_date_shifts_both_dates(self):
        result = self.run_clock(
            "2026-01-10", "employer", "--received-date", "2026-01-15"
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("appeal-by date: 2026-07-14", result.stdout)
        self.assertIn("external review request-by date: 2026-05-15", result.stdout)


if __name__ == "__main__":
    unittest.main()
