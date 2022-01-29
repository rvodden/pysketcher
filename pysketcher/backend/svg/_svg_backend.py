from functools import singledispatchmethod
import logging
from typing import Callable, Dict, Tuple, Type, Union

from lxml import etree
import pysketcher as ps

from pysketcher.backend.backend import Backend
from ._svg_adapter import SvgAdapter
from ._svg_curve import SvgCurve
from ._svg_circle import SvgCircle
from ._svg_composition import SvgComposition
from ._svg_line import SvgLine
from ._svg_rectangle import SvgRectangle
from ._svg_text import SvgText


class SvgBackend(Backend):
    """Simple interface for plotting. Makes use of Matplotlib for plotting."""

    SVG_SCALE: float = 35.43

    _doc: etree.ElementTree
    _root: etree.Element
    _axes: etree.SubElement
    _x_min: float
    _y_min: float
    _x_max: float
    _y_max: float

    def __init__(self, x_min, x_max, y_min, y_max):
        self._x_min = x_min
        self._x_max = x_max
        self._y_min = y_min
        self._y_max = y_max
        self._camera = None
        self._defs = None
        self._root = etree.Element(
            "svg",
            attrib={
                "xmlns": "http://www.w3.org/2000/svg",
                "version": "1.1",
                "width": f"{x_max - x_min}cm",
                "height": f"{y_max - y_min}cm",
                "viewBox": f"{self.SVG_SCALE * x_min} {self.SVG_SCALE * y_min} "
                f"{self.SVG_SCALE * (x_max - x_min)} "
                f"{self.SVG_SCALE * (y_max - y_min)}",
            },
        )
        self._doc = etree.ElementTree(element=self._root)
        self._configure_axes()
        self._load_defs()

    def _load_defs(self):
        self._defs = etree.SubElement(self._root, "defs")

    def _configure_axes(self):
        # self._axes = eT.SubElement(self._root, "g", attrib={
        #     "transform": f"translate({self._x_min},{self._y_max}) scale(1,-1)"
        # })
        self._axes = etree.SubElement(self._root, "g")

    @singledispatchmethod
    def add(self, shape: ps.Drawable) -> None:
        raise NotImplementedError(f"No adapter found for {type(shape)}.")

    @add.register
    def _(self, circle: ps.Circle):
        SvgCircle.plot(self._axes, circle)

    @add.register
    def _(self, line: ps.Line):
        SvgLine.plot(self._axes, line)

    @add.register
    def _(self, rectangle: ps.Rectangle):
        SvgRectangle.plot(self._axes, rectangle)

    @add.register
    def _(self, composition: ps.Composition):
        SvgComposition.plot(self._axes, composition)

    @add.register
    def _(self, text: ps.Text):
        SvgText.plot(self._axes, text)

    @add.register
    def _(self, curve: ps.Curve):
        SvgCurve.plot(self._axes, curve)

    def erase(self):
        raise NotImplementedError("Erase is not yet implemented")

    def show(self):
        raise NotImplementedError("Show is not yet implemented")

    def save(self, filename: str) -> None:
        logging.info(f"Saving to {filename}.")
        etree.indent(self._doc, space=" ", level=0)
        self._doc.write(filename, xml_declaration=True, encoding="utf-8")

    @property
    def _adapters(self) -> Dict[Type, SvgAdapter]:
        return {
        }

    def animate(
        self,
        func: Callable[[float], ps.Drawable],
        interval: Union[Tuple[float, float], Tuple[float, float, float]],
    ):
        raise NotImplementedError("Animation is not yet implemented")

    def show_animation(self):
        raise NotImplementedError("Animation is not yet implemented")

    def save_animation(self, filename: str):
        raise NotImplementedError("Animation is not yet implemented")
