from PyPola.Analysis.Experiment.analysis_mode_dialog import AnalysisMode, get_selected_mode
from PyPola.utilities.general_utilities import progress_bar
from PyPola.utilities.analysis_utilities import (
    get_qber_data, extract_datetime_from_polaview_file, print_measurement_and_qber_attributes,
    plot_stokes_parameters_and_qber_data,
)
from numpy import array, load, save, set_printoptions
from os import path

# Set the float print options to suppress scientific notation and use maximum precision
set_printoptions(suppress=True, precision=16)

nr_of_files = 600


def get_file_per_second_file(index: int):
    if 0 <= index < nr_of_files:
        return f"MeasurementData/FilePerSecondMeasurement/file_per_second_measurement_{index}.txt"
    raise ValueError("Index out of range")


########################################################################################################################
analysis_mode = get_selected_mode()
########################################################################################################################

if analysis_mode != AnalysisMode.PREPROCESSED_DISPLAY:
    time_data_path = f"PreprocessedData/FilePerSecondData/time_array.npy"
    s1_data_path = f"PreprocessedData/FilePerSecondData/s1_array.npy"
    s2_data_path = f"PreprocessedData/FilePerSecondData/s2_array.npy"
    s3_data_path = f"PreprocessedData/FilePerSecondData/s3_array.npy"

    if analysis_mode == AnalysisMode.SAMPLING:
        time_array = []
        s1_array = []
        s2_array = []
        s3_array = []

        progress = progress_bar(nr_of_points=nr_of_files, message="Reading file per second data...")
        for i in range(nr_of_files):
            datafile, date, time = extract_datetime_from_polaview_file(file=open(get_file_per_second_file(i), "r"))

            for line in datafile:
                # Theoretically the values are aranged like this:
                # t, power, s1, s2, s3, dop, dop_avg
                t, _, s1, s2, s3, _, _ = [float(item) for item in line.split("\t")]
                time_array.append(t / 1000)
                s1_array.append(s1)
                s2_array.append(s2)
                s3_array.append(s3)

            datafile.close()
            progress.update()
        progress.close()

        save(time_data_path, array(time_array))
        print("Time data saved.")
        save(s1_data_path, array(s1_array))
        print("S1 data saved.")
        save(s2_data_path, array(s2_array))
        print("S2 data saved.")
        save(s3_data_path, array(s3_array))
        print("S3 data saved.")
        exit()

    qber_data_path = f"PreprocessedData/FilePerSecondData/qber_array.npy"
    stokes_data_sampled = (
            path.exists(time_data_path) and
            path.exists(s1_data_path) and
            path.exists(s2_data_path) and
            path.exists(s3_data_path)
    )
    if analysis_mode == AnalysisMode.QBER_COMPUTATION:
        if not stokes_data_sampled:
            exit("NO STOKES DATA SAMPLED!")

        s1_array = load(s1_data_path)
        print("S1 data loaded.")
        s2_array = load(s2_data_path)
        print("S2 data loaded.")
        s3_array = load(s3_data_path)
        print("S3 data loaded.")
        qber_array = get_qber_data(s1_array, s2_array, s3_array)
        save(qber_data_path, array(qber_array))
        print("QBER data saved.")
        exit()

    qber_data_sampled = path.exists(qber_data_path)
    if not stokes_data_sampled or not qber_data_sampled:
        exit("NO DATA SAMPLED!")

    time_array = load(time_data_path)
    print("Time data loaded.")
    s1_array = load(s1_data_path)
    print("S1 data loaded.")
    s2_array = load(s2_data_path)
    print("S2 data loaded.")
    s3_array = load(s3_data_path)
    print("S3 data loaded")
    qber_array = load(qber_data_path)
    print("QBER data loaded.\n")

    if analysis_mode == AnalysisMode.PLOTTING:
        plot_stokes_parameters_and_qber_data(
            time_array=time_array,
            s1_array=s1_array,
            s2_array=s2_array,
            s3_array=s3_array,
            qber_array=qber_array,
            time_unit="s",
            sample_size=5,
            stokes_x_lims=(0, 600),
            stokes_y_lims=(-1.1, 1.1),
            qber_x_lims=(0, 600),
            qber_y_lims=(0, 0.1),
            stokes_x_grid_spacing=100,
            stokes_y_grid_spacing=0.25,
            qber_x_grid_spacing=100,
            qber_y_grid_spacing=0.02,
            measurement_name="10-Minute measurement",
            plot_sqrt_fit=True
        )
        exit()

    if analysis_mode == AnalysisMode.ATTRIBUTE_COMPUTATION:
        print_measurement_and_qber_attributes(s1_array, s2_array, s3_array, qber_array)
        exit()

print("""
S1_min=-0.04028
S1_avg=0.008838216720333338
S1_max=0.01923

S2_min=-0.88073
S2_avg=-0.8708954207930023
S2_max=-0.85229

S3_min=0.47377
S3_avg=0.49128657685700045
S3_max=0.52223

S1=0.009±0.000
S2=-0.871±0.000
S3=0.491±0.000

Max S1 fluctuation: 0.00326
Max S2 fluctuation: 0.00183
Max S3 fluctuation: 0.0032

Maximum QBER: 0.0915913211%

Square root fit plot for plot QBER of 10-Minute measurement:
t in seconds
f(t)=a*sqrt(t/s)
a=0.0036991634544139007±2.320571827364818e-07
a=0.003699±0.000000

sqrt_params=[0.0036991634544139]
sqrt_cov=[[5.3850536059592904e-14]]
""")
