# PyPola imports
from PyPola.Analysis.Experiment.Instruments.photonics_laser_control import Laser
from PyPola.Analysis.Experiment.Instruments.powermeter_control import Powermeter

# Mainstream imports
from numpy import full_like, min, max
from matplotlib import pyplot as plt
from time import time

# Advanced imports
from tkinter import Tk, messagebox
from threading import Thread

tested_wavelength = 1550

# Set up powermeter properly
powermeter_serial = "P0028123"
powermeter = Powermeter(connection_type="serial", connection_attribute_value=powermeter_serial)
if powermeter is None or powermeter.device is None:
    print(f"Powermeter: {powermeter}")
    # noinspection ALL
    print(f"Powermeter device: {powermeter.device}")
    exit(-1)
powermeter.set_wavelength(wavelength=tested_wavelength)

# Set up laser properly
laser_ip = "169.254.200.101"
laser_port = 2000
laser = Laser(connection_type="ip", connection_attribute_value=f"{laser_ip};{laser_port}")
if laser is None or laser.device is None:
    print(f"Laser: {laser}")
    # noinspection ALL
    print(f"Laser device: {laser.device}")
    exit(-1)
laser.set_wavelength(wavelength=tested_wavelength, laser_nr=1)
laser.set_power(power=10, laser_nr=1)

# Make the user double-check if the laser can be switched on safely
window = Tk()
window.withdraw()
response = messagebox.askokcancel("WARNING", "The laser will now be switched on!", parent=window)
window.destroy()
if not response:
    exit()
print("Laser activated")
laser.set_state(laser_nr=1, state=1)

# Perform the measurement
laser_power = []
laser_timestamps = []
powermeter_power = []
powermeter_timestamps = []
measurement_time = 3
measurement_start = time()


def laser_measurement():
    timestamp = time() - measurement_start
    while timestamp <= measurement_time:
        laser_data = laser.get_power(laser_nr=1)
        timestamp = time() - measurement_start
        laser_power.append(laser_data)
        laser_timestamps.append(timestamp)


def powermeter_measurement():
    timestamp = time() - measurement_start
    while timestamp <= measurement_time:
        powermeter_data = powermeter.get_measured_power()
        timestamp = time() - measurement_start
        powermeter_power.append(powermeter_data)
        powermeter_timestamps.append(timestamp)


laser_thread = Thread(target=laser_measurement)
powermeter_thread = Thread(target=powermeter_measurement)

# Start threads
laser_thread.start()
powermeter_thread.start()
laser_thread.join()
powermeter_thread.join()
laser.set_state(laser_nr=1, state=0)

# Compute laser data properties
laser_data_length = len(laser_power)
min_laser_power = min(laser_power)
max_laser_power = max(laser_power)
print(f"Laser data length: {laser_data_length}")

# Compute powermeter data properties
powermeter_data_length = len(powermeter_power)
min_powermeter_power = min(powermeter_power)
max_powermeter_power = max(powermeter_power)
print(f"Powermeter data length: {powermeter_data_length}")

# Print laser data and its bounds
plt.plot(laser_timestamps, laser_power, linewidth=0.5, color="orange", label="Laser power measurement")
plt.plot(laser_timestamps, full_like(laser_timestamps, min_laser_power),
         linewidth=0.5, color="red", label=f"Min laser power: {min_laser_power}")
plt.plot(laser_timestamps, full_like(laser_timestamps, max_laser_power),
         linewidth=0.5, color="red", label=f"Max laser power: {max_laser_power}")

# Print powermeter data and its bounds
plt.plot(powermeter_timestamps, powermeter_power, linewidth=0.5, color="blue", label="Powermeter power measurement")
plt.plot(powermeter_timestamps, full_like(powermeter_timestamps, min_powermeter_power),
         linewidth=0.5, color="purple", label=f"Min powermeter power: {min_powermeter_power}")
plt.plot(powermeter_timestamps, full_like(powermeter_timestamps, max_powermeter_power),
         linewidth=0.5, color="purple", label=f"Max powermeter power: {max_powermeter_power}")

###############################################
plt.title(f"Power Variation at 10 dBm setup")
plt.xlabel(f"Seconds [s]")
plt.ylabel(f"Power [dBm]")
plt.xlim([0, 3600])
plt.ylim([9.5, 10.25])
plt.grid(color="gray", linestyle="dotted", linewidth=0.25)
plt.legend(loc="upper left")
plt.show()
