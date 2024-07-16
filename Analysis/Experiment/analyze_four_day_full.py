from PyPola.Analysis.Experiment.analysis_mode_dialog import AnalysisMode, get_selected_mode
from PyPola.utilities.general_utilities import progress_bar
from PyPola.utilities.analysis_utilities import (
    get_qber_data, extract_datetime_from_interval_file, print_measurement_and_qber_attributes,
    plot_stokes_parameters_and_qber_data,
)
from numpy import array, load, save, set_printoptions
from os import path

# Set the float print options to suppress scientific notation and use maximum precision
set_printoptions(suppress=True, precision=16)
nr_of_files = 193


def get_four_day_file(index: int):
    if 0 <= index < nr_of_files:
        return f"MeasurementData/FourDayMeasurement/four_day_measurement_{index}.txt"
    raise ValueError("Index out of range")


def get_partial_data_array(dataset: str, index: int):
    if 0 <= index < nr_of_files:
        arrays_location = dataset[0].upper() + dataset[1:] + "Arrays"
        return f"PreprocessedData/FourDayData/{arrays_location}/partial_{dataset}_array_{index}.npy"
    raise ValueError("Index out of range")


########################################################################################################################
analysis_mode = get_selected_mode()
########################################################################################################################

if analysis_mode != AnalysisMode.PREPROCESSED_DISPLAY:
    full_time_data_path = f"PreprocessedData/FourDayData/TimeArrays/full_time_array.npy"
    full_s1_data_path = f"PreprocessedData/FourDayData/S1Arrays/full_s1_array.npy"
    full_s2_data_path = f"PreprocessedData/FourDayData/S2Arrays/full_s2_array.npy"
    full_s3_data_path = f"PreprocessedData/FourDayData/S3Arrays/full_s3_array.npy"

    if analysis_mode == AnalysisMode.SAMPLING:
        full_time_array = []
        full_s1_array = []
        full_s2_array = []
        full_s3_array = []

        progress = progress_bar(nr_of_points=nr_of_files, message="Reading maximum sampling data...")
        for i in range(nr_of_files):
            partial_time_array = []
            partial_s1_array = []
            partial_s2_array = []
            partial_s3_array = []

            datafile, date, time = extract_datetime_from_interval_file(file=open(get_four_day_file(i), "r"))
            t0_unintialized = True
            t0 = 0

            for line in datafile:
                # Theoretically the values are aranged like this:
                # t, power, s1, s2, s3, dop, dop_avg
                t, s1, s2, s3 = [float(item) for item in line.split(",")]
                full_time_array.append(t)
                full_s1_array.append(s1)
                full_s2_array.append(s2)
                full_s3_array.append(s3)

                if t0_unintialized:
                    t0 = t
                    t0_unintialized = False

                partial_time_array.append(t - t0)
                partial_s1_array.append(s1)
                partial_s2_array.append(s2)
                partial_s3_array.append(s3)
            datafile.close()

            # Round up the time values so that the plot displays the x-axis correctly
            partial_time_array[0] = 0.0

            partial_time_data_path = get_partial_data_array("time", i)
            partial_s1_data_path = get_partial_data_array("s1", i)
            partial_s2_data_path = get_partial_data_array("s2", i)
            partial_s3_data_path = get_partial_data_array("s3", i)
            partial_qber_data_path = get_partial_data_array("qber", i)

            save(partial_time_data_path, array(partial_time_array))
            save(partial_s1_data_path, array(partial_s1_array))
            save(partial_s2_data_path, array(partial_s2_array))
            save(partial_s3_data_path, array(partial_s3_array))

            progress.update()
        # Round up the time values so that the plot displays the x-axis correctly
        # noinspection ALL
        full_time_array[0] = 0.0
        progress.close()

        save(full_time_data_path, array(full_time_array))
        print("Time data saved.")
        save(full_s1_data_path, array(full_s1_array))
        print("S1 data saved.")
        save(full_s2_data_path, array(full_s2_array))
        print("S2 data saved.")
        save(full_s3_data_path, array(full_s3_array))
        print("S3 data saved.")
        exit()

    full_qber_data_path = f"PreprocessedData/FourDayData/QberArrays/full_qber_array.npy"
    stokes_data_sampled = (
            path.exists(full_time_data_path) and
            path.exists(full_s1_data_path) and
            path.exists(full_s2_data_path) and
            path.exists(full_s3_data_path)
    )
    if analysis_mode == AnalysisMode.QBER_COMPUTATION:
        if not stokes_data_sampled:
            exit("NO STOKES DATA SAMPLED!")

        full_s1_array = load(full_s1_data_path)
        print("S1 data loaded.")
        full_s2_array = load(full_s2_data_path)
        print("S2 data loaded.")
        full_s3_array = load(full_s3_data_path)
        print("S3 data loaded.")
        full_qber_array = get_qber_data(full_s1_array, full_s2_array, full_s3_array)
        save(full_qber_data_path, array(full_qber_array))

        for i in range(nr_of_files):
            print(f"Partial QBER array {i + 1}/{nr_of_files}")
            partial_s1_array_i = load(get_partial_data_array("s1", i))
            partial_s2_array_i = load(get_partial_data_array("s2", i))
            partial_s3_array_i = load(get_partial_data_array("s3", i))
            partial_qber_array_i = get_qber_data(partial_s1_array_i, partial_s2_array_i, partial_s3_array_i)

            partial_qber_data_path = get_partial_data_array("qber", i)
            save(partial_qber_data_path, array(partial_qber_array_i))
        print("QBER data saved.")
        exit()

    qber_data_sampled = path.exists(full_qber_data_path)
    if not stokes_data_sampled or not qber_data_sampled:
        exit("NO DATA SAMPLED!")

    full_time_array = load(full_time_data_path)
    print("Time data loaded.")
    full_s1_array = load(full_s1_data_path)
    print("S1 data loaded.")
    full_s2_array = load(full_s2_data_path)
    print("S2 data loaded.")
    full_s3_array = load(full_s3_data_path)
    print("S3 data loaded")
    full_qber_array = load(full_qber_data_path)
    print("QBER data loaded.\n")

    if analysis_mode == AnalysisMode.PLOTTING:
        plot_stokes_parameters_and_qber_data(
            time_array=[t / 3600 for t in full_time_array],
            s1_array=full_s1_array,
            s2_array=full_s2_array,
            s3_array=full_s3_array,
            qber_array=full_qber_array,
            time_unit="h",
            sample_size=None,
            stokes_x_lims=(0, 96),
            stokes_y_lims=(-1.1, 1.1),
            qber_x_lims=(0, 96),
            qber_y_lims=(0, 36),
            stokes_x_grid_spacing=12,
            stokes_y_grid_spacing=0.25,
            qber_x_grid_spacing=12,
            qber_y_grid_spacing=3,
            measurement_name="4-Day measurement",
            plot_sqrt_fit=True,
            time_scaling=3600
        )
        exit()

    if analysis_mode == AnalysisMode.ATTRIBUTE_COMPUTATION:
        print_measurement_and_qber_attributes(
            s1_array=full_s1_array,
            s2_array=full_s2_array,
            s3_array=full_s3_array,
            qber_array=full_qber_array
        )
        exit()

print("""
S1_min=-0.0858
S1_avg=0.30703448627831537
S1_max=0.645

S2_min=-0.1521
S2_avg=0.6188883728832887
S2_max=0.7448

S3_min=-0.9947
S3_avg=-0.6779319487318586
S3_max=-0.4413

S1=0.307±0.000
S2=0.619±0.000
S3=-0.678±0.000

Max S1 fluctuation: 0.0646
Max S2 fluctuation: 0.2594
Max S3 fluctuation: 0.0333

Maximum QBER: 34.0929212958%

Square root fit plot for plot QBER of 4-Day measurement:
t in seconds
f(t)=a*sqrt(t/s)
a=0.05536616467097066±5.508001213299877e-07
a=0.055366±0.000001

sqrt_params=[0.0553661646709707]
sqrt_cov=[[3.033807736571292e-13]]  
""")
