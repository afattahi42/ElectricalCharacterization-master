import time
import serial

class keithley2000:
    # configure the serial connections
    def __init__(self, comport):
        self.ser = serial.Serial(
            port=comport,
            baudrate=19200
        )
        self.ser.close()
        self.ser.open()
        self.ser.isOpen()

    def readval(self):
        #\r\n is for device terminators set to CR LF
        self.ser.write(':FETCh?\r\n'.encode('utf-8'))
        #wait one second before reading output.
        time.sleep(0.5)
        out=''
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1).decode('utf-8')
        if out != '':
            out=out.rstrip()
            return float(out)

