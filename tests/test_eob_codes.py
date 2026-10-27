import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "src" / "references" / "eob-codes.md"
DASHES = {chr(0x2013), chr(0x2014)}
SUSPECTED = {"17", "23", "24", "58", "97", "136", "151", "252"}
EXPECTED_CODES = {
    "CARC 4", "CARC 15", "CARC 16", "CARC 17", "CARC 18", "CARC 22",
    "CARC 23", "CARC 24", "CARC 26", "CARC 27", "CARC 29", "CARC 31",
    "CARC 32", "CARC 33", "CARC 50", "CARC 58", "CARC 96", "CARC 97",
    "CARC 119", "CARC 136", "CARC 151", "CARC 181", "CARC 182",
    "CARC 197", "CARC 198", "CARC 204", "CARC 252", "CARC A1",
    "CARC A2", "CARC A3", "RARC N54", "RARC N130", "RARC N290",
    "RARC N386",
}
BUCKETS = {
    "parity_violation",
    "eligibility_mismatch",
    "edi_rejection",
    "prior_auth_required",
    "timely_filing",
    "duplicate_claim",
    "coordination_of_benefits",
    "plan_exclusion",
    "informational",
}
NEXT_STEPS = {"correction", "appeal", "ask the therapist", "nothing"}


def cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


class EobCodeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = REFERENCE.read_text(encoding="utf-8")
        lines = cls.text.splitlines()
        start = lines.index("## Code table") + 1
        table = [cells(line) for line in lines[start:] if line.startswith("|")]
        cls.header = table[0]
        cls.rows = table[2:]

    def test_table_columns_and_required_cells(self):
        self.assertEqual(
            [
                "code",
                "official description",
                "earlier product wording",
                "plain-words meaning",
                "bucket",
                "next step",
            ],
            [value.lower() for value in self.header],
        )
        self.assertGreater(len(self.rows), 0)
        for row in self.rows:
            self.assertEqual(len(self.header), len(row), row)
            self.assertTrue(row[0])
            self.assertTrue(row[1])
            if row[1].startswith("UNREADABLE"):
                self.assertRegex(row[1], r"HTTP [1-5][0-9]{2}")
            else:
                self.assertIn("https://x12.org/", row[1])
                self.assertIn("read 2026-10-27", row[1])
            self.assertTrue(row[3])
            self.assertIn(row[4], BUCKETS)
            self.assertIn(row[5], NEXT_STEPS)

    def test_suspected_codes_have_match_notes(self):
        for code in SUSPECTED:
            self.assertRegex(
                self.text,
                rf"(?m)^- CARC {re.escape(code)}: (?:MATCHED|DID NOT MATCH)\.",
            )

    def test_code_inventory_covers_product_map_and_answer_keys(self):
        self.assertEqual(EXPECTED_CODES, {row[0] for row in self.rows})

    def test_wording_differences_are_flagged(self):
        by_code = {row[0]: row for row in self.rows}
        for code in SUSPECTED:
            row = by_code[f"CARC {code}"]
            self.assertIn("WORDING DIFFERS", row[2])

    def test_forbidden_dashes_are_absent(self):
        for dash in DASHES:
            self.assertNotIn(dash, self.text)


if __name__ == "__main__":
    unittest.main()
