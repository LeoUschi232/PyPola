from PyPola.FiberNetworkComponents.linbo3_polarization_controller import LiNbO3PolarizationController
from PyPola.Utilities.polarization_utilities import random_polarized_stokes_vector
from PyPola.Utilities.general_utilities import float_array_same, random_sign
from numpy import array, sqrt
from random import uniform
import unittest


class TestLiNbO3PolarizationController(unittest.TestCase):
    def test_linb03_s3_sqrt(self):
        controller = LiNbO3PolarizationController()
        fails_threshold = 0
        fails = 0
        for i in range(1000):
            s3 = random_sign() / sqrt(2)
            s2 = uniform(-s3, s3)
            s1 = random_sign() * sqrt(1 - s2 * s2 - s3 * s3)
            s = [[1], [s1], [s2], [s3]]
            z = [[1], [s1], [s2], [-s3]]
            expected_output = array(z).flatten()

            controller.reconfigure_polarization_transformation(input_stokes_vector=s, output_stokes_vector=z)
            actual_output = controller.pass_stokes_vector(s).flatten()

            if not float_array_same(expected_output, actual_output):
                fails += 1
        print(f"Number of fails: {fails}")
        self.assertLessEqual(fails, fails_threshold)

    def test_linb03_same_s1_and_s2(self):
        controller = LiNbO3PolarizationController()
        fails_threshold = 10
        fails = 0
        for i in range(1000):
            s = random_polarized_stokes_vector()
            z = [[1], s[1], s[2], [-s[3][0]]]
            expected_output = array(z).flatten()

            controller.reconfigure_polarization_transformation(input_stokes_vector=s, output_stokes_vector=z)
            actual_output = controller.pass_stokes_vector(s).flatten()

            if abs(expected_output[3] - actual_output[3]) < 1e-4:
                print(f"Success on pass {i}")
                print(f"Expected: {expected_output}")
                print(f"  Actual: {actual_output}\n")
            else:
                fails += 1
        print(f"Number of fails: {fails}")
        self.assertLessEqual(fails, fails_threshold)

    def test_linb03_main_transformations(self):
        main_output_polarizations = [
            [[1], [1], [0], [0]],
            [[1], [-1], [0], [0]],
            [[1], [0], [1], [0]],
            [[1], [0], [-1], [0]]
        ]
        print(f"Testing LiNbO3 Polarization Controller\n")
        for z in main_output_polarizations:
            polarization_controller = LiNbO3PolarizationController(output_stokes_vector=z)
            expected_z = array(z).flatten()

            fails_threshold = 3
            fails = 0
            for t in range(250):
                sv = random_polarized_stokes_vector()
                polarization_controller.reconfigure_polarization_transformation(input_stokes_vector=sv)
                actual_z = polarization_controller.pass_stokes_vector(sv).flatten()
                if not float_array_same(actual_z, expected_z):
                    fails += 1
            print(f"For z={expected_z}")
            print(f"Number of fails: {fails}\n")
            self.assertLessEqual(fails, fails_threshold)

    def test_linb03_arbitrary_transformations(self):
        print(f"Testing LiNbO3 Polarization Controller\n")
        polarization_controller = LiNbO3PolarizationController()

        fails_threshold = 10
        fails = 0
        for t in range(1000):
            s = random_polarized_stokes_vector()
            z = random_polarized_stokes_vector()
            expected_z = array(z).flatten()

            polarization_controller.reconfigure_polarization_transformation(
                input_stokes_vector=s,
                output_stokes_vector=z
            )
            actual_z = polarization_controller.pass_stokes_vector(s).flatten()
            if not float_array_same(actual_z, expected_z):
                fails += 1

        print(f"Number of fails: {fails}\n")
        self.assertLessEqual(fails, fails_threshold)
