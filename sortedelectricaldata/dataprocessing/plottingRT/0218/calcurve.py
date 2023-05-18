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

        slope, intercept, r2, predicted, stderr, prederr = linearfit(par124, sr830)

        self.slope = slope * par124a_gain
        self.intercept = intercept * par124a_gain
        self.prederr = prederr * par124a_gain


        if plot:

            print("r2",r2)
            print("prederr",self.prederr)
            print(slope,"* x +",self.intercept)

            plt.scatter(par124, sr830, marker="+")
            plt.plot(par124, predicted)

            plt.grid()

            plt.ylabel("SR830 (V)")
            plt.xlabel("PAR124A (V)")

            plt.show()

        return self.slope, self.intercept, self.prederr

    def translate_v(self, point):
        volt = point*self.slope + self.intercept
        unc = self.prederr

        return volt, unc

#filename = "logPAR124_SR830_calcurve_fixedV.txt"
#calibrator = CalCurve(filename)
#print(calibrator.calc_cal_curve(50e-6, plot=True))
