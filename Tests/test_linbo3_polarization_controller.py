from PyPola.FiberNetworkComponents.linbo3_polarization_controller import LiNbO3PolarizationController
from PyPola.Utilities.stokes_vector import StokesVector
from PyPola.Utilities.polarization_utilities import random_polarized_stokes_vector
import unittest


class TestLiNbO3PolarizationController(unittest.TestCase):

    def test_linb03_same_s1_and_s2(self):
        controller = LiNbO3PolarizationController()
        fails_threshold = 10
        fails = 0
        for i in range(1000):
            s = random_polarized_stokes_vector()
            s1, s2, s3 = s.as_3d_array()
            z = StokesVector(s0=1, s1=s1, s2=s2, s3=-s3)

            controller.reconfigure_polarization_transformation(input_stokes_vector=s, output_stokes_vector=z)
            actual_z = controller.pass_stokes_vector(s)

            if not actual_z.equals(z):
                fails += 1
        print(f"Fails threshold was set to: {fails_threshold}")
        print(f"Total number of fails: {fails}\n")
        self.assertLessEqual(fails, fails_threshold)

    def test_linb03_main_transformations(self):
        main_output_polarizations = [
            StokesVector(s0=1, s1=1, s2=0, s3=0),
            StokesVector(s0=1, s1=-1, s2=0, s3=0),
            StokesVector(s0=1, s1=0, s2=1, s3=0),
            StokesVector(s0=1, s1=0, s2=-1, s3=0)
        ]
        print(f"Testing LiNbO3 Polarization Controller\n")
        for z in main_output_polarizations:
            controller = LiNbO3PolarizationController(output_stokes_vector=z)

            fails_threshold = 3
            fails = 0
            for t in range(250):
                s = random_polarized_stokes_vector()
                controller.reconfigure_polarization_transformation(input_stokes_vector=s)
                actual_z = controller.pass_stokes_vector(s)

                if not actual_z.equals(z):
                    fails += 1

            print(f"For z={z.as_list()}")
            print(f"Fails threshold was set to: {fails_threshold}")
            print(f"Total number of fails: {fails}\n")
            self.assertLessEqual(fails, fails_threshold)

    def test_linb03_arbitrary_transformations(self):
        print(f"Testing LiNbO3 Polarization Controller\n")
        controller = LiNbO3PolarizationController()

        fails_threshold = 10
        fails = 0
        for t in range(1000):
            s = random_polarized_stokes_vector()
            z = random_polarized_stokes_vector()

            controller.reconfigure_polarization_transformation(
                input_stokes_vector=s,
                output_stokes_vector=z
            )
            actual_z = controller.pass_stokes_vector(s)
            if not actual_z.equals(z):
                fails += 1

        print(f"Fails threshold was set to: {fails_threshold}")
        print(f"Total number of fails: {fails}\n")
        self.assertLessEqual(fails, fails_threshold)
