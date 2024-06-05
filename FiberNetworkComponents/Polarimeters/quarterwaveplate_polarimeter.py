from PyPola.FiberNetworkComponents.Polarimeters.abstract_polarimeter import AbstractPolarimeter
from PyPola.FiberNetworkComponents.OpticalInstruments.polarization_waveplate import PolarizationWaveplate, WaveplateType
from PyPola.FiberNetworkComponents.OpticalInstruments.linear_polarizer import LinearPolarizer
from PyPola.utilities.stokes_vector import StokesVector
from PyPola.utilities.general_utilities import progress_bar
from numpy import pi, linspace, cos, sin
from time import sleep


class QuarterwavelatePolarimeter(AbstractPolarimeter):
    def __init__(self, number_of_rotations: int = 400):
        super().__init__()
        self.number_of_rotations = max([4, number_of_rotations])
        self.betas = linspace(start=0, stop=pi, num=self.number_of_rotations)
        self.quarterwaveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER, double_theta=0)
        self.polarizer = LinearPolarizer(double_theta=0.5 * pi)

    def set_number_of_roations(self, number_of_rotations: int):
        self.number_of_rotations = max([4, number_of_rotations])
        self.betas = linspace(start=0, stop=pi, num=self.number_of_rotations)

    def measure_stokes_parameters(self, input_stokes_vector: StokesVector):
        output_intensities = []
        progress = progress_bar(
            nr_of_points=5 * self.number_of_rotations,
            message="Measuring Stokes Parameters using Quarterwaveplate Polarization Analysis System"
        )
        for beta_i in self.betas:
            self.quarterwaveplate.rotate(2 * beta_i)
            stokes_vector = self.quarterwaveplate.pass_stokes_vector(input_stokes_vector)
            stokes_vector = self.polarizer.pass_stokes_vector(stokes_vector)
            output_intensities.append(stokes_vector.s0)
            progress.update()

        a0 = 0
        for oi in output_intensities:
            a0 += oi
            progress.update()
        a0 *= (1 / self.number_of_rotations)

        a1 = 0
        for beta_i, oi in zip(self.betas, output_intensities):
            a1 += oi * cos(2 * beta_i)
            progress.update()
        a1 *= (2 / self.number_of_rotations)

        a2 = 0
        for beta_i, oi in zip(self.betas, output_intensities):
            a2 += oi * cos(4 * beta_i)
            progress.update()
        a2 *= (2 / self.number_of_rotations)

        b2 = 0
        for beta_i, oi in zip(self.betas, output_intensities):
            b2 += oi * sin(4 * beta_i)
            progress.update()
        b2 *= (2 / self.number_of_rotations)
        progress.close()
        sleep(0.1)

        # Destroy input stokes vector because it got used up during the measurement process
        input_stokes_vector.use_up()
        calculated_s = [2 * a0 + 2 * a2, 4 * b2, -4 * a2, -2 * a1]

        return self.print_and_return_results(computed_stokes_parameters=calculated_s)

    def instrument_name(self):
        return "Quarterwaveplate Polarimeter"
