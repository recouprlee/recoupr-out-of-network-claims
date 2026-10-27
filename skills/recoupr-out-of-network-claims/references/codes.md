# codes

These are structure and source checks. They do not decide what code, diagnosis,
fee, date, provider detail, place of service, or modifier belongs on a
superbill. The therapist's source record controls. The insurer's own coding and
telehealth policy controls whether a claim accepts or pays a code.

## 1. Psychotherapy CPT codes

This table contains every code in `MH_CPT_CODES` in
`superbill-validation-constants.ts`. `Add-on` reflects the CMS October 2026
add-on code file for current codes. The two retained legacy codes are not in the
2026 CMS file, so unsupported details for them stay `NOT PUBLISHED`.

| CPT code | Short description | Time range when published | Add-on | Non-individual flag from input | Source |
| --- | --- | --- | --- | --- | --- |
| 90785 | Interactive complexity | NOT PUBLISHED | Yes | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90791 | Psychiatric diagnostic evaluation | NOT PUBLISHED | No | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90792 | Psychiatric diagnostic evaluation with medical services | NOT PUBLISHED | No | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90832 | Psychotherapy with patient, 30 minutes | 16 to 37 minutes | No | No | https://www.cms.gov/medicare-coverage-database/view/article.aspx?articleid=56937&ver=43; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90833 | Psychotherapy with patient and E/M service, 30 minutes | 16 to 37 minutes | Yes | No | https://www.cms.gov/medicare-coverage-database/view/article.aspx?articleid=56937&ver=43; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90834 | Psychotherapy with patient, 45 minutes | 38 to 52 minutes | No | No | https://www.cms.gov/medicare-coverage-database/view/article.aspx?articleid=56937&ver=43; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90836 | Psychotherapy with patient and E/M service, 45 minutes | 38 to 52 minutes | Yes | No | https://www.cms.gov/medicare-coverage-database/view/article.aspx?articleid=56937&ver=43; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90837 | Psychotherapy with patient, 60 minutes | 53 minutes or more | No | No | https://www.cms.gov/medicare-coverage-database/view/article.aspx?articleid=56937&ver=43; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90838 | Psychotherapy with patient and E/M service, 60 minutes | 53 minutes or more | Yes | No | https://www.cms.gov/medicare-coverage-database/view/article.aspx?articleid=56937&ver=43; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90839 | Crisis psychotherapy, initial service | First 60 minutes | No | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90840 | Crisis psychotherapy, additional service | Each additional 30 minutes | Yes | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90845 | Psychoanalysis | Not time defined; usually 45 to 50 minutes | No | No | https://www.cms.gov/medicare-coverage-database/view/article.aspx?articleid=56937&ver=43; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90846 | Family psychotherapy without the patient present | 26 minutes or more; descriptor says 50 minutes | No | Yes | https://www.cms.gov/medicare-coverage-database/view/article.aspx?articleid=56937&ver=43; https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip; `superbill-validation-constants.ts` (read 2026-10-27) |
| 90847 | Family psychotherapy with the patient present | 26 minutes or more; descriptor says 50 minutes | No | Yes | https://www.cms.gov/medicare-coverage-database/view/article.aspx?articleid=56937&ver=43; https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip; `superbill-validation-constants.ts` (read 2026-10-27) |
| 90849 | Multiple-family group psychotherapy | NOT PUBLISHED | No | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip; `superbill-validation-constants.ts` (read 2026-10-27) |
| 90853 | Group psychotherapy | NOT PUBLISHED | No | Yes | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip; `superbill-validation-constants.ts` (read 2026-10-27) |
| 90863 | Pharmacologic management with psychotherapy | NOT PUBLISHED | Yes | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90875 | Psychophysiological therapy | NOT PUBLISHED | No | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90876 | Psychophysiological therapy | NOT PUBLISHED | No | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90880 | Hypnotherapy | NOT PUBLISHED | No | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90885 | Psychiatric evaluation of records | NOT PUBLISHED | No | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 90887 | Interpretation and explanation of psychiatric examination results | NOT PUBLISHED | No | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 99202 | New patient office or outpatient E/M visit | 15 to 29 minutes when time selects the code | No | No | https://www.ama-assn.org/health-care-advocacy/administrative-burdens/are-physicians-required-document-time-spent-each; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 99203 | New patient office or outpatient E/M visit | 30 to 44 minutes when time selects the code | No | No | https://www.ama-assn.org/health-care-advocacy/administrative-burdens/are-physicians-required-document-time-spent-each; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 99204 | New patient office or outpatient E/M visit | 45 to 59 minutes when time selects the code | No | No | https://www.ama-assn.org/health-care-advocacy/administrative-burdens/are-physicians-required-document-time-spent-each; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 99205 | New patient office or outpatient E/M visit | 60 to 74 minutes when time selects the code | No | No | https://www.ama-assn.org/health-care-advocacy/administrative-burdens/are-physicians-required-document-time-spent-each; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 99211 | Established patient office or outpatient E/M visit | NOT PUBLISHED | No | No | https://www.ama-assn.org/health-care-advocacy/administrative-burdens/are-physicians-required-document-time-spent-each; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 99212 | Established patient office or outpatient E/M visit | 10 to 19 minutes when time selects the code | No | No | https://www.ama-assn.org/health-care-advocacy/administrative-burdens/are-physicians-required-document-time-spent-each; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 99213 | Established patient office or outpatient E/M visit | 20 to 29 minutes when time selects the code | No | No | https://www.ama-assn.org/health-care-advocacy/administrative-burdens/are-physicians-required-document-time-spent-each; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 99214 | Established patient office or outpatient E/M visit | 30 to 39 minutes when time selects the code | No | No | https://www.ama-assn.org/health-care-advocacy/administrative-burdens/are-physicians-required-document-time-spent-each; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 99215 | Established patient office or outpatient E/M visit | 40 to 54 minutes when time selects the code | No | No | https://www.ama-assn.org/health-care-advocacy/administrative-burdens/are-physicians-required-document-time-spent-each; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 99354 | Legacy prolonged service code; exact description NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED | No | `superbill-validation-constants.ts`; not listed in https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip (read 2026-10-27) |
| 99355 | Legacy prolonged service code; exact description NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED | No | `superbill-validation-constants.ts`; not listed in https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip (read 2026-10-27) |
| 99366 | Team conference with the patient by a health professional | NOT PUBLISHED | No | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 99367 | Team conference without the patient by a physician | NOT PUBLISHED | No | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 99368 | Team conference without the patient by a health professional | NOT PUBLISHED | No | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |
| 99417 | Prolonged office or outpatient E/M service | Each additional 15 minutes | Yes | No | https://www.cms.gov/files/zip/rvu26a-updated-12-29-2025.zip; https://www.cms.gov/files/zip/add-code-edits-medicare-effective-10012026.zip (read 2026-10-27) |

The input explicitly flags 90846, 90847, and 90853 as non-individual codes.
CMS describes 90849 as multiple-family group psychotherapy, but the input does
not include it in that flag set. The skill does not invent a new classification.
For a person's claim for their own sessions, a family or group description is a
warning to confirm that the superbill identifies that person and the actual
service. It is never permission to change the code.

## 2. Place of service codes

Only 02 and 10 mean telehealth in this input set.

| Code | Plain-words meaning | Telehealth | Source |
| --- | --- | --- | --- |
| 02 | Telehealth when the patient is not at home | Yes | https://www.cms.gov/medicare/coding-billing/place-of-service-codes/code-sets (read 2026-10-27) |
| 03 | School | No | https://www.cms.gov/medicare/coding-billing/place-of-service-codes/code-sets (read 2026-10-27) |
| 10 | Telehealth when the patient is at home | Yes | https://www.cms.gov/medicare/coding-billing/place-of-service-codes/code-sets (read 2026-10-27) |
| 11 | Office | No | https://www.cms.gov/medicare/coding-billing/place-of-service-codes/code-sets (read 2026-10-27) |
| 12 | Home or private residence | No | https://www.cms.gov/medicare/coding-billing/place-of-service-codes/code-sets (read 2026-10-27) |
| 49 | Independent outpatient clinic | No | https://www.cms.gov/medicare/coding-billing/place-of-service-codes/code-sets (read 2026-10-27) |
| 50 | Federally Qualified Health Center | No | https://www.cms.gov/medicare/coding-billing/place-of-service-codes/code-sets (read 2026-10-27) |
| 53 | Community Mental Health Center | No | https://www.cms.gov/medicare/coding-billing/place-of-service-codes/code-sets (read 2026-10-27) |
| 71 | State or local public health clinic | No | https://www.cms.gov/medicare/coding-billing/place-of-service-codes/code-sets (read 2026-10-27) |
| 72 | Rural Health Clinic | No | https://www.cms.gov/medicare/coding-billing/place-of-service-codes/code-sets (read 2026-10-27) |

## 3. Telehealth modifiers

The superbill carries a modifier only when the therapist's record and the
applicable coding rule call for it. This skill never adds, removes, or replaces
a modifier. The insurer's own policy controls, and the payer atlas caveats must
be checked before a claim is prepared.

| Modifier | Plain-words meaning | Superbill rule | Source |
| --- | --- | --- | --- |
| 95 | Real-time audio and video telemedicine | If the therapist's source record uses 95, it must be on a telehealth service line with place of service 02 or 10 in this skill's deterministic check. | https://www.cms.gov/training-education/medicare-learning-network/newsletter/mln-connects-newsletter-september-10-2026 (read 2026-10-27) |
| 93 | Real-time audio-only telemedicine | Carry 93 only when the therapist's source record and the insurer's own policy call for audio-only reporting. | https://www.ama-assn.org/practice-management/cpt/cpt-appendix-t-and-modifier-93-audio-only-medical-services (read 2026-10-27) |

## 4. ICD-10 code shape

| Form | Shape in words | F-only examples | Source |
| --- | --- | --- | --- |
| Dotted | One uppercase letter, two digits, then optionally a dot followed by one to four uppercase letters or digits | F41, F41.1, F43.23 | `superbill-validation-constants.ts` |
| EDI without a dot | One uppercase letter, two digits, then one to four uppercase letters or digits | F411, F4323 | `superbill-validation-constants.ts` |
| Fabricated-code guard | Reject U00 and U000 through U009 even though some pass the general shape check | NOT PUBLISHED | `superbill-validation-constants.ts` |

The diagnosis is the therapist's. This skill never proposes, changes, or
questions a diagnosis. A failed shape or fabricated-code check asks the
therapist to compare the superbill with the original clinical record.

## 5. NPI

| Fact | Plain-words rule | Source |
| --- | --- | --- |
| Shape | An NPI is exactly ten digits. | https://www.cms.gov/regulations-and-guidance/administrative-simplification/nationalprovidentstand (read 2026-10-27) |
| Check digit | Apply the Luhn modulus ten method to the first nine digits as if the 80840 prefix were present. Starting with the rightmost of those nine digits, double alternating digits, add the digits of those products and the untouched digits, add the CMS constant 24, and choose the final digit that brings the sum to the next multiple of ten. | https://www.cms.gov/Regulations-and-Guidance/Administrative-Simplification/NationalProvIdentStand/Downloads/NPIcheckdigit.pdf (read 2026-10-27) |
| Type 1 | An individual health care provider, including a sole proprietor. | https://www.cms.gov/files/document/npi-fact-sheet.pdf (read 2026-10-27) |
| Type 2 | A health care organization, such as a group practice or company. | https://www.cms.gov/files/document/npi-fact-sheet.pdf (read 2026-10-27) |

The template uses the NPI type that belongs to the billing arrangement in the
practice's records. It does not choose a type from the practice name.

## 6. Tax ID shapes

| Type | Shape in words | Superbill rule | Source |
| --- | --- | --- | --- |
| Employer number | Nine digits, commonly grouped as a two-digit prefix followed by seven digits | Use the practice's billing Tax ID from its records. | https://www.cms.gov/outreach-and-education/mln/wbt/mln4462429-mln-wbt-1500/1500/lesson04/12/index.html (read 2026-10-27) |
| Social security number | Nine digits | Use only when the practice's billing record says this is its Tax ID. No numeric example is shown here. | https://www.cms.gov/medicare/quality-initiatives-patient-assessment-instruments/pqrs/downloads/2015_pqrs_registry_reporting_made_simple.pdf (read 2026-10-27) |
| Billing entity | The person or organization that owns the Tax ID is the billing entity. | The superbill carries the practice's Tax ID and never a client's number of any kind. | https://www.cms.gov/outreach-and-education/mln/wbt/mln4462429-mln-wbt-1500/1500/lesson04/12/index.html (read 2026-10-27) |

## 7. Provider taxonomy codes

| Taxonomy code | Name | Source |
| --- | --- | --- |
| 101Y00000X | Counselor | `providerTaxonomies.ts` |
| 101YA0400X | Addiction Counselor | `providerTaxonomies.ts` |
| 101YM0800X | Mental Health Counselor | `providerTaxonomies.ts` |
| 101YP2500X | Professional Counselor | `providerTaxonomies.ts` |
| 103T00000X | Psychologist | `providerTaxonomies.ts` |
| 103TC0700X | Clinical Psychologist | `providerTaxonomies.ts` |
| 104100000X | Social Worker | `providerTaxonomies.ts` |
| 1041C0700X | Clinical Social Worker | `providerTaxonomies.ts` |
| 106H00000X | Marriage and Family Therapist | `providerTaxonomies.ts` |
