from pysketcher.backend.svg import SvgBackend

import numpy as np
import pysketcher as ps


class TestSvgBackend:
    def test_svg_backend(self):
        circle = ps.Circle(ps.Point(1.5, 1.5), 1)
        circle.style.line_color = ps.Style.Color.RED
        circle.set_fill_pattern(ps.Style.FillPattern.UP_RIGHT_TO_LEFT)
        line = ps.Line(ps.Point(1.5, 1.5), circle(-np.pi / 4))
        line.set_arrow(ps.Style.ArrowStyle.DOUBLE)
        fig = ps.Figure(0, 3, 0, 3, backend=SvgBackend)
        fig.add(circle)
        fig.add(line)
        fig.save("circle.svg")

        # TODO: add some asserts here :-)

    def test_svg_hatching(self):
        from examples.hatch_test import main

        fig = main(SvgBackend)
        fig.save("test_hatch.svg")

    def test_svg_hello_world(self):
        from examples.hello_world import main

        fig = main(SvgBackend)
        fig.save("hello_world.svg")

    def test_svg_curve(self):
        code = ps.Curve(
            [
                ps.Point(0, 0),
                ps.Point(1, 1),
                ps.Point(2, 4),
                ps.Point(3, 9),
                ps.Point(4, 16),
            ]
        )
        code.style.line_color = ps.Style.Color.BLACK
        model = ps.Composition(dict(text=code))
        fig = ps.Figure(0, 5, 0, 16, backend=SvgBackend)
        fig.add(model)
        fig.save("curve.svg")
