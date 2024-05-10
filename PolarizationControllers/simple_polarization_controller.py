from PyPola.PolarizationControllers.abstract_polarization_controller import AbstractPolarizationController
from PyPola.Utilities.stokes_vector import StokesVector, NormalizationType
from PyPola.Utilities.general_utilities import same, get_4x4_unit_matrix, normalize_and_clean
from numpy import array, sqrt


class SimplePolarizationController(AbstractPolarizationController):
    def __init__(self, input_stokes_vector: StokesVector = None, output_stokes_vector: StokesVector = None):
        super().__init__(input_stokes_vector, output_stokes_vector)

    def setup_mueller_matrix(self):
        self.fix_output_stokes_vector()
        s1, s2, s3 = self.input_stokes_vector.as_3d_array()
        z1, z2, _ = self.output_stokes_vector.as_3d_array()

        # If the vectors are the same, no change is necessary
        if same(s1, z1) and same(s2, z2) and same(s3, 0):
            self.mueller_matrix = get_4x4_unit_matrix()
            return

        # The First matrix is the rotation of the input vector onto the s1s2-plane
        # This can be done by using a quarterwaveplate with its rotation axis right beneath the input vector
        r_vec = normalize_and_clean([s1, s2, 0])
        cos_2t, sin_2t, _ = r_vec
        qwp_stokes_matrix = array([
            [1, 0, 0, 0],
            [0, cos_2t * cos_2t, cos_2t * sin_2t, sin_2t],
            [0, cos_2t * sin_2t, sin_2t * sin_2t, -cos_2t],
            [0, -sin_2t, cos_2t, 0]
        ])

        # The second matrix is obtained by rotating the state of polarization which is now on the s1s2-plane
        # over the angle of pi onto the desired output polarization.
        # This can be achieved by choosing the rotation axis for the halfwaveplate to be the vector
        # exactly halfway between the second state of polarization and the output polarization.
        normalization = sqrt(s1 * s1 + s2 * s2)
        r_vec = normalize_and_clean([s1 + s2 * s3 / normalization + z1, s2 - s1 * s3 / normalization + z2, 0])
        cos_2t, sin_2t, _ = r_vec
        hwp_stokes_matrix = array([
            [1, 0, 0, 0],
            [0, cos_2t * cos_2t - sin_2t * sin_2t, 2 * cos_2t * sin_2t, 0],
            [0, 2 * cos_2t * sin_2t, sin_2t * sin_2t - cos_2t * cos_2t, 0],
            [0, 0, 0, -1]
        ])

        # The final matrix is the application of the quarterwaveplate matrix from the left first
        # and the halfwaveplate matrix from the left afterward
        self.clean_mueller_matrix(hwp_stokes_matrix @ qwp_stokes_matrix)

    def fix_output_stokes_vector(self):
        if not same(self.output_stokes_vector.s3, 0):
            print(f"ERROR! Simple polarization controller cannot synthesize all states of polarization!")
            self.output_stokes_vector.s3 = 0
            self.output_stokes_vector.normalize(NormalizationType.POINCARE_SPHERE)
            print(f"Defaulting to synthesis onto polarization: {self.output_stokes_vector.as_list()}\n")
