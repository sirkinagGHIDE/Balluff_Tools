# ROI Calculator

Sales tool that compares the cost of a customer's current system with a proposed solution and shows when the proposed solution pays for itself. Built from `INTCAI_ROI_Calculator_rev1.xlsx` (Summary + Calculations sheets).

**Live page:** https://sirkinagghide.github.io/Balluff_Tools/roi-calculator/

## What it does

1. **Project:** customer, project, prepared by, date, and names for the two solutions (shown on the PDF; blank names show as "Current system" / "Proposed solution"). Assumptions: target payback (the spreadsheet's "Max ROI (Years)"; blank skips the target check), analysis period (3, 5, 7 or 10 years, default 5) and a default cost reduction (blank counts as 0%; the spreadsheet used 80%, `=C*0.2`).
2. **Upfront costs (one time):** hardware, software, labor, training for each solution. Fields start empty with ghost text; empty counts as $0.
3. **Annual operating costs:** downtime, operations labor, maintenance / PMs, energy / utilities, scrap / rework / quality, MRO, licenses, expedites, changeover, fines / penalties / liabilities, training, lost production. Each row takes a current $/yr and either a reduction % or a proposed $/yr; editing one updates the other.
4. **Results:** "Scale to project" multiplies everything entered above (upfront and operating, entered for one station / machine / line / site / unit) by the number of units in the project. The tables show per-unit totals plus a project-total row; KPIs, charts and the PDF use project totals. Payback is unchanged by scaling. Then: net investment, annual savings, payback, N-year net benefit and ROI, a target check, and three charts: payback timeline, cumulative cost of ownership (each year's cumulative cost labelled for both solutions), and operating cost by category.
5. **Frequency of occurrence calculator:** the timer button on each operating row opens it in a dialog. Annual cost = cost per occurrence × occurrences × periods per year. The optional build-up computes cost per occurrence as duration × (workers × labor rate × overtime factor [none, 1.5× or 2×] + downtime cost per hour) + parts. It opens automatically for operations labor, maintenance, changeover and training. Entries are kept per row, so reopening a row's calculator shows what was entered. Apply the result to the current or proposed column; the working is listed on the PDF under "Basis for estimates".
6. **Export PDF:** downloads a Letter summary. Page 1: KPIs, verdict, payback and cost-of-ownership charts. Then the cost comparison table, category chart and basis for estimates, which flow onto extra pages as needed (table header and section headings repeat; page numbers count the real total).

Inputs are saved in the browser (localStorage). **Reset** clears them.

## Formulas

| Result | Formula | Spreadsheet cell |
|---|---|---|
| Net investment | proposed upfront total − current upfront total | Summary!C23 (spreadsheet uses proposed only; identical when current upfront is $0) |
| Annual savings | Σ (current − proposed) operating cost | Summary!C24 |
| Payback (years) | net investment ÷ annual savings | Summary!C25 |
| Net position at year t | annual savings × t − net investment | Calculations!B3:G3 |
| N-year ROI | net position at year N ÷ net investment | — |
| Annual occurrences | occurrences × periods per year | Summary!C30 / Calculations!A7:H13 |

Periods per year: second, minute and hour use operating hours (hours per day × operating days); day uses operating days only, so hours per day has no effect on a per-day frequency; week, month and year use the calendar. The default 24 h × 7 days matches the spreadsheet exactly (8,760 h, 365 days). Week = 365 / 7, month = 12, year = 1.

## Files

- `index.html` is the whole tool: static HTML/CSS/JS, no build step.
- Chart.js 4.4.1 renders the charts. jsPDF 2.5.1 and html2canvas 1.4.1 load from cdnjs only when you export a PDF.
- `assets/` holds brand assets copied unmodified from [MultiMind-Studio/ai-marketing2](https://github.com/MultiMind-Studio/ai-marketing2): wordmark (SVG for the page, PNG for the PDF), claim lockup, favicons, and two icons from the Balluff icon library (`timer`, `simple-download`).

## Brand

Follows `design.md` / `tokens.css` in ai-marketing2:

- **Type:** Roboto Flex only; headings use heavier `wght` and narrower `wdth`.
- **Color:** achromatic surface. Balluff Red only on the Export PDF button, focus states, section-nav arrows and the payback marker. Charts use the data-viz palette: steel blue (solid line) = proposed, silver (dashed line) = current, so the two read apart by hue, lightness and line style. Target and warning states use the UI-state palette.
- **Layout:** square corners, left-aligned 1/4 + 3/4 sections, wordmark top-left on the page and top-right on the PDF (print convention), quiet footer with the claim lockup.
- **Voice:** numbers carry the claims; no superlatives.
