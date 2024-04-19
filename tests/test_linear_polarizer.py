from OpticalInstruments.linear_polarizer import LinearPolarizer
from Utilities.polarization_utilities import degree_of_polarization
from numpy import pi, array_equal, array, sqrt
from random import uniform
import unittest


class TestLinearPolarizer(unittest.TestCase):
    def test_linear_polarizer_transmission_matrices(self):
        horizontal_transmission_matrix = 0.5 * array([
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])
        vertical_transmission_matrix = 0.5 * array([
            [1, -1, 0, 0],
            [-1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ])
        plus45_transmission_matrix = 0.5 * array([
            [1, 0, 1, 0],
            [0, 0, 0, 0],
            [1, 0, 1, 0],
            [0, 0, 0, 0]
        ])
        minus45_transmission_matrix = 0.5 * array([
            [1, 0, -1, 0],
            [0, 0, 0, 0],
            [-1, 0, 1, 0],
            [0, 0, 0, 0]
        ])

        horizontal_polarizer = LinearPolarizer(angle_to_x_axis=0)
        vertical_polarizer = LinearPolarizer(angle_to_x_axis=pi / 2)
        plus45_polarizer = LinearPolarizer(angle_to_x_axis=pi / 4)
        minus45_polarizer = LinearPolarizer(angle_to_x_axis=-pi / 4)

        print(horizontal_polarizer.stokes_matrix)
        print(vertical_polarizer.stokes_matrix)
        print(plus45_polarizer.stokes_matrix)
        print(minus45_polarizer.stokes_matrix)

        self.assertTrue(array_equal(horizontal_polarizer.stokes_matrix, horizontal_transmission_matrix))
        self.assertTrue(array_equal(vertical_polarizer.stokes_matrix, vertical_transmission_matrix))
        self.assertTrue(array_equal(plus45_polarizer.stokes_matrix, plus45_transmission_matrix))
        self.assertTrue(array_equal(minus45_polarizer.stokes_matrix, minus45_transmission_matrix))

    def test_perfect_output_polarization(self):
        tests_amount = 1000
        for i in range(tests_amount):
            print(f"Test {100 * (i + 1) / tests_amount}% complete.")

            s1 = uniform(-1, 1)
            s2 = uniform(-1, 1)
            s3 = uniform(-1, 1)
            normalization = sqrt(s1 * s1 + s2 * s2 + s3 * s3)
            if normalization < 1e-12:
                continue
            if normalization > 1:
                s1 = s1 / normalization
                s2 = s2 / normalization
                s3 = s3 / normalization
            input_stokes_vector = [[1], [s1], [s2], [s3]]
            print(f"Input Stokes Vector:\n {input_stokes_vector}\n")

            random_angle = uniform(-pi, pi)
            polarizer = LinearPolarizer(angle_to_x_axis=random_angle)
            output_stokes_vector = polarizer.pass_stokes_vector(input_stokes_vector)
            print(f"Output Stokes Vector:\n {output_stokes_vector}\n")

            dop = degree_of_polarization(output_stokes_vector)
            difference = abs(dop - 1)
            self.assertTrue(difference < 1e-12, f"Fail on iteration: {i + 1}\nDegree of Polarization: {dop}\n")
