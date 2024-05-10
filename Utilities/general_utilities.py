from numpy import array, sign
from numpy.linalg import norm
from random import choice


def clean(f):
    return 0.0 if abs(f) < 3e-15 else float(f)


def normalize_and_clean(v):
    v = array(v)
    v = v / norm(v)
    return array([clean(x) for x in v])


def get_4x4_unit_matrix():
    return array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def random_sign():
    return choice([-1, +1])


def same(f1: float, f2: float):
    return abs(f1 - f2) < 1e-12


def float_array_same(v1, v2):
    v1 = list(array(v1).flatten())
    v2 = list(array(v2).flatten())
    if len(v1) != len(v2):
        return False
    for a, b in zip(v1, v2):
        if not same(a, b):
            return False
    return True


def sgn(fl: float):
    return sign(fl)
