# track-my-claim

Build or update a person's own claim tracker and read their EOB in plain words.
Never log in, call, email, submit, or appeal anything. Never change a code,
date, fee, diagnosis, EOB value, or insurer fact.

References: `references/tracking.md` and `references/payer-atlas.csv`.

## 1. Intake

Ask for:

```text
insurer and state
existing tracker rows, if any
dates of service and amount charged
date and route submitted
confirmation reference and insurer receipt date, if published or shown
current displayed status
the EOB, if it has arrived
```

Use only what the person supplies and the exact matched atlas row. Match both
insurer and aliases. Do not select by similarity.

## 2. Build or update the CSV

Use this header and one line per claim:

```text
insurer,dates of service,amount charged,date submitted,route,confirmation reference,expected decision date,atlas deadline,status,notes
```

Quote a CSV cell when it contains a comma, quote, or line break. Keep an absent
person-supplied value blank. Copy `member_deadline` exactly into `atlas
deadline`. Before submission, use `prepared`. After the person reports
submission, use `submitted`. Change status again only from the person's status
display, confirmation, or EOB.

Give the CSV lines in a fenced code block so the person can paste them into a
spreadsheet.

## 3. Compute the next check only from a published period

Follow the cadence priority in `references/tracking.md`.

1. Use an applicable, unambiguous atlas `processing_time` first.
2. Do not use the recognition turnaround input for a claim decision. Its documented periods concern TIN registration or provider certification.
3. Use the federal 30 calendar day post-service period only when the person confirms an employer plan subject to that rule and supplies the insurer receipt date.
4. Otherwise write `NOT PUBLISHED` for the period and `NOT COMPUTED` for the expected decision date.

For a published range, use the upper endpoint. For a published business-day
period, count Monday through Friday and state `holiday treatment: NOT
PUBLISHED` unless the source states it. If the source measures from receipt,
never substitute the submission date. If more than one period may apply, show
each exact period and do not choose.

Show:

```text
next check
published period:
period source:
start event required by source:
start date supplied by person:
next check date or NOT COMPUTED:
where to look: exact atlas status_check cell
```

## 4. Check status

Tell the person where to look by copying the matched atlas `status_check` cell.
The person signs in or makes any call. The routine does neither. Ask the person
to return with the displayed status, check date, any request, and whether an EOB
is available. Add those exact facts to `status` and `notes`.

## 5. Read an EOB

Read every uploaded page. Extract only printed values:

```text
EOB summary
insurer:
dates of service:
outcome: paid, partially paid, denied, or NOT FOUND
paid to: member, provider, or NOT FOUND
billed:
allowed:
deductible:
coinsurance:
plan paid:
patient responsibility:
denial code and exact message:
EOB date:
page and row for each value:
conflicts:
```

Use the plain-words outcome and column maps in `references/tracking.md`. Do not
infer the payee from a payment amount. Do not infer a denial code from the
amount paid. Write `NOT FOUND` for an absent value.

Update the CSV row from the EOB. Put the exact payee, denial code, and unresolved
conflict in `notes`. Keep any earlier submission confirmation.

For a denial or apparent short payment, say:

```text
This EOB is ready for appeal-my-denial. That routine can prepare an appeal for
you to review. Nothing has been filed, called, emailed, or submitted.
```

## 6. Close

End exactly:

```text
You check and submit your own claim. Nothing was filed, called, emailed, or
changed for you. Confirm the current status route on the insurer's own claims
page because that page wins over this skill. This is not legal, medical, or
billing advice.
```
