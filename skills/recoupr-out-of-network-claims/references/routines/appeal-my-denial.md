# appeal-my-denial

Prepare a person's own correction or appeal packet for an out-of-network
psychotherapy claim. Draft from the supplied records only. Never log in, file,
send, fax, email, call, sign, or submit anything. The person reviews, signs,
and sends the packet.

Never assert medical necessity beyond the therapist's signed documentation.
Never propose or change a diagnosis, procedure code, modifier, place of
service, date, fee, or provider fact. Never invent a fact, date, quotation,
deadline, route, or plan term. Use `[ASK]` for every missing fact.

References: `references/eob-codes.md`, `references/appeals.md`,
`references/payer-appeals.csv`, and `scripts/appeal_clock.py` in the repository.

## 1. Intake

First say exactly:

```text
I can prepare a correction or appeal packet for you to review, sign, and send.
I cannot file it, log in, send a message, fax, mail, place a call, or sign for
you. Nothing will be sent for you.
```

Ask for:

```text
Please share the complete EOB and denial letter, including the code and appeal
rights sections. Also share the superbill, the plan type, and the claim's
tracker row if you have it.
```

Ask only for items still absent:

```text
What exact insurer name appears on the EOB or card?
Is the plan employer, individual, or government coverage?
What state and policy situs are shown in the plan documents?
On what ISO date did you receive the denial notice, if known?
Did the insurer print an appeal deadline or submission route?
```

For government coverage, ask which program the notice names. Do not convert a
government plan into an employer or individual plan to obtain a date.

Give this intake record:

```text
documents received: EOB, denial letter, superbill, tracker row, plan pages
documents missing: [list]
insurer: [record value or [ASK]]
plan type: [employer, individual, government, or [ASK]]
government program: [record value, not applicable, or [ASK]]
state: [record value or [ASK]]
policy situs: [record value or [ASK]]
notice date: [record value or [ASK]]
received date: [person answer or [ASK]]
printed deadline: [exact text or NOT PUBLISHED]
printed route: [exact text or NOT PUBLISHED]
```

## 2. Read the notice

Extract only what the EOB and denial letter state. Do not paraphrase away a
qualification. Show:

```text
notice reading
claim number:
dates of service:
amount billed:
amount allowed:
amount paid:
member responsibility:
adjustment and remark codes:
denial reason as printed:
denial reason in plain words:
appeal-rights paragraph:
deadline as printed:
route as printed:
records or information requested:
plan term or criterion cited:
source conflicts:
```

If two records conflict, list both under `source conflicts`. Do not choose one.
If the complete appeal-rights paragraph is missing, request it before finalizing
the route or deadline.

## 3. Look up every code

For each code, find the exact code and code-list label in
`references/eob-codes.md`. Do not treat a CARC as a RARC or claim-status code.
Give:

```text
code | official description | plain-words meaning | bucket | next step |
notice text that accompanies it
```

Keep the bucket as a triage label. Never let a code or bucket decide the result
by itself. If the code is absent from the reference, write `NOT PUBLISHED` and
use only the notice's words. If A1, A2, or A3 appears without a named code list,
write `CODE LIST [ASK]` and do not select a meaning.

## 4. Decide correction or appeal

Open section 1 of `references/appeals.md`. Apply the rule to the notice and
records, not to a prediction or likelihood.

Choose `correction` only when all are true:

1. the notice names a missing, incomplete, or incorrect claim item
2. an existing record supplies or resolves that exact item
3. no diagnosis, code, date, fee, or provider fact must be guessed or changed

Choose `appeal` when the notice makes a benefit decision, including a coverage,
medical-necessity, authorization, limit, exclusion, or plan-interpretation
decision, and the records give a basis to request review.

Choose `UNRESOLVED` when the reason, record support, or appeal rights are
missing or conflicting. If the notice contains both a paperwork request and a
benefit decision, prepare the correction and preserve the appeal as a separate
rung. A correction does not prove that an appeal deadline paused.

Show the decision without a score:

```text
decision: correction, appeal, or UNRESOLVED
rule applied:
notice evidence:
record evidence:
missing evidence:
facts not inferred:
appeal clock preserved: yes
```

## 5. Set the clocks

Use the notice first. Copy every printed deadline exactly and label its source.
When a letter states a different deadline from a computed planning date, show
both and use this sentence exactly:

```text
The insurer's letter controls where it states a different deadline.
```

If an employer or individual notice has no printed deadline, use the notice
date or the person's received date with:

```text
python3 scripts/appeal_clock.py <notice-date> <employer-or-individual>
```

When the person supplies a received date, add:

```text
--received-date <received-date>
```

The script's appeal date uses the periods quoted in section 2 of
`references/appeals.md`. Its external-review date is a planning date. Recheck
it from the final internal decision and controlling state or federal route when
that rung opens. Do no arithmetic yourself and do not add grace periods.

For a government plan, run the script only to confirm its exit 2 refusal. Use
the program notice. If the notice has no deadline, write `NOT PUBLISHED`.

Give:

```text
clock source: denial letter, received date, regulation planning baseline, or government notice
basis date:
printed appeal deadline:
planning appeal-by date:
planning external-review request-by date:
deadline conflicts:
The insurer's letter controls where it states a different deadline.
```

## 6. Find the route

Match the EOB insurer to the exact `insurer` string in
`references/payer-appeals.csv`. Never choose by similarity. If more than one
row may apply, show the exact choices and ask which wording matches the card,
plan, or notice.

Copy the selected row without shortening caveats:

```text
appeal route
insurer:
appeal form or letter:
portal upload:
portal path:
internal deadline:
internal levels:
external review:
include list:
mental-health-specific route:
fax:
mail:
source URL:
verified on:
```

The denial notice wins over the payer row for the current claim. Keep
`NOT PUBLISHED`, `UNREADABLE`, `INFERRED`, and product limits exactly as written.
Do not turn a provider route into a member route.

For external review and a regulator complaint, find the state in section 4 of
`references/appeals.md`. Use policy situs when the plan records state it. If
the applicable state or funding rule is unresolved, show that conflict and do
not select a route. Other states remain `NOT PUBLISHED`.

## 7. Draft the matching letter

Select exactly one shape from section 6 of `references/appeals.md`:

- paperwork fix: reconsideration
- first benefit review: first-level internal appeal
- final eligible benefit review: external review request
- documented regulator concern: regulator complaint

For a published second internal level, use the first-level shape, change only
the heading to `second-level appeal`, and attach the first-level decision.

Fill each bracketed field only from the EOB, denial letter, superbill, plan
records, tracker, or person's answer. Replace every absent value with `[ASK]`.
Quote or closely restate only the reason actually printed. Include the fixed
payment-to-member paragraph and fixed claim-file request. Leave signature and
date blank. Do not add a diagnosis or code discussion that is not already in
the records.

Use the optional parity paragraph only when the records contain both the
mental-health term and a medical or surgical comparison. Cite only 29 U.S.C.
1185a(a)(3)(A) and the 2013 final rule, 78 FR 68240. Ask for review under those
sources. Never state that a violation occurred and never cite a later rule.

After the draft, show:

```text
draft audit
every fact and its source:
every [ASK] field:
medical-necessity statement source:
diagnosis or code changed: no
fact, date, or quotation invented: no
signature completed: no
date completed: no
```

## 8. Build the attachments list

Use section 7 of `references/appeals.md` and the selected payer include list.
Separate what is present from what is still needed:

```text
attachments present:
attachments still needed:
not requested by this route:
representative form: include only if the person chose a representative
clinical records: only those relevant to the printed reason
```

Never request an entire clinical file by default. Do not attach a new therapist
statement unless the denial reason and record need it.

## 9. Show the rungs ahead

Use the selected payer row, decision notice, and section 3 of
`references/appeals.md`. Show each rung even when its details are unknown:

```text
rung | opens when | route | deadline | required decision or proof
correction or reconsideration |
first-level internal appeal |
second-level internal appeal |
external review |
state regulator complaint |
```

Write `not offered in published row` only when the payer row says so. Otherwise
use `NOT PUBLISHED`. Do not imply that a complaint replaces an appeal or that
external review covers every reimbursement dispute.

## 10. Ask the therapist only when needed

For a missing or disputed code, date, modifier, place of service, diagnosis,
fee, or provider fact, ask the person to request a corrected superbill based on
the therapist's records. Do not suggest a replacement value.

When the denial says a therapist medical-necessity letter is the missing piece,
copy the exact request in section 8 of `references/appeals.md`. Do not expand it
with clinical claims. The person sends the request. This routine sends nothing
and does not ask the therapist to file, appeal, register, enroll, or call.

## 11. Close

End every result with exactly:

```text
You sign and send your own correction or appeal. Nothing was filed or sent for
you. Confirm the current route, deadline, and requirements in the denial notice
and on the insurer's own appeal page before sending because those current
instructions control. This is not legal, medical, or billing advice.
```
