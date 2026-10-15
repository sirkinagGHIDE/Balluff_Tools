# Diffuse sensor selector

A draw.io flowchart that helps the sales field team pick the right Balluff diffuse photoelectric sensor family (BOS) and learn what each family is for.

Open `bos-diffuse-sensor-selector.drawio` in [draw.io / diagrams.net](https://app.diagrams.net) (File → Open from → Device), or in the draw.io desktop app or VS Code extension. Export to PDF from there to keep the links clickable.

## Pages

Both pages are US Letter portrait (8.5 × 11 in, 850 × 1100 draw.io units).

1. **Select by housing.**
   - Start at the BOS R81K. If it doesn't solve the application, pick the housing that fits the mount: threaded barrel, miniature block, compact block or standard block.
   - Inside each group, a header line on each card names what makes that family the pick. Then choose the light type.
   - Each card shows range, housing material, IP69K where offered, light types and outputs.
2. **Select by application.** Ten common applications map to families, plus an at-a-glance table of all 14 families.

A range-first version of page 1 was drafted for comparison and dropped in favor of housing-first; it's in this folder's git history.

## Families covered

| Family    | Max range | Housing                    | Light            | Outputs | IP69K | Standout             |
|-----------|-----------|----------------------------|------------------|---------|-------|----------------------|
| BOS R81K  | 300 mm    | Block + M18 nose · plastic | Red              | PNP / NPN |       | Flexible mounting (start here) |
| BOS M8    | 60 mm     | M8 barrel · stainless      | Red              | IO-Link + PNP / NPN |       | Smallest barrel      |
| BOS M12   | 400 mm    | M12 barrel · brass         | Red, IR          | PNP / NPN |       | Prox form factor     |
| BOS M18   | 800 mm    | M18 barrel · brass         | Red, IR, Laser   | IO-Link + PNP / NPN |       | Widest barrel range  |
| BOS R030K | 30 mm     | Ultra-compact · plastic    | Red              | PNP / NPN |       | Ultra compact        |
| BOS Q08M  | 60 mm     | Miniature · metal          | Red, Laser       | IO-Link + PNP / NPN |       | Metal miniature      |
| BOS R020K | 150 mm    | Miniature · plastic        | Red              | PNP / NPN |       | Tiny housing         |
| BOS R072K | 1 m       | Compact · plastic          | Red, IR          | PNP / NPN |       | Entry line           |
| BOS R090K | 1 m       | Compact · plastic          | Red, IR, Laser   | PNP / NPN |       | Laser in a compact   |
| BOS 6K    | 1.5 m     | Compact · plastic          | Red, Laser, Blue | IO-Link + PNP / NPN | ●     | Blue light           |
| BOS R254  | 1 m       | Block · plastic            | Red, Laser       | IO-Link + PNP / NPN | ●     | Condition monitoring |
| BOS 21M   | 2 m       | Block · metal              | Red, IR, Laser   | IO-Link + PNP / NPN | ●     | Shiny objects        |
| BOS 64K   | 2 m       | Large block · plastic      | IR               | Relay NO / NC |       | Relay out, AC supply |
| BOS 23K   | 5 m       | Block · plastic            | Red, Laser       | IO-Link + PNP / NPN | ●     | Longest reach        |

- **Range:** each family's maximum; laser and LED versions differ.
- **BOS R090K:** includes the laser versions sold today as BOS 5K. Same form factor and supplier, and they will be replaced by R090K.
- **Background suppression:** most families offer it, so it isn't a selection step.
- **Excluded:** BOS M30, BOS 5K (grouped into R090K), BOS 50K and BOS 26K (legacy).

**Spec sources:**
- Range, light types and outputs come from the balluff.com diffuse series listing (F01319).
- IP69K and standout features come from the PMM brief.
- Housing material comes from each series page.
- Typical applications are a first proposal for PMM review.

**Links:** every product photo and "BOS ###" name (marked ↗) opens that family's series page on balluff.com.

**Contact on the sheet:** Austin Sirkin, Product Marketing Manager – Photoelectrics, 854-293-3773.

## Brand

Same rules as `distance-sensor-selector` and `portfolio-survey`:
- Roboto Flex
- achromatic surfaces with square corners
- Balluff Red for the start path

Light-type markers use color only to mean the light (red, grey for infrared, blue).

## Files

- `bos-diffuse-sensor-selector.drawio`: the diagram. Photos and the wordmark are embedded, so the file stands alone.
- `photos/`: real Balluff product photos (from assets.balluff.com), trimmed, one per family. The BOS 21M photo is the black version.
