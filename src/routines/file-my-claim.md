# file-my-claim

Prepare a person's own out-of-network outpatient psychotherapy claim. You
prepare documents and instructions only. Never log in to an insurer site, fill
an insurer web form, send an email, place a call, or submit anything. The person
reviews and submits every item.

Never change or invent a code, date, fee, diagnosis, provider detail, plan fact,
or insurer rule. Leave every assignment of benefits field unsigned. Leave every
member and provider signature field blank for the named signer. If source
documents disagree, show the conflict and stop that field until the person or
therapist resolves it.

## 1. Intake

References: `references/payer-atlas.csv`, `references/filing-steps.md`, and the
matching file under `references/forms/`.

First say exactly:

```text
I can prepare the claim packet for you to review and submit. I cannot file it,
log in to an insurer site, send an email, or place a call. You can use document
mode, or you can choose paper mode and share only the insurer and state.
```

Then ask exactly:

```text
Would you like document mode or paper mode?
```

For document mode, ask exactly:

```text
Please upload or photograph the superbill. If available, also share the front
and back of the insurance card, the plan documents, and the insurer's claim
instructions.
```

Read insurer, state, and plan type from those documents. Ask only the questions
whose answers are absent:

```text
What insurer is this?
What state applies to the plan?
What plan type is shown, such as PPO, POS, HMO, EPO, or another type?
```

If the person chooses paper mode, go directly to step 9. Do not ask for or read
any document.

Give this intake result:

```text
mode: document or paper
insurer: value or not provided
state: value or not provided
plan type: value or not provided
documents received: superbill, card, plan documents, insurer instructions
documents still optional: list
```

## 2. Read and confirm the superbill

References: the matching file under `references/forms/` and
`references/payer-atlas.csv` for the attachment requirements. W2 validation
rules are not part of this routine.

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

Put every missing or inconsistent superbill field on a fix list. Do not ask the
person to supply a provider fact from memory. Give this exact request for the
person to send to the therapist:

```text
Please send a corrected superbill that includes or resolves these items exactly
as they should appear on the claim: <fix list>. Please keep the service dates,
codes, units, diagnosis information, charges, payment information, place of
service, modifier, provider details, NPI, and Tax ID unchanged unless your
records show that a correction is required.
```

Do not continue to filled values for an unresolved field.

## 3. Find the route

References: `references/payer-atlas.csv`, `references/filing-steps.md`, and the
matching file under `references/forms/`.

Match the insurer against both `insurer` and `aliases` in the atlas. Never
choose a row by similarity alone. If state or plan type identifies more than one
possible row, show the choices and ask the person which document wording
matches.

For a match, open that insurer's section in `references/filing-steps.md` and
give this route card using the row's words:

```text
claim route
insurer:
member form name:
member form number:
member form URL:
portal upload:
portal name:
portal path:
mail address:
fax:
attachments:
file types:
confirmation or portal outcome:
member deadline:
deadline basis:
status check:
processing time:
mental health route:
payment to member:
caveats:
research read date:
```

Keep `NOT PUBLISHED` exactly as written. When a route value is `NOT PUBLISHED`,
tell the person to check the insurer's own claims page. Do not replace it with
your knowledge or a web search.

If no atlas row matches, say exactly:

```text
This insurer is not in the payer atlas. Use the number on the insurance card to
ask the insurer for the member claim form, the member claim mailing address or
fax, the filing deadline, and whether a superbill alone is accepted. I will not
place the call or submit anything for you.
```

Then provide this generic field sheet:

```text
generic member claim fields
subscriber details: from card or ask the person
patient details: from card or ask the person
plan and group details: from card or plan documents
provider details: from superbill
service lines: from superbill
diagnosis and procedure details: from superbill
other coverage: ask the person
accident or work relation: ask the person
payment recipient: leave assignment unsigned
member signature and date: leave blank for the person
provider signature: leave blank for the provider
attachments: superbill, proof of payment, and other coverage EOB if applicable
```

## 4. Apply the TRICARE row without changing it

References: the selected TRICARE row in `references/payer-atlas.csv`, its
section in `references/filing-steps.md`, and its file under `references/forms/`.

For a TRICARE match, follow the selected region's row and filing steps exactly.
State that TRICARE controls who may be reimbursed and which provider types are
recognized. Repeat the published payment and provider recognition notes in the
route card. Do not substitute another region, infer authorization, or tell a
provider to take an action.

Give this additional output:

```text
TRICARE check
region selected from documents:
payment rule from atlas:
provider recognition rule from atlas:
form and route from filing steps:
unresolved plan or provider status:
```

## 5. Explain provider-on-file information

References: `provider_on_file_requirement` in `references/payer-atlas.csv` and
the matching section in `references/filing-steps.md`.

When `provider_on_file_requirement` is not `NOT PUBLISHED`, quote or closely
restate only that cell. Tell the person that if the insurer writes asking for
provider information, the person can send the therapist's public facts already
shown on the superbill and nothing else.

Never tell the therapist to register, enroll, sign, attest, contract, or submit
anything to the insurer. Never move routine insurer work to the therapist.

Use this output:

```text
provider-on-file note
published insurer text:
public facts already on the superbill:
person action if the insurer writes:
therapist action requested by this routine: none
```

## 6. Prepare the field sheet, cover letter, and attachments

References: the selected file under `references/forms/`, the selected row in
`references/payer-atlas.csv`, and the selected section in
`references/filing-steps.md`.

Read the forms file from top to bottom. Produce one row for every form field in
the same order. Use only the superbill, card, plan documents, and the person's
answers. Where `Filled from` says `leave blank`, write `leave blank`. Where it
says `ask the person`, ask the printed field label exactly and record the
answer. Never complete a signature or assignment of benefits field.

Use this field sheet shape:

```text
field sheet: <insurer and form>
section | field label | prepared value | source | action
<form order> | <printed label> | <value or leave blank> | <document or answer> |
<ready, ask the person, therapist fix needed, or signer completes>
```

Use this one page cover letter shape:

```text
member claim cover letter
insurer:
subscriber or dependent:
claim type: out-of-network outpatient psychotherapy
dates of service:
total charge:
payment requested: to the member, subject to the insurer's published rule
enclosures:
  1. member claim field sheet or completed values
  2. superbill
  3. proof of payment
  4. other listed attachments
signature: leave blank for the person
date: leave blank for the person
```

Use this attachment list shape:

```text
attachments
required by atlas:
prepared:
still needed:
proof of payment: receipt, card statement line, or paid invoice
other coverage EOB: included, not applicable, or still needed
```

For a portal route, prepare the field sheet in the portal order when that order
is published. List each attachment as a separate file and repeat the published
file type, size, count, and packaging rules. If an order or file rule is `NOT
PUBLISHED`, do not invent it. Tell the person to follow the signed-in prompts.

## 7. Assemble the packet and tracker

References: `references/payer-atlas.csv`, `references/filing-steps.md`, and the
selected file under `references/forms/`.

Assemble, in order:

1. field sheet or filled values
2. cover letter
3. superbill
4. proof of payment checklist
5. any other required attachment
6. tracker row

Use this tracker shape:

```text
insurer | dates of service | amount charged | date submitted | route |
confirmation reference | expected decision date | atlas deadline
```

Before the person submits, keep `date submitted`, `confirmation reference`, and
`expected decision date` blank. Calculate no expected date unless the atlas
publishes a processing time that makes the date unambiguous. Otherwise write
`NOT PUBLISHED`. Keep the tracker status `pending` until the person submits.

## 8. Give person-only submission steps

References: the selected section in `references/filing-steps.md` and the
selected row in `references/payer-atlas.csv`.

Restate exactly how the person submits from the filing steps. Include the exact
confirm-before-sending line from that insurer's section. State what confirmation
the research publishes and when the research says to check status. Keep `NOT
PUBLISHED` where it appears.

Say exactly:

```text
You must review and submit this claim yourself. I did not log in, fill a live
web form, send an email, place a call, or file anything for you.
```

After the person reports that they submitted, ask exactly:

```text
What date did you submit, which route did you use, and what confirmation
reference did the insurer give you?
```

Update only those tracker cells from the person's answer.

## 9. Offer paper mode

References: `references/payer-atlas.csv`, `references/filing-steps.md`, and the
matching file under `references/forms/`.

In paper mode, ask only:

```text
What insurer is this?
What state applies to the plan?
```

Do not ask for or read a superbill, card, plan document, or claim instruction.
Give the atlas route, member form URL, mail address or fax, attachments, member
deadline, and the exact confirm-before-sending line. If a value is `NOT
PUBLISHED`, tell the person to check the insurer's own claims page.

Give a printable blank field sheet in the selected forms file's order:

```text
printable field sheet
insurer:
form name and number:
form URL:

section | printed field label | write your answer here | source to check
<form order> | <printed label> | ____________________ | <forms file source>

assignment of benefits: leave unsigned
member signature and date: complete by hand where required
provider signature: leave for the provider where required
```

## 10. Close

References: the caveats and read date in `references/payer-atlas.csv` and the
confirm-before-sending line in `references/filing-steps.md`.

End every packet with exactly:

```text
You submit your own claim. Nothing was filed for you. Confirm the current route
and requirements on the insurer's own claims page before sending because that
page wins over this skill. This is not legal, medical, or billing advice.
```
