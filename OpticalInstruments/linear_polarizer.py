from PyPola.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from numpy import cos, sin, array


class LinearPolarizer(AbstractOpticalInstrument):
    def __init__(self, double_theta: float | int = 0.0):
        super().__init__()
        self.double_theta = double_theta
        self.setup_mueller_matrix()

    def rotate(self, new_double_theta: float | int):
        self.double_theta = new_double_theta
        self.setup_mueller_matrix()

    def setup_mueller_matrix(self):
        cos_2a = cos(self.double_theta)
        sin_2a = sin(self.double_theta)

        raw_stokes_matrix = 0.5 * array([
            [1, cos_2a, sin_2a, 0],
            [cos_2a, cos_2a * cos_2a, cos_2a * sin_2a, 0],
            [sin_2a, cos_2a * sin_2a, sin_2a * sin_2a, 0],
            [0, 0, 0, 0]
        ])
        self.clean_mueller_matrix(raw_stokes_matrix)
