import SR830
import keithley2000gpib
import bk5491bthermistor as bk5491b
import keithley2110tc
import time

fn = "logPAR124_SR830_tempsweep_inclneg_2.txt"

LIA = SR830.SR830('com7')
thermistor = keithley2000gpib.k2000() # this is connected to the output of the PAR124A
meter = bk5491b.bkthermistor('com3') # this is connected to the output of the PAR124A

f = open(fn, "a")
f.write("time,tc temp (C),tr temp (C),tr res (ohm),PAR124,x,y,r,theta\n")
f.close()

while True:
    par124 = meter.fetchreading()
    temp_tc = 0
    res_tr, temp_tr = thermistor.fetchtemp()
    x,y,r,theta = LIA.readall()
    lockstatus = LIA.readlock()
    currtime = time.time()


    print(str(currtime), temp_tc, temp_tr, par124, x, y, r, theta)

    f = open(fn, "a")
    if not lockstatus: f.write(str(currtime)+","+str(temp_tc)+","+str(temp_tr)+","+str(res_tr)+","+str(par124)+","+str(x)+","+str(y)+","+str(r)+","+str(theta)+"\n")
    f.close()

    time.sleep(2)
