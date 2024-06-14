from PyPola.utilities.stokes_vector import StokesVector, NormalizationType
from numpy import sqrt, dot, sin, cos, pi
from random import uniform
from enum import Enum


class LinearPolarization(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    DIAGONAL = 2
    ANTIDIAGONAL = 3


def random_stokes_vector():
    s1 = uniform(-1, 1)
    s2_bound = sqrt(1 - s1 * s1)
    s2 = uniform(-s2_bound, s2_bound)
    s3_bound = sqrt(1 - s1 * s1 - s2 * s2)
    s3 = uniform(-s3_bound, s3_bound)
    return StokesVector(s0=1, s1=s1, s2=s2, s3=s3, normalization=NormalizationType.INTENSITY)


def stokes_vector_from_elliptical_parameters(i=1, p=1, psi=0, xi=0):
    s0 = i
    s1 = i * p * cos(2 * psi) * cos(2 * xi)
    s2 = i * p * sin(2 * psi) * cos(2 * xi)
    s3 = i * p * sin(2 * xi)
    return StokesVector(s0=s0, s1=s1, s2=s2, s3=s3)


def random_polarized_stokes_vector(bounds=None):
    if bounds is None:
        s1 = uniform(-1, 1)
        s2 = uniform(-1, 1)
        s3 = uniform(-1, 1)
    else:
        s1 = uniform(*bounds[0])
        s2 = uniform(*bounds[1])
        s3 = uniform(*bounds[2])
    return StokesVector(s0=1, s1=s1, s2=s2, s3=s3, normalization=NormalizationType.POINCARE_SPHERE)


def random_linearly_polarized_stokes_vector(bounds=None):
    if bounds is None:
        s1 = uniform(-1, 1)
        s2 = uniform(-1, 1)
    else:
        s1 = uniform(*bounds[0])
        s2 = uniform(*bounds[1])
    return StokesVector(s0=1, s1=s1, s2=s2, s3=0, normalization=NormalizationType.POINCARE_SPHERE)


def normalized_dot_product(stokes_vector_1: StokesVector, stokes_vector_2: StokesVector):
    stokes_vector_1.normalize(NormalizationType.POINCARE_SPHERE)
    stokes_vector_1.normalize(NormalizationType.POINCARE_SPHERE)
    return dot(stokes_vector_1.as_3d_array(), stokes_vector_2.as_3d_array())


double_theta_map = {
    LinearPolarization.HORIZONTAL: 0,
    LinearPolarization.VERTICAL: pi,
    LinearPolarization.DIAGONAL: 0.5 * pi,
    LinearPolarization.ANTIDIAGONAL: 1.5 * pi
}

linear_stokes_vector_map = {
    LinearPolarization.HORIZONTAL: StokesVector(s0=1, s1=1, s2=0, s3=0),
    LinearPolarization.VERTICAL: StokesVector(s0=1, s1=-1, s2=0, s3=0),
    LinearPolarization.DIAGONAL: StokesVector(s0=1, s1=0, s2=1, s3=0),
    LinearPolarization.ANTIDIAGONAL: StokesVector(s0=1, s1=0, s2=-1, s3=0)
}
