from PyPola.FiberNetworkComponents.optical_fiber import OpticalFiber
from PyPola.Utilities.polarization_utilities import get_angle_to_x_axis, degree_of_polarization
from numpy import array, pi, sign

input_stokes_vector = array([[1], [1], [0], [0]])
fiber = OpticalFiber(nr_of_segments=1000)

print(f"Angle before: {get_angle_to_x_axis(input_stokes_vector)}")
output_stokes_vector = fiber.pass_stokes_vector(input_stokes_vector)
print(f"Angle after: {get_angle_to_x_axis(output_stokes_vector)}")
print(f"Output stokes vector:\n{output_stokes_vector}")
print(f"Degree of polarization: {degree_of_polarization(output_stokes_vector)}")
print(pi/2)