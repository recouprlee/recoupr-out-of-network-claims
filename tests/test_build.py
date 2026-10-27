import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tools" / "build.py"
SKILL_NAME = "recoupr-out-of-network-claims"
DESCRIPTION = (
    "Prepares a person's own out-of-network therapy insurance claim or appeal "
    "from their therapist's superbill, plan documents, EOB and denial letter. "
    "Use when someone mentions a superbill, out-of-network therapy, "
    "reimbursement, an EOB, a denied claim or an appeal. The person submits "
    "the claim themselves; nothing is filed for them."
)
ROUTINES = (
    "file-my-claim",
    "check-my-superbill",
    "read-my-benefits",
    "track-my-claim",
    "appeal-my-denial",
    "client-handout",
    "superbill-template",
)
ATLAS_POINTER = (
    "Insurer filing details (form, address, portal, deadline, attachments) are "
    "not in this prompt. When a routine needs references/payer-atlas.csv, "
    "references/filing-steps.md, references/addresses.csv or a form file, ask me "
    "for my insurer and state, then ask me to open https://recoupr.ai/insurers/, "
    "pick my insurer, and paste that page's text here or upload its printed PDF. "
    "Treat that page as the insurer's atlas row and filing steps. If I cannot get "
    "it, say plainly that the route is not available and point me to the number "
    "on my insurance card. Never guess a form, address, portal or deadline."
)
ATLAS_HEADER = (
    "insurer,state,payer_id,member_form_url,form_revision,portal_upload,"
    "mail_address,fax,attachments,member_deadline,portal_shows_outcome,notes,"
    "source_url,verified_on"
)


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.work_root = Path(self.temp_dir.name) / "work"
        shutil.copytree(ROOT / "src", self.work_root / "src")

    def run_build(self, dist_name="dist", expected=0):
        result = subprocess.run(
            [
                sys.executable,
                str(BUILD),
                "--root",
                str(self.work_root),
                "--dist",
                str(self.work_root / dist_name),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result

    def test_zip_is_deterministic(self):
        self.run_build("dist-one")
        first = (self.work_root / "dist-one" / f"{SKILL_NAME}.zip").read_bytes()
        self.run_build("dist-two")
        second = (self.work_root / "dist-two" / f"{SKILL_NAME}.zip").read_bytes()
        self.assertEqual(first, second)

    def test_skill_frontmatter_and_line_limit(self):
        self.run_build()
        path = self.work_root / "dist" / SKILL_NAME / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        self.assertIn(f"name: {SKILL_NAME}\n", text)
        self.assertIn(f"description: {DESCRIPTION}\n", text)
        self.assertIn("license: Apache-2.0\n", text)
        self.assertIn("  author: recoupr\n", text)
        source = (self.work_root / "src" / "skill.md").read_text(encoding="utf-8")
        version = re.search(
            r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$',
            source,
            re.MULTILINE,
        ).group(1)
        self.assertIn(f'  version: "{version}"\n', text)
        self.assertIn('  homepage: "https://recoupr.ai"\n', text)
        name = re.search(r"^name: (.+)$", text, re.MULTILINE).group(1)
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1)
        self.assertEqual(path.parent.name, name)
        self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertLessEqual(len(name), 64)
        self.assertEqual(DESCRIPTION, description)
        self.assertGreaterEqual(len(description), 1)
        self.assertLessEqual(len(description), 1024)
        self.assertLess(len(text.splitlines()), 500)

    def test_paste_prompt_has_routines_and_atlas_pointer(self):
        self.run_build()
        path = self.work_root / "dist" / "paste-in-prompt.md"
        text = path.read_text(encoding="utf-8")
        for routine in ROUTINES:
            self.assertIn(f"## Routine: {routine}\n", text)
        self.assertIn(ATLAS_POINTER, text)
        self.assertNotIn(ATLAS_HEADER, text)

    def test_missing_menu_routine_fails(self):
        (self.work_root / "src" / "routines" / "file-my-claim.md").unlink()
        result = self.run_build(expected=1)
        self.assertIn("file-my-claim", result.stderr)

    def test_forbidden_dash_fails(self):
        path = self.work_root / "src" / "skill.md"
        path.write_text(path.read_text(encoding="utf-8") + chr(0x2014), encoding="utf-8")
        result = self.run_build(expected=1)
        self.assertIn("forbidden dash", result.stderr.lower())

    def test_capitalized_company_name_fails(self):
        path = self.work_root / "src" / "skill.md"
        bad_name = chr(82) + "ecoupr"
        path.write_text(
            path.read_text(encoding="utf-8") + "\n" + bad_name + "\n",
            encoding="utf-8",
        )
        result = self.run_build(expected=1)
        self.assertIn("lowercase", result.stderr.lower())

    def test_markdown_subset_renders_to_html(self):
        spec = importlib.util.spec_from_file_location("renderer", BUILD)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        markdown = (
            "# Heading\n\n- item\n\n1. step\n\n"
            "| a | b |\n| --- | --- |\n| c | d |\n\n"
            "```text\ncode\n```\n\n"
            "**bold** *italic* [link](https://example.org)\n"
        )
        rendered = module.markdown_to_html(markdown)
        for fragment in (
            "<h1>",
            "<ul>",
            "<ol>",
            "<table>",
            "<pre><code>",
            "<strong>",
            "<em>",
            "<a href=",
        ):
            self.assertIn(fragment, rendered)


if __name__ == "__main__":
    unittest.main()
