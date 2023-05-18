import MachineCode.SR2124
from MachineCode.SPD3303X import spd3303x
import numpy as np
import time
import os
from MachineCode.keithley2110tc import keithley2110tc
from MachineCode.arduinorelayinterface import Arduino


# Add a folder for data files
# use .format from now on
# add automatic offset + lowest voltage
# add frequency setting
# add filters

f = open(fn, "a")
f.write("i,x,y,r,theta,xK\n")
f.close()
SPD3303x.set_voltage(5)
SPD3303x.set_current(0)
keith = keithley2110tc()
relay = Arduino("COM3")

while True:
    for direction in [1, -1]:
        SPD3303x.set_current(0)
        time.sleep(1)
        if direction == 1:
            relay.enable_P1()
        else:
            relay.enable_P2()
        time.sleep(.5)


        i = 3.2
        
        SPD3303x.set_current(i)
        time.sleep(2)
        x, y, r, theta =LIA.readall() 
        lockstatus = LIA.readlock()
        xK = keith.voltage()
        f = open(fn, "a")

        print("i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}".format(i*direction, x, y, r, theta, xK))
        f.write(str(i*direction) + ',' + str(x)+',' + str(y) + ',' + str(r) + ',' + str(theta) + ',' + str(xK) + "\n")
        f.close()

    
SPD3303x.set_current(0)
SPD3303x.set_voltage(0)

    
