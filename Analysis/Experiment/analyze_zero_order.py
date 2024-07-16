from numpy import float64
from PyPola.utilities.analysis_utilities import analyze_stokes_parameter_data

time_array = [0]
s1_array = []
s2_array = []
s3_array = []
with open("MeasurementData/ZeroOrderMeasurement/zero_order_measurement_2.txt", "r") as datafile:
    # Ignore the title line
    datafile.readline()

    # Duplicate the first data line
    t, s1, s2, s3 = [float64(item) for item in datafile.readline().split(",")]
    time_array.append(t)
    s1_array.append(s1)
    s1_array.append(s1)
    s2_array.append(s2)
    s2_array.append(s2)
    s3_array.append(s3)
    s3_array.append(s3)

    # Read the rest of the data
    for line in datafile:
        t, s1, s2, s3 = [float64(item) for item in line.split(",")]
        time_array.append(t)
        s1_array.append(s1)
        s2_array.append(s2)
        s3_array.append(s3)

analyze_stokes_parameter_data(time_array, s1_array, s2_array, s3_array, time_unit="s")
