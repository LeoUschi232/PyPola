from PyPola.FiberNetworkComponents.Polarimeters.four_detector_polarimeter import FourDetecterPolarimeter
from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber, load_fiber_from_csv
from PyPola.utilities.general_utilities import progress_bar
from PyPola.utilities.stokes_vector import StokesVector
from numpy import pi, array, arange, dot, zeros
from matplotlib import pyplot as plt
from os import path

nr_of_measurements = 10000
measurements = arange(nr_of_measurements)
precomputed_fiber = {
    "chose_fiber": True,
    "n": 1000000,
    "t": 5,
    "d": 6,
    "v": 0
}

# This is the fiber setup and does not need to be configured
# as no data will be measured about the fiber just here
if precomputed_fiber["chose_fiber"]:
    n = precomputed_fiber["n"]
    t = precomputed_fiber["t"]
    d = precomputed_fiber["d"]
    v = precomputed_fiber["v"]
    fiber_path = f"Fibers/FibersLength{n}/fiber_n{n}_t{t}_d{d}_v{v}.csv"
    if path.exists(fiber_path):
        fiber = load_fiber_from_csv(fiber_path)
    else:
        fiber = OpticalFiber(
            nr_of_segments=n,
            temporal_pmd_theta_fluctuation=pi / (2 ** t),
            temporal_pmd_delta_fluctuation=pi / (2 ** d),
        )
else:
    fiber = OpticalFiber(
        nr_of_segments=100000,
        temporal_pmd_theta_fluctuation=pi / 128,
        temporal_pmd_delta_fluctuation=pi / 128,
    )

# The next part are the measurements of the stokes parameter at the fiber output
# They need not yet be compensated because the PolaFlex will only measure these parameters without compensation
# The measured data will be used to determine the compensation parameters
horizontal_sv = StokesVector(s0=1, s1=1, s2=0, s3=0)
vertical_sv = StokesVector(s0=1, s1=-1, s2=0, s3=0)
diagonal_sv = StokesVector(s0=1, s1=0, s2=1, s3=0)
antidiagonal_sv = StokesVector(s0=1, s1=0, s2=-1, s3=0)

polaflex = FourDetecterPolarimeter()
h_data = []
v_data = []
d_data = []
a_data = []
progress = progress_bar(
    nr_of_points=nr_of_measurements,
    message="Measuring Stokes Parameters using PolaFlex"
)
for _ in measurements:
    fiber.fluctuate_pmd()
    # Only save the bottom 3 stokes paramaters because the intensity is not needed
    h_data.append(polaflex.measure_stokes_parameters(fiber.pass_stokes_vector(horizontal_sv))[1:])
    v_data.append(polaflex.measure_stokes_parameters(fiber.pass_stokes_vector(vertical_sv))[1:])
    d_data.append(polaflex.measure_stokes_parameters(fiber.pass_stokes_vector(diagonal_sv))[1:])
    a_data.append(polaflex.measure_stokes_parameters(fiber.pass_stokes_vector(antidiagonal_sv))[1:])
    progress.update()
progress.close()

# After pure polarization state data has been measured, we can compute the qbers
qber_threshhold = 0.05
h_reference = array(h_data[0])
v_reference = array(v_data[0])
d_reference = array(d_data[0])
a_reference = array(a_data[0])
h_qbers = []
v_qbers = []
d_qbers = []
a_qbers = []
h_compensation_steps = [0]
v_compensation_steps = [0]
d_compensation_steps = [0]
a_compensation_steps = [0]
for i in measurements:
    h_output = array(h_data[i])
    v_output = array(v_data[i])
    d_output = array(d_data[i])
    a_output = array(a_data[i])
    h_qber = 0.5 * (1 - dot(h_reference, h_output))
    v_qber = 0.5 * (1 - dot(v_reference, v_output))
    d_qber = 0.5 * (1 - dot(d_reference, d_output))
    a_qber = 0.5 * (1 - dot(a_reference, a_output))
    h_qbers.append(h_qber)
    v_qbers.append(v_qber)
    d_qbers.append(d_qber)
    a_qbers.append(a_qber)
    if h_qber > qber_threshhold:
        h_reference = h_output
        h_compensation_steps.append(i)
    if v_qber > qber_threshhold:
        v_reference = v_output
        v_compensation_steps.append(i)
    if d_qber > qber_threshhold:
        d_reference = d_output
        d_compensation_steps.append(i)
    if a_qber > qber_threshhold:
        a_reference = a_output
        a_compensation_steps.append(i)


# Now finally plot the data
def plot_subarray(plot_index, sop_data, qber_data, compensation_data):
    plt.subplot(4, 2, plot_index)
    plt.plot(measurements, [sop_data[i][0] for i in measurements], color="blue", label="S1")
    plt.plot(measurements, [sop_data[i][1] for i in measurements], color="red", label="S2")
    plt.plot(measurements, [sop_data[i][2] for i in measurements], color="green", label="S3")
    plt.plot(measurements, zeros(shape=measurements.shape), color="black")
    plt.xlabel(f"t", fontsize=11)
    plt.ylabel(f"Stokes Parameters", fontsize=16)
    plt.xlim([0, nr_of_measurements])
    plt.ylim([-1, 1])
    plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
    plt.legend(loc="upper left", fontsize=14)

    plt.subplot(4, 2, plot_index + 1)
    plt.plot(measurements, qber_data, color="gold", label="QBER")
    for step in compensation_data:
        plt.axvline(x=step, color="purple", linestyle="--", linewidth=0.5)
    plt.xlabel(f"t", fontsize=11)
    plt.ylabel(f"Expected QBER ", fontsize=16)
    plt.xlim([0, nr_of_measurements])
    plt.ylim([0, 2 * qber_threshhold])
    plt.grid(color="gray", linestyle="dotted", linewidth=0.5)

    avg_steps_between_compensations = round(nr_of_measurements / len(compensation_data))
    plt.legend(
        loc="upper left",
        fontsize=14,
        title=f"Avg compensation interval: {avg_steps_between_compensations}",
        title_fontsize=14
    )


plot_subarray(1, h_data, h_qbers, h_compensation_steps)
plot_subarray(3, v_data, v_qbers, v_compensation_steps)
plot_subarray(5, d_data, d_qbers, d_compensation_steps)
plot_subarray(7, a_data, a_qbers, a_compensation_steps)
plt.show()
