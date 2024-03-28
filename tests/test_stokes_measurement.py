from OpticalInstruments.linear_polarizer import LinearPolarizer
from OpticalInstruments.polarization_waveplate import PolarizationWaveplate, WaveplateType
from OpticalInstruments.zz_polarization_utilities import (
    normalize_stokes_vector, random_polarized_stokes_vector, degree_of_polarization
)
from numpy import pi, cos, sin, linspace, concatenate
from random import uniform
import unittest


class TestStokesMeasurement(unittest.TestCase):
    def test_random_polarized_stokes_vector(self):
        attempts = 100
        for _ in range(attempts):
            stokes_vector = random_polarized_stokes_vector()
            dop = degree_of_polarization(stokes_vector)
            self.assertTrue(abs(dop - 1.0) < 1e-12, f"Stokes vector: {stokes_vector}\nDOP: {dop}\n")

    def test_polarization_analysis_using_least_squares_fit(self):
        input_stokes_vector = random_polarized_stokes_vector()
        actual_s0, actual_s1, actual_s2, actual_s3 = concatenate(input_stokes_vector)
        print(f"Input Stokes Vector:\n {input_stokes_vector}")
        print(actual_s0, actual_s1, actual_s2, actual_s3, "\n")

        # Polarization analysis system

        # H. G. Berry, G. Gabrielse, and A. E. Livingston paper says:
        # It is convenient to choose alpha = pi/4 so that cos(2a) = 0
        alpha = pi / 4
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)
        linear_polarizer = LinearPolarizer(angle_to_x_axis=alpha)
        delta = quarter_waveplate.phase_shift

        def model_intensity(beta_i, i, m, c, s):
            return (0.5 * (i + (m * cos(2 * beta_i) + c * sin(2 * beta_i)) * cos(2 * (alpha - beta_i))
                           + (c * cos(2 * beta_i) - m * sin(2 * beta_i)) * cos(delta) + s * sin(delta))
                    * sin(2 * (alpha - beta_i)))

        betas = linspace(0, 0.5 * pi, 100)
        print(f"Simulated intensity, Calculated intensity")
        for beta in betas:
            quarter_waveplate.rotate(beta)
            simulated_intensity = linear_polarizer.pass_stokes_vector(
                quarter_waveplate.pass_stokes_vector(input_stokes_vector)
            )[0][0]
            calculated_intensity = model_intensity(beta, 1, actual_s1, actual_s2, actual_s3)
            print(f"{simulated_intensity}, {calculated_intensity}")
