from PyPola.FiberNetworkComponents.Polarimeters.four_detector_polarimeter import FourDetecterPolarimeter
from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber
from PyPola.utilities.polarization_utilities import random_polarized_stokes_vector
from PyPola.utilities.stokes_vector import StokesVector
from random import uniform
from numpy import pi, array, sqrt

input_svs = [StokesVector(s0=1, s1=1, s2=0, s3=0, wavelength=wl) for wl in range(1540, 1561)]
fiber = OpticalFiber(
    nr_of_segments=10000,
    center_wavelength=1500,
    temporal_pmd_theta_fluctuation=pi / 64,
    temporal_pmd_delta_fluctuation=pi / 64,
    spectral_pmd_theta_fluctuation=pi / 64,
    spectral_pmd_delta_fluctuation=pi / 64
)
output_svs = [fiber.pass_stokes_vector(input_sv) for input_sv in input_svs]
for output_sv in output_svs:
    print(output_sv.as_list())
