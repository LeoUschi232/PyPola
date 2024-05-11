from PyPola.Utilities.general_utilities import float_array_same, clean
from numpy import array, sqrt, abs, sign, pi, arctan
from numpy.linalg import norm
from enum import Enum


class NormalizationType(Enum):
    NONE = 0
    INTENSITY = 1
    POINCARE_SPHERE = 2


class StokesVector:
    def __init__(
            self,
            s0: float | int,
            s1: float | int,
            s2: float | int,
            s3: float | int,
            normalization: NormalizationType = NormalizationType.NONE
    ):
        # Stokes parameters
        s0 = abs(s0)
        if s0 == 0:
            print("Warning: Stokes vector must have a non-zero intensity. Defaulting s0 to 1.")
            s0 = 1
        self.s0 = s0
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3

        # Normalization
        if normalization != NormalizationType.NONE:
            self.normalize(normalization)
            s0, s1, s2, s3 = self.as_array()

        # Intensity
        self.intensity = s0

        # Degree of polarization
        raw_dop = sqrt(s1 * s1 + s2 * s2 + s3 * s3) / s0
        self.degree_of_polarization = 0 if abs(raw_dop) < 1e-12 else min(1, max(0, raw_dop))

        # Orientation angle
        self.double_orientation_angle = 0
        if s1 == 0:
            self.double_orientation_angle = 0.5 * sign(s2) * pi
        elif s1 > 0:
            self.double_orientation_angle = arctan(s2 / s1)
        elif s2 == 0:
            self.double_orientation_angle = pi
        elif s2 > 0:
            self.double_orientation_angle = (arctan(s2 / s1) + pi)
        else:
            self.double_orientation_angle = (arctan(s2 / s1) - pi)

        # Ellipticity angle
        s1s2_normalization = sqrt(s1 * s1 + s2 * s2)
        if s1s2_normalization == 0:
            self.double_ellipticity_angle = 0.5 * sign(s3) * pi
        else:
            self.double_ellipticity_angle = arctan(s3 / sqrt(s1 * s1 + s2 * s2))

    def equals(self, other: "StokesVector"):
        return float_array_same(self.as_array(), other.as_array())

    def has_parameters(self, s0: float | int, s1: float | int, s2: float | int, s3: float | int):
        return float_array_same(self.as_array(), [s0, s1, s2, s3])

    def as_list(self):
        return [[self.clean(si)] for si in [self.s0, self.s1, self.s2, self.s3]]

    def as_vector(self):
        return array([[self.s0], [self.s1], [self.s2], [self.s3]])

    def as_array(self):
        return self.as_vector().flatten()

    def as_3d_array(self):
        return self.as_array()[1:]

    @staticmethod
    def clean(value):
        return 0.0 if abs(value) < 1e-12 else round(value, 12)

    def normalize(self, normalization: NormalizationType = NormalizationType.NONE):
        if normalization == NormalizationType.INTENSITY:
            self.s1, self.s2, self.s3 = self.as_3d_array() / self.s0
            self.s0 = 1
        elif normalization == NormalizationType.POINCARE_SPHERE:
            self.s0 = 1
            s_vec = self.as_3d_array()
            self.s1, self.s2, self.s3 = s_vec / norm(s_vec)
