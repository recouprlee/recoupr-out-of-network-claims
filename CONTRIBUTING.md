# Contributing

## Insurer rows

Add or fix insurer rows in `src/references/payer-atlas.csv`. Keep this column
order:

`insurer,state,payer_id,member_form_url,form_revision,portal_upload,mail_address,fax,attachments,member_deadline,portal_shows_outcome,notes,source_url,verified_on`

Every row must have `source_url` and `verified_on`. Use a public source. Do not
add personal data.

## Local checks

Run these commands from the repository root:

```text
python3 tools/build.py
python3 tools/check_drift.py
python3 tools/phi_scan.py .
python3 -m unittest discover -s tests -v
bash tools/validate.sh
```

The build writes the four release renderings under `dist/`. It also mirrors the
built skill under `skills/recoupr-out-of-network-claims/` for plugin discovery.
A second mirror under the generated skill folder's `skills/` directory lets the
installed Claude Code CLI validate that folder directly. The ZIP is created
before that validator-only mirror and contains one portable skill folder.

## Personal data scan

Reference files describe insurers, which have phone numbers and capitalized
names. They never hold a person's data. The scan permits those two patterns in
reference files, but email, birth date, identifier-value and SSN patterns still
run on them.

Fixtures use obvious `SENTINEL_` tokens for every person-like field. Seeded
scanner fixtures must also carry an obvious sentinel marker. Never use a real
name, birth date, address, contact value, member ID, policy ID or claim ID.

Do not use em dash or en dash characters. Write the company name as `recoupr`
in lowercase. The personal data scan runs in CI and blocks a merge on any hit.

Code and the skill instructions use the Apache License 2.0 in `LICENSE`. Files
under `src/references/` use the Creative Commons Attribution 4.0 International
license in `LICENSE-CONTENT`.
