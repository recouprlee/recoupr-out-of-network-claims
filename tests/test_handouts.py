import csv
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tools" / "build.py"
DRIFT = ROOT / "tools" / "check_drift.py"
ATLAS = ROOT / "src" / "references" / "payer-atlas.csv"
DASHES = {chr(0x2013), chr(0x2014)}
USED_COLUMNS = (
    "insurer",
    "states",
    "member_form_name",
    "member_form_number",
    "member_form_url",
    "portal_upload",
    "portal_name",
    "portal_path",
    "mail_address",
    "member_deadline",
    "source_url",
    "verified_on",
)


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


class HandoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.work_root = Path(cls.temp_dir.name) / "work"
        shutil.copytree(ROOT / "src", cls.work_root / "src")
        result = subprocess.run(
            [sys.executable, str(BUILD), "--root", str(cls.work_root)],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        cls.handout_root = cls.work_root / "dist" / "handouts"
        with ATLAS.open(newline="", encoding="utf-8") as handle:
            cls.rows = list(csv.DictReader(handle))[:12]

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def test_twelve_first_atlas_handouts_exist(self):
        expected = {f"{slug(row['insurer'])}.md" for row in self.rows}
        actual = {path.name for path in self.handout_root.glob("*.md")}
        self.assertEqual(expected, actual)
        self.assertEqual(12, len(actual))

    def test_each_handout_fits_one_page_limits(self):
        for path in sorted(self.handout_root.glob("*.md")):
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertLessEqual(len(text.splitlines()), 55)
                self.assertLessEqual(len(text), 4000)

    def test_drift_names_a_changed_handout(self):
        changed = self.work_root / "dist-changed-handout"
        shutil.copytree(self.work_root / "dist", changed)
        filename = f"{slug(self.rows[0]['insurer'])}.md"
        target = changed / "handouts" / filename
        target.write_bytes(target.read_bytes().replace(b"Three steps", b"Three Steps", 1))
        result = subprocess.run(
            [
                sys.executable,
                str(DRIFT),
                "--root",
                str(self.work_root),
                "--dist",
                str(changed),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn(f"handouts/{filename}", result.stderr)

    def test_placeholders_and_personal_fields_are_absent(self):
        for path in sorted(self.handout_root.glob("*.md")):
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                placeholders = set(re.findall(r"<[^>\n]+>", text))
                self.assertEqual({"<practice name>"}, placeholders)
                self.assertTrue(
                    text.startswith(
                        "# How to get reimbursed for sessions at <practice name>\n"
                    )
                )
                self.assertTrue(text.endswith("\nrecoupr.ai\n"))
                self.assertNotRegex(
                    text.lower(),
                    r"(?m)^(?:client name|member id|subscriber id|date of birth|birth date):",
                )

    def test_atlas_cells_are_verbatim_and_dashes_are_absent(self):
        for row in self.rows:
            path = self.handout_root / f"{slug(row['insurer'])}.md"
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                for column in USED_COLUMNS:
                    self.assertTrue(row[column], column)
                    self.assertIn(row[column], text, column)
                for dash in DASHES:
                    self.assertNotIn(dash, text)


if __name__ == "__main__":
    unittest.main()
