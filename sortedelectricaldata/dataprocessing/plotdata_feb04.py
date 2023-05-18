import matplotlib.pyplot as plt
import pandas as pd
import statistics
import math
from scipy.stats import linregress
from scipy import optimize
from functools import reduce
import numpy as np

plot_raw = True
plot_vtemp  = True
plot_vtime = True

plt.rcParams["figure.figsize"] = (12,6)

#data = pd.read_csv('020622_021022_degradation_inair.txt')
data = pd.read_csv('Feb04_DYT042_In/020522_cycle2.txt')

time = data["time (unix)"]
tctemp = data[" tc temp (C)"]
trtemp = data[" tr temp (C)"]
trres  = data[" tr res (ohm)"]
filmres = data[" film res (ohm)"]

filmres_pos = abs(filmres) * 4.53236 # van der pauw coefficient

def fittobandgap(temp, res):
    # assuming R = T^(-3/2) e^(Eg/2KbT)

    def predict_res(temp, eg, r0):
        kB = 8.6173303e-5 # eV K-1
        out = []
        for t in temp:
            out.append(r0 * math.exp(eg/(2*kB*t)))
        return out

    fit = optimize.curve_fit(predict_res, temp, res)

    params = fit[0]
    err = np.sqrt(np.diag(fit[1]))
    #print("FIT PARAMS",params)
    #print("FIT ERR",err)

    # test plot

    predicted = predict_res(temp, params[0], params[1])

    plt.scatter(temp, res)
    plt.scatter(temp, predicted)
    plt.show()

    ## need to do standard error ourselves. Oh well.

    prederr = math.sqrt((reduce(lambda a, b: a+b, [ (t-e)**2 for t,e in zip(predicted, res)])))

    #print("prederr", prederr)

    # eg, r0, eg_err, r0_err, predicted, prederr
    return params[0], params[1], err[0], err[1], predicted, prederr

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


if plot_raw:
    fig, (ax1, ax2) = plt.subplots(1,2)

    ax1.scatter([t+273 for t in trtemp], filmres_pos, label="Thermistor", marker='+')
    ax1.scatter([t+273 for t in tctemp], filmres_pos, label="Thermocouple", marker='+')
    ax1.legend()
    ax1.set_xlabel("temperature (K)")
    ax1.set_ylabel("$V_{34}/I_{12}$ (ohms)")
    ax1.grid()

    ax2.scatter([(t-time[0])/60 for t in time], [t+273 for t in trtemp], label="Thermistor", marker='+')
    ax2.scatter([(t-time[0])/60 for t in time], [t+273 for t in tctemp], label="Thermocouple", marker='+')
    ax2.legend()
    ax2.set_xlabel("time (minutes)")
    ax2.set_ylabel("temperature (K)")
    ax2.grid()

    plt.show()


# now - process data to eliminate hysteresis
# naively, we round all resistivity measurements to the nearest degree, then average all measurements

if plot_vtemp:

    res_tctemp_dict = {}
    res_trtemp_dict = {}

    tctemp_rounded = [round(t)+273 for t in tctemp]
    trtemp_rounded = [round(t)+273 for t in trtemp]

    for tc, tr, res in zip(tctemp_rounded, trtemp_rounded, filmres_pos):
        if tc in res_tctemp_dict.keys():
            res_tctemp_dict[tc].append(res)
        else:
            res_tctemp_dict[tc] = [res]

        if tr in res_trtemp_dict.keys():
            res_trtemp_dict[tr].append(res)
        else:
            res_trtemp_dict[tr] = [res]

    res_tctemp_avg = []
    res_trtemp_avg = []
    tctemp_avg = []
    trtemp_avg = []  

    for key in res_tctemp_dict.keys():
        tctemp_avg.append(key)
        res_tctemp_avg.append(statistics.mean(res_tctemp_dict[key]))

    for key in res_trtemp_dict.keys():
        trtemp_avg.append(key)
        res_trtemp_avg.append(statistics.mean(res_trtemp_dict[key]))


    Eg, r0, Eg_unc, r0_unc, predicted, preder = fittobandgap(trtemp_avg, res_trtemp_avg)


    # THIS IS BAD APPROXIMATION! -----
    ## now, we transform and fit to estimate Eg

    #TlnR = [t*math.log(r) for t,r in zip(trtemp_avg, res_trtemp_avg)]

    ## we do a linear fit to extract slope and intercept

    #slope, intercept, r2, predicted, stderr, prederr, int_stderr = linearfit(trtemp_avg, TlnR)

    #kB = 8.6173303e-5 # eV K-1

    ## now we calculate the band gap and r0
    #Eg = 2 * kB * intercept
    #Eg_unc = 2 * kB * int_stderr

    #r0 = math.exp(slope)
    #r0_unc = math.exp(slope)*stderr
    # END BAD APPROXIMATION ----

    print("Eg=",Eg,"+-",Eg_unc)
    print("R0=",r0,"+-",r0_unc)


    plt.scatter(trtemp_avg, res_trtemp_avg, label="thermistor", marker='+')
    #plt.scatter(tctemp_avg, res_tctemp_avg, label="thermocouple", marker='+')

    plt.legend()
    plt.xlabel("temperature (K)")
    plt.ylabel("$V_{34}/I_{12}$ (ohms)")
    plt.grid()

    plt.show()

if plot_vtime:

    plt.scatter([(t-time[0])/60 for t in time], filmres_pos, marker='+')
    plt.xlabel("time (minutes)")
    plt.ylabel("$V_{34}/I_{12}$ (ohms)")
    plt.yscale('log')
    plt.ylim([1,1e9])
    plt.grid()
    plt.show()

# trying to fit to variable-range hopping model for conductivity

#logtr = [math.log(1/res) for temp, res in zip(trtemp_avg, res_trtemp_avg)]
#t14 = [math.pow(temp+273, 1) for temp, res in zip(trtemp_avg, res_trtemp_avg)]

#plt.scatter(logtr, t14, marker='+')
#plt.xlabel('$T^{-1/4}$ (K)')
#plt.ylabel('$ln(\sigma)$')
#plt.grid()
#plt.show()
