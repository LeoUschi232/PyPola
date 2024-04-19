from PyPola.Utilities.polarization_utilities import (
    random_polarized_stokes_vector, degree_of_polarization, get_angle_to_x_axis
)
from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber, segment_variation
from numpy import pi, cos, sin, linspace, array, zeros, min, max, abs
from tqdm import tqdm as taquadum
from matplotlib import pyplot as plt
from time import sleep


def get_results_from_measurement(nr_of_fiber_segments, nr_of_timepoints, input_stokes_vector):
    optical_fiber = OpticalFiber(nr_of_segments=nr_of_fiber_segments)
    s1_array = []
    s2_array = []
    s3_array = []
    dop_array = []
    angle_array = []
    timepoints = array([i for i in range(1, nr_of_timepoints + 1)])

    print(f"Measuring output Stokes vectors")
    sleep(0.1)
    progress_bar = taquadum(total=nr_of_timepoints)
    for i in timepoints:
        optical_fiber.fluctuate_pmd()
        output_stokes_vector = optical_fiber.pass_stokes_vector(input_stokes_vector)

        s1_array.append(output_stokes_vector[1][0])
        s2_array.append(output_stokes_vector[2][0])
        s3_array.append(output_stokes_vector[3][0])
        dop_array.append(degree_of_polarization(output_stokes_vector))
        angle_array.append(get_angle_to_x_axis(output_stokes_vector))

        progress_bar.set_postfix({
            "Measurement": f"{i}/{nr_of_timepoints}"
        }, refresh=True)
        progress_bar.update(1)
    progress_bar.close()
    print("Measurement complete.")
    return timepoints, s1_array, s2_array, s3_array, dop_array, angle_array


def plot_measurements(measurements):
    timepoints = array(measurements[0])
    nr_of_timepoints = len(timepoints)

    s1_array = array(measurements[1])
    s2_array = array(measurements[2])
    s3_array = array(measurements[3])
    unaligned_angle_array = array(measurements[5])
    aligned_angle_array = align_angles(measurements[5])

    plt.subplot(2, 1, 1)
    plt.plot(timepoints, s1_array, color="blue", label="S1")
    plt.plot(timepoints, s2_array, color="red", label="S2")
    plt.plot(timepoints, s3_array, color="green", label="S3")
    plt.plot(timepoints, zeros(shape=timepoints.shape), color="black")
    plt.xlabel(f"Time")
    plt.ylabel(f"Stokes Parameters")
    plt.xlim([0, nr_of_timepoints])
    plt.ylim([-1, 1])
    plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
    plt.legend(loc="upper left")

    plt.subplot(2, 1, 2)
    plt.plot(timepoints, unaligned_angle_array, color="gold", label="Unaligned angle to fiber's x-axis")
    plt.plot(timepoints, aligned_angle_array, color="purple", label="Aligned angle to fiber's x-axis")
    plt.plot(timepoints, zeros(shape=timepoints.shape), color="black")
    plt.xlabel(f"Time")
    plt.ylabel(f"Angle to fiber's x-axis")
    plt.xlim([0, nr_of_timepoints])
    plt.ylim([
        min([min(unaligned_angle_array), min(aligned_angle_array)]),
        max([max(unaligned_angle_array), max(aligned_angle_array)])
    ])
    plt.grid(color="gray", linestyle="dotted", linewidth=0.5)
    plt.legend(loc="upper left")

    plt.show()


def align_angles(angle_array):
    array_size = len(angle_array)
    shift_tolerance = 0.8 * pi

    for i in range(1, array_size):
        if angle_array[i] - angle_array[i - 1] > shift_tolerance:
            # Handle jumping upwards
            # All further values should be shifted down
            for j in range(i, array_size):
                angle_array[j] -= pi
        elif angle_array[i] - angle_array[i - 1] < -shift_tolerance:
            # Handle jumping downwards
            # All further values should be shifted up
            for j in range(i, array_size):
                angle_array[j] += pi

    max_difference = 0.0
    for i in range(1, array_size):
        max_difference = max([max_difference, abs(angle_array[i] - angle_array[i - 1])])
    print(F"Angle maximum difference: {max_difference}\n")

    return array(angle_array)


measured_arrays = get_results_from_measurement(
    nr_of_fiber_segments=10000,
    nr_of_timepoints=1000000,
    input_stokes_vector=[[1], [1], [0], [0]]
)
plot_measurements(measured_arrays)
