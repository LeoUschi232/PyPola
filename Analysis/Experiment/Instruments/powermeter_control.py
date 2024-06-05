# PyPola imports
from PyPola.analysis.experiment.Instruments.Instruments_utils.control_superclass import Instrument

# Mainstream import
from numpy import empty


class Powermeter(Instrument):
    def __init__(self, connection_type: str, connection_attribute_value: str):
        super().__init__(connection_type, connection_attribute_value)

    def set_wavelength(self, wavelength):
        self.write_to_device(command=f"SENS:CORR:WAV {wavelength}")

    def get_wavelength(self):
        # Can be retrieved only if it was set before
        return float(self.query_from_device(command=f"SENS:CORR:WAV?"))

    def set_averaging(self, averaging):
        self.write_to_device(command=f"SENSe:AVERage:COUNt {averaging}")

    def get_averaging(self):
        # Can be retrieved only if it was set before
        average_count = self.query_from_device(command=f"SENSe:AVERage:COUNt?")
        if average_count is not None:
            return float(average_count)
        return 1.0

    def set_power_unit(self, power_unit):
        # Either watts "W" or "DBM"
        self.write_to_device(command=f"SENS:POW:UNIT {power_unit}")

    def set_zero(self):
        self.write_to_device(command=f"SENS:CORR:COLL:ZERO")

    def get_zero(self):
        # Can be retrieved only if it was set before
        return self.query_from_device(command=f"SENS:CORR:COLL:ZERO:MAGN?")

    def get_measured_power(self):
        self.write_to_device(command=f"CONF:POW")
        return float(self.query_from_device(command=f"READ?"))

    def set_auto_range(self, status=True):
        if status:
            value = "ON"
        else:
            value = "OFF"
        self.write_to_device(command=f"SEN:POW:RANG:AUTO {value}")

    def get_multiple_power(self, number_of_samples=1000):
        power = empty(number_of_samples)
        for i in range(number_of_samples):
            power[i] = self.get_measured_power()

        return [power, power.std(), power.mean()]

    def is_alive(self):
        value = self.query_from_device(command=f"SYSTEM:VER?")
        return 1 if len(value) > 0 else 0

    def get_status(self):
        return {
            "alive": self.is_alive(),
            "zero": self.get_zero(),
            "wavelength": self.get_wavelength(),
            "power": self.get_measured_power()
        }
