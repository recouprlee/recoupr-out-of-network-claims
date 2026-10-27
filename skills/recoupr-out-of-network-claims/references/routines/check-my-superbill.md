# check-my-superbill

Check a paper or PDF superbill for a client or therapist. Prepare a result only.
Never change a code, date, fee, diagnosis, provider detail, place of service,
modifier, or any other value. Never file anything for anyone.

References: `references/superbill-rules.md` and `references/codes.md`.

## 1. Intake

Say exactly:

```text
Please share the superbill or a clear photo of it. A redacted copy is fine. I
do not need an insurance card, plan document, or any other item for this check.
```

Accept a client-held copy or a therapist-held copy. Do not ask who will file a
claim. Do not ask for an unredacted copy when the labels and structure can be
checked on the redacted copy. Treat a visibly present but redacted client value
as present and not verified. Do not treat the redaction itself as a defect.

If a field needed for a shape, check digit, code-set, date, or arithmetic check
is hidden, state that the specific rule could not be checked from the redacted
copy. Do not guess, and do not ask for the hidden value.

## 2. Extract and confirm

Extract only what the superbill states. Show this confirmation sheet:

```text
superbill confirmation
practice name:
practice address:
practice phone:
provider name:
provider credentials:
provider license number:
provider license state:
NPI:
NPI type: type 1, type 2, or not stated
Tax ID:

service lines
date of service | CPT code | units | ICD-10 codes | diagnosis pointer |
charge | amount paid | place of service | telehealth modifier

total charge:
total paid:
source conflicts:
```

Ask exactly:

```text
Please confirm that this matches the superbill. I will not change or guess any
value.
```

If two parts of the document conflict, list both under `source conflicts`. Do
not choose one.

## 3. Run the rules

Open `references/superbill-rules.md`. Run every rule from SB-01 through SB-22
in order against the confirmed extraction. Do not substitute a coding opinion
for a listed structure check. Do not infer a diagnosis, service, modality,
location, provider identity, or billing entity.

Show a passing rule as:

```text
SB-xx | pass | field
```

Show a failed error as:

```text
SB-xx | error | field
fix list: <copy the rule's exact fix-list wording>
```

Show a warning as:

```text
SB-xx | warning | field
fix list: <copy the rule's exact fix-list wording>
person decision: confirm with the therapist or continue without changing it
```

For a hidden value, show:

```text
SB-xx | not checked from redacted copy | field
```

A `not checked` result is not a pass. It also is not a statement that the
superbill is wrong.

An error stops claim preparation until the therapist resolves it. A warning is
for the person to decide. Never turn a warning into a replacement code or
field. Never use the insurer, likely coverage, usual coding, or a similar
superbill to fill a value.

## 4. Give one fix list

If any rule fails, collect the exact fix-list wording from the failed rules in
rule order. Do not rewrite it. Give this request for the person to send to the
therapist:

```text
Please send a corrected superbill that resolves the items in this fix list
exactly as they should appear from your records:
<exact rule wording in SB order>

Please keep every code, date, fee, diagnosis, provider detail, place of
service, and modifier unchanged unless your records show that a correction is
required.
```

When a corrected superbill arrives, extract it again, ask for confirmation
again, and rerun every rule. Do not carry a corrected value into the new copy
from memory.

If every rule passes and there are no `not checked` results, say:

```text
superbill check: pass
No value was changed. This check covers the published structure rules only. It
does not predict coverage, reimbursement, or claim acceptance.
```

## 5. Optional local checker

For a plain-text copy in the label, colon, value fixture format, the person may
run:

```text
python3 scripts/check_superbill.py <text-copy.txt>
```

The script applies the deterministic parts of the same rules. Exit 0 means no
finding, exit 1 means warnings only, and exit 2 means at least one error. It
does not read a photo, use a network, rewrite a value, or decide whether a code
is clinically correct.

## 6. Close

End every result with exactly:

```text
You submit your own claim. Nothing was filed for you. Confirm the current route
and requirements on the insurer's own claims page before sending because that
page wins over this skill. This is not legal, medical, or billing advice.
```
