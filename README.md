# recoupr Out-of-Network Claims

A free skill for the AI assistant you already use. It reads your therapist's superbill and your plan documents, prepares your out-of-network therapy claim or your appeal, and you submit it yourself. No account, no fee, no cut. Your health information never touches recoupr.

Skill folder and name field: `recoupr-out-of-network-claims`.

## Get it

The easiest path is the download page: https://recoupr.ai/get-the-skill. It has one setup line per assistant.

From this repository:

- **ZIP of the skill folder**: https://github.com/recouprlee/recoupr-out-of-network-claims/releases/latest/download/recoupr-out-of-network-claims.zip. Unzip it and keep the folder together; `SKILL.md` is only the menu, the routines and references sit beside it.
- **Paste-in prompt** (one file for assistants with no skill loader): https://github.com/recouprlee/recoupr-out-of-network-claims/releases/latest/download/paste-in-prompt.md. Attach it to your first message and say "follow the attached skill".
- **Claude Code**: `/plugin install recoupr-out-of-network-claims --marketplace recouprlee/recoupr-out-of-network-claims` in a session (Claude Code 2.1.275 or later), or `/plugin marketplace add recouprlee/recoupr-out-of-network-claims` then `/plugin install recoupr-out-of-network-claims@recoupr-skills`.

The paste-in door was tested in October 2026 on Claude, ChatGPT, Gemini and Grok. Details in `docs/door-tests.md`.

## What is inside

Seven routines, in `src/routines/`:

| Routine | What it does |
| --- | --- |
| `file-my-claim` | Prepares the claim packet and the submission steps for your insurer |
| `check-my-superbill` | Checks a superbill against published structure rules and lists what is missing |
| `read-my-benefits` | Explains the plan terms you supply and estimates one session when every input is present |
| `track-my-claim` | Keeps a claim tracker and reads an explanation of benefits in plain words |
| `appeal-my-denial` | Prepares a denial response, an appeal letter and the attachment list |
| `client-handout` | Makes a one-page handout for a practice from public facts and one insurer row |
| `superbill-template` | Makes a blank superbill template from public practice facts |

References, in `src/references/`: the insurer atlas (76 insurers, every row with a public source URL and a read date), filing steps, mailing addresses, member forms, CPT and ICD-10 notes, EOB codes, appeal rules and the source list. Three small scripts in `scripts/` check a superbill's structure, compute appeal deadlines and estimate a benefit. They use only the Python standard library; the routines run them when a code runtime is available and fall back to the written rules when it is not.

## What it never does

- It never files or submits a claim or appeal. You do.
- It never changes or invents a code, date, fee, diagnosis, provider detail, plan fact or insurer rule.
- It never logs in, calls, emails or contacts anyone for you.
- It never signs a member, provider or assignment field.
- It never sends your documents or health information to recoupr.

Every insurer fact carries a read date. The insurer's own current page controls.

## Privacy

recoupr has no account for you and receives nothing from the skill. Anything you give your AI assistant goes to that vendor under its terms. If you would rather not upload documents, the skill has a paper mode that asks only for your insurer and state.

## Not advice

The skill is general information and document preparation help. It is not legal, medical, clinical, tax, insurance or billing advice. Terms: https://recoupr.ai/terms. Privacy: https://recoupr.ai/privacy.

## Contributing and security

Insurer rows change. Use the "Insurer row change" issue form with the public source URL, or read `CONTRIBUTING.md`. Never include personal data or health information in an issue.

Security reports go to howdy@recoupr.ai, not to a public issue. See `SECURITY.md`.

## License and trademark

Code and scripts: Apache License 2.0 (`LICENSE`). Written content (routines, references, templates): Creative Commons Attribution 4.0 (`LICENSE-CONTENT`). The recoupr name and logo are trademarks of recoupr LLC and are not licensed; see section 6 of the Apache License.

https://recoupr.ai
