import numpy as np
import time
import matplotlib.pyplot as plt

import pyvisa as visa

class spd3303x:
    def __init__(self):
        rm = visa.ResourceManager()
        #instrument = rm.list_resources()[0]
        #self.inst = rm.open_resource(instrument)

        self.inst = rm.open_resource('USB0::0x0483::0x7540::SPD3XIDD5R6466::INSTR')
        self.inst.write('CH1:CURRent 0\n')
        time.sleep(0.2)
        self.inst.write('CH1:VOLTage 0\n')
        time.sleep(0.2)

        #print(self.inst.read())

    def set_voltage(self, voltage):
        self.inst.write('CH1:VOLTage ' + str(voltage) + '\n')
        time.sleep(0.2)

    def set_current(self, current):
        self.inst.write('CH1:CURRent ' + str(current) + '\n')
        time.sleep(0.2)



