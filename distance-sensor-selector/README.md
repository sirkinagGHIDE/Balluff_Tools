# Distance sensor selector

A one-file draw.io flowchart that helps the sales field team pick the right Balluff photoelectric distance sensor family (BOD) in under a minute, and learn what each family is for.

Open `bod-distance-sensor-selector.drawio` in [draw.io / diagrams.net](https://app.diagrams.net) (File → Open from → Device), or in the draw.io desktop app or VS Code extension. Export to PDF or PNG from there.

## Pages

1. **Select by distance.** Start at the BOD 6K, the default. Check three things: target within 1.6 m, 0.1 mm resolution is enough, no display needed. If all three hold, quote the 6K. If not, branch on what's missing (more range, a display, or finer resolution) to one of the four other families. Each family appears exactly once. On the finer-resolution branch, the 21M vs 24K split is one question: hard target (dark, transparent, shiny) → 21M; otherwise → 24K with its display.
2. **Select by application.** For reps who don't have the numbers yet. Seven common applications map to families, plus an at-a-glance comparison matrix.

## Families covered

| Family  | Range     | Resolution | Housing        | Standout                          |
|---------|-----------|------------|----------------|-----------------------------------|
| BOD 6K  | ≤ 1600 mm | 0.1 mm     | Plastic, IP69K | Default; compact, washdown        |
| BOD 21M | ≤ 200 mm  | ≤ 10 µm    | Metal, IP67    | Hard targets: dark, transparent, shiny |
| BOD 24K | ≤ 650 mm† | ≤ 10 µm†   | Plastic, IP67  | Digital display                   |
| BOD 23K | ≤ 5000 mm | ≤ 5 mm     | Plastic, IP69K | Long reach in washdown            |
| BOD 37M | ≤ 20000 mm| ≤ 1 mm     | Metal, IP67    | 20 m, display, RS485              |

† BOD 24K long-range and high-resolution are separate versions; one part does not do both.

BOD 26K and BOD 66M are excluded as legacy. Older long-range 21M and 6K variants are intentionally not highlighted.

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
