from PyPola.FiberNetworkComponents.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from numpy import cos, sin, array


class MagnetoOpticRotator(AbstractOpticalInstrument):
    def __init__(self, double_theta: float = 0.0):
        super().__init__()
        self.double_theta = double_theta
        self.setup_mueller_matrix()

    def rotate(self, new_double_theta: float = 0.0):
        self.double_theta = new_double_theta
        self.setup_mueller_matrix()

    def setup_mueller_matrix(self):
        cos_2t = cos(self.double_theta)
        sin_2t = sin(self.double_theta)

        self.mueller_matrix = array([
            [1, 0, 0, 0],
            [0, cos_2t, sin_2t, 0],
            [0, -sin_2t, cos_2t, 0],
            [0, 0, 0, 1]
        ])

    def instrument_name(self):
        return "Magnetooptic Rotator"
