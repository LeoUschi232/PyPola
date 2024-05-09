from PyPola.FiberNetworkComponents.linbo3_polarization_controller import LiNbO3PolarizationController
from PyPola.FiberNetworkComponents.simple_polarization_controller import SimplePolarizationController
from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber
from PyPola.OpticalInstruments.linear_polarizer import LinearPolarizer
from PyPola.OpticalInstruments.polarization_waveplate import PolarizationWaveplate, WaveplateType
from PyPola.Utilities.stokes_vector import StokesVector, NormalizationType
from PyPola.Utilities.polarization_utilities import random_polarized_stokes_vector
from numpy import sqrt, array, sign, dot, arccos, pi
from numpy.linalg import norm
from random import uniform, choice

s_ref = StokesVector(s0=1, s1=1, s2=0, s3=0.3, normalization=NormalizationType.POINCARE_SPHERE)
qwp = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER, double_theta=pi)
print(qwp.pass_stokes_vector(s_ref).as_vector())
