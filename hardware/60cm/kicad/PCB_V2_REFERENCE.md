# 60 cm Word Clock — PCB v2 Reference / Assistant Memory

**Created:** 2026-11-24  
**Branch:** `plan/60cm-pcb-v2`  
**Source of truth:** `hardware/60cm/kicad/word-clock-pcb-design.md` plus user clarifications in chat.  
**Purpose:** My own working reference for the revised/final PCB design. If this conflicts with the user's design doc or a later chat message, ask the user; do not guess.

## 0. Do not touch / current build state

- Do **not** modify `hardware/60cm/kicad/word_clock_row/`.
- That project is **v1** and is obsolete for power topology. The user has deleted it; do not restore it.
- The old `power_rail_v2` project was also deleted by the user on 2026-11-25. Do not recreate it until asked.
- Current build order: **main 22-LED row PCB first**, then corner PCB, then power distribution, then controller PCB.

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
| Power rail | 1 | 50 × 320 mm | Fused star distribution; see `POWER_RAIL_BUILD_GUIDE.md` |
| Controller | 1 | 190 × 90 mm PCB | ESP32 + DS3231 + 74AHCT125; fits 200 × 100 mm cavity |

Total LEDs: **224**.  
Current active board: **LED row** — see `ROW_PCB_BUILD_GUIDE.md`.

## 3. Power architecture

```
5 V / 20 A PSU
  -> 15 A blade fuse (main)
  -> POWER RAIL (50 x 320 mm)
       -> Output 1:     1 A mini blade fuse -> corner 1 -> 2 -> 3 -> 4 (top, terminal up)
       -> Output 2..11: 2 A mini blade fuse -> row 1..10 (grouped middle)
       -> Output 12:    1 A mini blade fuse -> controller board (bottom)
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
- Corner boards: 4-pin in / 4-pin out using the same 3.50 mm 4Ucon footprint as row `J1`; see `CORNER_PCB_BUILD_GUIDE.md`.
- Controller data output: 2-pin = `DOUT, GND`; match row/corner input series.
- No XT60 on row boards: four conductors are needed and row current is only ~1.3 A.

### 5.2 Rail outputs and controller power input

- **2-pin 3.50 mm screw terminals**, same footprint as row `J2`: `TerminalBlock_4Ucon:TerminalBlock_4Ucon_1x02_P3.50mm_Horizontal`.
- 10 row outputs are spaced to fit inside the 320 mm rail; they do **not** need to match the 37.2714 mm row pitch.
- Controller power input uses a 2-pin 3.50 mm screw terminal from rail output 12.

### 5.3 Main input

- Main input uses the same 4-pin footprint as row `J1`: `TerminalBlock_4Ucon:TerminalBlock_4Ucon_1x04_P3.50mm_Horizontal`.
- Pins 1/2 are both `+5V_IN`; pins 3/4 are both `GND`. Use two separate PSU wires per rail because one 3.50 mm pole is only ~8 A.
- User decision 2026-11-24: no XT60. On 2026-11-25 the user said XT60 is acceptable if height allows; keep the 4Ucon footprint and decide on XT60 only if the future rail layout needs it.
- See `POWER_RAIL_BUILD_GUIDE.md` for the full rail build.

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

- Full connector pinout, BOM, one-board coordinates, wiring, DRC and export steps: **see `CORNER_PCB_BUILD_GUIDE.md`**.
- One PCB design is used at all four corners; rotate the finished board 0° / 90° / 270° / 180° as listed in the guide. Do not mirror or flip it.
- Mechanical envelope is already set: **30 × 30 mm grown inward** from the old 20 × 20 position.
- Top-left envelope: `x=30.06…60.06`, `y=30.05…60.05`.
- Top-right envelope: `x=539.94…569.94`, `y=30.05…60.05`.
- Bottom-left envelope: `x=30.06…60.06`, `y=539.95…569.95`.
- Bottom-right envelope: `x=539.94…569.94`, `y=539.95…569.95`.
- Two 4-pin 3.5 mm terminals are ~14 mm each and fit on opposite edges.
- 1 × WS2812B + 1 × 100 nF.
- Power and data both chain through each board.
- 100 nF only; 470 µF skipped because the four LEDs draw about 0.25 A worst case.
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
- 12 fused outputs in physical order:
  - 1 × 1 A mini blade for corner chain, first at the top (`J12`, terminal rotation 0°, wire up)
  - 10 × 2 A mini blade for rows, grouped in the middle (`J2`…`J11`)
  - 1 × 1 A mini blade for controller, last at the bottom (`J13`)
- Silkscreen each terminal (5V, GND, board number) and fuse rating.

### 6.4 Controller PCB — 190 × 90 mm

- Full parts list, netlist, ESP32 footprint rule, coordinates, keepout, DRC and export steps: **see `CONTROLLER_PCB_BUILD_GUIDE.md`**.
- User decision 2026-11-26 replaces the earlier protoboard decision: the controller is now a fabricated PCB.
- Board outline **190 × 90 mm**, placed at `x=205…395`, `y=505…595` inside the 200 × 100 mm cavity.
- 30-pin ESP32 DevKit (CH340C, USB-C): use generic `Conn_02x15_Odd_Even` symbol with the pad map in `CONTROLLER_PCB_BUILD_GUIDE.md`, and a custom footprint; measure row spacing and print 1:1 before ordering.
- DS3231 module: use generic `Conn_01x04`/`Conn_01x06` symbol plus matching pin-header footprint; wire from the actual module silkscreen.
- Feed 5 V to ESP32 **VIN** through a 1N5819 diode. Never feed 5 V to `3V3` or any GPIO.
- USB is for programming only.
- RTC: **DS3231 module** on ESP32 3.3 V; module has its own I²C pull-ups.
- SMD where practical: 74AHCT125 in SOIC-14, 1N5819 in SOD-123, 330 Ω / 10 kΩ resistors in 0805, 100 nF in 0805, 100 µF as SMD electrolytic. ESP32, DS3231 module, screw terminals and LDR stay THT/modules.
- Level shifter: 74AHCT125 powered from 5 V **before** the diode. ESP32 3.3 V logic into it; WS2812B needs ~3.5 V high on a 5 V supply.
- Data: ESP32 `D18` → U2 → 330 Ω → J2 → row 1 DIN. I²C: `D21`/`D22`.
- Ambient light sensor restored from the original 30 cm design: LDR1 from ESP32 `3V3` to `D33` (ADC1), with a 10 kΩ pulldown to GND. Firmware default `LDR_PIN` is already 33; sensitivity setting handles auto-dim.
- Antenna keepout on both layers at local `(80,80)`–`(110,90)` unless the antenna overhangs the board edge.
- Power input: 2-pin 3.50 mm 4Ucon screw terminal from rail output 12.
- Data output: 2-pin 3.50 mm 4Ucon screw terminal `DATA_OUT, GND` to row 1.
- Decoupling: 100 nF at U2 pins 14/7, 100 nF + 100 µF after the diode near ESP32 VIN.
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
- Row PCB and power rail are routed and exported; corner PCB is next; controller PCB is last.
- Controller is a fabricated 190 × 90 mm PCB. Order one locally, or 5 if using JLCPCB.
- JLCPCB minimum 5 pcs per design.
- Row board is SMT-friendly: all parts are SMD except the two screw terminals. Hand assembly or low-cost SMT assembly both work.
- Indian per-cm² shops may be cheaper for the single rail board.
- 10 row boards ≈ 1,184 cm² total.
- Dropping rows to 1 oz removes most of the large surcharge from the earlier 2 oz idea.

## 9. Open items / decisions still needed

1. ESP32 symbol/footprint workaround is resolved: generic 2×15 connector symbol + custom footprint with pad map; row spacing must still be measured and 1:1 test-fitted; see `CONTROLLER_PCB_BUILD_GUIDE.md`.
2. DS3231 module footprint/header layout — module family confirmed; match the actual header when the module arrives.
3. Dry-fit the 4-pin 4Ucon/DORABO input terminal; its two poles per rail must share the ~13 A feed.
4. Resolved for rail: XFCN `XF-508P-B-B` (LCSC `C19727305`) on stock `Fuse:Fuseholder_Blade_Mini_Keystone_3568`; dry-fit once.
5. Resolved for rail: same 15 A-rated holder for `F1`; buy 15 A / 2 A / 1 A mini blade fuses separately.
6. Rail copper weight: design at 1 oz, upgrade to 2 oz only if quote justifies it.
7. Resolved for rows: SMD 470 µF / 10 V / 105 °C, 8 × 10.5 mm (`Capacitor_SMD:CP_Elec_8x10.5`), e.g. Panasonic FK `EEE-FK1A471P`. Resolved for corners: 100 nF only, no 470 µF.
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
| Corner PCB | `CORNER_PCB_BUILD_GUIDE.md` | Created 2026-11-25 |
| Power distribution / rail | `POWER_RAIL_BUILD_GUIDE.md` | Created 2026-11-25 |
| Controller PCB | `CONTROLLER_PCB_BUILD_GUIDE.md` | Created 2026-11-26 |

`ROW_PCB_BUILD_GUIDE.md` contains the Mermaid wiring diagrams, cable labels, connector pinout, all component references with X/Y coordinates, and the KiCad schematic/PCB/assembly steps for one row board. Treat LED centres, M3 holes, and terminal pin order as fixed; capacitor and connector positions may move only to fit the exact purchased footprint.
