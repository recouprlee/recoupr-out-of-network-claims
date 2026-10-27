import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "src" / "references" / "payer-atlas.csv"
FORMS = ROOT / "src" / "references" / "forms"
IDENTITY_LABELS = (
    "Form number",
    "Revision",
    "URL",
    "Fillable",
    "Pages",
    "SHA-256",
    "Read date",
)
TABLE_HEADER = ["Section", "Field label", "Kind", "Required", "Filled from"]


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def table_cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


class FormsTests(unittest.TestCase):
    def test_forms_directory_and_files_exist(self):
        self.assertTrue(FORMS.is_dir())
        self.assertTrue(any(path.name != "INDEX.md" for path in FORMS.glob("*.md")))

    def test_every_form_has_identity_and_five_cell_rows(self):
        for path in sorted(FORMS.glob("*.md")):
            if path.name == "INDEX.md":
                continue
            with self.subTest(path=path.name):
                lines = path.read_text(encoding="utf-8").splitlines()
                self.assertTrue(lines and lines[0].startswith("# "))
                positions = {}
                for label in IDENTITY_LABELS:
                    matches = [
                        index
                        for index, line in enumerate(lines)
                        if line.startswith(f"{label}: ")
                    ]
                    self.assertEqual([matches[0]] if matches else [], matches)
                    positions[label] = matches[0]
                self.assertEqual(
                    list(positions.values()), sorted(positions.values()), path.name
                )
                sha = lines[positions["SHA-256"]].split(": ", 1)[1]
                self.assertRegex(sha, r"^(?:[0-9a-f]{64}|NOT PUBLISHED)$")
                form_number = lines[positions["Form number"]].split(": ", 1)[1]
                header_index = next(
                    index
                    for index, line in enumerate(lines)
                    if table_cells(line) == TABLE_HEADER
                )
                self.assertEqual(5, len(table_cells(lines[header_index + 1])))
                data_rows = [
                    line
                    for line in lines[header_index + 2 :]
                    if line.strip().startswith("|")
                ]
                if form_number not in {"NOT PUBLISHED", "UNREADABLE"}:
                    self.assertTrue(data_rows, f"{path.name}: no field rows")
                for line in data_rows:
                    self.assertEqual(5, len(table_cells(line)), path.name)

    def test_every_form_is_primary_or_indexed_once(self):
        with ATLAS.open(newline="", encoding="utf-8") as handle:
            atlas_rows = list(csv.DictReader(handle))
        primary = {
            f"{slug(row['insurer'])}-{slug(row['member_form_number'])}.md"
            for row in atlas_rows
        }
        index_path = FORMS / "INDEX.md"
        index_text = (
            index_path.read_text(encoding="utf-8") if index_path.exists() else ""
        )
        for path in sorted(FORMS.glob("*.md")):
            if path.name == "INDEX.md":
                continue
            references = int(path.name in primary) + len(
                re.findall(rf"`{re.escape(path.name)}`", index_text)
            )
            self.assertEqual(1, references, path.name)


if __name__ == "__main__":
    unittest.main()
