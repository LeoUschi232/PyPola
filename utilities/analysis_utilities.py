from PyPola.utilities.general_utilities import progress_bar
from _io import TextIOWrapper
from numpy import array, std, sqrt, log, linspace, dot, concatenate, set_printoptions
from numpy.linalg import norm
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from re import search


def distance(v1, v2):
    return norm(array(v1) - array(v2))


def logarithmic_fit(x, a, b, c, d):
    return a * log(b * x + c) + d


def square_root_fit(x, a):
    return a * sqrt(x)


def linear_fit(x, a):
    return a * x


def check_file_format(line_number: int, expected: str, actual: str):
    if actual.startswith(expected):
        return
    error_message = (
        f"File error:\n"
        f"Invalid format on line {line_number}.\n"
        f"Expected: {expected}\n"
        f"     Got: {actual}\n"
    )
    raise ValueError(error_message)


def extract_datetime_from_polaview_file(file: TextIOWrapper):
    date_match = search(r"Start Date: (\d{1,2}/\d{1,2}/\d{4})", file.readline())
    time_match = search(r"Start Time: (\d{1,2}:\d{1,2}:\d{1,2})", file.readline())

    if not date_match or not time_match:
        raise ValueError("Could not extract date and time from PolaView file.")

    month, day, year = date_match.group(1).split("/")
    date = f"{day}-{month}-{year}"
    time = time_match.group(1)

    expected_headers = [
        "Test system information",
        "",
        "Capture mode",
        "Total sampling numbers",
        "Time Interval",
        "Wavelength",
        "SOP sampling rate",
        "Integeration time",
        "Scrambler DOP Average Number",
        "Trace sensitivity",
        "Calibration matrix",
        "",
        "--Time"
    ]
    for line_nr, header in enumerate(expected_headers, start=3):
        check_file_format(line_number=line_nr, expected=header, actual=file.readline())

    return file, date, time


def extract_datetime_from_interval_file(file: TextIOWrapper):
    check_file_format(line_number=1, expected="Measurement begin:", actual=file.readline())
    date_string, time_string = file.readline().strip().split()
    year, month, day = date_string.split("-")
    check_file_format(line_number=3, expected="", actual=file.readline())
    check_file_format(line_number=4, expected="Time,S1,S2,S3", actual=file.readline())
    return file, f"{day}/{month}/{year}", time_string[:8]


def get_min_max_mean_stddev(si_array):
    si_min = si_array.min()
    si_max = si_array.max()
    si_average = si_array.mean()
    si_standard_deviation = std(si_array, ddof=1) / sqrt(len(si_array))
    return si_min, si_max, si_average, si_standard_deviation


def get_sampled_stokes_parameters(
        time_array,
        s1_array,
        s2_array,
        s3_array,
        sample_size: int
):
    if sample_size < 1:
        print(f"Invalid sampling fed into the plot_sampled_data function (sample_size={sample_size}).")
        print("Defaulting to sample_size=1")
        return time_array, s1_array, s2_array, s3_array

    n = len(time_array)
    sample_coherence = n % sample_size
    if sample_coherence != 0:
        print("Sample size incoherent with data size")
        print("Hang on tight while the data is transformed...")

        avg_timestep = (time_array[-1] - time_array[0]) / len(time_array)

        additional_size = sample_size - sample_coherence
        time_extension = linspace(
            time_array[-1] + avg_timestep,
            time_array[-1] + avg_timestep * additional_size,
            additional_size
        )

        time_array = concatenate((time_array, time_extension))
        s1_array = concatenate((s1_array, array([s1_array[-1]] * additional_size)))
        s2_array = concatenate((s2_array, array([s2_array[-1]] * additional_size)))
        s3_array = concatenate((s3_array, array([s3_array[-1]] * additional_size)))

    t_plottable = [0]
    s1_plottable = [s1_array[0]]
    s2_plottable = [s2_array[0]]
    s3_plottable = [s3_array[0]]

    progress = progress_bar(nr_of_points=n, message="Sampling Stokes parameters...")
    for i in range(0, n, sample_size):
        t_sample = time_array[i:i + sample_size]
        s1_sample = s1_array[i:i + sample_size]
        s2_sample = s2_array[i:i + sample_size]
        s3_sample = s3_array[i:i + sample_size]
        t_plottable.append(t_sample.mean())
        s1_plottable.append(s1_sample.mean())
        s2_plottable.append(s2_sample.mean())
        s3_plottable.append(s3_sample.mean())
        progress.update(sample_size)
    progress.close()

    t_plottable.append(time_array[-1])
    s1_plottable.append(s1_array[-1])
    s2_plottable.append(s2_array[-1])
    s3_plottable.append(s3_array[-1])
    return t_plottable, s1_plottable, s2_plottable, s3_plottable


def get_sampled_qber(time_array, qber_array, sample_size: int):
    if sample_size < 1:
        print(f"Invalid sampling fed into the plot_sampled_data function (sample_size={sample_size}).")
        print("Defaulting to sample_size=1")
        return time_array, qber_array

    n = len(time_array)
    sample_coherence = n % sample_size
    if sample_coherence != 0:
        print("Sample size incoherent with data size")
        print("Hang on tight while the data is transformed...")

        avg_timestep = (time_array[-1] - time_array[0]) / len(time_array)

        additional_size = sample_size - sample_coherence
        time_extension = linspace(
            time_array[-1] + avg_timestep,
            time_array[-1] + avg_timestep * additional_size,
            additional_size
        )

        time_array = concatenate((time_array, time_extension))
        qber_array = concatenate((qber_array, array([qber_array[-1]] * additional_size)))

    t_plottable = [0]
    qber_plottable = [qber_array[0]]

    progress = progress_bar(nr_of_points=n, message="Sampling QBER...")
    for i in range(0, n, sample_size):
        t_sample = time_array[i:i + sample_size]
        qber_sample = qber_array[i:i + sample_size]
        t_plottable.append(t_sample.mean())
        qber_plottable.append(qber_sample.mean())
        progress.update(sample_size)
    progress.close()

    t_plottable.append(time_array[-1])
    qber_plottable.append(qber_array[-1])
    return t_plottable, qber_plottable


def plot_stokes_parameters(
        time_array,
        s1_array,
        s2_array,
        s3_array,
        time_unit,
        sample_size=None,
        x_lims=None,
        y_lims=None,
        x_grid_spacing=None,
        y_grid_spacing=None,
        title=None
):
    if sample_size is not None and sample_size > 1:
        time_array, s1_array, s2_array, s3_array = get_sampled_stokes_parameters(
            time_array, s1_array, s2_array, s3_array, sample_size
        )

    plt.figure(figsize=(10, 7))
    plt.plot(time_array, s1_array, color="red", label="$S_1$")
    plt.plot(time_array, s2_array, color="blue", label="$S_2$")
    plt.plot(time_array, s3_array, color="green", label="$S_3$")

    if title is not None:
        plt.title(title, fontsize=20)

    plt.xlim(time_array[0], time_array[-1])
    plt.ylim(-1.1, 1.1)
    if x_lims is not None:
        plt.xlim(*x_lims)
    if y_lims is not None:
        plt.ylim(*y_lims)

    plt.tick_params(axis="both", which="major", labelsize=14)
    plt.xlabel("Time $t\\,\\mathrm{[" + str(time_unit) + "]}$", fontsize=18)
    plt.ylabel("Stokes Parameters", fontsize=18)
    plt.legend(fontsize=18)

    plt.grid(True)
    if x_grid_spacing is not None:
        plt.gca().xaxis.set_major_locator(plt.MultipleLocator(x_grid_spacing))
        plt.grid(True, which="major", axis="x", linestyle="-", linewidth=0.5)
    if y_grid_spacing is not None:
        plt.gca().yaxis.set_major_locator(plt.MultipleLocator(y_grid_spacing))
        plt.grid(True, which="major", axis="y", linestyle="-", linewidth=0.5)

    plt.show()


def analyze_stokes_parameter_data(s1_array, s2_array, s3_array):
    s1_array = array(s1_array)
    s2_array = array(s2_array)
    s3_array = array(s3_array)

    s1_min, s1_max, s1_average, s1_standard_daviation = get_min_max_mean_stddev(s1_array)
    s2_min, s2_max, s2_average, s2_standard_daviation = get_min_max_mean_stddev(s2_array)
    s3_min, s3_max, s3_average, s3_standard_daviation = get_min_max_mean_stddev(s3_array)

    print(f"S1_min={s1_min}")
    print(f"S1_avg={s1_average}")
    print(f"S1_max={s1_max}\n")

    print(f"S2_min={s2_min}")
    print(f"S2_avg={s2_average}")
    print(f"S2_max={s2_max}\n")

    print(f"S3_min={s3_min}")
    print(f"S3_avg={s3_average}")
    print(f"S3_max={s3_max}\n")

    print(f"S1={s1_average:0.3f}±{s1_standard_daviation:0.3f}")
    print(f"S2={s2_average:0.3f}±{s2_standard_daviation:0.3f}")
    print(f"S3={s3_average:0.3f}±{s3_standard_daviation:0.3f}\n")


def get_qber_data(s1_array, s2_array, s3_array):
    if len(s1_array) != len(s2_array) or len(s2_array) != len(s3_array):
        print("Invalid Stokes parameter data fed into the get_qber_data function.")
        return

    n = len(s1_array)
    qber_array = []
    s_ref = array([s1_array[0], s2_array[0], s3_array[0]])
    s_ref = s_ref / norm(s_ref)

    progress = progress_bar(nr_of_points=n, message="Computing QBER...")
    for i in range(n):
        s_quant = array([s1_array[i], s2_array[i], s3_array[i]])
        s_quant = s_quant / norm(s_quant)

        # The QBER is not expected to be negtive but due to float precision errors,
        # the computed QBER might be evaluated to be negative.
        # In that case we just take the zero
        qber = 50 * (1 - dot(s_ref, s_quant))
        qber_array.append(max(0, qber))

        progress.update()
    progress.close()

    return array(qber_array)


def get_max_qber_data(time_array, qber_array):
    if len(time_array) != len(qber_array):
        print("time_array length:", len(time_array))
        print("qber_array length:", len(qber_array))
        exit("Invalid QBER data fed into the get_max_qber_data function.")

    n = len(time_array)
    max_qber = 0
    max_time_array = [time_array[0]]
    max_qber_array = [0]
    for i in range(n):
        if qber_array[i] > max_qber:
            max_qber = qber_array[i]
            max_time_array.append(time_array[i])
            max_qber_array.append(max_qber)
    max_time_array.append(time_array[-1])
    max_qber_array.append(max_qber)
    return array(max_time_array), array(max_qber_array)


def plot_qber_data(
        time_array,
        qber_array,
        time_unit,
        sample_size=None,
        x_lims=None,
        y_lims=None,
        x_grid_spacing=None,
        y_grid_spacing=None,
        title=None,
        plot_sqrt_fit=False,
        time_scaling=None
):
    if sample_size is not None and sample_size > 1:
        time_array, qber_array = get_sampled_qber(time_array, qber_array, sample_size)

    max_time_array, max_qber_array = get_max_qber_data(time_array, qber_array)

    plt.figure(figsize=(10, 7))

    if title is not None:
        plt.title(title, fontsize=20)

    if plot_sqrt_fit:
        plt.plot(time_array, qber_array, color="yellow", label="QBER")

        scaled_time_array = time_array
        if time_scaling is not None:
            scaled_time_array = array([time_scaling * t for t in time_array])
        # noinspection ALL
        sqrt_params, sqrt_cov = curve_fit(square_root_fit, scaled_time_array, qber_array)

        a_main = sqrt_params[0]
        a_error = sqrt(sqrt_cov[0, 0])
        print(f"Square root fit plot for plot {title}:")
        print(f"t in seconds")
        print("f(t)=a*sqrt(t/s)")
        print(f"a={a_main}±{a_error}")
        print(f"a={a_main:0.6f}±{a_error:0.6f}\n")

        set_printoptions(suppress=False)
        print(f"sqrt_params={sqrt_params}")
        print(f"sqrt_cov={sqrt_cov}\n")
        set_printoptions(suppress=True, precision=16)

        first_t = int(scaled_time_array[0])
        final_t = int(scaled_time_array[-1]) + 1
        time_fit_array = linspace(first_t, final_t, 100 * final_t + 1)
        qber_sqrt_fit_array = square_root_fit(time_fit_array, *sqrt_params)
        if time_scaling is not None:
            time_fit_array = array([t / time_scaling for t in time_fit_array])

        plt.plot(time_fit_array, qber_sqrt_fit_array, color="darkorange", label="QBER Sqrt fit")
    else:
        plt.plot(time_array, qber_array, color="orange", label="QBER")

    plt.plot(max_time_array, max_qber_array, color="red", label="Max QBER")

    plt.xlim(time_array[0], time_array[-1])
    plt.ylim(0, 1.1 * max_qber_array[-1])
    if x_lims is not None:
        plt.xlim(*x_lims)
    if y_lims is not None:
        plt.ylim(*y_lims)

    plt.tick_params(axis="both", which="major", labelsize=14)

    plt.xlabel("Time $t\\,\\mathrm{[" + str(time_unit) + "]}$", fontsize=18)
    plt.ylabel("QBER $[\\%]$", fontsize=18)
    plt.legend(fontsize=18, loc="upper left")

    plt.grid(True)
    if x_grid_spacing is not None:
        plt.gca().xaxis.set_major_locator(plt.MultipleLocator(x_grid_spacing))
        plt.grid(True, which="major", axis="x", linestyle="-", linewidth=0.5)
    if y_grid_spacing is not None:
        plt.gca().yaxis.set_major_locator(plt.MultipleLocator(y_grid_spacing))
        plt.grid(True, which="major", axis="y", linestyle="-", linewidth=0.5)

    plt.show()


def plot_stokes_parameters_and_qber_data(
        time_array,
        s1_array,
        s2_array,
        s3_array,
        qber_array,
        time_unit,
        sample_size=None,
        stokes_x_lims=None,
        stokes_y_lims=None,
        qber_x_lims=None,
        qber_y_lims=None,
        stokes_x_grid_spacing=None,
        stokes_y_grid_spacing=None,
        qber_x_grid_spacing=None,
        qber_y_grid_spacing=None,
        measurement_name=None,
        plot_sqrt_fit=False,
        time_scaling=None
):
    plot_stokes_parameters(
        time_array=time_array,
        s1_array=s1_array,
        s2_array=s2_array,
        s3_array=s3_array,
        time_unit=time_unit,
        sample_size=sample_size,
        x_lims=stokes_x_lims,
        y_lims=stokes_y_lims,
        x_grid_spacing=stokes_x_grid_spacing,
        y_grid_spacing=stokes_y_grid_spacing,
        title=f"Stokes Parameters of {measurement_name}" if measurement_name is not None else None
    )
    plot_qber_data(
        time_array=time_array,
        qber_array=qber_array,
        time_unit=time_unit,
        sample_size=sample_size,
        x_lims=qber_x_lims,
        y_lims=qber_y_lims,
        x_grid_spacing=qber_x_grid_spacing,
        y_grid_spacing=qber_y_grid_spacing,
        title=f"QBER of {measurement_name}" if measurement_name is not None else None,
        plot_sqrt_fit=plot_sqrt_fit,
        time_scaling=time_scaling
    )


def compute_max_fluctuations(s1_array, s2_array, s3_array):
    progress = progress_bar(nr_of_points=len(s1_array), message="Analyzing Stokes parameter fluctuations...")

    max_s1_fluctuation = 0.0
    max_s2_fluctuation = 0.0
    max_s3_fluctuation = 0.0
    progress.update()

    for i in range(1, len(s1_array)):
        max_s1_fluctuation = max(max_s1_fluctuation, abs(s1_array[i] - s1_array[i - 1]))
        max_s2_fluctuation = max(max_s2_fluctuation, abs(s2_array[i] - s2_array[i - 1]))
        max_s3_fluctuation = max(max_s3_fluctuation, abs(s3_array[i] - s3_array[i - 1]))

        progress.update()
    progress.close()

    print(f"Max S1 fluctuation: {round(max_s1_fluctuation, 7)}")
    print(f"Max S2 fluctuation: {round(max_s2_fluctuation, 7)}")
    print(f"Max S3 fluctuation: {round(max_s3_fluctuation, 7)}\n")  #


def print_measurement_and_qber_attributes(s1_array, s2_array, s3_array, qber_array):
    analyze_stokes_parameter_data(s1_array, s2_array, s3_array)
    compute_max_fluctuations(s1_array, s2_array, s3_array)
    print(f"Maximum QBER: {round(qber_array.max(), 10)}%")
