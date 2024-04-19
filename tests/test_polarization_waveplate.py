from PyPola.OpticalInstruments.polarization_waveplate import PolarizationWaveplate, WaveplateType
from PyPola.Utilities.polarization_utilities import degree_of_polarization
from numpy import pi, array_equal, array
import unittest


class TestPolarizationWaveplate(unittest.TestCase):
    def test_quarter_waveplate_horizontal_input(self):
        """Linear horizontal polarized light passes through a quarter waveplate"""
        input_light = array([[1], [1], [0], [0]])
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)

        # Waveplate rotation angle to the x-axis is 0
        # Output light should come out the exact same as the input light
        quarter_waveplate.rotate(new_angle_to_x_axis=0)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(input_light, output_light))

        # Waveplate rotation angle to the x-axis is pi / 4
        # Output light should be right circular polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [0], [1]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 2
        # Output light should come out the exact same as the input light
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 2)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(input_light, output_light))

        # Waveplate rotation angle to the x-axis is 20 degrees
        # Output light should be elliptically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 9)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertFalse(array_equal(input_light, output_light))
        self.assertFalse(array_equal(array([[1], [0], [0], [1]]), output_light))
        dop = degree_of_polarization(output_light)
        print(f"Ellpitically polarized output light:\n{output_light}")
        print(f"Degree of polarization: {dop}")

    def test_quarter_waveplate_vertical_input(self):
        """Linear vertical polarized light passes through a quarter waveplate"""
        input_light = array([[1], [-1], [0], [0]])
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)

        # Waveplate rotation angle to the x-axis is 0
        # Output light should come out the exact same as the input light
        quarter_waveplate.rotate(new_angle_to_x_axis=0)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(input_light, output_light))

        # Waveplate rotation angle to the x-axis is pi / 4
        # Output light should be left circular polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [0], [-1]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 2
        # Output light should come out the exact same as the input light
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 2)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(input_light, output_light))

        # Waveplate rotation angle to the x-axis is 20 degrees
        # Output light should be elliptically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 9)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertFalse(array_equal(input_light, output_light))
        self.assertFalse(array_equal(array([[1], [0], [0], [-1]]), output_light))
        dop = degree_of_polarization(output_light)
        print(f"Ellpitically polarized output light:\n{output_light}")
        print(f"Degree of polarization: {dop}")

    def test_quarter_waveplate_plus45_input(self):
        """Linear +45° polarized light passes through a quarter waveplate"""
        input_light = array([[1], [0], [1], [0]])
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)

        # Waveplate rotation angle to the x-axis is 0
        # Output light should be right circular polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=0)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [0], [-1]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 4
        # Output light should come out the exact same as the input light
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(input_light, output_light))

        # Waveplate rotation angle to the x-axis is pi / 2
        # Output light should be left circular polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 2)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [0], [1]]), output_light))

        # Waveplate rotation angle to the x-axis is 20 degrees
        # Output light should be elliptically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 9)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertFalse(array_equal(input_light, output_light))
        self.assertFalse(array_equal(array([[1], [0], [0], [1]]), output_light))
        dop = degree_of_polarization(output_light)
        print(f"Ellpitically polarized output light:\n{output_light}")
        print(f"Degree of polarization: {dop}")

    def test_quarter_waveplate_minus45_input(self):
        """Linear -45° polarized light passes through a quarter waveplate"""
        input_light = array([[1], [0], [-1], [0]])
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)

        # Waveplate rotation angle to the x-axis is 0
        # Output light should be right circular polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=0)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [0], [1]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 4
        # Output light should come out the exact same as the input light
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(input_light, output_light))

        # Waveplate rotation angle to the x-axis is pi / 2
        # Output light should be left circular polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 2)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [0], [-1]]), output_light))

        # Waveplate rotation angle to the x-axis is 20 degrees
        # Output light should be elliptically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 9)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertFalse(array_equal(input_light, output_light))
        self.assertFalse(array_equal(array([[1], [0], [0], [1]]), output_light))
        dop = degree_of_polarization(output_light)
        print(f"Ellpitically polarized output light:\n{output_light}")
        print(f"Degree of polarization: {dop}")

    def test_quarter_waveplate_right_circular_input(self):
        """Right circular polarized light passes through a quarter waveplate"""
        input_light = array([[1], [0], [0], [1]])
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)

        # Waveplate rotation angle to the x-axis is 0
        # Output light should be +45° polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=0)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [1], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 4
        # Output light should be vertically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [-1], [0], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 2
        # Output light should be -45° polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 2)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [-1], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is 3 * pi / 4
        # Output light should be vertically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [-1], [0], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is 20 degrees
        # Output light should be elliptically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 9)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertFalse(array_equal(input_light, output_light))
        self.assertFalse(array_equal(array([[1], [-1], [0], [0]]), output_light))
        dop = degree_of_polarization(output_light)
        print(f"Ellpitically polarized output light:\n{output_light}")
        print(f"Degree of polarization: {dop}")

    def test_quarter_waveplate_left_circular_input(self):
        """Left circular polarized light passes through a quarter waveplate"""
        input_light = array([[1], [0], [0], [-1]])
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)

        # Waveplate rotation angle to the x-axis is 0
        # Output light should be -45° polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=0)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [-1], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 4
        # Output light should be horizontally polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [1], [0], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 2
        # Output light should be +45° polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 2)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [1], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is 3 * pi / 4
        # Output light should be horizontally polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [1], [0], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is 20 degrees
        # Output light should be elliptically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 9)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertFalse(array_equal(input_light, output_light))
        self.assertFalse(array_equal(array([[1], [0], [0], [1]]), output_light))
        dop = degree_of_polarization(output_light)
        print(f"Ellpitically polarized output light:\n{output_light}")
        print(f"Degree of polarization: {dop}")

    def test_half_waveplate_horizontal_input(self):
        """Linear horizontal polarized light passes through a half waveplate"""
        input_light = array([[1], [1], [0], [0]])
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.HALF)

        # Waveplate rotation angle to the x-axis is 0
        # Output light should come out the exact same as the input light
        quarter_waveplate.rotate(new_angle_to_x_axis=0)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(input_light, output_light))

        # Waveplate rotation angle to the x-axis is pi / 4
        # Output light should be vertically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [-1], [0], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 2
        # Output light should come out the exact same as the input light
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 2)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(input_light, output_light))

        # Waveplate rotation angle to the x-axis is 20 degrees
        # Output light should be elliptically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 9)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertFalse(array_equal(input_light, output_light))
        self.assertFalse(array_equal(array([[1], [-1], [0], [0]]), output_light))
        dop = degree_of_polarization(output_light)
        print(f"Ellpitically polarized output light:\n{output_light}")
        print(f"Degree of polarization: {dop}")

    def test_half_waveplate_vertical_input(self):
        """Linear vertical polarized light passes through a half waveplate"""
        input_light = array([[1], [-1], [0], [0]])
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.HALF)

        # Waveplate rotation angle to the x-axis is 0
        # Output light should come out the exact same as the input light
        quarter_waveplate.rotate(new_angle_to_x_axis=0)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(input_light, output_light))

        # Waveplate rotation angle to the x-axis is pi / 4
        # Output light should be horizontally polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [1], [0], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 2
        # Output light should come out the exact same as the input light
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 2)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(input_light, output_light))

        # Waveplate rotation angle to the x-axis is 20 degrees
        # Output light should be elliptically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 9)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertFalse(array_equal(input_light, output_light))
        self.assertFalse(array_equal(array([[1], [1], [0], [0]]), output_light))
        dop = degree_of_polarization(output_light)
        print(f"Ellpitically polarized output light:\n{output_light}")
        print(f"Degree of polarization: {dop}")

    def test_half_waveplate_plus45_input(self):
        """Linear +45° polarized light passes through a half waveplate"""
        input_light = array([[1], [0], [1], [0]])
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.HALF)

        # Waveplate rotation angle to the x-axis is 0
        # Output light should be -45° polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=0)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [-1], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 4
        # Output light should come out the exact same as the input light
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(input_light, output_light))

        # Waveplate rotation angle to the x-axis is pi / 2
        # Output light should be -45° polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 2)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [-1], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is 20 degrees
        # Output light should be elliptically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 9)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertFalse(array_equal(input_light, output_light))
        self.assertFalse(array_equal(array([[1], [0], [-1], [0]]), output_light))
        dop = degree_of_polarization(output_light)
        print(f"Ellpitically polarized output light:\n{output_light}")
        print(f"Degree of polarization: {dop}")

    def test_half_waveplate_minus45_input(self):
        """Linear -45° polarized light passes through a half waveplate"""
        input_light = array([[1], [0], [-1], [0]])
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.HALF)

        # Waveplate rotation angle to the x-axis is 0
        # Output light should be +45° polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=0)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [1], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 4
        # Output light should come out the exact same as the input light
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(input_light, output_light))

        # Waveplate rotation angle to the x-axis is pi / 2
        # Output light should be +45° polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 2)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [1], [0]]), output_light))

        # Waveplate rotation angle to the x-axis is 20 degrees
        # Output light should be elliptically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 9)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertFalse(array_equal(input_light, output_light))
        self.assertFalse(array_equal(array([[1], [0], [1], [0]]), output_light))
        dop = degree_of_polarization(output_light)
        print(f"Ellpitically polarized output light:\n{output_light}")
        print(f"Degree of polarization: {dop}")

    def test_helf_waveplate_right_circular_input(self):
        """Right circular polarized light passes through a quarter waveplate"""
        input_light = array([[1], [0], [0], [1]])
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.HALF)

        # Waveplate rotation angle to the x-axis is 0
        # Output light should be left circular polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=0)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [0], [-1]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 4
        # Output light should be left circular polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [0], [-1]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 2
        # Output light should be left circular polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 2)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [0], [-1]]), output_light))

        # Waveplate rotation angle to the x-axis is 20 degrees
        # Output light should be elliptically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 9)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertFalse(array_equal(input_light, output_light))
        dop = degree_of_polarization(output_light)
        print(f"Ellpitically polarized output light:\n{output_light}")
        print(f"Degree of polarization: {dop}")

    def test_helf_waveplate_left_circular_input(self):
        """Left circular polarized light passes through a quarter waveplate"""
        input_light = array([[1], [0], [0], [-1]])
        quarter_waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.HALF)

        # Waveplate rotation angle to the x-axis is 0
        # Output light should be right circular polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=0)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [0], [1]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 4
        # Output light should be right circular polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 4)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [0], [1]]), output_light))

        # Waveplate rotation angle to the x-axis is pi / 2
        # Output light should be right circular polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 2)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertTrue(array_equal(array([[1], [0], [0], [1]]), output_light))

        # Waveplate rotation angle to the x-axis is 20 degrees
        # Output light should be elliptically polarized
        quarter_waveplate.rotate(new_angle_to_x_axis=pi / 9)
        output_light = quarter_waveplate.pass_stokes_vector(input_light)
        self.assertFalse(array_equal(input_light, output_light))
        dop = degree_of_polarization(output_light)
        print(f"Ellpitically polarized output light:\n{output_light}")
        print(f"Degree of polarization: {dop}")
