# Appeals reference

This reference prepares a person's own appeal packet. It does not decide
coverage, give legal advice, change a code or diagnosis, or send anything.
Every route must be checked against the current denial notice and plan.

## 1. Correction against appeal

"Denials and short payments on out-of-network claims are common and often
procedural." Source: `23-eob-denied-or-underpaid.md`, reviewed 2026-10-27.

Use correction when the notice identifies a fact or document that can be
matched to an existing record: a missing attachment, an omitted field, a
provider identifier, other-payer information, or a duplicate. Correct only
what the EOB, denial letter, superbill, claim copy, card, or plan record proves.
Do not replace a diagnosis, procedure code, modifier, place of service, date,
or provider fact. Source: `appeal-decision.service.ts`, correction buckets and
admin-review rules, reviewed 2026-10-27.

Use appeal when the notice makes a benefit decision: medical necessity,
coverage or exclusion, a benefit maximum, an authorization decision, a timely
filing decision, or another plan interpretation. The letter may challenge only
what the supplied records support. A code is a clue, not the decision. Source:
`appeal-classifier.service.ts`, `appeal-decision.service.ts`, and
`appeal-letter-input.ts`, reviewed 2026-10-27.

If the notice is unclear, label the decision `UNRESOLVED`, ask for the complete
denial and appeal-rights paragraph, and preserve both paths. A correction does
not prove that an appeal clock stopped. Source: `appeals-by-channel.md`, section
"When to appeal, correct, or stop," research date 2026-10-07.

## 2. The clocks by plan type

The denial letter's stated deadline controls the packet unless the person has
reliable plan or legal information showing otherwise. Record the notice date,
the date received if known, and the printed deadline separately. The script is
a planning aid, not a finding that a plan or claim is governed by a rule.

### Employer plans governed by ERISA

An appeal request period must be "at least 180 days" after receipt of the
adverse-benefit notice. Source: [29 CFR 2560.503-1](https://www.law.cornell.edu/cfr/text/29/2560.503-1), paragraph (h)(3)(i), read 2026-10-27.

An initial post-service claim decision is due within 30 days after receipt of
the claim. The operative phrase is "not later than 30 days." Source:
[29 CFR 2560.503-1](https://www.law.cornell.edu/cfr/text/29/2560.503-1), paragraph (f)(2)(iii)(B), read 2026-10-27.

For a post-service appeal, a plan with one appeal has 60 days after receiving
the request. The operative phrase is "not later than 60 days." A plan with
"two appeals" has 30 days for each. Source: [29 CFR 2560.503-1](https://www.law.cornell.edu/cfr/text/29/2560.503-1), paragraph (i)(2)(iii)(A), read 2026-10-27.

The claimant may obtain the relevant claim documents "upon request and free of
charge." Source: [29 CFR 2560.503-1](https://www.law.cornell.edu/cfr/text/29/2560.503-1), paragraph (h)(2)(iii), read 2026-10-27.

### Individual and group plans under the Affordable Care Act

Covered group and individual internal processes incorporate the ERISA rules,
subject to the stated modifications. The individual provision says it is
"subject to the requirements." Source: [45 CFR 147.136](https://www.law.cornell.edu/cfr/text/45/147.136), paragraphs (b)(2)(i) and (b)(3)(i), read 2026-10-27.

The federal external-review request window is "within four months" after
receipt of an adverse or final internal adverse notice. Source:
[45 CFR 147.136](https://www.law.cornell.edu/cfr/text/45/147.136), paragraph (d)(2)(ii), read 2026-10-27. A qualifying state process must
also allow at least four months under paragraph (c)(2)(vi).

The assigned IRO must issue its written final decision "within 45 days" after
receiving the request. Source: [45 CFR 147.136](https://www.law.cornell.edu/cfr/text/45/147.136), paragraph (d)(2)(iii)(B)(6), read 2026-10-27.

Subject to the remedies and payment exceptions in the paragraph, the decision
is "binding on the plan or issuer" and the claimant. Source:
[45 CFR 147.136](https://www.law.cornell.edu/cfr/text/45/147.136), paragraph (d)(2)(iii)(B)(7)(v), read 2026-10-27.

On reversal, the plan or issuer "immediately must provide coverage or payment"
for the claim. Source: [45 CFR 147.136](https://www.law.cornell.edu/cfr/text/45/147.136), paragraph (d)(2)(iv), read 2026-10-27.

### Government programs

The Department of Labor says Medicare, Medicaid, and FEHB are not covered by
these ERISA claim-procedure rules and "have their own specific rules for claims
procedures." Source: [DOL benefit claims FAQ](https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/resource-center/faqs/benefit-claims-procedure-regulation), A-1, read 2026-10-27.

| Program | Different route and starting point | Source |
| --- | --- | --- |
| Medicare | Medicare Advantage starts with "Reconsideration by the Medicare Health Plan." Other Medicare starting routes: NOT PUBLISHED in the reviewed page. | [CMS Medicare Part C appeals overview](https://www.cms.gov/medicare/appeals-grievances/managed-care-appeals-grievances/appeals-overview), section "five successive levels of appeal," read 2026-10-27 |
| Medicaid | Route differs. Starting point: NOT PUBLISHED. | [DOL benefit claims FAQ](https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/resource-center/faqs/benefit-claims-procedure-regulation), A-1, read 2026-10-27 |
| TRICARE | Route differs. "Start the appeal process on TRICARE.mil" and follow the program notice. | [CMS TRICARE action plan](https://www.cms.gov/initiatives/your-patient-rights/medical-bill-rights/get-help/find-action-plan/care-tricare), section "File an appeal with TRICARE," read 2026-10-27 |
| FEHB | Route differs. Starting point: NOT PUBLISHED. | [DOL benefit claims FAQ](https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/resource-center/faqs/benefit-claims-procedure-regulation), A-1, read 2026-10-27 |

## 3. The rungs

| Rung | When it opens | What to send | Where and deadline |
| --- | --- | --- | --- |
| Correction or reconsideration | The notice asks for a missing, incomplete, or incorrect claim item and the existing records resolve it. | Reconsideration letter, EOB, denial, corrected field or named attachment, and proof of the original submission when relevant. | Use the denial notice first, then the insurer row in `payer-appeals.csv`. Preserve the internal-appeal clock. Source: product decision inputs reviewed 2026-10-27 and payer row source. |
| First-level internal appeal | The notice makes a benefit decision, or a correction was not accepted and the notice provides appeal rights. | First-level letter, EOB, denial, superbill, proof of payment, plan language supplied by the person, and only relevant therapist documentation. | Use the denial notice first. Otherwise use `payer-appeals.csv`. For an ERISA plan, the baseline request period is 180 days under 29 CFR 2560.503-1(h)(3)(i), read 2026-10-27. |
| Second-level internal appeal | The first-level decision is upheld and the insurer row or decision letter publishes a second level. | Second-level request or first-level shape labeled second level, first-level decision, earlier packet, and any new record evidence. | Use the first-level decision and the insurer row. If either says `NOT PUBLISHED`, do not invent a second level or deadline. Source: four dated payer appeal inventories, read 2026-10-09. |
| External review | A final internal adverse decision states external-review eligibility, or the controlling process allows earlier review. | External-review request shape, final internal decision, denial, EOB, relevant records, and the state or federal form's published items. | Use the decision notice and the state table. Federal baseline is four months under 45 CFR 147.136(d)(2)(ii), read 2026-10-27. State and plan eligibility can differ. |
| State regulator complaint | The person wants the regulator to review handling, routing, delay, or another documented concern. It does not replace an appeal unless the regulator says it does. | Complaint shape, notices, submission proof, decisions, a timeline from records, and only relevant attachments. | Use the documented state row. A generic complaint deadline is NOT PUBLISHED. Source: `appeals-by-channel.md`, research date 2026-10-07. |

## 4. State external review and regulator routes

These rows reproduce only `DOCUMENTED` state findings from
`appeals-by-channel.md`, research date 2026-10-07. The plan's funding, policy
situs, product, and notice determine whether a route applies. The person's
residence alone does not. A regulator complaint does not automatically preserve
an appeal deadline. Source: the same input, section "Nineteen state frameworks
for fully insured plans."

| State | External review route and timing | Regulator route | Source and input date |
| --- | --- | --- | --- |
| AL | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| AK | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| AZ | DIFI health-care appeal packet; statute states four months under its specified sections. | Arizona DIFI packet route. | [DIFI packet](https://difi.az.gov/sites/default/files/Final%20Health%20Care%20Appeal%20Packet_6.28.24%20%281%29.pdf); [ARS 20-2537](https://www.azleg.gov/ars/20/02537.htm); input 2026-10-07 |
| AR | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| CA | CDI independent medical review generally allows six months after an insurer uphold; DMHC has a separate complaint and IMR process. | Use CDI or DMHC according to the plan regulator. | [CDI](https://www.insurance.ca.gov/01-consumers/110-health/60-resources/01-imr/index.cfm); [DMHC](https://www.dmhc.ca.gov/FileaComplaint/IndependentMedicalReviewComplaintForms.aspx); input 2026-10-07 |
| CO | Statutory external review under CRS 10-16-113.5; four months after internal appeal denial. | Regulator intake: NOT PUBLISHED. | [Colorado legislative text](https://leg.colorado.gov/sites/default/files/images/olls/crs2024-title-10.pdf), pages 796 and 799; input 2026-10-07 |
| CT | Connecticut Insurance Department external review; 120 days after written notice that internal appeals are exhausted. | Connecticut Insurance Department. | [CID route](https://portal.ct.gov/cid/consumer-information-center/consumer-resource-library/external-review); [application](https://portal.ct.gov/cid/-/media/cid/forms/external-review-application.pdf); input 2026-10-07 |
| DE | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| FL | Federal external review described in Florida behavioral-health guidance; 180 days internal and four months external, subject to scope. | Florida DFS guidance route. | [Florida DFS](https://myfloridacfo.com/division/consumers/consumerprotections/behavioralhealthoverview); input 2026-10-07 |
| GA | Georgia managed-care independent-review rules coexist with the applicable federal process; exact product deadline NOT PUBLISHED. | Georgia OCI rule route. | [Georgia rule](https://oci.georgia.gov/document/document/120-2-111-04pdf/download); [CMS map](https://www.cms.gov/cciio/resources/files/external_appeals); input 2026-10-07 |
| HI | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| ID | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| IL | IDOI external review for eligible state-regulated plans; four months after final adverse determination. | Illinois Department of Insurance. | [IDOI](https://idoi.illinois.gov/consumers/file-an-external-review.html); input 2026-10-07 |
| IN | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| IA | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| KS | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| KY | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| LA | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| ME | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| MD | Maryland Insurance Administration after the insurer grievance process; four months after the grievance decision. | Maryland Insurance Administration. | [MIA](https://insurance.maryland.gov/consumer/pages/appealsandgrievances.aspx); input 2026-10-07 |
| MA | Office of Patient Protection external review; four months for eligible denials. | Massachusetts Office of Patient Protection. | [OPP](https://www.mass.gov/info-details/external-review-process-overview); input 2026-10-07 |
| MI | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| MN | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| MS | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| MO | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| MT | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| NE | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| NV | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| NH | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| NJ | DOBI IURO for eligible utilization-management denials; four months after final internal decision. | New Jersey Department of Banking and Insurance. | [DOBI](https://nj.gov/dobi/chap352/352umappealsqanda.html); input 2026-10-07 |
| NM | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| NY | DFS external appeal; member deadline four months from final first-level denial. An optional second internal review does not extend it. | New York Department of Financial Services. | [DFS](https://www.dfs.ny.gov/complaints/file_external_appeal); input 2026-10-07 |
| NC | Smart NC external review for eligible denials; 120 days after final adverse decision. | North Carolina Department of Insurance. | [NCDOI](https://www.ncdoi.gov/consumers/health-insurance/health-claim-denied/request-external-review); input 2026-10-07 |
| ND | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| OH | External request within 180 days after final adverse determination under ORC 3922. | Regulator intake: NOT PUBLISHED. | [ORC 3922](https://codes.ohio.gov/ohio-revised-code/chapter-3922); input 2026-10-07 |
| OK | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| OR | IRO assigned through Oregon DFR; 180 days after final written internal decision. | Oregon Division of Financial Regulation. | [DFR](https://dfr.oregon.gov/business/reg/health/pages/external-review.aspx); [ORS 743B](https://www.oregonlegislature.gov/bills_laws/ors/ors743B.html); input 2026-10-07 |
| PA | Pennsylvania independent review; four months from final denial. | Pennsylvania Insurance Department. | [PID](https://www.pa.gov/services/insurance/request-a-review-if-your-health-insurance-denied-a-treatment-medication-or-service); input 2026-10-07 |
| RI | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| SC | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| SD | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| TN | Written external-review request to the carrier for qualifying denials; 180 days after final determination. | Tennessee Department of Commerce and Insurance disclosure route. | [TDCI](https://www.tn.gov/content/dam/tn/commerce/documents/insurance/forms/ERODisclosureForm08212024.pdf); input 2026-10-07 |
| TX | Use the denial's federal or state external route; exact case deadline NOT PUBLISHED. | Texas Department of Insurance complaint and assistance route. | [TDI](https://www.tdi.texas.gov/consumer/complaint-health.html); input 2026-10-07 |
| UT | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| VT | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| VA | SCC external review for eligible Virginia plans; 120 days after notice of the external-review right. | Virginia State Corporation Commission Bureau of Insurance. | [SCC](https://www.scc.virginia.gov/consumers/insurance/health-insurance-consumer/external-review/); input 2026-10-07 |
| WA | Independent review for qualifying medical-judgment decisions; notice must state a 180-day request period. | Regulator complaint intake: NOT PUBLISHED. | [WAC route](https://app.leg.wa.gov/wac/default.aspx?cite=284-43A-140); [deadline rule](https://app.leg.wa.gov/wac/default.aspx?cite=284%2D43%2D3150); input 2026-10-07 |
| WV | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| WI | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |
| WY | NOT PUBLISHED | NOT PUBLISHED | NOT PUBLISHED |

## 5. Mental health parity in plain words

Federal law says a covered plan's mental-health and substance-use financial
requirements may be "no more restrictive" than the predominant requirements
applied to substantially all medical and surgical benefits.
Source: [29 U.S.C. 1185a](https://www.law.cornell.edu/uscode/text/29/1185a), section (a)(3)(A)(i), read 2026-10-27.

It also says treatment limitations may be "no more restrictive" than the
predominant limitations applied to substantially all medical and surgical
benefits. Source: [29 U.S.C. 1185a](https://www.law.cornell.edu/uscode/text/29/1185a), section (a)(3)(A)(ii), read 2026-10-27.

If a covered plan provides medical or surgical benefits through
"out-of-network providers," the statute requires consistent out-of-network
mental-health or substance-use benefits. Source:
[29 U.S.C. 1185a](https://www.law.cornell.edu/uscode/text/29/1185a), section
(a)(5), read 2026-10-27.

The 2013 final rule says it implements parity "with respect to financial
requirements and treatment limitations" for group plans and group and
individual insurance coverage. Source: [78 FR 68240](https://www.govinfo.gov/content/pkg/FR-2013-11-13/pdf/2013-27086.pdf), Summary, published 2013-11-13, read 2026-10-27.

Use a parity paragraph only when the supplied plan records show the medical or
surgical comparison. State the two recorded terms and ask the reviewer to
apply 29 U.S.C. 1185a(a)(3)(A) and the 2013 final rule, 78 FR 68240. Do not
state that a violation occurred. Do not cite a later rule in the letter.

## 6. Letter shapes

Fill only from the EOB, denial letter, superbill, plan records, tracker, and the
person's answers. Replace a missing field with `[ASK]`. Do not silently omit or
infer it. Keep signature and date blank. Source for claim fields:
`appeal-letter-input.ts`, reviewed 2026-10-27.

### Reconsideration for a paperwork fix

```text
[INSURER ADDRESS OR ROUTE FROM NOTICE]

Re: request for reconsideration and reprocessing
member: [MEMBER NAME FROM EOB]
member ID: [MEMBER ID FROM EOB OR CARD]
claim number: [CLAIM NUMBER FROM EOB]
date or dates of service: [DATES FROM EOB AND SUPERBILL]
denial notice date: [DATE FROM NOTICE]

I request reconsideration and reprocessing of this member-paid out-of-network
claim. The notice states: [NOTICE REASON, QUOTED OR CLOSELY RESTATED]. It asks
for: [MISSING OR CORRECTED ITEM]. I am providing [ATTACHMENT OR RECORD VALUE].
No diagnosis, code, date, fee, or provider fact has been changed unless the
attached record itself shows the correction.

Any benefit payment due for this member-paid out-of-network claim should be
paid to the member. This letter does not assign benefits or change the payee.

Please confirm reprocessing in writing. Please also provide, at no charge,
copies of all documents, records, and other information relevant to this claim
and review, including the plan terms and criteria relied on.

signature: ____________________
date: ____________________
```

### First-level internal appeal

```text
[INSURER APPEAL ADDRESS OR ROUTE FROM NOTICE]

Re: first-level appeal
member: [MEMBER NAME FROM EOB]
member ID: [MEMBER ID FROM EOB OR CARD]
claim number: [CLAIM NUMBER FROM EOB]
date or dates of service: [DATES FROM EOB AND SUPERBILL]
denied or underpaid amount: [AMOUNT FROM EOB]
denial notice date: [DATE FROM NOTICE]

I appeal the benefit decision stated as: [NOTICE REASON, QUOTED OR CLOSELY
RESTATED]. The records show: [FACTS FROM EOB, SUPERBILL, PLAN, TRACKER, OR
PERSON'S ANSWER]. I ask the plan to review the attached records and the plan
term identified as [PLAN TERM OR [ASK]].

[OPTIONAL PARITY PARAGRAPH ONLY WHEN THE REQUIRED COMPARISON IS IN THE RECORDS]

Any benefit payment due for this member-paid out-of-network claim should be
paid to the member. This letter does not assign benefits or change the payee.

Please reverse or revise the decision only to the extent supported by the
records. Please provide, at no charge, copies of all documents, records, and
other information relevant to this claim and review, including the plan terms
and criteria relied on.

signature: ____________________
date: ____________________
```

### External review request

```text
[EXTERNAL REVIEW ROUTE FROM FINAL DECISION OR STATE TABLE]

Re: request for external review
member: [MEMBER NAME FROM FINAL DECISION]
member ID: [MEMBER ID FROM FINAL DECISION OR CARD]
claim number: [CLAIM NUMBER]
date or dates of service: [DATES]
final internal decision date: [DATE]

I request external review of the final internal decision stated as: [FINAL
DECISION REASON, QUOTED OR CLOSELY RESTATED]. I completed the internal process
as shown by [FINAL DECISION OR EXHAUSTION RECORD]. The records I ask the
reviewer to consider are: [ATTACHMENTS].

[OPTIONAL PARITY PARAGRAPH ONLY WHEN THE REQUIRED COMPARISON IS IN THE RECORDS]

Any benefit payment due for this member-paid out-of-network claim should be
paid to the member. This request does not assign benefits or change the payee.

Please provide the written external-review decision. Please also provide,
at no charge, copies of all documents, records, and other information
relevant to this claim and review, including the plan terms and criteria relied
on.

signature: ____________________
date: ____________________
```

### Regulator complaint

```text
[REGULATOR ROUTE FROM STATE TABLE]

Re: complaint about handling of a health claim and appeal
member: [MEMBER NAME FROM RECORDS]
insurer and plan: [FROM CARD OR PLAN]
claim number: [FROM EOB]
date or dates of service: [FROM EOB AND SUPERBILL]

I ask the regulator to review this documented concern: [DELAY, ROUTING,
NOTICE, OR OTHER FACT FROM RECORDS]. The timeline is: [DATED EVENTS FROM EOB,
DENIALS, DECISIONS, SUBMISSION PROOF, AND TRACKER]. I am not asking this
complaint to replace any appeal unless the regulator confirms that result.

Any benefit payment due for this member-paid out-of-network claim should be
paid to the member. This complaint does not assign benefits or change the
payee.

Please confirm receipt and identify any next step. Please also provide, at no
charge, copies of all documents, records, and other information relevant to
this claim and review, including the plan terms and criteria relied on.

signature: ____________________
date: ____________________
```

## 7. Attachments by rung

| Rung | Attachment checklist | Source |
| --- | --- | --- |
| Reconsideration | EOB; denial letter; the exact missing attachment or existing record that corrects the named field; original submission proof when relevant. | Product correction rules reviewed 2026-10-27; selected payer include list. |
| First-level appeal | EOB; denial letter; superbill; proof of payment; claim submission proof; cited plan pages supplied by the person; only relevant therapist records; representative form only if the person chose a representative. | `appeal-letter-input.ts`, reviewed 2026-10-27; selected payer include list. |
| Second-level appeal | First-level decision; first-level packet; new record evidence if any; second-level form when the insurer publishes one. | Four payer appeal inventories, read 2026-10-09. |
| External review | Final internal decision; denial and EOB; internal packet; external-review form; identification-card copy and clinical support only where the published route asks for them. | Selected state row and payer external-review cell. |
| Regulator complaint | Notices; decisions; dated submission and receipt proof; tracker timeline; only documents needed to show the complaint. | `appeals-by-channel.md`, research date 2026-10-07. |

Never attach an entire clinical file by default. Use only records relevant to
the stated reason and the route's published request. No source reviewed here
authorizes inventing, changing, or expanding clinical content.

## 8. What the letter never says

The letter never says that treatment was medically necessary beyond what the
therapist's own signed documentation says. It never proposes or changes a
diagnosis, procedure code, modifier, place of service, date, fee, or provider
fact. It never adds a fact or quotation absent from the records. It never
threatens the insurer, predicts an outcome, or states a legal conclusion.
Source: W4 drafting rule and product letter input, reviewed 2026-10-27.

When the denial says a therapist's medical-necessity letter is missing, give
the person exactly this request to send:

```text
Please provide a signed and dated letter based only on your existing records
for the service or services identified in the denial. Please state the
documented diagnosis and codes already used, the dates and type of service, the
documented clinical rationale and frequency, and any record-based response to
the insurer's stated criterion. Please do not add a fact or quotation, and do
not change a diagnosis, code, date, fee, place of service, modifier, or provider
detail unless your records show that a correction is required.
```
