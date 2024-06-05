# System imports
from time import sleep
import gc as garbage_collector
import pyvisa

# The dictionary kn_device_to_serial shall be continuously updated with new device numbers
# and their respective serial numbers.
kn_device_to_serial = {
    300: "DP8C163852873",
    301: "DP8C163652523",
    302: "DP8C163852878",
    303: "DP8C163652865",
    304: "DP8C163652864",
    305: "DP8C163852861",
    306: "DP8C163852875",
    307: "DP8C163852877",
    308: "DP8C163852863",
}

# You can continue adding entries to this dictionary as you discover more instruments with model numbers
model_to_serial = {
    "PM400": "P5001635",
    "PM100D": "P0010787"
}


# Signals and Slots are essential for enabling multithreaded communication in Instrument classes,
# such as the communication implemented in the Optical Spectrum Analyzer.
class Instrument:
    """
    This is a base class for all instruments/devices used within the system.
    Common methods and attributes applicable to all instruments should be defined here.
    """

    def __init__(
            self,
            connection_type: str = None,
            connection_attribute_value: str = None,
            delay_override: float = 0.01,
            lib: str = "@py"
    ):
        super().__init__()
        self.delay = delay_override
        self.connector_window = None
        self.device = None
        if connection_type is not None:
            try:
                self.address = ""
                self.rm = pyvisa.ResourceManager(lib)
                self.instrument_list = self.rm.list_resources()
                print(f"Instrument list: {self.instrument_list}")

                if connection_type == "address":
                    self.address = connection_attribute_value
                elif connection_type == "kn_number":
                    connection_attribute_value = kn_device_to_serial[int(connection_attribute_value)]
                    print(f"Assigned serial number: {connection_attribute_value}")
                    connection_type = "serial"
                if connection_type == "serial":
                    address_not_found = True
                    for active_address in self.instrument_list:
                        if connection_attribute_value in active_address:
                            self.address = active_address
                            address_not_found = False
                    if address_not_found:
                        raise pyvisa.VisaIOError(error_code=3221159998)
                elif connection_type == "model":
                    serial = model_to_serial[connection_attribute_value]
                    self.address = f"USB0::0x1313::0x8075::{serial}::INSTR"
                elif connection_type == "ip":
                    try:
                        ip, port = connection_attribute_value.split(";")
                        self.address = f"TCPIP0::{ip}::{port}::SOCKET"
                    except:
                        ip = connection_attribute_value
                        self.address = f"TCPIP0::{ip}::inst0:INSTR"
                    print(self.address)
                elif connection_type == "gpib":
                    self.address = f"GPIB::{connection_attribute_value}::INSTR"

                print(f"<DEBUG> Using device address: {self.address}")
                if len(self.address) <= 0:
                    raise pyvisa.VisaIOError(error_code=3221159998)
                else:
                    self.device = self.rm.open_resource(self.address)
                    self.status = "Connected"
                    print(f"Connected to: {self.address}")
            except pyvisa.VisaIOError:
                self.status = "Not Connected"
                print("Error: PyVISA is not able to find any devices")
        else:
            print(f"=> Connecting using custom connection method <=")

    def write_to_device(self, command):
        if hasattr(self.device, "write"):
            try:
                self.device.write(command)
                sleep(self.delay)
            except Exception as error:
                # handle the exception
                print("An exception occurred when communicatin to ", str(self.address), ":", type(error).__name__)
        else:
            print("Can't execute command. Resource doesn't have write-method")

    def query_from_device(self, command):
        if hasattr(self.device, "query"):
            try:
                response = self.device.query(command)
                sleep(self.delay)
                return response
            except Exception as error:
                # handle the exception
                print("An exception occurred when communicatin to ", str(self.address), ":", type(error).__name__)
        else:
            print("Can't execute command. Resource doesn't have query-method")
            return None

    async def is_alive(self):
        alive_value = self.query_from_device(command="*IDN?")
        return 1 if alive_value else 0

    def close_visa_rm(self):
        if hasattr(self, "rm") and self.rm is not None:
            self.rm.close()
            self.rm = None
        garbage_collector.collect()

    def __del__(self):
        self.close_visa_rm()
