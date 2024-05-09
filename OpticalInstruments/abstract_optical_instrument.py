from numpy import array
from PyPola.Utilities.general_utilities import same
from PyPola.Utilities.stokes_vector import StokesVector


class AbstractOpticalInstrument:
    def __init__(self):
        self.mueller_matrix = array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def setup_mueller_matrix(self):
        pass

    def clean_mueller_matrix(self, raw_mueller_matrix=None):
        if raw_mueller_matrix is None:
            raw_mueller_matrix = self.mueller_matrix
        self.mueller_matrix = array([
            [0.0 if same(value, 0) else float(value) for value in row]
            for row in raw_mueller_matrix
        ])

    def pass_stokes_vector(self, input_stokes_vector: StokesVector):
        s0, s1, s2, s3 = (self.mueller_matrix @ input_stokes_vector.as_vector()).flatten()
        return StokesVector(s0=s0, s1=s1, s2=s2, s3=s3)
