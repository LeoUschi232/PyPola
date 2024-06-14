from PyPola.FiberNetworkComponents.PolarizationControllers.abstract_polarization_controller import (
    AbstractPolarizationController
)
from PyPola.utilities.stokes_vector import StokesVector
from PyPola.utilities.general_utilities import same, float_array_same, get_4x4_unit_matrix, sgn, normalize
from numpy import array, sqrt, dot, sign, cross
from numpy.linalg import norm


class DeltaWaveplatePolarizationController(AbstractPolarizationController):
    def __init__(
            self,
            input_stokes_vector: StokesVector = None,
            output_stokes_vector: StokesVector = None,
            response_time: int = 1
    ):
        super().__init__(input_stokes_vector, output_stokes_vector, response_time)

    def setup_mueller_matrix(self):
        expected_z = self.output_stokes_vector.as_array()
        _, s1, s2, s3 = self.input_stokes_vector.as_array()
        _, z1, z2, z3 = expected_z
        s_vec = self.input_stokes_vector.as_3d_array()
        z_vec = self.output_stokes_vector.as_3d_array()

        # Case 1 out of 3
        # If the vectors are the same, no change is necessary
        if float_array_same(s_vec, z_vec):
            self.setup_adjustment_matrix(new_required_matrix=get_4x4_unit_matrix())
            return

        # Case 2 out of 3
        # The simple delta case described in the docs
        if same(s2, z2) and same(s1, z1):
            square_normalizer = s1 * s1 + s2 * s2
            a = (s1 * s1 - s2 * s2) / square_normalizer
            b = (2 * s1 * s2) / square_normalizer
            required_matrix = array([
                [1, 0, 0, 0],
                [0, a, b, 0],
                [0, b, -a, 0],
                [0, 0, 0, -1]
            ])
            self.setup_adjustment_matrix(new_required_matrix=required_matrix)
            return

        # Case 3 out of 3
        # Now it is no longer relevant if possibly some vectors are the same
        # because the additional cases don't require edge-case computation and would only result in useless extra code
        r_vec = normalize(sgn(z2 - s2) * array([z2 - s2, s1 - z1, 0]))
        cos_2t, sin_2t, _ = r_vec

        # The term for the cos(delta) will hold up because the dot product of the 2 helping vectors can be negative.
        # However, even after computing cos(delta), there is still ambiguity as to the sign of sin(delta)
        # The correct sign for sin(delta) is positive if the rotation axis and the cross product of the 2 assisting
        # vectors are pointing in the same direction and negative if they are pointing in opposite directions
        s_extra = s_vec - dot(s_vec, r_vec) * r_vec
        z_extra = z_vec - dot(z_vec, r_vec) * r_vec

        # The following 2 variables could be collapsed into one expression but are kept
        # such that their value can be assessed during debugging
        rotation_vector = normalize(cross(s_extra, z_extra))
        direction_sign = sign(dot(rotation_vector, r_vec))

        cos_d = dot(s_extra, z_extra) / (norm(s_extra) * norm(z_extra))
        sin_d = direction_sign * sqrt(1 - cos_d * cos_d)
        required_matrix = array([
            [1, 0, 0, 0],
            [0, cos_2t * cos_2t + sin_2t * sin_2t * cos_d, cos_2t * sin_2t * (1 - cos_d), sin_2t * sin_d],
            [0, cos_2t * sin_2t * (1 - cos_d), cos_2t * cos_2t * cos_d + sin_2t * sin_2t, -cos_2t * sin_d],
            [0, -sin_2t * sin_d, cos_2t * sin_d, cos_d]
        ])
        self.setup_adjustment_matrix(new_required_matrix=required_matrix)

    def instrument_name(self):
        return "LiNbO3 Polarization Controller"
