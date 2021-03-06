from hypothesis import given, note
from hypothesis.strategies import booleans, floats, from_type
import numpy as np

from pysketcher import Angle
from tests.utils import given_inferred


class TestAngle:
    @given_inferred
    def test_range(self, x: Angle):
        assert -np.pi < x
        assert x <= np.pi

    @given_inferred
    def test_equality(self, x: float):
        if -np.pi < x < np.pi:
            assert x == Angle(x)
        else:
            assert Angle(x) == Angle(x)

    @given_inferred
    def test_addition(self, a: Angle, b: Angle):
        c = a + b
        assert type(c) == Angle
        assert -np.pi <= c
        assert c <= np.pi

    @given_inferred
    def test_subtraction(self, a: Angle, b: Angle):
        c = a - b
        assert type(c) == Angle
        assert -np.pi <= c
        assert c <= np.pi

    @given_inferred
    def test_multiplication(self, a: Angle, b: float):
        c = a * b
        assert type(c) == Angle
        assert c <= np.pi
        assert -np.pi < c

    @given(from_type(Angle), floats(min_value=1e-6, max_value=1e6), booleans())
    def test_division(self, a: Angle, b: float, negate: bool):
        if negate:
            b = -b
        c = a / b
        note(c)
        assert type(c) == Angle
        assert -np.pi <= c
        assert c <= np.pi
