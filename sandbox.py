from PyPola.PolarizationControllers.linbo3_polarization_controller import LiNbO3PolarizationController
from PyPola.PolarizationControllers.simple_polarization_controller import SimplePolarizationController
from PyPola.PolarizationControllers.qwp_hwp_qwp_polarization_controller import QwpHwpQwpPolarizationController
from PyPola.Utilities.stokes_vector import StokesVector, NormalizationType
from PyPola.Utilities.polarization_utilities import random_polarized_stokes_vector
from PyPola.Utilities.general_utilities import normalize_and_clean
from numpy import arccos, sqrt


s = random_polarized_stokes_vector()
z = StokesVector(s0=1, s1=1, s2=0, s3=0)

linbo3_controller = LiNbO3PolarizationController(input_stokes_vector=s, output_stokes_vector=z)
simple_controller = SimplePolarizationController(input_stokes_vector=s, output_stokes_vector=z)
qwphwpqwp_controller = QwpHwpQwpPolarizationController(input_stokes_vector=s, output_stokes_vector=z)
print(f"Input Stokes vector: {s.as_list()}\n")
print(linbo3_controller.mueller_matrix)
print(simple_controller.mueller_matrix)
print(qwphwpqwp_controller.mueller_matrix)
print(" ")
print(linbo3_controller.pass_stokes_vector(s).as_list())
print(simple_controller.pass_stokes_vector(s).as_list())
print(qwphwpqwp_controller.pass_stokes_vector(s).as_list())
