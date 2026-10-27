#!/usr/bin/env python3
"""Check that generated renderings carry the source text without drift."""

import argparse
import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path

import build


class DriftError(Exception):
    """The first generated mismatch."""


class TextCollector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def normalized_html_text(value):
    collector = TextCollector()
    collector.feed(value)
    return " ".join(" ".join(collector.parts).split())


def source_blocks(markdown):
    return [block for block in re.split(r"\n\s*\n", markdown.strip()) if block.strip()]


def parse_scalar(value, path, line_number):
    value = value.strip()
    if not value:
        raise DriftError(f"{path}:{line_number}: empty frontmatter value")
    if value[0] in "\"'":
        if len(value) < 2 or value[-1] != value[0]:
            raise DriftError(f"{path}:{line_number}: unclosed frontmatter quote")
        return value[1:-1]
    return value


def parse_frontmatter(text, path):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise DriftError(f"{path}: frontmatter does not start with delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise DriftError(f"{path}: frontmatter does not end with delimiter") from error
    result = {}
    current_mapping = None
    for index, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  "):
            if current_mapping is None or not line.startswith("  "):
                raise DriftError(f"{path}:{index}: invalid frontmatter indentation")
            key, separator, value = line.strip().partition(":")
            if not separator or not key:
                raise DriftError(f"{path}:{index}: invalid frontmatter field")
            if key in result[current_mapping]:
                raise DriftError(f"{path}:{index}: duplicate frontmatter field {key}")
            result[current_mapping][key] = parse_scalar(value, path, index)
            continue
        key, separator, value = line.partition(":")
        if not separator or not key or key.strip() != key:
            raise DriftError(f"{path}:{index}: invalid frontmatter field")
        if key in result:
            raise DriftError(f"{path}:{index}: duplicate frontmatter field {key}")
        if value.strip():
            result[key] = parse_scalar(value, path, index)
            current_mapping = None
        else:
            result[key] = {}
            current_mapping = key
    return result


def read_required(path, label):
    try:
        return path.read_bytes()
    except OSError as error:
        raise DriftError(f"{label}: {error}") from error


def require_equal(actual, expected, label):
    if actual != expected:
        raise DriftError(f"{label}: bytes do not match source")


def check_zip(zip_path, expected_files):
    try:
        with zipfile.ZipFile(zip_path, "r") as archive:
            names = set(archive.namelist())
            for relative, expected in expected_files.items():
                archive_name = f"{build.SKILL_NAME}/{relative}"
                if archive_name not in names:
                    raise DriftError(f"{zip_path.name}:{archive_name}: file is missing")
                require_equal(
                    archive.read(archive_name),
                    expected,
                    f"{zip_path.name}:{archive_name}",
                )
    except (OSError, zipfile.BadZipFile) as error:
        raise DriftError(f"{zip_path.name}: {error}") from error


def check_print_paragraphs(printable, source_markdown, label):
    page_text = normalized_html_text(printable.decode("utf-8"))
    for number, block in enumerate(source_blocks(source_markdown), start=1):
        block_text = normalized_html_text(build.markdown_to_html(block))
        if block_text and block_text not in page_text:
            raise DriftError(f"print/index.html:{label}: paragraph {number} is missing")


def check(root, dist_dir):
    body, routine_names, routines, references, templates = build.load_sources(root)
    expected_skill = build.render_skill_markdown(body, routine_names)
    expected_paste = build.render_paste_prompt(
        body, routine_names, routines, references
    )
    expected_print = build.render_print_html(expected_paste)
    expected_handouts = build.render_handouts(root)

    skill_dir = dist_dir / build.SKILL_NAME
    skill_path = skill_dir / "SKILL.md"
    actual_skill = read_required(skill_path, f"{build.SKILL_NAME}/SKILL.md")
    frontmatter = parse_frontmatter(
        actual_skill.decode("utf-8"), f"{build.SKILL_NAME}/SKILL.md"
    )
    if frontmatter.get("name") != skill_dir.name:
        raise DriftError(
            f"{build.SKILL_NAME}/SKILL.md: name does not equal folder name"
        )
    if frontmatter.get("description") != build.DESCRIPTION:
        raise DriftError(
            f"{build.SKILL_NAME}/SKILL.md: description does not match required text"
        )
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", frontmatter["name"]):
        raise DriftError(f"{build.SKILL_NAME}/SKILL.md: name is not valid")
    if not 1 <= len(frontmatter["name"]) <= 64:
        raise DriftError(f"{build.SKILL_NAME}/SKILL.md: name length is not valid")
    if not 1 <= len(frontmatter["description"]) <= 1024:
        raise DriftError(f"{build.SKILL_NAME}/SKILL.md: description length is not valid")
    require_equal(actual_skill, expected_skill, f"{build.SKILL_NAME}/SKILL.md")

    expected_files = {"SKILL.md": expected_skill}
    for name in routine_names:
        relative = f"references/routines/{name}.md"
        expected_files[relative] = routines[name]
    for filename, content in references.items():
        expected_files[f"references/{filename}"] = content
    for filename, content in templates.items():
        expected_files[f"templates/{filename}"] = content
    for relative, expected in expected_files.items():
        actual = read_required(skill_dir / relative, f"{build.SKILL_NAME}/{relative}")
        require_equal(actual, expected, f"{build.SKILL_NAME}/{relative}")

    validator_skill_dir = skill_dir / "skills" / build.SKILL_NAME
    for relative, expected in expected_files.items():
        label = f"{build.SKILL_NAME}/skills/{build.SKILL_NAME}/{relative}"
        actual = read_required(validator_skill_dir / relative, label)
        require_equal(actual, expected, label)

    plugin_skill_dir = root / "skills" / build.SKILL_NAME
    for relative, expected in expected_files.items():
        label = f"skills/{build.SKILL_NAME}/{relative}"
        actual = read_required(plugin_skill_dir / relative, label)
        require_equal(actual, expected, label)

    check_zip(dist_dir / f"{build.SKILL_NAME}.zip", expected_files)

    paste_path = dist_dir / "paste-in-prompt.md"
    actual_paste = read_required(paste_path, "paste-in-prompt.md")
    require_equal(actual_paste, expected_paste, "paste-in-prompt.md")
    for name in routine_names:
        if routines[name] not in actual_paste:
            raise DriftError(f"paste-in-prompt.md: routine {name} bytes are missing")
    for filename in build.PASTE_REFERENCES:
        if references[filename] not in actual_paste:
            raise DriftError(
                f"paste-in-prompt.md: reference {filename} bytes are missing"
            )
    atlas = references["payer-atlas.csv"]
    if atlas in actual_paste:
        raise DriftError("paste-in-prompt.md: payer-atlas.csv must be replaced")
    if build.ATLAS_POINTER.encode("utf-8") not in actual_paste:
        raise DriftError("paste-in-prompt.md: payer atlas pointer is missing")

    print_path = dist_dir / "print" / "index.html"
    actual_print = read_required(print_path, "print/index.html")
    require_equal(actual_print, expected_print, "print/index.html")
    check_print_paragraphs(
        actual_print, body.decode("utf-8"), "src/skill.md"
    )
    for name in routine_names:
        check_print_paragraphs(
            actual_print,
            routines[name].decode("utf-8"),
            f"src/routines/{name}.md",
        )
    for filename in build.PASTE_REFERENCES:
        check_print_paragraphs(
            actual_print,
            references[filename].decode("utf-8"),
            f"src/references/{filename}",
        )

    handout_dir = dist_dir / "handouts"
    try:
        actual_names = {
            path.name for path in handout_dir.iterdir() if path.is_file()
        }
    except OSError as error:
        raise DriftError(f"handouts: {error}") from error
    if actual_names != set(expected_handouts):
        missing = sorted(set(expected_handouts) - actual_names)
        extra = sorted(actual_names - set(expected_handouts))
        detail = f"missing {missing[0]}" if missing else f"unexpected {extra[0]}"
        raise DriftError(f"handouts: {detail}")
    for filename, expected in sorted(expected_handouts.items()):
        actual = read_required(handout_dir / filename, f"handouts/{filename}")
        require_equal(actual, expected, f"handouts/{filename}")


def parse_args(argv=None):
    default_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=default_root)
    parser.add_argument("--dist", type=Path)
    arguments = parser.parse_args(argv)
    arguments.root = arguments.root.resolve()
    if arguments.dist is None:
        arguments.dist = arguments.root / "dist"
    else:
        arguments.dist = arguments.dist.resolve()
    return arguments


def main(argv=None):
    arguments = parse_args(argv)
    try:
        check(arguments.root, arguments.dist)
    except (DriftError, build.BuildError, UnicodeDecodeError) as error:
        print(f"drift check failed: {error}", file=sys.stderr)
        return 1
    print("Drift check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
