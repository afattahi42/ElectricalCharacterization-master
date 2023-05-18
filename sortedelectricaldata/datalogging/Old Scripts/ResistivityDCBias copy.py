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
biasD = 1
maxV = 60
numPoints = 121
up = True
down = True
#######################

startTime = time.time()
timeStamp = str(time.time())[:10]
fn = "resistivity{}.txt".format(timeStamp)

f = open("Data/ResistivityDCBias/"+fn, "w+")
f.write("t,i,x,y,r,theta,xK,tc,therm,dc\n")
f.close()


LIA = SR2124.SR2124('COM7')
SPD3303x = spd3303x(2)
relay = Arduino("COM3")


SPD3303x.set_current(.007) # safety control
SPD3303x.set_series_voltage(0) # safety control

for i in ["up", "down"]:
    if i == "up":
        if up == True:
            sweepSpace = np.linspace(0, maxV, numPoints)
        else:
            break

    elif i == "down":
        if down == True:
            sweepSpace = np.linspace(maxV, 0, numPoints)
        else:
            break

    for dc in sweepSpace:
        SPD3303x.set_series_voltage(dc)
        time.sleep(1.5)
        LIA.overloadDetect()


        x, y, r, theta =LIA.readall() 
        lockstatus = LIA.readlock()
        # xK = keith.voltage() * LIA.readsens()/10
        xK = 0
        # tc = keith.thermoCoupleTemp()
        i = 0
        tc = 0
        #therm = keith.resistance()
        therm = 0
        #temp = 0
        f = open("Data/ResistivityDCBias/"+fn, "a")
        t = time.time() # - startTime
        print("t: {}, i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}, tc: {}, therm: {}, dc: {}".format(t-startTime, i, x, y, r, theta, xK, tc, therm, dc*biasD))
        f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(t, i, x, y, r, theta, xK, tc, therm, dc*biasD) + "\n")
        f.close()




    
#SPD3303x.set_voltage(0, channel = 2)
#SPD3303x.set_current(0, channel = 2)    

    

LIA.autoOffsetX()
time.sleep(3)
LIA.autoOffsetY()

SPD3303x.set_current(0, channel = 2) # safety control
SPD3303x.set_series_voltage(0) # safety control

#from playsound import playsound
#while True:
   # playsound('sound1.mp3')


def voltage_stepDown(inst, channel):
    current_voltage = inst.read_voltage(channel)
    #while 