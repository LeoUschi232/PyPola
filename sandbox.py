from PyPola.FiberNetworkComponents.Polarimeters.four_detector_polarimeter import FourDetecterPolarimeter
from PyPola.FiberNetworkComponents.OpticalInstruments.polarization_beam_splitter import PolarizationBeamSplitter
from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber
from PyPola.utilities.polarization_utilities import random_polarized_stokes_vector
from PyPola.utilities.stokes_vector import StokesVector
from random import uniform
from numpy import pi, array, sqrt

horizontal_sv = StokesVector(s0=1, s1=1, s2=0, s3=0)
vertical_sv = StokesVector(s0=1, s1=-1, s2=0, s3=0)
diagonal_sv = StokesVector(s0=1, s1=0, s2=1, s3=0)
antidiagonal_sv = StokesVector(s0=1, s1=0, s2=-1, s3=0)
pbs = PolarizationBeamSplitter(transmission_double_theta=0)

transmitted_horizontal, reflected_horizontal = [sv.s0 for sv in pbs.pass_stokes_vector(horizontal_sv)]
transmitted_vertical, reflected_vertical = [sv.s0 for sv in pbs.pass_stokes_vector(vertical_sv)]
transmitted_diagonal, reflected_diagonal = [sv.s0 for sv in pbs.pass_stokes_vector(diagonal_sv)]
transmitted_antidiagonal, reflected_antidiagonal = [sv.s0 for sv in pbs.pass_stokes_vector(antidiagonal_sv)]
print("Transmission angle: 0°")
print("  Horizontal:", round(transmitted_horizontal, 2), round(reflected_horizontal, 2))
print("    Vertical:", round(transmitted_vertical, 2), round(reflected_vertical, 2))
print("    Diagonal:", round(transmitted_diagonal, 2), round(reflected_diagonal, 2))
print("Antidiagonal:", round(transmitted_antidiagonal, 2), round(reflected_antidiagonal, 2), "\n")

pbs.rotate(new_transmission_double_theta=pi / 2)
transmitted_horizontal, reflected_horizontal = [sv.s0 for sv in pbs.pass_stokes_vector(horizontal_sv)]
transmitted_vertical, reflected_vertical = [sv.s0 for sv in pbs.pass_stokes_vector(vertical_sv)]
transmitted_diagonal, reflected_diagonal = [sv.s0 for sv in pbs.pass_stokes_vector(diagonal_sv)]
transmitted_antidiagonal, reflected_antidiagonal = [sv.s0 for sv in pbs.pass_stokes_vector(antidiagonal_sv)]
print("Transmission angle: 45°")
print("  Horizontal:", round(transmitted_horizontal, 2), round(reflected_horizontal, 2))
print("    Vertical:", round(transmitted_vertical, 2), round(reflected_vertical, 2))
print("    Diagonal:", round(transmitted_diagonal, 2), round(reflected_diagonal, 2))
print("Antidiagonal:", round(transmitted_antidiagonal, 2), round(reflected_antidiagonal, 2), "\n")

pbs.rotate(new_transmission_double_theta=pi)
transmitted_horizontal, reflected_horizontal = [sv.s0 for sv in pbs.pass_stokes_vector(horizontal_sv)]
transmitted_vertical, reflected_vertical = [sv.s0 for sv in pbs.pass_stokes_vector(vertical_sv)]
transmitted_diagonal, reflected_diagonal = [sv.s0 for sv in pbs.pass_stokes_vector(diagonal_sv)]
transmitted_antidiagonal, reflected_antidiagonal = [sv.s0 for sv in pbs.pass_stokes_vector(antidiagonal_sv)]
print("Transmission angle: 90°")
print("  Horizontal:", round(transmitted_horizontal, 2), round(reflected_horizontal, 2))
print("    Vertical:", round(transmitted_vertical, 2), round(reflected_vertical, 2))
print("    Diagonal:", round(transmitted_diagonal, 2), round(reflected_diagonal, 2))
print("Antidiagonal:", round(transmitted_antidiagonal, 2), round(reflected_antidiagonal, 2), "\n")

pbs.rotate(new_transmission_double_theta=3 * pi / 2)
transmitted_horizontal, reflected_horizontal = [sv.s0 for sv in pbs.pass_stokes_vector(horizontal_sv)]
transmitted_vertical, reflected_vertical = [sv.s0 for sv in pbs.pass_stokes_vector(vertical_sv)]
transmitted_diagonal, reflected_diagonal = [sv.s0 for sv in pbs.pass_stokes_vector(diagonal_sv)]
transmitted_antidiagonal, reflected_antidiagonal = [sv.s0 for sv in pbs.pass_stokes_vector(antidiagonal_sv)]
print("Transmission angle: 135°")
print("  Horizontal:", round(transmitted_horizontal, 2), round(reflected_horizontal, 2))
print("    Vertical:", round(transmitted_vertical, 2), round(reflected_vertical, 2))
print("    Diagonal:", round(transmitted_diagonal, 2), round(reflected_diagonal, 2))
print("Antidiagonal:", round(transmitted_antidiagonal, 2), round(reflected_antidiagonal, 2), "\n")
