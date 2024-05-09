from numpy import sqrt, arctan, sign, pi, dot, array, sin, cos
from random import uniform


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


def stokes_vector_from_elliptical_parameters(i=1, p=1, psi=0, xi=0):
    return [[i], [i * p * cos(2 * psi) * cos(2 * xi)], [i * p * sin(2 * psi) * cos(2 * xi)], [i * p * sin(2 * xi)]]


def random_polarized_stokes_vector(bounds=None):
    if bounds is None:
        s1 = uniform(-1, 1)
        s2 = uniform(-1, 1)
        s3 = uniform(-1, 1)
    else:
        s1 = uniform(*bounds[0])
        s2 = uniform(*bounds[1])
        s3 = uniform(*bounds[2])
    normalization = sqrt(s1 * s1 + s2 * s2 + s3 * s3)
    if normalization < 1e-12:
        return [[1], [0], [0], [0]]
    return [[1], [s1 / normalization], [s2 / normalization], [s3 / normalization]]


def random_linearly_polarized_stokes_vector(bounds=None):
    if bounds is None:
        s1 = uniform(-1, 1)
        s2 = uniform(-1, 1)
    else:
        s1 = uniform(*bounds[0])
        s2 = uniform(*bounds[1])
    normalization = sqrt(s1 * s1 + s2 * s2)
    if normalization < 1e-12:
        return [[1], [0], [0], [0]]
    return [[1], [s1 / normalization], [s2 / normalization], [0]]


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
    return 0.5 * (arctan(s2 / s1) - pi)


def get_ellipticity_angle(stokes_vector):
    _, s1, s2, s3 = [s_i[0] for s_i in stokes_vector]
    return 0.5 * arctan(s3 / sqrt(s1 * s1 + s2 * s2))


def normalized_dotp(stokes_vector_1, stokes_vector_2):
    stokes_vector_1 = array(normalize_stokes_vector(stokes_vector_1)[1:])
    stokes_vector_2 = array(normalize_stokes_vector(stokes_vector_2)[1:])
    return dot(stokes_vector_1, stokes_vector_2)
