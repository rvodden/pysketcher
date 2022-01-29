from __future__ import annotations
from lxml import etree

from ._svg_adapter import SvgAdapter
from ._svg_style import SvgStyle

import pysketcher as ps


class SvgCircle(SvgAdapter):
    def plot(self, shape: ps.Circle, axes: etree.Element, defs: etree.Element):
        etree.SubElement(
            axes,
            "circle",
            attrib={
                "cx": f"{shape.center.x}cm",
                "cy": f"{shape.center.y}cm",
                "r": f"{shape.radius}cm",
                **SvgStyle(shape.style).attribs(defs),
            },
        )
