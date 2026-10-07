# Portfolio Request survey

Internal survey where sales reps flag product gaps and portfolio requests for review. It covers the full Balluff portfolio: 9 product areas based on balluff.com (Sensors, RFID, Machine Vision & Optical ID, Industrial Communication, Connectivity, Control & Machine Lights, Power Supplies, Accessories, and Systems Solutions & Software), 56 product families. Systems Solutions & Software lists the named solutions: CMTK (Condition Monitoring Toolkit), Guided GCS (Changeover Solution) and BET (Balluff Engineering Tool). Sensors can be narrowed further by technology (inductive, photoelectric, capacitive and so on).

Reps filter by product area or search by code, pick the closest family, and describe the technical requirement. They also tag competitors, rank target markets, give pricing and volume expectations, and can attach a file or add links.

- The competitor list shows the top 10 for the product picked; the rest are behind "Show all", and a type-ahead box adds any competitor, listed or not.
- Pricing, customer count and volume each accept a preset range or a custom value.

Submitting emails the Product Marketing Manager for that portfolio. No extra step.

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

All configuration is at the top of the `<script>` block in `index.html`:

- `ROUTING`: who receives each request (see below)
- `AREAS`: the 9 product areas and their fallback icon
- `SENSOR_TECHS`: the sensor technology sub-filter; each sensor family has a matching `tech` key
- `PRODUCTS`: product families. Each has `key`, `area`, `seg`, `code`, `name`, `blurb`, an optional `img`, and (for sensors) `tech`. Don't rename existing `key` values; email filters and saved drafts rely on them.
- `COMPETITOR_SETS`: the competitor list for each `seg` (product segment), most relevant first. Only the first `COMPETITOR_TOP_N` (10) show by default.
  - A product shows its segment's list.
  - "Something new" shows every competitor for the chosen area.
  - With no product picked, the list stays empty until the rep picks one, opens the full list, or types a name.
- `MARKETS`, `PRICE_RANGES`, `CUSTOMER_RANGES`, `VOLUME_RANGES`, `TIMELINE`
- `FILE_TYPES`, `BLOCKED_HINTS`, `ATTACHMENT_MAX_BYTES`, `MAX_LINKS`: attachment and link rules

## Routing to Product Marketing Managers

Every request currently goes to `ROUTING.fallback`. To give a colleague their portfolio, fill in their entry in `index.html`:

```js
var ROUTING = {
  fallback: {role:"Product Marketing Manager", email:"austin.sirkin@balluff.com"},
  byArea:   { rfid: {role:"Product Marketing Manager", email:"first.last@balluff.com"}, ... },
  byProduct:{ btl:  {role:"Product Marketing Manager", email:"first.last@balluff.com"} }
};
```

The most specific match wins: `byProduct`, then `byArea`, then `fallback`. The recipient is used for both the automatic email and the "Email Product Marketing" fallback button.

**Each new address must be activated once in FormSubmit.** The first submission sent to a new address triggers a FormSubmit confirmation email, and that person has to click it before delivery starts. Send one test request per new address before you announce it.

## Attachments and links

Reps can attach **one file up to 3 MB** and add **up to 5 links**.

**Accepted file types:**
- **Documents:** .pdf, .docx, .xlsx, .pptx, .csv, .txt
- **Images:** .jpg, .jpeg, .png
- **CAD:** .step, .stp, .dxf

**Not accepted, with the reason shown to the rep:**
- Macro-enabled Office files (.docm, .xlsm, .pptm)
- Legacy Office formats (.doc, .xls, .ppt), which can carry macros
- Archives (.zip, .rar, .7z), which can't be inspected
- Programs and scripts (.exe, .bat, .ps1, .js, …)
- Web files (.html, .svg), which can contain script
- Uncommon image formats

**How a file is checked:** extension allowlist, then the browser-reported MIME type, then the file's leading "magic" bytes. A renamed `.exe` won't pass as a `.pdf`.

**Links:** only `http://` and `https://` addresses are accepted. `javascript:`, `data:`, `file:` and links with embedded usernames or passwords are rejected. A bare address like `balluff.sharepoint.com/...` gets `https://` added. Links are sent as plain text.

These checks run in the browser. They are a guardrail against honest mistakes and casual misuse, not a virus scan. Anyone can bypass a client-side check, so recipients should still treat attachments with normal caution.

## How submission works

The form posts to [FormSubmit](https://formsubmit.co/) (`https://formsubmit.co/ajax/<recipient>`), which emails the submission directly. There's no backend of our own.

The email subject is `Portfolio Request <ref> — <product area> — <product>`. The body includes a **Product area** field. Markets are listed as `Name (High, P3)`, and custom values are marked `(custom)`.

There's no separate dashboard or log; each submission is one email. To keep them organized, set up a filter in your email client for subjects starting with `Portfolio Request`, or one per product area.

## Updating

The page is hosted on GitHub Pages, served from `main` at the repo root. Edit `index.html` (and `photos/` as needed), commit, and push to `main`. Pages redeploys within a minute or two.
