import pkgutil
from typing import Dict

from lxml import etree

import pysketcher as ps


class SvgStyle:
    _style: ps.Style
    LINE_STYLE_MAP = {
        ps.Style.LineStyle.SOLID: None,
        ps.Style.LineStyle.DOTTED: ".1",
        ps.Style.LineStyle.DASHED: ".4 .1",
        ps.Style.LineStyle.DASH_DOT: ".4 .1 .1 .1",
    }

    FILL_PATTERN_MAP = {
        ps.Style.FillPattern.CIRCLE: "circle",
        ps.Style.FillPattern.CROSS: "cross",
        ps.Style.FillPattern.DOT: "dot",
        ps.Style.FillPattern.HORIZONTAL: "horizontal",
        ps.Style.FillPattern.SQUARE: "square",
        ps.Style.FillPattern.STAR: "star",
        ps.Style.FillPattern.SMALL_CIRCLE: "smallCircle",
        ps.Style.FillPattern.VERTICAL: "vertical",
        ps.Style.FillPattern.UP_LEFT_TO_RIGHT: "upLeftToRight",
        ps.Style.FillPattern.UP_RIGHT_TO_LEFT: "upRightToLeft",
    }

    COLOR_MAP = {
        ps.Style.Color.GREY: "Grey",
        ps.Style.Color.BLACK: "Black",
        ps.Style.Color.BLUE: "Blue",
        ps.Style.Color.BROWN: "Brown",
        ps.Style.Color.CYAN: "Cyan",
        ps.Style.Color.GREEN: "Green",
        ps.Style.Color.MAGENTA: "Magenta",
        ps.Style.Color.ORANGE: "Orange",
        ps.Style.Color.PURPLE: "Purple",
        ps.Style.Color.RED: "Red",
        ps.Style.Color.YELLOW: "Yellow",
        ps.Style.Color.WHITE: "White",
    }

    ARROW_MAP = {
        ps.Style.ArrowStyle.START: "startArrowHead",
        ps.Style.ArrowStyle.END: "endArrowHead",
    }

    def __init__(self, style: ps.Style):
        self._style = style

    @property
    def line_width(self) -> float:
        return self._style.line_width

    @property
    def line_style(self) -> str:
        return self.LINE_STYLE_MAP.get(self._style.line_style)

    @property
    def line_color(self):
        return self.COLOR_MAP.get(self._style.line_color)

    @property
    def fill_color(self):
        return self.COLOR_MAP.get(self._style.fill_color)

    @property
    def fill_pattern(self):
        return self.FILL_PATTERN_MAP.get(self._style.fill_pattern)

    @property
    def arrow(self):
        return self.ARROW_MAP.get(self._style.arrow)

    def __str__(self):
        return (
            "line_style: %s, line_width: %s, line_color: %s,"
            " fill_pattern: %s, fill_color: %s, arrow: %s"
            % (
                self.line_style,
                self.line_width,
                self.line_color,
                self.fill_pattern,
                self.fill_color,
                self.arrow,
            )
        )

    def _load_def(self, defs: etree.Element, df: str):
        df = etree.fromstring(pkgutil.get_data(__name__, f"templates/{df}.xml"))
        defs.append(df)

    def attribs(self, defs: etree.Element) -> Dict[str, str]:
        ret_dict = {}

        self._process_line_settings(ret_dict)
        self._process_fill_settings(defs, ret_dict)
        self._process_arrows(defs, ret_dict)

        return ret_dict

    def _process_fill_settings(self, defs, ret_dict):
        ret_dict["fill"] = self.fill_color if self.fill_color else "none"
        if self.fill_pattern:
            self._load_def(defs, self.fill_pattern)
            ret_dict["fill"] = f"url(#{self.fill_pattern})"

    def _process_line_settings(self, ret_dict):
        if self.line_width:
            ret_dict["stroke-width"] = f"{self.line_width}px"
        if self.line_color:
            ret_dict["stroke"] = self.line_color
        if self.line_style:
            ret_dict["stroke-dasharray"] = self.line_style

    def _process_arrows(self, defs, ret_dict):
        if self._style.arrow in [ps.Style.ArrowStyle.END, ps.Style.ArrowStyle.DOUBLE]:
            end_arrow = self.ARROW_MAP[ps.Style.ArrowStyle.END]
            self._load_def(defs, end_arrow)
            ret_dict["marker-end"] = f"url(#{end_arrow})"
        if self._style.arrow in [ps.Style.ArrowStyle.START, ps.Style.ArrowStyle.DOUBLE]:
            start_arrow = self.ARROW_MAP[ps.Style.ArrowStyle.START]
            self._load_def(defs, start_arrow)
            ret_dict["marker-start"] = f"url(#{start_arrow})"


class SvgTextStyle(SvgStyle):
    FONT_FAMILY_MAP = {
        ps.TextStyle.FontFamily.SERIF: "serif",
        ps.TextStyle.FontFamily.SANS: "sans-serif",
        ps.TextStyle.FontFamily.MONO: "monospace",
    }

    ALIGNMENT_MAP = {
        ps.TextStyle.Alignment.LEFT: "left",
        ps.TextStyle.Alignment.RIGHT: "right",
        ps.TextStyle.Alignment.CENTER: "middle",
    }

    _style: ps.TextStyle

    def __init__(self, text_style: ps.TextStyle):
        super().__init__(text_style)

    @property
    def font_size(self) -> float:
        return self._style.font_size

    @property
    def font_family(self) -> str:
        return self.FONT_FAMILY_MAP.get(self._style.font_family)

    @property
    def alignment(self) -> str:
        return self.ALIGNMENT_MAP.get(self._style.alignment)

    def attribs(self, defs: etree.Element) -> Dict[str, str]:
        ret_dict = super().attribs(defs)

        if self.font_size:
            ret_dict["font-size"] = f"{self.font_size}pt"

        if self.font_family:
            ret_dict["font-family"] = self.font_family

        if self.alignment:
            ret_dict["text-anchor"] = self.alignment

        return ret_dict
