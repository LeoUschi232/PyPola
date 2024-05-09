from PyPola.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from enum import Enum
from numpy import pi, cos, sin


class WaveplateType(Enum):
    QUARTER = 1
    HALF = 2
    MODIFIABLE = 3


class PolarizationWaveplate(AbstractOpticalInstrument):
    def __init__(
            self, waveplate_type: WaveplateType = WaveplateType.MODIFIABLE,
            double_theta: float = 0.0,
            delta: float = 0.0
    ):
        super().__init__()
        self.waveplate_type = waveplate_type
        self.double_theta = double_theta
        self.delta = delta

        # Overwrite phase shift if waveplate type is quarter or half
        if waveplate_type == WaveplateType.QUARTER:
            self.delta = pi / 2
        elif waveplate_type == WaveplateType.HALF:
            self.delta = pi

        self.stokes_matrix = None
        self.setup_stokes_matrix()

    def setup_stokes_matrix(self):
        cos_2t = cos(self.double_theta)
        sin_2t = sin(self.double_theta)
        cos_d = cos(self.delta)
        sin_d = sin(self.delta)

        if self.waveplate_type == WaveplateType.QUARTER:
            raw_stokes_matrix = [
                [1, 0, 0, 0],
                [0, cos_2t * cos_2t, cos_2t * sin_2t, sin_2t],
                [0, cos_2t * sin_2t, sin_2t * sin_2t, -cos_2t],
                [0, -sin_2t, cos_2t, 0]
            ]
        elif self.waveplate_type == WaveplateType.HALF:
            raw_stokes_matrix = [
                [1, 0, 0, 0],
                [0, cos_2t * cos_2t - sin_2t * sin_2t, 2 * cos_2t * sin_2t, 0],
                [0, 2 * cos_2t * sin_2t, sin_2t * sin_2t - cos_2t * cos_2t, 0],
                [0, 0, 0, -1]
            ]
        else:
            raw_stokes_matrix = [
                [1, 0, 0, 0],
                [0, cos_2t * cos_2t + sin_2t * sin_2t * cos_d, cos_2t * sin_2t * (1 - cos_d), sin_2t * sin_d],
                [0, cos_2t * sin_2t * (1 - cos_d), cos_2t * cos_2t * cos_d + sin_2t * sin_2t, -cos_2t * sin_d],
                [0, -sin_2t * sin_d, cos_2t * sin_d, cos_d]
            ]
        self.clean_stokes_matrix(raw_stokes_matrix)

    def rotate(self, new_double_theta: float):
        self.double_theta = new_double_theta
        self.setup_stokes_matrix()

    def modify(self, new_delta: float):
        if self.waveplate_type != WaveplateType.MODIFIABLE:
            print("Cannot modify none-modifiable waveplate")
            return

        self.delta = new_delta
        self.setup_stokes_matrix()

    @staticmethod
    def convert_x_axis_angle_to_double_theta(x_axis_angle):
        return 2 * (x_axis_angle + pi / 2)
