from PyPola.Utilities.polarization_utilities import (
    random_polarized_stokes_vector, degree_of_polarization, get_angle_to_x_axis,
    stokes_vector_from_elliptical_parameters
)
from numpy import pi, linspace
import unittest


class TestPolarizationUtils(unittest.TestCase):
    def test_random_polarized_stokes_vector(self):
        attempts = 100
        for _ in range(attempts):
            stokes_vector = random_polarized_stokes_vector()
            dop = degree_of_polarization(stokes_vector)
            self.assertTrue(abs(dop - 1.0) < 1e-12, f"Stokes vector: {stokes_vector}\nDOP: {dop}\n")

    def test_angle_to_x_axis(self):
        self.assertEqual(get_angle_to_x_axis([[1], [1], [0], [0]]), 0.0)
        self.assertEqual(get_angle_to_x_axis([[1], [-1], [0], [0]]), pi / 2)
        self.assertEqual(get_angle_to_x_axis([[1], [0], [1], [0]]), pi / 4)
        self.assertEqual(get_angle_to_x_axis([[1], [0], [-1], [0]]), -pi / 4)
        self.assertEqual(get_angle_to_x_axis([[2], [1], [1], [0]]), pi / 8)
        self.assertEqual(get_angle_to_x_axis([[2], [-1], [1], [0]]), 3 * pi / 8)
        self.assertEqual(get_angle_to_x_axis([[2], [1], [-1], [0]]), -pi / 8)
        self.assertEqual(get_angle_to_x_axis([[2], [-1], [-1], [0]]), -3 * pi / 8)

        for expected_psi in linspace(-pi / 2, pi / 2, 256):
            sv = stokes_vector_from_elliptical_parameters(psi=expected_psi)
            actual_psi = get_angle_to_x_axis(sv)
            print(f"Expected: {expected_psi}")
            print(f"  Actual: {actual_psi}\n")
            self.assertTrue(abs(actual_psi - expected_psi) < 1e-12)
