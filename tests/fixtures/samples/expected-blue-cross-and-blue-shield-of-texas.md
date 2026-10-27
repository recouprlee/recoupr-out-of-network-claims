# Expected packet: Blue Cross and Blue Shield of Texas

Human-judge documentation for
`superbill-blue-cross-and-blue-shield-of-texas.txt`.

## Superbill confirmation

| Field | Confirmed value |
| --- | --- |
| Practice name | Example Counseling |
| Practice address | SENTINEL_PROVIDER_ADDRESS_1, Example Street, Example City, EX 00000 |
| Practice phone | SENTINEL_PROVIDER_PHONE_1 |
| Provider name | SENTINEL_PROVIDER_NAME_1 |
| Credentials | LCSW |
| License number and state | SENTINEL_PROVIDER_LICENSE_1, EX |
| NPI and type | SENTINEL_NPI_1_0000000000, type 1 |
| Company Tax ID | SENTINEL_TAX_ID_1_000000000 |
| First service | 2026-10-01, 90837, 1 unit, F99, pointer 1, 150.00 paid, place 10, modifier 95 |
| Second service | 2026-10-08, 90837, 1 unit, F99, pointer 1, 150.00 paid, place 10, modifier 95 |
| Total | 300.00 charged and 300.00 paid |

Fix list: none for the fields the fixture states. Do not infer client sex,
subscriber relationship, employment, accident, illness onset, other coverage,
or Medicare answers.

## Route card

| Field | Atlas value |
| --- | --- |
| Insurer | Blue Cross and Blue Shield of Texas (HCSC), including ERS HealthSelect |
| Member form | Claim Form 730526, revision 0424 |
| Form URL | https://www.bcbstx.com/docs/forms/claim/tx/medical-claim-tx.pdf |
| Portal upload | YES |
| Portal | Blue Access for Members (BAM) |
| Portal path | BAM Message Center > Create a new message > attach form and original provider bill > subject Claims Submission Attachments > Send |
| Mail address | NOT PUBLISHED |
| Fax | NOT PUBLISHED |
| File types | NOT PUBLISHED; login pop-up is UNREADABLE |
| Confirmation | NOT PUBLISHED |
| Deadline | Individual and family plans: end of the following calendar year; HealthSelect: 18 months from date of service; other group plans: NOT PUBLISHED |
| Deadline basis | YES: individual and family, ERS HealthSelect, and employer or self-funded terms differ |
| Status | BAM or BCBSTX Mobile App > Claims; BAM alerts are available; phone status is also published |
| Processing time | NOT PUBLISHED |
| Payment | Select To pay Insured/Subscriber; do not select in-network credit |
| Caveat | Coverage and filing rules depend on the controlling plan; HMO or EPO plans may have no routine out-of-network benefit; Medicare Advantage and Medicaid are excluded from this commercial member route |
| Read date | 2026-10-09 |

## Field sheet in form order

| Section | Field label | Prepared value | Source or action |
| --- | --- | --- | --- |
| Payment selection | To pay Insured/Subscriber | unresolved | atlas says select this; forms file says leave blank; person must confirm on current form |
| Payment selection | To get in-network credit for your cash payment to a provider | leave blank | forms file says leave blank |
| 1 | Insured/Subscriber Name (Last, First, Middle Initial) | ask the person | do not assume the client is the subscriber |
| 1 | Mailing Address | ask the person | do not assume the client is the subscriber |
| 1 | City and State | ask the person | card or person |
| 1 | ZIP Code | ask the person | card or person |
| 1 | Insured Employed? | ask the person | person answer |
| 1 | Date of Retirement | ask if retired | person answer |
| 2 | Group Number | SENTINEL_GROUP_NUMBER_1 | fixture card details |
| 2 | Insured/Subscriber Identification Number (from ID card) | SENTINEL_MEMBER_ID_1 | fixture card details |
| 2 | Patient's Full Name (Last, First, Middle) | SENTINEL_CLIENT_NAME_1 | fixture card details |
| 2 | Patient's Sex | ask the person | absent from fixture |
| 2 | birth field (label as printed) | SENTINEL_BIRTH_DATE_1 | fixture card details |
| 2 | Patient's Relationship to Insured | ask the person | absent from fixture |
| 3 | Type of treatment received | outpatient psychotherapy | superbill |
| 3 | Injury - Date of accident | ask the person | complete only if injury applies |
| 3 | Illness - Date of first symptom | ask the person | absent from fixture |
| 3 | Pregnancy - Date of conception | ask the person | complete only if applicable |
| 3 | Preventive - Date of service | not applicable unless person confirms | do not infer |
| 4 | Describe diagnosis, symptoms, or care | F99; outpatient psychotherapy | superbill |
| 5 | Was illness or injury work connected? | ask the person | absent from fixture |
| 5 | Name and address of employer | ask if yes | person answer |
| 6 | If injury, was a motor vehicle involved? | ask if injury | person answer |
| 7 | Other health benefits plan? | ask the person | absent from fixture |
| 7 | Insurance Co. | ask if yes | card or person |
| 7 | Address | ask if yes | card or person |
| 7 | Employer | ask if yes | person answer |
| 7 | Insured name | ask if yes | card or person |
| 7 | Policy # | ask if yes | card or person |
| 7 | Effective date of coverage | ask if yes | card or person |
| 7 | Sex of Insured | ask if yes | card or person |
| 7 | birth field (label as printed) | ask if yes | card or person |
| 7 | Relationship to patient | ask if yes | card or person |
| 8 | Entitled to Medicare Part A? | ask the person | absent from fixture |
| 8 | Part A Effective | ask if yes | card or person |
| 8 | Entitled to Medicare Part B? | ask the person | absent from fixture |
| 8 | Part B Effective | ask if yes | card or person |
| 8 | Medicare due to a disability? | ask the person | absent from fixture |
| 8 | Disability Effective | ask if yes | card or person |
| 8 | Patient's Medicare Identification Number | ask if applicable | card or person |
| 9 | Signature of Insured | leave blank | person signs by hand |
| 9 | Date | leave blank | person dates by hand |
| 9 | Daytime telephone number | SENTINEL_CLIENT_PHONE_1 | fixture card details, confirm subscriber use |
| 10 | Total amount for all covered services and supplies | 300.00 | superbill |

## Cover letter

```text
member claim cover letter
insurer: Blue Cross and Blue Shield of Texas
subscriber or dependent: ask the person
claim type: out-of-network outpatient psychotherapy
dates of service: 2026-10-01 and 2026-10-08
total charge: 300.00
payment requested: to the member, subject to the atlas payment rule
enclosures: Claim Form 730526, superbill, and proof of payment
signature: leave blank for the person
date: leave blank for the person
```

## Attachments and tracker

- Prepared: form field sheet and superbill.
- Still needed: person answers, person signature, and proof of payment such as
  a receipt, card statement line, or paid invoice.
- Other coverage EOB: ask the person and include only when applicable.

```text
Blue Cross and Blue Shield of Texas | 2026-10-01; 2026-10-08 | 300.00 |
<blank until submitted> | BAM Message Center | <blank until received> |
NOT PUBLISHED | atlas deadline above
```

## Person-only submission

The person completes and signs the current form, attaches the original provider
bill and proof of payment, and follows the BAM Message Center path above. The
person confirms the current portal path before sending, retains the submission
result, and checks Claims in BAM. Nothing is filed by the routine.
