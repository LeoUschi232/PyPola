from PyPola.FiberNetworkComponents.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from PyPola.utilities.stokes_vector import StokesVector


class AbstractPolarimeter(AbstractOpticalInstrument):
    def __init__(self):
        super().__init__()

    def measure_stokes_vector(self, input_stokes_vector: StokesVector):
        pass

    @staticmethod
    def print_and_return_stokes_vector(computed_stokes_parameters, wavelength, dont_print=False):
        if dont_print:
            return StokesVector(*computed_stokes_parameters, wavelength)
        print("Measurement results")
        print("S0:", computed_stokes_parameters[0])
        print("S1:", computed_stokes_parameters[1])
        print("S2:", computed_stokes_parameters[2])
        print("S3:", computed_stokes_parameters[3])
        return StokesVector(*computed_stokes_parameters, wavelength)
