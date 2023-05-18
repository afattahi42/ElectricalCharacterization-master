import math
import time
import serial

# configure the serial connections
class bkthermistor:
# for lt73 3000 2a 1k0 5%:

    def __init__(self, comport):
        self.ser = serial.Serial(
            port=comport,
        )
        self.ser.close()
        self.ser.open()
        self.ser.isOpen()

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

    def fetchtemp(self):
        #\r\n is for device terminators set to CR LF
        self.ser.write(':FETCh?\r\n'.encode('utf-8'))
        #wait one second before reading output.
        time.sleep(0.5)
        out=''
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1).decode('utf-8')
        if out != '':
            out=out.rstrip()
            outfloat = float(out.split(':FETCh?\r')[1])
            return outfloat, self.res_to_temp(outfloat)

    def fetchreading(self):
        #\r\n is for device terminators set to CR LF
        self.ser.write(':FETCh?\r\n'.encode('utf-8'))
        #wait one second before reading output.
        time.sleep(0.5)
        out=''
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1).decode('utf-8')
        if out != '':
            out=out.rstrip()
            outfloat = float(out.split(':FETCh?\r')[1])
            return outfloat



#print(res_to_temp(0.997e3))
