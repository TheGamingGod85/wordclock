# 60 cm wordclock cut files

All SVGs are **1:1 in millimetres** on a **600 × 600 mm** sheet. Red (`#ff0000`) lines are the main cut paths; blue (`#0000ff`) circles on the frame files are M3 clearance holes and must be cut/drilled too. The 0.5 mm stroke is a drawing style, not kerf — no kerf compensation is included.

| File | Qty | Material | What to cut |
|---|---:|---|---|
| `faceplate_clear_600.svg` | 1 | Clear cast acrylic, 600 × 600 mm (thickness not fixed in the design) | Outer 600 × 600 square; four Ø12 mm corner LED holes; two Ø4 registration holes at (15, 300) and (585, 300). |
| `faceplate_EN_stencil_600.svg` | 1 | Black acrylic, 600 × 600 mm (thin sheet; thickness not fixed) | Outer square, same four Ø12 and two Ø4 holes, plus the 111 Allerta Stencil letter paths. Do **not** mirror — letters read correctly from the front. |
| `frame_cut2_lightwells_600.svg` | 1 | 6 mm MDF, 600 × 600 mm | Outer square; 110 light wells, each 27.6 × 27.6 mm, on a 33.2 × 37.2714 mm grid; four Ø12 corner holes; two Ø4 registration holes. |
| `frame_cut1_600.svg` | 1 | 3 mm MDF, 600 × 600 mm | Outer square; 200 × 100 mm controller cavity/notch at the bottom centre; two Ø4 registration holes; 48 Ø3.2 mm M3 standoff holes. Verify standoff positions against the final PCB. |
| `frame_spacers_600.svg` | 2–3 | 6 mm MDF per layer, 600 × 600 mm | Outer square; 540 × 540 mm inner opening (30 mm border); 100 × 30 mm cable notch in the bottom rail; two Ø4 registration holes. Cut one piece per spacer layer. |
| `frame_back_600.svg` | 1 | Back-panel board, 600 × 600 mm (material/thickness not fixed in the design) | Outer square; 500 × 500 mm hatch inset 50 mm from each edge; four Ø6 screw holes in the corners; two Ø4 registration holes; 48 Ø3.2 mm M3 standoff holes. Keep the 500 × 500 piece as the removable hatch. |

Not in `cut/`: the **diffuser** between the LEDs and stencil. Use a 600 × 600 mm sheet of paper or translucent film.
