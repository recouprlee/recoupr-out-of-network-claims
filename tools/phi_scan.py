#!/usr/bin/env python3
"""Scan files for person-shaped data without printing matched text."""

import argparse
import os
import re
import sys
from pathlib import Path


SENTINEL_RE = re.compile(
    r"\bSENTINEL_[A-Z0-9_]+(?:@[A-Z0-9.-]+)?", re.IGNORECASE
)
SLASH_DATE_RE = re.compile(
    r"(?<!\d)(?:0?[1-9]|1[0-2])/(?:0?[1-9]|[12]\d|3[01])/(?:\d{4}|\d{2})(?!\d)"
)
HYPHEN_DATE_RE = re.compile(
    r"(?<!\d)\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])(?!\d)"
)
DOB_TERM_RE = re.compile(r"\b(?:DOB|date of birth|birth date)\b", re.IGNORECASE)
ID_LABEL_RE = re.compile(
    r"\b(?:member id|subscriber id|policy number|claim number)\b", re.IGNORECASE
)
ID_TOKEN_RE = re.compile(r"\b[A-Za-z0-9]{6,}\b")
SSN_RE = re.compile(r"(?<!\d)\d{3}[- ]\d{2}[- ]\d{4}(?!\d)")
CAPITALIZED_NAME_RE = re.compile(
    r"\b[A-Z][a-z]{1,19}(?:[ \t]+[A-Z][a-z]{1,19})+\b"
)
EMAIL_RE = re.compile(
    r"\b[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,63}\b"
)
PHONE_RE = re.compile(
    r"(?<!\d)(?:\(\d{3}\)|\d{3})[ .-]?\d{3}[ .-]?\d{4}(?!\d)"
)
IGNORED_DIRECTORY_NAMES = {".git", "dist", "__pycache__"}


def mask_spans(value, spans):
    characters = list(value)
    for start, end in spans:
        characters[start:end] = " " * (end - start)
    return "".join(characters)


def mask_sentinels(line):
    return mask_spans(line, (match.span() for match in SENTINEL_RE.finditer(line)))


def span_distance(first, second):
    if first[1] < second[0]:
        return second[0] - first[1]
    if second[1] < first[0]:
        return first[0] - second[1]
    return 0


def has_dob(line):
    terms = [match.span() for match in DOB_TERM_RE.finditer(line)]
    dates = [match.span() for match in SLASH_DATE_RE.finditer(line)]
    dates.extend(match.span() for match in HYPHEN_DATE_RE.finditer(line))
    return any(span_distance(term, date) <= 40 for term in terms for date in dates)


def has_member_id(line):
    for label in ID_LABEL_RE.finditer(line):
        window = line[label.end() : label.end() + 40]
        for token_match in ID_TOKEN_RE.finditer(window):
            token = token_match.group(0)
            if any(character.isalpha() for character in token) and any(
                character.isdigit() for character in token
            ):
                return True
    return False


def has_name_beside_identifier(line):
    slash_dates = list(SLASH_DATE_RE.finditer(line))
    identifiers = list(ID_LABEL_RE.finditer(line))
    identifiers.extend(DOB_TERM_RE.finditer(line))
    identifiers.extend(SSN_RE.finditer(line))
    if not identifiers and not slash_dates:
        return False
    spans = [match.span() for match in identifiers]
    spans.extend(match.span() for match in slash_dates)
    candidate = mask_spans(line, spans)
    return CAPITALIZED_NAME_RE.search(candidate) is not None


def has_contact(line):
    for match in EMAIL_RE.finditer(line):
        address = match.group(0)
        local, domain = address.rsplit("@", 1)
        if local.lower().startswith("sentinel_"):
            continue
        if domain.lower() in {"recoupr.ai", "example.org"}:
            continue
        return True
    return PHONE_RE.search(line) is not None


def patterns_for_line(line):
    candidate = mask_sentinels(line)
    hits = []
    if has_dob(candidate):
        hits.append("dob")
    if has_member_id(candidate):
        hits.append("member-id")
    if SSN_RE.search(candidate):
        hits.append("ssn")
    if has_name_beside_identifier(candidate):
        hits.append("name-beside-id")
    if has_contact(candidate):
        hits.append("contact")
    return hits


def is_seeded_path(path):
    parts = path.resolve().parts
    for index in range(len(parts) - 2):
        if parts[index : index + 3] == ("tests", "fixtures", "seeded"):
            return True
    return False


def iter_files(target):
    if target.is_file():
        yield target
        return
    if not target.exists():
        raise FileNotFoundError(target)
    if not target.is_dir():
        return
    explicit_seeded = is_seeded_path(target)
    for directory, names, filenames in os.walk(target, followlinks=False):
        directory_path = Path(directory)
        kept = []
        for name in sorted(names):
            child = directory_path / name
            if child.is_symlink() or name in IGNORED_DIRECTORY_NAMES:
                continue
            if is_seeded_path(child) and not explicit_seeded:
                continue
            kept.append(name)
        names[:] = kept
        for filename in sorted(filenames):
            path = directory_path / filename
            if path.is_symlink():
                continue
            if is_seeded_path(path) and not explicit_seeded:
                continue
            yield path


def scan_file(path):
    try:
        data = path.read_bytes()
    except OSError as error:
        raise RuntimeError(f"{path}: {error}") from error
    if b"\0" in data:
        return []
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return []
    hits = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in patterns_for_line(line):
            hits.append((path, line_number, pattern))
    return hits


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    return parser.parse_args(argv)


def main(argv=None):
    arguments = parse_args(argv)
    hits = []
    seen_files = set()
    try:
        for target in arguments.paths:
            for path in iter_files(target):
                resolved = path.resolve()
                if resolved in seen_files:
                    continue
                seen_files.add(resolved)
                hits.extend(scan_file(path))
    except (FileNotFoundError, RuntimeError) as error:
        print(f"scan failed: {error}", file=sys.stderr)
        return 1
    for path, line_number, pattern in hits:
        print(f"{path.as_posix()}:{line_number}: {pattern}")
    if hits:
        print(f"Scan found {len(hits)} personal data pattern hit(s).")
        return 2
    print("Clean: no personal data patterns found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
