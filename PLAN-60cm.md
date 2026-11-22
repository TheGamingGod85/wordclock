# 60 cm Wordclock — Plan

Status: planning only. No code or templates have been changed yet.

## Goal

Make a 60 cm × 60 cm version of the wordclock. English only.

## Decisions already made

- Keep the **same 110 English letters** and the same word layout as the current clock.
- Make the letters about **twice as big** as today.
- Put **two LEDs in each letter**: one lighting the top half, one lighting the bottom half.
- Use a **flat board (PCB) with solder pads**, like the Nodo kit, instead of long LED strips.
- Keep the current way of telling time: words in 5-minute steps, plus 4 corner dots for the leftover minutes.
  For example, 4:39 still shows "IT IS TWENTY-FIVE TO FIVE" + 4 dots.

## What we are not doing

We are not adding more letters or more words.

With more letters we could say "IT IS FOUR THIRTY-NINE" exactly, but:

- in the same 60 cm frame the letters would be small again,
- we would need 440 LEDs instead of 220, with a much bigger power supply,
- every word position in the code would have to be rewritten and rechecked.

Big letters and a small code change are more important here.

## Numbers

| | Current clock | Planned clock |
|---|---|---|
| Panel | 30 × 30 cm | 60 × 60 cm |
| Letter grid | 11 across × 10 down | same |
| LEDs for letters | 110 (one per letter) | 220 (two per letter) |
| Corner minute dots | 4 | 4 |
| Total LEDs | 114 | 224 |
| Step between letters | about 17 mm | about 33 mm |
| Hole for one letter | about 14 mm | about 28 mm |
| Lit area | about 18 × 17 cm | about 36 × 33 cm |
| Power supply | 5 V / 6 A | 5 V / about 15 A |

## Work list

### 1. Face and frame

- Scale the English faceplate SVG to 600 × 600 mm. Ignore the other languages.
- Scale the frame SVGs: back panel, LED support, light wells and spacers.
- Make the light wells deeper or add dividers, so light from one letter does not leak into the next.
- New glass panel and picture frame: 60 × 60 cm.
- Cutting needs a workshop with a large bed, or the frame must be split into panels that are glued together. The glass must be etched as one piece.

### 2. LED board

- One flat board holding 220 LEDs in 10 rows of 11, plus the 4 corner LEDs.
- Two pads per letter, close together vertically, so both halves of a letter light evenly.
- Serpentine data wiring as today; power fed in from several points on the board.
- The board sits inside the frame where the LED strips are today.
- Testing: build one sample letter with 2 LEDs first and check that the letter looks evenly lit. Do this before ordering the full board.

### 3. Firmware (small change)

The words stay exactly where they are. Only the "one letter = two LEDs" rule is new.

- `software/wordclock/src/src/ClockFace.h` and `ClockFace.cpp`: count 224 LEDs and light both LEDs of a letter together.
- `software/wordclock/src/src/Display.cpp`: scrolling text and painting must also light both LEDs of a cell.
- `software/wordclock/src/src/Iot.cpp`: the painting API message grows from 110 colours to 220.
- `software/wordclock/src/paint.html`: can stay at 11 × 10 letters; the code handles the pairs.
- Nodo-specific LED mapping is not used: this is our own board, like the original ESP32 build.

### 4. Power

- Replace the 6 A supply with about 15 A (224 LEDs at full white can draw about 13 A).
- Add several power entry points on the board instead of one feed at the end.

### 5. Checks before calling it done

- One sample letter lights evenly.
- Every English time phrase still lights the correct letters.
- Corner dots still show 1–4 leftover minutes.
- Painting and scrolling text still work.
- Full-white test runs without the power supply or board heating up.

## Still to decide later

- One big PCB (~36 × 33 cm) or ten smaller boards, one per row. One board is closer to the Nodo idea; smaller boards are cheaper and easier to replace.
- Which workshop can cut the frame and etch the glass.
- Final letter size on the faceplate, after seeing the sample letter.
- Exact board size and connector positions, once the frame design is fixed.
