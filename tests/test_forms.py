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
PAYEE_LABEL_RE = re.compile(
    r"\b(?:pay|payment)\s+(?:benefits\s+)?(?:to\s+)?"
    r"(?:member|provider|insured|subscriber|policyholder)\b"
    r"|\b(?:member|provider|policyholder)\s+payment\b"
    r"|\bpay benefits (?:directly to|for this claim)\b"
    r"|\bbenefits paid directly to\b"
    r"|\bissue payment to\b"
    r"|\bauthorize payment\b"
    r"|\baccept assignment\b"
    r"|\bassignment of benefits\b"
    r"|\bdirect payment\b"
    r"|\bpayee\b"
    r"|\breimburse(?:ment|d)?\s+(?:to|payable to)\b",
    re.IGNORECASE,
)
PAYEE_FILLED_FROM_RE = re.compile(
    r"^(?:select: .+ \(atlas payment_to_member\)"
    r"|leave blank: assignment of benefits, do not sign"
    r"|ask the person: the atlas does not state the member option "
    r"\(atlas payment_to_member is NOT PUBLISHED\))$"
)
NON_PAYEE_PAYMENT_RE = re.compile(r"^Did you make payment to provider\?", re.IGNORECASE)


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

    def test_payee_fields_use_atlas_shapes(self):
        for path in sorted(FORMS.glob("*.md")):
            if path.name == "INDEX.md":
                continue
            for line in path.read_text(encoding="utf-8").splitlines():
                cells = table_cells(line) if line.strip().startswith("|") else []
                if (
                    len(cells) != 5
                    or not PAYEE_LABEL_RE.search(cells[1])
                    or NON_PAYEE_PAYMENT_RE.search(cells[1])
                ):
                    continue
                with self.subTest(path=path.name, field=cells[1]):
                    self.assertRegex(cells[4], PAYEE_FILLED_FROM_RE)

    def test_bcbstx_member_payment_is_selected(self):
        path = (
            FORMS
            / "blue-cross-and-blue-shield-of-texas-hcsc-including-ers-healthselect-730526.md"
        )
        rows = [
            table_cells(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("|")
        ]
        target = next(row for row in rows if row[1] == "To pay Insured/Subscriber")
        self.assertTrue(target[4].startswith("select:"), target[4])

    def test_selected_payee_options_are_named_by_the_atlas(self):
        with ATLAS.open(newline="", encoding="utf-8") as handle:
            atlas_rows = list(csv.DictReader(handle))
        by_filename = {
            f"{slug(row['insurer'])}-{slug(row['member_form_number'])}.md": row
            for row in atlas_rows
        }
        for path in sorted(FORMS.glob("*.md")):
            if path.name == "INDEX.md":
                continue
            for line in path.read_text(encoding="utf-8").splitlines():
                cells = table_cells(line) if line.strip().startswith("|") else []
                if len(cells) != 5 or not cells[4].startswith("select: "):
                    continue
                with self.subTest(path=path.name, field=cells[1]):
                    self.assertIn(path.name, by_filename)
                    option = cells[4].removeprefix("select: ").removesuffix(
                        " (atlas payment_to_member)"
                    )
                    self.assertIn(option, by_filename[path.name]["payment_to_member"])


if __name__ == "__main__":
    unittest.main()
