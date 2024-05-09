from PyPola.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from numpy import cos, sin, array


class MagnetoOpticRotator(AbstractOpticalInstrument):
    def __init__(self, angle_to_x_axis: float = 0.0):
        super().__init__()
        self.angle_to_x_axis = angle_to_x_axis
        self.setup_stokes_matrix()

    def rotate(self, new_angle_to_x_axis):
        self.angle_to_x_axis = new_angle_to_x_axis
        self.setup_stokes_matrix()

    def setup_stokes_matrix(self):
        cos_2a = cos(2 * self.angle_to_x_axis)
        sin_2a = sin(2 * self.angle_to_x_axis)

        raw_stokes_matrix = array([
            [1, 0, 0, 0],
            [0, cos_2a, sin_2a, 0],
            [0, -sin_2a, cos_2a, 0],
            [0, 0, 0, 1]
        ])
        self.clean_stokes_matrix(raw_stokes_matrix)
