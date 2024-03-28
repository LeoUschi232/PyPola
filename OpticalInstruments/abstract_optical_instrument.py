from numpy import array


class AbstractOpticalInstrument:
    def __init__(self):
        self.stokes_matrix = array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def setup_stokes_matrix(self):
        pass

    def clean_stokes_matrix(self, raw_stokes_matrix):
        self.stokes_matrix = array([
            [0.0 if abs(value) < 1e-12 else float(value) for value in row]
            for row in raw_stokes_matrix
        ])

    def pass_stokes_vector(self, input_stokes_vector):
        input_stokes_vector = array(input_stokes_vector)
        output_stokes_vector = self.stokes_matrix @ input_stokes_vector
        return array([[0.0 if abs(float(item[0])) < 1e-12 else float(item[0])] for item in output_stokes_vector])
