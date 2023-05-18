import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calcurve
import statistics
import math
from scipy.stats import linregress
from functools import reduce
from scipy import optimize
from matplotlib.pyplot import figure
from matplotlib.ticker import FormatStrFormatter


# USER EDITABLE -------------------


# ---- FEB 25 ----

sweep_points = [[31906,33700], [33700, 35393], [39565, 41397], [41397, 43074], [47239, 49000], [49000, 50696], [55038, 56887], [56887, 58535], [62716, 64445], [64445, 66254], [70394, 72244], [72244, 73972], [78050, 79870], [79870, 81560], [85730, 87440], [87440, 89260]]

#filename = "Feb25_DYT048_NiAu_Ag/logPAR124_SR830_sweeps.txt"
filename = "logPAR124_SR830_sweeps.txt"

# ---- FEB 18 ----

# filename = "Feb18_DYT048_AlAu/logPAR124_SR830_tempsweep_inclneg_mod.txt" # this is just the relevant points from inclneg

# sweep_points = [[2248, 4357], [4613, 6661], [6831, 8882], [8926, 11227], [11286, 13514], [13541, 15821], [15864, 18132], [18176, 20446], [20579, 22761], [22980, 25017], [25221, 27309], [27322, 29644], [29709, 31962], [31984, 34188], [34414, 36583], [36671, 38937], [38968, 41215], [41339, 43444], [43582, 45880], [45961, 48169], [48186, 50455]] # for inclneg_2

# sweep_points = [[62, 2368], [9364, 11939], [14132, 16163]] # these are points FOR RAW DEG. SWEEP GRAPH

# sweep_points = [[62, 2368], [2368, 4753], [4753, 6965], [6965, 9364], [9364, 11939], [11939, 14132], [14132, 16163], [16163, 18621]]

# There's so much degradation that there's a lot of hysteresis. So include up and down sweeps separately.

# sweep_points = [[571, 1758], [1758, 2977], [2977, 4108], [4108, 5382], [5382, 6466], [6466, 7709], [7709, 8824], [8824, 10000], [10000, 11214], [11214, 12361], [12361, 13558],[13588, 14664], [14664, 15922], [15922, 16872], [16872, 18300]]

# ---- FEB 11 ----

# filename = "Feb11_DYT048_NiAu/logPAR124_SR830_air.txt"

mode = "plotrt" # choosepoints testrt fitrt plotrt twopoint plotdetvtime

# DON'T TOUCH ---------------------

kB = 8.6173303e-5 # eV K-1

# setting up calibration
PAR124_cal_fn = "logPAR124A_SR830_calcurve_fixedV_outliersremoved.txt"
calibrator = calcurve.CalCurve(PAR124_cal_fn)
calibrator.calc_cal_curve(5e-3)

#data = pd.read_csv("logPAR124_SR830_afterdeath.txt")
data = pd.read_csv(filename)

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

def calc_res(SR830_x, SR830_y, PAR124A):
    out = []
    out_unc = []
    for sr_x, sr_y, par in zip(SR830_x, SR830_y, PAR124A):

        par_v, par_v_unc = calibrator.translate_v(abs(par))

        # AFTER DEATH
        current = par_v/1e4 # assume linear relationship, uncalibrated
        voltage = sr_x/10 # same.

        res = voltage / current * 4.53236 # van der pauw coefficient

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
x_par = abs(data["sr2124"])
y_sr = abs(data["y"])
x_sr  = abs(data["x"])
temp_th = data["tr temp (C)"]+273

resistivity, resistivity_unc = calc_res(x_sr, y_sr, x_par)

if mode == "choosepoints":
    # first, do dumb plot of resistance. We will use this to choose start and end points for each sweep (manually)

    # maybe we try to do some fitting. Let's do a fourth-order polynomial fit, find all crossings, and mark these points

    xindices = list(range(len(resistivity)))

    fit = np.polynomial.Polynomial.fit(xindices[0:19000], resistivity[0:19000], deg=4)
    print("FIT", fit)

    fit_yvals = [fit(x) for x in xindices]

    calc_crossings = []

    curr_period_start = 0
    greaterthan = (resistivity[0] > fit_yvals[0])
    index = 0
    for emp, fit in zip(resistivity, fit_yvals): # this effectively just finds zero crossings. So combine every two lists after
        # let pos -> neg transition denote new period
        if emp < fit and greaterthan == True:
            if (index - curr_period_start) > 500: calc_crossings.append([curr_period_start, index])
            curr_period_start = index

        greaterthan = (emp > fit)

        index += 1

    calc_crossings_merged = []

    for i in range(0, len(calc_crossings)-1, 2):
        calc_crossings_merged.append([calc_crossings[i][0], calc_crossings[i+1][1]])

    print(calc_crossings)

    plt.plot(resistivity)
    plt.plot(fit_yvals)

    for el in calc_crossings:
        plt.plot([el[0], el[1]], [statistics.mean(resistivity)]*2)

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

if mode == "testrt": # fix here

    plt.rcParams["figure.figsize"] = (5,4)
    plt.tight_layout()
    plt.gca().ticklabel_format(axis='y', scilimits=[-3, 3])

    for sw_time, temp, res in hyst_sweeps:
        temp, res = (list(t) for t in zip(*sorted(zip(temp, res))))
        plt.scatter(temp, res, s=2, alpha=0.1)
    for sw_time, temp, res in no_hyst_sweeps:
        temp, res = (list(t) for t in zip(*sorted(zip(temp, res))))
        plt.plot(temp, res, label=(str( round((sw_time[0]-time[0])/60,2) ) + "hrs"))
        #plt.scatter(temp, res, label=(str( round((sw_time[0]-time[0])/60,2) ) + "hrs"), marker = '+', s=4)

    plt.grid()
    plt.legend(prop={'size': 9})
    plt.xlabel("temperature (K)")
    plt.ylabel("$V_{34}/I_{12}$ (ohms)")

    plt.title("DYT048 AC $ρ(T)$")

    plt.show()

if mode == "fitrt":
    # assume temperature dependence goes as R = T^-3/2 R0 exp(Eg/2KbT).
    # so approx -> Tln(R) = Tln(R0) + Eg/2Kb. Just to start, let's plot these against each other
        # plotting Tln(R) against T. Then can extract ln(R0), Eg/2Kb from linear fit
        # so R0 = exp(slope)
    # replaced with real curve fit.

    Eg_all = []

    for sw_time, temp, res in no_hyst_sweeps:
        # BAD APPROX START
        # TlnR = [t*math.log(r) for t,r in zip(temp, res)]
        # plt.scatter(temp, TlnR, marker="+")

        # we do a linear fit to extract slope and intercept

        # slope, intercept, r2, predicted, stderr, prederr, int_stderr = linearfit(temp, TlnR)

        # now we calculate the band gap
        # Eg = 2 * kB * intercept
        # Eg_unc = 2 * kB * int_stderr
        # BAD APPROX END

        Eg, r0, Eg_unc, r0_unc, predicted, preder = fittobandgap(temp, res)

        Eg_all.append(Eg)

        # label by timestamp
        scan_starttime = str(round((sw_time[0]-time[0])/60,2)) + " hrs"

        print(scan_starttime + ": Eg =", round(Eg,5), "±", round(Eg_unc,5), "eV, R0 = ",round(r0,5),"±", round(r0_unc,5),"ohm")

    print("\nOverall Eg =", round(statistics.mean(Eg_all),5), "±", round(statistics.stdev(Eg_all),5), "eV")

    #plt.show()

elif mode == "plotrt":

    fig, tempax = plt.subplots()
    resax = tempax.twinx()

    tempax.set_xlabel("time (minutes)")
    tempax.set_ylabel("temperature (K)")
    resax.set_ylabel("$V_{34}/I_{12}$ (ohms)")
    print(time)
    resax.plot(time, [r+u for r,u in zip(resistivity, resistivity_unc)], alpha=0.5, c='b')
    resax.plot(time, [r-u for r,u in zip(resistivity, resistivity_unc)], alpha=0.5, c='b')
    resax.plot(time, resistivity, label="Ω")
    tempax.plot(time, temp_th, c='orange', label = "T")

    resax.legend(loc=1)
    tempax.legend(loc=2)

    resax.set_xlim([0, 60])
    #resax.set_xlim([0, 5300])
    resax.set_ylim([0,6e5])
    plt.grid()
    plt.show()

elif mode == "twopoint":

    par_v, par_v_unc = calibrator.translate_v(abs(x_par))
    current = par_v / 1e4
    resistivity = [50e-3 / c for c in current] # this is amplitude of wave provided by SR830

    plt.plot(time, resistivity)
    plt.grid()
    plt.xlabel("time (minutes)")
    plt.ylabel("resistance (ohms)")
    plt.title("two-point AC IV")

    plt.show()

elif mode == "plotdetvtime":
    # this requires us to do the same manipulation as in fitrt, extract the coefficients and uncertainties, and plot

    Egs = []
    Eg_uncs = []

    r0s = []
    r0_uncs = []

    times = []


    for sw_time, temp, res in no_hyst_sweeps:
        #TlnR = [t*math.log(r) for t,r in zip(temp, res)]

        ## we do a linear fit to extract slope and intercept

        #slope, intercept, r2, predicted, stderr, prederr, int_stderr = linearfit(temp, TlnR)

        ## now we calculate the band gap and r0
        #Eg = 2 * kB * intercept
        #Eg_unc = 2 * kB * int_stderr

        #r0 = math.exp(slope)
        #r0_unc = math.exp(slope)*stderr

        Eg, r0, Eg_unc, r0_unc, predicted, preder = fittobandgap(temp, res)

        Egs.append(Eg)
        Eg_uncs.append(Eg_unc)

        r0s.append(r0)
        r0_uncs.append(r0_unc)

        scan_starttime = (sw_time[0]-time[0])/60
        times.append(scan_starttime)

    # just for fun, we do linear fits to the band gap and r0 to 'guide the eye'
    # TODO: fix gross legend formatting - want both legends on one axes

    s, i_eg, r2_eg, bgpred, s, peg, ist_eg = linearfit(times, Egs)
    s, i, r2, r0pred, s, pr0, ist = linearfit(times, r0s)

    chi2stat = 0
    dof = -2 # two free fitting parameters

    resids = [yemp - ypred for yemp, ypred in zip(Egs, bgpred)]

    for resid, stdev in zip(resids, Eg_uncs):
        if stdev != 0:
            dof += 1
            chi2stat += (resid/stdev)**2

    chi2dof = chi2stat/dof



    print("extrapolated zero-time Eg:",i_eg,"pm",ist_eg,"ev","r2",r2_eg, "chi2",chi2dof)

    # now we plot R0, Eg on same axes
    fig, bgax = plt.subplots()
    r0ax = bgax.twinx()

    fig = plt.gcf()
    fig.set_size_inches(5,4)

    r0ax.ticklabel_format(axis='y', scilimits=[-1, 1])
    #bgax.ticklabel_format(axis='y', scilimits=[-2, 2])

    #r0ax.yaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
    bgax.yaxis.set_major_formatter(FormatStrFormatter('%0.3f'))

    bgax.set_xlabel("Time (hours)")
    bgax.set_ylabel("Eg (eV)")
    r0ax.set_ylabel("$R_0$ (arb. units)")
    fig.subplots_adjust(right=0.85)
    fig.subplots_adjust(left=0.18)

    bgax.scatter(times, Egs, marker="+", label="$E_g$", c='blue')
    bgax.errorbar(times, Egs, Eg_uncs, linestyle="None", ecolor='blue', alpha=0.5)
    bgax.plot(times, bgpred, c='blue', alpha=0.5)

    r0ax.scatter(times, r0s, marker="+", label="$R_0$", c='orange')
    r0ax.errorbar(times, r0s, r0_uncs, linestyle="None", ecolor='orange', alpha=0.5)
    r0ax.plot(times, r0pred, c='orange', alpha=0.5)

    r0ax.legend(loc='upper right')
    bgax.legend(loc='upper left')
    plt.grid()
    plt.show()
