# Portfolio Request survey

Internal survey where sales reps flag product gaps and portfolio requests for review. Reps pick the closest matching product (with a photo), describe the technical requirement, tag competitors and target markets, and give pricing/volume expectations. Submitting emails Austin directly — no extra step.

**Live page:** https://sirkinagghide.github.io/Balluff_Tools/portfolio-survey/

## Files

- `index.html` — the full page, plain static HTML/CSS/JS, no build step
- `photos/` — product reference photos shown in the picker, named `<product-code>.jpg` (or `<code>-<variant>.jpg` where a code covers more than one product)

## How submission works

The form posts to [FormSubmit](https://formsubmit.co/) (`https://formsubmit.co/ajax/austin.sirkin@balluff.com`), which emails the submission directly — no backend of our own. FormSubmit requires a one-time confirmation: the *first* submission ever sent to this email address triggers an activation email from FormSubmit that must be clicked before delivery starts working. After that, every submission auto-delivers.

There's no separate dashboard/log — each submission is one email. To keep them organized, set up a filter/rule in your email client for subject lines starting `Portfolio Request` (e.g. auto-label or move to a folder).

## Updating

Hosted via GitHub Pages, served from `main` at the repo root. Edit `index.html` (and `photos/` as needed), commit, and push to `main` — Pages redeploys automatically within a minute or two.
