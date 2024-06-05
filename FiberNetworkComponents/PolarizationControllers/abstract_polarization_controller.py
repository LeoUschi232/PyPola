from PyPola.FiberNetworkComponents.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from PyPola.utilities.stokes_vector import StokesVector
from numpy import pi

half_pi = 0.5 * pi


class AbstractPolarizationController(AbstractOpticalInstrument):
    def __init__(
            self,
            input_stokes_vector: StokesVector = None,
            output_stokes_vector: StokesVector = None
    ):
        super().__init__()
        if output_stokes_vector is None:
            output_stokes_vector = StokesVector(s0=1, s1=1, s2=0, s3=0)
        if input_stokes_vector is None:
            input_stokes_vector = StokesVector(s0=1, s1=1, s2=0, s3=0)
        self.input_stokes_vector = input_stokes_vector
        self.output_stokes_vector = output_stokes_vector
        self.setup_mueller_matrix()

    def setup_mueller_matrix(self):
        pass

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
