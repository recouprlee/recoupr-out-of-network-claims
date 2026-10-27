import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "tools" / "phi_scan.py"


class PhiScanTests(unittest.TestCase):
    def run_scan(self, *paths):
        return subprocess.run(
            [sys.executable, str(SCAN), *(str(path) for path in paths)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_clean_fixtures_pass(self):
        result = self.run_scan(ROOT / "tests" / "fixtures" / "clean")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("clean", result.stdout.lower())

    def test_each_seeded_fixture_reports_its_pattern(self):
        expected = {
            "dob.txt": "dob",
            "member-id.txt": "member-id",
            "ssn.txt": "ssn",
            "name-beside-id.txt": "name-beside-id",
            "contact.txt": "contact",
        }
        seeded = ROOT / "tests" / "fixtures" / "seeded"
        for filename, pattern in expected.items():
            with self.subTest(filename=filename):
                result = self.run_scan(seeded / filename)
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertIn(f": {pattern}\n", result.stdout)

    def test_report_never_prints_source_line(self):
        path = ROOT / "tests" / "fixtures" / "seeded" / "ssn.txt"
        source_line = path.read_text(encoding="utf-8").strip()
        result = self.run_scan(path)
        self.assertEqual(2, result.returncode)
        self.assertNotIn(source_line, result.stdout)

    def test_repository_scan_ignores_seeded_directory(self):
        result = self.run_scan(ROOT)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_reference_file_allows_insurer_name_and_phone(self):
        content = (
            ROOT / "tests" / "fixtures" / "seeded" / "reference-contact.txt"
        ).read_text(encoding="utf-8")
        parent = ROOT / "src" / "references"
        with tempfile.TemporaryDirectory(dir=parent) as directory:
            target = Path(directory) / "reference-contact.txt"
            target.write_text(content, encoding="utf-8")
            result = self.run_scan(target)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_non_reference_file_reports_name_and_contact(self):
        content = (
            ROOT / "tests" / "fixtures" / "seeded" / "reference-contact.txt"
        ).read_text(encoding="utf-8")
        parent = ROOT / "tests" / "fixtures" / "seeded"
        with tempfile.TemporaryDirectory(dir=parent) as directory:
            target = Path(directory) / "reference-contact.txt"
            target.write_text(content, encoding="utf-8")
            result = self.run_scan(target)
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn(": name-beside-id\n", result.stdout)
        self.assertIn(": contact\n", result.stdout)

    def test_reference_file_reports_member_id(self):
        content = (
            ROOT / "tests" / "fixtures" / "seeded" / "member-id.txt"
        ).read_text(encoding="utf-8")
        parent = ROOT / "src" / "references"
        with tempfile.TemporaryDirectory(dir=parent) as directory:
            target = Path(directory) / "member-id.txt"
            target.write_text(content, encoding="utf-8")
            result = self.run_scan(target)
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn(": member-id\n", result.stdout)

    def test_reference_file_reports_ssn(self):
        content = (
            ROOT / "tests" / "fixtures" / "seeded" / "ssn.txt"
        ).read_text(encoding="utf-8")
        parent = ROOT / "src" / "references"
        with tempfile.TemporaryDirectory(dir=parent) as directory:
            target = Path(directory) / "ssn.txt"
            target.write_text(content, encoding="utf-8")
            result = self.run_scan(target)
        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn(": ssn\n", result.stdout)


if __name__ == "__main__":
    unittest.main()
