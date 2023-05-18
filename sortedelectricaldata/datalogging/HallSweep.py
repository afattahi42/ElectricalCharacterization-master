from  MachineCode import SR2124
from MachineCode.SPD3303X import spd3303x
import numpy as np
import time
import os
from MachineCode.keithley2110tc import keithley2110tc
from MachineCode.arduinorelayinterface import Arduino
import matplotlib.pyplot as plt
######################
# Sweep parameters
sweepRate = 33
#######################

timeStamp = str(time.time())[:10]
fn = "hallSweep{}.txt".format(timeStamp)
f = open("Data/HallSweep/"+fn, "w+")
f.write("t,i,x,y,r,theta,xK\n")
f.close()

LIA = SR2124.SR2124('COM7')
SPD3303x = spd3303x()
relay = Arduino("COM3")

SPD3303x.set_voltage(5)
SPD3303x.set_current(0)


startTime = time.time() 
for direction in [(0, 3.2), (3.2, 0), (0, -3.2), (-3.2,0)]: 
    for i in np.linspace(direction[0], direction[1], sweepRate):
        if direction[0] > -1 and direction[1] > -1:
            relay.enable_P1()
        else:
            relay.enable_P2()
        
        SPD3303x.set_current(abs(i))
        time.sleep(.5)
        x, y, r, theta = LIA.readall() 
        xK = 0
        f = open("Data/HallSweep/"+fn, "a")
        t = time.time()
        print("t: {}, i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}".format(t-startTime, i, x, y, r, theta, xK))
        f.write(str(t) + ',' + str(i) + ',' + str(x)+',' + str(y) + ',' + str(r) + ',' + str(theta) + ',' + str(xK) + "\n")
        f.close()
        plt.scatter(i, r, color = 'blue')
        #plt.scatter(i, x*-1, color = 'green')
        plt.pause(.05)
plt.show()

SPD3303x.set_current(0)
SPD3303x.set_voltage(0)
print(fn)
    
