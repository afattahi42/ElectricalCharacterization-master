import matplotlib.pyplot as plt
import pandas as pd
import statistics
from scipy.stats import linregress

def linearfit(x, y):
    slope, intercept,r,p,stderr = linregress(x,y)
    predicted = []
    for el in x:
        predicted.append(el*slope + intercept)

    r2 = r**2
    return slope, intercept, r2, predicted, stderr

filename = "logPAR124_SR830_calcurve_fixedV.txt"
data = pd.read_csv(filename)

par124 = -1*data["PAR124"]
sr830  = data["x"]

slope, intercept, r2, predicted, stderr = linearfit(sr830, par124)

print("r2",r2,"stderr",stderr)
print(slope,"* x +",intercept)

plt.scatter(sr830, par124, marker="+")
plt.plot(sr830, predicted)

plt.grid()

plt.xlabel("SR830 (V)")
plt.ylabel("PAR124A (V)")

plt.show()
