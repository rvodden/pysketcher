from math import inf

from conftest import isclose
from hypothesis import assume, HealthCheck, note, settings
import numpy as np
import pytest

from pysketcher import Angle, Point
from tests.utils import given_inferred


class TestPoint:
    @given_inferred
    def test_coordinates(self, x: float, y: float) -> None:
        p = Point(x, y)
        assert p.x == x
        assert p.y == y

    @given_inferred
    def test_equality(self, x: float, y: float) -> None:
        assert Point(x, y) == Point(x, y)

    @given_inferred
    def test_adding(self, x1: float, x2: float, y1: float, y2: float):
        a = Point(x1, y1)
        b = Point(x2, y2)
        assert a + b == Point(x1 + x2, y1 + y2)

    @given_inferred
    def test_translation(self, x1: float, x2: float, y1: float, y2: float):
        a = Point(x1, y1)
        b = Point(x2, y2)
        assert a + b == Point(x1 + x2, y1 + y2)

    @given_inferred
    def test_subtraction(self, x1: float, x2: float, y1: float, y2: float):
        a = Point(x1, y1)
        b = Point(x2, y2)
        assert a - b == Point(x1 - x2, y1 - y2)

    @given_inferred
    def test_multiplication(self, x: float, y: float, s: float):
        a = Point(x, y)
        assert a * s == Point(x * s, y * s)

    @given_inferred
    def test_scale(self, x: float, y: float, s: float):
        a = Point(x, y)
        assert a.scale(s) == Point(x * s, y * s)

    @given_inferred
    def test_abs(self, x: float, y: float):
        assume(x * x != inf)
        assume(y * y != inf)
        a = Point(x, y)
        assert abs(a) == np.hypot(x, y)

    @given_inferred
    @settings(suppress_health_check=[HealthCheck.filter_too_much])
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

    @given_inferred
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

    @given_inferred
    def test_normal_vector(self, a: Point):
        if isclose(abs(a), 0.0):
            with pytest.raises(ZeroDivisionError):
                a.normal
        else:
            angle = a.normal.angle - a.angle
            assert isclose(angle, np.pi / 2.0)

    @given_inferred
    def test_rotation_about_zero(self, a: Point, angle: Angle):
        assume(abs(a) != 0)
        b = a.rotate(angle, Point(0.0, 0.0))
        aa = a.angle
        bb = b.angle
        note(f"a angle: {aa}")
        note(f"b angle: {bb}")
        assert isclose(bb - aa, angle)

    @given_inferred
    @settings(suppress_health_check=[HealthCheck.filter_too_much])
    def test_rotation(self, a: Point, angle: Angle, center: Point):
        assume(abs(a - center) != 0)
        b = a.rotate(angle, center)
        new_angle = (b - center).angle - (a - center).angle
        note(str(angle))
        note(str(new_angle))
        assert isclose(angle, angle)


#
#
# from_coordinate_lists_data = [
#     ([1, 2, 3, 4], [1, 2, 3, 4], [Point(1, 1), Point(2, 2), Point(3, 3), Point(4, 4)])
# ]
#
#
# @pytest.mark.parametrize("xs, ys, expected", from_coordinate_lists_data)
# def test_from_coordinate_lists(xs: List[float],
# ys: List[float],
# expected: List[Point]):
#     assert Point.from_coordinate_lists(xs, ys) == expected
#
#
# @pytest.mark.parametrize("xs, ys, expected", from_coordinate_lists_data)
# def test_to_coordinate_lists(xs, ys, expected):
#     assert Point.to_coordinate_lists(expected) == (xs, ys)
