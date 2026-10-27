# Expected packet: Aetna

Human-judge documentation for `superbill-aetna.txt`.

## Superbill confirmation

| Field | Confirmed value |
| --- | --- |
| Practice name | Example Counseling |
| Practice address | SENTINEL_PROVIDER_ADDRESS_3, Example Street, Example City, EX 00000 |
| Practice phone | SENTINEL_PROVIDER_PHONE_3 |
| Provider name | SENTINEL_PROVIDER_NAME_3 |
| Credentials | LCSW |
| License number and state | SENTINEL_PROVIDER_LICENSE_3, EX |
| NPI and type | SENTINEL_NPI_3_0000000000, type 1 |
| Company Tax ID | SENTINEL_TAX_ID_3_000000000 |
| First service | 2026-10-01, 90837, 1 unit, F99, pointer 1, 150.00 paid, place 10, modifier 95 |
| Second service | 2026-10-08, 90837, 1 unit, F99, pointer 1, 150.00 paid, place 10, modifier 95 |
| Total | 300.00 charged and 300.00 paid |

Fix list: none for the core superbill fields. Ask the person for every employee,
relationship, other-coverage, accident, employment, and optional-provider answer
that the fixture does not state. Do not infer any answer.

## Route card

| Field | Atlas value |
| --- | --- |
| Insurer | Aetna |
| Member form | Medical Benefits Request GC-7, revision 6-25 S |
| Form URL | https://www.aetna.com/content/dam/aetna/pdfs/aetnacom/individuals-families-health-insurance/document-library/medical-claim-form.pdf |
| Portal upload | YES |
| Portal | Aetna member website |
| Portal path | Claims > Submit a Claim for plans exposing the online route; alternate published employer path: Support > Contact Us > Send Message > attach claim form |
| Mail address | NOT PUBLISHED |
| Fax | NOT PUBLISHED |
| File types | NOT PUBLISHED; signed-in form is UNREADABLE |
| Confirmation | NOT PUBLISHED |
| Deadline | NOT PUBLISHED |
| Deadline basis | YES: employer and plan documents control |
| Status | Aetna member website can check and manage claims |
| Processing time | NOT PUBLISHED |
| Payment | NOT PUBLISHED; INFERRED: leave optional block 28 unsigned to avoid direct provider payment |
| Caveat | Online filing is plan dependent; generic public form page publishes a paper route; HMO or EPO routine out-of-network coverage, self-funded terms, Medicare Advantage, and Medicaid require separate plan instructions |
| Read date | 2026-10-09 |

## Field sheet in form order

| Section | Field label | Prepared value | Source or action |
| --- | --- | --- | --- |
| fraud statement | patient signature | leave blank | person signs by hand |
| fraud statement | date | leave blank | person dates by hand |
| employee | employer's name | ask the person | absent from fixture |
| employee | policy or group number | SENTINEL_GROUP_NUMBER_3 | fixture card details |
| employee | employee Aetna id number | SENTINEL_MEMBER_ID_3, confirm employee use | do not assume client is employee |
| employee | employee name | ask the person | do not assume client is employee |
| employee | birth field as printed | ask the person | card or person |
| employee | active or retired | ask the person | person answer |
| employee | date of retirement | ask if retired | person answer |
| employee | employee address | ask the person | do not assume client is employee |
| employee | address is new | ask the person | person answer |
| employee | daytime telephone number | ask the person | do not assume client is employee |
| patient | patient name | SENTINEL_CLIENT_NAME_3 | fixture card details |
| patient | patient Aetna id number | SENTINEL_MEMBER_ID_3 | fixture card details |
| patient | birth field as printed | SENTINEL_BIRTH_DATE_3 | fixture card details |
| patient | relationship to employee | ask the person | absent from fixture |
| patient | address if different from employee | SENTINEL_CLIENT_ADDRESS_3 if different | confirm with person |
| patient | gender or leave blank | ask the person or leave blank | form permits no disclosure |
| patient | marital status | ask the person | absent from fixture |
| patient | is patient employed? | ask the person | absent from fixture |
| patient | employer name and address | ask if employed | person answer |
| accident | is claim related to an accident? | ask the person | absent from fixture |
| accident | date | ask if yes | person answer |
| accident | time | ask if yes | person answer |
| accident | is claim related to employment? | ask the person | absent from fixture |
| outside United States | country of service | not applicable unless person says otherwise | ask the person |
| outside United States | reason for outside service | not applicable unless person says otherwise | ask the person |
| other coverage | any family expenses covered by another plan? | ask the person | absent from fixture |
| other coverage | policyholder, policy number, and carrier | ask if yes | card or person |
| other coverage | member id number | ask if yes | card or person |
| other coverage | member name | ask if yes | card or person |
| other coverage | birth field as printed | ask if yes | card or person |
| authorization | patient or authorized person signature | leave blank | person signs by hand |
| authorization | date | leave blank | person dates by hand |
| assignment of benefits | authorize payment to provider | leave blank | assignment stays unsigned |
| assignment of benefits | signature | leave blank | assignment stays unsigned |
| assignment of benefits | date | leave blank | assignment stays unsigned |
| provider | date of illness or injury | leave blank if provider section is not used | ask only if section is used |
| provider | date first consulted | leave blank if provider section is not used | ask only if section is used |
| provider | similar illness or injury dates | leave blank if provider section is not used | ask only if section is used |
| provider | emergency | leave blank if provider section is not used | ask only if section is used |
| provider | date able to return to work | leave blank if provider section is not used | ask only if section is used |
| provider | total disability dates | leave blank if provider section is not used | ask only if section is used |
| provider | partial disability dates | leave blank if provider section is not used | ask only if section is used |
| provider | referring physician | leave blank if provider section is not used | ask only if section is used |
| provider | hospitalization dates | leave blank if provider section is not used | ask only if section is used |
| provider | facility name and address | Example Counseling address if section is used | superbill |
| diagnosis | diagnosis or nature of illness | F99 if section is used | superbill |
| service line | date of service | 2026-10-01; 2026-10-08 if section is used | superbill |
| service line | place of service | 10 for each line if section is used | superbill |
| service line | procedure code | 90837 for each line if section is used | superbill |
| service line | description of service | outpatient psychotherapy for each line if section is used | superbill |
| service line | charges | 150.00 for each line if section is used | superbill |
| service line | days or units | 1 for each line if section is used | superbill |
| service line | diagnosis code | F99 for each line if section is used | superbill |
| provider | physician name and address | SENTINEL_PROVIDER_NAME_3 and Example Counseling address if section is used | superbill |
| provider | telephone number | SENTINEL_PROVIDER_PHONE_3 if section is used | superbill |
| provider | taxpayer identifying number | SENTINEL_TAX_ID_3_000000000 if section is used | superbill |
| provider | patient account number | ask if section is used | person or therapist answer |
| charges | total charge | 300.00 if section is used | superbill |
| charges | amount paid | 300.00 if section is used | superbill |
| charges | balance due | 0.00 if section is used | superbill says paid in full |
| provider | physician or supplier signature | leave blank | provider signs only if required |
| provider | national provider identifier | SENTINEL_NPI_3_0000000000 if section is used | superbill |
| provider | date | leave blank | provider dates only if required |

The expected route uses the itemized superbill attachment, so the provider
section can remain unused. The person must confirm this on the current form.

## Cover letter

```text
member claim cover letter
insurer: Aetna
subscriber or dependent: ask the person
claim type: out-of-network outpatient psychotherapy
dates of service: 2026-10-01 and 2026-10-08
total charge: 300.00
payment requested: to the member, while retaining the atlas payment caveat
enclosures: Medical Benefits Request GC-7, superbill, and proof of payment
signature: leave blank for the person
date: leave blank for the person
```

## Attachments and tracker

- Prepared: form field sheet and itemized superbill.
- Still needed: person answers, person signature, and a receipt, card statement
  line, or paid invoice.
- Other coverage EOB: ask the person and include only when applicable.

```text
Aetna | 2026-10-01; 2026-10-08 | 300.00 | <blank until submitted> |
plan-specific member website route | <blank until received> |
NOT PUBLISHED | NOT PUBLISHED
```

## Person-only submission

The person first confirms that the plan exposes online claim submission. The
person then follows Claims > Submit a Claim, or the published secure-message
alternative when that plan provides it, and attaches the current form,
superbill, proof of payment, and any applicable other-coverage EOB. The person
retains the result and checks claims in the member website. Nothing is filed by
the routine.
