# PyPola imports
from PyPola.analysis.experiment.Instruments.Instruments_utils.control_superclass import Instrument

# Advanced imports
from time import sleep


class Laser(Instrument):
    def __init__(self, connection_type: str, connection_attribute_value: str):
        super().__init__(connection_type, connection_attribute_value)

        self.laser = 1
        self.chassis = 1
        self.slot = 1
        self.device.read_termination = ";\r\n"

    def get_system(self):
        layout = super().query_from_device(command=f"LAY?")
        print(layout)
        return layout

    def change_laser_attributes(self, laser, chassis, slot):
        self.laser = laser
        self.chassis = chassis
        self.slot = slot

    def busy(self, laser_nr=None):
        if laser_nr is None:
            laser_nr = self.laser

        delay = 0.01
        opc_command = f"*OPC?"
        source_busy_command = f":SOUR:BUSY? {self.chassis},{self.slot},{laser_nr}"

        sleep(2)
        while super().query_from_device(command=opc_command) != "1":
            sleep(delay)
        while super().query_from_device(command=source_busy_command) != "0":
            sleep(delay)

    def set_wavelength(self, wavelength, laser_nr=None):
        if laser_nr is None:
            laser_nr = self.laser
        super().query_from_device(command=f":SOUR:WAV {self.chassis},{self.slot},{laser_nr},{wavelength}")

    def get_wavelength(self, laser_nr=None):
        if laser_nr is None:
            laser_nr = self.laser
        return float(super().query_from_device(command=f":SOUR:WAV? {self.chassis},{self.slot},{laser_nr}"))

    def get_wavelength_limit(self, laser_nr=None):
        if laser_nr is None:
            laser_nr = self.laser
        query = super().query_from_device(command=f":SOUR:WAV:LIM? {self.chassis},{self.slot},{laser_nr}")
        return eval(f"[{query}]")

    def get_fine_limit(self, laser_nr=None):
        if laser_nr is None:
            laser_nr = self.laser
        query = super().query_from_device(command=f":SOUR:OFF:LIM? {self.chassis},{self.slot},{laser_nr}")
        return eval(f"[{query}]")

    def set_fine(self, frequency, laser_nr=None):
        if laser_nr is None:
            laser_nr = self.laser
        super().query_from_device(command=f":SOUR:OFF {self.chassis},{self.slot},{laser_nr},{frequency}")
        self.busy()

    def get_fine(self, laser_nr=None):
        if laser_nr is None:
            laser_nr = self.laser
        return float(super().query_from_device(command=f":SOUR:OFF? {self.chassis},{self.slot},{laser_nr}"))

    def get_power(self, laser_nr=None):
        if laser_nr is None:
            laser_nr = self.laser
        # Querrying APOW instead of POW will output the laser's current optical output power reading
        # For more information refer to:
        # https://www.laserdiodesource.com/files/manuals/laserdiodesource_com/9006/Manual_CoBrite_DX_DX2-1615913063.pdf
        return super().query_from_device(command=f":SOUR:APOW? {self.chassis},{self.slot},{laser_nr}")

    def set_power(self, power, laser_nr=None):
        if laser_nr is None:
            laser_nr = self.laser
        super().query_from_device(command=f":SOUR:POW {self.chassis},{self.slot},{laser_nr},{power}")
        self.busy()

    def get_state(self, laser_nr=None):
        if laser_nr is None:
            laser_nr = self.laser
        return super().query_from_device(command=f":SOUR:STAT? {self.chassis},{self.slot},{laser_nr}")

    def set_state(self, state, laser_nr=None):
        if laser_nr is None:
            laser_nr = self.laser
        super().query_from_device(command=f":SOUR:STAT {self.chassis},{self.slot},{laser_nr},{state}")

    def get_status(self):
        return {
            "alive": self.is_alive(),
            "chassis": self.chassis,
            "slot": self.slot,
            "laser": self.laser,
            "state": self.get_state(),
            "wavelength": self.get_wavelength(),
            "wavelength limit": self.get_wavelength_limit(),
            "fine tuning": self.get_fine(),
            "fine tuning limit": self.get_fine_limit()(),
            "power": self.get_power()()
        }
