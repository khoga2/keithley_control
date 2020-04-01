# Keithley IV Sweep for 6430 Source Meter
# K. Hogan 2019
# Command line input: python IV_sweep.py min_voltage max_voltage voltage_step filename.txt deviceid_plottitle
# Example: python IV_sweep.py -10 10 0.5 test "Test IV"

import sys
import visa
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Variable intake and assignment
startv = sys.argv[1]
stopv = sys.argv[2]
stepv = sys.argv[3]
filename = sys.argv[4]
deviceID = sys.argv[5]
startvprime = float(startv)
stopvprime = float(stopv)
stepvprime = float(stepv)
steps = (stopvprime - startvprime) / stepvprime 

# Assign keithley to resource ASRL6::INSTR 
rm = visa.ResourceManager()
rm.list_resources()
Keithley = rm.open_resource('ASRL6::INSTR')
Keithley.write("*RST")
#Keithley.baud_rate = 57600
Keithley.timeout = 200000 # Needs to be long enough to complete sweeping

# Turn off concurrent functions and set sensor to current with fixed voltage
# Set measurement speed to NPLC 1.0
Keithley.write(":SENS:FUNC:CONC OFF")
Keithley.write(":SOUR:FUNC VOLT")
Keithley.write(":SENS:FUNC 'CURR'")
Keithley.write(":SENS:RES:NPLC 1.0")

# Voltage starting, ending, and spacing values based on input
Keithley.write(":SOUR:VOLT:STAR " + str(startv))
Keithley.write(":SOUR:VOLT:STOP " + str(stopv))
Keithley.write(":SOUR:VOLT:STEP " + str(stepv))
Keithley.write(":SOUR:SWE:RANG AUTO")

# Set compliance current (in A), sweep direction, and data acquisition
Keithley.write(":SENS:CURR:PROT 105E-3") #limit is -105mA to 105mA for 6430 model
Keithley.write(":SOUR:SWE:SPAC LIN")
Keithley.write(":SOUR:SWE:POIN " + str(steps))
Keithley.write(":SOUR:SWE:DIR UP")
Keithley.write(":TRIG:COUN " + str(steps))
Keithley.write(":FORM:ELEM CURR")

# Set sweep mode and turn output on
Keithley.write(":SOUR:VOLT:MODE SWE")
Keithley.write(":OUTP ON")

# Initiate sweep, collect ACSII current values, and turn output off
result = Keithley.query(":READ?")
yvalues = Keithley.query_ascii_values(":FETC?")
Keithley.write(":OUTP OFF")
Keithley.write(":SOUR:VOLT 0")

# Create xvalues array and calculate conductance
xvalues = np.arange(startvprime,stopvprime,stepvprime)
slope, intercept, r_value, p_value, std_error = stats.linregress(xvalues, yvalues)
print("Resistance:", 1/slope, "Ohms")

# Plot IV and save data to txt file
plt.plot(xvalues,yvalues)
plt.xlabel(' Voltage (V)')
plt.ylabel(' Current (A)')
plt.title(str(deviceID))
plt.show()
np.savetxt(filename + "_IV.txt", (xvalues,yvalues)) 

# Calculate Maximum Power Point in IV curve
# Save power data to file
power = np.array(xvalues * yvalues)
maxpower = np.amax(power)
maxpower_loc = np.argmax(power)
np.savetxt(filename + "_Power.txt", (xvalues,power)) 


# Print out max power value, location in np array
# then print x,y values cooresponding to np location
#print(maxpower)
#print(maxpower_loc)
#print(xvalues[maxpower_loc], yvalues[maxpower_loc])
#print(power)
#print(xvalues)

# Plot the power vs voltage in the IV quandrant of the IV curve
# and save the data into a file. 
plt.xlim([0, np.amax(xvalues)])
plt.ylim([np.amin(power), 0])
plt.plot(xvalues,power)
plt.xlabel(' Voltage (V)')
plt.ylabel(' Power (W)')
plt.title(' Maximum Power')
plt.show()
