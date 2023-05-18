import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("logPAR124_SR830_sweeps.txt")

def calc_res(SR830, PAR124A):
    out = []
    for sr, par in zip(SR830, PAR124A):

        # BEFORE DEATH
        current = par/10*2e-3/10e3 # assume linear relationship, uncalibrated
        voltage = sr/10 # same.

        # AFTER DEATH
        current = par/10*50e-6/10e3 # assume linear relationship, uncalibrated
        voltage = sr/1 # same.

        out.append(voltage/current)
    
    return out

time = [(t - data["time"][0])/60 for t in data["time"]]
x_par = data["PAR124"]
x_sr  = data["x"]
temp_th = data["tr temp (C)"]

resistivity = calc_res(x_sr, x_par)

plt.plot(time, temp_th)
plt.ylabel("temp (C)")
plt.xlabel("time (min)")
plt.show()

#plt.plot(temp_th, resistivity)
#plt.xlabel("temp (C)")
#plt.ylabel("resistance (uncal)")
#plt.show()


plt.plot(time, resistivity)
plt.xlabel("time (minutes)")
plt.ylabel("resistance (uncal)")
plt.show()

# plt.plot(time, x_par)
# plt.xlabel("time (minutes)")
# plt.ylabel("par124a raw voltage")
# plt.show()

# plt.plot(time, x_sr)
# plt.xlabel("time (minutes)")
# plt.ylabel("sr830 raw voltage")
# plt.show()