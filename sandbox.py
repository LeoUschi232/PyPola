from PyPola.PolarizationControllers.linbo3_polarization_controller import LiNbO3PolarizationController
from PyPola.PolarizationControllers.simple_polarization_controller import SimplePolarizationController
from PyPola.PolarizationControllers.qwp_hwp_qwp_polarization_controller import QwpHwpQwpPolarizationController
from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber
from PyPola.Utilities.stokes_vector import StokesVector, NormalizationType
from PyPola.Utilities.polarization_utilities import random_polarized_stokes_vector
from PyPola.Utilities.general_utilities import normalize_and_clean
from numpy import arccos, sqrt


z1 = StokesVector(s0=1, s1=1, s2=0, s3=0)
z2 = StokesVector(s0=1, s1=-1, s2=0, s3=0)
z3 = StokesVector(s0=1, s1=0, s2=1, s3=0)
z4 = StokesVector(s0=1, s1=0, s2=-1, s3=0)
z5 = StokesVector(s0=1, s1=0, s2=0, s3=1)
z6 = StokesVector(s0=1, s1=0, s2=0, s3=-1)

fiber = OpticalFiber(nr_of_segments=100000)
s_ref1 = fiber.pass_stokes_vector(z1)
s_ref2 = fiber.pass_stokes_vector(z2)
s_ref3 = fiber.pass_stokes_vector(z3)
s_ref4 = fiber.pass_stokes_vector(z4)
s_ref5 = fiber.pass_stokes_vector(z5)
s_ref6 = fiber.pass_stokes_vector(z6)

linbo3_controller = LiNbO3PolarizationController(input_stokes_vector=s_ref1, output_stokes_vector=z1)
qwphwpqwp_controller = QwpHwpQwpPolarizationController(input_stokes_vector=s_ref1, output_stokes_vector=z1)

print(linbo3_controller.pass_stokes_vector(s_ref1).as_list())
print(qwphwpqwp_controller.pass_stokes_vector(s_ref1).as_list())
print(linbo3_controller.pass_stokes_vector(s_ref2).as_list())
print(qwphwpqwp_controller.pass_stokes_vector(s_ref2).as_list())
print(linbo3_controller.pass_stokes_vector(s_ref3).as_list())
print(qwphwpqwp_controller.pass_stokes_vector(s_ref3).as_list())
print(linbo3_controller.pass_stokes_vector(s_ref4).as_list())
print(qwphwpqwp_controller.pass_stokes_vector(s_ref4).as_list())
print(linbo3_controller.pass_stokes_vector(s_ref5).as_list())
print(qwphwpqwp_controller.pass_stokes_vector(s_ref5).as_list())
print(linbo3_controller.pass_stokes_vector(s_ref6).as_list())
print(qwphwpqwp_controller.pass_stokes_vector(s_ref6).as_list())
