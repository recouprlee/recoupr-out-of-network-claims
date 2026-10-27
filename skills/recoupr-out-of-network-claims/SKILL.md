---
name: recoupr-out-of-network-claims
description: Prepares a person's own out-of-network therapy insurance claim or appeal from their therapist's superbill, plan documents, EOB and denial letter. Use when someone mentions a superbill, out-of-network therapy, reimbursement, an EOB, a denied claim or an appeal. The person submits the claim themselves; nothing is filed for them.
license: Apache-2.0
metadata:
  author: recoupr
  version: "0.0.1"
  homepage: "https://recoupr.ai"
---
# recoupr Out-of-Network Claims

## Task menu

- **file-my-claim**: Say "Help me prepare my out-of-network claim."
- **check-my-superbill**: Say "Check my superbill."
- **read-my-benefits**: Say "Help me read my out-of-network benefits."
- **track-my-claim**: Say "Help me track my claim."
- **appeal-my-denial**: Say "Help me prepare my appeal."
- **client-handout**: Say "Make a client handout."
- **superbill-template**: Say "Make a superbill template."

## Guardrails

This skill never changes a code, a date, a fee or a diagnosis. It never files anything for anyone. The person reviews and submits every item. Assignment of benefits stays unsigned. This is not legal, medical or billing advice. The insurer's own page wins over this skill.

## Privacy

Documents go into the person's own assistant under that assistant's terms and never go to recoupr. A paper path exists for anyone who prefers it.

## Routines

- [file-my-claim](references/routines/file-my-claim.md)
- [check-my-superbill](references/routines/check-my-superbill.md)
- [read-my-benefits](references/routines/read-my-benefits.md)
- [track-my-claim](references/routines/track-my-claim.md)
- [appeal-my-denial](references/routines/appeal-my-denial.md)
- [client-handout](references/routines/client-handout.md)
- [superbill-template](references/routines/superbill-template.md)
