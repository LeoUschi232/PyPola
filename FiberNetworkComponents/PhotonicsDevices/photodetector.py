from PyPola.FiberNetworkComponents.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from PyPola.utilities.stokes_vector import StokesVector
from PyPola.utilities.general_utilities import same
from numpy import pi, sin, cos, array, arctan


class Photodetector(AbstractOpticalInstrument):
    def __init__(self, k: float = 1, rp: float = 0, rs: float = 0, delta: float = 0.5 * pi):
        super().__init__()

        # Proportionlity constant
        self.k = k
        if self.k < 0:
            self.print_bad_argument_error_message("k", 1)
            self.k = 1

        # Parallel intensity reflectance
        if not 0 <= rp <= 1:
            self.print_bad_argument_error_message("rp", 0)
            rp = 0

        # Perpendicular intensity reflectance
        if not 0 <= rs <= 1:
            self.print_bad_argument_error_message("rs", 0)
            rs = 0

        # Phase shift difference beween incident polarization orientations
        self.delta = delta
        if not 0 <= self.delta <= 2 * pi:
            self.print_bad_argument_error_message("delta", "pi/2")
            self.psi = 0.5 * pi

        # Parallel intensity reflectance and average surface reflectance
        if same(rp, 0):
            self.psi = 0.0
        elif same(rs, 0):
            self.psi = 0.5 * pi
        else:
            self.psi = arctan(rp / rs)
        if same(rp, 0) and same(rs, 0):
            self.r = 0
        else:
            self.r = 0.5 * (rp * rp + rs * rs)
        self.setup_mueller_matrix()
        self.photocurrent = 0.0

    def setup_mueller_matrix(self):
        cos_2psi, sin_2psi = [(cos(x), sin(x)) for x in [2 * self.psi]][0]
        cos_d = cos(self.delta)
        sin_d = sin(self.delta)
        self.mueller_matrix = self.r * array([
            [1, -cos_2psi, 0, 0],
            [-cos_2psi, 1, 0, 0],
            [0, 0, sin_2psi * cos_d, sin_2psi * sin_d],
            [0, 0, -sin_2psi * sin_d, sin_2psi * cos_d]
        ])

    def pass_stokes_vector(self, input_stokes_vector: StokesVector):
        output_stokes_vector = super().pass_stokes_vector(input_stokes_vector)
        self.photocurrent = self.k * (input_stokes_vector.s0 - output_stokes_vector.s0)
        return output_stokes_vector

    def instrument_name(self):
        return "Photodetector"
