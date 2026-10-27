# Changelog

## 0.1.0, 10-27-2026

### Seven routines

- `file-my-claim` prepares a person's claim packet and submission steps.
- `check-my-superbill` checks a superbill against published structure rules.
- `read-my-benefits` explains supplied plan terms and estimates one session when every input is present.
- `track-my-claim` maintains a claim tracker and reads an EOB in plain words.
- `appeal-my-denial` prepares a denial response, appeal letter, and attachment list.
- `client-handout` makes a one-page handout from public practice facts and one insurer row.
- `superbill-template` makes a reusable blank template from public practice facts.

### Five things it never does

- It never files or submits a claim or appeal.
- It never changes or invents a code, date, fee, diagnosis, provider detail, plan fact, or insurer rule.
- It never logs in, calls, emails, or contacts anyone for the person.
- It never signs a member, provider, or assignment field.
- It never sends a person's documents or health information to recoupr.

Insurer facts carry a read date. The insurer's own page controls.
