from PyPola.OpticalInstruments.polarization_waveplate import PolarizationWaveplate, WaveplateType
from PyPola.Utilities.stokes_vector import StokesVector, NormalizationType
from PyPola.Utilities.general_utilities import normalize_and_clean
from numpy import arccos

s = StokesVector(s0=1, s1=0.458258, s2=0.8, s3=0.387298, normalization=NormalizationType.POINCARE_SPHERE)
z = StokesVector(s0=1, s1=1, s2=-1, s3=0, normalization=NormalizationType.POINCARE_SPHERE)
r = StokesVector(s0=1, s1=0.458258, s2=0.8, s3=0, normalization=NormalizationType.POINCARE_SPHERE)
print(r.as_3d_array())

qwp = PolarizationWaveplate(waveplate_type=WaveplateType.QUARTER, double_theta=arccos(r.s1))
s_new = qwp.pass_stokes_vector(s)
print(s_new.as_3d_array())

r_new = normalize_and_clean(s_new.as_3d_array() + z.as_3d_array())
print(r_new)