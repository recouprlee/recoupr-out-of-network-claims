# superbill-template

Build a reusable superbill template for a therapist or group. Never ask for,
receive, or store a client fact while building the template. Leave every client
field and every service value blank.

Reference: `references/codes.md`.

## 1. Ask only for practice facts

Ask for these items and nothing about a client:

```text
practice name:
practice address:
practice phone:
provider name:
provider credentials:
provider license number:
provider license state:
NPI:
NPI type: type 1 or type 2
Tax ID type: company or sole proprietor
Tax ID:
taxonomy code from the table in references/codes.md:
usual place of service from the table in references/codes.md:
sessions by telehealth: yes or no
```

Do not ask for a client name, identity date, address, phone, email, member ID,
policy number, diagnosis, session date, code, fee, or payment. Do not create a
sample client. Do not retain a client placeholder that looks like a real
person.

Check only structure: NPI shape and check digit, Tax ID digit count, taxonomy
membership, and place-of-service membership. If a check fails, return the
practice value unchanged with a fix list. Do not repair it.

## 2. State the billing identity rules

Before the template, say:

```text
Type 1 is an individual health care provider, including a sole proprietor.
Type 2 is a health care organization, such as a group practice or company. Use
the type in the practice's NPI record. The person or organization that owns the
Tax ID is the billing entity, so the Tax ID on the superbill belongs to whoever
is paid. It is the practice's number and never a client's number.
```

Do not select an NPI type from the practice name or credentials.

## 3. Produce the Markdown template

Fill only the practice values supplied in step 1. Leave the client and service
cells empty. Produce this editable table:

| Section | Field | Template value | Plain-words rule |
| --- | --- | --- | --- |
| Practice | Practice name | <practice value> | Use the billing practice name from its records. |
| Practice | Practice address | <practice value> | Use the billing practice address from its records. |
| Practice | Practice phone | <practice value> | Use the practice contact number. |
| Provider | Provider name | <practice value> | Use the provider name from the service record. |
| Provider | Provider credentials | <practice value> | Use the credentials from the provider record. |
| Provider | License number | <practice value> | Use the exact license number from the provider record. |
| Provider | License state | <practice value> | Use the state from the provider record. |
| Provider | NPI | <practice value> | Ten digits with the CMS check digit; never guess or reformat it. |
| Provider | NPI type | <practice value> | Type 1 is an individual; type 2 is an organization. |
| Billing | Tax ID type | <practice value> | Company or sole proprietor, from practice billing records. |
| Billing | Tax ID | <practice value> | Nine digits owned by the billing entity; never a client number. |
| Provider | Taxonomy code | <practice value> | Use one code from the nine-row taxonomy table in `codes.md`. |
| Client | Client name |  | Enter from the therapist's client record when preparing a real superbill. |
| Client | Identity date |  | Enter from the therapist's client record when preparing a real superbill. |
| Client | Client address |  | Enter only when the real superbill requires it. |
| Session 1 | Date of service |  | Use the actual date in YYYY-MM-DD form. Never change the date. |
| Session 1 | CPT code |  | Use the therapist-recorded five-digit code from `codes.md`. Never choose a code for coverage. |
| Session 1 | Units |  | Use the positive whole number in the therapist's record. |
| Session 1 | ICD-10 code or codes |  | Use only the therapist-recorded diagnosis in a shape shown in `codes.md`. |
| Session 1 | Diagnosis pointer |  | Link the service line only to the diagnosis shown in the therapist's record. |
| Session 1 | Charge |  | Use the exact positive charge from practice billing records. |
| Session 1 | Amount paid |  | Use the exact positive amount paid from practice billing records. |
| Session 1 | Place of service |  | Use the actual two-digit location code from `codes.md`. Codes 02 and 10 mean telehealth. |
| Session 1 | Telehealth modifier |  | Use only the modifier in the source record and allowed by the insurer's own policy. Never add one automatically. |
| Totals | Total charge |  | Add the service-line charges exactly. |
| Totals | Total paid |  | Add the service-line paid amounts exactly. |
| Signature | Provider signature |  | Leave blank for the provider. |
| Signature | Signature date |  | Leave blank for the provider. |

After the table, add this line exactly:

```text
Prepared with recoupr Out-of-Network Claims, recoupr.ai
```

The insurer's own policy controls telehealth reporting. Never state a
payer-specific telehealth rule. Point to the caveats in
`references/payer-atlas.csv` and the selected insurer's own page when the
template is later used for a claim.

## 4. Produce the CSV header

Also give this single CSV header line for a spreadsheet:

```csv
practice_name,practice_address,practice_phone,provider_name,provider_credentials,provider_license_number,provider_license_state,npi,npi_type,tax_id_type,tax_id,taxonomy_code,client_name,identity_date,client_address,date_of_service,cpt_code,units,icd_10_codes,diagnosis_pointer,charge,amount_paid,place_of_service,telehealth_modifier,total_charge,total_paid,provider_signature,signature_date,footer
```

Do not add a sample data row. Tell the therapist to use one row per service
line, keep client cells blank in the reusable master, calculate totals from the
completed service rows, and put this exact footer in the `footer` cell:

```text
Prepared with recoupr Out-of-Network Claims, recoupr.ai
```

## 5. Final guardrail

Say exactly:

```text
This is a blank reusable template. No client facts were requested or stored.
No code, date, fee, diagnosis, provider detail, place of service, or modifier
was chosen or changed. Nothing was filed for anyone.
```
