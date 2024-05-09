from PyPola.FiberNetworkComponents.linbo3_polarization_controller import LiNbO3PolarizationController
from PyPola.FiberNetworkComponents.simple_polarization_controller import SimplePolarizationController
from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber
from PyPola.OpticalInstruments.linear_polarizer import LinearPolarizer
from PyPola.OpticalInstruments.polarization_waveplate import PolarizationWaveplate, WaveplateType
from PyPola.Utilities.polarization_utilities import (
    random_polarized_stokes_vector, get_angle_to_x_axis, get_ellipticity_angle, degree_of_polarization
)
from numpy import sqrt, array, sign, dot, arccos, pi
from numpy.linalg import norm
from random import uniform, choice

s_ref = array([1, 0, -0.5])
s_ref = s_ref / norm(s_ref)
s_ref = [[1], *[[si] for si in s_ref]]
qwp = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER, double_theta=pi)

print(s_ref)
print(get_angle_to_x_axis(s_ref))
print(get_ellipticity_angle(s_ref))
print(get_angle_to_x_axis(s_ref) + get_ellipticity_angle(s_ref))
s_ref = qwp.pass_stokes_vector(s_ref)
print(s_ref)
print(get_angle_to_x_axis(s_ref))
print(get_ellipticity_angle(s_ref))
print(get_angle_to_x_axis(s_ref) + get_ellipticity_angle(s_ref))
