from numpy import sqrt, arctan, sign, pi
from random import uniform
from matplotlib import pyplot as plt


def degree_of_polarization(stokes_vector):
    s0, s1, s2, s3 = [s_i[0] for s_i in stokes_vector]
    raw_dop = sqrt(s1 * s1 + s2 * s2 + s3 * s3) / s0
    return 0 if abs(raw_dop) < 1e-12 else min(1, max(0, raw_dop))


def normalize_stokes_vector(stokes_vector):
    s0, s1, s2, s3 = [s_i[0] for s_i in stokes_vector]
    i2p2 = s1 * s1 + s2 * s2 + s3 * s3
    if i2p2 > s0 * s0:
        print(f"Stokes vectore cannot be normalized.\nInvalid Stokes vector:\n{stokes_vector}")
        return [[1], [0], [0], [0]]
    return [[1], [s1 / s0], [s2 / s0], [s3 / s0]]


def random_stokes_vector():
    s1 = uniform(-1, 1)
    s2 = uniform(-1, 1)
    s3 = uniform(-1, 1)
    normalization = sqrt(s1 * s1 + s2 * s2 + s3 * s3)
    if normalization < 1e-12:
        return [[1], [0], [0], [0]]
    if normalization > 1:
        return [[1], [s1 / normalization], [s2 / normalization], [s3 / normalization]]
    return [[1], [s1], [s2], [s3]]


def random_polarized_stokes_vector():
    s1 = uniform(-1, 1)
    s2 = uniform(-1, 1)
    s3 = uniform(-1, 1)
    normalization = sqrt(s1 * s1 + s2 * s2 + s3 * s3)
    if normalization < 1e-12:
        return [[1], [0], [0], [0]]
    return [[1], [s1 / normalization], [s2 / normalization], [s3 / normalization]]


def get_angle_to_x_axis(stokes_vector):
    _, s1, s2, _ = [s_i[0] for s_i in stokes_vector]
    if s1 == 0:
        return 0.25 * sign(s2) * pi
    if s1 > 0:
        return 0.5 * arctan(s2 / s1)
    if s2 == 0:
        return 0.5 * pi
    if s2 > 0:
        return 0.5 * (arctan(s2 / s1) + pi)
    return  0.5 * (arctan(s2 / s1) - pi)


