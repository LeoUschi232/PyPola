from numpy import array, sign, pi, sin, cos
from numpy.linalg import norm
from random import choice


def clean(f):
    return 0.0 if abs(f) < 1e-12 else round(f, 12)


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


def p_sin(fl: float):
    if same(fl, - 2 * pi) or same(fl, -pi) or same(fl, 0) or same(fl, pi) or same(fl, 2 * pi):
        return 0.0
    if same(fl, - 0.5 * pi) or same(fl, 1.5 * pi):
        return -1.0
    if same(fl, -1.5 * pi) or same(fl, 0.5 * pi):
        return 1.0
    return sin(fl)


def p_cos(fl):
    if same(fl, - 1.5 * pi) or same(fl, -0.5 * pi) or same(fl, 0.5 * pi) or same(fl, 1.5 * pi):
        return 1.0
    if same(fl, -2 * pi) or same(fl, 0) or same(fl, 2 * pi):
        return 0.0
    if same(fl, - pi) or same(fl, pi):
        return -1.0
    return cos(fl)
