import matplotlib.pyplot as plt
import pandas as pd
import statistics
from scipy.stats import linregress
from functools import reduce
import math

# in general, assume that this calibration is identical (although scaled) between gain values on both lock ins. So just scale slope and intercept.

def linearfit(x, y):
    slope, intercept,r,p,stderr = linregress(x,y)
    predicted = []
    for el in x:
        predicted.append(el*slope + intercept)

    r2 = r**2

    # need to do standard error ourselves. Oh well.

    prederr = math.sqrt((reduce(lambda a, b: a+b, [ (t-e)**2 for t,e in zip(predicted, y)])))

    # In general, try to +/- with SR830 y component. Seems like realistic error.

    return slope, intercept, r2, predicted, stderr, prederr

class CalCurve:

    def __init__(self, filename):
        self.filename = filename

    def calc_cal_curve(self, par124a_gain, plot=False):

        par124a_scaling_factor = 0.5

        data = pd.read_csv(self.filename)

        par124 = abs(data["PAR124"])*par124a_scaling_factor
        sr830  = data["x"]

        par124a_filt = []
        sr830_filt = []

        for p, s in zip(par124, sr830):
            if s < 0.37:
                par124a_filt.append(p)
                sr830_filt.append(s)

        par124 = par124a_filt
        sr830 = sr830_filt

        slope, intercept, r2, predicted, stderr, prederr = linearfit(par124, sr830)

        self.slope = slope * par124a_gain
        self.intercept = intercept * par124a_gain
        self.prederr = prederr * par124a_gain

        # cluster points and estimate uncertainty at each point. Note that we cluster by y value (sr830)

        sr830_cluster = {}
        for v, p in zip(sr830, par124):
            if v not in sr830_cluster.keys(): sr830_cluster[v] = [p]
            else: sr830_cluster[v].append(p)

        # now find mean, standard deviation of each point

        sr830_condensed = []
        par124_condensed = []
        par124_condensed_unc = []

        for key in sr830_cluster.keys():
            if len(sr830_cluster[key]) > 1:
                sr830_condensed.append(key)
                par124_condensed.append(statistics.mean(sr830_cluster[key]))
                par124_condensed_unc.append(math.sqrt(statistics.stdev(sr830_cluster[key])**2))
            else:
                print("NO STDEV FOR PT",key)

        # generating predicted vals

        _slope, _intercept, _r2, _predicted, _stderr, _prederr = linearfit(par124_condensed, sr830_condensed)

        resids = [yemp - ypred for yemp, ypred in zip(sr830_condensed, _predicted)]


        # generating predicted uncertainty

        sr830_condensed_unc = [p*_slope for p in par124_condensed_unc]

        chi2stat = 0
        dof = -2 # two free fitting parameters

        for resid, stdev in zip(resids, sr830_condensed_unc):
            if stdev != 0:
                dof += 1
                chi2stat += (resid/stdev)**2

        chi2dof = chi2stat/dof

        print("chi2dof",chi2dof)

        if plot:

            print("r2",r2)
            print("prederr",self.prederr)
            print(slope,"* x +",self.intercept)

            fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios':[2, 1]})
            fig.tight_layout(pad=2)
            fig.subplots_adjust(left=0.2)

            fig.set_size_inches(5, 5)

            ax[0].scatter(par124_condensed, sr830_condensed, marker="+", color="black")
            ax[0].plot(par124_condensed, _predicted, alpha=0.5, color="black")

            ax[1].scatter(par124_condensed, resids, marker="_", color="black")
            ax[1].errorbar(par124_condensed, resids, sr830_condensed_unc, linestyle="none", color="black")

            ax[1].grid()

            ax[0].set_ylabel("SR830 (V)")
            ax[1].set_ylabel("SR830 Residuals (V)")
            ax[1].set_xlabel("PAR124A (V)")

            plt.show()

        return self.slope, self.intercept, self.prederr

    def translate_v(self, point):
        volt = point*self.slope + self.intercept
        unc = self.prederr

        return volt, unc

filename = "logPAR124A_SR830_calcurve_fixedV_outliersremoved.txt"
calibrator = CalCurve(filename)
print(calibrator.calc_cal_curve(50e-6, plot=True))
