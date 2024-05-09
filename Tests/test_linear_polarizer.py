from PyPola.OpticalInstruments.linear_polarizer import LinearPolarizer
from PyPola.Utilities.polarization_utilities import random_polarized_stokes_vector
from numpy import pi, array_equal, array
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

        horizontal_polarizer = LinearPolarizer(double_theta=0)
        vertical_polarizer = LinearPolarizer(double_theta=pi)
        plus45_polarizer = LinearPolarizer(double_theta=pi / 2)
        minus45_polarizer = LinearPolarizer(double_theta=-pi / 2)

        self.assertTrue(array_equal(horizontal_polarizer.mueller_matrix, horizontal_transmission_matrix))
        self.assertTrue(array_equal(vertical_polarizer.mueller_matrix, vertical_transmission_matrix))
        self.assertTrue(array_equal(plus45_polarizer.mueller_matrix, plus45_transmission_matrix))
        self.assertTrue(array_equal(minus45_polarizer.mueller_matrix, minus45_transmission_matrix))

    def test_perfect_output_polarization(self):
        tests_amount = 1000
        for i in range(tests_amount):
            input_stokes_vector = random_polarized_stokes_vector()
            random_angle = uniform(-pi, pi)
            polarizer = LinearPolarizer(double_theta=random_angle)
            output_stokes_vector = polarizer.pass_stokes_vector(input_stokes_vector)

            dop = output_stokes_vector.degree_of_polarization
            difference = abs(dop - 1)
            self.assertTrue(difference < 1e-12, f"Fail on iteration: {i + 1}\nDegree of Polarization: {dop}\n")
