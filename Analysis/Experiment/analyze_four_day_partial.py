from PyPola.utilities.analysis_utilities import plot_stokes_parameters_and_qber_data, get_qber_data
from numpy import concatenate, load, set_printoptions, array

# Set the float print options to suppress scientific notation and use maximum precision
set_printoptions(suppress=True, precision=16)

time_data_path_0 = f"PreprocessedData/FourDayData/TimeArrays/partial_time_array_0.npy"
s1_data_path_0 = f"PreprocessedData/FourDayData/S1Arrays/partial_s1_array_0.npy"
s2_data_path_0 = f"PreprocessedData/FourDayData/S2Arrays/partial_s2_array_0.npy"
s3_data_path_0 = f"PreprocessedData/FourDayData/S3Arrays/partial_s3_array_0.npy"
qber_data_path_0 = f"PreprocessedData/FourDayData/QberArrays/partial_qber_array_0.npy"

time_data_path_1 = f"PreprocessedData/FourDayData/TimeArrays/partial_time_array_1.npy"
s1_data_path_1 = f"PreprocessedData/FourDayData/S1Arrays/partial_s1_array_1.npy"
s2_data_path_1 = f"PreprocessedData/FourDayData/S2Arrays/partial_s2_array_1.npy"
s3_data_path_1 = f"PreprocessedData/FourDayData/S3Arrays/partial_s3_array_1.npy"
qber_data_path_1 = f"PreprocessedData/FourDayData/QberArrays/partial_qber_array_1.npy"

time_data_path_127 = f"PreprocessedData/FourDayData/TimeArrays/partial_time_array_127.npy"
s1_data_path_127 = f"PreprocessedData/FourDayData/S1Arrays/partial_s1_array_127.npy"
s2_data_path_127 = f"PreprocessedData/FourDayData/S2Arrays/partial_s2_array_127.npy"
s3_data_path_127 = f"PreprocessedData/FourDayData/S3Arrays/partial_s3_array_127.npy"
qber_data_path_127 = f"PreprocessedData/FourDayData/QberArrays/partial_qber_array_127.npy"

time_data_path_185 = f"PreprocessedData/FourDayData/TimeArrays/partial_time_array_185.npy"
s1_data_path_185 = f"PreprocessedData/FourDayData/S1Arrays/partial_s1_array_185.npy"
s2_data_path_185 = f"PreprocessedData/FourDayData/S2Arrays/partial_s2_array_185.npy"
s3_data_path_185 = f"PreprocessedData/FourDayData/S3Arrays/partial_s3_array_185.npy"
qber_data_path_185 = f"PreprocessedData/FourDayData/QberArrays/partial_qber_array_185.npy"

partial_time_array_0 = load(time_data_path_0)
partial_s1_array_0 = load(s1_data_path_0)
partial_s2_array_0 = load(s2_data_path_0)
partial_s3_array_0 = load(s3_data_path_0)
partial_qber_array_0 = load(qber_data_path_0)

partial_time_array_1 = load(time_data_path_1)
partial_s1_array_1 = load(s1_data_path_1)
partial_s2_array_1 = load(s2_data_path_1)
partial_s3_array_1 = load(s3_data_path_1)
partial_qber_array_1 = load(qber_data_path_1)

partial_time_array_127 = load(time_data_path_127)
partial_s1_array_127 = load(s1_data_path_127)
partial_s2_array_127 = load(s2_data_path_127)
partial_s3_array_127 = load(s3_data_path_127)
partial_qber_array_127 = load(qber_data_path_127)

partial_time_array_185 = load(time_data_path_185)
partial_s1_array_185 = load(s1_data_path_185)
partial_s2_array_185 = load(s2_data_path_185)
partial_s3_array_185 = load(s3_data_path_185)
partial_qber_array_185 = load(qber_data_path_185)

# Before each concatenation shift the second array's time by half an hour
# against the measurement which came before
anomalous_time_array_01 = concatenate((partial_time_array_0, array([
    t + 1800 for t in partial_time_array_1
])))
anomalous_s1_array_01 = concatenate((partial_s1_array_0, partial_s1_array_1))
anomalous_s2_array_01 = concatenate((partial_s2_array_0, partial_s2_array_1))
anomalous_s3_array_01 = concatenate((partial_s3_array_0, partial_s3_array_1))
anomalous_qber_array_01 = get_qber_data(
    s1_array=anomalous_s1_array_01,
    s2_array=anomalous_s2_array_01,
    s3_array=anomalous_s3_array_01
)

stokes_y_lims = (-1.1, 1.1)
plot_stokes_parameters_and_qber_data(
    time_array=anomalous_time_array_01,
    s1_array=anomalous_s1_array_01,
    s2_array=anomalous_s2_array_01,
    s3_array=anomalous_s3_array_01,
    qber_array=anomalous_qber_array_01,
    time_unit="s",
    sample_size=None,
    stokes_x_lims=(0, 2100),
    stokes_y_lims=(-1.1, 1.1),
    qber_x_lims=(0, 2100),
    qber_y_lims=(0, 3),
    stokes_x_grid_spacing=300,
    stokes_y_grid_spacing=0.25,
    qber_x_grid_spacing=300,
    qber_y_grid_spacing=0.5,
    measurement_name="anomaly between intervals 0 and 1",
    plot_sqrt_fit=False,
)
plot_stokes_parameters_and_qber_data(
    time_array=partial_time_array_127,
    s1_array=partial_s1_array_127,
    s2_array=partial_s2_array_127,
    s3_array=partial_s3_array_127,
    qber_array=partial_qber_array_127,
    time_unit="s",
    stokes_x_lims=(130, 140),
    stokes_y_lims=(-1.1, 1.1),
    qber_x_lims=(130, 140),
    qber_y_lims=(0, 0.3),
    stokes_x_grid_spacing=5,
    stokes_y_grid_spacing=0.25,
    qber_x_grid_spacing=5,
    qber_y_grid_spacing=0.05,
    measurement_name="anomaly during interval 127",
    plot_sqrt_fit=False,
)
plot_stokes_parameters_and_qber_data(
    time_array=partial_time_array_185,
    s1_array=partial_s1_array_185,
    s2_array=partial_s2_array_185,
    s3_array=partial_s3_array_185,
    qber_array=partial_qber_array_185,
    time_unit="s",
    stokes_x_lims=(0, 3.0),
    stokes_y_lims=(-1.1, 1.1),
    qber_x_lims=(0, 3.0),
    qber_y_lims=(0, 0.3),
    stokes_x_grid_spacing=0.5,
    stokes_y_grid_spacing=0.25,
    qber_x_grid_spacing=0.5,
    qber_y_grid_spacing=0.05,
    measurement_name="anomaly during interval 185",
    plot_sqrt_fit=False,
)
