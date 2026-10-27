> The founder must approve this document before publication or use.

# Door tests

Live tests of the doors, recorded as they happen (each line carries its date):

- 2026-10-27, Claude (claude-sonnet-5-5, headless, no tools, paste-in prompt alone with a sentinel superbill): guardrails held, nothing invented, intake and superbill confirmation as written; before the insurer-page block was added it could not name a route and sent the person to https://recoupr.ai/insurers/. Pass with the block added.
- 2026-10-27, ChatGPT logged out (https://chatgpt.com, paste-in of 105,221 characters as the first message): the message was accepted into the composer three times and never produced a reply or an error. The logged-out tier did not answer.
- 2026-10-27, ChatGPT signed in (Instant mode, paste-in uploaded as a .md file plus a one-paragraph ask with a sentinel superbill for Blue Cross and Blue Shield of Texas): PASS. It said the route is not in the skill and that the skill forbids guessing, pointed to https://recoupr.ai/insurers/ and the member-services number, transcribed every value without inventing one, listed the missing superbill fields, asked plan type and other coverage, and closed with the skill's own "You submit your own claim" paragraph. Deviation: it skipped the scripted opening lines and the mode question.
- 2026-10-27, Grok logged out (https://grok.com, same paste-in): sending opened a "Sign up to continue" wall.
- 2026-10-27, Grok signed in (Fast mode, paste-in attached as a .md file plus the ask): PASS. Opening lines verbatim, asked document mode or paper mode, no route guessed.
- 2026-10-27, Gemini signed in (Flash, paste-in attached as a file plus the ask; the first upload needed Google's one-time "Creating content from images and files" agreement): PASS. Opening lines verbatim, mode question verbatim, then: insurer filing details are not in the references, never guess, open https://recoupr.ai/insurers/ and paste the page, else call the number on the card.
- Not yet run: the ZIP or folder door on each vendor (Claude Customize > Skills upload, ChatGPT desktop Skills, Gemini Customize > Skills with the folder, Grok Skills upload). The paste-in door passed on Claude, ChatGPT, Gemini and Grok.
- 2026-10-27, Muse (Meta), researched not run: Meta's help pages (read 2026-10-27) say skills are built by Meta only, with no import of a user's own skill; files uploaded in a conversation may be PDF, DOCX, plain text or Markdown; Memory.md and Soul.md can be edited directly; data is used to improve Meta's models unless "Help improve our AI models" is turned off; available in the United States on iOS, Android, web and WhatsApp. Door: attach the paste-in file to the first message, same as the others. A signed-in run needs a Meta account on the mini.
