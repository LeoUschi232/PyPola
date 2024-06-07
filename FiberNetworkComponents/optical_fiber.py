from PyPola.FiberNetworkComponents.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from PyPola.utilities.stokes_vector import StokesVector
from PyPola.utilities.general_utilities import double_pi, maxabs
from numpy import sin, cos, max, array, savetxt, loadtxt
from random import uniform
from tqdm import tqdm as taquadum
import csv


def save_fiber_to_csv(fiber, filename):
    fiber_dict = fiber.to_dict()
    mueller_matrix = fiber_dict.pop("mueller_matrix")

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write the properties (except mueller_matrix)
        for key, value in fiber_dict.items():
            writer.writerow([key, value])

        # Write the mueller matrix separately
        writer.writerow(["mueller_matrix"])
        savetxt(csvfile, mueller_matrix, delimiter=",")


def load_fiber_from_csv(filename):
    fiber_dict = {}
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == "mueller_matrix":
                break
            fiber_dict[row[0]] = float(row[1])

        # Load the mueller matrix
        mueller_matrix = loadtxt(csvfile, delimiter=",")
        fiber_dict["mueller_matrix"] = mueller_matrix
    return OpticalFiber.from_dict(fiber_dict)


class OpticalFiber(AbstractOpticalInstrument):
    def __init__(
            self,
            nr_of_segments: int,
            center_wavelength: float = 1550,
            temporal_pmd_theta_fluctuation: float = 0,
            temporal_pmd_delta_fluctuation: float = 0,
            spectral_pmd_theta_fluctuation: float = 0,
            spectral_pmd_delta_fluctuation: float = 0,
            transmission_factor: float = 1
    ):
        super().__init__()
        self.nr_of_segments = max([1, abs(nr_of_segments)])
        self.temporal_pmd_theta_fluctuation = maxabs(temporal_pmd_theta_fluctuation, double_pi)
        self.temporal_pmd_delta_fluctuation = maxabs(temporal_pmd_delta_fluctuation, double_pi)
        self.spectral_pmd_theta_fluctuation = maxabs(spectral_pmd_theta_fluctuation, double_pi)
        self.spectral_pmd_delta_fluctuation = maxabs(spectral_pmd_delta_fluctuation, double_pi)
        self.center_wavelength = abs(center_wavelength)
        self.transmission_factor = maxabs(transmission_factor, 1)

        self.current_segment_double_theta = uniform(0, double_pi)
        self.current_spectral_double_theta = uniform(0, double_pi)
        self.current_spectral_delta = uniform(-self.spectral_pmd_delta_fluctuation, self.spectral_pmd_delta_fluctuation)
        self.setup_mueller_matrix()

    def setup_mueller_matrix(self):
        print(f"Setting up optical fiber...")
        progress_bar = taquadum(total=self.nr_of_segments)
        for i in range(1, self.nr_of_segments + 1):
            self.fluctuate_pmd()
            progress_bar.set_postfix({
                "Segments": f"{i}/{self.nr_of_segments}"
            })
            progress_bar.update()
        progress_bar.close()
        print(f" => Finished setting up optical fiber.")

    @staticmethod
    def get_segment_matrix(double_theta, delta):
        cos_2t = cos(double_theta)
        sin_2t = sin(double_theta)
        cos_d = cos(delta)
        sin_d = sin(delta)
        return array([
            [1, 0, 0, 0],
            [0, cos_2t * cos_2t + sin_2t * sin_2t * cos_d, cos_2t * sin_2t * (1 - cos_d), sin_2t * sin_d],
            [0, cos_2t * sin_2t * (1 - cos_d), cos_2t * cos_2t * cos_d + sin_2t * sin_2t, -cos_2t * sin_d],
            [0, -sin_2t * sin_d, cos_2t * sin_d, cos_d]
        ])

    def fluctuate_pmd(self):
        self.current_segment_double_theta \
            += uniform(-self.temporal_pmd_theta_fluctuation, self.temporal_pmd_theta_fluctuation)
        current_segment_delta = uniform(-self.temporal_pmd_delta_fluctuation, self.temporal_pmd_delta_fluctuation)
        self.current_spectral_double_theta \
            += uniform(-self.spectral_pmd_theta_fluctuation, self.spectral_pmd_theta_fluctuation)
        self.current_spectral_delta = uniform(-self.spectral_pmd_delta_fluctuation, self.spectral_pmd_delta_fluctuation)

        segment_matrix = self.get_segment_matrix(self.current_segment_double_theta, current_segment_delta)
        self.mueller_matrix = segment_matrix @ self.mueller_matrix

    def pass_stokes_vector(self, input_stokes_vector):
        transformation_matrix = self.mueller_matrix
        if input_stokes_vector.wavelength != self.center_wavelength:
            spectral_transformation = self.get_segment_matrix(
                double_theta=self.current_spectral_double_theta,
                delta=(input_stokes_vector.wavelength - self.center_wavelength) * self.current_spectral_delta
            )
            transformation_matrix = spectral_transformation @ transformation_matrix
        s0, s1, s2, s3 = self.transmission_factor * (transformation_matrix @ input_stokes_vector.as_vector()).flatten()
        return StokesVector(s0=s0, s1=s1, s2=s2, s3=s3)

    def to_dict(self):
        return {
            "nr_of_segments": self.nr_of_segments,
            "center_wavelength": self.center_wavelength,
            "temporal_pmd_theta_fluctuation": self.temporal_pmd_theta_fluctuation,
            "temporal_pmd_delta_fluctuation": self.temporal_pmd_delta_fluctuation,
            "spectral_pmd_theta_fluctuation": self.spectral_pmd_theta_fluctuation,
            "spectral_pmd_delta_fluctuation": self.spectral_pmd_delta_fluctuation,
            "transmission_factor": self.transmission_factor,
            "current_segment_double_theta": self.current_segment_double_theta,
            "current_spectral_double_theta": self.current_spectral_double_theta,
            "current_spectral_delta": self.current_spectral_delta,
            "mueller_matrix": self.mueller_matrix
        }

    @classmethod
    def from_dict(cls, data):
        # Create an instance without calling the constructor
        fiber = cls.__new__(cls)

        # Manually set the attributes
        fiber.nr_of_segments = data["nr_of_segments"]
        fiber.center_wavelength = data["center_wavelength"]
        fiber.temporal_pmd_theta_fluctuation = data["temporal_pmd_theta_fluctuation"]
        fiber.temporal_pmd_delta_fluctuation = data["temporal_pmd_delta_fluctuation"]
        fiber.spectral_pmd_theta_fluctuation = data["spectral_pmd_theta_fluctuation"]
        fiber.spectral_pmd_delta_fluctuation = data["spectral_pmd_delta_fluctuation"]
        fiber.transmission_factor = data["transmission_factor"]
        fiber.current_segment_double_theta = data["current_segment_double_theta"]
        fiber.current_spectral_double_theta = data["current_spectral_double_theta"]
        fiber.current_spectral_delta = data["current_spectral_delta"]
        fiber.mueller_matrix = data["mueller_matrix"]
        return fiber

    def instrument_name(self):
        return "Optical Fiber"
