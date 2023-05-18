from simple_pid import PID
import time
import matplotlib.pyplot as plt
from MachineCode.SPD3303X import spd3303x
from MachineCode.keithley2110tc import keithley2110tc
from MachineCode import arduinorelayinterface
import sys
from MachineCode import bk5491bthermistor

######################
# Sweep parameters
desiredTemp = 25 # min is like 6ish unless we bump the current  up, need to check max current for pelt elements tho

# .
#######################

timeStamp = str(time.time())[:10]
fn = "fixedTemp{}.txt".format(timeStamp)
f = open("Data/tempControl/"+fn, "w+")
f.write("t,i,temp_desired,temp_tc,therm_res,therm_temp\n")
f.close()
# pid: 25, 1, 0, .25 within .01; 60, .2, .008, .18 within 1; 10, 1.2, .01, .1 within .1;
def main(desired_temp = desiredTemp, p= 1, i = 0 , d = .25): # i = .02
    supply = spd3303x(1)
    keithley = keithley2110tc(2)
    relays = arduinorelayinterface.Arduino('COM8')
    pid = PID(p, i, d, setpoint = desired_temp) 
    pid.output_limits = (0, 1.5) 
    supply.set_voltage(12, channel = 2)
    thermistor = bk5491bthermistor.bkthermistor("COM11")
    


    while True:
        if desired_temp < 22:
            heat = -1
            relays.enable_P1()
        else:
            heat = 1
            relays.enable_P2()

        tc_temp = keithley.thermoCoupleTemp()
        kill_function(tc_temp)
        therm_res, therm_temp = thermistor.fetchtemp()
        

        pid.setpoint = desired_temp * heat
        current = pid(tc_temp*heat)

        supply.set_current(current, channel = 2)

        current_time = time.time()
        plt.scatter(current_time, tc_temp, color = 'green')
        plt.scatter(current_time, therm_temp, color = 'green')
        print("desired_temp = " + str(desired_temp), "current = " + str(current), "tc_temp = " +  str(tc_temp) + " therm_res = " + str(therm_res) + " therm_temp = " + str(therm_temp))

        f = open("Data/tempControl/"+fn, "a")
        f.write("{},{},{},{},{},{}\n".format(current_time, desired_temp, current, tc_temp, therm_res, therm_temp))
        f.close()

        time.sleep(.6)


def kill_function(tc_temp):
    """ kills if temp above 70 C"""

    if tc_temp > 70:
        supply = spd3303x(1, channel = 2)
        supply.set_voltage(0, channel = 2)
        supply.set_current(0, channel = 2)
        print("temp above 70C")
        print("EXITING - TEMP > 70 C")
        sys.exit()

main()