#!/usr/bin/env python3
"""Run deterministic structure checks on a plain-text superbill."""

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


CPT_CODES = {
    "90785", "90791", "90792", "90832", "90833", "90834", "90836",
    "90837", "90838", "90839", "90840", "90845", "90846", "90847",
    "90849", "90853", "90863", "90875", "90876", "90880", "90885",
    "90887", "99202", "99203", "99204", "99205", "99211", "99212",
    "99213", "99214", "99215", "99354", "99355", "99366", "99367",
    "99368", "99417",
}
NON_INDIVIDUAL_CPT_CODES = {"90846", "90847", "90853"}
PLACE_OF_SERVICE_CODES = {"02", "03", "10", "11", "12", "49", "50", "53", "71", "72"}
TELEHEALTH_PLACE_OF_SERVICE_CODES = {"02", "10"}
ICD_10_DOTTED_RE = re.compile(r"^[A-Z]\d{2}(?:\.[0-9A-Z]{1,4})?$")
ICD_10_EDI_RE = re.compile(r"^[A-Z]\d{2}[0-9A-Z]{1,4}$")
FABRICATED_ICD_10_RE = re.compile(r"^U00[0-9]?$")
SESSION_RE = re.compile(r"^Session\s+(\d+)\s*$", re.IGNORECASE)
AMOUNT_RE = re.compile(r"^\$?\d+(?:\.\d{1,2})?$")

FIX = {
    "SB-01": "Please send a corrected superbill that includes the client's name and identity date exactly as shown in your records.",
    "SB-02": "Please send a corrected superbill that includes the practice name, practice address, practice phone, provider name, and provider credentials exactly as shown in your records.",
    "SB-03": "Please send a corrected superbill that includes the provider license number and license state exactly as shown in your records.",
    "SB-04": "Please check the NPI against your records and send a corrected superbill with the exact 10-digit NPI.",
    "SB-05": "Please check the NPI against your records and send a corrected superbill with the exact NPI if your record shows a correction is required.",
    "SB-06": "Please check the practice Tax ID against your billing records and send a corrected superbill with the exact 9-digit Tax ID. Never send a client's number.",
    "SB-07": "Please check the diagnosis code against the original clinical record and send a corrected superbill with the exact therapist-recorded code.",
    "SB-08": "Please check the diagnosis code against the original clinical record and replace the placeholder only with the exact therapist-recorded diagnosis code.",
    "SB-09": "Please send a corrected superbill that includes at least one service-line block for the session in your records.",
    "SB-10": "Please check the date of service against your records and send a corrected superbill with the exact date in YYYY-MM-DD form.",
    "SB-11": "Please check the CPT code against the original clinical record and send a corrected superbill with the exact 5-digit code.",
    "SB-12": "Please check the CPT code against the original clinical record and send a corrected superbill with the exact therapist-recorded code.",
    "SB-13": "Please check the place of service against the encounter record and send a corrected superbill with the exact 2-digit code.",
    "SB-14": "Please check the place of service and modifier against the encounter record and the insurer's own policy, then send a corrected superbill if your records show a correction is required.",
    "SB-15": "Please check the units against the original clinical record and send a corrected superbill with the exact positive whole number.",
    "SB-16": "Please check the charge against your billing records and send a corrected superbill with the exact positive amount.",
    "SB-17": "Please check the amount paid against your billing records and send a corrected superbill with the exact positive amount.",
    "SB-18": "Please check the diagnosis pointer against the original clinical record and send a corrected superbill with the exact pointer.",
    "SB-19": "Please check the total charge against your billing records and send a corrected superbill with the exact positive total.",
    "SB-20": "Please reconcile the stated total charge with the service-line charges in your billing records and send a corrected superbill with the exact recorded amounts.",
    "SB-21": "Please check the total paid against your billing records and send a corrected superbill with the exact positive total.",
    "SB-22": "Please confirm that the superbill identifies this person and the actual family or group service. Do not change the code unless your record shows that a correction is required.",
}


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    field: str

    def render(self):
        return f"{self.rule} | {self.severity} | {self.field} | {FIX[self.rule]}"


def normalized_label(value):
    return " ".join(value.strip().lower().split())


def parse_superbill(text):
    header = {}
    sessions = []
    current = None
    top_level_after_sessions = {"total charge", "total paid", "payment status"}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = SESSION_RE.fullmatch(line)
        if match:
            current = {"session number": match.group(1)}
            sessions.append(current)
            continue
        if ":" not in line:
            continue
        label, value = line.split(":", 1)
        key = normalized_label(label)
        target = header if current is None or key in top_level_after_sessions else current
        target[key] = value.strip()
    return header, sessions


def first_value(mapping, *labels):
    for label in labels:
        value = mapping.get(normalized_label(label), "").strip()
        if value:
            return value
    return ""


def sentinel_digits(value):
    if value.startswith("SENTINEL_"):
        match = re.search(r"_(\d+)$", value)
        return match.group(1) if match else ""
    return value


def npi_checksum_is_valid(value):
    identifier = [int(character) for character in value[:9]]
    total = 24
    for index, digit in enumerate(identifier):
        if (len(identifier) - 1 - index) % 2 == 0:
            product = digit * 2
            total += product // 10 + product % 10
        else:
            total += digit
    expected = (10 - total % 10) % 10
    return expected == int(value[-1])


def diagnosis_codes(session):
    value = first_value(session, "ICD-10 code", "ICD-10 codes")
    return [part for part in re.split(r"[,;\s]+", value) if part]


def parse_amount(value):
    if not AMOUNT_RE.fullmatch(value):
        return None
    try:
        amount = Decimal(value.lstrip("$"))
    except InvalidOperation:
        return None
    return amount if amount > 0 else None


def session_field(session, label):
    return f"Session {session['session number']} {label}"


def validate(header, sessions, today=None):
    today = today or date.today()
    findings = []

    client_fields = (
        first_value(header, "Client name", "Patient name"),
        first_value(
            header,
            "Identity date on card",
            "Client date of birth",
            "Patient date of birth",
            "Date of birth",
        ),
    )
    if not all(client_fields):
        findings.append(Finding("SB-01", "error", "Client identity"))

    provider_fields = (
        "Practice name",
        "Practice address",
        "Practice phone",
        "Provider name",
        "Provider credentials",
    )
    if not all(first_value(header, field) for field in provider_fields):
        findings.append(Finding("SB-02", "error", "Practice and provider details"))

    if not first_value(header, "Provider license number") or not first_value(
        header, "Provider license state"
    ):
        findings.append(Finding("SB-03", "error", "Provider license"))

    raw_npi = first_value(header, "NPI")
    npi = sentinel_digits(raw_npi)
    if not re.fullmatch(r"\d{10}", npi):
        findings.append(Finding("SB-04", "error", "NPI"))
    elif not (
        raw_npi.startswith("SENTINEL_") and npi == "0000000000"
    ) and not npi_checksum_is_valid(npi):
        findings.append(Finding("SB-05", "error", "NPI"))

    tax_id = sentinel_digits(first_value(header, "Tax ID"))
    if not re.fullmatch(r"\d{9}", tax_id):
        findings.append(Finding("SB-06", "error", "Tax ID"))

    for session in sessions:
        codes = diagnosis_codes(session)
        if not codes or not all(
            ICD_10_DOTTED_RE.fullmatch(code) or ICD_10_EDI_RE.fullmatch(code)
            for code in codes
        ):
            findings.append(
                Finding("SB-07", "error", session_field(session, "ICD-10 code"))
            )

    for session in sessions:
        for code in diagnosis_codes(session):
            if FABRICATED_ICD_10_RE.fullmatch(code):
                findings.append(
                    Finding("SB-08", "error", session_field(session, "ICD-10 code"))
                )

    if not sessions:
        findings.append(Finding("SB-09", "error", "Session blocks"))

    for session in sessions:
        value = first_value(session, "Date of service")
        try:
            parsed = date.fromisoformat(value)
            valid = parsed.isoformat() == value and parsed <= today
        except ValueError:
            valid = False
        if not valid:
            findings.append(
                Finding("SB-10", "error", session_field(session, "Date of service"))
            )

    for session in sessions:
        code = first_value(session, "CPT code")
        if not re.fullmatch(r"\d{5}", code):
            findings.append(
                Finding("SB-11", "error", session_field(session, "CPT code"))
            )

    for session in sessions:
        code = first_value(session, "CPT code")
        if re.fullmatch(r"\d{5}", code) and code not in CPT_CODES:
            findings.append(
                Finding("SB-12", "error", session_field(session, "CPT code"))
            )

    for session in sessions:
        value = first_value(session, "Place of service")
        if value not in PLACE_OF_SERVICE_CODES:
            findings.append(
                Finding("SB-13", "error", session_field(session, "Place of service"))
            )

    for session in sessions:
        modifiers = {
            item for item in re.split(r"[,;\s]+", first_value(session, "Telehealth modifier"))
            if item
        }
        if "95" in modifiers and first_value(
            session, "Place of service"
        ) not in TELEHEALTH_PLACE_OF_SERVICE_CODES:
            findings.append(
                Finding("SB-14", "error", session_field(session, "Telehealth modifier"))
            )

    for session in sessions:
        value = first_value(session, "Units")
        if not re.fullmatch(r"[1-9]\d*", value):
            findings.append(
                Finding("SB-15", "error", session_field(session, "Units"))
            )

    charges = []
    charges_valid = True
    for session in sessions:
        amount = parse_amount(first_value(session, "Charge"))
        if amount is None:
            charges_valid = False
            findings.append(
                Finding("SB-16", "error", session_field(session, "Charge"))
            )
        else:
            charges.append(amount)

    for session in sessions:
        if parse_amount(first_value(session, "Amount paid")) is None:
            findings.append(
                Finding("SB-17", "error", session_field(session, "Amount paid"))
            )

    for session in sessions:
        if not first_value(session, "Diagnosis pointer"):
            findings.append(
                Finding("SB-18", "error", session_field(session, "Diagnosis pointer"))
            )

    total_charge = parse_amount(first_value(header, "Total charge"))
    if total_charge is None:
        findings.append(Finding("SB-19", "error", "Total charge"))
    elif charges_valid and sessions and total_charge != sum(charges, Decimal("0")):
        findings.append(Finding("SB-20", "error", "Total charge"))

    if parse_amount(first_value(header, "Total paid")) is None:
        findings.append(Finding("SB-21", "error", "Total paid"))

    for session in sessions:
        if first_value(session, "CPT code") in NON_INDIVIDUAL_CPT_CODES:
            findings.append(
                Finding("SB-22", "warning", session_field(session, "CPT code"))
            )

    return findings


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("superbill", type=Path)
    return parser.parse_args(argv)


def main(argv=None):
    arguments = parse_args(argv)
    try:
        text = arguments.superbill.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"checker failed: {error}", file=sys.stderr)
        return 2
    findings = validate(*parse_superbill(text))
    for finding in findings:
        print(finding.render())
    if any(finding.severity == "error" for finding in findings):
        return 2
    if findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
