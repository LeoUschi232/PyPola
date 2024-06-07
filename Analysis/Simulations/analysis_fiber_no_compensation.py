from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber
from PyPola.FiberNetworkComponents.OpticalInstruments.polarization_beam_splitter import PolarizationBeamSplitter
from PyPola.utilities.stokes_vector import StokesVector
from random import uniform
from numpy import pi, array, sqrt

horizontal_sv = StokesVector(s0=1, s1=1, s2=0, s3=0)
vertical_sv = StokesVector(s0=1, s1=-1, s2=0, s3=0)
diagonal_sv = StokesVector(s0=1, s1=0, s2=1, s3=0)
antidiagonal_sv = StokesVector(s0=1, s1=0, s2=-1, s3=0)
pbs = PolarizationBeamSplitter()

fiber_lengths = [10 ** i for i in range(1, 6)]
fiber_theta_fluctuations = [(2 ** i) * pi / 2048 for i in range(7)]
fiber_delta_fluctuations = [(2 ** i) * pi / 2048 for i in range(7)]

for fiber_length in fiber_lengths:
    for fiber_theta_fluctuation in fiber_theta_fluctuations:
        for fiber_delta_fluctuation in fiber_delta_fluctuations:
            fiber = OpticalFiber(
                nr_of_segments=fiber_length,
                temporal_pmd_theta_fluctuation=fiber_theta_fluctuation,
                temporal_pmd_delta_fluctuation=fiber_delta_fluctuation
            )

            pbs.rotate(new_transmission_double_theta=0)
            horizontal_sv_transmitted, horizontal_sv_reflected \
                = pbs.pass_stokes_vector(fiber.pass_stokes_vector(horizontal_sv))
            vertical_sv_transmitted, vertical_sv_reflected \
                = pbs.pass_stokes_vector(fiber.pass_stokes_vector(vertical_sv))

            pbs.rotate(new_transmission_double_theta=0.25 * pi)
            diagonal_sv_transmitted, diagonal_sv_reflected \
                = pbs.pass_stokes_vector(fiber.pass_stokes_vector(diagonal_sv))
            antidiagonal_sv_transmitted, antidiagonal_sv_reflected \
                = pbs.pass_stokes_vector(fiber.pass_stokes_vector(antidiagonal_sv))

            # TODO: Finish up QBER calculation
