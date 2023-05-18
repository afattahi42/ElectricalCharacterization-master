import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calcurve
import statistics
import math
from scipy.stats import linregress
from functools import reduce


# USER EDITABLE -------------------


sweep_points = [[432, 1200], [1378, 2017], [2951, 5277], [10058, 12290]]
#filename = "logPAR124_SR830_tempsweep_inclneg.txt"
filename = "logPAR124_SR830_tempsweep.txt"
mode = "plotrt" # choosepoints testrt fitrt plotrt

# DON'T TOUCH ---------------------

kB = 8.6173303e-5 # eV K-1

# setting up calibration
PAR124_cal_fn = "logPAR124_SR830_calcurve_fixedV.txt"
calibrator = calcurve.CalCurve(PAR124_cal_fn)
calibrator.calc_cal_curve(2e-3)

#data = pd.read_csv("logPAR124_SR830_afterdeath.txt")
data = pd.read_csv(filename)


def linearfit(x, y):
    fitresult = linregress(x,y)

    slope = fitresult.slope
    intercept = fitresult.intercept
    r = fitresult.rvalue
    p = fitresult.pvalue
    stderr = fitresult.stderr
    int_stderr = fitresult.intercept_stderr

    predicted = []
    for el in x:
        predicted.append(el*slope + intercept)

    r2 = r**2

    # need to do standard error ourselves. Oh well.

    prederr = math.sqrt((reduce(lambda a, b: a+b, [ (t-e)**2 for t,e in zip(predicted, y)])))

    # In general, try to +/- with SR830 y component. Seems like realistic error.

    return slope, intercept, r2, predicted, stderr, prederr, int_stderr

def calc_res(SR830_x, SR830_y, PAR124A):
    out = []
    out_unc = []
    for sr_x, sr_y, par in zip(SR830_x, SR830_y, PAR124A):

        par_v, par_v_unc = calibrator.translate_v(abs(par))

        # AFTER DEATH
        current = par_v/1e4 # assume linear relationship, uncalibrated
        voltage = sr_x/10 # same.

        res = voltage / current

        res_unc = (par_v_unc / par_v)*res # assuming SR830 uncertainty is comparatively negligible

        out.append(res)
        out_unc.append(res_unc)

    # In general, try to +/- with SR830 y component. Seems like realistic error.

    return out, out_unc

def remove_hysteresis(temp_th, resistivity):
    # just averages over forward and reverse sweeps

    res_tctemp_dict = {}
    res_trtemp_dict = {}

    trtemp_rounded = [round(t) for t in temp_th]

    for tr, res in zip(trtemp_rounded, resistivity):
        if tr in res_trtemp_dict.keys():
            res_trtemp_dict[tr].append(res)
        else:
            res_trtemp_dict[tr] = [res]

    res_trtemp_avg = []
    trtemp_avg = []

    for key in res_trtemp_dict.keys():
        trtemp_avg.append(key)
        res_trtemp_avg.append(statistics.mean(res_trtemp_dict[key]))

    return trtemp_avg, res_trtemp_avg



time = [(t - data["time"][0])/60 for t in data["time"]]
x_par = data["PAR124"]
y_sr = data["y"]
x_sr  = data["x"]
temp_th = data["tr temp (C)"]+273

resistivity, resistivity_unc = calc_res(x_sr, y_sr, x_par)

if mode == "choosepoints":
    # first, do dumb plot of resistance. We will use this to choose start and end points for each sweep (manually)
    plt.plot(resistivity)
    plt.ylabel("resistivity (arb. units)")
    plt.show()


hyst_sweeps = []
no_hyst_sweeps = []

for start_index, stop_index in sweep_points:
    sweep_temp = temp_th[start_index:stop_index]
    sweep_resistivity = resistivity[start_index:stop_index]
    sweep_time = time[start_index:stop_index]

    sweep_t_corr, sweep_r_corr = remove_hysteresis(sweep_temp, sweep_resistivity)

    hyst_sweeps.append([sweep_time, sweep_temp, sweep_resistivity])
    no_hyst_sweeps.append([sweep_time, sweep_t_corr, sweep_r_corr])

if mode == "testrt":

    for sw_time, temp, res in hyst_sweeps:
        plt.scatter(temp, res, s=2, alpha=0.1)
    for sw_time, temp, res in no_hyst_sweeps:
        plt.plot(temp[:-3], res[:-3], label=(str( round((sw_time[0]-time[0])/60,2) ) + "hrs"))

    plt.legend()
    plt.xlabel("temperature (K)")
    plt.ylabel("$V_{34}/I_{12}$ (ohms)")

    plt.show()

if mode == "fitrt":
    # assume temperature dependence goes as R = R0 exp(Eg/2KbT).
    # so Tln(R) = Tln(R0) + Eg/2Kb. Just to start, let's plot these against each other
        # plotting Tln(R) against T. Then can extract ln(R0), Eg/2Kb from linear fit

    for sw_time, temp, res in no_hyst_sweeps:
        TlnR = [t*math.log(r) for t,r in zip(temp, res)]
        plt.scatter(temp, TlnR, marker="+")

        # we do a linear fit to extract slope and intercept

        slope, intercept, r2, predicted, stderr, prederr, int_stderr = linearfit(temp, TlnR)

        # now we calculate the band gap
        Eg = 2 * kB * intercept
        Eg_unc = 2 * kB * int_stderr

        # label by timestamp
        scan_starttime = str(round((sw_time[0]-time[0])/60,2)) + " hrs"

        print(scan_starttime + ": Eg =", round(Eg,5), "±", round(Eg_unc,5), "eV")

    plt.show()

elif mode == "plotrt":

    fig, tempax = plt.subplots()
    resax = tempax.twinx()

    tempax.set_xlabel("time (minutes)")
    tempax.set_ylabel("temperature (K)")
    resax.set_ylabel("$V_{34}/I_{12}$ (ohms)")

    resax.plot(time, [r+u for r,u in zip(resistivity, resistivity_unc)], alpha=0.5, c='b')
    resax.plot(time, [r-u for r,u in zip(resistivity, resistivity_unc)], alpha=0.5, c='b')
    resax.plot(time, resistivity, label="Ω")
    tempax.plot(time, temp_th, c='orange', label = "T")

    resax.legend(loc=1)
    tempax.legend(loc=2)

    resax.set_ylim([0,2e5])
    plt.grid()
    plt.show()
