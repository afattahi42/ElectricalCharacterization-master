import time
import serial
import numpy as np

class Lakeshore421:
    # configure the serial connections
    def __init__(self, comport):
        self.ser = serial.Serial(
            port=comport,
            baudrate=9600
        )
        self.ser.close()
        self.ser.open()
        self.ser.isOpen()

    def readval(self, command, parse=True):
        #\r\n is for device terminators set to CR LF
        self.ser.write((command+'\r\n').encode('utf-8'))
        #wait one second before reading output.
        time.sleep(1)
        out=''
        while self.ser.inWaiting() > 0:
            print(out)
            n =self.ser.read(1)
            print(n, type(n))
            out += n.decode('utf-8', errors = "ignore")
            time.sleep(1)
        if out != '':
            out=out.rstrip()
            if parse: return float(out)
            else: return out

    def readx(self):
        return self.readval("OUTP?1")
    
    def ready(self):
        return self.readval("OUTP?2")

    def readr(self):
        return self.readval("OUTP?3")

    def readtheta(self):
        return self.readval("OUTP?4")

    def readf(self):
        return self.readval("FREQ?")

    def readv(self):
        return self.readval("SLVL?")

    def readall(self):
        csv = self.readval("SNAP?1,2,3,4", parse=False).split(",")
        x = float(csv[0])
        y = float(csv[1])
        r = float(csv[2])
        theta = float(csv[3])
        return x,y,r,theta

    def readlock(self):
        lockbit = self.readval("LIAS?3")
        print("UNLOCK STATUS",lockbit)
        return(lockbit)

    def setf(self, f):
        self.ser.write(("FREQ"+str(f)+'\r\n').encode('utf-8'))

    def setv(self, v):
        self.ser.write(("SLVL"+str(v)+'\r\n').encode('utf-8'))
    

#LIA = SR830('com4')

#x,y,r,theta = LIA.readall()

#print(x,y,r,theta)

# LIA.setv(0)
# LIA.setf(10)

# #sys.exit()

# flog = open("2ptscan.txt","w")
# flog.write("f,v,x,y,r,theta\n")


# for f in np.linspace(10,1000,10):
#     for v in np.linspace(0,1,10):
#         LIA.setf(f)
#         LIA.setv(v)
#         time.sleep(0.2)
        
#         x,y,r,theta = LIA.readall()

#         print(f,v,x,y,r,theta)

#         flog.write(str(f)+","+str(v)+","+str(x)+","+str(y)+","+str(r)+","+str(theta)+"\n")

# flog.close()



