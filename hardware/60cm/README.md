# 60 cm wordclock templates

Generated from the archived 30 cm design in `hardware/_archive_30cm/`.

Run `uv run 60cm` from this folder to regenerate every SVG. It uses only the Python standard library.

## Files

| File | Material | Notes |
|---|---|---|
| `faceplate_clear_600.svg` | clear cast acrylic | Front sheet. Includes corner LED holes and two registration holes. |
| `faceplate_EN_stencil_600.svg` | black acrylic | Cut the red paths out. Letters read correctly from the front. |
| `frame_cut1_600.svg` | 3 mm MDF | LED board support, with a bottom cavity for the controller. |
| `frame_cut2_lightwells_600.svg` | 6 mm MDF | 110 wells: one per letter, scaled from the original hole. |
| `frame_spacers_600.svg` | 6 mm MDF | One frame; cut as many layers as needed. |
| `frame_back_600.svg` | back panel | Hatch and screw holes. |
| `overlay_600.svg` | preview only | All six layers stacked; legend lists them front to back. |
| `overlay_stencil_font_600.svg` | preview only | Same stack, but letters drawn with `STENCIL.TTF` (C:\Windows\Fonts) to compare bridges. Not a cut file. |

All cut lines are red (`#ff0000`), fill none, 0.5 mm stroke. The sheets are 600 × 600 mm.

Registration holes at (15, 300) and (585, 300) line the two face sheets up, outside the spacer inner cut line. Corner LED holes are 12 mm across.
