import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODES = ROOT / "src" / "references" / "codes.md"
DASHES = {chr(0x2013), chr(0x2014)}
EXPECTED_CPT = {
    "90785", "90791", "90792", "90832", "90833", "90834", "90836",
    "90837", "90838", "90839", "90840", "90845", "90846", "90847",
    "90849", "90853", "90863", "90875", "90876", "90880", "90885",
    "90887", "99202", "99203", "99204", "99205", "99211", "99212",
    "99213", "99214", "99215", "99354", "99355", "99366", "99367",
    "99368", "99417",
}
EXPECTED_POS = {"02", "03", "10", "11", "12", "49", "50", "53", "71", "72"}


def cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def section_rows(lines, heading):
    start = lines.index(heading) + 1
    end = next(
        (index for index in range(start, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    rows = [cells(line) for line in lines[start:end] if line.startswith("|")]
    return rows[2:]


class CodesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = CODES.read_text(encoding="utf-8")
        cls.lines = cls.text.splitlines()

    def test_cpt_codes_are_exactly_five_digits_and_unique(self):
        rows = section_rows(self.lines, "## 1. Psychotherapy CPT codes")
        values = [row[0] for row in rows]
        self.assertTrue(all(re.fullmatch(r"\d{5}", value) for value in values))
        self.assertEqual(len(values), len(set(values)))
        self.assertEqual(EXPECTED_CPT, set(values))

    def test_place_of_service_codes_are_two_digits(self):
        rows = section_rows(self.lines, "## 2. Place of service codes")
        values = [row[0] for row in rows]
        self.assertTrue(all(re.fullmatch(r"\d{2}", value) for value in values))
        self.assertEqual(EXPECTED_POS, set(values))

    def test_every_table_has_a_nonempty_source_column(self):
        lines = self.lines
        index = 0
        tables = 0
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
            tables += 1
            self.assertIn("source", [item.lower() for item in header])
            source_index = [item.lower() for item in header].index("source")
            index += 2
            while index < len(lines) and lines[index].startswith("|"):
                row = cells(lines[index])
                self.assertEqual(len(header), len(row), f"line {index + 1}")
                self.assertTrue(row[source_index], f"line {index + 1}: empty source")
                index += 1
        self.assertGreater(tables, 0)

    def test_taxonomy_table_has_nine_rows(self):
        rows = section_rows(self.lines, "## 7. Provider taxonomy codes")
        self.assertEqual(9, len(rows))

    def test_forbidden_dashes_are_absent(self):
        for dash in DASHES:
            self.assertNotIn(dash, self.text)


if __name__ == "__main__":
    unittest.main()
