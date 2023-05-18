from MachineCode.SR2124 import SR2124
from MachineCode.SR830 import SR830
import time
import serial
import numpy as np
from MachineCode.Keithley2400 import Keithley2400

######################
# Sweep parameters
f2 = 442.3
v2 = .01 # Minimum v necessary to get full range of DC bias: Why: bias values can be set up to 1000 the reference amplitude
steps = 40
maxV = 10 # max bias voltage
gateBiasMaxV = 210
#######################




SR2124 = SR2124('COM7')
#SR830 = SR830('COM9')
keith = Keithley2400("COM10")

SR2124.setv(v2)
SR2124.setf(f2)
SR2124.setb(0)
SR2124.onb(1)

timeStamp = str(time.time())[:10]
fn = "differential_resistance_DC_{}.txt".format(timeStamp)

f = open("Data/Differential_Resistance/"+fn, "a")
f.write("t,gateBias,f2,bias,v2,x2,y2,r2,theta2,x8,y8,r8,theta8\n")
f.close()

keith.slowIVMode()
keith.setComplianceCurrent(.001)# safety control
keith.setVoltage(0) # safety control

keith.outputOn()


a = [np.linspace(0, maxV, steps), np.linspace(maxV, 0, steps)] # , np.linspace(0, -maxV, steps), np.linspace(-maxV, 0, steps)





for gateBias in gateBiasL:
    keith.setVoltage(gateBias)
    time.sleep(1.5)

    for sweepSpace in a:
        for bias in sweepSpace:
            bias =  round(bias, 2) # lock in wont take values with more decimal places then it holds
            
            SR2124.setb(bias)
            time.sleep(1.5)
            

            x2, y2, r2, theta2 = SR2124.readall()
           # x8, y8, r8, theta8 = SR830.readall()
            x8, y8, r8, theta8 = [0,0,0,0]

            print(f2,gateBias,bias,v2,x2,y2,r2,theta2, x8, y8, r8, theta8)
            t = time.time()
            f = open("Data/Differential_Resistance/"+fn, "a")
            f.write(("{},"*12 + '{}\n').format(t,gateBias,f2,bias,v2,x2,y2,r2,theta2, x8, y8, r8, theta8))
            f.close()

keith.outputOff()

