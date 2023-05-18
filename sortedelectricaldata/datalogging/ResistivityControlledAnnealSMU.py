from MachineCode import SR2124
from MachineCode.SPD3303X import spd3303x
import numpy as np
import time
import os
from MachineCode.keithley2110tc import keithley2110tc
from MachineCode.arduinorelayinterface import Arduino
from MachineCode.Keithley2400 import Keithley2400
from MachineCode import SR830

######################
# Sweep parameters
minV = -40
maxV = 40
numPoints = 51
annealTime = 120
annealVoltage = 80
annealIncrement = 2.5
totalRunTime = 60*60*12
sampleID = None
maxVGate = 201
#######################




startTime = time.time()
timeStamp = str(time.time())[:10]
fn = "resistivity{}.txt".format(timeStamp)

f = open("Data/ResistivityDCBiasSMU/"+fn, "w+")
f.write("t,i,x,y,r,theta,xK,tc,therm,dc,trueGateDC,trueGateI,x2,y2,r2,theta2\n")
f.close()


LIA = SR2124.SR2124('COM7')
relay = Arduino("COM3")
keith = Keithley2400("COM10")
LIA2 = SR830.SR830("COM9")

keith.slowIVMode()
keith.setComplianceCurrent(.001)# safety control
keith.setVoltage(0) # safety control


sweepSpaceL = [[0, maxV, numPoints], [maxV, 0, numPoints], [0, minV, numPoints], [minV, 0, numPoints]]
keith.outputOn()


def anneal(annealVoltage, annealTime):
    start_time = time.time()
    current_time = time.time()
    while current_time - start_time < annealTime:
        current_time = time.time()
        keith.setVoltage(annealVoltage)
        dc = annealVoltage
        LIA.overloadDetect()

        data = keith.read2()
        formattedData = data.decode().strip().split(',')
        trueGateDC = formattedData[0]
        trueGateI = formattedData[1]
        print(trueGateDC, trueGateI)

        x, y, r, theta =LIA.readall() 
        x2, y2, r2, theta2 =LIA2.readall() 
        lockstatus = LIA.readlock()
        # xK = keith.voltage() * LIA.readsens()/10
        xK = 0
        # tc = keith.thermoCoupleTemp()
        i = 0
        tc = 0
        #therm = keith.resistance()
        therm = 0
        #temp = 0
        f = open("Data/ResistivityDCBiasSMU/"+fn, "a")
        t = time.time() # - startTime
        #print("t: {}, i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}, tc: {}, therm: {}, dc: {}, trueGateDC: {}, trueGateI: {}".format(t-startTime, i, x, y, r, theta, xK, tc, therm, dc, trueGateDC, trueGateI))
        f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(t, i, x, y, r, theta, xK, tc, therm, dc, trueGateDC, trueGateI, x2, y2, r2, theta2) + "\n")
        f.close()
        time.sleep(1)

def voltage_stepDown(inst, channel):
    current_voltage = inst.read_voltage(channel)
    #while 

startTime = time.time()
runTime = time.time() - startTime

while annealVoltage < maxVGate:
    anneal(annealVoltage = annealVoltage, annealTime = annealTime)
    for sweepSpaceParams in sweepSpaceL:
        sweepSpace = np.linspace(sweepSpaceParams[0], sweepSpaceParams[1], sweepSpaceParams[2])
        for dc in sweepSpace:
            keith.setVoltage(dc) # tass?
            LIA.overloadDetect()

            data = keith.read2()
            formattedData = data.decode().strip().split(',')
            trueGateDC = formattedData[0]
            trueGateI = formattedData[1]
            print(trueGateDC, trueGateI)

            x, y, r, theta =LIA.readall() 
            x2, y2, r2, theta2 =LIA.readall() 
            lockstatus = LIA.readlock()
            # xK = keith.voltage() * LIA.readsens()/10
            xK = 0
            # tc = keith.thermoCoupleTemp()
            i = 0
            tc = 0
            #therm = keith.resistance()
            therm = 0
            #temp = 0
            f = open("Data/ResistivityDCBiasSMU/"+fn, "a")
            t = time.time() # - startTime
            #print("t: {}, i: {}, x: {}, y: {}, r: {}, theta: {}, xK: {}, tc: {}, therm: {}, dc: {}, trueGateDC: {}, trueGateI: {}".format(t-startTime, i, x, y, r, theta, xK, tc, therm, dc, trueGateDC, trueGateI))
            f.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(t, i, x, y, r, theta, xK, tc, therm, dc, trueGateDC, trueGateI, x2, y2, r2, theta2) + "\n")
            f.close()
    runTime = time.time()-startTime
    annealVoltage += annealIncrement
            




    
#SPD3303x.set_voltage(0, channel = 2)
#SPD3303x.set_current(0, channel = 2)    

    

LIA.autoOffsetX()
time.sleep(3)
LIA.autoOffsetY()

keith.outputOff()
