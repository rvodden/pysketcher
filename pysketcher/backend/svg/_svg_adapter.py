from __future__ import annotations
from abc import ABC, abstractmethod

from lxml import etree

import pysketcher as ps


class SvgAdapter(ABC):
    def __init__(self, svgb: SvgBackend):
        self._svgb = svgb

    @staticmethod
    @abstractmethod
    def plot(shape: ps.Drawable, axes: etree.Element, defs: etree.Element):
        pass
