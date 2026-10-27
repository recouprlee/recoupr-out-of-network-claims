# Claim tracking and EOB reading

Research read date: 2026-10-27

## 1. Tracker columns

Use one CSV row per submitted claim. This is the `file-my-claim` row with
`status` and `notes` added.

| Column | What goes there | Source |
| --- | --- | --- |
| insurer | Exact matched atlas insurer | payer-atlas.csv |
| dates of service | Dates copied from the submitted packet | payer-atlas.csv |
| amount charged | Charge copied from the submitted packet | payer-atlas.csv |
| date submitted | Date the person says they submitted | payer-atlas.csv |
| route | Exact route the person says they used | filing-steps.md |
| confirmation reference | Exact submission reference the person received, or `NOT PUBLISHED` | payer-atlas.csv |
| expected decision date | Computed only from an applicable published period and the date from which that source measures | payer-atlas.csv; https://www.law.cornell.edu/cfr/text/29/2560.503-1 (Read date: 2026-10-27) |
| atlas deadline | Exact `member_deadline` cell | payer-atlas.csv |
| status | `prepared`, `submitted`, `received`, `in review`, `applied to deductible`, `partially paid`, `paid`, or `denied`, based only on the person's confirmation or EOB | claimStatusExplainer.ts; memberEobCopy.ts |
| notes | Exact unresolved fact, request, EOB result, payee, or next check basis | claimStatusExplainer.ts; memberEobCopy.ts |

CSV header:

```text
insurer,dates of service,amount charged,date submitted,route,confirmation reference,expected decision date,atlas deadline,status,notes
```

## 2. Follow-up cadence

Use the first applicable row. Never turn an unpublished or wrong-scope period
into a date.

| Priority | Period to use | When it applies | Source |
| --- | --- | --- | --- |
| 1 | Copy the exact `processing_time` value from the matched atlas row | Use it only when it publishes one unambiguous period that applies to this claim and route | payer-atlas.csv |
| 2 | `NOT PUBLISHED` for claim decisions | The DOCUMENTED rows with nonempty turnaround periods in the turnaround input state TIN registration or TRICARE provider certification scope, not post-service claim decision scope, so none supplies a claim follow-up period | L1-recognition-turnaround.csv |
| 3 | 30 calendar days after plan receipt; one extension of up to 15 calendar days when the regulation's conditions are met | Use only after the person confirms this is an employer plan subject to 29 CFR 2560.503-1 and supplies the plan receipt date | https://www.law.cornell.edu/cfr/text/29/2560.503-1 (Read date: 2026-10-27) |
| 4 | `NOT PUBLISHED` | Use when no applicable atlas period exists and the person cannot confirm the employer plan rule applies | payer-atlas.csv; https://www.law.cornell.edu/cfr/text/29/2560.503-1 (Read date: 2026-10-27) |

Exact federal post-service sentences from 29 CFR 2560.503-1(f)(2)(iii)(B):

> "In the case of a post-service claim, the plan administrator shall notify the claimant, in accordance with paragraph (g) of this section, of the plan's adverse benefit determination within a reasonable period of time, but not later than 30 days after receipt of the claim."

> "This period may be extended one time by the plan for up to 15 days, provided that the plan administrator both determines that such an extension is necessary due to matters beyond the control of the plan and notifies the claimant, prior to the expiration of the initial 30-day period, of the circumstances requiring the extension of time and the date by which the plan expects to render a decision."

Source: https://www.law.cornell.edu/cfr/text/29/2560.503-1

Read date: 2026-10-27

For an atlas range, use its upper endpoint as the next check. For business days,
count Monday through Friday and state that holiday treatment is `NOT PUBLISHED`
unless the source says otherwise. If two periods could apply, or the start event
is missing, show the exact periods and write `NOT COMPUTED` instead of choosing.

## 3. What to do at a check

| Stage | Where the person looks | What to record | Source |
| --- | --- | --- | --- |
| After submission | Use the exact matched atlas `status_check` cell | Current displayed status, check date, and confirmation reference | payer-atlas.csv |
| At the published next check | Use the same exact `status_check` route | Any change, request, EOB availability, or `no change` | payer-atlas.csv |
| Information requested | Read the insurer notice and plan document | Exact requested item and response deadline; the routine does not send it | memberEobCopy.ts |
| EOB available | Read every page of the person's EOB | Payee, outcome, billed, allowed, deductible, coinsurance, plan paid, patient responsibility, and denial code | memberEobCopy.ts; 21-eob-received.md |
| Denied or partly paid | Route the EOB and its code to `appeal-my-denial` | `denied` or `partially paid`; no code, date, fee, or diagnosis is changed | memberEobCopy.ts; 23-eob-denied-or-underpaid.md |

## 4. EOB outcomes in plain words

| EOB result | Plain words | Tracker status | Source |
| --- | --- | --- | --- |
| Paid to the member | The insurer approved reimbursement and says payment goes to the person. Record only the amount and payee printed on the EOB. | `paid` | claimStatusExplainer.ts; memberEobCopy.ts |
| Paid to the provider | The insurer approved an amount but says payment goes to the provider. Do not relabel it as member reimbursement. | `paid` with payee in notes | memberEobCopy.ts |
| Applied to the deductible | The claim may be covered even though the plan paid zero. The EOB says some or all of the allowed amount was credited to the deductible. | `applied to deductible` | eligibilityBenefitExplainer.ts; memberEobCopy.ts |
| Denied with a code | The insurer declined reimbursement and printed a reason code or message. Copy it exactly and hand the EOB to `appeal-my-denial`. | `denied` | claimStatusExplainer.ts; memberEobCopy.ts; 23-eob-denied-or-underpaid.md |
| Partially paid | The insurer paid some amount. Compare the printed allowed amount, deductible, coinsurance, plan paid, and patient responsibility without changing any value. Hand an apparent short payment to `appeal-my-denial`. | `partially paid` | memberEobCopy.ts; 23-eob-denied-or-underpaid.md |

## 5. Common EOB columns

| Column | Plain words | Source |
| --- | --- | --- |
| Billed | What the provider charged | memberEobCopy.ts |
| Allowed | The amount the plan used for covered claim arithmetic, which may be less than billed | eligibilityBenefitExplainer.ts; https://www.cms.gov/files/document/uniform-glossary-english-060723.pdf (Read date: 2026-10-27) |
| Deductible | The allowed amount credited to what the person must meet before plan payment begins | eligibilityBenefitExplainer.ts |
| Coinsurance | The person's or plan's stated percentage of the allowed amount after deductible; read the EOB label before deciding whose share it shows | eligibilityBenefitExplainer.ts |
| Plan paid | The amount the EOB says the plan paid | memberEobCopy.ts |
| Patient responsibility | The amount the EOB assigns to the person under its claim calculation; compare it with what was already paid but do not rewrite it | memberEobCopy.ts |
