from PyPola.FiberNetworkComponents.Polarimeters.abstract_polarimeter import AbstractPolarimeter
from PyPola.FiberNetworkComponents.PhotonicsDevices.photodetector import Photodetector
from PyPola.FiberNetworkComponents.OpticalInstruments.magneto_optic_rotator import MagnetoOpticRotator
from PyPola.utilities.general_utilities import same, round_p, get_4x4_unit_matrix
from PyPola.utilities.stokes_vector import StokesVector
from numpy import pi, array
from numpy.linalg import inv

default_rp_list = [0.25, 0.5, 0.75, 0]
default_rs_list = [0.75, 0.25, 0.5, 0]


class FourDetecterPolarimeter(AbstractPolarimeter):
    def __init__(
            self,
            k_list=None,
            rp_list=None,
            rs_list=None,
            delta_list=None,
            alpha12=0.25 * pi,
            alpha23=0.25 * pi
    ):
        super().__init__()

        # First set of assertions checks the correctness of the argmuent format
        if not isinstance(k_list, list) or len(k_list) != 4:
            if k_list is not None:
                self.print_bad_argument_error_message("k_list", "[1,1,1,1]")
            k_list = [1, 1, 1, 1]
        if not isinstance(rp_list, list) or len(rp_list) != 4:
            if rp_list is not None:
                self.print_bad_argument_error_message("rp_list", "[0,0,0,0]")
            rp_list = default_rp_list
        if not isinstance(rs_list, list) or len(rs_list) != 4:
            if rs_list is not None:
                self.print_bad_argument_error_message("rs_list", "[0,0,0,0]")
            rs_list = default_rs_list
        if not isinstance(delta_list, list) or len(delta_list) != 4:
            if delta_list is not None:
                self.print_bad_argument_error_message("delta_list", "[pi/2,pi/2,pi/2,pi/2]")
            delta_list = [0.5 * pi for _ in range(4)]

        # Second check each argument for correctness individually
        for i in range(4):
            if k_list[i] <= 0:
                self.print_bad_argument_error_message(f"k_{i}", 1)
                k_list[i] = 1
        for i in range(3):
            # Make sure that psi!=0 for any photodetector
            if not 0 < rp_list[i] <= 1:
                self.print_bad_argument_error_message(f"rp_{i}", default_rp_list[i])
                rp_list[i] = default_rp_list[i]

            # Make sure that psi!=pi/2 for any photodetector
            if not 0 < rs_list[i] <= 1:
                self.print_bad_argument_error_message(f"rs_{i}", default_rs_list[i])
                rs_list[i] = default_rs_list[i]

            # Make sure that psi!=pi/4 for any photodetector
            if rp_list[i] == rs_list[i]:
                self.print_bad_argument_error_message(f"rp_{i}/rs_{i}", default_rp_list[i] / default_rs_list[i])
                rp_list[i] = default_rp_list[i]
                rs_list[i] = default_rs_list[i]

        # Third handle invalid rotation angles
        if not 0 < alpha12 < pi:
            self.print_bad_argument_error_message(f"alpha12", "pi/4")
            alpha12 = 0.25 * pi
        if not 0 < alpha23 < pi:
            self.print_bad_argument_error_message(f"alpha23", "pi/4")
            alpha23 = 0.25 * pi

        # Fourth make sure that the final detector is fully absorbing
        rp_list[3] = 0.0
        rs_list[3] = 0.0

        # The rest of possible invalid values will be handled by the photodetectors
        self.photodetectors = [Photodetector(k_list[i], rp_list[i], rs_list[i], delta_list[i]) for i in range(4)]
        self.rotators = [MagnetoOpticRotator(2 * alpha12), MagnetoOpticRotator(2 * alpha23)]
        self.instrument_matrix = None
        self.setup_instrument_matrix()

    def setup_instrument_matrix(self):
        # The derivation of this instrument matrix is performed in the documentation
        k1, k2, k3, k4 = [photodetector.k for photodetector in self.photodetectors]
        m_pd1, m_pd2, m_pd3, m_pd4 = [photodetector.mueller_matrix for photodetector in self.photodetectors]
        m_r1, m_r2 = [rotator.mueller_matrix for rotator in self.rotators]
        m1 = get_4x4_unit_matrix()
        a_row1 = k1 * (m1 - m_pd1)[0]
        a_row2 = k2 * ((m1 - m_pd2) @ m_r1 @ m_pd1)[0]
        a_row3 = k3 * ((m1 - m_pd3) @ m_r2 @ m_pd2 @ m_r1 @ m_pd1)[0]
        a_row4 = k4 * (m_pd3 @ m_r2 @ m_pd2 @ m_r1 @ m_pd1)[0]
        self.instrument_matrix = array([a_row1, a_row2, a_row3, a_row4])
        self.mueller_matrix = inv(self.instrument_matrix)

    def calibrate_default(self):
        self.calibrate(
            stokes_vector_1=StokesVector(1, 1, 0, 0),
            stokes_vector_2=StokesVector(1, -0.33380685923377, 0, -0.94264149109218),
            stokes_vector_3=StokesVector(1, -0.33380685923377, 0.81577039496968, 0.47232578102351),
            stokes_vector_4=StokesVector(1, -0.33380685923377, -0.81577039496968, 0.47232578102351)
        )

    def calibrate(
            self,
            stokes_vector_1: StokesVector,
            stokes_vector_2: StokesVector,
            stokes_vector_3: StokesVector,
            stokes_vector_4: StokesVector
    ):
        s_matrix = array([
            [stokes_vector_1.s0, stokes_vector_2.s0, stokes_vector_3.s0, stokes_vector_4.s0],
            [stokes_vector_1.s1, stokes_vector_2.s1, stokes_vector_3.s1, stokes_vector_4.s1],
            [stokes_vector_1.s2, stokes_vector_2.s2, stokes_vector_3.s2, stokes_vector_4.s2],
            [stokes_vector_1.s3, stokes_vector_2.s3, stokes_vector_3.s3, stokes_vector_4.s3]
        ])
        i_matrix = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        stokes_vectors = [stokes_vector_1, stokes_vector_2, stokes_vector_3, stokes_vector_4]
        for i in range(4):
            stokes_vector = stokes_vectors[i]
            sv = self.photodetectors[0].pass_stokes_vector(stokes_vector)
            sv = self.rotators[0].pass_stokes_vector(sv)
            sv = self.photodetectors[1].pass_stokes_vector(sv)
            sv = self.rotators[1].pass_stokes_vector(sv)
            sv = self.photodetectors[2].pass_stokes_vector(sv)
            sv = self.photodetectors[3].pass_stokes_vector(sv)
            if not (same(sv.s0, 0) and same(sv.s1, 0) and same(sv.s2, 0) and same(sv.s3, 0)):
                print(f"Error occured during calibration of 4-Detector Photopolarimeter.")
                print(f"Final stokes vector was not fully absorbed.\nFinal stokes vector: {sv}\n")
                return
            for j in range(4):
                current = self.photodetectors[j].photocurrent
                i_matrix[j][i] = current
        self.instrument_matrix = array(i_matrix) @ inv(s_matrix)
        self.mueller_matrix = inv(self.instrument_matrix)

    def measure_stokes_vector(self, input_stokes_vector: StokesVector):
        if self.mueller_matrix is None:
            print(f"4-Detector Photopolarimeter isn't calibrated!")
            return
        sv = self.photodetectors[0].pass_stokes_vector(input_stokes_vector)
        sv = self.rotators[0].pass_stokes_vector(sv)
        sv = self.photodetectors[1].pass_stokes_vector(sv)
        sv = self.rotators[1].pass_stokes_vector(sv)
        sv = self.photodetectors[2].pass_stokes_vector(sv)
        sv = self.photodetectors[3].pass_stokes_vector(sv)
        if not (same(sv.s0, 0) and same(sv.s1, 0) and same(sv.s2, 0) and same(sv.s3, 0)):
            print(f"Error occured during measurement stokes parameters using 4-Detector Photopolarimeter.")
            print(f"Final stokes vector was not fully absorbed.\nFinal stokes vector: {sv}\n")
            return

        i_vector = array([[photodetector.photocurrent] for photodetector in self.photodetectors])
        s_vector = (self.mueller_matrix @ i_vector).flatten()
        return self.print_and_return_stokes_vector(
            computed_stokes_parameters=s_vector,
            wavelength=input_stokes_vector.wavelength,
            dont_print=True
        )

    def instrument_name(self):
        return "4-Detector Polarimeter"

    def __repr__(self):
        return str([[round_p(value) for value in row] for row in self.instrument_matrix])

    def __str__(self):
        return str(array([[round_p(value) for value in row] for row in self.instrument_matrix]))
