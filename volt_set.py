# Set Current for 6430 Source Meter
# K. Hogan 2019
# Command line input: python curr_set.py current_setpoint(in amps) device_Size(in microns) 
# Example: python curr_set.py 0.01 400

import sys
import visa
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

volt_set = sys.argv[1]
dev_size = sys.argv[2]
volt_set_prime = float(volt_set)

# Assign keithley to resource ASRL6::INSTR 
rm = visa.ResourceManager()
Keithley = rm.open_resource('ASRL6::INSTR')
Keithley.write("*RST")
Keithley.timeout = 100000

# Turn off concurrent functions and set sensor to voltage with fixed voltage
# Set measurement speed to NPLC 1.0
Keithley.write(":SENS:FUNC:CONC OFF")
Keithley.write(":SOUR:FUNC VOLT")
Keithley.write(":SENS:FUNC 'CURR'")
Keithley.write(":SENS:RES:NPLC 1.0")

Keithley.write(":SOUR:VOLT " + str(volt_set_prime))
Keithley.write(":OUTP ON")
enter_maker = input("Press enter to turn off voltage source ")

Keithley.write(":OUTP OFF")