from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber
from PyPola.FiberNetworkComponents.OpticalInstruments.polarization_beam_splitter import PolarizationBeamSplitter
from PyPola.utilities.stokes_vector import StokesVector
from numpy import pi, arange
from matplotlib import pyplot as plt

horizontal_sv = StokesVector(s0=1, s1=1, s2=0, s3=0)
vertical_sv = StokesVector(s0=1, s1=-1, s2=0, s3=0)
diagonal_sv = StokesVector(s0=1, s1=0, s2=1, s3=0)
antidiagonal_sv = StokesVector(s0=1, s1=0, s2=-1, s3=0)
pbs = PolarizationBeamSplitter()

# The fiber is assumed to be a single-mode fiber.
# Fiber property combinations to iterate over:
fiber_lengths = [1000, 10000, 100000]
fiber_theta_fluctuations = [pi / (2 ** i) for i in range(8, 4, -1)]
fiber_delta_fluctuations = [pi / (2 ** i) for i in range(8, 4, -1)]
combined_fiber_properties = [
    [fiber_length, fiber_theta_fluctuation, fiber_delta_fluctuation]
    for fiber_length in fiber_lengths
    for fiber_theta_fluctuation in fiber_theta_fluctuations
    for fiber_delta_fluctuation in fiber_delta_fluctuations
]

# Lists to save the QBIT error rates for each fiber property combination
# combinations = len(fiber_lengths) * len(fiber_theta_fluctuations) * len(fiber_delta_fluctuations)
nr_of_datapoints = 45
horizontal_qbers = []
vertical_qbers = []
diagonal_qbers = []
antidiagonal_qbers = []

for i in range(len(combined_fiber_properties)):
    fiber_length, fiber_theta_fluctuation, fiber_delta_fluctuation = combined_fiber_properties[i]
    horizontal_qber = 0
    vertical_qber = 0
    diagonal_qber = 0
    antidiagonal_qber = 0
    for _ in range(nr_of_datapoints):
        print(f"No compensation fiber analysis progress {i + 1}/{len(combined_fiber_properties)}")
        fiber = OpticalFiber(
            nr_of_segments=fiber_length,
            temporal_pmd_theta_fluctuation=fiber_theta_fluctuation,
            temporal_pmd_delta_fluctuation=fiber_delta_fluctuation
        )

        # The quantum bits which would have been measured in the wrong base would be disgarded anyway.
        # Therefore, we can assume that all quantum bits to be considered are those measured in the right base.
        # We set the angle of the polarization beam splitter to 0° for the horizontal-vertical basis
        # and to 45° for the diagonal-antidiagonal basis.
        pbs.rotate(new_transmission_double_theta=0)
        horizontal_sv_transmitted, horizontal_sv_reflected \
            = pbs.pass_stokes_vector(fiber.pass_stokes_vector(horizontal_sv))
        vertical_sv_transmitted, vertical_sv_reflected \
            = pbs.pass_stokes_vector(fiber.pass_stokes_vector(vertical_sv))

        pbs.rotate(new_transmission_double_theta=0.5 * pi)
        diagonal_sv_transmitted, diagonal_sv_reflected \
            = pbs.pass_stokes_vector(fiber.pass_stokes_vector(diagonal_sv))
        antidiagonal_sv_transmitted, antidiagonal_sv_reflected \
            = pbs.pass_stokes_vector(fiber.pass_stokes_vector(antidiagonal_sv))

        # The quantum bit error rate is the probability that the photon got either transmitted when it should
        # have been reflected or reflected when it should have been transmitted.
        # The probability of the photon getting transmitted or reflected is for a single quantum bit the same
        # thing as the intensity of the transmitted or reflected light pulse in a macroscopic consideration.
        horizontal_qber += horizontal_sv_reflected.s0 / nr_of_datapoints
        vertical_qber += vertical_sv_transmitted.s0 / nr_of_datapoints
        diagonal_qber += diagonal_sv_reflected.s0 / nr_of_datapoints
        antidiagonal_qber += antidiagonal_sv_transmitted.s0 / nr_of_datapoints
    horizontal_qbers.append(horizontal_qber)
    vertical_qbers.append(vertical_qber)
    diagonal_qbers.append(diagonal_qber)
    antidiagonal_qbers.append(antidiagonal_qber)

# Create a list of labels for each combination of fiber properties
labels = [(
    f"L:10^{len(str(fiber_length)) - 1}\n"
    f"θ:{round(fiber_theta_fluctuation, 2)}\n"
    f"δ:{round(fiber_delta_fluctuation, 2)}"
) for fiber_length, fiber_theta_fluctuation, fiber_delta_fluctuation in combined_fiber_properties]

bar_width = 0.2
x = arange(len(combined_fiber_properties))

# Create a figure and axis
fig, ax = plt.subplots(figsize=(20, 10))

# Plotting the bars for each QBER
bar1 = ax.bar(x - 1.5 * bar_width, horizontal_qbers, bar_width, label="Horizontal", color="yellow")
bar2 = ax.bar(x - 0.5 * bar_width, vertical_qbers, bar_width, label="Vertical", color="blue")
bar3 = ax.bar(x + 0.5 * bar_width, diagonal_qbers, bar_width, label="Diagonal", color="red")
bar4 = ax.bar(x + 1.5 * bar_width, antidiagonal_qbers, bar_width, label="Antidiagonal", color="green")

# Adding labels to the x-axis
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8, rotation=90)

# Adding labels and title
ax.set_xlabel("Fiber Segment counts")
ax.set_ylabel("Average expected QBER")
ax.set_title("Expected QBERs for Different Segment counts")
ax.legend()

# Show the plot
plt.tight_layout()
plt.show()
