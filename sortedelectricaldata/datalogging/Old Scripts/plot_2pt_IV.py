# plot x (all), y as 2 subplots, with error bars

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
    return slope, intercept, r2, predicted,stderr

filename = "IV24.txt"

data = pd.read_csv(filename)

curr_x = abs(data["x"])
curr_y = abs(data["y"])

volt = data["v"]
freq = data["f"]

curr_x_freqs = {} # dictionary of dictionaries of lists. {f: {v1: {}, v2: {}, v3: {}}}
curr_y_freqs = {}

for f, v, x, y in zip(freq, volt, curr_x, curr_y):
    if f not in curr_x_freqs.keys():
        curr_x_freqs[f] = {}

    if f not in curr_y_freqs.keys():
        curr_y_freqs[f] = {}

    if round(v,2) in curr_x_freqs[f].keys():
        curr_x_freqs[f][round(v,2)].append(x)
    else:
        curr_x_freqs[f][round(v,2)] = [x]

    if round(v,2) in curr_y_freqs[f].keys():
        curr_y_freqs[f][round(v,2)].append(y)
    else:
        curr_y_freqs[f][round(v,2)] = [y]

# now process to generate uncertainties. Want a data structure that looks like: {f: [[v], [x], [x_unc], [y], [y_unc]]}

toplotx = {}
toploty = {}

for freqs in curr_x_freqs.keys(): # assume x, y have same freqs
    vlist = []
    xlist = []
    xunclist = []
    for v in curr_x_freqs[freqs]:
        vlist.append(v)
        xlist.append(statistics.mean(curr_x_freqs[freqs][v]))
        xunclist.append(statistics.stdev(curr_x_freqs[freqs][v]))

    toplotx[freqs] = [vlist, xlist, xunclist]

for freqs in curr_y_freqs.keys(): # assume x, y have same freqs
    vlist = []
    ylist = []
    yunclist = []
    for v in curr_y_freqs[freqs]:
        vlist.append(v)
        ylist.append(statistics.mean(curr_y_freqs[freqs][v]))
        yunclist.append(statistics.stdev(curr_y_freqs[freqs][v]))


    toploty[freqs] = [vlist, ylist, yunclist]

# now we plot

fig, ax = plt.subplots(2)

print(toplotx.keys())

for freq in toplotx.keys():

    s, i, r2, pred, stderr = linearfit(toplotx[freq][0][1:], toplotx[freq][1][1:])
    print("freq",freq,"resistance",1/s,"intercept",s,"r2",r2,"stderr",stderr)
    ax[0].plot(toplotx[freq][0][1:], pred, alpha=0.2)

    ax[0].scatter(toplotx[freq][0][1:], toplotx[freq][1][1:], marker = '_', label=str(freq)+"Hz")
    ax[0].errorbar(toplotx[freq][0][1:], toplotx[freq][1][1:], toplotx[freq][2][1:], linestyle="none")

ax[0].set_ylabel("Current-x $\mu A$")

for freq in toploty.keys():
    ax[1].scatter(toploty[freq][0][1:], toploty[freq][1][1:], marker = '_', label=str(freq)+"Hz")
    ax[1].errorbar(toploty[freq][0][1:], toploty[freq][1][1:], toploty[freq][2][1:], linestyle="none")

ax[1].set_ylabel("Current-y $\mu A$")

plt.xlabel("Voltage (V)")

ax[0].set_title(filename)

ax[0].grid()
ax[1].grid()

ax[0].legend()
ax[1].legend()

plt.show()
#plt.scatter(volt, curr)
#plt.show()

#plt.scatter(volt, resistance)
#plt.show()

