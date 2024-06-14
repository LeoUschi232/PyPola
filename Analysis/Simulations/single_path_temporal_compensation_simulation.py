from PyPola.FiberNetworkComponents.PolarizationControllers.delta_waveplate_polarization_controller import (
    DeltaWaveplatePolarizationController
)
from PyPola.FiberNetworkComponents.PolarizationControllers.qwp_hwp_qwp_polarization_controller import (
    QwpHwpQwpPolarizationController
)
from PyPola.FiberNetworkComponents.PolarizationControllers.variable_retardation_polarization_controller import (
    VariableRetardationPolarizationController
)
from PyPola.FiberNetworkComponents.OpticalInstruments.polarization_beam_splitter import (
    PolarizationBeamSplitter, PbsPass
)
from PyPola.FiberNetworkComponents.optical_fiber import load_fiber_from_csv
from PyPola.utilities.general_utilities import progress_bar
from PyPola.utilities.stokes_vector import StokesVector
from PyPola.utilities.polarization_utilities import LinearPolarization, double_theta_map, linear_stokes_vector_map
from numpy import min, max, average

# Prepared polarization state controllers to choose from for the simulation
# Since a unit of time is defined to bne 250 ns in this simulation, the contrtollers have the following response times:
# EOSpace LiBnO3 100 ns => 0 units
# GP fibersqueezer 35 um => 140 units
# Thorlabs fibertwister 400 ms => 1600000 units
eospace_linbo3_controller = DeltaWaveplatePolarizationController(response_time=0)
thorlabs_fibertwister_controller = QwpHwpQwpPolarizationController(response_time=1600000)
gp_fibersqueezer_controller = VariableRetardationPolarizationController(response_time=140)

########################################################################################################################
"""
Here adjust the parameters of the simulation.
Keep in mind that timesteps are counted in units of 100 nanoseconds.
"""
chosen_controller = gp_fibersqueezer_controller
compensation_interval = 2000
transmission_time = 60000
fiber_length = 100000
optical_fiber = load_fiber_from_csv(f"Fibers/FibersLength{fiber_length}/fiber_n{fiber_length}_t6_d6_v1.csv")
input_sop = LinearPolarization.HORIZONTAL

########################################################################################################################
# Initialize controller matrix
s_input = linear_stokes_vector_map[input_sop]
s_ref = optical_fiber.pass_stokes_vector(s_input)
chosen_controller.reconfigure_polarization_transformation(s_ref, s_input)
for _ in range(chosen_controller.response_time):
    optical_fiber.fluctuate_pmd()
    chosen_controller.pass_stokes_vector(s_input)
pbs = PolarizationBeamSplitter(transmission_double_theta=double_theta_map[input_sop])

progress = progress_bar(nr_of_points=transmission_time)
qbers = []
for timestep in range(transmission_time):
    optical_fiber.fluctuate_pmd()
    progress.update()

    if timestep % compensation_interval == 0:
        s_ref = optical_fiber.pass_stokes_vector(s_input)
        chosen_controller.reconfigure_polarization_transformation(s_ref, s_input)
        continue

    s_quant = optical_fiber.pass_stokes_vector(s_input)
    z_quant = chosen_controller.pass_stokes_vector(s_quant)
    _, z_reflected = pbs.pass_stokes_vector(z_quant)
    qber = z_reflected.s0
    if qber > 0.5:
        print(f"QBER over 50% at step:", timestep)
    qbers.append(qber)
progress.close()

print(f"Minimum QBER:", round(100 * min(qbers), 2), "%")
print(f"Average QBER:", round(100 * average(qbers), 2), "%")
print(f"Maximum QBER:", round(100 * max(qbers), 2), "%")
