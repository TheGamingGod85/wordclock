# 60 cm electronics

`wordclock_60cm.fzz` is the complete 60 cm circuit sketch. Open it in Fritzing.
It contains the **224 individual WS2812B LEDs** placed at the real 60 cm
well/corner coordinates, plus a **proto-board controller** that fits the
200 × 100 mm frame cavity.

## Boards

| Board | Part | Purpose |
| --- | --- | --- |
| PCB_LED_PANEL | Two-layer rectangular PCB, 380 × 390 mm | Carries all 224 WS2812B LEDs at the 60 cm well/corner positions |
| PROTO_CTRL | Basic perfboard/proto board | Controller assembly in the 200 × 100 mm frame cavity |

## Controller parts (on proto board)

| Ref | Part | Purpose |
| --- | --- | --- |
| J1_BARREL_5V | 5.5 × 2.1 mm barrel jack | 5 V input from a **5 V / 10 A+** supply (15 A recommended for full white margin) |
| U2_BUCK_5V | RioRand LM2596 buck module | Steps/ regulates input to a stable 5.00 V rail before connecting LEDs |
| C1_1000uF | 1000 µF electrolytic capacitor | Across 5 V/GND near power entry; observe polarity |
| U1_ESP32 | ESP32 DevKitC on female headers | Plugs into two female header rows on the proto board; removable for programming/replacement |
| R1_470 | 470 Ω resistor | In series on LED data line, close to the JST/data output |
| J2_JST_DATA | 3-pin JST connector | 5 V / GND / DATA output to the LED panel (use JST-XH/PH/SM as you prefer, but keep pinout consistent) |
| RTC1_DS3231 | DS3231 RTC breakout | Optional: keeps time when offline |
| LVL1 | 4-channel level shifter | Optional but recommended: 3.3 V ESP32 data/SCL/SDA to 5 V-safe levels |
| LDR1 + R2_10K | LDR + 10 kΩ divider | Optional: ambient light on ADC |

## LED panel

- **224 LEDs total**: 110 letters × 2 LEDs each + 4 corner minute dots.
- **Chain order**: row-serpentine by letter wells (matching 60 cm layout), corners last.
- **Placement**: each LED instance is positioned at its real 60 cm coordinate in PCB view.
- **Power**: connect 5 V and GND to every LED/power pad as required by the physical PCB; the sketch shows sampled power wires for readability, but the real panel must have solid 5 V/GND distribution and power injection at row ends/bands.
- **Data**: single chain `DOUT -> DIN` through the panel; only data is daisy-chained.

## Connections

| From | To | Signal |
| --- | --- | --- |
| J1_BARREL_5V | U2_BUCK_5V IN+/IN− | Supply input |
| U2_BUCK_5V OUT+ | C1 +, U1_ESP32 5V/VIN, J2_JST_DATA 5V, LED panel 5V | 5 V rail |
| U2_BUCK_5V OUT− | C1 −, U1_ESP32 GND, J2_JST_DATA GND, LED panel GND | Common ground |
| U1_ESP32 GPIO27 (data) | R1_470 -> J2_JST_DATA DATA | LED data |
| J2_JST_DATA DATA | LED1 DIN ... LED224 DOUT chain | WS2812B data chain |
| U1_ESP32 3V3/SDA/SCL | LVL1/RTC1 | Optional I²C |
| LDR1/R2_10K | U1_ESP32 ADC | Optional light sensor |

> **Check in Fritzing GUI before soldering.** The sketch passes `fz check`, but
> ESP32 pin labels/connectors vary by Fritzing part. Confirm GPIO27/5V/GND/3V3/SDA/SCL/ADC
> on the placed ESP32 part before wiring the proto board.

## Power notes

- Set the buck to **5.00 V** with no LEDs connected, then connect LEDs.
- Worst case 224 WS2812B full white is ~13.4 A; normal clock colours are much lower.
- Keep one common ground: ESP32, buck, capacitor, JST, and LED panel.
- Power the ESP32 from the regulated 5 V rail through its 5V/VIN pin, or use USB
  only for programming/debug. Do not feed 5 V into 3.3 V.
- `C1` goes at the power entry, close to the buck/proto output.

## Previews

`preview/` contains rendered breadboard/schematic/PCB SVGs. They are read-only
references; edit the `.fzz` in Fritzing.

## What is not fabrication-ready

- The LED panel is **electrically/logically represented** in Fritzing with 224
  placed WS2812B parts and a rectangular PCB outline. For a real flat LED PCB,
  you still need PCB CAD (KiCad/EasyEDA/etc.) for footprints, copper pours/traces,
  row power injection pads, JST landing pads, and mounting holes.
- The proto-board controller is intended for hand soldering on perfboard, not as
  a fabricated controller PCB.
- Corner capacitive touch pads are intentionally omitted (legacy, not used by
  firmware).
