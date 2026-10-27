import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tools" / "build.py"
DRIFT = ROOT / "tools" / "check_drift.py"
SKILL_NAME = "recoupr-out-of-network-claims"


class W1BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.work_root = Path(self.temp_dir.name) / "work"
        shutil.copytree(ROOT / "src", self.work_root / "src")
        self.dist = self.work_root / "dist"
        subprocess.run(
            [sys.executable, str(BUILD), "--root", str(self.work_root)],
            text=True,
            capture_output=True,
            check=True,
        )

    def test_full_renderings_include_forms_and_filing_steps(self):
        reference_root = self.work_root / "src" / "references"
        filing_steps = reference_root / "filing-steps.md"
        self.assertTrue(filing_steps.is_file())
        relative_files = [
            path.relative_to(reference_root)
            for path in sorted(reference_root.rglob("*"))
            if path.is_file()
        ]
        self.assertTrue(any(path.parts[0] == "forms" for path in relative_files))

        full_roots = (
            self.dist / SKILL_NAME / "references",
            self.dist / SKILL_NAME / "skills" / SKILL_NAME / "references",
            self.work_root / "skills" / SKILL_NAME / "references",
        )
        for relative in relative_files:
            expected = (reference_root / relative).read_bytes()
            for full_root in full_roots:
                self.assertEqual(expected, (full_root / relative).read_bytes())

        zip_path = self.dist / f"{SKILL_NAME}.zip"
        with zipfile.ZipFile(zip_path) as archive:
            for relative in relative_files:
                name = f"{SKILL_NAME}/references/{relative.as_posix()}"
                self.assertEqual(
                    (reference_root / relative).read_bytes(), archive.read(name)
                )

        paste = (self.dist / "paste-in-prompt.md").read_bytes()
        self.assertNotIn(filing_steps.read_bytes(), paste)
        for form in sorted((reference_root / "forms").glob("*.md")):
            self.assertNotIn(form.read_bytes(), paste)

    def test_drift_names_a_changed_form(self):
        relative = Path("forms") / "aetna-gc-7.md"
        target = self.dist / SKILL_NAME / "references" / relative
        content = target.read_bytes()
        target.write_bytes(content.replace(b"Fillable: YES", b"Fillable: NO", 1))
        result = subprocess.run(
            [
                sys.executable,
                str(DRIFT),
                "--root",
                str(self.work_root),
                "--dist",
                str(self.dist),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn(relative.as_posix(), result.stderr)


if __name__ == "__main__":
    unittest.main()
