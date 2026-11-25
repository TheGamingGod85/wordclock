"""Generate the 60 cm wordclock templates from the archived 30 cm design."""

from __future__ import annotations

import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

REPO = Path(__file__).resolve().parents[4]
SVG_NS = "{http://www.w3.org/2000/svg}"
OUT = REPO / "hardware" / "60cm"
ARCHIVE = REPO / "hardware" / "_archive_30cm"
CUT = OUT / "cut"
BACKUP = OUT / "backup"
PREVIEW = OUT / "preview"
FONTS = OUT / "fonts"
ALLERTA = FONTS / "AllertaStencil-Regular.ttf"

CUT_STYLE = "fill:none;stroke:#ff0000;stroke-width:0.5"
HOLE_STYLE = "fill:none;stroke:#0000ff;stroke-width:0.5"
REG_LEFT = 15.0
REG_RIGHT = 585.0
CORNER_R = 6.0
WELL = 27.6
HOLE_R = 1.6
POWER_RAIL_X = 60.0
POWER_RAIL_Y = 140.0
POWER_RAIL_W = 50.0
POWER_RAIL_H = 320.0
POWER_RAIL_HOLE_INSET = 5.0


def num(value: float) -> str:
    return f"{value:.4f}".rstrip("0").rstrip(".")


def rect(x: float, y: float, w: float, h: float) -> str:
    return (
        f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" '
        f'height="{num(h)}" style="{CUT_STYLE}"/>'
    )


def circle(cx: float, cy: float, r: float) -> str:
    return f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(r)}" style="{CUT_STYLE}"/>'


def hole_circle(cx: float, cy: float, r: float) -> str:
    return f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(r)}" style="{HOLE_STYLE}"/>'


def power_rail_holes() -> list[tuple[float, float]]:
    hx1 = POWER_RAIL_X + POWER_RAIL_HOLE_INSET
    hx2 = POWER_RAIL_X + POWER_RAIL_W - POWER_RAIL_HOLE_INSET
    hy1 = POWER_RAIL_Y + POWER_RAIL_HOLE_INSET
    hy2 = POWER_RAIL_Y + POWER_RAIL_H - POWER_RAIL_HOLE_INSET
    return [(hx1, hy1), (hx2, hy1), (hx1, hy2), (hx2, hy2)]


def row_mounting_holes() -> list[tuple[float, float]]:
    holes: list[tuple[float, float]] = []
    for row in range(10):
        top = 116.241 + row * 37.2714
        holes.extend(
            [
                (118.972, top + 4.0),
                (480.972, top + 4.0),
                (118.972, top + 28.0),
                (480.972, top + 28.0),
            ]
        )
    return holes


def corner_mounting_holes() -> list[tuple[float, float]]:
    # 30x30 mm corner boards grown inward, holes 5 mm inset on board diagonals.
    # Diagonal pair is chosen to clear the r=6 corner light-well cutout.
    return [
        (55.06, 35.05),
        (35.06, 55.05),
        (544.94, 35.05),
        (564.94, 55.05),
        (35.06, 544.95),
        (55.06, 564.95),
        (564.94, 544.95),
        (544.94, 564.95),
    ]


def all_mounting_holes() -> list[tuple[float, float]]:
    return row_mounting_holes() + corner_mounting_holes() + power_rail_holes()


def shape_rect(x: float, y: float, w: float, h: float) -> str:
    return (
        f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" '
        f'height="{num(h)}"/>'
    )


def shape_circle(cx: float, cy: float, r: float) -> str:
    return f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(r)}"/>'


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
        circle(40.06, 40.05, CORNER_R),
        circle(559.94, 40.05, CORNER_R),
        circle(40.06, 559.95, CORNER_R),
        circle(559.94, 559.95, CORNER_R),
        circle(REG_LEFT, 300, 2),
        circle(REG_RIGHT, 300, 2),
    ]
    (CUT / "faceplate_clear_600.svg").write_text(
        svg(
            "Clear front sheet: solid 600 x 600 mm cast acrylic, no cutouts.",
            [rect(0, 0, 600, 600)],
        ),
        encoding="utf-8",
    )

    matrix = f'<g transform="matrix({num(a)},0,0,{num(d)},0,0)">'

    # Keep the original outlines as a backup cut file.
    original = common + [matrix]
    original += [f'<path d="{p.attrib["d"]}" style="{CUT_STYLE}"/>' for p in letters]
    original.append("</g>")
    (BACKUP / "faceplate_EN_stencil_original_600.svg").write_text(
        svg("Backup: original stencil outlines from the 30 cm design.", original),
        encoding="utf-8",
    )

    # Production stencil uses Allerta Stencil: its bridges stop letter counters falling out.
    production = common + [matrix]
    production += stencil_font_letter_paths(ALLERTA, style=f'style="{CUT_STYLE}"')
    production.append("</g>")
    (CUT / "faceplate_EN_stencil_600.svg").write_text(
        svg(
            "Black stencil: cut these red paths out of a 600 x 600 mm sheet. "
            "Letters read correctly from the front. Allerta Stencil font.",
            production,
        ),
        encoding="utf-8",
    )
    return len(letters)


def frame_files() -> None:
    # Cut1: board support and controller cavity.
    (CUT / "frame_cut1_600.svg").write_text(
        svg(
            "Cut from 3 mm MDF. The LED board is glued to this layer.",
            [
                rect(0, 0, 600, 600),
                rect(200, 500, 200, 100),
                circle(REG_LEFT, 300, 2),
                circle(REG_RIGHT, 300, 2),
                "<!-- PCB standoff mounting holes: M3 clearance r=1.6mm. Row boards 370x32mm, corner boards 30x30mm, power rail 50x320mm. -->",
                *[hole_circle(x, y, HOLE_R) for x, y in all_mounting_holes()],
            ],
        ),
        encoding="utf-8",
    )

    # Cut2: one well per letter, the 30 cm hole scaled by two.
    corner_holes = [
        circle(40.06, 40.05, CORNER_R),
        circle(559.94, 40.05, CORNER_R),
        circle(40.06, 559.95, CORNER_R),
        circle(559.94, 559.95, CORNER_R),
        circle(REG_LEFT, 300, 2),
        circle(REG_RIGHT, 300, 2),
    ]
    wells = [rect(0, 0, 600, 600), *corner_holes]
    pitch_x, pitch_y = 33.2, 37.2714
    for row in range(10):
        for col in range(11):
            x = 120.172 + col * pitch_x
            y = 118.441 + row * pitch_y
            wells.append(rect(x, y, WELL, WELL))
    (CUT / "frame_cut2_lightwells_600.svg").write_text(
        svg(
            "Cut from 6 mm MDF. One well per letter, scaled from the 30 cm design.",
            wells,
        ),
        encoding="utf-8",
    )

    # Spacers: one frame, cut as many layers as needed.
    (CUT / "frame_spacers_600.svg").write_text(
        svg(
            "Cut from 6 mm MDF. Repeat for each spacer layer.",
            [
                rect(0, 0, 600, 600),
                rect(30, 30, 540, 540),
                rect(250, 570, 100, 30),
                circle(REG_LEFT, 300, 2),
                circle(REG_RIGHT, 300, 2),
            ],
        ),
        encoding="utf-8",
    )

    # Back panel with hatch and screw holes.
    (CUT / "frame_back_600.svg").write_text(
        svg(
            "Cut from the 600 x 600 mm back panel.",
            [
                rect(0, 0, 600, 600),
                rect(50, 50, 500, 500),
                circle(25, 25, 3),
                circle(575, 25, 3),
                circle(25, 575, 3),
                circle(575, 575, 3),
                circle(REG_LEFT, 300, 2),
                circle(REG_RIGHT, 300, 2),
                "<!-- PCB standoff mounting holes: M3 clearance r=1.6mm. Row boards 370x32mm, corner boards 30x30mm, power rail 50x320mm. -->",
                *[hole_circle(x, y, HOLE_R) for x, y in all_mounting_holes()],
            ],
        ),
        encoding="utf-8",
    )


def overlay_power_rail_file(name: str = "overlay_power_rail_600.svg") -> None:
    base = (PREVIEW / "overlay_600.svg").read_text(encoding="utf-8")
    extra = [
        '<g id="pcb_mounting_holes" stroke="#0000ff" fill="none" stroke-width="0.6">',
        *[shape_circle(x, y, HOLE_R) for x, y in all_mounting_holes()],
        "</g>",
        '<g id="row_pcb_outlines" stroke="#d62728" fill="none" stroke-width="0.8">',
        *[
            shape_rect(114.972, 116.241 + row * 37.2714, 370.0, 32.0)
            for row in range(10)
        ],
        "</g>",
        '<g id="corner_pcb_outlines" stroke="#8c564b" fill="none" stroke-width="0.8">',
        *[
            shape_rect(x, y, 30.0, 30.0)
            for x, y in (
                (30.06, 30.05),
                (539.94, 30.05),
                (30.06, 539.95),
                (539.94, 539.95),
            )
        ],
        "</g>",
        '<g id="power_rail_pcb" stroke="#e377c2" fill="none" stroke-width="0.8">',
        shape_rect(POWER_RAIL_X, POWER_RAIL_Y, POWER_RAIL_W, POWER_RAIL_H),
        *[shape_circle(x, y, HOLE_R) for x, y in power_rail_holes()],
        "</g>",
        '<line x1="620" y1="300" x2="650" y2="300" stroke="#0000ff" stroke-width="3"/>',
        '<text x="660" y="304" font-family="sans-serif" font-size="12" fill="#111">PCB mounting holes</text>',
        '<line x1="620" y1="324" x2="650" y2="324" stroke="#d62728" stroke-width="3"/>',
        '<text x="660" y="328" font-family="sans-serif" font-size="12" fill="#111">Row PCB outlines</text>',
        '<line x1="620" y1="348" x2="650" y2="348" stroke="#8c564b" stroke-width="3"/>',
        '<text x="660" y="352" font-family="sans-serif" font-size="12" fill="#111">Corner PCB outlines</text>',
        '<line x1="620" y1="372" x2="650" y2="372" stroke="#e377c2" stroke-width="3"/>',
        '<text x="660" y="376" font-family="sans-serif" font-size="12" fill="#111">Power rail PCB</text>',
    ]
    (PREVIEW / name).write_text(
        base.replace("</svg>", "\n".join(extra) + "\n</svg>"), encoding="utf-8"
    )


def stencil_font_letter_paths(
    font_path: Path, style: str = 'fill="#9467bd" stroke="none"'
) -> list[str]:
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    glyphs = font.getGlyphSet()
    units = font["head"].unitsPerEm
    source = REPO / "hardware" / "faceplate" / "glass-template-EN-font.svg"
    root = ET.parse(source).getroot()
    paths: list[str] = []
    scale = 36 / units
    for text in root.iter(f"{SVG_NS}text"):
        x, y = map(float, re.search(r"translate\(([\d.]+),([\d.]+)\)", text.attrib["transform"]).groups())
        advance = 0.0
        for char in "".join(text.itertext()):
            name = cmap.get(ord(char))
            if name is None:
                continue
            pen = SVGPathPen(glyphs)
            # Bake placement into the outline so a 0.5 mm cut stroke stays 0.5 mm.
            transform = Transform(scale, 0, 0, -scale, x + advance, y)
            glyphs[name].draw(TransformPen(pen, transform))
            paths.append(f'<path d="{pen.getCommands()}" {style}/>')
            # Advance by ink width, not the font's full em, so O' stays inside its well.
            bounds = BoundsPen(glyphs)
            glyphs[name].draw(bounds)
            advance += (bounds.bounds[2] - bounds.bounds[0]) * scale + 2
    return paths


def overlay_file(name: str = "overlay_600.svg", letter_paths: list[str] | None = None) -> None:
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

    corners = [
        (40.06, 40.05),
        (559.94, 40.05),
        (40.06, 559.95),
        (559.94, 559.95),
    ]
    reg = [shape_circle(REG_LEFT, 300, 2), shape_circle(REG_RIGHT, 300, 2)]

    def group(name: str, color: str, lines: list[str]) -> str:
        return (
            f'<g id="{name}" stroke="{color}" fill="none" stroke-width="0.6">\n'
            + "\n".join(lines)
            + "\n</g>"
        )

    back = [shape_rect(0, 0, 600, 600), shape_rect(50, 50, 500, 500)]
    back += [shape_circle(x, y, 3) for x, y in ((25, 25), (575, 25), (25, 575), (575, 575))]
    back += reg

    spacers = [shape_rect(0, 0, 600, 600), shape_rect(30, 30, 540, 540), shape_rect(250, 570, 100, 30)] + reg
    cut1 = [shape_rect(0, 0, 600, 600), shape_rect(200, 500, 200, 100)] + reg

    wells = [shape_rect(0, 0, 600, 600)]
    wells += [shape_circle(x, y, CORNER_R) for x, y in corners]
    wells += reg
    pitch_x, pitch_y = 33.2, 37.2714
    for row in range(10):
        for col in range(11):
            x = 120.172 + col * pitch_x
            y = 118.441 + row * pitch_y
            wells.append(shape_rect(x, y, WELL, WELL))

    stencil = [shape_rect(0, 0, 600, 600)]
    stencil += [shape_circle(x, y, CORNER_R) for x, y in corners]
    stencil += reg
    if letter_paths is None:
        letter_paths = [f'<path d="{p.attrib["d"]}"/>' for p in letters]
    stencil.append(f'<g transform="matrix({num(a)},0,0,{num(d)},0,0)">')
    stencil += letter_paths
    stencil.append("</g>")

    clear = [shape_rect(0, 0, 600, 600)]

    groups = [
        group("back_panel", "#777777", back),
        group("spacers", "#e69500", spacers),
        group("cut1_board_support", "#1f77b4", cut1),
        group("cut2_light_wells", "#2ca02c", wells),
        group("black_stencil", "#9467bd", stencil),
        group("clear_front", "#17becf", clear),
    ]

    legend = [
        '<text x="620" y="35" font-family="sans-serif" font-size="16" fill="#111">60 cm wordclock - layer overlay</text>',
        '<text x="620" y="60" font-family="sans-serif" font-size="12" fill="#111">Front to back:</text>',
    ]
    labels = [
        ("Clear acrylic front", "#17becf"),
        ("Black stencil", "#9467bd"),
        ("Cut2 light wells", "#2ca02c"),
        ("Cut1 LED support", "#1f77b4"),
        ("Spacers", "#e69500"),
        ("Back panel", "#777777"),
    ]
    for index, (label, color) in enumerate(labels):
        y = 85 + index * 24
        legend.append(
            f'<line x1="620" y1="{y}" x2="650" y2="{y}" stroke="{color}" stroke-width="3"/>'
        )
        legend.append(
            f'<text x="660" y="{y + 4}" font-family="sans-serif" font-size="12" fill="#111">{label}</text>'
        )
    legend.append(
        '<text x="620" y="270" font-family="sans-serif" font-size="11" fill="#111">'
        f'Registration holes: ({num(REG_LEFT)}, 300) and ({num(REG_RIGHT)}, 300)'
        "</text>"
    )

    content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" width="900mm" height="600mm" '
        'viewBox="0 0 900 600">\n'
        "<!-- Layers drawn back-to-front; legend lists them front-to-back. -->\n"
        + "\n".join(groups + legend)
        + "\n</svg>\n"
    )
    (PREVIEW / name).write_text(content, encoding="utf-8")


def main() -> None:
    for folder in (CUT, BACKUP, PREVIEW, FONTS):
        folder.mkdir(parents=True, exist_ok=True)
    backup()
    count = face_files()
    frame_files()
    overlay_file("overlay_600.svg", stencil_font_letter_paths(ALLERTA))
    overlay_power_rail_file()
    overlay_file("overlay_original_stencil_600.svg")
    overlay_file("overlay_stencil_font_600.svg", stencil_font_letter_paths(Path("C:/Windows/Fonts/STENCIL.TTF")))
    for font_file in sorted(FONTS.glob("*.ttf")):
        if font_file == ALLERTA:
            continue  # overlay_600.svg already shows the chosen font
        name = f"overlay_{font_file.stem}_600.svg"
        overlay_file(name, stencil_font_letter_paths(font_file))
        print(f"  font preview: {name}")
    print(f"Archived 30 cm templates in {ARCHIVE.relative_to(REPO)}")
    print(f"Generated {count} letter cut paths in {OUT.relative_to(REPO)}")
    for folder in (CUT, BACKUP, PREVIEW):
        for path in sorted(folder.glob("*.svg")):
            print(f"  {path.relative_to(OUT)}: {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
