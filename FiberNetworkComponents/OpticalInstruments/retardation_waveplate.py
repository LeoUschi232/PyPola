from PyPola.FiberNetworkComponents.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from enum import Enum
from numpy import pi, array, cos, sin


class WaveplateType(Enum):
    QUARTER = 1
    HALF = 2
    MODIFIABLE = 3


class RetardationWaveplate(AbstractOpticalInstrument):
    def __init__(
            self, waveplate_type: WaveplateType = WaveplateType.MODIFIABLE,
            double_theta: float = 0.0,
            delta: float = 0.0
    ):
        super().__init__()
        self.waveplate_type = waveplate_type
        self.double_theta = double_theta
        self.delta = delta

        # Overwrite phase shift if the waveplate type is quarter or half
        if waveplate_type == WaveplateType.QUARTER:
            self.delta = 0.5 * pi
        elif waveplate_type == WaveplateType.HALF:
            self.delta = pi

        self.stokes_matrix = None
        self.setup_mueller_matrix()

    def setup_mueller_matrix(self):
        cos_2t = cos(self.double_theta)
        sin_2t = sin(self.double_theta)
        cos_d = cos(self.delta)
        sin_d = sin(self.delta)

        if self.waveplate_type == WaveplateType.QUARTER:
            self.mueller_matrix = array([
                [1, 0, 0, 0],
                [0, cos_2t * cos_2t, cos_2t * sin_2t, sin_2t],
                [0, cos_2t * sin_2t, sin_2t * sin_2t, -cos_2t],
                [0, -sin_2t, cos_2t, 0]
            ])
            return
        if self.waveplate_type == WaveplateType.HALF:
            self.mueller_matrix = array([
                [1, 0, 0, 0],
                [0, cos_2t * cos_2t - sin_2t * sin_2t, 2 * cos_2t * sin_2t, 0],
                [0, 2 * cos_2t * sin_2t, sin_2t * sin_2t - cos_2t * cos_2t, 0],
                [0, 0, 0, -1]
            ])
            return
        self.mueller_matrix = array([
            [1, 0, 0, 0],
            [0, cos_2t * cos_2t + sin_2t * sin_2t * cos_d, cos_2t * sin_2t * (1 - cos_d), sin_2t * sin_d],
            [0, cos_2t * sin_2t * (1 - cos_d), cos_2t * cos_2t * cos_d + sin_2t * sin_2t, -cos_2t * sin_d],
            [0, -sin_2t * sin_d, cos_2t * sin_d, cos_d]
        ])

    def rotate(self, new_double_theta: float):
        self.double_theta = new_double_theta
        self.setup_mueller_matrix()

    def modify(self, new_delta: float):
        if self.waveplate_type != WaveplateType.MODIFIABLE:
            print("Cannot modify none-modifiable waveplate")
            return

        self.delta = new_delta
        self.setup_mueller_matrix()

    def instrument_name(self):
        return "Retardation Waveplate"

    @staticmethod
    def convert_x_axis_angle_to_double_theta(x_axis_angle):
        return 2 * (x_axis_angle + 0.5 * pi)
