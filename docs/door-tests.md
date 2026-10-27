> The founder must approve this document before publication or use.

# Door tests

Live tests of the doors, recorded as they happen (each line carries its date):

- 2026-10-27, Claude (claude-sonnet-5-5, headless, no tools, paste-in prompt alone with a sentinel superbill): guardrails held, nothing invented, intake and superbill confirmation as written; before the insurer-page block was added it could not name a route and sent the person to https://recoupr.ai/insurers/. Pass with the block added.
- 2026-10-27, ChatGPT logged out (https://chatgpt.com, paste-in of 105,221 characters as the first message): the message was accepted into the composer three times and never produced a reply or an error; the text returned to the composer. Not a pass, not a fail: the logged-out tier did not answer. Needs a logged-in run.
- 2026-10-27, Grok logged out (https://grok.com, same paste-in): sending opened a "Sign up to continue" wall. Needs a logged-in run.
- Gemini: not run; skills upload needs a signed-in personal Google account on the web or Mac app.
- Claude free tier ZIP upload, ChatGPT desktop ZIP, Gemini folder upload, Grok file upload: not run.
