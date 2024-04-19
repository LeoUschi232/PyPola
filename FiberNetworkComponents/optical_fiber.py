from PyPola.OpticalInstruments.linear_polarizer import LinearPolarizer
from PyPola.OpticalInstruments.polarization_waveplate import PolarizationWaveplate
from PyPola.OpticalInstruments.abstract_optical_instrument import AbstractOpticalInstrument
from numpy import array, pi, sin, cos, tan, arctan, sinh, cosh
from random import uniform
from time import sleep
from tqdm import tqdm as taquadum

segment_variation = pi / 256


class OpticalFiber(AbstractOpticalInstrument):
    def __init__(self, nr_of_segments: int = 1000, loss_factor: float = 1, loss_fluctuates: bool = False):
        super().__init__()

        self.nr_of_segments = max(1, nr_of_segments)
        self.loss_factor = 1
        self.loss_fluctuates = loss_fluctuates
        if 0 < loss_factor <= 1:
            self.loss_factor = loss_factor

        self.current_segment_angle = uniform(0, pi)
        self.setup_stokes_matrix()

    def fluctuate_loss(self):
        if self.loss_fluctuates:
            self.loss_factor = max(0, min(self.loss_factor + uniform(-0.02, 0.02), 1))

    def setup_stokes_matrix(self):
        print(f"\nSetting up optical fiber...")
        sleep(0.1)
        progress_bar = taquadum(total=self.nr_of_segments)
        for i in range(1, self.nr_of_segments + 1):
            self.fluctuate_pmd()
            progress_bar.set_postfix({
                "Segments": f"{i}/{self.nr_of_segments}"
            }, refresh=True)
            progress_bar.update(1)
        progress_bar.close()
        print(f"Finished setting up optical fiber.\n")

    @staticmethod
    def get_segment_matrix(angle_to_fast_axis, phase_shift):
        cos_2a = cos(2 * angle_to_fast_axis)
        sin_2a = sin(2 * angle_to_fast_axis)
        cos_d = cos(phase_shift)
        sin_d = sin(phase_shift)
        return [
            [1, 0, 0, 0],
            [0, cos_2a * cos_2a + sin_2a * sin_2a * cos_d, cos_2a * sin_2a * (1 - cos_d), sin_2a * sin_d],
            [0, cos_2a * sin_2a * (1 - cos_d), cos_2a * cos_2a * cos_d + sin_2a * sin_2a, -cos_2a * sin_d],
            [0, -sin_2a * sin_d, cos_2a * sin_d, cos_d]
        ]

    def fluctuate_pmd(self):
        current_phase_shift = uniform(-segment_variation, segment_variation)
        self.current_segment_angle += uniform(-segment_variation, segment_variation)
        if self.current_segment_angle > pi:
            self.current_segment_angle -= pi

        segment_matrix = self.get_segment_matrix(self.current_segment_angle, current_phase_shift)
        self.stokes_matrix = segment_matrix @ self.stokes_matrix

    def pass_stokes_vector(self, input_stokes_vector):
        return self.loss_factor * super().pass_stokes_vector(input_stokes_vector)
