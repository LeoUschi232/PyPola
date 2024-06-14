from PyPola.utilities.stokes_vector import StokesVector, round_p
from PyPola.utilities.general_utilities import get_4x4_unit_matrix
from numpy import array


class AbstractOpticalInstrument:
    def __init__(self):
        self.mueller_matrix = get_4x4_unit_matrix()

    def setup_mueller_matrix(self):
        pass

    def pass_stokes_vector(self, input_stokes_vector: StokesVector):
        s0, s1, s2, s3 = (self.mueller_matrix @ input_stokes_vector.as_vector()).flatten()
        return StokesVector(s0, s1, s2, s3)

    def print_mueller_matrix(self):
        print(str(array([[round_p(value) for value in mueller_row] for mueller_row in self.mueller_matrix])))

    def print_bad_argument_error_message(self, argument_name, default_value):
        print(f"ERROR!")
        print(f"Attempted to pass bad argument for {argument_name} to {self.instrument_name()}!")
        print(f"Defaulting to {argument_name}={default_value}...\n")

    def __repr__(self):
        return str([[round_p(value) for value in mueller_row] for mueller_row in self.mueller_matrix])

    def __str__(self):
        return str(array([[round_p(value) for value in mueller_row] for mueller_row in self.mueller_matrix]))

    def instrument_name(self):
        pass
