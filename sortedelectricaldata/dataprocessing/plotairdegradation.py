import math
import pandas as pd
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("Feb11_DYT048_NiAu/logPAR124_SR830_air_sweeptemp.txt")

def calc_res(SR830, PAR124A):
    out = []
    for sr, par in zip(SR830, PAR124A):
        current = par*1e-3/10e3 # assume linear relationship, uncalibrated
        voltage = sr/10 # same.
        out.append(voltage/current)
    return out

def predict_res(time, a, b):
    out = []
    for t in time: out.append( a*math.exp(b*t))
    return out

time = [(t - data["time"][0])/60 for t in data["time"]]
x_par = data["PAR124"]
x_sr  = data["x"]
temp_th = data["tr temp (C)"]

resistivity = calc_res(x_sr, x_par)

plt.plot(time, resistivity)
plt.xlabel("time (minutes)")
plt.ylabel("$V_{34}/I_{12}$ (ohms)")
plt.grid()

# now we fit to exponential model
fit = optimize.curve_fit(predict_res, time, resistivity, p0=[1, 0.017])
a, timeconst = fit[0]
a_err, timeconst_err = np.sqrt(np.diag(fit[1]))
pred = predict_res(time, a, timeconst)
#pred = predict_res(time, 1, 0.017)

print("a",a,"a_err",a_err)
print("halflife",1/timeconst,"hl_err",1/timeconst - 1/(timeconst - timeconst_err))

plt.plot(time, pred)
plt.show()
