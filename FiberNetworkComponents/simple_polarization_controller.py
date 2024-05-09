from PyPola.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from PyPola.Utilities.general_utilities import same, get_4x4_unit_matrix, sgn
from numpy import array, sqrt
from numpy.linalg import norm


class SimplePolarizationController(AbstractOpticalInstrument):
    def __init__(self, input_stokes_vector=None, output_stokes_vector=None):
        super().__init__()
        if input_stokes_vector is None:
            input_stokes_vector = [[1], [1], [0], [0]]
        if output_stokes_vector is None:
            output_stokes_vector = [[1], [1], [0], [0]]

        self.input_stokes_vector = input_stokes_vector
        self.output_stokes_vector = output_stokes_vector
        if not same(output_stokes_vector[3][0], 0):
            print(f"ERROR!")
            print(f"Simple polarization controller cannot synthesize all states of polarization!")
            z = array(output_stokes_vector).flatten()
            z[3] = 0
            z = z / norm(z)
            self.output_stokes_vector = [[zi] for zi in z]
            print(f"Defaulting to synthesis onto polarization:\n{self.output_stokes_vector}\n")

        self.setup_stokes_matrix()

    def setup_stokes_matrix(self):
        _, s1, s2, s3 = [si[0] for si in self.input_stokes_vector]
        _, z1, z2, _ = [zi[0] for zi in self.output_stokes_vector]

        # If the vectors are the same, no change is necessary
        if same(s1, z1) and same(s2, z2) and same(s3, 0):
            self.stokes_matrix = get_4x4_unit_matrix()
            return

        # First matrix is the rotation of the input vector onto the s1s2-plane
        # This can be done by using a quarterwaveplate with its rotation axis right beneath the input vector
        r_vec = array([s1, s2, 0])
        r_vec = r_vec / norm(r_vec)
        cos_2t, sin_2t, _ = r_vec
        qwp_stokes_matrix = array([
            [1, 0, 0, 0],
            [0, cos_2t * cos_2t, cos_2t * sin_2t, sin_2t],
            [0, cos_2t * sin_2t, sin_2t * sin_2t, -cos_2t],
            [0, -sin_2t, cos_2t, 0]
        ])

        # The second matrix is obtained by rotating the state of polarization which is now on the s1s2-plane
        # over the angle of pi onto the desired output polarization
        # This can be accomplished by choosing the rotation axis for the halfwaveplate to be the vector
        # exactly halfway between the second state of polarization and the output polarization
        normalization = sqrt(s1 * s1 + s2 * s2)
        s_new = array([s1 + s2 * s3 / normalization, s2 - s1 * s3 / normalization, 0])
        r_vec = array([s1 + s2 * s3 / normalization + z1, s2 - s1 * s3 / normalization + z2, 0])
        r_vec = r_vec / norm(r_vec)
        cos_2t, sin_2t, _ = r_vec
        hwp_stokes_matrix = array([
            [1, 0, 0, 0],
            [0, cos_2t * cos_2t - sin_2t * sin_2t, 2 * cos_2t * sin_2t, 0],
            [0, 2 * cos_2t * sin_2t, sin_2t * sin_2t - cos_2t * cos_2t, 0],
            [0, 0, 0, -1]
        ])

        # The final matrix is the application of the quarterwaveplate matrix from the left first
        # and the halfwaveplate matrix from the left afterward
        self.clean_stokes_matrix(hwp_stokes_matrix @ qwp_stokes_matrix)

    def reconfigure_polarization_transformation(self, input_stokes_vector=None, output_stokes_vector=None):
        if input_stokes_vector is not None:
            if output_stokes_vector is not None:
                self.output_stokes_vector = output_stokes_vector
            self.input_stokes_vector = input_stokes_vector
        elif output_stokes_vector is not None:
            self.output_stokes_vector = output_stokes_vector
        else:
            return
        if not same(self.output_stokes_vector[3][0], 0):
            print(f"ERROR!")
            print(f"Simple polarization controller cannot synthesize all states of polarization!")
            z = array(self.output_stokes_vector[1:]).flatten()
            z[2] = 0
            z = z / norm(z)
            self.output_stokes_vector = [1, z[0], z[1], 0]
            print(f"Defaulting to synthesis onto polarization:\n{self.output_stokes_vector}\n")
        self.setup_stokes_matrix()
