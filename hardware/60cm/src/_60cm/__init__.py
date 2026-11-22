"""Generate the 60 cm wordclock templates from the archived 30 cm design."""

from __future__ import annotations

import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
SVG_NS = "{http://www.w3.org/2000/svg}"
OUT = REPO / "hardware" / "60cm"
ARCHIVE = REPO / "hardware" / "_archive_30cm"

CUT = "fill:none;stroke:#ff0000;stroke-width:0.5"


def num(value: float) -> str:
    return f"{value:.4f}".rstrip("0").rstrip(".")


def rect(x: float, y: float, w: float, h: float) -> str:
    return (
        f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" '
        f'height="{num(h)}" style="{CUT}"/>'
    )


def circle(cx: float, cy: float, r: float) -> str:
    return f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(r)}" style="{CUT}"/>'


def svg(comment: str, lines: list[str]) -> str:
    body = "\n".join(lines)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" width="600mm" '
        'height="600mm" viewBox="0 0 600 600">\n'
        f"<!-- {comment} -->\n{body}\n"
        "</svg>\n"
    )


def backup() -> None:
    for folder in ("faceplate", "frame", "electronics"):
        (ARCHIVE / folder).mkdir(parents=True, exist_ok=True)
    for src in (REPO / "hardware" / "faceplate").glob("*.svg"):
        shutil.copy2(src, ARCHIVE / "faceplate" / src.name)
    for src in (REPO / "hardware" / "frame").glob("*.svg"):
        shutil.copy2(src, ARCHIVE / "frame" / src.name)
    shutil.copy2(
        REPO / "hardware" / "electronics" / "wordclock.fzz",
        ARCHIVE / "electronics" / "wordclock.fzz",
    )


def face_files() -> int:
    source = REPO / "hardware" / "faceplate" / "glass_template_EN_mirrored.svg"
    root = ET.parse(source).getroot()
    letters = [
        p
        for p in root.iter(f"{SVG_NS}path")
        if "style" not in p.attrib and "fill" not in p.attrib
    ]

    scale = 2.0 * 25.4 / 96.0
    a = 1.3325375 * scale
    d = 1.3326584 * scale

    common = [
        rect(0, 0, 600, 600),
        circle(40.06, 40.05, 4),
        circle(559.94, 40.05, 4),
        circle(40.06, 559.95, 4),
        circle(559.94, 559.95, 4),
        circle(30, 300, 2),
        circle(570, 300, 2),
    ]
    (OUT / "faceplate_clear_600.svg").write_text(
        svg("Clear front sheet: cut from 600 x 600 mm cast acrylic.", common),
        encoding="utf-8",
    )

    stencil = common + [
        f'<g transform="matrix({num(a)},0,0,{num(d)},0,0)">'
    ]
    stencil += [
        f'<path d="{p.attrib["d"]}" style="{CUT}"/>' for p in letters
    ]
    stencil.append("</g>")
    (OUT / "faceplate_EN_stencil_600.svg").write_text(
        svg(
            "Black stencil: cut these red paths out of a 600 x 600 mm sheet. "
            "Letters read correctly from the front.",
            stencil,
        ),
        encoding="utf-8",
    )
    return len(letters)


def frame_files() -> None:
    # Cut1: board support and controller cavity.
    (OUT / "frame_cut1_600.svg").write_text(
        svg(
            "Cut from 3 mm MDF. The LED board is glued to this layer.",
            [
                rect(0, 0, 600, 600),
                rect(220, 500, 160, 100),
                circle(30, 300, 2),
                circle(570, 300, 2),
            ],
        ),
        encoding="utf-8",
    )

    # Cut2: two stacked wells per letter.
    corner_holes = [
        circle(40.06, 40.05, 4),
        circle(559.94, 40.05, 4),
        circle(40.06, 559.95, 4),
        circle(559.94, 559.95, 4),
        circle(30, 300, 2),
        circle(570, 300, 2),
    ]
    wells = [rect(0, 0, 600, 600), *corner_holes]
    pitch_x, pitch_y = 33.2, 37.2714
    top_inset = (pitch_y - (13.8 * 2 + 4)) / 2
    for row in range(10):
        for col in range(11):
            x = 120.172 + col * pitch_x
            y = 118.441 + row * pitch_y
            wells.append(rect(x, y + top_inset, 27.6, 13.8))
            wells.append(rect(x, y + top_inset + 17.8, 27.6, 13.8))
    (OUT / "frame_cut2_lightwells_600.svg").write_text(
        svg(
            "Cut from 6 mm MDF. Two wells per letter light the top and bottom halves.",
            wells,
        ),
        encoding="utf-8",
    )

    # Spacers: one frame, cut as many layers as needed.
    (OUT / "frame_spacers_600.svg").write_text(
        svg(
            "Cut from 6 mm MDF. Repeat for each spacer layer.",
            [
                rect(0, 0, 600, 600),
                rect(30, 30, 540, 540),
                rect(250, 570, 100, 30),
                circle(30, 300, 2),
                circle(570, 300, 2),
            ],
        ),
        encoding="utf-8",
    )

    # Back panel with hatch and screw holes.
    (OUT / "frame_back_600.svg").write_text(
        svg(
            "Cut from the 600 x 600 mm back panel.",
            [
                rect(0, 0, 600, 600),
                rect(50, 50, 500, 500),
                circle(25, 25, 3),
                circle(575, 25, 3),
                circle(25, 575, 3),
                circle(575, 575, 3),
                circle(30, 300, 2),
                circle(570, 300, 2),
            ],
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    backup()
    count = face_files()
    frame_files()
    print(f"Archived 30 cm templates in {ARCHIVE.relative_to(REPO)}")
    print(f"Generated {count} letter cut paths and 6 SVG files in {OUT.relative_to(REPO)}")
    for path in sorted(OUT.glob("*.svg")):
        print(f"  {path.name}: {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
