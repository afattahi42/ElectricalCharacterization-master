# Note - this only plots AC resistance measurements. Should provide comparison with DC measurements on FEB25 data.
# Note - this only plots 10Hz measurements. Include one plot with 10, 20, 50hz sweeps for comparison.

# plot x (all), y as 2 subplots, with error bars

# want to plot all IVs as different curves (12, 13, 14, 23, 24)

import matplotlib.pyplot as plt
import pandas as pd
import statistics
from scipy.stats import linregress

root = "Feb11_DYT048_NiAu"
#root = "Feb18_DYT048_AlAu"
#root = "Feb25_DYT048_NiAu_Ag"
title = "DYT48, NiAu/Ag Contacts AC IV"

def linearfit(x, y):
    slope, intercept,r,p,stderr = linregress(x,y)
    predicted = []
    for el in x:
        predicted.append(el*slope + intercept)

    r2 = r**2
    return slope, intercept, r2, predicted,stderr


pointnames = ["IV12.txt", "IV13.txt", "IV14.txt", "IV23.txt", "IV24.txt", "IV34.txt"]

filenames = [root + "/" + pointname for pointname in pointnames]

fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios':[2, 1]})
fig.tight_layout(pad=2)
fig.subplots_adjust(left=0.13)

res_all_contacts = []

for filename in filenames:

    contactpair = filename.split("/")[1].split(".txt")[0]

    data = pd.read_csv(filename)

    curr_x = [ el * 1e6 for el in abs(data["x"])]
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


    #print(toplotx.keys())

    toplotx_resids = {}

    for freq in toplotx.keys():

        if freq != 10: continue

        s, i, r2, pred, stderr = linearfit(toplotx[freq][0][1:], toplotx[freq][1][1:])

        resids = [yemp - ypred for yemp, ypred in zip(toplotx[freq][1][1:], pred)]

        chi2stat = 0
        dof = -2 # two free fitting parameters

        for resid, stdev in zip(resids, toplotx[freq][2][1:]):
            if stdev != 0:
                dof += 1
                chi2stat += (resid/stdev)**2

        chi2dof = chi2stat/dof

        toplotx_resids[freq] = [toplotx[freq][0][1:], resids]

        print("freq",freq,"resistance",1/s,"intercept",i,"r2",r2,"resistance err",-1/s + 1/(s-stderr),"chi2/DoF",chi2dof)
        res_all_contacts.append(1/s)
        ax[0].plot(toplotx[freq][0][1:], pred, alpha=0.2)

        ax[0].scatter(toplotx[freq][0][1:], toplotx[freq][1][1:], marker = '_', label=contactpair)
        ax[0].errorbar(toplotx[freq][0][1:], toplotx[freq][1][1:], toplotx[freq][2][1:], linestyle="none")

    ax[0].set_ylabel("Current ($\mu A$)")

    for freq in toplotx_resids.keys():

        if freq != 10: continue

        ax[1].scatter(toplotx_resids[freq][0], toplotx_resids[freq][1], marker = '_', label=contactpair)
        ax[1].errorbar(toplotx_resids[freq][0], toplotx_resids[freq][1], toplotx[freq][2][1:], linestyle="none")

    ax[1].set_ylabel("Current Residuals ($\mu A$)")

    ax[1].set_ylim([-2e-2, 2e-2])
    ax[1].plot([min(toplotx_resids[freq][0]), max(toplotx_resids[freq][0])], [0,0], c='black')
    ax[1].yaxis.set_ticks([-2e-2, 0, 2e-2])

    plt.xlabel("Voltage (V)")

    ax[0].set_title(title)

    ax[0].grid()
    ax[1].grid()

    ax[0].legend()

print("Mean R",statistics.mean(res_all_contacts), "Stdev R",statistics.stdev(res_all_contacts))

plt.savefig(root+".png")
plt.show()
