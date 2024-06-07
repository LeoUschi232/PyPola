from PyPola.FiberNetworkComponents.Polarimeters.abstract_polarimeter import AbstractPolarimeter
from PyPola.FiberNetworkComponents.OpticalInstruments.linear_polarizer import LinearPolarizer
from PyPola.utilities.stokes_vector import StokesVector
from PyPola.utilities.general_utilities import progress_bar, same
from numpy import pi, linspace, cos, sin, sqrt, arccos


class SimplePolarimeter(AbstractPolarimeter):
    def __init__(self, number_of_rotations: int = 400):
        super().__init__()
        self.number_of_rotations = max([4, number_of_rotations])
        self.alphas = linspace(start=0, stop=pi, num=self.number_of_rotations)
        self.polarizer = LinearPolarizer(double_theta=0)

    def set_number_of_roations(self, number_of_rotations: int):
        self.number_of_rotations = max([4, number_of_rotations])
        self.alphas = linspace(start=-0.5 * pi, stop=0.5 * pi, num=self.number_of_rotations)

    def measure_stokes_parameters(self, input_stokes_vector: StokesVector):
        dop = input_stokes_vector.degree_of_polarization
        if not same(dop, 1):
            print(f"Simple polarimeter can only measure pure polarization states!")
            print(f"Cannot measure stokes vector with DOP: {dop}")
            return [0, 0, 0, 0]

        progress = progress_bar(
            nr_of_points=self.number_of_rotations,
            message="Measuring Stokes Parameters using Simple Polarization Analysis System"
        )

        lowest_intensity = input_stokes_vector.s0
        highest_intensity = 0
        highest_alpha = 0
        for alpha_i in self.alphas:
            self.polarizer.rotate(new_double_theta=2 * alpha_i)
            intensity = self.polarizer.pass_stokes_vector(input_stokes_vector).intensity

            if intensity < lowest_intensity:
                lowest_intensity = intensity
            if intensity > highest_intensity:
                highest_alpha = alpha_i
                highest_intensity = intensity
            progress.update()
        progress.close()

        # Now calculate the stokes parameters
        s0 = highest_intensity + lowest_intensity
        double_psi = 2 * highest_alpha
        double_xi = 2 * arccos(sqrt(highest_intensity / s0))
        s1 = s0 * cos(double_psi) * cos(double_xi)
        s2 = s0 * sin(double_psi) * cos(double_xi)
        abs_s3 = s0 * sin(double_xi)

        return self.print_and_return_parameters(
            computed_stokes_parameters=[s0, s1, s2, abs_s3],
            wavelength=input_stokes_vector.wavelength,
            dont_print=True
        )

    def instrument_name(self):
        return "Simple Polarimeter"
