from OpticalInstruments.linear_polarizer import LinearPolarizer
from OpticalInstruments.polarization_waveplate import PolarizationWaveplate, WaveplateType
from OpticalInstruments.magneto_optic_rotator import MagnetoOpticRotator
from Utilities.polarization_utilities import (
    random_polarized_stokes_vector, degree_of_polarization
)
from numpy import pi, cos, sin, linspace, concatenate
import unittest


class TestStokesMeasurement(unittest.TestCase):

    def test_polarization_analysis_quarterwaveplate_4_rotators(self):
        input_stokes_vector = random_polarized_stokes_vector()
        actual_s0, actual_s1, actual_s2, actual_s3 = concatenate(input_stokes_vector)
        print(f"Input Stokes Vector:\n {input_stokes_vector}")
        print(actual_s0, actual_s1, actual_s2, actual_s3, "\n")

        # It is convenient to choose LA angle pi/4 so that cos(2a) = 0
        # General Photonics Catalog suggests using MO rotator angle pi/8
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)
        linear_polarizer = LinearPolarizer(angle_to_x_axis=pi / 4)
        mo_rotator = MagnetoOpticRotator(angle_to_x_axis=pi / 8)
        gamma = quarter_waveplate.phase_shift
        alpha = 2 * mo_rotator.angle_to_x_axis
        beta = 2 * mo_rotator.angle_to_x_axis

        # PAS = Polarization Analysis System
        def pas_output_intensity_model(qwp_angle, s0, s1, s2, s3):
            theta_p = linear_polarizer.angle_to_x_axis - qwp_angle

            term1 = cos(2 * alpha) * cos(2 * (beta - theta_p))
            term2 = sin(2 * alpha) * sin(2 * (beta - theta_p)) * cos(gamma)
            term3 = sin(2 * alpha) * cos(2 * (beta - theta_p))
            term4 = cos(2 * alpha) * sin(2 * (beta - theta_p)) * cos(gamma)
            term5 = sin(2 * (beta - theta_p)) * sin(gamma)

            return 0.5 * (s0 + s1 * (term1 - term2) - s2 * (term3 + term4) - s3 * (term5))

        qwp_angles = [angle for angle in linspace(0, pi / 2, 100)]
        intensities = []
        print("Quarterwaveplate angle, Simulated intensity, Calculated intensity")
        for qwp_angle_i in qwp_angles:
            quarter_waveplate.rotate(qwp_angle_i)

            next_stokes_vector = mo_rotator.pass_stokes_vector(input_stokes_vector)
            next_stokes_vector = mo_rotator.pass_stokes_vector(next_stokes_vector)
            next_stokes_vector = quarter_waveplate.pass_stokes_vector(next_stokes_vector)
            next_stokes_vector = mo_rotator.pass_stokes_vector(next_stokes_vector)
            next_stokes_vector = mo_rotator.pass_stokes_vector(next_stokes_vector)
            next_stokes_vector = linear_polarizer.pass_stokes_vector(next_stokes_vector)
            simulated_intensity = next_stokes_vector[0][0]

            calculated_intensity = pas_output_intensity_model(qwp_angle_i, actual_s0, actual_s1, actual_s2, actual_s3)
            print(f"{qwp_angle_i}, {simulated_intensity}, {calculated_intensity}")

    def test_polarization_analysis_quarterwaveplate_simple_1(self):
        input_stokes_vector = random_polarized_stokes_vector()
        actual_s0, actual_s1, actual_s2, actual_s3 = concatenate(input_stokes_vector)
        print(f"Input Stokes Vector:\n {input_stokes_vector}")
        print(actual_s0, actual_s1, actual_s2, actual_s3, "\n")

        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)
        linear_polarizer = LinearPolarizer(angle_to_x_axis=pi / 2)
        delta = quarter_waveplate.phase_shift
        alpha = linear_polarizer.angle_to_x_axis

        # PAS = Polarization Analysis System
        cos_delta = cos(delta)
        sin_delta = sin(delta)

        def pas_output_intensity_model(beta, s0, s1, s2, s3):
            i = s0
            m = s1
            c = s2
            s = s3
            cos_2_beta = cos(2 * beta)
            sin_2_beta = sin(2 * beta)
            cos_2_alpha_beta = cos(2 * (alpha - beta))
            sin_2_alpha_beta = sin(2 * (alpha - beta))

            term_1 = (m * cos_2_beta + c * sin_2_beta) * cos_2_alpha_beta

            subterm_21 = (c * cos_2_beta - m * sin_2_beta) * cos_delta
            term_2 = (subterm_21 + s * sin_delta) * sin_2_alpha_beta
            return 0.5 * (i + term_1 + term_2)

        qwp_angles = [angle for angle in linspace(0, pi / 2, 300)]
        print("Quarterwaveplate angle, Simulated intensity, Calculated intensity, Difference, Below tolerance")
        for beta in qwp_angles:
            quarter_waveplate.rotate(new_angle_to_x_axis=beta)

            next_stokes_vector = quarter_waveplate.pass_stokes_vector(input_stokes_vector)
            next_stokes_vector = linear_polarizer.pass_stokes_vector(next_stokes_vector)

            simulated_intensity = next_stokes_vector[0][0]
            calculated_intensity = pas_output_intensity_model(beta, actual_s0, actual_s1, actual_s2, actual_s3)
            difference = abs(simulated_intensity - calculated_intensity)
            below_tolerance = "YES" if difference < 1e-12 else "NO"
            print(f"{beta}, {simulated_intensity}, {calculated_intensity}, {difference}, {below_tolerance}")

    def test_polarization_analysis_quarterwaveplate_simple_2(self):
        input_stokes_vector = random_polarized_stokes_vector()
        actual_s0, actual_s1, actual_s2, actual_s3 = concatenate(input_stokes_vector)
        print(f"Input Stokes Vector:\n {input_stokes_vector}")
        print(actual_s0, actual_s1, actual_s2, actual_s3, "\n")

        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)
        linear_polarizer = LinearPolarizer(angle_to_x_axis=pi / 2)
        delta = quarter_waveplate.phase_shift
        alpha = linear_polarizer.angle_to_x_axis

        # PAS = Polarization Analysis System
        cos_2_alpha = cos(2 * alpha)
        sin_2_alpha = sin(2 * alpha)
        cos_delta = cos(delta)
        sin_delta = sin(delta)

        def pas_output_intensity_model(beta, s0, s1, s2, s3):
            i = s0
            m = s1
            c = s2
            s = s3
            cos_2_beta = cos(2 * beta)
            sin_2_beta = sin(2 * beta)
            cos_4_beta = cos(4 * beta)
            sin_4_beta = sin(4 * beta)
            cos_2_alpha_beta = cos(2 * (alpha - beta))
            sin_2_alpha_beta = sin(2 * (alpha - beta))

            subterm_11 = 0.5 * (m * cos_2_alpha + c * sin_2_alpha) * (1 + cos(delta))
            term_1 = 0.5 * (i + subterm_11)

            term_2 = 0.5 * s * sin_delta * sin_2_alpha_beta

            subterm_31 = (m * cos_2_alpha - c * sin_2_alpha) * cos_4_beta
            subterm_32 = (m * sin_2_alpha + c * cos_2_alpha) * sin_4_beta
            term_3 = 0.25 * (subterm_31 + subterm_32) * (1 - cos_delta)
            return term_1 + term_2 + term_3

        qwp_angles = [angle for angle in linspace(0, pi / 2, 300)]
        print("Quarterwaveplate angle, Simulated intensity, Calculated intensity, Difference, Below tolerance")
        for beta in qwp_angles:
            quarter_waveplate.rotate(new_angle_to_x_axis=beta)

            next_stokes_vector = quarter_waveplate.pass_stokes_vector(input_stokes_vector)
            next_stokes_vector = linear_polarizer.pass_stokes_vector(next_stokes_vector)

            simulated_intensity = next_stokes_vector[0][0]
            calculated_intensity = pas_output_intensity_model(beta, actual_s0, actual_s1, actual_s2, actual_s3)
            difference = abs(simulated_intensity - calculated_intensity)
            below_tolerance = "YES" if difference < 1e-12 else "NO"
            print(f"{beta}, {simulated_intensity}, {calculated_intensity}, {difference}, {below_tolerance}")
