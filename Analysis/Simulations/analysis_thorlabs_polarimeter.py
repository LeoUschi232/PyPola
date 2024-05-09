from PyPola.Utilities.polarization_utilities import random_polarized_stokes_vector
from numpy import pi, cos, sin, linspace, array
from tqdm import tqdm as taquadum
from time import sleep


def progress_bar(nr_of_points, message=""):
    print(message)
    sleep(0.1)
    return taquadum(total=nr_of_points)


def output_intensity_v1(s0, s1, s2, s3, alpha, beta):
    term1 = (s1 * cos(2 * beta) + s2 * sin(2 * beta)) * cos(2 * beta - 2 * alpha)
    term2 = s3 * sin(2 * beta - 2 * alpha)
    return 0.5 * (s0 + term1 + term2)


def output_intensity_v2(sv, alpha, beta):
    return output_intensity_v1(*sv.as_array(), alpha, beta)


def manifest_actual_vs_computed_table(actual_data, computed_data):
    actual_data_string = f"{array(actual_data).flatten()}"[1:-1]
    computed_data_string = f"{array(computed_data).flatten()}"[1:-1]
    print(f"           S0          S1          S2          S3")
    print(f"  Actual:", actual_data_string)
    print(f"Computed:", computed_data_string)


def measure_with_thorlabs_polarimeter(input_stokes_vector, n=180000, max_beta=pi, alpha=pi / 4):
    betas = linspace(start=0, stop=max_beta, num=n)

    output_intensities = []
    progress = progress_bar(nr_of_points=n, message="Measuring intensities")
    for beta_i in betas:
        output_intensities.append(output_intensity_v2(input_stokes_vector, alpha, beta_i))
        progress.update()
    progress.close()

    a0 = 0
    progress = progress_bar(nr_of_points=n, message="Calculating A0")
    for oi in output_intensities:
        a0 += oi
        progress.update()
    a0 *= (1 / n)
    progress.close()

    a1 = 0
    progress = progress_bar(nr_of_points=n, message="Calculating A1")
    for beta_i, oi in zip(betas, output_intensities):
        a1 += oi * cos(2 * beta_i)
        progress.update()
    a1 *= (2 / n)
    progress.close()

    a2 = 0
    progress = progress_bar(nr_of_points=n, message="Calculating A2")
    for beta_i, oi in zip(betas, output_intensities):
        a2 += oi * cos(4 * beta_i)
        progress.update()
    a2 *= (2 / n)
    progress.close()

    b2 = 0
    progress = progress_bar(nr_of_points=n, message="Calculating B2")
    for beta_i, oi in zip(betas, output_intensities):
        b2 += oi * sin(4 * beta_i)
        progress.update()
    b2 *= (2 / n)
    progress.close()

    print(f"A0={a0}\nA1={a1}\nA2={a2}\nB1=0\nB2={b2}\n")
    calculated_s0 = 2 * a0 + 2 * a2
    calculated_s1 = 4 * b2
    calculated_s2 = -4 * a2
    calculated_s3 = -2 * a1

    manifest_actual_vs_computed_table(
        actual_data=input_stokes_vector.as_array(),
        computed_data=[calculated_s0, calculated_s1, calculated_s2, calculated_s3]
    )
    return [[calculated_s0], [calculated_s1], [calculated_s2], [calculated_s3]]


stokes_vector = random_polarized_stokes_vector()
print("Input:", stokes_vector.as_list())
measure_with_thorlabs_polarimeter(stokes_vector)
