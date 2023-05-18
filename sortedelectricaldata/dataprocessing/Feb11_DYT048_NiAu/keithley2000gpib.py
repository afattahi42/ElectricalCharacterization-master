#from pymeasure.instruments.keithley import Keithley2000
import pyvisa as visa
import math
import time

class k2000:
    def __init__(self):
        rm = visa.ResourceManager()
        self.inst = rm.open_resource('GPIB0::16')

        self.c0 = 0.9288
        self.c1 = 0.0028
        self.c2 = 1.9983e-6
        self.r25 = 1.035e3

    def res_to_temp(self, res):
        a = self.c2
        b = self.c1
        c = (self.c0-res/self.r25)
        t = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)
        return t

    def read(self):
        return float(self.inst.query(':FETCh?'))

    def fetchtemp(self):
        currval = self.read()
        return currval, self.res_to_temp(currval)
