import numpy as np

atol = 1e-4


def isclose(a: float, b: float):
    return np.isclose(a, b, atol=atol)
