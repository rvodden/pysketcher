import numpy as np
import pytest
from hypothesis.strategies import register_type_strategy

import pysketcher as ps
from pysketcher.backend.matplotlib import MatplotlibBackend

from tests.strategies import make_float, make_angle


def pytest_addoption(parser):
    parser.addoption("--backend", choices=['matplotlib', 'svg'], default='matplotlib')
    parser.addoption("--show", const=True, default=False, action="store_const")

@pytest.fixture(scope="session", autouse=True)
def setup_testing(request):
    np.seterr(over="warn", divide="warn")
    register_type_strategy(ps.Angle, make_angle())
    register_type_strategy(float, make_float())


@pytest.fixture(autouse=True)
def add_np(doctest_namespace):
    doctest_namespace["np"] = np
    doctest_namespace["ps"] = ps
    doctest_namespace["MatplotlibBackend"] = MatplotlibBackend

