import SR830
import SR830_gpib
import time

# note: we assume two SR830 lock ins, one over serial and one over GPIB.
# The serial lock in provides frequency, a source sine wave, and measures voltage through a preamp
# The GPIB lock in measures current through a preamp

current_preamp_gain = 1e6
voltage_preamp_gain = 10

fn = "sampletest_dyt48.txt"

LIA_V = SR830.SR830('com6')
LIA_A = SR830_gpib.SR830_GPIB()

f = open(fn, "a")
f.write("time,res,x_v,y_v,r_v,t_v,x_a,y_a,r_a,t_a\n") # v corresponds to voltage, a corresponds to current
f.close()

while True:

    x_v,y_v,r_v,t_v = LIA_V.readall()
    x_v = x_v / voltage_preamp_gain
    y_v = y_v / voltage_preamp_gain
    r_v = r_v / voltage_preamp_gain

    x_a,y_a,r_a,t_a = LIA_A.readall()
    x_a = x_a / current_preamp_gain
    y_a = y_a / current_preamp_gain
    r_a = r_a / current_preamp_gain

    res = x_v/x_a

    print("V=",x_v,"I=",x_a,"=> R=",res)

    lockstatus = LIA_A.readlock() # as clock from LIA_V
    currtime = time.time()


    print(str(currtime), res, x_v, x_a, y_v, y_a, r_v, r_a, t_v, t_a)

    f = open(fn, "a")
    if not lockstatus: f.write(str(currtime)+","+str(res)+","+str(x_v)+","+str(x_a)+","+str(y_v)+","+str(y_a)+","+str(r_v)+","+str(r_a)+","+str(t_v)+","+str(t_a)+"\n")
    f.close()

    time.sleep(2)
