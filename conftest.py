from typing import Type

from hypothesis.strategies import builds, floats, SearchStrategy
import numpy as np
import pytest

import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend
from tests.utils import TypeStrategy

mx = 1e30
mn = 1e-30
atol = 1e-4


@pytest.fixture(scope="session", autouse=True)
def setup_testing(request):
    np.seterr(over="warn", divide="warn")


@pytest.fixture(autouse=True)
def add_np(doctest_namespace):
    doctest_namespace["np"] = np
    doctest_namespace["ps"] = ps
    doctest_namespace["MatplotlibBackend"] = MatplotlibBackend


def isclose(a: float, b: float):
    return np.isclose(a, b, atol=atol)


@TypeStrategy()
def make_angle(typ: Type) -> SearchStrategy[ps.Angle]:
    def flt(a: typ):
        if a != 0.0:
            return abs(a) > mn

    return builds(ps.Angle, make_float(typ)).filter(flt)


@TypeStrategy()
def make_float(typ: Type) -> SearchStrategy[float]:
    strategy = floats(allow_nan=False, allow_infinity=False).filter(
        lambda x: -mx < x < mx
    )
    return strategy


@TypeStrategy()
def make_point(typ: Type) -> SearchStrategy[ps.Point]:
    def flt(a: ps.Point) -> bool:
        retval = True
        if a.x != 0.0:
            retval = retval and a.x > mn
        if a.y != 0.0:
            retval = retval and a.y > mn
        return retval and mx > abs(a) > 0.0

    return builds(ps.Point, make_float(float), make_float(float)).filter(flt)
