from MachineCode import SR2124
from MachineCode.SPD3303X import spd3303x
import numpy as np
import time
import os
from MachineCode.keithley2110tc import keithley2110tc
from MachineCode.arduinorelayinterface import Arduino
import time

######################
# Sweep parameters
freqSweep = np.linspace(20, 200, 361)
#######################

startTime = time.time()
timeStamp = str(time.time())[:10]
fn = "ResistivityVFrequency{}.txt".format(timeStamp)

f = open("Data/ResistivityVFrequency/"+fn, "w+")
f.write("t,f,x,y,r,theta,xK,tc,therm,dc\n")
f.close()


LIA = SR2124.SR2124('COM7')


for freq in freqSweep:
    print(freq)
    LIA.setf(freq)
    time.sleep(1.5)
    # LIA.overloadDetect()
    x, y, r, theta = LIA.readall() 
    # lockstatus = LIA.readlock()
    xK = 0
    # tc = keith.thermoCoupleTemp()
    tc = 0
    #therm = keith.resistance()
    therm = 0
    #temp = 0
    f = open("Data/ResistivityVFrequency/"+fn, "a")
    t = time.time() # - startTime
    print("t: {}, f: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}, tc: {}, therm: {}".format(t-startTime, freq, x, y, r, theta, xK, tc, therm))
    f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}".format(t, freq, x, y, r, theta, xK, tc, therm) + "\n")
    f.close()


LIA.autoOffsetX()
time.sleep(3)
LIA.autoOffsetY()
