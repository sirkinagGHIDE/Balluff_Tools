# Distance sensor selector

A one-file draw.io flowchart that helps the sales field team pick the right Balluff photoelectric distance sensor family (BOD) in under a minute, and learn what each family is for.

Open `bod-distance-sensor-selector.drawio` in [draw.io / diagrams.net](https://app.diagrams.net) (File → Open from → Device), or in the draw.io desktop app or VS Code extension. Export to PDF or PNG from there.

## Pages

Both pages are US Letter portrait (8.5 × 11 in, 850 × 1100 draw.io units) and print 1:1 from File → Export as → PDF.


1. **Select by distance.** Flows top to bottom. Start at the BOD 6K, the default. Check three things: target within 1.5 m, 0.1 mm resolution is enough, no display needed. If all three hold, quote the 6K. If not, branch on what's missing (more range, a display, or finer resolution) to one of the four other families. Each family appears exactly once. On the finer-resolution branch, the 21M vs 24K split is one question: hard target (dark, transparent, shiny) → 21M; otherwise → 24K. Arrows into the 24K name the version: long-range (from the display branch) or high-res (from the finer-resolution branch).
2. **Select by application.** For reps who don't have the numbers yet. Seven common applications map to families, plus an at-a-glance comparison matrix.

## Families covered

| Family  | Range     | Resolution | Housing        | Standout                          |
|---------|-----------|------------|----------------|-----------------------------------|
| BOD 6K  | ≤ 1500 mm | 0.1 mm     | Plastic, IP69K | Default; compact, washdown        |
| BOD 21M | ≤ 200 mm  | ≤ 10 µm    | Metal, IP67    | Hard targets: dark, transparent, shiny |
| BOD 24K | ≤ 650 mm† | ≤ 10 µm†   | Plastic, IP67  | Digital display                   |
| BOD 23K | ≤ 5000 mm | ≤ 5 mm     | Plastic, IP69K | Long reach in washdown            |
| BOD 37M | ≤ 20000 mm| ≤ 1 mm     | Metal, IP67    | Long range, display, RS485 (no IO-Link) |

† BOD 24K long-range and high-resolution are separate versions; one part does not do both.

BOD 26K and BOD 66M are excluded as legacy. Older long-range 21M and 6K variants are intentionally not highlighted.

**Links:** every product photo and "BOD ###" name (marked ↗) opens that family's series page on balluff.com. That covers the page 1 cards, the page 2 product boxes, and the page 2 table headers. Links work in the draw.io viewer (Ctrl/Cmd-click while editing) and in an exported PDF.

| Family  | Series page |
|---------|-------------|
| BOD 6K  | https://www.balluff.com/en-us/products/BOD002R?pm=BOD6K&pf=F01328 |
| BOD 21M | https://www.balluff.com/en-us/products/BOD000M?pm=BOD21M&pf=F01328 |
| BOD 23K | https://www.balluff.com/en-us/products/BOD0020?pm=BOD23K&pf=F01328 |
| BOD 24K | https://www.balluff.com/en-us/products/BOD002N?pm=BOD24K&pf=F01328 |
| BOD 37M | https://www.balluff.com/en-us/products/BOD001W?pm=BOD37M&pf=F01328 |

**Contact on the sheet:** Austin Sirkin, Product Marketing Manager – Photoelectrics, 854-293-3773.

**Spec sources:** range, resolution, IP rating and display come from the PMM draft. Interfaces come from the balluff.com series listing. Typical applications are a first proposal for PMM review.

## Brand

The selector follows the same brand rules as `portfolio-survey` (from `design.md` / `tokens.css` in ai-marketing2):

- Roboto Flex
- achromatic surfaces with square corners
- Balluff Red only for the start path and best-in-class callouts

The wordmark is embedded from `portfolio-survey/assets/`.

## Files

- `bod-distance-sensor-selector.drawio`: the diagram. Photos and the wordmark are embedded, so the file stands alone.
- `photos/`: real Balluff product photos (from assets.balluff.com), trimmed, one per family. The BOD 21M photo is the black version.
