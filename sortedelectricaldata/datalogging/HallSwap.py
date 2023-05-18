from MachineCode import SR2124
from MachineCode.SPD3303X import spd3303x
import numpy as np
import time
import os
from MachineCode.keithley2110tc import keithley2110tc
from MachineCode.arduinorelayinterface import Arduino
import time
import matplotlib.pyplot as plt


######################
# Sweep parameters

#######################

startTime = time.time()
timeStamp = str(time.time())[:10]
fn = "hallSwap{}.txt".format(timeStamp)
f = open("Data/HallSwap/"+fn, "w+")
f.write("t,i,x,y,r,theta,xK,tc, therm\n")
f.close()

LIA = SR2124.SR2124('COM7')
SPD3303x = spd3303x()

SPD3303x.set_voltage(5)
SPD3303x.set_current(0)
#keith = keithley2110tc(1)
relay = Arduino("COM3")

# plt.axis([0, 10, 0, 1])
LIA.autoOffsetX()
time.sleep(3)
LIA.autoOffsetY()

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
        time.sleep(1.5)
        x, y, r, theta =LIA.readall() 
        lockstatus = LIA.readlock()
        # xK = keith.voltage() * LIA.readsens()/10
        xK = 0
        # tc = keith.thermoCoupleTemp()
        tc = 0
        #therm = keith.resistance()
        therm = 0
        #temp = 0
        f = open("Data/HallSwap/"+fn, "a")
        t = time.time() # - startTime
        print("t: {}, i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}, tc: {}, therm: {}".format(t-startTime, i*direction, x, y, r, theta, xK, tc, therm))
        f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}".format(t, i*direction, x, y, r, theta, xK, tc, therm) + "\n")
        f.close()
        if direction == 1:
            plt.scatter(t, x, color = 'green')
           # plt.scatter(t, x, color = 'blue')
        else:
            plt.scatter(t, x, color = 'brown')
           # plt.scatter(t, x, color = 'yellow')
        plt.pause(0.05)

plt.show()
SPD3303x.set_current(0)
SPD3303x.set_voltage(0)

    
