from hypothesis import example, given, note
from hypothesis.strategies import booleans, floats
import numpy as np

from pysketcher import Angle
from tests.strategies import make_angle, make_float


class TestAngle:
    @given(make_float())
    @example(8725732868031747.0)
    @example(8726832379593987.0)
    def test_range(self, x: float):
        a = Angle(x)
        assert -np.pi < a
        assert a <= np.pi

    @given(make_float())
    def test_equality(self, x: float):
        if -np.pi < x < np.pi:
            assert x == Angle(x)
        else:
            assert Angle(x) == Angle(x)

    @given(make_angle(), make_float())
    def test_addition(self, a: Angle, b: Angle):
        c = a + b
        assert type(c) == Angle
        assert -np.pi <= c
        assert c <= np.pi

    @given(make_angle(), make_angle())
    def test_subtraction(self, a: Angle, b: Angle):
        c = a - b
        assert type(c) == Angle
        assert -np.pi <= c
        assert c <= np.pi

    @given(make_angle(), make_float())
    def test_multiplication(self, a: Angle, b: float):
        c = a * b
        assert type(c) == Angle
        assert c <= np.pi
        assert -np.pi < c

    @given(make_angle(), floats(min_value=1e-6, max_value=1e6), booleans())
    def test_division(self, a: Angle, b: float, negate: bool):
        if negate:
            b = -b
        c = a / b
        note(c)
        assert type(c) == Angle
        assert -np.pi <= c
        assert c <= np.pi
