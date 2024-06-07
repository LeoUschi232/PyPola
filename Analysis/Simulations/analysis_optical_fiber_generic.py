from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber
from PyPola.utilities.stokes_vector import StokesVector
from numpy import pi, array, zeros, min, max, abs, dot
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
    timepoints = array(range(1, nr_of_timepoints + 1))

    print(f"Measuring output Stokes vectors")
    sleep(0.1)
    progress_bar = taquadum(total=nr_of_timepoints)
    for i in timepoints:
        optical_fiber.fluctuate_pmd()
        output_stokes_vector = optical_fiber.pass_stokes_vector(input_stokes_vector)

        s1_array.append(output_stokes_vector.s1)
        s2_array.append(output_stokes_vector.s2)
        s3_array.append(output_stokes_vector.s3)
        dop_array.append(output_stokes_vector.degree_of_polarization)
        angle_array.append(0.5 * output_stokes_vector.double_orientation_angle)

        progress_bar.set_postfix({"Measurement": f"{i}/{nr_of_timepoints}"})
        progress_bar.update()
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


def get_qber_between_steps(measurements, qber_threshold: float = 0.03):
    reference_sv = [measurements[1][0], measurements[2][0], measurements[3][0]]
    print(f"Reconfiguration of polarization controller after t=0")

    qbers = [0]
    compensation_timestamps = [0]
    for t in range(1, len(measurements[0])):
        sv2 = array([measurements[1][t], measurements[2][t], measurements[3][t]])
        sv1_dotp_sv2 = dot(reference_sv, sv2)
        qber = 0.5 * (1 - sv1_dotp_sv2)
        qbers.append(qber)
        if sv1_dotp_sv2 < 1 - 2 * qber_threshold:
            reference_sv = sv2
            compensation_timestamps.append(t)
            print(f"\nQBER:", round(100 * qber, 2), "%")
            print(f"Reconfiguration of polarization controller after t={t}")
            print(f"New reference vector:\n{reference_sv}")

    return qbers, compensation_timestamps


measured_arrays = get_results_from_measurement(
    nr_of_fiber_segments=10000,
    nr_of_timepoints=10000,
    input_stokes_vector=StokesVector(s0=1, s1=1, s2=0, s3=0)
)
plot_measurements(measured_arrays)
qbers, compensation_timestamps = get_qber_between_steps(
    measurements=measured_arrays,
    qber_threshold=0.05
)
avg_timesteps_between_compensations = round(10000 / len(compensation_timestamps))
print(f"\nAverage timesteps between compensations: {avg_timesteps_between_compensations}")
