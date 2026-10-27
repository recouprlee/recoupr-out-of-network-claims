import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INSTALL_LINE = (
    "/plugin install recoupr-out-of-network-claims "
    "--marketplace recouprlee/recoupr-out-of-network-claims"
)
REQUIRED_DOCS = (
    DOCS / "launch.md",
    DOCS / "newsletter" / "issue-01.md",
    DOCS / "outreach" / "sequence.md",
    DOCS / "outreach" / "rates-page-line.md",
    DOCS / "outreach" / "handout-note.md",
    DOCS / "outreach" / "measure.md",
)
ROOT_DOCS = (
    ROOT / "RELEASE.md",
    ROOT / "CHANGELOG.md",
    ROOT / "README.md",
)
WORD_RE = re.compile(r"\b[\w']+\b")


def read(path):
    return path.read_text(encoding="utf-8")


def word_count(text):
    return len(WORD_RE.findall(text))


class DocumentationTests(unittest.TestCase):
    def all_documents(self):
        self.assertTrue(DOCS.is_dir(), "docs directory is missing")
        for path in REQUIRED_DOCS + ROOT_DOCS:
            self.assertTrue(path.is_file(), f"{path.relative_to(ROOT)} is missing")
        return ROOT_DOCS + tuple(sorted(DOCS.rglob("*.md")))

    def test_founder_approval_is_at_the_top(self):
        for path in self.all_documents():
            with self.subTest(path=path.relative_to(ROOT)):
                first_line = next(line for line in read(path).splitlines() if line.strip())
                self.assertIn("founder", first_line.lower())
                self.assertIn("approve", first_line.lower())

    def test_forbidden_dash_characters_are_absent(self):
        for path in self.all_documents():
            with self.subTest(path=path.relative_to(ROOT)):
                text = read(path)
                self.assertNotIn(chr(0x2014), text)
                self.assertNotIn(chr(0x2013), text)

    def test_company_name_stays_lowercase(self):
        sentence_start = re.compile(
            r"(?:\A|[.!?]\s+|\n)\s*(?:[#>*+-]+\s*)?Recoup\b"
        )
        for path in self.all_documents():
            with self.subTest(path=path.relative_to(ROOT)):
                text = read(path)
                self.assertNotIn("Recoupr", text)
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

    def test_each_outreach_touch_is_under_120_words(self):
        path = DOCS / "outreach" / "sequence.md"
        self.assertTrue(path.is_file(), "outreach sequence is missing")
        sections = re.findall(
            r"^## Touch [123]\n(?P<body>.*?)(?=^## Touch [123]\n|\Z)",
            read(path),
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertEqual(3, len(sections))
        for number, section in enumerate(sections, start=1):
            with self.subTest(touch=number):
                self.assertLess(word_count(section), 120)

    def test_launch_word_count_is_in_range(self):
        path = DOCS / "launch.md"
        self.assertTrue(path.is_file(), "launch write-up is missing")
        count = word_count(read(path))
        self.assertGreaterEqual(count, 550)
        self.assertLessEqual(count, 850)

    def test_every_url_uses_https(self):
        bare_domain = re.compile(
            r"(?<!@)(?<!https://)\b(?:[a-z0-9-]+\.)+(?:ai|com|gov|io|net|org)\b",
            flags=re.IGNORECASE,
        )
        for path in self.all_documents():
            with self.subTest(path=path.relative_to(ROOT)):
                text = read(path)
                self.assertNotIn("http://", text)
                self.assertIsNone(bare_domain.search(text))

    def test_readme_contains_install_line(self):
        self.assertIn(INSTALL_LINE, read(ROOT / "README.md"))

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
