import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tools" / "build.py"
DRIFT = ROOT / "tools" / "check_drift.py"
SKILL_NAME = "recoupr-out-of-network-claims"


class DriftTests(unittest.TestCase):
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

    def run_drift(self, dist):
        return subprocess.run(
            [
                sys.executable,
                str(DRIFT),
                "--root",
                str(self.work_root),
                "--dist",
                str(dist),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_current_renderings_match(self):
        result = self.run_drift(self.dist)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_changed_rendering_is_named(self):
        changed = self.work_root / "dist-changed"
        shutil.copytree(self.dist, changed)
        relative = Path(SKILL_NAME) / "references" / "routines" / "file-my-claim.md"
        target = changed / relative
        content = target.read_bytes()
        target.write_bytes(content.replace(b"pending", b"Pending", 1))
        result = self.run_drift(changed)
        self.assertNotEqual(0, result.returncode)
        self.assertIn(relative.as_posix(), result.stderr)


if __name__ == "__main__":
    unittest.main()
