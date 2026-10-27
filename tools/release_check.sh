#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

python3 - <<'PY'
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path.cwd()
ARTIFACTS = (
    "dist/recoupr-out-of-network-claims.zip",
    "dist/recoupr-out-of-network-claims/SKILL.md",
    "dist/paste-in-prompt.md",
)


def fail(name):
    print(f"release check failed: {name}", file=sys.stderr)
    raise SystemExit(2)


for relative in ARTIFACTS:
    path = ROOT / relative
    if not path.is_file():
        fail(f"{relative} is missing")
    if path.stat().st_size == 0:
        fail(f"{relative} is empty")

workflow_path = ROOT / ".github" / "workflows" / "release.yml"
try:
    workflow_lines = workflow_path.read_text(encoding="utf-8").splitlines()
except OSError:
    fail(".github/workflows/release.yml cannot be read")

workflow_files = []
in_files = False
files_indent = None
for line in workflow_lines:
    stripped = line.strip()
    indent = len(line) - len(line.lstrip())
    if not in_files and stripped == "files: |":
        in_files = True
        files_indent = indent
        continue
    if in_files:
        if stripped and indent <= files_indent:
            break
        if stripped:
            workflow_files.append(stripped)
if tuple(workflow_files) != ARTIFACTS:
    fail("release workflow artifact names do not match")

try:
    plugin = json.loads(
        (ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    marketplace = json.loads(
        (ROOT / ".claude-plugin" / "marketplace.json").read_text(
            encoding="utf-8"
        )
    )
except (OSError, json.JSONDecodeError):
    fail("release manifest version cannot be read")
if not isinstance(plugin, dict) or not isinstance(marketplace, dict):
    fail("release manifest version cannot be read")

versions = {
    ".claude-plugin/plugin.json": plugin.get("version"),
}
plugins = marketplace.get("plugins")
if (
    not isinstance(plugins, list)
    or len(plugins) != 1
    or not isinstance(plugins[0], dict)
):
    fail(".claude-plugin/marketplace.json skill entry is missing")
versions[".claude-plugin/marketplace.json"] = plugins[0].get("version")

try:
    source_skill = (ROOT / "src" / "skill.md").read_text(encoding="utf-8")
except OSError:
    fail("src/skill.md version cannot be read")
source_match = re.search(
    r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$',
    source_skill,
    flags=re.MULTILINE,
)
if source_match is None:
    fail("src/skill.md metadata.version is missing")
versions["src/skill.md"] = source_match.group(1)

for relative in (
    "dist/recoupr-out-of-network-claims/SKILL.md",
    "dist/recoupr-out-of-network-claims/skills/recoupr-out-of-network-claims/SKILL.md",
    "skills/recoupr-out-of-network-claims/SKILL.md",
):
    try:
        text = (ROOT / relative).read_text(encoding="utf-8")
    except OSError:
        fail(f"{relative} version cannot be read")
    match = re.search(
        r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$',
        text,
        flags=re.MULTILINE,
    )
    if match is None:
        fail(f"{relative} version is missing")
    versions[relative] = match.group(1)

if not all(
    isinstance(value, str) and re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", value)
    for value in versions.values()
):
    fail("version string is missing or invalid")
version_values = set(versions.values())
if len(version_values) != 1:
    fail("version strings do not match")
version = next(iter(version_values))

zip_path = ROOT / ARTIFACTS[0]
try:
    with zipfile.ZipFile(zip_path) as archive:
        zip_skill = archive.read(
            "recoupr-out-of-network-claims/SKILL.md"
        ).decode("utf-8")
except (OSError, KeyError, UnicodeDecodeError, zipfile.BadZipFile):
    fail("ZIP skill version cannot be read")
zip_match = re.search(
    r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$',
    zip_skill,
    flags=re.MULTILINE,
)
if zip_match is None or zip_match.group(1) != version:
    fail("ZIP skill version does not match")

try:
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
except OSError:
    fail("CHANGELOG.md cannot be read")
if re.search(rf"^## {re.escape(version)}\b", changelog, flags=re.MULTILINE) is None:
    fail(f"CHANGELOG.md entry for {version} is missing")

try:
    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
except OSError:
    fail(f"{ARTIFACTS[0]} cannot be read for SHA-256")
print(f"release check passed for version {version}")
print(f"SHA-256 {digest}  {ARTIFACTS[0]}")
PY
