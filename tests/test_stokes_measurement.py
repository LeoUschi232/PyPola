from PyPola.FiberNetworkComponents.OpticalInstruments.linear_polarizer import LinearPolarizer
from PyPola.FiberNetworkComponents.OpticalInstruments.retardation_waveplate import RetardationWaveplate, WaveplateType
from PyPola.FiberNetworkComponents.OpticalInstruments.magneto_optic_rotator import MagnetoOpticRotator
from PyPola.utilities.polarization_utilities import random_polarized_stokes_vector
from PyPola.utilities.general_utilities import same
from numpy import pi, cos, sin, linspace
import unittest


class TestStokesMeasurement(unittest.TestCase):

    def test_polarization_analysis_quarterwaveplate_4_rotators(self):
        input_stokes_vector = random_polarized_stokes_vector()
        actual_s0, actual_s1, actual_s2, actual_s3 = input_stokes_vector.as_array()
        print(f"Input Stokes Vector: {input_stokes_vector.as_list()}")

        # It is convenient to choose LA angle pi/4 so that cos(2a) = 0
        # General Photonics Catalog suggests using MO rotator angle pi/8
        quarter_waveplate = RetardationWaveplate(waveplate_type=WaveplateType.QUARTER)
        linear_polarizer = LinearPolarizer(double_theta=pi / 2)
        mo_rotator = MagnetoOpticRotator(double_theta=pi / 4)
        gamma = quarter_waveplate.delta
        alpha = mo_rotator.double_theta
        beta = mo_rotator.double_theta

        # PAS = Polarization Analysis System
        def pas_output_intensity_model(qwp_angle, s0, s1, s2, s3):
            theta_p = linear_polarizer.double_theta - qwp_angle

            term1 = cos(2 * alpha) * cos(2 * (beta - theta_p))
            term2 = sin(2 * alpha) * sin(2 * (beta - theta_p)) * cos(gamma)
            term3 = sin(2 * alpha) * cos(2 * (beta - theta_p))
            term4 = cos(2 * alpha) * sin(2 * (beta - theta_p)) * cos(gamma)
            term5 = sin(2 * (beta - theta_p)) * sin(gamma)

            return 0.5 * (s0 + s1 * (term1 - term2) - s2 * (term3 + term4) - s3 * term5)

        qwp_angles = linspace(0, pi / 2, 300)
        print("Quarterwaveplate angle, Simulated intensity, Calculated intensity")
        for qwp_angle_i in qwp_angles:
            double_theta = quarter_waveplate.convert_x_axis_angle_to_double_theta(qwp_angle_i)
            quarter_waveplate.rotate(new_double_theta=double_theta)

            next_stokes_vector = mo_rotator.pass_stokes_vector(input_stokes_vector)
            next_stokes_vector = mo_rotator.pass_stokes_vector(next_stokes_vector)
            next_stokes_vector = quarter_waveplate.pass_stokes_vector(next_stokes_vector)
            next_stokes_vector = mo_rotator.pass_stokes_vector(next_stokes_vector)
            next_stokes_vector = mo_rotator.pass_stokes_vector(next_stokes_vector)
            next_stokes_vector = linear_polarizer.pass_stokes_vector(next_stokes_vector)
            simulated_intensity = next_stokes_vector.intensity

            calculated_intensity = pas_output_intensity_model(qwp_angle_i, actual_s0, actual_s1, actual_s2, actual_s3)
            print(f"{qwp_angle_i}, {simulated_intensity}, {calculated_intensity}")

    def test_polarization_analysis_quarterwaveplate_simple_1(self):
        input_stokes_vector = random_polarized_stokes_vector()
        actual_s0, actual_s1, actual_s2, actual_s3 = input_stokes_vector.as_array()
        print(f"Input Stokes Vector:\n {input_stokes_vector.as_list()}")

        double_alpha = pi / 2
        quarter_waveplate = RetardationWaveplate(waveplate_type=WaveplateType.QUARTER)
        linear_polarizer = LinearPolarizer(double_theta=double_alpha)

        def pas_output_intensity_model(double_beta, s0, s1, s2, s3):
            s1s2_subterm = s1 * cos(double_beta) + s2 * sin(double_beta)
            cos_2b_2a = cos(double_beta - double_alpha)
            sin_2b_2a = sin(double_beta - double_alpha)
            return 0.5 * (s0 + s1s2_subterm * cos_2b_2a + s3 * sin_2b_2a)

        failed = False
        qwp_angles = linspace(0, pi / 2, 300)
        print("Quarterwaveplate angle, Simulated intensity, Calculated intensity, Difference, Below tolerance")
        for qwp_angle in qwp_angles:
            double_beta_i = 2 * qwp_angle
            quarter_waveplate.rotate(new_double_theta=double_beta_i)

            next_stokes_vector = quarter_waveplate.pass_stokes_vector(input_stokes_vector)
            next_stokes_vector = linear_polarizer.pass_stokes_vector(next_stokes_vector)

            simulated_intensity = next_stokes_vector.intensity
            calculated_intensity = pas_output_intensity_model(double_beta_i, actual_s0, actual_s1, actual_s2, actual_s3)
            difference = abs(simulated_intensity - calculated_intensity)

            below_tolerance = "YES" if same(difference, 0) else "NO"
            if not same(difference, 0):
                failed = True
            print(f"{qwp_angle}, {simulated_intensity}, {calculated_intensity}, {difference}, {below_tolerance}")
        self.assertFalse(failed)

    def test_polarization_analysis_quarterwaveplate_simple_2(self):
        input_stokes_vector = random_polarized_stokes_vector()
        actual_s0, actual_s1, actual_s2, actual_s3 = input_stokes_vector.as_array()
        print(f"Input Stokes Vector:\n {input_stokes_vector.as_list()}")

        double_alpha = pi / 2
        quarter_waveplate = RetardationWaveplate(waveplate_type=WaveplateType.QUARTER)
        linear_polarizer = LinearPolarizer(double_theta=double_alpha)

        # PAS = Polarization Analysis System
        cos_2_alpha = cos(double_alpha)
        sin_2_alpha = sin(double_alpha)

        def pas_output_intensity_model(double_beta, s0, s1, s2, s3):
            cos_0_term = 0.5 * s0 + 0.25 * (s1 * cos_2_alpha + s2 * sin_2_alpha)
            cos_2b_term = -0.5 * s3 * sin_2_alpha * cos(double_beta)
            sin_2b_term = 0.5 * s3 * cos_2_alpha * sin(double_beta)
            cos_4b_term = 0.25 * (s1 * cos_2_alpha - s2 * sin_2_alpha) * cos(2 * double_beta)
            sin_4b_term = 0.25 * (s2 * cos_2_alpha + s1 * sin_2_alpha) * sin(2 * double_beta)
            return cos_0_term + cos_2b_term + sin_2b_term + cos_4b_term + sin_4b_term

        failed = False
        qwp_angles = linspace(0, pi / 2, 300)
        print("Quarterwaveplate angle, Simulated intensity, Calculated intensity, Difference, Below tolerance")
        for qwp_angle in qwp_angles:
            double_beta_i = 2 * qwp_angle
            quarter_waveplate.rotate(new_double_theta=double_beta_i)

            next_stokes_vector = quarter_waveplate.pass_stokes_vector(input_stokes_vector)
            next_stokes_vector = linear_polarizer.pass_stokes_vector(next_stokes_vector)

            simulated_intensity = next_stokes_vector.intensity
            calculated_intensity = pas_output_intensity_model(double_beta_i, actual_s0, actual_s1, actual_s2, actual_s3)
            difference = abs(simulated_intensity - calculated_intensity)

            below_tolerance = "YES" if same(difference, 0) else "NO"
            if not same(difference, 0):
                failed = True
            print(f"{qwp_angle}, {simulated_intensity}, {calculated_intensity}, {difference}, {below_tolerance}")
        self.assertFalse(failed)
