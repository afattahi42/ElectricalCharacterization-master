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
sweepRate = 33
maxV = 32
#######################

timeStamp = str(time.time())[:10]
fn = "hallDCBias{}.txt".format(timeStamp)

f = open("Data/HallEffectDCBias/"+fn, "w+")
f.write("t,i,x,y,r,theta,xK,tc,therm,dc\n")
f.close()

startTime = time.time() 
biasD = -1

LIA = SR2124.SR2124('COM7')
SPD3303x1 = spd3303x() # sol curr
SPD3303x2 = spd3303x(2) # gate bias
relay = Arduino("COM3")


SPD3303x1.set_voltage(5)
SPD3303x1.set_current(0)


SPD3303x2.set_current(.005) # safety control
SPD3303x2.set_series_voltage(0) # safety control

for dc in np.linspace(0, maxV, sweepRate):
    SPD3303x2.set_series_voltage(dc)
    time.sleep(.5)
    LIA.overloadDetect()

    for direction in [1, -1]:
        SPD3303x1.set_current(0)
        time.sleep(1)
        if direction == 1:
            relay.enable_P1()
        else:
            relay.enable_P2()
        time.sleep(.5)


        i = 3.2
        
        SPD3303x1.set_current(i)
        time.sleep(1.2)
        x, y, r, theta =LIA.readall() 
        lockstatus = LIA.readlock()
        # xK = keith.voltage() * LIA.readsens()/10
        xK = 0
        # tc = keith.thermoCoupleTemp()
        tc = 0
        #therm = keith.resistance()
        therm = 0
        #temp = 0
        f = open("Data/HallEffectDCBias/"+fn, "a")
        t = time.time() # - startTime
        print("t: {}, i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}, tc: {}, therm: {}, dc: {}".format(t-startTime, i*direction, x, y, r, theta, xK, tc, therm, dc*biasD))
        f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(t, i*direction, x, y, r, theta, xK, tc, therm, dc*biasD) + "\n")
        f.close()



    """i = 0
    SPD3303x.set_current(i)
    time.sleep(3)
    x, y, r, theta =LIA.readall() 
    lockstatus = LIA.readlock()
    xK = keith.voltage()
    f = open(fn, "a")

    print("i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}".format(i, x, y, r, theta, xK))
    f.write(str(i) + ',' + str(x)+',' + str(y) + ',' + str(r) + ',' + str(theta) + ',' + str(xK) + "\n")
    f.close()"""
    
SPD3303x2.set_series_voltage(0)
SPD3303x2.set_current(0, channel = 2)    
SPD3303x1.set_current(0)

    

LIA.autoOffsetX()
time.sleep(3)
LIA.autoOffsetY()