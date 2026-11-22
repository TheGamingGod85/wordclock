"""Generate the 60 cm wordclock templates from the archived 30 cm design."""

from __future__ import annotations

import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

REPO = Path(__file__).resolve().parents[4]
SVG_NS = "{http://www.w3.org/2000/svg}"
OUT = REPO / "hardware" / "60cm"
ARCHIVE = REPO / "hardware" / "_archive_30cm"
ALLERTA = OUT / "fonts" / "AllertaStencil-Regular.ttf"

CUT = "fill:none;stroke:#ff0000;stroke-width:0.5"
REG_LEFT = 15.0
REG_RIGHT = 585.0
CORNER_R = 6.0
WELL = 27.6


def num(value: float) -> str:
    return f"{value:.4f}".rstrip("0").rstrip(".")


def rect(x: float, y: float, w: float, h: float) -> str:
    return (
        f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" '
        f'height="{num(h)}" style="{CUT}"/>'
    )


def circle(cx: float, cy: float, r: float) -> str:
    return f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(r)}" style="{CUT}"/>'


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
    (OUT / "faceplate_clear_600.svg").write_text(
        svg("Clear front sheet: cut from 600 x 600 mm cast acrylic.", common),
        encoding="utf-8",
    )

    matrix = f'<g transform="matrix({num(a)},0,0,{num(d)},0,0)">'

    # Keep the original outlines as a backup cut file.
    original = common + [matrix]
    original += [f'<path d="{p.attrib["d"]}" style="{CUT}"/>' for p in letters]
    original.append("</g>")
    (OUT / "faceplate_EN_stencil_original_600.svg").write_text(
        svg("Backup: original stencil outlines from the 30 cm design.", original),
        encoding="utf-8",
    )

    # Production stencil uses Allerta Stencil: its bridges stop letter counters falling out.
    production = common + [matrix]
    production += stencil_font_letter_paths(ALLERTA, style=f'style="{CUT}"')
    production.append("</g>")
    (OUT / "faceplate_EN_stencil_600.svg").write_text(
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
    (OUT / "frame_cut1_600.svg").write_text(
        svg(
            "Cut from 3 mm MDF. The LED board is glued to this layer.",
            [
                rect(0, 0, 600, 600),
                rect(220, 500, 160, 100),
                circle(REG_LEFT, 300, 2),
                circle(REG_RIGHT, 300, 2),
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
    (OUT / "frame_cut2_lightwells_600.svg").write_text(
        svg(
            "Cut from 6 mm MDF. One well per letter, scaled from the 30 cm design.",
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
                circle(REG_LEFT, 300, 2),
                circle(REG_RIGHT, 300, 2),
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
                circle(REG_LEFT, 300, 2),
                circle(REG_RIGHT, 300, 2),
            ],
        ),
        encoding="utf-8",
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
            advance += font["hmtx"][name][0] * scale
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
    cut1 = [shape_rect(0, 0, 600, 600), shape_rect(220, 500, 160, 100)] + reg

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
    clear += [shape_circle(x, y, CORNER_R) for x, y in corners]
    clear += reg

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
    (OUT / name).write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    backup()
    count = face_files()
    frame_files()
    overlay_file("overlay_600.svg", stencil_font_letter_paths(ALLERTA))
    overlay_file("overlay_original_stencil_600.svg")
    overlay_file("overlay_stencil_font_600.svg", stencil_font_letter_paths(Path("C:/Windows/Fonts/STENCIL.TTF")))
    font_dir = OUT / "fonts"
    for font_file in sorted(font_dir.glob("*.ttf")):
        if font_file == ALLERTA:
            continue  # overlay_600.svg already shows the chosen font
        name = f"overlay_{font_file.stem}_600.svg"
        overlay_file(name, stencil_font_letter_paths(font_file))
        print(f"  font preview: {name}")
    print(f"Archived 30 cm templates in {ARCHIVE.relative_to(REPO)}")
    print(f"Generated {count} letter cut paths and {len(list(OUT.glob('*.svg')))} SVG files in {OUT.relative_to(REPO)}")
    for path in sorted(OUT.glob("*.svg")):
        print(f"  {path.name}: {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
