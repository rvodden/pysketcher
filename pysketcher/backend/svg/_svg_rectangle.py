from lxml import etree

from ._svg_adapter import SvgAdapter
from ._svg_style import SvgStyle

import pysketcher as ps


class SvgRectangle(SvgAdapter):
    @staticmethod
    def plot(shape: ps.Rectangle, axes: etree.Element, defs: etree.Element):
        etree.SubElement(
            axes,
            "rect",
            attrib={
                "x": f"{shape.lower_left.x}cm",
                "y": f"{shape.lower_left.y}cm",
                "width": f"{shape.width}cm",
                "height": f"{shape.height}cm",
                **SvgStyle(shape.style).attribs(defs),
            },
        )
