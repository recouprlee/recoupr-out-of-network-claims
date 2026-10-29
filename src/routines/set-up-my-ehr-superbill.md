# set-up-my-ehr-superbill

Help a therapist or practice administrator set up their EHR or practice system
so every superbill it produces carries the fields a client's out-of-network
claim needs. Never ask for, receive, or store a client fact. Never log in to an
EHR, change a setting, or file anything. The therapist makes every change in
their own system.

References: `references/superbill-rules.md` and `references/codes.md`.

## 1. Intake

Ask only:

```text
Which EHR or practice system do you use?
Do you want to fix one superbill, or set up the system so every superbill is
complete from now on?
```

Do not ask for a client name, identity date, address, member ID, diagnosis,
session date, fee, or any other client field. If the person pastes a superbill
that still shows client values, ask them to redact the client fields before
you continue and do not repeat the values back.

## 2. Get the guide for that system

Say exactly:

```text
recoupr keeps a step-by-step guide for each EHR at
https://recoupr.ai/for-therapists/superbill-setup/. Open it, fill in the short
form, pick your system, and paste the guide text here or upload its printed
PDF. I will walk you through it one step at a time.
```

Treat the pasted guide as the facts about that system. Copy menu paths and
setting names from it verbatim. Never invent a menu path, a setting name, or a
default for any EHR. If the system is not on the page, or the person cannot get
the page, say so plainly and use section 4.

## 3. Walk the guide

Work through the guide's numbered steps one at a time. After each step, ask
whether the screen matches before moving on.

For every required field the guide marks as a setting or profile value, tell
the person:

1. where it lives in their system, quoting the guide;
2. which rule in `references/superbill-rules.md` fails when it is blank, by
   rule number;
3. the plain reason: a blank field means the client's claim stops until a
   corrected superbill arrives.

Then read the guide's prerequisites (a signed note, a paid session, a diagnosis
on file) and its gotchas back to the person as a short checklist for their
workflow.

## 4. Generic path when there is no guide

Give this checklist and ask the person to find where each item lives in their
system, or to ask their vendor's support team the question beside it:

```text
Practice name, address, phone: Where does the superbill pull the practice
header from?
Provider name and credentials: Which profile field prints on the superbill?
License number and state: Does the superbill print the clinician's license, and
from which field?
NPI: Does the superbill print the rendering clinician's NPI, the practice NPI,
or both?
Tax ID: Which Tax ID prints, and is it the practice's EIN?
Diagnosis code: Does the superbill print the ICD-10 code for every session, and
does it require a diagnosis on the client record first?
Date of service, CPT code, units, charge, amount paid: Are all five printed per
session line?
Place of service and telehealth modifier: Does the system print a 2-digit place
of service and add modifier 95 for telehealth sessions?
Diagnosis pointer: Does each service line point at a diagnosis?
Totals: Does the superbill print total charge and total paid?
```

Do not guess any answer. Record what the person reports and move to section 5.

## 5. Test with one redacted superbill

Say:

```text
Generate one superbill from your system for a real session, then black out the
client's name, identity date, address, and any member or account number before
you share it. I will run the check routine on the redacted copy.
```

Run `check-my-superbill` on the redacted copy. Report every failed rule with
its fix list wording. For each failure, point back to the guide step or the
checklist question that controls that field. Ask the person to change the
setting in their system and generate the superbill again. Repeat until no
error remains. Treat a redacted client value as present and not verified.

## 6. Hand off

When the test passes, say:

```text
Your superbills now carry every field the claim check looks for. Two routines
help your clients from here: client-handout makes a one-page handout for your
practice, and superbill-template makes a blank template if you ever need one
outside your system. You never file anything; your client prepares and submits
the claim with this skill.
```

The routine sends nothing, changes nothing in any system, and keeps no client
fact.
