# Expected packet: UnitedHealthcare

Human-judge documentation for `superbill-unitedhealthcare.txt`.

## Superbill confirmation

| Field | Confirmed value |
| --- | --- |
| Practice name | Example Counseling |
| Practice address | SENTINEL_PROVIDER_ADDRESS_2, Example Street, Example City, EX 00000 |
| Practice phone | SENTINEL_PROVIDER_PHONE_2 |
| Provider name | SENTINEL_PROVIDER_NAME_2 |
| Credentials | LCSW |
| License number and state | SENTINEL_PROVIDER_LICENSE_2, EX |
| NPI and type | SENTINEL_NPI_2_0000000000, type 1 |
| Company Tax ID | SENTINEL_TAX_ID_2_000000000 |
| First service | 2026-10-01, 90837, 1 unit, F99, pointer 1, 150.00 paid, place 10, modifier 95 |
| Second service | 2026-10-08, 90837, 1 unit, F99, pointer 1, 150.00 paid, place 10, modifier 95 |
| Total | 300.00 charged and 300.00 paid |

Fix list: none for the fields the fixture states. Ask the person about the
policyholder relationship, gender, new-address answer, accident, and other
coverage. Do not infer those answers.

## Route card

| Field | Atlas value |
| --- | --- |
| Insurer | UnitedHealthcare, including Optum behavioral health |
| Member form | Medical Claim Form M57270, revision 5/19 |
| Form URL | https://member.uhc.com/myuhc/content/dam/myuhc/pdfs/claim-forms/CMS1500ClaimForm010402.pdf |
| Portal upload | YES |
| Portal | UnitedHealthcare member account |
| Portal path | Claims & Accounts > Submit a claim |
| Mail address | NOT PUBLISHED |
| Fax | NOT PUBLISHED |
| File types | NOT PUBLISHED; signed-in form is UNREADABLE |
| Confirmation | EOB after processing; submission reference is NOT PUBLISHED for domestic commercial route |
| Deadline | NOT PUBLISHED; submit as soon as possible |
| Deadline basis | YES: employer plan and controlling plan document set the limit |
| Status | Member account EOB; UnitedHealthcare app can show claims |
| Processing time | Many claims are processed within 14 business days; reimbursement check may take up to 30 days after processing |
| Payment | NOT PUBLISHED; INFERRED: leave the direct-to-provider assignment box unchecked |
| Caveat | Out-of-network benefits, authorization, behavioral administrator, and filing limit are plan specific; Medicare Advantage and Medicaid are excluded |
| Read date | 2026-10-09 |

## Field sheet in form order

| Section | Field label | Prepared value | Source or action |
| --- | --- | --- | --- |
| identification | member id from health plan card | SENTINEL_MEMBER_ID_2 | fixture card details |
| identification | group number | SENTINEL_GROUP_NUMBER_2 | fixture card details |
| patient information | name | SENTINEL_CLIENT_NAME_2 | fixture card details |
| patient information | birth field as printed | SENTINEL_BIRTH_DATE_2 | fixture card details |
| patient information | home address | SENTINEL_CLIENT_ADDRESS_2 | fixture card details |
| patient information | city | ask the person | address components are not stated |
| patient information | state | ask the person | plan state is not an address |
| patient information | ZIP code | ask the person | address components are not stated |
| patient information | gender | ask the person | absent from fixture |
| patient information | relationship to subscriber or policyholder | ask the person | absent from fixture |
| patient information | new address? | ask the person | absent from fixture |
| patient information | phone | SENTINEL_CLIENT_PHONE_2 | fixture card details |
| policyholder information | employee name | ask the person | complete if different |
| policyholder information | phone | ask the person | complete if different |
| policyholder information | home address | ask the person | complete if different |
| policyholder information | birth field as printed | ask the person | complete if different |
| policyholder information | city | ask the person | complete if different |
| policyholder information | state | ask the person | complete if different |
| policyholder information | ZIP code | ask the person | complete if different |
| policyholder information | new address? | ask the person | complete if different |
| provider information | provider or rendering provider name | SENTINEL_PROVIDER_NAME_2 | superbill |
| provider information | provider Tax ID | SENTINEL_TAX_ID_2_000000000 | superbill |
| provider information | NPI number | SENTINEL_NPI_2_0000000000 | superbill |
| provider information | group or facility name | Example Counseling | superbill |
| provider information | provider address | SENTINEL_PROVIDER_ADDRESS_2, Example Street, Example City, EX 00000 | superbill |
| provider information | address where services were rendered | SENTINEL_PROVIDER_ADDRESS_2, Example Street, Example City, EX 00000 | superbill |
| provider information | city | Example City | superbill |
| provider information | state | EX | superbill |
| provider information | ZIP code | 00000 | superbill |
| provider information | phone number | SENTINEL_PROVIDER_PHONE_2 | superbill |
| accident information | date of accident | ask if applicable | person answer |
| accident information | type of accident | ask if applicable | person answer |
| accident information | how did the accident happen? | ask if applicable | person answer |
| other insurance | is the patient covered by another plan? | ask the person | absent from fixture |
| other insurance | name of person carrying other insurance | ask if yes | card or person |
| other insurance | birth field as printed | ask if yes | card or person |
| other insurance | name of other insurance carrier | ask if yes | card or person |
| other insurance | policy number | ask if yes | card or person |
| other insurance | employer name | ask if yes | person answer |
| other insurance | effective date | ask if yes | card or person |
| other insurance | cancellation date | ask if applicable | card or person |
| other insurance | other carrier EOB attached? | ask if yes | person answer |
| assignment of benefits | direct provider payment box | leave blank | assignment stays unsigned |
| certification | signature | leave blank | person signs by hand |
| certification | date | leave blank | person dates by hand |

## Cover letter

```text
member claim cover letter
insurer: UnitedHealthcare
subscriber or dependent: ask the person
claim type: out-of-network outpatient psychotherapy
dates of service: 2026-10-01 and 2026-10-08
total charge: 300.00
payment requested: to the member, while retaining the atlas payment caveat
enclosures: Medical Claim Form M57270, superbill, proof of payment, and other
insurance EOB if applicable
signature: leave blank for the person
date: leave blank for the person
```

## Attachments and tracker

- Prepared: form field sheet and superbill with the required service details.
- Still needed: person answers, person signature, and a receipt, card statement
  line, or paid invoice.
- Other coverage EOB: ask the person and include only when applicable.

```text
UnitedHealthcare | 2026-10-01; 2026-10-08 | 300.00 |
<blank until submitted> | member account | <blank until received> |
NOT PUBLISHED | NOT PUBLISHED; submit as soon as possible
```

## Person-only submission

The person signs in, opens Claims & Accounts, selects Submit a claim, follows
the signed-in prompts, and attaches the form, superbill, receipts, and any
primary carrier EOB. File types and a submission reference are not published.
The person retains the result and checks the member account EOB. Nothing is
filed by the routine.
