import re
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_superbill.py"
BAD = ROOT / "tests" / "fixtures" / "bad-superbills"
SAMPLES = ROOT / "tests" / "fixtures" / "samples"
EXPECTED = BAD / "expected-hits.md"


class CheckSuperbillTests(unittest.TestCase):
    def run_checker(self, path):
        return subprocess.run(
            [sys.executable, str(CHECKER), str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def expected_hits(self):
        result = {}
        for line in EXPECTED.read_text(encoding="utf-8").splitlines():
            match = re.fullmatch(r"\| (bad-\d{2}-SB-\d{2}\.txt) \| (SB-\d{2}) \|", line)
            if match:
                result[match.group(1)] = match.group(2)
        return result

    def test_each_bad_fixture_yields_exactly_its_rule(self):
        expected = self.expected_hits()
        self.assertEqual(10, len(expected))
        files = sorted(BAD.glob("bad-*.txt"))
        self.assertEqual(sorted(expected), [path.name for path in files])
        for path in files:
            with self.subTest(path=path.name):
                result = self.run_checker(path)
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                hits = re.findall(r"^(SB-\d{2}) \|", result.stdout, re.MULTILINE)
                self.assertEqual([expected[path.name]], hits, result.stdout)

    def test_three_w1_samples_pass_clean(self):
        files = sorted(SAMPLES.glob("superbill-*.txt"))
        self.assertEqual(3, len(files))
        for path in files:
            with self.subTest(path=path.name):
                result = self.run_checker(path)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertEqual("", result.stdout)

    def test_exit_zero_one_and_two(self):
        clean = SAMPLES / "superbill-aetna.txt"
        self.assertEqual(0, self.run_checker(clean).returncode)
        source = clean.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            warning = Path(directory) / "SENTINEL_WARNING_SUPERBILL.txt"
            warning.write_text(
                source.replace("CPT code: 90837", "CPT code: 90846"),
                encoding="utf-8",
            )
            result = self.run_checker(warning)
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertEqual(["SB-22", "SB-22"], re.findall(r"^(SB-\d{2}) \|", result.stdout, re.MULTILINE))
        error = BAD / "bad-01-SB-04.txt"
        self.assertEqual(2, self.run_checker(error).returncode)

    def test_npi_checksum_is_checked_for_nonzero_sentinel_digits(self):
        source = (SAMPLES / "superbill-aetna.txt").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            valid = Path(directory) / "SENTINEL_VALID_NPI.txt"
            valid.write_text(
                source.replace(
                    "SENTINEL_NPI_3_0000000000",
                    "SENTINEL_NPI_CHECKSUM_1234567893",
                ),
                encoding="utf-8",
            )
            invalid = Path(directory) / "SENTINEL_INVALID_NPI.txt"
            invalid.write_text(
                source.replace(
                    "SENTINEL_NPI_3_0000000000",
                    "SENTINEL_NPI_CHECKSUM_1234567890",
                ),
                encoding="utf-8",
            )
            valid_result = self.run_checker(valid)
            invalid_result = self.run_checker(invalid)
        self.assertEqual(0, valid_result.returncode, valid_result.stdout + valid_result.stderr)
        self.assertEqual(2, invalid_result.returncode, invalid_result.stdout + invalid_result.stderr)
        self.assertEqual(
            ["SB-05"],
            re.findall(r"^(SB-\d{2}) \|", invalid_result.stdout, re.MULTILINE),
        )

    def test_script_fix_wording_matches_rules_reference(self):
        spec = importlib.util.spec_from_file_location("check_superbill", CHECKER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        rules_path = ROOT / "src" / "references" / "superbill-rules.md"
        rules = {}
        for line in rules_path.read_text(encoding="utf-8").splitlines():
            match = re.fullmatch(
                r"\d+\. (SB-\d{2}) \| (?:error|warning) \| .+ \| "
                r'Fix list: "(.+)"',
                line,
            )
            if match:
                rules[match.group(1)] = match.group(2)
        self.assertEqual([f"SB-{number:02d}" for number in range(1, 23)], list(rules))
        self.assertEqual(rules, module.FIX)


if __name__ == "__main__":
    unittest.main()
