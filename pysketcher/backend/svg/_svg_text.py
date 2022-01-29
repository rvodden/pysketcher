from lxml import etree

import pysketcher as ps

from pysketcher.backend.svg._svg_adapter import SvgAdapter
from pysketcher.backend.svg._svg_style import SvgTextStyle


class SvgText(SvgAdapter):
    @staticmethod
    def plot(text: ps.Text, axes: etree.Element, defs: etree.Element):
        textElement = etree.SubElement(
            axes,
            "text",
            attrib={
                "x": f"{text.position.x}cm",
                "y": f"{text.position.y}cm",
                **SvgTextStyle(text.style).attribs(defs),
            },
        )
        textElement.text = text.text
