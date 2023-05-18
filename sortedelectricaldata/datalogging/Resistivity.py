from MachineCode import SR2124
from MachineCode.SPD3303X import spd3303x
import numpy as np
import time
import os
from MachineCode.keithley2110tc import keithley2110tc
from MachineCode.arduinorelayinterface import Arduino
import time
from MachineCode import SR830

######################
# Sweep parameters

#######################

startTime = time.time()
timeStamp = str(time.time())[:10]
fn = "resistivity{}.txt".format(timeStamp)

f = open("Data/Resistivity/"+fn, "w+")
f.write("t,i,x,y,r,theta,x2,y2,r2,theta2,xK,tc,therm,dc\n")
f.close()


LIA = SR2124.SR2124('COM7')
LIA2 = SR830.SR830("COM9")


while True:
    time.sleep(1.5)
    LIA.overloadDetect()
    x, y, r, theta =LIA.readall() 
    x2, y2, r2, theta2 =LIA2.readall() 
    lockstatus = LIA.readlock()
    # xK = keith.voltage() * LIA.readsens()/10
    xK = 0
    # tc = keith.thermoCoupleTemp()
    i = 0
    tc = 0
    #therm = keith.resistance()
    therm = 0
    #temp = 0
    f = open("Data/Resistivity/"+fn, "a")
    t = time.time() # - startTime
    print("t: {}, i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}, tc: {}, therm: {}".format(t-startTime, i, x, y, r, theta, xK, tc, therm))
    f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(t, i, x, y, r, theta, x2, y2, r2, theta2, xK, tc, therm) + "\n")
    f.close()


LIA.autoOffsetX()
time.sleep(3)
LIA.autoOffsetY()
