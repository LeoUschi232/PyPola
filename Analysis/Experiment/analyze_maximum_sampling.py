from PyPola.Analysis.Experiment.analysis_mode_dialog import AnalysisMode, get_selected_mode
from PyPola.utilities.general_utilities import progress_bar
from PyPola.utilities.analysis_utilities import (
    get_qber_data, extract_datetime_from_polaview_file, print_measurement_and_qber_attributes,
    plot_stokes_parameters_and_qber_data,
)
from numpy import array, load, save, set_printoptions
from numpy.linalg import norm
from os import path

# Set the float print options to suppress scientific notation and use maximum precision
set_printoptions(suppress=True, precision=16)
nr_of_files = 1200


def get_maximum_sampling_file(index: int):
    if 0 <= index < nr_of_files:
        return f"MeasurementData/MaximumSamplingMeasurement/maximum_sampling_measurement_{index}.txt"
    raise ValueError("Index out of range")


########################################################################################################################
analysis_mode = get_selected_mode()
########################################################################################################################

if analysis_mode != AnalysisMode.PREPROCESSED_DISPLAY:
    time_data_path = f"PreprocessedData/MaximumSamplingData/time_array.npy"
    s1_data_path = f"PreprocessedData/MaximumSamplingData/s1_array.npy"
    s2_data_path = f"PreprocessedData/MaximumSamplingData/s2_array.npy"
    s3_data_path = f"PreprocessedData/MaximumSamplingData/s3_array.npy"

    if analysis_mode == AnalysisMode.SAMPLING:
        time_array = []
        s1_array = []
        s2_array = []
        s3_array = []

        progress = progress_bar(nr_of_points=nr_of_files, message="Reading maximum sampling data...")
        for i in range(nr_of_files):
            datafile, date, time = extract_datetime_from_polaview_file(file=open(get_maximum_sampling_file(i), "r"))

            for line in datafile:
                # Theoretically the values are aranged like this:
                # t, power, s1, s2, s3, dop, dop_avg
                t, _, s1, s2, s3, _, _ = [float(item) for item in line.split("\t")]

                time_array.append(t)
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

    qber_data_path = f"PreprocessedData/MaximumSamplingData/qber_array.npy"
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
            time_unit="ms",
            sample_size=10,
            stokes_x_lims=(0, 15000),
            stokes_y_lims=(-1.1, 1.1),
            qber_x_lims=(0, 15000),
            qber_y_lims=(0, 0.16),
            stokes_x_grid_spacing=3000,
            stokes_y_grid_spacing=0.25,
            qber_x_grid_spacing=3000,
            qber_y_grid_spacing=0.02,
            measurement_name="Maximum Sampling measurement",
            plot_sqrt_fit=True,
            time_scaling=0.001
        )
        exit()

    if analysis_mode == AnalysisMode.ATTRIBUTE_COMPUTATION:
        print_measurement_and_qber_attributes(s1_array, s2_array, s3_array, qber_array)
        exit()

print("""
S1_min=0.45146
S1_avg=0.49363423217549723
S1_max=0.5099

S2_min=0.07974
S2_avg=0.10732214704150032
S2_max=0.15525

S3_min=0.85284
S3_avg=0.8629966314845005
S3_max=0.88061

S1=0.494±0.000
S2=0.107±0.000
S3=0.863±0.000

Max S1 fluctuation: 0.00345
Max S2 fluctuation: 0.00405
Max S3 fluctuation: 0.00193

Maximum QBER: 0.1471482838%

Square root fit plot for plot QBER of Maximum Sampling measurement:
t in seconds
f(t)=a*sqrt(t/s)
a=0.03439195011382412±1.4223027222730799e-06
a=0.034392±0.000001

sqrt_params=[0.0343919501138241]
sqrt_cov=[[2.0229450337854137e-12]]
""")
