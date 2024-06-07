from PyPola.FiberNetworkComponents.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from PyPola.utilities.stokes_vector import StokesVector
from numpy import array, cos, sin


class PolarizationBeamSplitter(AbstractOpticalInstrument):
    def __init__(self, transmission_double_theta: float = 0.0):
        super().__init__()
        self.transmission_double_theta = transmission_double_theta
        self.transmission_mueller_matrix = None
        self.reflection_mueller_matrix = None
        self.setup_mueller_matrix()

    def rotate(self, new_transmission_double_theta: float = 0.0):
        self.transmission_double_theta = new_transmission_double_theta
        self.setup_mueller_matrix()

    def setup_mueller_matrix(self):
        cos_2t = cos(self.transmission_double_theta)
        sin_2t = sin(self.transmission_double_theta)
        self.transmission_mueller_matrix = 0.5 * array([
            [1, cos_2t, sin_2t, 0],
            [cos_2t, cos_2t * cos_2t, cos_2t * sin_2t, 0],
            [sin_2t, cos_2t * sin_2t, sin_2t * sin_2t, 0],
            [0, 0, 0, 0]
        ])

        cos_2t = -sin(self.transmission_double_theta)
        sin_2t = cos(self.transmission_double_theta)
        self.reflection_mueller_matrix = 0.5 * array([
            [1, cos_2t, sin_2t, 0],
            [cos_2t, cos_2t * cos_2t, cos_2t * sin_2t, 0],
            [sin_2t, cos_2t * sin_2t, sin_2t * sin_2t, 0],
            [0, 0, 0, 0]
        ])

    def pass_stokes_vector(self, input_stokes_vector: StokesVector):
        ts0, ts1, ts2, ts3 = (self.transmission_mueller_matrix @ input_stokes_vector.as_vector()).flatten()
        rs0, rs1, rs2, rs3 = (self.reflection_mueller_matrix @ input_stokes_vector.as_vector()).flatten()
        return StokesVector(ts0, ts1, ts2, ts3), StokesVector(rs0, rs1, rs2, rs3)

    def instrument_name(self):
        return "Polarization Mueller Matrix"
