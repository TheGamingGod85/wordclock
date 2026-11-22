# 60 cm electronics

`wordclock_60cm.fzz` is the circuit for the 60 cm clock. Open it in Fritzing.
It reuses the original 30 cm wiring, with the LED panel updated for this build
and the unused corner touch pads removed.

## Parts

| Ref | Part | Purpose |
| --- | --- | --- |
| J1 | 5 V power jack | External supply, **5 V / 15 A** recommended |
| C1 | 1000 µF capacitor | Inrush protection across the 5 V rail |
| U2 | ESP32 dev board | WiFi, timekeeping, LED data |
| RTC1 | DS3231 (ZS-042) | Keeps time when offline; CR2032 backup battery |
| LDR + R1 | Photocell + 10 kΩ | Ambient light sensor on ADC1 |
| L1 | 4-channel level shifter | 3.3 V data from ESP32 to 5 V LED chain |
| LED1 | WS2812B panel | All **224 LEDs**: 110 letters × 2 + 4 corner dots |

`LED1` is one Fritzing part standing for the whole daisy chain, exactly as the
original sketch used one LED for its 114-LED strip. The properties on the part
record the real count and layout.

## Connections

| From | To | Signal |
| --- | --- | --- |
| J1 PWR | C1 +, U2 VIN, L1 HV, LED1 VCC | 5 V rail |
| J1 GND | C1 −, U2 GND, L1 GND, LED1 VSS, RTC1 GND | Ground |
| U2 3V3 | RTC1 VCC, L1 LV, LDR pin 1 | 3.3 V rail |
| U2 D21 | RTC1 SDA | I²C data |
| U2 D22 | RTC1 SCL | I²C clock |
| U2 D32 | L1 LV4 | LED data out of ESP32 |
| L1 HV4 | LED1 DIN | 5 V LED data |
| LDR pin 0 | R1 pin 0 | Light sensor divider |
| R1 pin 1 | U2 D33 | ADC1 light reading |

The four old capacitive touch pads are gone. GPIO 12, 13, 14 and 27 are free.

## Power and wiring notes

- Worst case for 224 WS2812B at full white is about 13.4 A, so use a 5 V supply
  rated for at least 15 A. Normal clock colours use far less.
- Feed 5 V and GND into the flat LED PCB at **several points** (one per row of
  22 LEDs). Only the data line needs to be a single chain from row to row.
- `C1` sits at the supply entry, not at the far end of the LED panel.
- The data order is row by row, matching `ClockFace.cpp` in the firmware.
- Keep the level shifter: the first WS2812B wants a 5 V data pulse, while the
  ESP32 only outputs 3.3 V.

## Previews

`preview/wordclock_60cm_schematic.svg` and the other two SVGs in that folder are
rendered views of the sketch. They are for reading only — open the `.fzz` in
Fritzing to edit it.

## What is not in this sketch

This is the **circuit**, not the flat PCB layout. The 60 cm LED PCB itself
(footprints, row power injection pads and connector positions) is still to be
designed; the cut files for the face and frame are in `../cut/`.
