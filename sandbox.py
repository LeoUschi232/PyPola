from OpticalInstruments.polarization_waveplate import PolarizationWaveplate, WaveplateType
from OpticalInstruments.linear_polarizer import LinearPolarizer
from OpticalInstruments.zz_polarization_utilities import degree_of_polarization
from numpy import pi, cos, sin

input_polarization = [[1], [1], [0], [0]]
print(degree_of_polarization(input_polarization))

polarizer = LinearPolarizer(angle_to_x_axis=pi)
waveplate = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER)
output_polarization = waveplate.pass_stokes_vector(input_polarization)
print(output_polarization)
print(degree_of_polarization(output_polarization))
