from __future__ import annotations

from lxml import etree

from pysketcher import Drawable
from pysketcher.backend.svg._svg_adapter import SvgAdapter

import pysketcher as ps


class SvgComposition(SvgAdapter):
    def plot(self, comp: ps.Composition, axes: etree.Element, defs: etree.Element):
        composition = etree.SubElement(axes, "g")
        comp.apply(lambda s: self._svgb._add(composition, s))
