# Word Clock PCB System: Design Document

## 1. Project summary

A word clock built from 224 WS2812B addressable LEDs, driven by an ESP32 with an RTC module, powered from a single 5 V / 20 A supply. The system is split into four kinds of PCB:

| Board | Qty | Size | Purpose |
|---|---|---|---|
| LED board | 10 | 370 × 32 mm | 22 WS2812B each (220 LEDs total) |
| Corner board | 4 | 30 × 30 mm (max) | 1 WS2812B each (4 LEDs total), chained to one another |
| Power rail board | 1 | 50 × 320 mm | Takes the 5 V / 20 A input and distributes it to every other board through individual fused outputs |
| Controller board | 1 | TBD | ESP32, RTC, level shifter, data output |

Total LEDs: 220 + 4 = 224.

## 2. Key design decisions and why

### 2.1 Star power distribution instead of daisy-chaining power

Power is **not** passed from one LED board to the next. Each LED board gets its own feed from the power rail board. Reasons:

- Daisy-chaining 10 boards would push the combined current of every downstream board through the first board's copper and its connectors.
- Boards at the end of a chain see lower voltage, so their LEDs get dimmer and shift colour (WS2812B blue and green fail first as the supply droops).
- A fault in one board would not be isolated, and a single fuse could not protect each board's traces.

With a star layout, every LED board only carries its own load (~1.3 A worst case), and a fault on one branch trips that branch's fuse only.

### 2.2 Standard 1 oz copper for the LED boards

Per LED board: 22 LEDs × ~60 mA (full white) ≈ 1.3 A. On a 32 mm wide board with wide 5 V and GND pours on both layers, 1 oz copper is more than enough. 2 oz is unnecessary here and would add a large surcharge on a 370 mm board.

### 2.3 Power rail board copper weight (open decision)

The rail board carries the full load (~13.4 A worst case: 224 × 60 mA). Options:

- **2 oz copper:** safer for the main input path. Small board, so surcharge is modest.
- **1 oz with a center feed and full pours on both layers:** probably adequate, since the current splits in two directions from the centre.

Decide based on a quote. If ordering from JLCPCB (min 5 pcs), 2 oz on 5 × 160 cm² is wasteful, so a local per-cm² shop at 1-2 pcs is a better fit for this one board.

### 2.4 Firmware brightness cap

Full white on all 224 LEDs is ~13.4 A, which approaches the 20 A supply and the 15 A main fuse. Firmware should cap brightness (about 50-60%), which keeps real draw far below the limits and is rarely noticeable on a word clock.

## 3. Electrical architecture

```
5V/20A PSU
   |
[15 A blade fuse]
   |
POWER RAIL BOARD (50 x 320 mm)
   |-- Output 1..10  --[2 A mini blade fuse]--> LED boards 1..10 (parallel)
   |-- Output 11     --[1 A mini blade fuse]--> Corner board 1 --> 2 --> 3 --> 4 (power chained)
   |-- Output 12     --[1 A mini blade fuse]--> Controller board (ESP32 + RTC)

DATA (single chain):
ESP32 GPIO -> 74AHCT125 (5V) -> 330 ohm -> LED board 1 DIN
LED board 1 DOUT -> LED board 2 DIN -> ... -> LED board 10 DIN/DOUT
DOUT of board 10 -> Corner 1 DIN -> Corner 2 -> Corner 3 -> Corner 4 (last DOUT unconnected)
```

Note: the data order between board 10 and the corner boards is an assumption. Confirm against the physical word-clock layout, and adjust the chain order if the corner LEDs sit elsewhere in the sequence.

## 4. Board-by-board specification

### 4.1 Power rail board (50 × 320 mm)

- **Input:** main 5 V / 20 A, through a chunky connector (screw terminal or XT60, not a barrel jack), fed into the **centre** of the board, not one end. A centre feed halves the worst-case current path.
- **Main fuse:** 15 A blade fuse (ATC/mini blade in a holder) between the PSU and the rail board. Sized at 15 A rather than 20 A because 20 A is the supply limit, not the copper's limit. The pour must be able to carry 15 A.
- **Layer plan:** top layer = 5 V pour, bottom layer = solid GND pour, stitched with vias.
- **Pour width:** roughly 15-20 mm for each rail on both layers (IPC-2221 estimate for ~13 A at ~10 °C rise on 1 oz is about 11 mm per rail; verify with a trace-width calculator).
- **Outputs (12 total):** see section 5 for terminal types. Each output has its own fuse in series on the 5 V line:
  - 10 outputs for the LED boards: 2 A mini blade fuse (ATM/APM) in a PCB-mount holder.
  - 1 output for the corner chain: 1 A.
  - 1 output for the controller: 1 A.
- **Terminal pitch:** place the 10 LED-board outputs at the same pitch as the LED boards (32 mm plus any gap) so feed wires are short and straight.
- **Bulk capacitance:** ~1000 µF electrolytic at the input.
- **Silkscreen:** label every terminal (5V, GND, board number).

Note on fuse choice: blade fuses are used instead of resettable PTCs. A blade fuse blows once and stays open until replaced, so a fault gets noticed and fixed, while a PTC trips, cools and retries and can sit weak on a marginal fault. Holders sit in the 5 V pour path, so keep copper continuous around them, check the holder footprint against the 50 mm board width, silkscreen the rating next to each holder, and keep spare fuses on hand.

### 4.2 LED board (10×, 370 × 32 mm)

- **Components:**
  - 22 × WS2812B
  - 1 × 100 nF decoupling capacitor per LED (as already designed)
  - 1 × 470 µF capacitor (100-470 µF acceptable) at the 5V/GND input terminal
  - Terminals (see section 5)
- **Copper:** standard 1 oz, 2 layers, FR4, 1.6 mm.
- **Layout:** wide 5 V and GND pours on both layers; data line routed as a thin trace LED to LED.
- **Silkscreen:** label 5V, GND, DIN, DOUT on both ends.

### 4.3 Corner board (4×, 30 × 30 mm max)

Space is tight at 30 × 30 mm with a 4-pin terminal on each of two opposite sides. Use compact terminals (3.5 mm pitch screw terminals, JST connectors, or pin headers) and check that two 4-pin parts plus the WS2812B and its 100 nF capacitor fit before finalising the outline.


- **Components:** 1 × WS2812B, 1 × 100 nF decoupling capacitor, 2 terminals (one on each side).
- Power and data both pass through each board to the next.
- 470 µF capacitor is optional; a single one at corner 1's input is enough if the chain is only 4 LEDs (~0.25 A).
- Last board's right-side terminal stays empty.

### 4.4 Controller board

- **ESP32** (dev module or bare module).
  - If using a bare module, include a 5 V to 3.3 V regulator. If using a dev module, its onboard regulator is fine; power it from the 5 V input.
- **RTC module** with its own coin-cell backup.
- **Level shifter:** 74AHCT125 powered from 5 V. WS2812B on a 5 V supply expects a logic-high of about 3.5 V (0.7 × Vdd), and the ESP32 outputs 3.3 V, which can work on short wires but fails randomly on longer runs.
- **Series resistor:** ~330 Ω on the data line, placed close to the output terminal, to suppress ringing.
- **Power input:** 5 V and GND from rail output 12 (1 A fuse).
- **Output terminal:** 2-pin (DOUT, GND) to LED board 1's DIN and second GND pin.
- **Decoupling:** 100 nF near the level shifter and ESP32, plus bulk capacitance on the 5 V input.

## 5. Terminal and wiring scheme

There is only one ground net in the whole system (the rail's GND). The controller GND and the rail GND are the same net, so no separate controller ground terminal is needed.

### LED boards (main 10)

- **Left terminal: 4-pin** = 5V, GND, DIN, GND
  - 5V and GND come from the rail board's fused output for that board.
  - DIN and the second GND come from the previous board's right terminal (or the controller board for board 1).
- **Right terminal: 2-pin** = DOUT, GND
  - Runs to the next board's DIN and second GND pin.
- **All GND pins on a board tie to the same GND pour.**
- The extra GND wire runs alongside the data wire as a short return path. This matters because the boards are 370 mm wide and the data wire runs a long distance. Twist DOUT with GND for noise immunity.

### Corner boards

- **Left terminal: 4-pin** = 5V, GND, DIN, GND
- **Right terminal: 4-pin** = 5V, GND, DOUT, GND
- Power and data chain through each board. Extra GND on corners 2-4 is optional because chained power GND already runs next to the data wire.

### Controller board

- Output: 2-pin (DOUT, GND) to board 1.

## 6. Protection summary

| Location | Protection | Rating |
|---|---|---|
| Main input | Blade fuse | 15 A |
| Each LED board output | Mini blade fuse | 2 A |
| Corner chain output | Mini blade fuse | 1 A |
| Controller output | Mini blade fuse | 1 A |

## 7. Bill of materials summary

| Item | Qty |
|---|---|
| WS2812B | 224 |
| 100 nF capacitor (one per LED) | 224 |
| 470 µF capacitor (LED boards) | 10 |
| 1000 µF capacitor (rail input) | 1 |
| 2 A mini blade fuse (plus spares) | 10 |
| 1 A mini blade fuse (plus spares) | 2 |
| PCB-mount mini blade fuse holder (outputs) | 12 |
| 15 A blade fuse + holder (main input) | 1 |
| 4-pin screw terminal | 10 (LED boards, left) + 8 (corner boards, left and right) |
| 2-pin screw terminal | 10 (LED boards, right) + 1 (controller out) |
| Rail output terminals | 12 |
| ESP32 | 1 |
| RTC module with coin cell | 1 |
| 74AHCT125 | 1 |
| 330 Ω resistor | 1 |

Terminal counts are indicative; confirm against the final schematics.

## 8. Manufacturing and ordering

**Budget:** ₹5-8k, up to ₹10k if PCBA is included.

**Boards to order:**
- 10 LED boards: 370 × 32 mm, 2 layers, FR4, 1 oz.
- 1 power rail board: 50 × 320 mm, 2 layers, 1 oz or 2 oz (see 2.3). Updated from the earlier 50 × 150 mm idea.
- 4 corner boards: 30 × 30 mm max.

**Options and findings:**
- The ₹10-20k local quotes and the JLCPCB total (about $80 plus shipping, plus possible customs duty of roughly 10% BCD + 18% IGST) were driven by the 2 oz copper and the area of the long boards. Dropping the LED boards to 1 oz removes most of that cost.
- Indian per-cm² job shops list prices around ₹0.85/cm² (70 micron) and ₹2.18/cm² (105 micron). These are listings, not quotes, but they are a useful anchor. The 10 LED boards total about 1,184 cm².
- LionCircuits offers 2 oz on its rush service with free India shipping; ask directly for a quote on the long boards.
- JLCPCB minimum is 5 pcs per design.
- PCBA is unlikely to fit in ₹10k with these boards. Plan to hand-assemble, or find a local assembler for the LED boards only.

## 9. Open items

1. Rail board copper weight: 1 oz vs 2 oz (decide after quotes).
2. Data order between LED boards and corner boards (confirm against the clock layout).
3. Whether LED rows alternate direction between boards; this decides which edge DIN and DOUT land on.
4. Controller board size and whether the ESP32 is a dev module or a bare module.
5. Per-LED vs per-pair decoupling (current design uses 100 nF on every LED).

## 10. Design rules to remember

- One ground net everywhere; every GND pin on a board connects to the same ground pour.
- Never daisy-chain power across the 10 main LED boards; each gets its own fused feed.
- Level-shift the ESP32 data line before the first LED.
- Cap brightness in firmware.
- Silkscreen every terminal label on every board.
