from PyPola.FiberNetworkComponents.PolarizationControllers.abstract_polarization_controller import (
    AbstractPolarizationController
)
from PyPola.utilities.stokes_vector import StokesVector
from PyPola.utilities.general_utilities import same, get_4x4_unit_matrix, sgn
from numpy import array, sqrt


class VariableRetardationPolarizationController(AbstractPolarizationController):
    def __init__(
            self,
            input_stokes_vector: StokesVector = None,
            output_stokes_vector: StokesVector = None,
            response_time: int = 1
    ):
        super().__init__(input_stokes_vector, output_stokes_vector, response_time)

    def setup_mueller_matrix(self):
        s1, s2, s3 = self.input_stokes_vector.as_3d_array()
        z1, z2, z3 = self.output_stokes_vector.as_3d_array()

        # If the vectors are the same, no change is necessary
        if same(s1, z1) and same(s2, z2) and same(s3, z3):
            self.setup_adjustment_matrix(new_required_matrix=get_4x4_unit_matrix())
            return

        # Rotation onto the S1S3-plane
        sqrt_s2s3 = sqrt(s2 * s2 + s3 * s3)
        if s2 == 0:
            cos_d1, sin_d1 = 1, 0
        else:
            cos_d1 = sgn(s2) * s3 / sqrt_s2s3
            sin_d1 = abs(s2) / sqrt_s2s3
        fiber_squeezer_1 = array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, cos_d1, -sin_d1],
            [0, 0, sin_d1, cos_d1]
        ])
        s2, s3 = 0, sin_d1 * s2 + cos_d1 * s3

        # Rotation onto the S3-axis
        sqrt_s1s3 = sqrt(s1 * s1 + s3 * s3)
        if s1 == 0:
            cos_d2, sin_d2 = 1, 0
        else:
            cos_d2 = -sgn(s1) * s3 / sqrt_s1s3
            sin_d2 = abs(s1) / sqrt_s1s3
        fiber_squeezer_2 = array([
            [1, 0, 0, 0],
            [0, cos_d2, 0, sin_d2],
            [0, 0, 1, 0],
            [0, -sin_d2, 0, cos_d2]
        ])
        s2, s3 = 0, -sgn(s1)

        # Rotation into the z-plane
        if z2 == 0.0:
            cos_d3, sin_d3 = 1, 0
        else:
            cos_d3 = -sgn(z2) * sgn(s3) * sqrt(1 - z2 * z2)
            sin_d3 = -sgn(s3) * z2
        fiber_squeezer_3 = array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, cos_d3, -sin_d3],
            [0, 0, sin_d3, cos_d3]
        ])
        s2, s3 = -sin_d3 * s3, cos_d3 * s3

        # Rotation onto z
        sqrt_z1z3 = sqrt(z1 * z1 + z3 * z3)
        if z1 == 0.0:
            cos_d4, sin_d4 = sgn(s3) * sgn(z3), 0
        else:
            cos_d4 = sgn(s3) * z3 / sqrt_z1z3
            sin_d4 = sgn(s3) * z1 / sqrt_z1z3
        fiber_squeezer_4 = array([
            [1, 0, 0, 0],
            [0, cos_d4, 0, sin_d4],
            [0, 0, 1, 0],
            [0, -sin_d4, 0, cos_d4]
        ])

        # Complete the full matrix
        required_matrix = fiber_squeezer_4 @ fiber_squeezer_3 @ fiber_squeezer_2 @ fiber_squeezer_1
        self.setup_adjustment_matrix(new_required_matrix=required_matrix)

    def instrument_name(self):
        return "Fiber Squeezer Polarization Controller"
