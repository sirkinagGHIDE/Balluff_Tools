# Portfolio Request survey

Internal survey where sales reps flag product gaps and portfolio requests for review. It covers the full Balluff portfolio: all 10 product areas from balluff.com (Sensors, RFID, Machine Vision & Optical ID, Industrial Communication, Connectivity, Control & Machine Lights, Power Supplies, Accessories, Systems Solutions, Software), 62 product families.

Reps filter by product area or search by code, pick the closest family, and describe the technical requirement. They also tag competitors (the list adapts to the selected product area), rank target markets, and give pricing and volume expectations. Submitting emails Austin directly. No extra step.

**Live page:** https://sirkinagghide.github.io/Balluff_Tools/portfolio-survey/

## Files

- `index.html` is the whole page: plain static HTML/CSS/JS, no build step.
- `photos/` holds real product reference photos, named `<product-key>.jpg`.
- `assets/` holds brand assets copied unmodified from the Balluff brand substrate ([MultiMind-Studio/ai-marketing2](https://github.com/MultiMind-Studio/ai-marketing2)):
  - the wordmark (`balluff-wordmark-black.svg`)
  - the B-signet + claim lockup (`balluff-claim-black.png`)
  - favicons
  - area icons from the Balluff icon library (`assets/icons/`)

## Brand

The page follows `design.md` / `tokens.css` in ai-marketing2:

- **Type:** Roboto Flex only, with hierarchy carried on the `wght`, `opsz` and `wdth` axes.
- **Color:** achromatic surface. Balluff Red is reserved for the primary button, selection, focus and links. Errors and success use the UI-state palette, never Balluff Red.
- **Layout:** square corners, a left-aligned 1/3 + 2/3 section layout, and the wordmark top-left (web convention).
- **Footer:** quiet, with the claim lockup.

**No generated imagery.** Families without a real photo show a text tile with the product code, or the area's Balluff icon if there's no code. To add a photo, drop `photos/<key>.jpg` in place and add `img:"photos/<key>.jpg"` to that family in the `PRODUCTS` array in `index.html`.

## Editing the lists

All picker data is at the top of the `<script>` block in `index.html`:

- `AREAS`: the 10 product areas (balluff.com taxonomy) and their fallback icon
- `PRODUCTS`: product families. Each has `key`, `area`, `code`, `name`, `blurb` and an optional `img`. Don't rename existing `key` values; email filters and saved drafts rely on them.
- `COMPETITORS`: each competitor is tagged with the `areas` it competes in
- `MARKETS`, `PRICE_RANGES`, `CUSTOMER_RANGES`, `VOLUME_RANGES`, `TIMELINE`

## How submission works

The form posts to [FormSubmit](https://formsubmit.co/) (`https://formsubmit.co/ajax/austin.sirkin@balluff.com`), which emails the submission directly. There's no backend of our own.

FormSubmit requires a one-time confirmation. The *first* submission ever sent to this address triggers an activation email from FormSubmit, and someone has to click it before delivery starts. After that, every submission is delivered automatically.

The email subject is `Portfolio Request <ref> — <product area> — <product>`. The body includes a **Product area** field so requests can be routed to the right product manager.

There's no separate dashboard or log; each submission is one email. To keep them organized, set up a filter in your email client for subjects starting with `Portfolio Request`, or one per product area.

## Updating

The page is hosted on GitHub Pages, served from `main` at the repo root. Edit `index.html` (and `photos/` as needed), commit, and push to `main`. Pages redeploys within a minute or two.
