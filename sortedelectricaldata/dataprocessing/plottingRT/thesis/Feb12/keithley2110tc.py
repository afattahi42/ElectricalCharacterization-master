import pyvisa as visa

class keithley2110tc:
    def __init__(self):
        rm = visa.ResourceManager()
        #instrument = rm.list_resources()[0]
        #self.inst = rm.open_resource(instrument)

        self.inst = rm.open_resource("USB0::0x05E6::0x2110::8008050::INSTR")

    def thermoCoupleTemp(self):
        temp = float(self.inst.query('meas:tco?'))
        return temp