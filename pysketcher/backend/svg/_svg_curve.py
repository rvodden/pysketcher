from lxml import etree

import pysketcher as ps

from ._svg_adapter import SvgAdapter
from ._svg_style import SvgStyle


class SvgCurve(SvgAdapter):
    def plot(self, curve: ps.Curve, axes: etree.Element, defs: etree.Element):
        etree.SubElement(
            axes,
            "path",
            attrib={
                "d": self._data(curve),
                **SvgStyle(curve.style).attribs(defs),
            },
        )

    def _data(self, curve: ps.Curve) -> str:
        pts = curve.points
        d = f"M{pts[0].x} {pts[0].y}"
        for p in pts[1:]:
            d += f" L{p.x * self._svgb.SVG_SCALE} {p.y * self._svgb.SVG_SCALE}"
        return d
