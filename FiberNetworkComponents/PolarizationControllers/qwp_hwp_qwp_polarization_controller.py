from PyPola.FiberNetworkComponents.PolarizationControllers.abstract_polarization_controller import (
    AbstractPolarizationController
)
from PyPola.utilities.stokes_vector import StokesVector
from PyPola.utilities.general_utilities import same, get_4x4_unit_matrix, normalize
from numpy import array, sqrt


class QwpHwpQwpPolarizationController(AbstractPolarizationController):

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

        # The commprehensive derivation of the rotation vectors can be found in the docs
        r_qwp1 = normalize([s1, s2, 0])
        r_qwp2 = normalize([z1, z2, 0])

        s1s2_normalization = sqrt(s1 * s1 + s2 * s2)
        z1z2_normalization = sqrt(z1 * z1 + z2 * z2)
        r_hwp = normalize([
            s1 + s2 * s3 / s1s2_normalization + z1 - z2 * z3 / z1z2_normalization,
            s2 - s1 * s3 / s1s2_normalization + z2 + z1 * z3 / z1z2_normalization,
            0
        ])

        cos_2t, sin_2t, _ = r_qwp1
        qwp1_stokes_matrix = array([
            [1, 0, 0, 0],
            [0, cos_2t * cos_2t, cos_2t * sin_2t, sin_2t],
            [0, cos_2t * sin_2t, sin_2t * sin_2t, -cos_2t],
            [0, -sin_2t, cos_2t, 0]
        ])
        cos_2t, sin_2t, _ = r_hwp
        hwp_stokes_matrix = array([
            [1, 0, 0, 0],
            [0, cos_2t * cos_2t - sin_2t * sin_2t, 2 * cos_2t * sin_2t, 0],
            [0, 2 * cos_2t * sin_2t, sin_2t * sin_2t - cos_2t * cos_2t, 0],
            [0, 0, 0, -1]
        ])
        cos_2t, sin_2t, _ = r_qwp2
        qwp2_stokes_matrix = array([
            [1, 0, 0, 0],
            [0, cos_2t * cos_2t, cos_2t * sin_2t, sin_2t],
            [0, cos_2t * sin_2t, sin_2t * sin_2t, -cos_2t],
            [0, -sin_2t, cos_2t, 0]
        ])

        required_matrix = qwp2_stokes_matrix @ hwp_stokes_matrix @ qwp1_stokes_matrix
        self.setup_adjustment_matrix(new_required_matrix=required_matrix)

    def instrument_name(self):
        return "QWP-HWP-QWP Polarization Controller"
