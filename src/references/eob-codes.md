# EOB codes for psychotherapy claims

Use the code list named on the EOB or denial notice. A code is a routing clue,
not a decision by itself. Read every accompanying remark and the appeal-rights
paragraph before choosing correction or appeal. The bucket preserves the
earlier product map where one existed. It does not establish coverage, coding,
medical necessity, or an appeal outcome.

Official CARC source: [X12 Claim Adjustment Reason Codes](https://x12.org/codes/claim-adjustment-reason-codes), HTTP 200, read 2026-10-27.

Official RARC source: [X12 Remittance Advice Remark Codes](https://x12.org/codes/remittance-advice-remark-codes), HTTP 200, read 2026-10-27.

The official-description column gives a sourced paraphrase of the X12 text.
Use the linked X12 page when the exact official wording is required.

The synthetic answer keys labeled A1, A2, and A3 as remark codes. X12 publishes
those values in the CARC list, not the RARC list. The table therefore labels
them CARC. If a record names a different code list, do not apply these meanings.

## Code table

| code | official description | earlier product wording | plain-words meaning | bucket | next step |
| --- | --- | --- | --- | --- | --- |
| CARC 4 | X12 says the procedure code conflicts with its modifier and points to the policy-identification segment when present. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Procedure code inconsistent with modifier | The payer says the procedure and modifier do not fit together. Do not change either value yourself. | edi_rejection | ask the therapist |
| CARC 15 | X12 says the authorization identifier is missing, invalid, or inapplicable to the billed service or provider. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Authorization number missing/invalid | The payer could not apply the authorization number to this service or provider. | edi_rejection | correction |
| CARC 16 | X12 says claim information is missing or the submission has a billing error, excludes attachment requests from this code, and requires an accompanying non-alert remark or reject reason. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Claim/service lacks information | The claim has missing or invalid submission information. Read the required accompanying remark code. | edi_rejection | correction |
| CARC 17 | X12 says requested information was absent or inadequate and requires an accompanying remark or reject reason. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Requested payment adjusted - benefit not covered by plan | The payer says requested information was absent or incomplete. Read the accompanying remark for the exact item. | plan_exclusion | correction |
| CARC 18 | X12 identifies an exact duplicate claim or service and limits the group-code use, subject to the stated workers' compensation exception. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Exact duplicate claim/service | The payer says it already has the same claim or service. Compare claim numbers and service lines before responding. | duplicate_claim | correction |
| CARC 22 | X12 says another payer may cover the care under coordination of benefits. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Care may be covered by another payer per coordination of benefits | The payer thinks another plan may have to process the claim first. | duplicate_claim | correction |
| CARC 23 | X12 says the amount reflects prior-payer adjudication, payment, or adjustment and limits use to group code OA. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Payment adjusted, charges covered under capitation | The amount reflects what another payer already paid or adjusted. | coordination_of_benefits | correction |
| CARC 24 | X12 says the charges fall under a capitation arrangement or managed-care plan. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Charges covered by savings from another payer | The payer says the charge belongs under a managed-care payment arrangement. | coordination_of_benefits | correction |
| CARC 26 | X12 says the expense occurred before coverage began. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | Expenses incurred prior to coverage | The payer says the service happened before coverage began. Compare the notice with plan records. | plan_exclusion | appeal |
| CARC 27 | X12 says the expense occurred after coverage ended. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | Expenses incurred after coverage terminated | The payer says coverage ended before the service. Compare the notice with eligibility records. | eligibility_mismatch | correction |
| CARC 29 | X12 says the filing time limit has passed. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Time limit for filing has expired | The payer says the claim arrived after its filing limit. Preserve submission proof and the printed deadline. | timely_filing | appeal |
| CARC 31 | X12 says the payer cannot identify the person as its insured. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | Patient cannot be identified as our insured | The payer could not match the person to coverage. Compare the submitted identifiers with the card. | eligibility_mismatch | correction |
| CARC 32 | X12 says the payer's records do not show an eligible dependent. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | Our records indicate the patient is not an eligible dependent | The payer says the dependent was not eligible. Compare the notice with plan records. | eligibility_mismatch | correction |
| CARC 33 | X12 says the insured lacks dependent coverage. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | Insured has no dependent coverage | The payer says the plan lacks dependent coverage. Compare the notice with plan records. | eligibility_mismatch | correction |
| CARC 50 | X12 says the payer considers the service noncovered on medical-necessity grounds and points to the policy-identification segment when present. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Non-covered service | The payer made a medical-necessity coverage decision. Use only the therapist's existing documentation. | parity_violation | appeal |
| CARC 58 | X12 says the payer considers the place of service inappropriate or invalid and points to the policy-identification segment when present. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Treatment not covered by this payer/plan | The payer disputes the place of service. Do not change it without the therapist's records. | eligibility_mismatch | ask the therapist |
| CARC 96 | X12 identifies a noncovered charge, requires an accompanying non-alert remark or reject reason, and points to the policy-identification segment when present. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Non-covered charge | The payer says the charge is not covered. Read the accompanying remark and plan reason. | parity_violation | appeal |
| CARC 97 | X12 says the allowance for this service is included in another service that was already adjudicated and points to the policy-identification segment when present. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Payment adjusted - benefit limitation | The payer says this service was already included in another service's payment. | parity_violation | appeal |
| CARC 119 | X12 says the applicable benefit maximum for the period or occurrence has been reached. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Benefit max reached | The payer says the plan's stated benefit maximum has been used. | parity_violation | appeal |
| CARC 136 | X12 says prior-payer coverage rules were not followed and limits use to group code OA. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Claim not covered by this plan/contract | The payer says another payer's coverage rules were not followed. | plan_exclusion | appeal |
| CARC 151 | X12 says the submitted information does not support the number or frequency of services. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Prior authorization required, not obtained | The payer says the submitted record does not support the number or frequency of services. | prior_auth_required | ask the therapist |
| CARC 181 | X12 says the procedure code was invalid for the service date. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | Procedure code was invalid on date of service | The payer says the procedure code was not valid for that service date. Do not replace it yourself. | edi_rejection | ask the therapist |
| CARC 182 | X12 says the procedure modifier was invalid for the service date. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | Procedure modifier was invalid on date of service | The payer says the modifier was not valid for that service date. Do not replace it yourself. | edi_rejection | ask the therapist |
| CARC 197 | X12 says required precertification, authorization, notification, or pretreatment was absent. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Precertification/authorization absent | The payer says required approval or notice was absent. Compare the denial with plan and authorization records. | prior_auth_required | appeal |
| CARC 198 | X12 says the precertification, authorization, notification, or pretreatment limit was exceeded. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Precertification, not effective date of service | The payer says the approved service limit was exceeded. | eligibility_mismatch | appeal |
| CARC 204 | X12 says the current benefit plan does not cover the service, equipment, or drug. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | NOT IN EARLIER MAP | The payer says the current plan does not cover the service. Check the cited plan term. | plan_exclusion | appeal |
| CARC 252 | X12 says an attachment or other documentation is required for adjudication and requires an accompanying non-alert remark or reject reason. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | WORDING DIFFERS: Service not adjudicated, system error | The payer needs an attachment or other named document before it can decide the claim. | edi_rejection | correction |
| CARC A1 | X12 uses this as a general denial only when no more specific CARC is available and requires an accompanying non-alert remark or reject reason. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | NOT IN EARLIER MAP | This only says denied. Another code or the notice must supply the reason. | informational | nothing |
| CARC A2 | X12 lists this deactivated code as a contractual adjustment. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | NOT IN EARLIER MAP | This is a deactivated CARC for a contractual adjustment. Read the document's current accompanying codes. | informational | nothing |
| CARC A3 | X12 lists this deactivated code for satisfied Medicare Secondary Payer liability. [X12 CARC](https://x12.org/codes/claim-adjustment-reason-codes), read 2026-10-27 | NOT IN EARLIER MAP | This is a deactivated CARC about Medicare secondary-payer liability. Read the program notice. | informational | nothing |
| RARC N54 | X12 says claim information conflicts with the precertified or authorized services. [X12 RARC](https://x12.org/codes/remittance-advice-remark-codes), read 2026-10-27 | NOT IN EARLIER MAP | The claim information does not match the authorized service record. | prior_auth_required | ask the therapist |
| RARC N130 | X12 directs the reader to plan benefit documents or guidelines for service restrictions. [X12 RARC](https://x12.org/codes/remittance-advice-remark-codes), read 2026-10-27 | NOT IN EARLIER MAP | The payer points to a plan restriction but this code does not identify it. | plan_exclusion | appeal |
| RARC N290 | X12 says the rendering provider's primary identifier is missing, incomplete, or invalid. [X12 RARC](https://x12.org/codes/remittance-advice-remark-codes), read 2026-10-27 | NOT IN EARLIER MAP | The payer needs a corrected rendering-provider identifier from the existing provider record. | edi_rejection | correction |
| RARC N386 | X12 says the decision relies on a National Coverage Determination and directs the reader to the Medicare Coverage Database. [X12 RARC](https://x12.org/codes/remittance-advice-remark-codes), read 2026-10-27 | NOT IN EARLIER MAP | The decision cites a Medicare national coverage determination. Use the government-program notice route. | plan_exclusion | appeal |

## Suspected wording checks

- CARC 17: DID NOT MATCH.
- CARC 23: DID NOT MATCH.
- CARC 24: DID NOT MATCH.
- CARC 58: DID NOT MATCH.
- CARC 97: DID NOT MATCH.
- CARC 136: DID NOT MATCH.
- CARC 151: DID NOT MATCH.
- CARC 252: DID NOT MATCH.

For all eight, the earlier product wording named a different reason than the
official X12 text or omitted the reason that controls the code. The official
X12 wording above controls this reference. A person should still use the full
EOB and denial letter because one code never supplies the whole decision.
