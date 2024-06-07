from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber, load_fiber_from_csv
from PyPola.FiberNetworkComponents.OpticalInstruments.polarization_beam_splitter import PolarizationBeamSplitter
from PyPola.utilities.stokes_vector import StokesVector
from numpy import pi, arange
from matplotlib import pyplot as plt
from os import path

horizontal_sv = StokesVector(s0=1, s1=1, s2=0, s3=0)
vertical_sv = StokesVector(s0=1, s1=-1, s2=0, s3=0)
diagonal_sv = StokesVector(s0=1, s1=0, s2=1, s3=0)
antidiagonal_sv = StokesVector(s0=1, s1=0, s2=-1, s3=0)
pbs = PolarizationBeamSplitter()

# The fiber is assumed to be a single-mode fiber.
# Fiber property combinations to iterate over:
fiber_lengths = [1000, 10000, 100000, 1000000]
theta_fluctuations = [(pi / (2 ** i), i) for i in range(8, 4, -1)]
delta_fluctuations = [(pi / (2 ** i), i) for i in range(8, 4, -1)]

# Lists to save the QBIT error rates for each fiber property combination
# combinations = len(fiber_lengths) * len(fiber_theta_fluctuations) * len(fiber_delta_fluctuations)
horizontal_qbers = []
vertical_qbers = []
diagonal_qbers = []
antidiagonal_qbers = []

max_progress = len(fiber_lengths) * len(theta_fluctuations) * len(delta_fluctuations)
progress = 0
for fiber_length in fiber_lengths:
    for fiber_theta_fluctuation, i_t in theta_fluctuations:
        for fiber_delta_fluctuation, i_d in delta_fluctuations:
            horizontal_qber = 0
            vertical_qber = 0
            diagonal_qber = 0
            antidiagonal_qber = 0
            v = 0
            while True:
                fiber_path = f"Fibers/FibersLength{fiber_length}/fiber_n{fiber_length}_t{i_t}_d{i_d}_v{v}.csv"
                if not path.exists(fiber_path):
                    if v > 0:
                        horizontal_qber /= v
                        vertical_qber /= v
                        diagonal_qber /= v
                        antidiagonal_qber /= v
                    break
                fiber = load_fiber_from_csv(fiber_path)

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
                horizontal_qber += horizontal_sv_reflected.s0
                vertical_qber += vertical_sv_transmitted.s0
                diagonal_qber += diagonal_sv_reflected.s0
                antidiagonal_qber += antidiagonal_sv_transmitted.s0
                v += 1
            horizontal_qbers.append(horizontal_qber)
            vertical_qbers.append(vertical_qber)
            diagonal_qbers.append(diagonal_qber)
            antidiagonal_qbers.append(antidiagonal_qber)
            progress += 1
            print(f"No compensation fiber analysis progress: {progress}/{max_progress}")

# Create a figure and axis
bar_width = 0.2
horizontal_x = arange(-0.3, max_progress - 0.3, 1)
vertical_x = arange(-0.1, max_progress - 0.1, 1)
diagonal_x = arange(0.1, max_progress + 0.1, 1)
antidiagonal_x = arange(0.3, max_progress + 0.3, 1)
figure, axes = plt.subplots()

# Plotting the bars for each QBER
bar1 = axes.bar(horizontal_x, horizontal_qbers, bar_width, label="Horizontal", color="yellow")
bar2 = axes.bar(vertical_x, vertical_qbers, bar_width, label="Vertical", color="blue")
bar3 = axes.bar(diagonal_x, diagonal_qbers, bar_width, label="Diagonal", color="red")
bar4 = axes.bar(antidiagonal_x, antidiagonal_qbers, bar_width, label="Antidiagonal", color="green")

# Adding labels and title with increased font size
axes.set_xlabel("Fiber Segment counts", fontsize=18)
axes.set_ylabel("Average expected QBER", fontsize=18)
axes.set_title("Expected QBERs for Different Segment counts", fontsize=22)
axes.legend(loc="upper left", fontsize=16)

# Setting y-axis limits
axes.set_ylim(0.0, 1.0)

# Adding grid with specified line thicknesses
# To ensure no grid lines are shown for the x-axis, we set x-axis major and minor grid lines explicitly to False.
axes.yaxis.grid(True, which="both")
axes.grid(which="minor", linewidth=0.5, linestyle="-", color="gray", axis="y")
axes.grid(which="major", linewidth=1.0, linestyle="-", color="black", axis="y")

# Setting minor ticks
axes.set_yticks([i * 0.1 for i in range(11)], minor=True)
axes.set_yticks([i * 0.5 for i in range(3)], minor=False)

# Make it so the values on the x-axis are not the same as the progress values, but 1000, 10000, 100000, 1000000.
# Here we set the x-axis ticks to match the fiber lengths and adjust their labels accordingly.
axes.set_xticks(arange(max_progress / 8, max_progress, max_progress / 4))
axes.set_xticklabels([1000, 10000, 100000, 1000000], fontsize=14)

# Increase font size for y-axis tick labels
axes.tick_params(axis="y", labelsize=14)

# Show the plot
plt.tight_layout()
plt.show()
