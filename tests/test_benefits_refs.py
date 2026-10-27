import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCES = (
    ROOT / "src" / "references" / "benefits.md",
    ROOT / "src" / "references" / "tracking.md",
)
SOURCE_FILES = {
    "eligibilityBenefitExplainer.ts",
    "eligibility-parser.service.ts",
    "claimStatusExplainer.ts",
    "memberEobCopy.ts",
    "21-eob-received.md",
    "23-eob-denied-or-underpaid.md",
    "L1-recognition-turnaround.csv",
    "payer-atlas.csv",
    "filing-steps.md",
}


def cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def tables(text):
    lines = text.splitlines()
    index = 0
    while index + 1 < len(lines):
        if not lines[index].startswith("|"):
            index += 1
            continue
        header = cells(lines[index])
        rule = cells(lines[index + 1])
        if len(header) != len(rule) or not all(
            re.fullmatch(r":?-{3,}:?", item) for item in rule
        ):
            index += 1
            continue
        rows = []
        index += 2
        while index < len(lines) and lines[index].startswith("|"):
            rows.append((index + 1, cells(lines[index])))
            index += 1
        yield header, rows


class BenefitReferenceTests(unittest.TestCase):
    def test_every_table_row_has_a_source_and_no_empty_cell(self):
        for path in REFERENCES:
            text = path.read_text(encoding="utf-8")
            found = 0
            for header, rows in tables(text):
                found += 1
                lowered = [value.lower() for value in header]
                self.assertIn("source", lowered, path.name)
                source_index = lowered.index("source")
                self.assertTrue(rows, f"{path.name}: table has no rows")
                for line_number, row in rows:
                    self.assertEqual(len(header), len(row), f"{path}:{line_number}")
                    self.assertTrue(
                        all(row), f"{path}:{line_number}: table cell is empty"
                    )
                    self.assertTrue(row[source_index], f"{path}:{line_number}: source")
            self.assertGreater(found, 0, path.name)

    def test_every_url_uses_https(self):
        for path in REFERENCES:
            text = path.read_text(encoding="utf-8")
            urls = re.findall(r"\b[a-zA-Z]+://[^\s|)>]+", text)
            self.assertTrue(urls, path.name)
            for url in urls:
                self.assertTrue(url.startswith("https://"), f"{path.name}: {url}")

    def test_sources_are_input_filenames_or_https_urls(self):
        for path in REFERENCES:
            text = path.read_text(encoding="utf-8")
            for header, rows in tables(text):
                source_index = [value.lower() for value in header].index("source")
                for line_number, row in rows:
                    source = row[source_index]
                    self.assertTrue(
                        source.startswith("https://")
                        or any(filename in source for filename in SOURCE_FILES),
                        f"{path}:{line_number}: invalid source {source}",
                    )


if __name__ == "__main__":
    unittest.main()
