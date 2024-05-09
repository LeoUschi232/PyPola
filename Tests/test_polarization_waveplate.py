from PyPola.OpticalInstruments.polarization_waveplate import PolarizationWaveplate, WaveplateType
from PyPola.Utilities.stokes_vector import StokesVector
from numpy import pi
import unittest


class TestPolarizationWaveplate(unittest.TestCase):
    def test_quarterwaveplate_horizontal_input(self):
        """Linear horizontal polarized light passes through a quarter waveplate"""
        input_light = StokesVector(s0=1, s1=1, s2=0, s3=0)
        quarterwaveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)

        quarterwaveplate.rotate(new_double_theta=0)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(input_light.equals(output_light))

        quarterwaveplate.rotate(new_double_theta=pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=-1))

        quarterwaveplate.rotate(new_double_theta=pi)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(input_light.equals(output_light))

        quarterwaveplate.rotate(new_double_theta=pi / 9)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertFalse(input_light.equals(output_light))
        self.assertFalse(output_light.has_parameters(s0=1, s1=0, s2=0, s3=1))
        dop = output_light.degree_of_polarization
        print(f"Elliptically polarized output light:\n{output_light.as_vector()}")
        print(f"Degree of polarization: {dop}")

    def test_quarterwaveplate_vertical_input(self):
        """Linear vertical polarized light passes through a quarter waveplate"""
        input_light = StokesVector(s0=1, s1=-1, s2=0, s3=0)
        quarterwaveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)

        quarterwaveplate.rotate(new_double_theta=0)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(input_light.equals(output_light))

        quarterwaveplate.rotate(new_double_theta=pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=1))

        quarterwaveplate.rotate(new_double_theta=pi)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(input_light.equals(output_light))

        quarterwaveplate.rotate(new_double_theta=pi / 9)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertFalse(input_light.equals(output_light))
        self.assertFalse(output_light.has_parameters(s0=1, s1=0, s2=0, s3=-1))
        dop = output_light.degree_of_polarization
        print(f"Elliptically polarized output light:\n{output_light.as_vector()}")
        print(f"Degree of polarization: {dop}")

    def test_quarterwaveplate_plus45_input(self):
        """Linear +45° polarized light passes through a quarter waveplate"""
        input_light = StokesVector(s0=1, s1=0, s2=1, s3=0)
        quarterwaveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)

        quarterwaveplate.rotate(new_double_theta=0)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=1))

        quarterwaveplate.rotate(new_double_theta=pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(input_light.equals(output_light))

        quarterwaveplate.rotate(new_double_theta=pi)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=-1))

        quarterwaveplate.rotate(new_double_theta=pi / 9)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertFalse(input_light.equals(output_light))
        self.assertFalse(output_light.has_parameters(s0=1, s1=0, s2=0, s3=1))
        dop = output_light.degree_of_polarization
        print(f"Elliptically polarized output light:\n{output_light.as_vector()}")
        print(f"Degree of polarization: {dop}")

    def test_quarterwaveplate_minus45_input(self):
        """Linear -45° polarized light passes through a quarter waveplate"""
        input_light = StokesVector(s0=1, s1=0, s2=-1, s3=0)
        quarterwaveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)

        quarterwaveplate.rotate(new_double_theta=0)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=-1))

        quarterwaveplate.rotate(new_double_theta=pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(input_light.equals(output_light))

        quarterwaveplate.rotate(new_double_theta=pi)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=1))

        quarterwaveplate.rotate(new_double_theta=pi / 9)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertFalse(input_light.equals(output_light))
        self.assertFalse(output_light.has_parameters(s0=1, s1=0, s2=0, s3=1))
        dop = output_light.degree_of_polarization
        print(f"Elliptically polarized output light:\n{output_light.as_vector()}")
        print(f"Degree of polarization: {dop}")

    def test_quarterwaveplate_right_circular_input(self):
        """Right circular polarized light passes through a quarter waveplate"""
        input_light = StokesVector(s0=1, s1=0, s2=0, s3=1)
        quarterwaveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)

        quarterwaveplate.rotate(new_double_theta=0)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=-1, s3=0))

        quarterwaveplate.rotate(new_double_theta=pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=1, s2=0, s3=0))

        quarterwaveplate.rotate(new_double_theta=pi)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=1, s3=0))

        quarterwaveplate.rotate(new_double_theta=-pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=-1, s2=0, s3=0))

        quarterwaveplate.rotate(new_double_theta=pi / 9)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertFalse(input_light.equals(output_light))
        self.assertFalse(output_light.has_parameters(s0=1, s1=-1, s2=0, s3=0))
        dop = output_light.degree_of_polarization
        print(f"Elliptically polarized output light:\n{output_light.as_vector()}")
        print(f"Degree of polarization: {dop}")

    def test_quarterwaveplate_left_circular_input(self):
        """Left circular polarized light passes through a quarter waveplate"""
        input_light = StokesVector(s0=1, s1=0, s2=0, s3=-1)
        quarterwaveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)

        quarterwaveplate.rotate(new_double_theta=0)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=1, s3=0))

        quarterwaveplate.rotate(new_double_theta=pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=-1, s2=0, s3=0))

        quarterwaveplate.rotate(new_double_theta=pi)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=-1, s3=0))

        quarterwaveplate.rotate(new_double_theta=-pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=1, s2=0, s3=0))

        quarterwaveplate.rotate(new_double_theta=pi / 9)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertFalse(input_light.equals(output_light))
        self.assertFalse(output_light.has_parameters(s0=1, s1=0, s2=0, s3=1))
        dop = output_light.degree_of_polarization
        print(f"Elliptically polarized output light:\n{output_light.as_vector()}")
        print(f"Degree of polarization: {dop}")

    def test_halfwaveplate_horizontal_input(self):
        """Linear horizontal polarized light passes through a half waveplate"""
        input_light = StokesVector(s0=1, s1=1, s2=0, s3=0)
        quarterwaveplate = PolarizationWaveplate(waveplate_type=WaveplateType.HALF)

        quarterwaveplate.rotate(new_double_theta=0)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(input_light.equals(output_light))

        quarterwaveplate.rotate(new_double_theta=pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=-1, s2=0, s3=0))

        quarterwaveplate.rotate(new_double_theta=pi)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(input_light.equals(output_light))

        quarterwaveplate.rotate(new_double_theta=pi / 9)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertFalse(input_light.equals(output_light))
        self.assertFalse(output_light.has_parameters(s0=1, s1=-1, s2=0, s3=0))
        dop = output_light.degree_of_polarization
        print(f"Elliptically polarized output light:\n{output_light.as_vector()}")
        print(f"Degree of polarization: {dop}")

    def test_halfwaveplate_vertical_input(self):
        """Linear vertical polarized light passes through a half waveplate"""
        input_light = StokesVector(s0=1, s1=-1, s2=0, s3=0)
        quarterwaveplate = PolarizationWaveplate(waveplate_type=WaveplateType.HALF)

        quarterwaveplate.rotate(new_double_theta=0)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(input_light.equals(output_light))

        quarterwaveplate.rotate(new_double_theta=pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=1, s2=0, s3=0))

        quarterwaveplate.rotate(new_double_theta=pi)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(input_light.equals(output_light))

        quarterwaveplate.rotate(new_double_theta=pi / 9)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertFalse(input_light.equals(output_light))
        self.assertFalse(output_light.has_parameters(s0=1, s1=1, s2=0, s3=0))
        dop = output_light.degree_of_polarization
        print(f"Elliptically polarized output light:\n{output_light.as_vector()}")
        print(f"Degree of polarization: {dop}")

    def test_halfwaveplate_plus45_input(self):
        """Linear +45° polarized light passes through a half waveplate"""
        input_light = StokesVector(s0=1, s1=0, s2=1, s3=0)
        quarterwaveplate = PolarizationWaveplate(waveplate_type=WaveplateType.HALF)

        quarterwaveplate.rotate(new_double_theta=0)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=-1, s3=0))

        quarterwaveplate.rotate(new_double_theta=pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(input_light.equals(output_light))

        quarterwaveplate.rotate(new_double_theta=pi)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=-1, s3=0))

        quarterwaveplate.rotate(new_double_theta=pi / 9)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertFalse(input_light.equals(output_light))
        self.assertFalse(output_light.has_parameters(s0=1, s1=0, s2=-1, s3=0))
        dop = output_light.degree_of_polarization
        print(f"Elliptically polarized output light:\n{output_light.as_vector()}")
        print(f"Degree of polarization: {dop}")

    def test_halfwaveplate_minus45_input(self):
        """Linear -45° polarized light passes through a half waveplate"""
        input_light = StokesVector(s0=1, s1=0, s2=-1, s3=0)
        quarterwaveplate = PolarizationWaveplate(waveplate_type=WaveplateType.HALF)

        quarterwaveplate.rotate(new_double_theta=0)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=1, s3=0))

        quarterwaveplate.rotate(new_double_theta=pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(input_light.equals(output_light))

        quarterwaveplate.rotate(new_double_theta=pi)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=1, s3=0))

        quarterwaveplate.rotate(new_double_theta=pi / 9)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertFalse(input_light.equals(output_light))
        self.assertFalse(output_light.has_parameters(s0=1, s1=0, s2=1, s3=0))
        dop = output_light.degree_of_polarization
        print(f"Elliptically polarized output light:\n{output_light.as_vector()}")
        print(f"Degree of polarization: {dop}")

    def test_halfwaveplate_right_circular_input(self):
        """Right circular polarized light passes through a quarter waveplate"""
        input_light = StokesVector(s0=1, s1=0, s2=0, s3=1)
        quarterwaveplate = PolarizationWaveplate(waveplate_type=WaveplateType.HALF)

        quarterwaveplate.rotate(new_double_theta=0)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=-1))

        quarterwaveplate.rotate(new_double_theta=pi / 4)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=-1))

        quarterwaveplate.rotate(new_double_theta=pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=-1))

        quarterwaveplate.rotate(new_double_theta=pi)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=-1))

        quarterwaveplate.rotate(new_double_theta=pi / 9)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertFalse(input_light.equals(output_light))
        dop = output_light.degree_of_polarization
        print(f"Elliptically polarized output light:\n{output_light.as_vector()}")
        print(f"Degree of polarization: {dop}")

    def test_halfwaveplate_left_circular_input(self):
        """Left circular polarized light passes through a quarter waveplate"""
        input_light = StokesVector(s0=1, s1=0, s2=0, s3=-1)
        quarterwaveplate = PolarizationWaveplate(waveplate_type=WaveplateType.HALF)

        quarterwaveplate.rotate(new_double_theta=0)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=1))

        quarterwaveplate.rotate(new_double_theta=pi / 4)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=1))

        quarterwaveplate.rotate(new_double_theta=pi / 2)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=1))

        quarterwaveplate.rotate(new_double_theta=pi)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertTrue(output_light.has_parameters(s0=1, s1=0, s2=0, s3=1))

        quarterwaveplate.rotate(new_double_theta=pi / 9)
        output_light = quarterwaveplate.pass_stokes_vector(input_light)
        self.assertFalse(input_light.equals(output_light))
        dop = output_light.degree_of_polarization
        print(f"Elliptically polarized output light:\n{output_light.as_vector()}")
        print(f"Degree of polarization: {dop}")
