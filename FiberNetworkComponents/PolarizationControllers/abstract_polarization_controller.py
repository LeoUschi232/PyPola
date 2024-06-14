from PyPola.FiberNetworkComponents.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from PyPola.utilities.stokes_vector import StokesVector
from PyPola.utilities.general_utilities import minabs, get_4x4_unit_matrix


class AbstractPolarizationController(AbstractOpticalInstrument):
    def __init__(
            self,
            input_stokes_vector: StokesVector = None,
            output_stokes_vector: StokesVector = None,
            response_time: int = 1
    ):
        super().__init__()
        if output_stokes_vector is None:
            output_stokes_vector = StokesVector(s0=1, s1=1, s2=0, s3=0)
        if input_stokes_vector is None:
            input_stokes_vector = StokesVector(s0=1, s1=1, s2=0, s3=0)
        self.input_stokes_vector = input_stokes_vector
        self.output_stokes_vector = output_stokes_vector

        # The response time is given as a multiple of 250 nanoseconds
        # because PolaFlex maximum measurement speed is 4000000 Hz
        self.response_time = abs(response_time)
        self.adjustment_steps_left = self.response_time + 1
        self.adjustment_step = 1 / self.adjustment_steps_left
        self.adjustment_matrix = get_4x4_unit_matrix()
        self.setup_mueller_matrix()

    def setup_adjustment_matrix(self, new_required_matrix):
        self.adjustment_steps_left = self.response_time + 1
        self.adjustment_matrix = self.adjustment_step * (new_required_matrix - self.mueller_matrix)

    def reconfigure_polarization_transformation(
            self,
            input_stokes_vector: StokesVector = None,
            output_stokes_vector: StokesVector = None
    ):
        if input_stokes_vector is not None:
            if output_stokes_vector is not None:
                self.output_stokes_vector = output_stokes_vector
            self.input_stokes_vector = input_stokes_vector
        elif output_stokes_vector is not None:
            self.output_stokes_vector = output_stokes_vector
        else:
            return
        self.setup_mueller_matrix()

    def pass_stokes_vector(self, input_stokes_vector: StokesVector):
        if self.adjustment_steps_left <= 0:
            return super().pass_stokes_vector(input_stokes_vector)

        self.adjustment_steps_left -= 1
        self.mueller_matrix = self.mueller_matrix + self.adjustment_matrix
        return super().pass_stokes_vector(input_stokes_vector)
