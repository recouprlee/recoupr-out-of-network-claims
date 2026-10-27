# read-my-benefits

Read a person's own out-of-network outpatient psychotherapy benefits. Prepare
an explanation and arithmetic only. Never log in, place a call, send an email,
file anything, or change a code, date, fee, diagnosis, or plan value.

Reference: `references/benefits.md`.

## 1. Intake

Say exactly:

```text
I can read the benefit pages you share, or give you a script for your own call.
I cannot log in, call, email, or contact the insurer for you. I will not guess a
missing plan value.
```

Then ask:

```text
Do you have the Summary of Benefits and Coverage or plan document pages? If
not, do you have the insurance card and are you willing to call member services
yourself with a script?
```

Use document mode when pages are shared. Use call mode only when the person
chooses to make the call. If neither is available, explain how to request the
SBC and stop with every benefit field `NOT FOUND`.

## 2. Document mode

Open the SBC field map in `references/benefits.md`. Read only the shared pages.
For every value, retain the document's own network term. Do not treat an
in-network number as out-of-network. Do not treat a coverage period as the plan
year when the document does not say that.

Show:

```text
benefit reading
plan and document title:
coverage period:
plan year start:
out-of-network outpatient mental health covered:
out-of-network individual deductible:
out-of-network family deductible:
individual deductible met or remaining:
family deductible met or remaining:
plan share after deductible:
out-of-network out-of-pocket limit:
out-of-network out-of-pocket met or remaining:
visit limit and remaining visits:
authorization requirement:
referral requirement:
allowed amount for CPT 90837:
allowed amount for CPT 90834:
allowed amount for CPT 90791:
allowed amount basis:

source for each found value
field | exact value | page | row or heading
```

Write `NOT FOUND` for an absent value and page or row. Show conflicting values
side by side and do not choose one. Offer the matching call question only for a
missing or conflicting field.

## 3. Call mode

Open `Nine member services questions` in `references/benefits.md`. Give all
nine questions in their exact order. Remind the person:

```text
You make the call. Write the answer exactly. Also write down the
representative's name, the call date, and the reference number.
```

After the person returns, take the answers without rewording a number. Show the
same `benefit reading` sheet. Put `CALL ANSWER` in the page column and the
question number in the row or heading column. Use `NOT FOUND` for every
unanswered field.

## 4. Estimate one session

Explain first:

```text
The insurer's allowed amount decides the covered base. The therapist's charge
does not become the allowed amount. This estimate is not a promise of payment.
```

Ask for these five numbers only if they are stated in the document or call
answers:

```text
charge
allowed amount for this CPT code
out-of-network deductible remaining
coinsurance percent that the plan pays
out-of-network out-of-pocket remaining
```

If any number is absent, negative, or disputed, do not run an estimate. Say
which input is missing and use the matching call question. Never supply a
default.

When all five are present, use the arithmetic in `references/benefits.md` or:

```text
python3 scripts/estimate_benefit.py CHARGE ALLOWED_AMOUNT DEDUCTIBLE_REMAINING PLAN_SHARE_PERCENT OUT_OF_POCKET_REMAINING
```

Repeat every input beside its document page, row, or call question. Then show:

```text
one-session estimate
amount applied to deductible:
plan expected payment:
person expected cost:
remaining deductible:
remaining out-of-pocket:
allowed amount source:
plan rule not represented by this arithmetic:
```

If the plan states a copay, special limit, authorization penalty, excluded
service, or different out-of-pocket treatment, list it as not represented. Do
not adjust the calculator by judgment.

## 5. Close

End exactly:

```text
You read your own plan documents or make your own call. Nothing was filed or
changed for you. Confirm the current benefits and allowed amount with the
insurer because the plan document and insurer decision control. This is not
legal, medical, or billing advice.
```
