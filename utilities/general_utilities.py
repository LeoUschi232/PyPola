from numpy import array, sign
from numpy.linalg import norm
from random import choice
from time import sleep
from tqdm import tqdm


def normalize(v):
    v = array(v).flatten()
    return v / norm(v)


def get_4x4_unit_matrix():
    return array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def random_sign():
    return choice([-1, +1])


def round_p(f):
    return 0.0 if same(f, 0) else round(f, 12)


def same(f1: float, f2: float):
    return abs(f1 - f2) < 1e-12


def float_array_same(v1, v2):
    v1 = array(v1)
    v2 = array(v2)
    if v1.shape != v2.shape:
        return False
    v1 = v1.flatten()
    v2 = v2.flatten()
    for a, b in zip(v1, v2):
        if not same(a, b):
            return False
    return True


def sgn(fl: float):
    return sign(fl)


def progress_bar(nr_of_points, message=""):
    print(message)
    sleep(0.1)
    return tqdm(total=nr_of_points)
