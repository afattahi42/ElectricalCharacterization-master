import time
import pyvisa as visa
import numpy as np

class SR830_GPIB:
    # configure the serial connections
    def __init__(self):

        rm = visa.ResourceManager()

        self.inst = rm.open_resource('GPIB0::2::INSTR')

    def readval(self, command, parse=True):


        out = self.inst.query(command)
        if parse: return float(out)
        else: return out

        #\r\n is for device terminators set to CR LF
        #self.ser.write((command+'\r\n').encode('utf-8'))

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



