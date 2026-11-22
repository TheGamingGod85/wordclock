# 60 cm wordclock templates

Generated from the archived 30 cm design in `hardware/_archive_30cm/`.

Run `uv run 60cm` from this folder to regenerate every SVG. It writes into the folders below.

## Folders

| Folder | What is in it |
|---|---|
| `cut/` | The files to send to the cutter. These are the ones you need. |
| `backup/` | The original stencil outlines, kept in case Allerta does not cut well. |
| `preview/` | Layer-stack overlays and the font comparison image. Preview only — never cut these. |
| `fonts/` | The Google Fonts used for the stencil and comparisons (OFL licensed). |

## Files to cut

| File | Material | Notes |
|---|---|---|
| `cut/faceplate_clear_600.svg` | clear cast acrylic | Front sheet. Includes corner LED holes and two registration holes. |
| `cut/faceplate_EN_stencil_600.svg` | black acrylic | **Production cut file.** Allerta Stencil letters; bridges stop counter pieces falling out. |
| `cut/frame_cut1_600.svg` | 3 mm MDF | LED board support, with a bottom cavity for the controller. |
| `cut/frame_cut2_lightwells_600.svg` | 6 mm MDF | 110 wells: one per letter, scaled from the original hole. |
| `cut/frame_spacers_600.svg` | 6 mm MDF | One frame; cut as many layers as needed. |
| `cut/frame_back_600.svg` | back panel | Hatch and screw holes. |

## Backup

| File | Notes |
|---|---|
| `backup/faceplate_EN_stencil_original_600.svg` | The original 30 cm-derived letter outlines, as a cut-ready file. |

## Previews

| File | Notes |
|---|---|
| `preview/overlay_600.svg` | All six layers stacked with the production Allerta letters; legend lists them front to back. |
| `preview/overlay_original_stencil_600.svg` | Same stack with the backup original outlines. |
| `preview/overlay_stencil_font_600.svg` | Same stack, letters from Windows `STENCIL.TTF`. |
| `preview/overlay_BigShouldersStencilDisplay_600.svg` | Same stack, Google Fonts "Big Shoulders Stencil Display". |
| `preview/overlay_StardosStencil-Bold_600.svg` | Same stack, Google Fonts "Stardos Stencil Bold". |
| `preview/overlay_StardosStencil-Regular_600.svg` | Same stack, Google Fonts "Stardos Stencil Regular". |
| `preview/font_compare.png` | Side-by-side sample of all five fonts. |

All cut lines are red (`#ff0000`), fill none, 0.5 mm stroke. The sheets are 600 × 600 mm.

Registration holes at (15, 300) and (585, 300) line the two face sheets up, outside the spacer inner cut line. Corner LED holes are 12 mm across.
