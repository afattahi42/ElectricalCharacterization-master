import time, serial, os, sys
class Keithley2400LV():
    def __init__(self, portName, verbose=False):
        self.serialDevice = None
        self.portName = portName
        self.verbose = verbose
        self.baudrate = 57600
        self.bytesize = 8
        self.stopbits = 1
        self.parity = "N"
        self.timeout = 2
        self.fullDataPath = None


    def openPort(self):
        self.serialDevice = serial.Serial(port=self.portName,
                                          baudrate=self.baudrate,
                                          bytesize=self.bytesize,
                                          stopbits=self.stopbits,
                                          parity=self.parity,
                                          timeout=self.timeout)


    def closePort(self):
        self.serialDevice.close()


    def turnOutput_ON(self):
        self.serialDevice.write(b"OUTPUT ON\n")
        if self.verbose:
            print("The output for the Keithley 2400-LV at " + self.portName + " has been set to ON")


    def turnOutput_OFF(self):
        self.serialDevice.write(b"OUTPUT OFF\n")
        if self.verbose:
            print("The output for the Keithley 2400-LV at " + self.portName + " has been set to OFF")


    def getMeasermentVoltage(self):
        self.serialDevice.write(b'MEAS:VOLT?\n')
        voltageStr = readKeithley(self.serialDevice)
        if self.verbose:
            print(voltageStr, "is the read voltage from the Keithley 2400-LV")
        return voltageStr


    def setKeithley2400LV_voltage(self, setVoltage):
        self.serialDevice.write(b":FUNC VOLT\n")
        writeString = b":SOUR:VOLT " + numberFormat(setVoltage) + b"\n"
        self.serialDevice.write(writeString)
        if self.verbose:
            print("Keithley 2400-LV was set to a voltage of", setVoltage)


    def getSourceCurrent(self):
        self.serialDevice.write(b'SOUR:CURR?\n')
        current = float(readKeithley(self.serialDevice))
        if self.verbose:
            print(current, "is the read current from the Keithley 2400-LV")


    def setSourceCurrent(self, setCurrent):
        self.serialDevice.write(b"SOUR:FUNC CURR\n")
        writeString = b":SOUR:CURR " + numberFormat(setCurrent) + b"\n"
        self.serialDevice.write(writeString)
        if self.verbose:
            print("Keithley 2400-LV was set to a current of", setCurrent, "Amps")


    def initLEDsweep(self):
        self.serialDevice.write(b"SOUR:CURR:RANG MIN\n")
        self.serialDevice.write(b"SOUR:CURR:RANG UP\n")
        self.serialDevice.write(b"SOUR:CURR:RANG UP\n")
        self.serialDevice.write(b"SOUR:CURR:RANG UP\n")
        self.serialDevice.write(b"SENS:FUNC \"VOLT\"\n")
        self.serialDevice.write(b"SENS:VOLT:PROT " + numberFormat(3) + b"\n")
        self.serialDevice.write(b"SYST:RSEN ON\n")



    def getRange_Keithley2400LV(self):
        writeString = b":CURR:RANG?\n"
        self.serialDevice.write(writeString)
        theRange = readKeithley(self.serialDevice)
        if self.verbose:
            print(theRange, "is the current RANGE from the Keithley 2400-LV")
        return theRange
