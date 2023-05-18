import pyvisa as visa

class keithley2110tc:
    def __init__(self, instNo):
        rm = visa.ResourceManager()
        #instrument = rm.list_resources()[0]
        #self.inst = rm.open_resource(instrument)

        # 1 is res, 2 is tc
        if instNo == 1:
            self.inst = rm.open_resource("USB0::0x05E6::0x2110::8008050::INSTR")
        elif instNo == 2:
            self.inst = rm.open_resource("USB0::0x05E6::0x2110::8015782::INSTR")

    def thermoCoupleTemp(self):
        temp = float(self.inst.query('meas:tco?'))
        return temp
    
    def resistance(self):
        r = float(self.inst.query('meas:res?'))
        return r

 