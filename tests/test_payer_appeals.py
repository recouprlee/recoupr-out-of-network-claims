import csv
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "src" / "references" / "payer-atlas.csv"
APPEALS = ROOT / "src" / "references" / "payer-appeals.csv"
HEADER = [
    "insurer",
    "appeal_form_or_letter",
    "portal_upload",
    "portal_path",
    "internal_deadline",
    "internal_levels",
    "external_review",
    "include_list",
    "mh_specific",
    "fax",
    "mail",
    "source_url",
    "verified_on",
]


class PayerAppealsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with ATLAS.open(newline="", encoding="utf-8") as handle:
            cls.atlas_rows = list(csv.DictReader(handle))
        with APPEALS.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            cls.header = reader.fieldnames
            cls.rows = list(reader)

    def test_header_and_insurer_roster_match_atlas(self):
        self.assertEqual(HEADER, self.header)
        self.assertEqual(
            [row["insurer"] for row in self.atlas_rows],
            [row["insurer"] for row in self.rows],
        )

    def test_every_cell_is_populated(self):
        for line_number, row in enumerate(self.rows, start=2):
            for column in HEADER:
                self.assertTrue(row[column].strip(), f"line {line_number}: {column}")

    def test_source_urls_and_verified_dates(self):
        for line_number, row in enumerate(self.rows, start=2):
            urls = row["source_url"].split(";")
            self.assertTrue(
                all(url.startswith("https://") for url in urls),
                f"line {line_number}: source_url",
            )
            verified = row["verified_on"]
            if verified != "NOT PUBLISHED":
                parsed = date.fromisoformat(verified)
                self.assertEqual(2026, parsed.year, f"line {line_number}")


if __name__ == "__main__":
    unittest.main()
