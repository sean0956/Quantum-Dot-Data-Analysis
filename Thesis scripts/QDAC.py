import qcodes as qc
import numpy as np
from time import sleep
import qcodes.instrument_drivers.QDevil.QDevil_QDAC as QDac
from qcodes.instrument_drivers.QDevil.QDevil_QDAC import Mode

# Connect to the instrument
# By default the initialisation skips reading the current sensors on all channels
# as this takes some 0.2-0.5 secs per channel due to the sensor settling time.
# You can force reading the current sensors at startup by specifiying "update_currents=True" in the call.

qdac = QDac.QDac(name='qdac', address='ASRL2::INSTR', update_currents=False)
print("Number of channels: ",qdac.num_chans)
#####################################################################################################
# Setting the output voltage of a channel using "set"
qdac.ch01.v.set(1)
# Reading the output voltage of a channel using "get"
print('Channel 1 voltage: {} {}'.format(qdac.ch01.v.get(), qdac.ch01.v.unit))
# Setting the output voltage of a channel using short-hand notation, which is used hereafter
qdac.ch01.v(-1)
# Reading the output voltage of a channel using short hand notion "qdac.ch01.v()", which is used hereafter
print('Channel 1 voltage: {} {}'.format(qdac.ch01.v(), qdac.ch01.v.unit))
# Reading the current output of a channel
print(qdac.ch01.i(), qdac.ch01.i.unit)

#####################################################################################################
# For smooth voltage changes the maximal voltage change (in V/s) may be set for each channel
qdac.ch01.slope(1)
qdac.ch02.slope(2)
# An overview may be printed (all other channels have 'Inf' slope)
qdac.print_slopes()
# Now setting channel 1 and 2 voltages will cause slow ramping to 0V (1 V/s and 2 V/s, respectively)
# Note that ch02 is already at 0 V, so the ramping function will complain bacause a ramp time
# less than 2 ms is not possible.
qdac.ch01.v(0)
qdac.ch02.v(0)
sleep(1)
# Note that only 8 (or fewer) channels can be slow ramped at a time
# To disable slow ramping of a channel, set its slope to 'Inf':
qdac.ch01.slope('Inf')
qdac.print_slopes()
#####################################################################################################
# This will query voltages of all channels of a 24 channel QDAC
# Note that index 0 refer to channel 01, and so on
print(qdac.channels[0:8].v())
# Similarly, we may set them. The outputs will not change simultaneously but witin some milliseconds.
qdac.channels[0:8].v(-0.9)
#####################################################################################################
# To each channel one may assign a SYNC output
# SYNC output 1 will fire a 10 ms 5 V pulse when ch02 initiates a ramp
# ch will ramp when setting a voltage while a slope is assinged, or when using "ramp_voltages"
qdac.ch02.sync(1)
# note that a pulse is still fired even if no visible ramp is performed
# e.g if ramping from 1 V to 1 V

# The sync pulse settings can be modified
qdac.ch02.sync_delay(0)  # The sync pulse delay (s)
qdac.ch02.sync_duration(25e-3)  # The sync pulse duration (secs). Default is 10 ms.

# Print an overview of assigned SYNC ports
qdac.print_syncs()
# Plug in an oscilloscope to CH02 and SYNC1 and observe the ramping and the sync pulse
qdac.ch02.slope(1)
qdac.ch02.v(-0.5)
sleep(3)
qdac.ch02.v(1)
# syncs are unassigned by assigning sync 0
qdac.ch02.sync(0)
#####################################################################################################
# Here we ramp channels 1, 2, 3, and 7 from there current values to zero, in 0.2 seconds
duration = qdac.ramp_voltages([1,2,3,7],[],[0,0,0,0],0.2)
sleep(duration+0.05)
# As it takes tens of milliseconds to read the channels' current voltage, it is faster
# if their previous voltages are known:
duration = qdac.ramp_voltages([1,2,3,7],[0,0,0,0],[1,2,3,4],0.2)
sleep(duration+0.05)
#####################################################################################################
# Perform a 1D scan of the QDAC ch01 and record the current on
# the same channel also using the QDAC.
# Replace the QDAC current measurement by a DMM to do a typical physical measurement

from qcodes.dataset.plotting import plot_by_id
from qcodes.dataset.measurements import Measurement
from time import ctime
STATION = qc.station.Station(qdac)
qc.new_experiment("QDAC", "TestIV"+ctime())
meas = Measurement()
meas.register_parameter(qdac.ch01.v)  # register the independent parameter
meas.register_parameter(qdac.ch01.i, setpoints=(qdac.ch01.v,))  # now register the dependent one
meas.write_period = 2
with meas.run() as datasaver:
    for set_v in np.linspace(-1, 1, 10):
        qdac.ch01.v(set_v)
        sleep(0.1)
        get_i = qdac.ch01.i()
        datasaver.add_result((qdac.ch01.v, set_v),
                            (qdac.ch01.i, get_i))
        print(set_v, get_i)
    dataset = datasaver.dataset
myplot = plot_by_id(dataset.run_id)
qc.dataset.plotting.plt.show()      # Sometimes it is necessasry to out-comment this line in Jupyter....
#####################################################################################################
####2Dscan
# set outputs to zero
qdac.ch01.v(0)
qdac.ch02.v(0)
qdac.ch03.v(0)

# enable sync on one of the fast channels (sync signal is output at every start of a staircase ramp.)
# for example for triggering a digitizer
qdac.ch02.sync(1)
# enable a 10ms sync delay which allows for stabilizing of the device
qdac.ch02.sync_delay(0.01)
# Note! The slope definitions are not used during the 2D scan
duration = qdac.ramp_voltages_2d( slow_chans=[1], slow_vstart=[0], slow_vend=[1],
                                  fast_chans=[2,3], fast_vstart=[0,0], fast_vend=[1,-1],
                                  slow_steps = 10, fast_steps = 10,
                                  step_length=0.02)
# wait for the ramp to finish
sleep(duration+0.1)

qdac.print_syncs()
# Set outputs back to zero
# First remove sync output so that we do not trigger an acquisition
qdac.ch02.sync(0)
qdac.ch01.v.set(0)
qdac.ch02.v.set(0)
qdac.ch03.v.set(0)
#####################################################################################################

# The "QDac.Mode" enum class is used for setting and reading the mode.

# This will set the voltage output range to low, and the current sensor range to low
qdac.ch01.mode(Mode.vlow_ilow)
print(qdac.ch01.mode.cache().get_label())

# This will return ch01 to the default mode: high voltage range, high current sensing range
qdac.ch01.mode(Mode.vhigh_ihigh)
print(qdac.ch01.mode.cache().get_label())
#####################################################################################################
# Here is a small example showing demonstrating the behavior - if posible hook up an oscilloscope on ch01
#
qdac.ch01.slope('Inf')                # Make sure that we are not fooled by a slow changing ch01
qdac.ch01.mode(Mode.vhigh_ihigh)      # Attenuation OFF (the default), high voltage range
qdac.ch01.v(1.5)                      # Set the voltage to outside the low voltage range (but inside present range)
qdac.mode_force(True)            # Enable changing voltage range eventhough the output is non-zero
qdac.ch01.mode(Mode.vlow_ilow)   # Attenuation ON, low voltage range - signal is clipped, and a dip occurred
print(qdac.ch01.v())            # Returns approximately 1.1V as the output is clipped to the low range limit
qdac.ch01.mode(Mode.vhigh_ihigh)      # Attenuation off, high voltage range
print(qdac.ch01.v())                  # Returns approximately 1.1V, unchanged - but a spike occured
# Return to protected mode
qdac.mode_force(False)
# Now provoke an error
print(qdac.ch01.v())
print(qdac.ch01.mode.cache().get_label())     # Pretty printing the mode parameter
try:
    qdac.ch01.mode(Mode.vlow_ilow)
except ValueError as ve:
    print("ERROR: ", ve)

#####################################################################################################
qdac.print_overview(update_currents=False)

#####################################################################################################
print(qdac.temp0_0.get(), qdac.temp0_0.unit)
print(qdac.temp2_1.get(), qdac.temp0_0.unit)

#####################################################################################################
qdac.reset(update_currents=False)
# Then print the overview gain
qdac.print_overview(update_currents=False)
# Shut down the VISA connection
qdac.close()