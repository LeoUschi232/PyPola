from PyPola.FiberNetworkComponents.PolarizationControllers.abstract_polarization_controller import \
    AbstractPolarizationController
from PyPola.FiberNetworkComponents.PolarizationControllers.delta_waveplate_polarization_controller import \
    DeltaWaveplatePolarizationController
from PyPola.FiberNetworkComponents.PolarizationControllers.qwp_hwp_qwp_polarization_controller import \
    QwpHwpQwpPolarizationController
from PyPola.FiberNetworkComponents.PolarizationControllers.variable_retardation_polarization_controller import \
    VariableRetardationPolarizationController
from PyPola.utilities.stokes_vector import StokesVector
from PyPola.utilities.polarization_utilities import random_polarized_stokes_vector
from numpy import mean
import unittest


class TestPolarizationControllers(unittest.TestCase):
    def test_delta_waveplate_polarization_controller(self):
        self.test_any_polarization_controller(controller=DeltaWaveplatePolarizationController(response_time=0))

    def test_qwp_hwp_qwp_polarization_controller(self):
        self.test_any_polarization_controller(controller=QwpHwpQwpPolarizationController(response_time=0))

    def test_variable_retardation_waveplates_polarization_controller(self):
        self.test_any_polarization_controller(controller=VariableRetardationPolarizationController(response_time=0))

    def test_any_polarization_controller(self, controller: AbstractPolarizationController = None):
        if controller is None:
            return

        # First out of 3 stages of testing the controller
        # In this stage the vectors S and Z have the same s1 and s2 values
        fails_threshold = 10
        fails = 0
        fail_differences = []
        for i in range(1000):
            s = random_polarized_stokes_vector()
            s1, s2, s3 = s.as_3d_array()
            z = StokesVector(s0=1, s1=s1, s2=s2, s3=-s3)
            controller.reconfigure_polarization_transformation(input_stokes_vector=s, output_stokes_vector=z)
            actual_z = controller.pass_stokes_vector(s)
            if not actual_z.equals(z):
                fails += 1
                fail_differences.append([abs(diff) for diff in z.as_3d_array() - actual_z.as_3d_array()])
        fail_message = (
            f"\nFails = {fails} > {fails_threshold} = Fails-threshold"
            f"\nAverage Stokes parameter fail difference: {mean(fail_differences)}"
        )
        self.assertLessEqual(fails, fails_threshold, msg=fail_message)

        # Second out of 3 stages of testing the controller
        # In this stage the vector Z is one of the main linear output polarizations
        fails_threshold = 10
        fails = 0
        fail_differences = []
        main_output_polarizations = [
            StokesVector(s0=1, s1=1, s2=0, s3=0),
            StokesVector(s0=1, s1=-1, s2=0, s3=0),
            StokesVector(s0=1, s1=0, s2=1, s3=0),
            StokesVector(s0=1, s1=0, s2=-1, s3=0)
        ]
        for z in main_output_polarizations:
            controller.reconfigure_polarization_transformation(output_stokes_vector=z)
            fails_threshold = 3
            fails = 0
            for t in range(250):
                s = random_polarized_stokes_vector()
                controller.reconfigure_polarization_transformation(input_stokes_vector=s)
                actual_z = controller.pass_stokes_vector(s)

                if not actual_z.equals(z):
                    fails += 1
                    fail_differences.append([abs(diff) for diff in z.as_3d_array() - actual_z.as_3d_array()])
        fail_message = (
            f"\nFails = {fails} > {fails_threshold} = Fails-threshold"
            f"\nAverage Stokes parameter fail difference: {mean(fail_differences)}"
        )
        self.assertLessEqual(fails, fails_threshold, msg=fail_message)

        # Third out of 3 stages of testing the controller
        # In this stage the vector Z can be any polarized stokes vector
        fails_threshold = 10
        fails = 0
        fail_differences = []
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
                fail_differences.append([abs(diff) for diff in z.as_3d_array() - actual_z.as_3d_array()])
        fail_message = (
            f"\nFails = {fails} > {fails_threshold} = Fails-threshold"
            f"\nAverage Stokes parameter fail difference: {mean(fail_differences)}"
        )
        self.assertLessEqual(fails, fails_threshold, msg=fail_message)
