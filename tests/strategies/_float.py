from hypothesis.strategies import builds, floats, one_of, SearchStrategy

import pysketcher as ps

mx = 1e30
mn = 1e-30


def make_float() -> SearchStrategy[float]:
    strategy = floats(
        min_value=mn,
        max_value=mx,
        allow_nan=False,
        allow_infinity=False,
        allow_subnormal=False,
    )
    return strategy


def make_angle() -> SearchStrategy[ps.Angle]:
    def angle_float():
        return one_of(
            floats(
                min_value=mn,
                max_value=mx,
                allow_nan=False,
                allow_infinity=False,
                allow_subnormal=False,
            ),
            floats(
                max_value=-mn,
                min_value=-mx,
                allow_nan=False,
                allow_infinity=False,
                allow_subnormal=False,
            ),
        )

    return builds(ps.Angle, angle_float())
