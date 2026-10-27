import pathlib
import csv
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INSTALL_LINE = "/plugin install recoupr-out-of-network-claims@recoupr-skills"
MARKETPLACE_LINE = "/plugin marketplace add recouprlee/recoupr-out-of-network-claims"
REQUIRED_DOCS = (
    DOCS / "launch.md",
    DOCS / "door-tests.md",
)
ROOT_DOCS = (
    ROOT / "RELEASE.md",
    ROOT / "CHANGELOG.md",
    ROOT / "README.md",
)
WORD_RE = re.compile(r"\b[\w']+\b")
MISSION = (
    "recoupr exists to fix the out-of-network claim mess. Out-of-network "
    "therapy claims should be frictionless, reliable and free for the client. "
    "That has been the mission since day one. Simple is handing the tools "
    "straight to the client, keeping private-pay therapists a thousand miles "
    "from any insurance portal, and giving it all away. When the claim is "
    "simple, you recoup your out-of-pocket cost and stay in therapy longer. "
    "No company should charge you, or take a cut of your own insurance money, "
    "to help you understand your policy. recoup what matters."
)


def read(path):
    return path.read_text(encoding="utf-8")


def word_count(text):
    return len(WORD_RE.findall(text))


class DocumentationTests(unittest.TestCase):
    def all_documents(self):
        self.assertTrue(DOCS.is_dir(), "docs directory is missing")
        for path in REQUIRED_DOCS + ROOT_DOCS:
            self.assertTrue(path.is_file(), f"{path.relative_to(ROOT)} is missing")
        docs = tuple(sorted(path for path in DOCS.rglob("*") if path.is_file()))
        return ROOT_DOCS + docs

    def test_no_internal_approval_banner_in_public_files(self):
        """The repository is public: no file may carry the internal founder-approval banner."""
        root = pathlib.Path(__file__).resolve().parents[1]
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix not in {".md", ".yml", ".yaml", ".json", ".txt"}:
                continue
            if any(part in {"dist", ".git", "__pycache__"} for part in path.parts):
                continue
            with self.subTest(path=str(path.relative_to(root))):
                self.assertNotIn("founder must approve", path.read_text(encoding="utf-8").lower())

    def test_forbidden_dash_characters_are_absent(self):
        for path in self.all_documents():
            with self.subTest(path=path.relative_to(ROOT)):
                text = read(path)
                self.assertNotIn(chr(0x2014), text)
                self.assertNotIn(chr(0x2013), text)

    def test_company_name_stays_lowercase(self):
        capitalized_company = chr(82) + "ecoupr"
        capitalized_verb = chr(82) + "ecoup"
        sentence_start = re.compile(
            r"(?:\A|[.!?]\s+|\n)\s*(?:[#>*+-]+\s*)?"
            + capitalized_verb
            + r"\b"
        )
        for path in self.all_documents():
            with self.subTest(path=path.relative_to(ROOT)):
                text = read(path)
                self.assertNotIn(capitalized_company, text)
                self.assertIsNone(sentence_start.search(text))

    def test_forbidden_release_language_is_absent(self):
        forbidden = (
            "HIPAA",
            "BAA",
            "$",
            "pricing",
            "platform",
            "dashboard",
            "pilot",
            "Claim.MD",
        )
        for path in self.all_documents():
            with self.subTest(path=path.relative_to(ROOT)):
                text = read(path)
                for value in forbidden:
                    self.assertNotIn(value, text)

    def test_launch_word_count_is_in_range(self):
        path = DOCS / "launch.md"
        self.assertTrue(path.is_file(), "launch write-up is missing")
        count = word_count(read(path))
        self.assertGreaterEqual(count, 550)
        self.assertLessEqual(count, 850)

    def test_launch_contains_the_mission_verbatim(self):
        self.assertIn(MISSION, read(DOCS / "launch.md"))

    def test_launch_research_counts_match_references(self):
        atlas_path = ROOT / "src" / "references" / "payer-atlas.csv"
        with atlas_path.open(newline="", encoding="utf-8") as handle:
            insurer_count = len(list(csv.DictReader(handle)))
        form_count = len(
            [
                path
                for path in (ROOT / "src" / "references" / "forms").glob("*.md")
                if path.name != "INDEX.md"
            ]
        )
        launch = read(DOCS / "launch.md")
        self.assertEqual(76, insurer_count)
        self.assertEqual(77, form_count)
        self.assertIn(f"{insurer_count} insurers'", launch)
        self.assertIn(f"{form_count} form files", launch)

    def test_every_url_uses_https(self):
        bare_domain = re.compile(
            r"(?<!@)(?<!https://)\b(?:[a-z0-9-]+\.)+(?:ai|com|gov|io|net|org)\b",
            flags=re.IGNORECASE,
        )
        for path in self.all_documents():
            with self.subTest(path=path.relative_to(ROOT)):
                text = read(path)
                self.assertNotIn("http://", text)
                without_https_urls = re.sub(r"https://[^\s<>)]+", "", text)
                self.assertIsNone(bare_domain.search(without_https_urls))

    def test_readme_contains_install_line(self):
        readme = read(ROOT / "README.md")
        self.assertIn(MARKETPLACE_LINE, readme)
        self.assertIn(INSTALL_LINE, readme)

    def test_release_check_passes_after_build(self):
        build = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "build.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, build.returncode, build.stdout + build.stderr)
        result = subprocess.run(
            ["bash", str(ROOT / "tools" / "release_check.sh")],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
