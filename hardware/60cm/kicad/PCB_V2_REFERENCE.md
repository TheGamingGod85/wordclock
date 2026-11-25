# 60 cm Word Clock — PCB v2 Reference / Assistant Memory

**Created:** 2026-11-24  
**Branch:** `plan/60cm-pcb-v2`  
**Source of truth:** `hardware/60cm/kicad/word-clock-pcb-design.md` plus user clarifications in chat.  
**Purpose:** My own working reference for the revised/final PCB design. If this conflicts with the user's design doc or a later chat message, ask the user; do not guess.

## 0. Do not touch / current build state

- Do **not** modify `hardware/60cm/kicad/word_clock_row/`.
- That project is **v1** and is obsolete for power topology. The user has deleted it; do not restore it.
- The old `power_rail_v2` project was also deleted by the user on 2026-11-25. Do not recreate it until asked.
- Current build order: **main 22-LED row PCB first**, then corner PCB, then power distribution, then controller protoboard wiring.

## 1. What v2 changes from v1

v1 row board had daisy-chained power through 3-pin JST-XH connectors and provisional 2 oz copper. v2 replaces that:

- **Power is star-distributed** from a dedicated rail board. Power is not passed from row to row.
- **No JST-XH anywhere.** Use screw terminals.
- **Rows are identical**: DIN left, DOUT right. No flipped/mirrored boards.
- **1 oz copper on rows**; 2 oz only optional on the rail after quotes.
- **Bulk capacitors added** at row inputs and rail input.
- **Mini blade fuses** everywhere, not resettable PTCs.

## 2. Board set

| Board | Qty | Size | Purpose |
|---|---:|---|---|
| LED row | 10 | 370 × 32 mm | 22 WS2812B each = 220 LEDs |
| Corner | 4 | 30 × 30 mm max | 1 WS2812B each = 4 LEDs |
| Power rail | 1, deferred | 50 × 320 mm | Fused star distribution; project deleted, restart later |
| Controller | 1 | Protoboard, not fabricated | ESP32 + DS3231 + level shifter on protoboard |

Total LEDs: **224**.  
Current active board: **LED row** — see `ROW_PCB_BUILD_GUIDE.md`.

## 3. Power architecture

```
5 V / 20 A PSU
  -> 15 A blade fuse (main)
  -> POWER RAIL (50 x 320 mm)
       -> Output 1..10: 2 A mini blade fuse -> row 1..10
       -> Output 11:    1 A mini blade fuse -> corner 1 -> 2 -> 3 -> 4
       -> Output 12:    1 A mini blade fuse -> controller board
```

Rules:

- **One GND net everywhere.** Controller GND and rail GND are the same net.
- **Never daisy-chain power across the 10 rows.**
- Each row only carries its own ~1.3 A worst case.
- Corner boards **do** chain power through all four.
- Firmware caps brightness to ~50–60%; full-white 224 LEDs is ~13.4 A.

## 4. Data architecture

```
ESP32 GPIO
  -> 74AHCT125 (powered from 5 V)
  -> 330 ohm series resistor near output
  -> row 1 DIN
  -> row 1 DOUT -> row 2 DIN -> ... -> row 10 DOUT
  -> corner 1 DIN -> corner 2 -> corner 3 -> corner 4
  -> corner 4 DOUT unconnected
```

Important:

- This physical order is an **assumption**, not a confirmed clock-layout decision.
- Firmware will remap LED indices, so physical chain order does not need to match visual clock order.
- **Do not alternate row direction.** All 10 rows are identical: DIN left, DOUT right.
- Between rows, run a twisted `DOUT + GND` wire from row N right end back to row N+1 left end.
- Row right terminal is **data-only**: `DOUT, GND`; it does **not** carry 5 V.

## 5. Connector and footprint policy

### 5.1 Rows, corners, controller data output

- Row boards use **3.50 mm fixed screw terminals**. Exact footprints are in `ROW_PCB_BUILD_GUIDE.md`.
  - Row left: 4-pin `TerminalBlock_4Ucon:TerminalBlock_4Ucon_1x04_P3.50mm_Horizontal` = `5V, GND, DIN, GND`.
  - Row right: 2-pin `TerminalBlock_4Ucon:TerminalBlock_4Ucon_1x02_P3.50mm_Horizontal` = `DOUT, GND`.
  - Reason: the 5.00 mm 4-pin body is ~21 mm long and overlaps the locked left M3 holes; the 3.50 mm body is ~15.7 mm and fits.
- Corner boards: still planned as 4-pin in / 4-pin out; exact part decided in the corner guide.
- Controller data output: 2-pin = `DOUT, GND`; match row/corner input series.
- No XT60 on row boards: four conductors are needed and row current is only ~1.3 A.

### 5.2 Rail outputs and controller power input

- **2-pin 5.08 mm screw terminals**, footprint `TerminalBlock_Generic:Screw_Terminal_01x02`.
- 10 row outputs are spaced to fit inside the 320 mm rail; they do **not** need to match the 37.2714 mm row pitch.
- Controller power input uses 2-pin 5.08 mm from rail output 12.

### 5.3 Main input

- Main input uses the same generic screw terminal footprint as the outputs: `TerminalBlock_Generic:Screw_Terminal_01x02`.
- User decision 2026-11-24: no XT60. On 2026-11-25 the user said XT60 is acceptable if height allows; keep the screw-terminal footprint for now and decide on XT60 only if the future rail layout needs it.
- Current rating / wire gauge still needs a sanity check before fabrication.

### 5.4 Fuses

- Main: **15 A blade fuse** + PCB-mount holder.
- Outputs: **mini blade ATM/APM** in PCB-mount holders.
  - 10 × 2 A for rows
  - 1 × 1 A for corner chain
  - 1 × 1 A for controller
- **Pick a specific PCB-mount mini blade holder** and take its footprint from the datasheet.
- No PTCs. Blade fuses blow open and stay blown so faults are noticed.
- Silkscreen every fuse rating and every terminal label.

### 5.5 Why no JST-XH

- Needs a crimp tool.
- Only ~3 A per pin.
- Screw terminals accept arbitrary wire and need no crimping.

## 6. Board details

### 6.1 LED row board — 10×, 370 × 32 mm

- Exact BOM, references, values and footprints: **see `ROW_PCB_BUILD_GUIDE.md` section 4**.
- 22 × genuine WS2812B-V5 (`LED_SMD:LED_WS2812B_PLCC4_5.0x5.0mm_P3.2mm`).
- 22 × 100 nF X7R 0805, one per LED. Keep per-LED decoupling; per-pair was not adopted.
- 1 × SMD 470 µF / 10 V / 105 °C at the 5 V/GND input (`Capacitor_SMD:CP_Elec_8x10.5`), e.g. Panasonic FK `EEE-FK1A471P`.
- 1 oz copper, 2 layers, FR4, 1.6 mm. **HASL only** — leaded or lead-free, whichever is cheaper. User rejected ENIG on cost.
- Wide 5 V and GND pours on both layers; data as thin trace LED-to-LED.
- Silkscreen 5V, GND, DIN, DOUT on both ends.
- All GND pins tie to the same GND pour.

### 6.2 Corner board — 4×, 30 × 30 mm max

- Mechanical envelope is already set: **30 × 30 mm grown inward** from the old 20 × 20 position.
- Top-left envelope: `x=30.06…60.06`, `y=30.05…60.05`.
- Top-right envelope: `x=539.94…569.94`, `y=30.05…60.05`.
- Bottom-left envelope: `x=30.06…60.06`, `y=539.95…569.95`.
- Bottom-right envelope: `x=539.94…569.94`, `y=539.95…569.95`.
- Two 4-pin 3.5 mm terminals are ~14 mm each and fit on opposite edges.
- 1 × WS2812B + 1 × 100 nF.
- Power and data both chain through each board.
- 470 µF optional; only needed once at corner 1 if desired.
- Last board right terminal stays empty.
- Current diagonal M3 holes, 5 mm inset, clear of the Ø12 corner light-well:
  - Top-left: `(55.06,35.05)`, `(35.06,55.05)`
  - Top-right: `(544.94,35.05)`, `(564.94,55.05)`
  - Bottom-left: `(35.06,544.95)`, `(55.06,564.95)`
  - Bottom-right: `(564.94,544.95)`, `(544.94,564.95)`

### 6.3 Power rail board — 1×, 50 × 320 mm

- Location in 600 mm frame: `x=60…110`, `y=140…460`.
- Mounting holes: `(65,145)`, `(105,145)`, `(65,455)`, `(105,455)`.
- Design for **1 oz first**; 2 oz optional after quotes.
- Top layer: 5 V pour. Bottom layer: solid GND pour. Via stitch them.
- pours ~15–20 mm wide on both layers.
- Centre-fed 5 V input to halve worst-case path.
- 15 A main blade fuse between PSU and rail.
- ~1000 µF electrolytic at input.
- 12 fused outputs:
  - 10 × 2 A mini blade for rows, at 32 mm pitch
  - 1 × 1 A mini blade for corner chain
  - 1 × 1 A mini blade for controller
- Silkscreen each terminal (5V, GND, board number) and fuse rating.

### 6.4 Controller — protoboard, not a fabricated PCB

- User decision 2026-11-25: controller will be built on protoboard. Do **not** design a controller PCB.
- Use a 30-pin ESP32 dev module on female headers; exact module decided when the protoboard is built.
- Use the dev module's onboard regulator. Feed 5 V into its **5V/VIN** pin. Never feed 5 V to 3.3 V.
- USB is for programming only.
- Keep the protoboard inside the frame cavity `x=200…500`, `y=500…600` (200 × 100 mm).
- RTC: **DS3231 module** with coin-cell backup, on its own I2C headers.
- Level shifter: 74AHCT125 powered from 5 V. ESP32 3.3 V logic into it; WS2812B needs ~3.5 V high on a 5 V supply.
- 330 Ω series resistor close to the output terminal.
- Power input: 2-pin 5.08 mm screw terminal from rail output 12.
- Data output: 2-pin 3.5 mm screw terminal `DOUT, GND` to row 1.
- Decoupling: 100 nF near level shifter and ESP32, plus bulk on 5 V input.
- All grounds are one net.

## 7. Mechanical / cut-layer coordination

- Clear faceplate: **solid 600 × 600 acrylic, no holes**.
- Black stencil: carries 4 corner-dot holes and 2 registration holes.
- Light-well layer (`frame_cut2_lightwells_600.svg`): 110 wells + 4 Ø12 corner holes.
- Frame standoff holes total **52**:
  - 40 row holes
  - 8 corner holes (diagonal positions above)
  - 4 power-rail holes
- Row PCB envelope: `x=114.972…484.972`, rows at 37.2714 mm pitch, height 32 mm.
- Power rail already drawn in `preview/overlay_power_rail_600.svg`; no PCB outline belongs in `/cut`.
- LED-strip alternative preview: `preview/overlay_led_strips_600.svg`. It shows two 11-LED strips per row, 12 mm apart, plus the 4 corner LEDs and power rail. PCB plan remains unchanged.

## 8. Manufacturing / ordering notes

- Budget: ₹5–8k, up to ₹10k if PCBA included.
- Current build order: 10 row PCBs first; corner and rail later. Rail project was deleted and must be restarted from scratch when needed.
- Controller is protoboard, not an ordered PCB.
- JLCPCB minimum 5 pcs per design.
- Row board is SMT-friendly: all parts are SMD except the two screw terminals. Hand assembly or low-cost SMT assembly both work.
- Indian per-cm² shops may be cheaper for the single rail board.
- 10 row boards ≈ 1,184 cm² total.
- Dropping rows to 1 oz removes most of the large surcharge from the earlier 2 oz idea.

## 9. Open items / decisions still needed

1. Exact 30-pin ESP32 dev module model/dimensions — decide when the protoboard controller is built.
2. Exact DS3231 module footprint/header layout — module family confirmed, footprint still to pick.
3. Confirm current rating of generic `Screw_Terminal_01x02` for the ~13 A main input; footprint choice is already fixed.
4. Specific PCB-mount mini blade ATM/APM fuse holder part number + datasheet footprint.
5. Specific 15 A blade fuse holder part number + datasheet footprint.
6. Rail copper weight: design at 1 oz, upgrade to 2 oz only if quote justifies it.
7. Resolved for rows: SMD 470 µF / 10 V / 105 °C, 8 × 10.5 mm (`Capacitor_SMD:CP_Elec_8x10.5`), e.g. Panasonic FK `EEE-FK1A471P`. Corner still TBD.
8. Final KiCad project structure — user creates it; do not create or edit old project.

## 10. Hard rules to remember

- One ground net everywhere.
- Never daisy-chain power across the 10 rows.
- Level-shift before the first LED.
- Cap brightness in firmware.
- Silkscreen every terminal and fuse rating.
- Take connector/fuse footprints from real datasheets; do not guess.
- Data order is an assumption; firmware will remap.
- All rows identical; no flipped boards.

## 11. Build guides

These are the standalone step-by-step files. Create them one at a time; do not start the next board until the current one is finished.

| Board | Guide | Status |
|---|---|---|
| Main 22-LED row PCB | `ROW_PCB_BUILD_GUIDE.md` | Created 2026-11-25 |
| Corner PCB | `CORNER_PCB_BUILD_GUIDE.md` | Not created yet |
| Power distribution / rail | `POWER_RAIL_BUILD_GUIDE.md` | Not created yet; old project deleted |
| Controller protoboard | `CONTROLLER_PROTOBOARD_GUIDE.md` | Not created yet |

`ROW_PCB_BUILD_GUIDE.md` contains the Mermaid wiring diagrams, cable labels, connector pinout, all component references with X/Y coordinates, and the KiCad schematic/PCB/assembly steps for one row board. Treat LED centres, M3 holes, and terminal pin order as fixed; capacitor and connector positions may move only to fit the exact purchased footprint.
