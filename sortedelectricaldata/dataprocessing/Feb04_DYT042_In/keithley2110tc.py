import pyvisa as visa

class keithley2110tc:
    def __init__(self):
        rm = visa.ResourceManager()
        instrument = rm.list_resources()[0]
        self.inst = rm.open_resource(instrument)

    def thermoCoupleTemp(self):
        temp = float(self.inst.query('meas:tco?'))
        return temp