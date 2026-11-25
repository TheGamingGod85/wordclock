# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "ezdxf>=1.4",
#   "svgpathtools>=1.7",
# ]
# ///
"""Generate one DXF per SVG in this folder.

Run: uv run make_dxfs.py
Writes: DXFs/<svg name>.dxf
"""
from __future__ import annotations

import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import ezdxf
import ezdxf.bbox
from svgpathtools import parse_path

HERE = Path(__file__).resolve().parent
OUT = HERE / "DXFs"
SVG_NS = "{http://www.w3.org/2000/svg}"
RECT = f"{SVG_NS}rect"
CIRCLE = f"{SVG_NS}circle"
PATH = f"{SVG_NS}path"
SHAPES = {RECT, CIRCLE, PATH}
IDENTITY = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
ACI = {"CUT_RED": 1, "M3_BLUE": 5}


def numbers(value: str) -> tuple[float, ...]:
    return tuple(float(item) for item in re.split(r"[\s,]+", value.strip()) if item)


def matrix(values: tuple[float, ...]) -> tuple[float, ...]:
    if len(values) != 6:
        raise ValueError(f"matrix() needs 6 values, got {values}")
    return values


def translate(values: tuple[float, ...]) -> tuple[float, ...]:
    if len(values) not in (1, 2):
        raise ValueError(f"translate() needs 1 or 2 values, got {values}")
    return (1.0, 0.0, 0.0, 1.0, values[0], values[1] if len(values) == 2 else 0.0)


def scale(values: tuple[float, ...]) -> tuple[float, ...]:
    if len(values) not in (1, 2):
        raise ValueError(f"scale() needs 1 or 2 values, got {values}")
    return (values[0], 0.0, 0.0, values[1] if len(values) == 2 else values[0], 0.0, 0.0)


BUILDERS = {"matrix": matrix, "translate": translate, "scale": scale}


def mul(a: tuple[float, ...], b: tuple[float, ...]) -> tuple[float, ...]:
    a11, a12, a21, a22, dx, dy = a
    b11, b12, b21, b22, bx, by = b
    return (
        a11 * b11 + a12 * b21,
        a11 * b12 + a12 * b22,
        a21 * b11 + a22 * b21,
        a21 * b12 + a22 * b22,
        a11 * bx + a12 * by + dx,
        a21 * bx + a22 * by + dy,
    )


def parse_transform(value: str) -> tuple[float, ...]:
    result = IDENTITY
    for name, args in re.findall(r"([a-zA-Z]+)\s*\(([^)]*)\)", value):
        if name not in BUILDERS:
            raise ValueError(f"Unsupported SVG transform: {name}")
        result = mul(result, BUILDERS[name](numbers(args)))
    return result


def cumulative_matrix(elem: ET.Element, parents: dict[ET.Element, ET.Element]) -> tuple[float, ...]:
    transforms = []
    current = elem
    while current is not None:
        transform = current.attrib.get("transform")
        if transform:
            transforms.append(parse_transform(transform))
        current = parents.get(current)
    result = IDENTITY
    for transform in reversed(transforms):
        result = mul(result, transform)
    return result


def dxf_point(m: tuple[float, ...], x: float, y: float, height: float) -> tuple[float, float]:
    a, b, c, d, e, f = m
    return (a * x + c * y + e, height - (b * x + d * y + f))  # SVG y is down; DXF y is up.


def layer_for(elem: ET.Element) -> str:
    match = re.search(r"stroke\s*:\s*#([0-9a-fA-F]{6})", elem.attrib.get("style", ""))
    if not match:
        return "CUT_RED"
    color = match.group(1).lower()
    return {"ff0000": "CUT_RED", "0000ff": "M3_BLUE"}.get(color, f"CUT_{color.upper()}")


def add_shape(msp, elem: ET.Element, parents: dict[ET.Element, ET.Element], height: float) -> None:
    m = cumulative_matrix(elem, parents)
    layer = layer_for(elem)
    if layer not in msp.doc.layers:
        msp.doc.layers.add(layer, color=ACI.get(layer, 7), lineweight=0)
    attrs = {"layer": layer, "lineweight": 0}  # Hairline: lineweight is display only, not cut geometry.

    if elem.tag == RECT:
        x, y = float(elem.attrib["x"]), float(elem.attrib["y"])
        w, h = float(elem.attrib["width"]), float(elem.attrib["height"])
        points = [
            dxf_point(m, x, y, height),
            dxf_point(m, x + w, y, height),
            dxf_point(m, x + w, y + h, height),
            dxf_point(m, x, y + h, height),
        ]
        msp.add_lwpolyline(points, close=True, dxfattribs=attrs)
        return

    if elem.tag == CIRCLE:
        x, y, r = (float(elem.attrib[k]) for k in ("cx", "cy", "r"))
        msp.add_circle(dxf_point(m, x, y, height), r, dxfattribs=attrs)
        return

    if elem.tag == PATH:
        for subpath in parse_path(elem.attrib["d"]).continuous_subpaths():
            points = []
            for segment in subpath:
                steps = 1 if type(segment).__name__ == "Line" else max(4, math.ceil(segment.length() / 0.5))
                for i in range(steps + 1):
                    if i == 0 and points:
                        continue
                    point = segment.point(i / steps)
                    points.append(dxf_point(m, point.real, point.imag, height))
            if len(points) < 2:
                continue
            if math.dist(points[0], points[-1]) < 1e-6:
                points.pop()
            msp.add_lwpolyline(points, close=True, dxfattribs=attrs)


def expected_entities(root: ET.Element) -> int:
    total = 0
    for elem in root.iter():
        if elem.tag in (RECT, CIRCLE):
            total += 1
        elif elem.tag == PATH:
            total += len(parse_path(elem.attrib["d"]).continuous_subpaths())
    return total


def sheet_size(root: ET.Element) -> tuple[float, float]:
    viewbox = numbers(root.attrib.get("viewBox", "0 0 600 600"))
    if len(viewbox) != 4:
        raise ValueError(f"Unsupported viewBox: {root.attrib.get('viewBox')}")
    return viewbox[2], viewbox[3]


def convert(svg: Path) -> None:
    root = ET.parse(svg).getroot()
    width, height = sheet_size(root)
    parents = {child: parent for parent in root.iter() for child in parent}
    expected = expected_entities(root)

    doc = ezdxf.new("R2010", setup=True)
    doc.header["$INSUNITS"] = 4  # millimetres
    doc.header["$MEASUREMENT"] = 1
    doc.header["$LWDISPLAY"] = 0
    doc.header["$EXTMIN"] = (0.0, 0.0, 0.0)
    doc.header["$EXTMAX"] = (width, height, 0.0)
    msp = doc.modelspace()

    for elem in root.iter():
        if elem.tag in SHAPES:
            add_shape(msp, elem, parents, height)

    assert len(msp) == expected, f"{svg.name}: {len(msp)} entities, expected {expected}"
    extents = ezdxf.bbox.extents(msp)
    assert abs(extents.extmin.x) < 1e-6 and abs(extents.extmin.y) < 1e-6, extents.extmin
    assert abs(extents.extmax.x - width) < 1e-6 and abs(extents.extmax.y - height) < 1e-6, extents.extmax
    assert not doc.audit().has_errors, f"{svg.name}: DXF audit failed"

    out = OUT / f"{svg.stem}.dxf"
    doc.saveas(out)
    print(f"{svg.name} -> {out.relative_to(HERE)}: {expected} entities")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for svg in sorted(HERE.glob("*.svg")):
        convert(svg)


if __name__ == "__main__":
    main()
