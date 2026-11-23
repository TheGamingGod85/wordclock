# 60 cm Mechanical Verification Report (Standoff Mounting)

**Status:** Verification/documentation only — no further design changes made.  
**Branch:** `plan/60cm-clean` (current workspace).  
**Date:** 2026-11-23.  
**Scope:** Standoff mounting holes added to `frame_back_600.svg` and `frame_cut1_600.svg`; 32 mm row PCB height assumption; corner PCB provisional mounting holes.

## 1. Updated SVG files

| File | Status | Mounting holes |
|---|---|---|
| `hardware/60cm/cut/frame_back_600.svg` | Updated | 48 blue circles, `r=1.6 mm` (M3 clearance), includes comment block |
| `hardware/60cm/cut/frame_cut1_600.svg` | Updated | 48 blue circles, `r=1.6 mm` (M3 clearance), includes comment block |
| `hardware/60cm/cut/frame_cut2_lightwells_600.svg` | Not modified for standoffs | 0 standoff holes |
| `hardware/60cm/cut/frame_spacers_600.svg` | Not modified for standoffs | 0 standoff holes |

**Preserved geometry:** Existing red cut geometry in back/cut1 was not removed. The only additions are the comment and 48 blue mounting-hole circles before `</svg>`.

**Alignment check:** Blue mounting-hole sets extracted from back and cut1 are identical (48/48 same coordinates). See Section 3.

## 2. Mounting hole coordinate table

### Coordinate system / units

- **Origin:** SVG origin `(0,0)` at top-left of the 600×600 mm sheet.
- **Units:** millimeters (`mm`). SVG viewBox is `0 0 600 600` on a `600mm × 600mm` canvas.
- **Axes:** +X right, +Y down (SVG convention).
- **Hole size:** `r=1.6 mm` (3.2 mm diameter), M3 clearance. Style: `fill:none;stroke:#0000ff;stroke-width:0.5`.

### Row PCB mounting holes (40)

Canonical CSV: `hardware/60cm/verification/mounting_holes_row_40.csv`  
All-holes CSV: `hardware/60cm/verification/mounting_holes_all_48.csv`

Assumed row PCB envelope: **370.0 × 32.0 mm**, centered on each 11-letter row.  
Board X: `114.9720 .. 484.9720 mm` (same for all rows).  
Hole inset: **4.0 mm** from board edge.

| PCB | Board top Y (mm) | Board bottom Y (mm) | TL (X,Y) | TR (X,Y) | BL (X,Y) | BR (X,Y) |
|---|---:|---:|---|---|---|---|
| ROW_01 | 116.2410 | 148.2410 | (118.9720,120.2410) | (480.9720,120.2410) | (118.9720,144.2410) | (480.9720,144.2410) |
| ROW_02 | 153.5124 | 185.5124 | (118.9720,157.5124) | (480.9720,157.5124) | (118.9720,181.5124) | (480.9720,181.5124) |
| ROW_03 | 190.7838 | 222.7838 | (118.9720,194.7838) | (480.9720,194.7838) | (118.9720,218.7838) | (480.9720,218.7838) |
| ROW_04 | 228.0552 | 260.0552 | (118.9720,232.0552) | (480.9720,232.0552) | (118.9720,256.0552) | (480.9720,256.0552) |
| ROW_05 | 265.3266 | 297.3266 | (118.9720,269.3266) | (480.9720,269.3266) | (118.9720,293.3266) | (480.9720,293.3266) |
| ROW_06 | 302.5980 | 334.5980 | (118.9720,306.5980) | (480.9720,306.5980) | (118.9720,330.5980) | (480.9720,330.5980) |
| ROW_07 | 339.8694 | 371.8694 | (118.9720,343.8694) | (480.9720,343.8694) | (118.9720,367.8694) | (480.9720,367.8694) |
| ROW_08 | 377.1408 | 409.1408 | (118.9720,381.1408) | (480.9720,381.1408) | (118.9720,405.1408) | (480.9720,405.1408) |
| ROW_09 | 414.4122 | 446.4122 | (118.9720,418.4122) | (480.9720,418.4122) | (118.9720,442.4122) | (480.9720,442.4122) |
| ROW_10 | 451.6836 | 483.6836 | (118.9720,455.6836) | (480.9720,455.6836) | (118.9720,479.6836) | (480.9720,479.6836) |

### Corner PCB mounting holes (8, PROVISIONAL)

Canonical CSV: `hardware/60cm/verification/mounting_holes_corner_8.csv`

Assumed corner PCB: **20.0 × 20.0 mm** centered on corner LED, two M3 clearance holes at **±7.0 mm** in X from LED center, same Y as LED center. **Provisional — confirm against final corner PCB design before fabrication.**

| PCB | LED | LED (X,Y) mm | Hole H1 (X,Y) mm | Hole H2 (X,Y) mm | Notes |
|---|---|---:|---:|---:|---|
| CORNER_TL_LED221 | LED221 | (40.0600,40.0500) | (33.0600,40.0500) | (47.0600,40.0500) | Provisional |
| CORNER_TR_LED222 | LED222 | (559.9400,40.0500) | (552.9400,40.0500) | (566.9400,40.0500) | Provisional |
| CORNER_BL_LED223 | LED223 | (40.0600,559.9500) | (33.0600,559.9500) | (47.0600,559.9500) | Provisional |
| CORNER_BR_LED224 | LED224 | (559.9400,559.9500) | (552.9400,559.9500) | (566.9400,559.9500) | Provisional |

## 3. Row PCB mounting verification

### 3.1 Hole fit within 370 × 32 mm PCB

**Result: PASS (for assumed envelope).** All 40 row holes are inside their respective 370×32 mm board envelopes.

| Check | Value | Result |
|---|---|---|
| Board width | 370.0 mm | Assumed |
| Board height | 32.0 mm | Assumed (replaces 50 mm to avoid overlap) |
| Hole inset from board edge | 4.0 mm | Assumed |
| Hole X from board left/right edge | 4.0 mm / 366.0 mm | Inside |
| Hole Y from board top/bottom edge | 4.0 mm / 28.0 mm | Inside |
| Hole radius | 1.6 mm (M3 clearance) | Edge clearance = 2.4 mm to board edge; see 3.2 |

### 3.2 4 mm inset mechanical safety

**Result: CONDITIONALLY ACCEPTABLE, needs PCB-edge/copper keepout confirmation.**

- 4.0 mm inset to hole center leaves **2.4 mm** from hole edge to PCB edge (for 1.6 mm radius hole). This is tight but common for M3 mounting if board edge/copper keepout is respected.
- Recommended check in KiCad: NPTH/pad/hole copper keepout and board-edge clearance rules; keep copper/traces >= manufacturer+mechanical margin from hole edge and board edge.
- With 32 mm board height, holes are 24 mm apart vertically (4 mm from top + 24 mm + 4 mm from bottom). This gives room between holes, but connector/LED keepouts must be checked in the actual PCB layout.

### 3.3 Clearance from LED footprints, connectors, copper, PCB edges

**Result: PARTIALLY VERIFIED.**

| Item | Verification | Result |
|---|---|---|
| Hole-to-hole spacing | Min center distance 13.2714 mm (ROW_04_BL–ROW_05_TL) | PASS, no overlap |
| Hole-to-matrix-LED center | Min 10.8167 mm (ROW_01_TL to LED001 center) | PASS for footprint body; WS2812B 5×5 mm => 2.5 mm half, hole r 1.6 mm => ~6.72 mm edge clearance |
| Hole-to-board edge | 2.4 mm edge clearance (4.0 mm center inset - 1.6 mm radius) | CONDITIONAL; verify with fab/mechanical rules |
| Hole-to-connectors | No PCB layout available in current workspace (`hardware/60cm/kicad` removed) | **UNRESOLVED** |
| Hole-to-copper/pours/traces | No PCB layout available | **UNRESOLVED** |
| Hole-to-mounting hardware head/washer | Depends on selected standoff/screw/washer | **UNRESOLVED** |

### 3.4 Alignment between back panel and cut1

**Result: PASS.**

- `frame_back_600.svg` blue mounting holes: 48
- `frame_cut1_600.svg` blue mounting holes: 48
- Coordinate sets identical: **Yes** (exact same cx/cy/r/style values extracted).

## 4. Corner PCB details

### 4.1 Corner LED coordinates

| LED | X (mm) | Y (mm) | Location |
|---|---:|---:|---|
| LED221 | 40.0600 | 40.0500 | Top-left corner |
| LED222 | 559.9400 | 40.0500 | Top-right corner |
| LED223 | 40.0600 | 559.9500 | Bottom-left corner |
| LED224 | 559.9400 | 559.9500 | Bottom-right corner |

Coordinates match the 60 cm corner holes used in face/cut2 geometry (`40.06,40.05`, `559.94,40.05`, `40.06,559.95`, `559.94,559.95`).

### 4.2 Proposed 20 × 20 mm board dimensions

**Result: PROVISIONAL ASSUMPTION.** A 20×20 mm board centered on the corner LED fits the corner area, but no corner PCB CAD exists in this workspace to confirm connector placement, LED footprint, or copper clearances.

### 4.3 Two mounting hole coordinates per board

See Section 2 table and `mounting_holes_corner_8.csv`. All 8 corner holes are inside the assumed 20×20 mm envelopes.

### 4.4 Connector and LED clearances

**Result: UNRESOLVED / PROVISIONAL.**

- Hole-to-corner-LED center distance: 7.0 mm. With LED 5×5 mm (2.5 mm half) and hole r 1.6 mm, nominal edge clearance is ~2.9 mm — likely acceptable for footprint body, but must be checked against actual corner PCB footprint, pads, silkscreen, and connector.
- Corner PCB has JST-XH 3-pin vertical connectors (`J_IN/J_OUT`) in prior design intent; connector/body/cable clearances cannot be verified without corner PCB layout.
- Corner boards must not interfere with frame edge, screw holes, or face corner LED holes.

## 5. Mechanical stackup

**Result: PARTIALLY KNOWN; hardware selection required.**

| Layer/Item | Value | Status |
|---|---|---|
| Back panel thickness | 600×600 mm panel; thickness **not specified in repo docs** | **UNRESOLVED** (user/material dependent) |
| Cut1 thickness | 3 mm MDF (per `frame_cut1_600.svg` comment) | Known from file |
| Cut2 light wells | 6 mm MDF (per `frame_cut2_lightwells_600.svg` comment) | Known from file |
| Spacers | 6 mm MDF per layer, repeat as needed (per `frame_spacers_600.svg` comment) | Known as design intent; quantity TBD |
| Clear front sheet | Acrylic (per README) | Known as material; thickness TBD |
| Distance between back panel and cut1 | Depends on standoff/body design; if standoffs pass through cut1 and mount to back panel, gap can be 0 or spacer-defined | **UNRESOLVED** |
| Proposed standoff length | **TBD**. Must place row/corner PCB plane behind light wells with clearance for LED height, solder joints, connector bodies, cables, and diffuser stackup. | **UNRESOLVED** |
| Screw lengths | **TBD**. Depends on back panel thickness + cut1 + standoff + PCB + washer/nut/head engagement. | **UNRESOLVED** |
| Washers/nuts | **TBD**. Use insulating washers/sleeves if metal hardware risks shorting. | **UNRESOLVED** |
| Mounting hardware | M3 recommended by hole size; confirm screw head/washer diameter clears PCB components and standoff shoulder | **UNRESOLVED** |

**Recommendation:** Select standoff after final PCB component heights (WS2812B, JST-XH vertical, solder fillets) and full frame stackup are confirmed. Use nylon/insulating standoffs or insulated shoulder washers where copper clearance is uncertain.

## 6. LED-to-light-well alignment

### 6.1 Matrix LED verification (220 LEDs / 110 wells)

**Result: PASS by coordinate formula; PASS against generated 60 cm geometry.**

- 110 wells = 11 columns × 10 rows. Well pitch X = 33.2 mm, pitch Y = 37.2714 mm. Well size = 27.6×27.6 mm. Well origin = (120.172, 118.441).
- 2 LEDs per well, vertical placement: `x = well_left + 7.8`, `y = well_top + 7.8` and `well_top + 19.8`.
- All 220 generated matrix LED coordinates match expected positions exactly within floating-point formatting tolerance.

| Check | Result |
|---|---|
| Total matrix LEDs | 220 |
| Wells covered | 110 (all rows/cols 1..10 × 1..11) |
| LEDs per well | 2 |
| X within well | 7.8 mm from left edge (20.0 mm from right edge) |
| Top LED Y within well | 7.8 mm from top edge |
| Bottom LED Y within well | 19.8 mm from top edge |
| Bottom LED clearance to well bottom | 7.8 mm |
| LED package fit | WS2812B 5×5 mm centered on nominal point fits inside 27.6×27.6 mm well with margin |

CSV: `hardware/60cm/verification/led_coordinates_220_matrix.csv`

### 6.2 Corner LEDs

Corner LEDs (LED221–224) are at the existing 60 cm corner hole centers (40.06,40.05 / 559.94,40.05 / 40.06,559.95 / 559.94,559.95) and are not inside the 11×10 letter matrix wells.

## 7. Collision report

| Check | Status | Details |
|---|---|---|
| Mounting hole overlap (hole-hole) | **PASS** | Min center spacing 13.2714 mm (ROW_04_BL–ROW_05_TL); hole diameter 3.2 mm => 10.07 mm edge clearance |
| Row PCB envelope overlap (32 mm height) | **PASS** | Adjacent 32 mm boards gap 5.2714 mm; 0 overlaps |
| Old 50 mm height overlap | **FAIL (avoided by 32 mm)** | 50 mm would overlap at 37.2714 mm pitch. Not used. |
| Mounting hole to matrix LED footprint | **PASS (nominal)** | Min center distance 10.8167 mm; nominal edge clearance ~6.72 mm with 5×5 LED and r1.6 hole |
| Mounting hole to corner LED footprint | **PASS (nominal, provisional corner PCB)** | 7.0 mm center distance; nominal edge clearance ~2.9 mm |
| Back/cut1 mounting hole alignment | **PASS** | Identical 48-hole sets |
| Holes in lightwell/spacer layers | **PASS** | Removed from `frame_cut2_lightwells_600.svg` and `frame_spacers_600.svg` |
| Connector clearances | **UNRESOLVED** | No row/corner PCB CAD in workspace; verify JST-XH vertical bodies/cables against hole/edge keepouts |
| Copper/pour/trace clearances | **UNRESOLVED** | No PCB CAD; verify in KiCad DRC and mechanical keepout |
| Standoff/washer/screw head clearances | **UNRESOLVED** | Hardware not selected |
| Back panel/cut1 existing cut features vs new holes | **PASS (visual/coordinate check)** | New holes are inside panel area and away from existing red features by inspection; back-panel existing holes are different sizes/positions. No automated CAD interference test run. |
| Corner PCB board overlap with frame/cutouts | **UNRESOLVED** | 20×20 mm assumption not validated against full corner mechanical envelope |

## 8. Unresolved assumptions (explicit)

1. **Corner PCB mechanical design is provisional.** 20×20 mm board, 2 holes at ±7 mm X from LED center, same Y — assumed, not validated by corner PCB CAD.
2. **No PCB layout exists in workspace.** `hardware/60cm/kicad/` was removed; connector/copper/keepout/DRC clearances cannot be fully verified.
3. **Row PCB is assumed 370×32 mm with 4 mm corner inset M3 holes.** Final PCB outline and hole placement must match this assumption before fabrication.
4. **Back panel thickness, standoff length, screw length, washer/nut selection are TBD.**
5. **Cut1 is 3 mm MDF by file comment; back panel thickness/material not specified.**
6. **Standoff/hardware electrical isolation not specified.** Use insulating hardware or verify clearances to copper.
7. **LED coordinates are from 60 cm geometric formula.** They are consistent with the 60 cm generator/constants and current stencil/well geometry; they should be treated as the canonical input for PCB placement, but final PCB CAD must use the same coordinate source.
8. **No physical prototype fit check performed.** SVG/coordinate verification only.

## 9. Files produced for this verification

- `hardware/60cm/verification/REPORT.md` (this report)
- `hardware/60cm/verification/mounting_holes_row_40.csv`
- `hardware/60cm/verification/mounting_holes_corner_8.csv`
- `hardware/60cm/verification/mounting_holes_all_48.csv`
- `hardware/60cm/verification/led_coordinates_220_matrix.csv`
- Updated SVGs (design files): `hardware/60cm/cut/frame_back_600.svg`, `hardware/60cm/cut/frame_cut1_600.svg`
