# Note - this only plots AC resistance measurements. Should provide comparison with DC measurements on FEB25 data.
# Note - this only plots 10Hz measurements. Include one plot with 10, 20, 50hz sweeps for comparison.

# plot x (all), y as 2 subplots, with error bars

# want to plot all IVs as different curves (12, 13, 14, 23, 24)

import matplotlib.pyplot as plt
import pandas as pd
import statistics
from scipy.stats import linregress

root = "Feb25_DYT048_NiAu_Ag"
title = "DYT48, NiAu/Ag Contacts DC IV"

def linearfit(x, y):
    slope, intercept,r,p,stderr = linregress(x,y)
    predicted = []
    for el in x:
        predicted.append(el*slope + intercept)

    r2 = r**2
    return slope, intercept, r2, predicted,stderr


ac_pointnames = ["IV12.txt", "IV13.txt", "IV14.txt", "IV23.txt", "IV24.txt", "IV34.txt"]
dc_pointnames = ["IV12DC.asc", "IV13DC.asc", "IV14DC.asc", "IV23DC.asc", "IV24DC.asc", "IV34DC.asc"]

ac_filenames = [root + "/" + pointname for pointname in ac_pointnames]
dc_filenames = [root + "/" + pointname for pointname in dc_pointnames]

fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios':[2, 1]})
fig.tight_layout(pad=2)
fig.subplots_adjust(left=0.13)

res_all_contacts = []

for filename, dc_filename in zip(ac_filenames, dc_filenames):

    #print(filename, dc_filename)

    contactpair = dc_filename.split("/")[1].split(".txt")[0]

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

    # construct similar traces for DC IVs

    data = pd.read_csv(dc_filename, delim_whitespace=True, skiprows=5, skipfooter=13, header=None, names=['V', 'I', 'time', 'type', 'other'], engine='python')

    voltage = data["V"]
    current = [d*1e6 for d in data["I"]]

    dc_data_prep = {}

    for v, c in zip(voltage, current):
        v_r = round(v, 1) # substantially more rounding here. Unsure if we're losing information
        if v_r in dc_data_prep.keys(): dc_data_prep[v_r].append(c)
        else: dc_data_prep[v_r] = [c]

    vol = []
    curr = []
    curr_unc = []

    for v in dc_data_prep.keys():
        vol.append(v)
        curr.append(statistics.mean(dc_data_prep[v]))
        curr_unc.append(statistics.stdev(dc_data_prep[v]))

    # now we plot

    #print(toplotx.keys())

    curr_resids = []

    s, i, r2, pred, stderr = linearfit(vol, curr)

    resids = [yemp - ypred for yemp, ypred in zip(curr, pred)]

    chi2stat = 0
    dof = -2 # two free fitting parameters

    for resid, stdev in zip(resids, curr_unc):
        if stdev != 0:
            dof += 1
            chi2stat += (resid/stdev)**2

    chi2dof = chi2stat/dof

    print("resistance",1/s,"intercept",s,"r2",r2,"resistance err",-1/s + 1/(s+stderr),"chi2/DoF",chi2dof)
    res_all_contacts.append(1/s)

    ax[0].plot(vol, pred, alpha=0.2)

    ax[0].scatter(vol, curr, marker = '_', label=contactpair.replace(".asc",""))
    ax[0].errorbar(vol, curr, curr_unc, linestyle="none")

    ax[0].set_ylabel("Current ($\mu A$)")

    ax[1].scatter(vol, resids, marker = '_', label=contactpair)
    ax[1].errorbar(vol, resids, curr_unc, linestyle="none")

    ax[1].set_ylabel("Current Residuals ($\mu A$)")

    ax[1].set_ylim([-5e-3, 5e-3])
    ax[1].plot([min(resids), max(resids)], [0,0], c='black')
    ax[1].yaxis.set_ticks([-1e-2, 0, 1e-2])

    plt.xlabel("Voltage (V)")

    #ax[0].set_title(title)

    ax[0].grid()
    ax[1].grid()

    ax[0].legend()

print("Mean r", statistics.mean(res_all_contacts), "stdev r", statistics.stdev(res_all_contacts))

plt.savefig(root+".png")
plt.show()
