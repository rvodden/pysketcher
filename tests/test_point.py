from math import inf

from hypothesis import assume, given, note
from hypothesis.strategies import builds
import numpy as np
import pytest

from pysketcher import Angle, Point
from tests.strategies import make_angle, make_float
from tests.utils import isclose


def make_point():
    return builds(Point, make_float(), make_float())


class TestPoint:
    @given(make_float(), make_float())
    def test_coordinates(self, x: float, y: float) -> None:
        p = Point(x, y)
        assert p.x == x
        assert p.y == y

    @given(make_float(), make_float())
    def test_equality(self, x: float, y: float) -> None:
        assert Point(x, y) == Point(x, y)

    @given(make_float(), make_float(), make_float(), make_float())
    def test_adding(self, x1: float, x2: float, y1: float, y2: float):
        a = Point(x1, y1)
        b = Point(x2, y2)
        assert a + b == Point(x1 + x2, y1 + y2)

    @given(make_float(), make_float(), make_float(), make_float())
    def test_translation(self, x1: float, x2: float, y1: float, y2: float):
        a = Point(x1, y1)
        b = Point(x2, y2)
        assert a + b == Point(x1 + x2, y1 + y2)

    @given(make_float(), make_float(), make_float(), make_float())
    def test_subtraction(self, x1: float, x2: float, y1: float, y2: float):
        a = Point(x1, y1)
        b = Point(x2, y2)
        assert a - b == Point(x1 - x2, y1 - y2)

    @given(make_float(), make_float(), make_float())
    def test_multiplication(self, x: float, y: float, s: float):
        a = Point(x, y)
        assert a * s == Point(x * s, y * s)

    @given(make_float(), make_float(), make_float())
    def test_scale(self, x: float, y: float, s: float):
        a = Point(x, y)
        assert a.scale(s) == Point(x * s, y * s)

    @given(make_float(), make_float())
    def test_abs(self, x: float, y: float):
        assume(x * x != inf)
        assume(y * y != inf)
        a = Point(x, y)
        assert abs(a) == np.hypot(x, y)

    @given(make_point())
    def test_angle(self, a: Point):
        if a.x != 0.0:
            assume(abs(a.y / a.x) < 1e4)
        if a.y != 0.0:
            assume(abs(a.x / a.y) < 1e4)
        angle = a.angle
        note(angle)
        b = Point(abs(a), 0.0).rotate(angle, Point(0.0, 0.0))
        note(f"The angle is : {np.format_float_scientific(a.angle)}")
        note(f"The length is : {np.format_float_scientific(abs(a))}")
        assert b == a
        assert -np.pi <= angle <= np.pi

    @given(make_float(), make_float())
    def test_unit_vector(self, x: float, y: float):
        a = Point(x, y)
        if isclose(abs(a), 0.0):
            with pytest.raises(ZeroDivisionError):
                a.unit_vector
        else:
            b = a.unit_vector
            note(f"angle of a: {np.format_float_scientific(a.angle)}")
            note(f"angle of b: {np.format_float_scientific(b.angle)}")
            assert isclose(a.angle, b.angle)
            note(f"magnitude of b: {abs(b)}")
            assert isclose(abs(b), 1.0)

    @given(make_point())
    def test_normal_vector(self, a: Point):
        if isclose(abs(a), 0.0):
            with pytest.raises(ZeroDivisionError):
                a.normal
        else:
            angle = a.normal.angle - a.angle
            assert isclose(angle, np.pi / 2.0)

    @given(make_point(), make_angle())
    def test_rotation_about_zero(self, a: Point, angle: Angle):
        assume(abs(a) != 0)
        b = a.rotate(angle, Point(0.0, 0.0))
        aa = a.angle
        bb = b.angle
        note(f"a angle: {aa}")
        note(f"b angle: {bb}")
        assert isclose(bb - aa, angle)

    @given(make_point(), make_angle(), make_point())
    def test_rotation(self, a: Point, angle: Angle, center: Point):
        assume(abs(a - center) != 0)
        b = a.rotate(angle, center)
        new_angle = (b - center).angle - (a - center).angle
        note(str(angle))
        note(str(new_angle))
        assert isclose(angle, angle)
