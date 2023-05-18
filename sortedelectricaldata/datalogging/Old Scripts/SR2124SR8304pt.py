import MachineCode.SR830
import MachineCode.keithley2000gpib
import MachineCode.bk5491bthermistor as bk5491b
import MachineCode.keithley2110tc
import time
import MachineCode.SR2124

fn = "logPAR124_SR830_sweeps.txt"

LIA8 = SR830.SR830('COM5')
# thermistor = keithley2000gpib.k2000() # this is connected to the output of the PAR124A

LIA2 = SR2124.SR2124('COM3')

f = open(fn, "a")
f.write("time,tc temp (C),tr temp (C),tr res (ohm),sr2124,x,y,r,theta\n")
f.close()

while True:
    sr2124 = LIA2.readall()[0]
    temp_tc = tc.thermoCoupleTemp()
    #res_tr, temp_tr = thermistor.fetchtemp()
    res_tr = 0
    temp_tr = 0

    x,y,r,theta = LIA8.readall()
    lockstatus = LIA8.readlock()
    currtime = time.time()


    print(str(currtime), temp_tc, temp_tr, sr2124, x, y, r, theta)

    f = open(fn, "a")
    if not lockstatus: f.write(str(currtime)[:2]+","+str(temp_tc)+","+str(temp_tr)+","+str(res_tr)+","+str(sr2124)+","+str(x)+","+str(y)+","+str(r)+","+str(theta)+"\n")
    f.close()

    time.sleep(2)
