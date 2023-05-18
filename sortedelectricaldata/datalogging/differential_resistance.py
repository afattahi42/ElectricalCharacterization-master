from MachineCode.SR2124 import SR2124
from MachineCode.SR830 import SR830
import time
import serial
import numpy as np

######################
# Sweep parameters
f2 = 442.3
v2 = .1 # Minimum v necessary to get full range of DC bias: Why: bias values can be set up to 1000 the reference amplitude
steps = 200
maxV = 10 # max bias voltage
#######################




SR2124 = SR2124('COM7')
SR830 = SR830('COM9')

SR2124.setv(v2)
SR2124.setf(f2)
SR2124.setb(0)
SR2124.onb(1)

timeStamp = str(time.time())[:10]
fn = "differential_resistance_{}.txt".format(timeStamp)

f = open("Data/Differential_Resistance/"+fn, "a")
f.write("t,f2,bias,v2,x2,y2,r2,theta2,x8,y8,r8,theta8\n")
f.close()



a = [np.linspace(0, maxV, steps), np.linspace(maxV, 0, steps), np.linspace(0, -maxV, steps), np.linspace(-maxV, 0, steps)]

for sweepSpace in a:
    for bias in sweepSpace:
        bias =  round(bias, 2) # lock in wont take values with more decimal places then it holds
        
        SR2124.setb(bias)
        time.sleep(1.5)
        

        x2, y2, r2, theta2 = SR2124.readall()
        x8, y8, r8, theta8 = SR830.readall()

        print(f2,bias,v2,x2,y2,r2,theta2, x8, y8, r8, theta8)
        t = time.time()
        f = open("Data/Differential_Resistance/"+fn, "a")
        f.write(("{},"*11 + '{}\n').format(t,f2,bias,v2,x2,y2,r2,theta2, x8, y8, r8, theta8))
        f.close()

