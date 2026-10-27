import csv
import re
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "src" / "references" / "payer-atlas.csv"
ADDRESSES = ROOT / "src" / "references" / "addresses.csv"
FORMS = ROOT / "src" / "references" / "forms"
HEADER = [
    "insurer",
    "aliases",
    "states",
    "payer_kind",
    "member_form_name",
    "member_form_number",
    "member_form_revision",
    "member_form_url",
    "form_fillable",
    "portal_upload",
    "portal_name",
    "portal_path",
    "file_types",
    "confirmation",
    "mail_address",
    "fax",
    "attachments",
    "superbill_alone_accepted",
    "cms1500_required",
    "member_signature",
    "provider_signature",
    "payment_to_member",
    "member_deadline",
    "deadline_basis",
    "status_check",
    "processing_time",
    "mh_route",
    "provider_on_file_requirement",
    "in_network_superbill_note",
    "caveats",
    "source_url",
    "verified_on",
]
OPTIONAL_COLUMNS = {"aliases", "states", "fax", "mail_address", "caveats"}
BINARY_LITERALS = {"YES", "NO", "NOT PUBLISHED"}
RESEARCH_LITERALS = {
    'portal_upload': set(),
    'superbill_alone_accepted': {
        'NO: Blue Shield claim form plus itemized provider bill is required',
        'NO: Claim Form 17925 plus itemized bills is required for the public PDF route',
        'NO: Claim Form 228934 plus original itemized bill is required',
        'NO: DD Form 2642 and supporting documents are required',
        'NO: Health Benefits Claim Form plus itemized bills is required on the published member route',
        'NO: Medical Claim Form 24066MUMENABS plus an itemized bill is required for the public PDF route',
        'NO: Medical Claim Form and itemized bill are required',
        'NO: Medical Claim Form plus itemized bills or receipts is required',
        'NO: Medical Claim Form plus original itemized bills or receipts is required; a superbill may serve as the itemized bill',
        'NO: Member Medical Claim Form plus itemized bill is required for the public PDF route',
        'NO: Out-of-Plan Reimbursement Form F005 plus the original itemized bill is required',
        'NO: Oxford form plus Superbill or Invoice and payment receipts is required',
        'NO: Statement of Medical Claim MBS-010 requires the member page plus either the provider page or an itemized bill; a superbill is not named',
        'NO: Subscriber Health Care Claim Form plus receipts and/or a superbill is required',
        'NO: submit only CMS-1500 (02-12); supporting bills or receipts may also be required',
        'NO: the online route requires claim information plus a receipt; the PDF route requires Member Claim Form BE236 plus provider receipts',
        'NO: the portal requires on-screen claim information plus required documents; the PDF route requires the member form plus itemized bills',
        'NOT PUBLISHED: login-gated form and instructions are UNREADABLE',
        'NOT PUBLISHED: the portal waives the claim form but does not expressly name a superbill',
    },
    'cms1500_required': {
        'NO: CMS-1500 is not required; the 2026 brochure permits CMS-1500 or a claim form containing the listed information when the member must file',
        'NO: Horizon uses its member form or the online workflow with an itemized bill; CMS-1500 is not required or named',
        'NO: an itemized provider bill is accepted with DD Form 2642',
        'NO: member form plus itemized bill or superbill is the published route',
        'NO: the Anthem Member Medical Claim Form is accepted',
        'NO: the Anthem member Medical Claim Form is accepted',
        'NO: the Anthem member form is accepted; CMS-1500 is not required or named',
        'NO: the Medical Mutual member claim form is accepted',
        'NO: the Oxford New York member Medical Claim Form is accepted',
        'NO: the Oxford member Medical Claim Form is accepted',
        "NO: the Subscriber's Statement of Claim is the published member form",
        'NO: the member portal or Member Claim Form BE236 is the published route; CMS-1500 is not required or named',
        'NO: the provider may complete the embedded HCFA-1500 page or attach an itemized bill instead',
        'NOT PUBLISHED: CMS-1500 is not mentioned',
        'NOT PUBLISHED: CMS-1500 is not mentioned in the member instructions',
        'NOT PUBLISHED: login-gated form and instructions are UNREADABLE',
        'PLAN-DEPENDENT',
        'YES: CMS-1500 (02-12) is the required claim form',
        'YES: a completed CMS form from the provider is mandatory',
    },
    'payment_to_member': {
        'Claim payments are issued only to the policyholder; an optional assignment requests provider payment, but CareFirst reserves the right to pay the subscriber',
        'For an out-of-network provider, leave Payment Instructions unsigned; Cigna says it sends payment to the member when the provider has no contract and/or that section is blank',
        'Generally YES for nonparticipating-provider services according to Anthem provider guidance; mandates and negotiated arrangements can alter payment',
        'Generally sent to the member for a nonparticipating provider, subject to mandates or negotiated agreements',
        'If benefits are not assigned, payment may be made to the member or provider; signing Authorization of Payment requests direct provider payment',
        'Insured or subscriber, as stated in the form title',
        'Member or beneficiary reimbursement after paying a nonparticipating provider; DD 2642 has no assignment-of-benefits field',
        'Member reimbursement when proof of payment is attached and the optional assignment section is not completed; otherwise payment may go to the provider',
        'Member unless the Assignment of Benefits box requesting direct provider payment is checked',
        'Member unless the optional assignment section is completed; the form says completing it sends payment directly to the provider',
        'Member when SELF is selected; provider when PROVIDER is selected and item 14 is signed',
        'Member when To me, the subscriber is selected and proof of payment is supplied; provider when Directly to the provider of service is selected',
        'Member: Blue Cross NC describes self-filing as reimbursement or being paid back for covered services',
        'Member: the public instructions say the form is used to be reimbursed and contain no assignment-of-benefits field',
        'Member; if box 13 assignment is signed, Carelon pays the provider instead',
        'NO: cited Oregon individual policy states Regence pays out-of-network providers directly',
        'NOT GUARANTEED: Asuris decides whether to pay the member, provider, or both jointly, subject to legal requirements',
        "NOT PUBLISHED: cited 2026 group contract permits payment to the member, provider, another person, or jointly at Premera's option",
        'NOT PUBLISHED: current form and QHP page do not state the payment recipient',
        'NOT PUBLISHED: issuing home Plan controls',
        'NOT PUBLISHED: the current form only states that a participating provider is paid directly',
        'NOT PUBLISHED: the form has optional direct-provider assignment language but does not state the default payee when it is unsigned',
        'NOT PUBLISHED: the paper form requires non-Medicare members to authorize payment to the named provider and provides no box that leaves payment with the member',
        'NOT PUBLISHED; INFERRED: leave optional block 28 unsigned to avoid direct provider payment',
        'NOT PUBLISHED; INFERRED: leave the direct-to-provider assignment box unchecked',
        'NOT PUBLISHED; INFERRED: the form requests reimbursement after the member paid, but it does not identify the payee',
        'NOT PUBLISHED; INFERRED: the form requests reimbursement and requires proof of payment, but it does not identify the payee',
        'NOT PUBLISHED; INFERRED: the form requests reimbursement for a service paid in full, but it does not identify the payee',
        'NOT PUBLISHED; INFERRED: this is a member-submitted paid-claim route, but the current form and handbook do not state the payee',
        'PLAN-DEPENDENT: UMP may pay the member, provider, or both jointly; proof of payment can be required when the member paid before submitting',
        'PLAN-DEPENDENT: cited policy permits payment directly to the provider or solely to the insured when sufficient proof shows the bill was paid in full',
        'PLAN-DEPENDENT: in most cases payment is member-payable to the subscriber, but payment may go to the provider by plan type and service',
        'Payments for services from a nonparticipating provider are generally sent to the member',
        'Payments for services from a nonparticipating provider are generally sent to the member, subject to mandates or agreements',
        'Reimbursement is sent to the Plan subscriber at the address on record',
        'Select Issue payment to Member',
        'Select Pay to Member',
        'Select To pay Insured/Subscriber; do not select in-network credit',
        'The 2026 Texas EOC says benefits are paid to the member unless the member directs provider payment; the current universal form says member payment occurs only when the provider indicates it, creating a published conflict',
        'YES only when Policyholder payment (me) is selected on the form; 2026 PPO policy reserves the right to pay the provider directly',
        'YES when No is checked for authorization to pay the provider',
        'YES when To pay Insured/Subscriber is selected; the alternate selection requests in-network credit for a cash payment',
        'YES when assignment is not signed; the form says sign assignment only to pay the physician or supplier directly',
        'YES when benefits are not assigned; cited handbook says a paid provider bill is reimbursed to the member, and the form has a separate box to pay the provider directly',
        'YES when benefits are not assigned; the form states payment is made to the plan subscriber',
        'YES when money is due under plan benefits and benefits are not otherwise assigned',
        'YES when the assignment section is left blank',
        'YES when the provider has already been paid and the optional assignment signature is left unsigned',
        'YES: Surest says it may reimburse the member up to the maximum allowed amount when the plan has out-of-network benefits',
        'YES: applicable reimbursement can only be made payable to the primary cardholder',
        'YES: payment goes to the subscriber or policyholder unless alternate payee fields are completed',
        'YES: payment goes to the subscriber unless benefits are assigned or the plan provides otherwise',
        'YES: reimbursement check goes directly to the member for covered services from a nonparticipating provider',
        'YES: reimbursement is payable only to the primary card holder',
        'YES: the member pays for out-of-network care and submits for reimbursement',
        'YES; AZ Blue says payment for a non-contracted provider is sent directly to the member, minus cost share',
        'YES; claim payments are issued only to the policyholder unless assignment is completed, and CareFirst reserves the right to pay the subscriber',
    },
}
DASHES = {chr(0x2013), chr(0x2014)}


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


class AtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with ATLAS.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            cls.header = reader.fieldnames
            cls.rows = list(reader)

    def test_header_is_exact(self):
        self.assertEqual(HEADER, self.header)

    def test_address_research_matches_atlas(self):
        with ADDRESSES.open(newline="", encoding="utf-8") as handle:
            address_rows = list(csv.DictReader(handle))

        self.assertEqual(
            [row["insurer"] for row in self.rows],
            [row["insurer"] for row in address_rows],
        )
        for line_number, row in enumerate(address_rows, start=2):
            self.assertTrue(
                row["source_url"].startswith("https://"),
                f"line {line_number}: source_url must start with https://",
            )
            date.fromisoformat(row["read_date"])
        for line_number, row in enumerate(self.rows, start=2):
            self.assertTrue(
                row["mail_address"].strip(),
                f"line {line_number}: mail_address is empty",
            )

    def test_required_cells_are_not_empty(self):
        for line_number, row in enumerate(self.rows, start=2):
            for column in HEADER:
                if column not in OPTIONAL_COLUMNS:
                    self.assertTrue(
                        row[column].strip(),
                        f"line {line_number}: {column} is empty",
                    )

    def test_insurers_are_unique(self):
        insurers = [row["insurer"] for row in self.rows]
        self.assertEqual(len(insurers), len(set(insurers)))

    def test_source_urls_and_dates(self):
        for line_number, row in enumerate(self.rows, start=2):
            urls = row["source_url"].split(";")
            self.assertTrue(all(url.startswith("https://") for url in urls))
            verified = date.fromisoformat(row["verified_on"])
            self.assertEqual(2026, verified.year, f"line {line_number}")

    def test_states_are_semicolon_joined_codes(self):
        pattern = re.compile(r"[A-Z]{2}(?:;[A-Z]{2})*")
        for line_number, row in enumerate(self.rows, start=2):
            states = row["states"]
            self.assertTrue(
                not states or pattern.fullmatch(states),
                f"line {line_number}: invalid states",
            )

    def test_published_form_numbers_have_a_forms_file(self):
        form_names = {
            path.name for path in FORMS.glob("*.md") if path.name != "INDEX.md"
        }
        for line_number, row in enumerate(self.rows, start=2):
            number = row["member_form_number"]
            if number == "NOT PUBLISHED":
                continue
            suffix = f"-{slug(number)}.md"
            self.assertTrue(
                any(name.endswith(suffix) for name in form_names),
                f"line {line_number}: no forms file for {number}",
            )

    def test_judgment_columns_use_research_literals(self):
        columns = (
            "portal_upload",
            "superbill_alone_accepted",
            "cms1500_required",
            "payment_to_member",
        )
        for line_number, row in enumerate(self.rows, start=2):
            for column in columns:
                self.assertIn(
                    row[column],
                    BINARY_LITERALS | RESEARCH_LITERALS[column],
                    f"line {line_number}: unexpected {column} literal",
                )

    def test_forbidden_dashes_are_absent(self):
        text = ATLAS.read_text(encoding="utf-8")
        for dash in DASHES:
            self.assertNotIn(dash, text)

    def test_personal_data_scan_is_clean(self):
        spec = __import__("importlib.util").util.spec_from_file_location(
            "phi_scan", ROOT / "tools" / "phi_scan.py"
        )
        module = __import__("importlib.util").util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual([], module.scan_file(ATLAS))


if __name__ == "__main__":
    unittest.main()
