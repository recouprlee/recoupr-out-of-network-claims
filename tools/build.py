#!/usr/bin/env python3
"""Build deterministic renderings of the skill from src/."""

import argparse
import csv
import html
import re
import shutil
import sys
import zipfile
from pathlib import Path


SKILL_NAME = "recoupr-out-of-network-claims"
DESCRIPTION = (
    "Prepares a person's own out-of-network therapy insurance claim or appeal "
    "from their therapist's superbill, plan documents, EOB and denial letter. "
    "Use when someone mentions a superbill, out-of-network therapy, "
    "reimbursement, an EOB, a denied claim or an appeal. The person submits "
    "the claim themselves; nothing is filed for them."
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
PASTE_REFERENCES = ("codes.md", "eob-codes.md", "appeals.md", "sources.md")
HANDOUT_COUNT = 12
HANDOUT_COLUMNS = (
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
HANDOUT_TOKEN_RE = re.compile(r"\{\{([a-z_]+)\}\}")
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
MENU_ITEM_RE = re.compile(
    r'^- \*\*([a-z0-9]+(?:-[a-z0-9]+)*)\*\*: Say ".+"$', re.MULTILINE
)
COMPANY_RE = re.compile(r"recoupr", re.IGNORECASE)
INLINE_TOKEN_RE = re.compile(
    r"(`[^`]+`|\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\)|\*[^*]+\*)"
)
TABLE_RULE_RE = re.compile(r"^:?-{3,}:?$")


class BuildError(Exception):
    """A source or output error that should be shown without a traceback."""


def read_utf8(path):
    try:
        return path.read_bytes().decode("utf-8")
    except UnicodeDecodeError as error:
        raise BuildError(f"{path}: is not valid UTF-8") from error
    except OSError as error:
        raise BuildError(f"{path}: {error}") from error


def parse_routine_menu(body):
    section_match = re.search(
        r"^## Task menu\n(?P<section>.*?)(?=^## |\Z)",
        body,
        flags=re.MULTILINE | re.DOTALL,
    )
    if section_match is None:
        raise BuildError("src/skill.md: missing Task menu section")
    names = MENU_ITEM_RE.findall(section_match.group("section"))
    if not names:
        raise BuildError("src/skill.md: Task menu has no routines")
    if len(names) != len(set(names)):
        raise BuildError("src/skill.md: Task menu repeats a routine")
    return names


def validate_source_text(path, text, source_root):
    relative = path.relative_to(source_root).as_posix()
    for character, label in ((chr(0x2014), "em dash"), (chr(0x2013), "en dash")):
        if character in text:
            line = text[: text.index(character)].count("\n") + 1
            raise BuildError(f"src/{relative}:{line}: forbidden dash character, {label}")
    for match in COMPANY_RE.finditer(text):
        if match.group(0) != "recoupr":
            line = text[: match.start()].count("\n") + 1
            raise BuildError(
                f"src/{relative}:{line}: company name must be lowercase recoupr"
            )


def parse_source_skill(text):
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        raise BuildError("src/skill.md: frontmatter does not start with delimiter")
    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.rstrip("\r\n") == "---":
            end = index
            break
    if end is None:
        raise BuildError("src/skill.md: frontmatter does not end with delimiter")

    name = None
    version = None
    section = None
    for line_number, raw_line in enumerate(lines[1:end], start=2):
        line = raw_line.rstrip("\r\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  "):
            if section != "metadata":
                raise BuildError(
                    f"src/skill.md:{line_number}: unexpected frontmatter indentation"
                )
            key, separator, value = line.strip().partition(":")
            if not separator or not value.strip():
                raise BuildError(
                    f"src/skill.md:{line_number}: invalid metadata field"
                )
            if key == "version":
                version = value.strip().strip("\"'")
            continue
        key, separator, value = line.partition(":")
        if not separator or not key or key.strip() != key:
            raise BuildError(
                f"src/skill.md:{line_number}: invalid frontmatter field"
            )
        if key == "name":
            name = value.strip().strip("\"'")
            section = None
        elif key == "metadata" and not value.strip():
            section = "metadata"
        else:
            section = None

    if name != SKILL_NAME:
        raise BuildError(f"src/skill.md: name must be {SKILL_NAME}")
    if version is None:
        raise BuildError("src/skill.md: metadata.version is missing")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise BuildError("src/skill.md: metadata.version is not a version number")
    body = "".join(lines[end + 1 :])
    if not body.strip():
        raise BuildError("src/skill.md: body is empty")
    return body, version


def load_sources(root):
    source_root = root / "src"
    if not source_root.is_dir():
        raise BuildError(f"{source_root}: source directory is missing")
    source_files = sorted(path for path in source_root.rglob("*") if path.is_file())
    if not source_files:
        raise BuildError(f"{source_root}: source directory is empty")
    text_by_path = {}
    for path in source_files:
        text = read_utf8(path)
        validate_source_text(path, text, source_root)
        text_by_path[path] = text

    skill_path = source_root / "skill.md"
    if skill_path not in text_by_path:
        raise BuildError("src/skill.md: file is missing")
    body, version = parse_source_skill(text_by_path[skill_path])
    routine_names = parse_routine_menu(body)
    routine_dir = source_root / "routines"
    routine_files = {
        path.stem: path
        for path in sorted(routine_dir.glob("*.md"))
        if path.is_file()
    }
    for name in routine_names:
        if name not in routine_files:
            raise BuildError(f"src/routines/{name}.md: menu routine file is missing")
    unlisted = sorted(set(routine_files) - set(routine_names))
    if unlisted:
        raise BuildError(f"src/routines/{unlisted[0]}.md: routine is not in the menu")

    references_dir = source_root / "references"
    reference_files = sorted(
        path for path in references_dir.rglob("*") if path.is_file()
    )
    required_references = {
        "payer-atlas.csv",
        "codes.md",
        "eob-codes.md",
        "appeals.md",
        "sources.md",
    }
    found_references = {
        path.name for path in reference_files if path.parent == references_dir
    }
    missing_references = sorted(required_references - found_references)
    if missing_references:
        raise BuildError(
            f"src/references/{missing_references[0]}: required reference is missing"
        )

    routines = {
        name: text_by_path[routine_files[name]].encode("utf-8")
        for name in routine_names
    }
    references = {
        path.relative_to(references_dir).as_posix(): text_by_path[path].encode("utf-8")
        for path in reference_files
    }
    templates_dir = source_root / "templates"
    template_files = sorted(
        path for path in templates_dir.rglob("*") if path.is_file()
    )
    templates = {
        path.relative_to(templates_dir).as_posix(): text_by_path[path].encode("utf-8")
        for path in template_files
    }
    return (
        body.encode("utf-8"),
        version,
        routine_names,
        routines,
        references,
        templates,
    )


def render_skill_markdown(body, routine_names, version):
    frontmatter = (
        "---\n"
        f"name: {SKILL_NAME}\n"
        f"description: {DESCRIPTION}\n"
        "license: Apache-2.0\n"
        "metadata:\n"
        "  author: recoupr\n"
        f'  version: "{version}"\n'
        '  homepage: "https://recoupr.ai"\n'
        "---\n"
    ).encode("utf-8")
    output = bytearray(frontmatter)
    output.extend(body)
    if not output.endswith(b"\n"):
        output.extend(b"\n")
    output.extend(b"\n## Routines\n\n")
    for name in routine_names:
        output.extend(f"- [{name}](references/routines/{name}.md)\n".encode("utf-8"))
    if len(output.decode("utf-8").splitlines()) >= 500:
        raise BuildError("generated SKILL.md must be under 500 lines")
    return bytes(output)


def append_section(output, heading, content):
    if not output.endswith(b"\n"):
        output.extend(b"\n")
    output.extend(b"\n")
    output.extend(heading.encode("utf-8"))
    output.extend(b"\n\n")
    output.extend(content)


def render_paste_prompt(body, routine_names, routines, references):
    output = bytearray(
        b"You are helping me with my own out-of-network therapy claim.\n"
        b"Follow the instructions below exactly.\n\n"
    )
    output.extend(b"## Insurer filing details\n\n")
    output.extend(ATLAS_POINTER.encode("utf-8"))
    output.extend(b"\n\n")
    output.extend(body)
    for name in routine_names:
        append_section(output, f"## Routine: {name}", routines[name])
    for filename in PASTE_REFERENCES:
        append_section(output, f"## Reference: {filename}", references[filename])
    if not output.endswith(b"\n"):
        output.extend(b"\n")
    output.extend(b"\n")
    output.extend(ATLAS_POINTER.encode("utf-8"))
    output.extend(b"\n")
    return bytes(output)


def render_inline(text):
    output = []
    position = 0
    for match in INLINE_TOKEN_RE.finditer(text):
        output.append(html.escape(text[position : match.start()]))
        token = match.group(0)
        if token.startswith("`"):
            output.append(f"<code>{html.escape(token[1:-1])}</code>")
        elif token.startswith("**"):
            output.append(f"<strong>{render_inline(token[2:-2])}</strong>")
        elif token.startswith("["):
            label, target = token[1:].split("](", 1)
            output.append(
                f'<a href="{html.escape(target[:-1], quote=True)}">'
                f"{render_inline(label)}</a>"
            )
        else:
            output.append(f"<em>{render_inline(token[1:-1])}</em>")
        position = match.end()
    output.append(html.escape(text[position:]))
    return "".join(output)


def split_table_row(line):
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def is_table(lines, index):
    if index + 1 >= len(lines) or "|" not in lines[index]:
        return False
    rules = split_table_row(lines[index + 1])
    headers = split_table_row(lines[index])
    return bool(rules) and len(rules) == len(headers) and all(
        TABLE_RULE_RE.fullmatch(rule) for rule in rules
    )


def starts_block(lines, index):
    line = lines[index]
    return bool(
        not line.strip()
        or line.startswith("```")
        or re.match(r"^#{1,6} ", line)
        or re.match(r"^[-*+] ", line)
        or re.match(r"^\d+\. ", line)
        or is_table(lines, index)
    )


def markdown_to_html(markdown):
    lines = markdown.splitlines()
    output = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith("```"):
            index += 1
            code_lines = []
            while index < len(lines) and not lines[index].startswith("```"):
                code_lines.append(lines[index])
                index += 1
            if index < len(lines):
                index += 1
            output.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
            continue
        heading = re.match(r"^(#{1,6}) (.+)$", line)
        if heading:
            level = len(heading.group(1))
            output.append(f"<h{level}>{render_inline(heading.group(2))}</h{level}>")
            index += 1
            continue
        if is_table(lines, index):
            headers = split_table_row(lines[index])
            index += 2
            rows = []
            while index < len(lines) and lines[index].strip() and "|" in lines[index]:
                rows.append(split_table_row(lines[index]))
                index += 1
            head = "".join(f"<th>{render_inline(cell)}</th>" for cell in headers)
            body_rows = []
            for row in rows:
                cells = row + [""] * (len(headers) - len(row))
                body_rows.append(
                    "<tr>"
                    + "".join(
                        f"<td>{render_inline(cell)}</td>" for cell in cells[: len(headers)]
                    )
                    + "</tr>"
                )
            output.append(
                "<table><thead><tr>"
                + head
                + "</tr></thead><tbody>"
                + "".join(body_rows)
                + "</tbody></table>"
            )
            continue
        unordered = re.match(r"^[-*+] (.+)$", line)
        ordered = re.match(r"^\d+\. (.+)$", line)
        if unordered or ordered:
            tag = "ul" if unordered else "ol"
            pattern = re.compile(r"^[-*+] (.+)$" if unordered else r"^\d+\. (.+)$")
            items = []
            while index < len(lines):
                item = pattern.match(lines[index])
                if item is None:
                    break
                items.append(f"<li>{render_inline(item.group(1))}</li>")
                index += 1
            output.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        paragraph = [line.strip()]
        index += 1
        while index < len(lines) and not starts_block(lines, index):
            paragraph.append(lines[index].strip())
            index += 1
        output.append(f"<p>{render_inline(' '.join(paragraph))}</p>")
    return "\n".join(output)


def render_print_html(paste_prompt):
    markdown = paste_prompt.decode("utf-8")
    content = markdown_to_html(markdown)
    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>recoupr out-of-network claims</title>
<style>
:root {{ color-scheme: light; }}
body {{ color: #111; font-family: Arial, sans-serif; line-height: 1.45; margin: 2rem auto; max-width: 52rem; padding: 0 1rem; }}
h1, h2, h3, h4, h5, h6 {{ line-height: 1.2; page-break-after: avoid; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #777; padding: 0.35rem; text-align: left; vertical-align: top; }}
pre {{ border: 1px solid #bbb; overflow-wrap: anywhere; padding: 0.75rem; white-space: pre-wrap; }}
a {{ color: inherit; }}
@media print {{
  body {{ margin: 0; max-width: none; padding: 0; }}
  a {{ text-decoration: none; }}
  table, pre, ul, ol {{ break-inside: avoid; }}
}}
</style>
</head>
<body>
{content}
</body>
</html>
"""
    return document.encode("utf-8")


def reset_directory(path, root):
    resolved = path.resolve()
    protected = {Path("/").resolve(), root.resolve(), (root / "src").resolve()}
    if resolved in protected:
        raise BuildError(f"refusing to replace protected path: {path}")
    if path.is_symlink():
        raise BuildError(f"refusing to replace symbolic link: {path}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def write_skill_folder(
    skill_dir,
    skill_markdown,
    routine_names,
    routines,
    references,
    templates,
):
    (skill_dir / "references" / "routines").mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_bytes(skill_markdown)
    for name in routine_names:
        (skill_dir / "references" / "routines" / f"{name}.md").write_bytes(
            routines[name]
        )
    for filename in sorted(references):
        target = skill_dir / "references" / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(references[filename])
    for filename in sorted(templates):
        target = skill_dir / "templates" / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(templates[filename])


def add_zip_entry(archive, name, data=None):
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
    info.create_system = 3
    if data is None:
        info.external_attr = (0o40755 << 16) | 0x10
        info.compress_type = zipfile.ZIP_STORED
        archive.writestr(info, b"")
    else:
        info.external_attr = 0o100644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, data)


def write_deterministic_zip(skill_dir, zip_path):
    directories = [skill_dir]
    directories.extend(sorted(path for path in skill_dir.rglob("*") if path.is_dir()))
    files = sorted(path for path in skill_dir.rglob("*") if path.is_file())
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for directory in directories:
            relative = directory.relative_to(skill_dir.parent).as_posix().rstrip("/") + "/"
            add_zip_entry(archive, relative)
        for path in files:
            relative = path.relative_to(skill_dir.parent).as_posix()
            add_zip_entry(archive, relative, path.read_bytes())


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def render_handouts(root):
    source_root = root / "src"
    template_path = source_root / "templates" / "handout.md"
    template = read_utf8(template_path)
    validate_source_text(template_path, template, source_root)
    tokens = set(HANDOUT_TOKEN_RE.findall(template))
    unknown = sorted(tokens - set(HANDOUT_COLUMNS))
    if unknown:
        raise BuildError(f"{template_path}: unknown handout token {unknown[0]}")
    missing = sorted(set(HANDOUT_COLUMNS) - tokens)
    if missing:
        raise BuildError(f"{template_path}: missing handout token {missing[0]}")

    atlas_path = source_root / "references" / "payer-atlas.csv"
    try:
        with atlas_path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as error:
        raise BuildError(f"{atlas_path}: {error}") from error
    if len(rows) < HANDOUT_COUNT:
        raise BuildError(f"{atlas_path}: fewer than {HANDOUT_COUNT} insurer rows")

    rendered = {}
    for line_number, row in enumerate(rows[:HANDOUT_COUNT], start=2):
        for column in HANDOUT_COLUMNS:
            if not row.get(column, "").strip():
                raise BuildError(f"{atlas_path}:{line_number}: {column} is empty")
        body = HANDOUT_TOKEN_RE.sub(lambda match: row[match.group(1)], template)
        if HANDOUT_TOKEN_RE.search(body):
            raise BuildError(f"{template_path}: unresolved handout token")
        if len(body.splitlines()) > 55:
            raise BuildError(f"{row['insurer']}: handout exceeds 55 lines")
        if len(body) > 4000:
            raise BuildError(f"{row['insurer']}: handout exceeds 4000 characters")
        filename = f"{slug(row['insurer'])}.md"
        if filename in rendered:
            raise BuildError(f"{atlas_path}:{line_number}: duplicate handout slug")
        rendered[filename] = body.encode("utf-8")
    return rendered


def write_handouts(handout_dir, handouts):
    handout_dir.mkdir(parents=True)
    for filename, content in sorted(handouts.items()):
        (handout_dir / filename).write_bytes(content)


def build(root, dist_dir):
    body, version, routine_names, routines, references, templates = load_sources(
        root
    )
    skill_markdown = render_skill_markdown(body, routine_names, version)
    paste_prompt = render_paste_prompt(body, routine_names, routines, references)
    printable = render_print_html(paste_prompt)
    handouts = render_handouts(root)

    reset_directory(dist_dir, root)
    skill_dir = dist_dir / SKILL_NAME
    write_skill_folder(
        skill_dir,
        skill_markdown,
        routine_names,
        routines,
        references,
        templates,
    )
    write_deterministic_zip(skill_dir, dist_dir / f"{SKILL_NAME}.zip")
    validator_skill_dir = skill_dir / "skills" / SKILL_NAME
    write_skill_folder(
        validator_skill_dir,
        skill_markdown,
        routine_names,
        routines,
        references,
        templates,
    )
    (dist_dir / "paste-in-prompt.md").write_bytes(paste_prompt)
    (dist_dir / "print").mkdir(parents=True)
    (dist_dir / "print" / "index.html").write_bytes(printable)
    write_handouts(dist_dir / "handouts", handouts)

    plugin_skill_dir = root / "skills" / SKILL_NAME
    reset_directory(plugin_skill_dir, root)
    write_skill_folder(
        plugin_skill_dir,
        skill_markdown,
        routine_names,
        routines,
        references,
        templates,
    )
    return dist_dir


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
        output = build(arguments.root, arguments.dist)
    except (BuildError, OSError, zipfile.BadZipFile) as error:
        print(f"build failed: {error}", file=sys.stderr)
        return 1
    print(
        f"Built skill folder, ZIP, paste-in prompt, printable page and handouts in {output}"
    )
    print(f"Mirrored plugin skill in {arguments.root / 'skills' / SKILL_NAME}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
