from PyPola.FiberNetworkComponents.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from PyPola.utilities.stokes_vector import StokesVector
from numpy import pi, sin, cos, max, min, array
from random import uniform
from time import sleep
from tqdm import tqdm as taquadum


class OpticalFiber(AbstractOpticalInstrument):
    def __init__(self, nr_of_segments: int = 1000, loss_factor: float = 1, loss_fluctuates: bool = False):
        super().__init__()

        self.nr_of_segments = max([1, nr_of_segments])
        self.loss_factor = min([1, max([0, loss_factor])])
        self.pmd_variation = pi / 64
        self.loss_fluctuates = loss_fluctuates

        self.current_segment_double_theta = uniform(0, pi)
        self.setup_mueller_matrix()

    def fluctuate_loss(self):
        if self.loss_fluctuates:
            self.loss_factor = max([0, min([self.loss_factor + uniform(-0.02, 0.02), 1])])

    def setup_mueller_matrix(self):
        print(f"\nSetting up optical fiber...")
        sleep(0.1)
        progress_bar = taquadum(total=self.nr_of_segments)
        for i in range(1, self.nr_of_segments + 1):
            self.fluctuate_pmd()
            progress_bar.set_postfix({
                "Segments": f"{i}/{self.nr_of_segments}"
            })
            progress_bar.update()
        progress_bar.close()
        print(f"Finished setting up optical fiber.\n")

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
        current_segment_delta = uniform(-self.pmd_variation, self.pmd_variation)
        self.current_segment_double_theta += uniform(-self.pmd_variation, self.pmd_variation)
        if self.current_segment_double_theta > pi:
            self.current_segment_double_theta -= pi
        elif self.current_segment_double_theta < -pi:
            self.current_segment_double_theta += pi

        segment_matrix = self.get_segment_matrix(self.current_segment_double_theta, current_segment_delta)
        self.mueller_matrix = segment_matrix @ self.mueller_matrix

    def pass_stokes_vector(self, input_stokes_vector):
        s0, s1, s2, s3 = self.loss_factor * super().pass_stokes_vector(input_stokes_vector).as_array()
        return StokesVector(s0=s0, s1=s1, s2=s2, s3=s3)
