import MachineCode.SR830
import MachineCode.keithley2000gpib
import MachineCode.bk5491bthermistor as bk5491b
import time
import numpy as np
import matplotlib.pyplot as plt

fn = "logPAR124S_R830_calcurve2.txt"

LIA = SR830.SR830('com4')
meter = bk5491b.bkthermistor('com3') # this is connected to the output of the PAR124A

f = open(fn, "w")
f.write("time,voltage,PAR124,x,y,r,theta\n")
f.close()

ps = []
xs = []

for i in range(3):
    for v in np.linspace(0,0.4,50):

        LIA.setv(v)

        time.sleep(2)

        par124 = meter.fetchreading()
        x,y,r,theta = LIA.readall()
        currtime = time.time()

        ps.append(par124)
        xs.append(x)

        print(str(currtime), v, par124, x, y, r, theta)

        f = open(fn, "a")
        f.write(str(currtime)+","+str(v)+","+str(par124)+","+str(x)+","+str(y)+","+str(r)+","+str(theta)+"\n")
        f.close()

plt.plot(ps, xs)
plt.show()

