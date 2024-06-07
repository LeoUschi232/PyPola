from PyPola.FiberNetworkComponents.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from PyPola.utilities.stokes_vector import StokesVector


class AbstractPolarimeter(AbstractOpticalInstrument):
    def __init__(self):
        super().__init__()

    def measure_stokes_parameters(self, input_stokes_vector: StokesVector):
        pass

    @staticmethod
    def print_and_return_parameters(computed_stokes_parameters, dont_print=False):
        if dont_print:
            return computed_stokes_parameters
        print("Measurement results")
        print("S0:", computed_stokes_parameters[0])
        print("S1:", computed_stokes_parameters[1])
        print("S2:", computed_stokes_parameters[2])
        print("S3:", computed_stokes_parameters[3])
        return computed_stokes_parameters
