from lxml import etree

from ._svg_adapter import SvgAdapter
from ._svg_style import SvgStyle

import pysketcher as ps


class SvgLine(SvgAdapter):
    def plot(self, shape: ps.Line, axes: etree.Element, defs: etree.Element):
        etree.SubElement(
            axes,
            "line",
            attrib={
                "x1": f"{shape.start.x}cm",
                "y1": f"{shape.start.y}cm",
                "x2": f"{shape.end.x}cm",
                "y2": f"{shape.end.y}cm",
                **SvgStyle(shape.style).attribs(defs),
            },
        )
