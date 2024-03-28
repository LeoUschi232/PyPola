from OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from enum import Enum
from numpy import pi, cos, sin


class WaveplateType(Enum):
    QUARTER = 1
    HALF = 2
    MODIFIABLE = 3


class PolarizationWaveplate(AbstractOpticalInstrument):
    def __init__(
            self, waveplate_type: WaveplateType = WaveplateType.MODIFIABLE,
            angle_to_x_axis: float = 0.0,
            phase_shift: float = 0.0
    ):
        super().__init__()
        self.waveplate_type = waveplate_type
        self.angle_to_fast_axis = angle_to_x_axis + pi / 2
        self.phase_shift = phase_shift

        # Overwrite phase shift if waveplate type is quarter or half
        if waveplate_type == WaveplateType.QUARTER:
            self.phase_shift = pi / 2
        elif waveplate_type == WaveplateType.HALF:
            self.phase_shift = pi

        self.stokes_matrix = None
        self.setup_stokes_matrix()

    def setup_stokes_matrix(self):
        cos_2a = cos(2 * self.angle_to_fast_axis)
        sin_2a = sin(2 * self.angle_to_fast_axis)
        cos_d = cos(self.phase_shift)
        sin_d = sin(self.phase_shift)

        if self.waveplate_type == WaveplateType.QUARTER:
            raw_stokes_matrix = [
                [1, 0, 0, 0],
                [0, cos_2a * cos_2a, cos_2a * sin_2a, sin_2a],
                [0, cos_2a * sin_2a, sin_2a * sin_2a, -cos_2a],
                [0, -sin_2a, cos_2a, 0]
            ]
        elif self.waveplate_type == WaveplateType.HALF:
            raw_stokes_matrix = [
                [1, 0, 0, 0],
                [0, cos_2a * cos_2a - sin_2a * sin_2a, 2 * cos_2a * sin_2a, 0],
                [0, 2 * cos_2a * sin_2a, sin_2a * sin_2a - cos_2a * cos_2a, 0],
                [0, 0, 0, -1]
            ]
        else:
            raw_stokes_matrix = [
                [1, 0, 0, 0],
                [0, cos_2a * cos_2a + sin_2a * sin_2a * cos_d, cos_2a * sin_2a * (1 - cos_d), sin_2a * sin_d],
                [0, cos_2a * sin_2a * (1 - cos_d), cos_2a * cos_2a * cos_d + sin_2a * sin_2a, -cos_2a * sin_d],
                [0, -sin_2a * sin_d, cos_2a * sin_d, cos_d]
            ]
        self.clean_stokes_matrix(raw_stokes_matrix)

    def rotate(self, new_angle_to_x_axis: float):
        self.angle_to_fast_axis = new_angle_to_x_axis + pi / 2
        self.setup_stokes_matrix()

    def modify(self, new_phase_shift: float):
        if self.waveplate_type != WaveplateType.MODIFIABLE:
            print("Cannot modify none-modifiable waveplate")
            return

        self.phase_shift = new_phase_shift
        self.setup_stokes_matrix()
