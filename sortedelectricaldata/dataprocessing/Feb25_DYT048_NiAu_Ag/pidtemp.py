from simple_pid import PID
import time
import matplotlib.pyplot as plt
from SPD3303X import spd3303x
from keithley2110tc import keithley2110tc
import arduinorelayinterface
import sys

logfname = "tempcontrollog.txt"
f = open(logfname,"a")
f.write("time,desired temp,current,tc_temp\n")
f.close()


# def singleCycle(desired_min = -15, desired_max= 60, p= 5, i = .05, d = .1, current_min = 0, current_max = 5):
   # """cool down to min, go up to max, go down to min"""
    # approach_desired(desired_temp = -15)
    #approach_desired(desired_temp = 50)
    #approach_desired(desired_temp = -15)

def tempSweep(max_temp, temp_interval = 1, time_interval = 60): # sweep rate degrees/second
    """sweeps up to a maximum temperature at constant rate
    """
    print("running tempsweep")

    approach_desired(max_temp = max_temp, rate = temp_interval/time_interval)

def tempSweepHyst(max_temp, min_temp, temp_interval = 1, time_interval = 60): # sweep rate degrees/second
    """sweeps up to a maximum temperature at constant rate, then sweeps down to min_temp  at the same rate
    """

    # assumes min_temp is < 0. Assumes ambient is ~20 C.

    print("running tempsweep - DOWN. Ambient ->",min_temp)
    pid = approach_desired_exit(target_temp = min_temp, heat = -1, direction = -1, rate = temp_interval/time_interval)

    print("running tempsweep - UP.",min_temp,"-> ambient.")
    approach_desired_exit(prev_pid = pid, target_temp = 22, heat = -1, waitatambient = True, direction = 1, rate = temp_interval/time_interval)

    print("running tempsweep - UP. Ambient ->",max_temp)
    pid = approach_desired_exit(target_temp = max_temp, heat = 1, direction = 1, rate = temp_interval/time_interval)

    print("running tempsweep - DOWN.",max_temp,"-> ambient.")
    approach_desired_exit(prev_pid = pid, target_temp = 27, heat = 1, waitatambient = True, direction = -1, rate = temp_interval/time_interval)

   



def approach_desired_exit(prev_pid = None, target_temp = 10, heat = 1, waitatambient = False, waittime_set = 60*5, direction = 1, p= 0.5, i = 0.005, d = 0, current_min = 0, current_max = 2, rate = 1/60, adjust_rate = 5):
    """increases/decreases desired temp. by constant rate and sets current accordingly used pid. 
    Once desired temperature is reached, waits 5 minutes for equilibrium and exits

    direction == 1 => increases temp during sweep
    direction == 0 => decreases temp during sweep

    heat == 1 => running Peltier in heat mode
    heat == 0 => running Peltier in cool mode
    """
    print("running approach_desired_exit to T=",target_temp)
    
    supply = spd3303x()
    keithley = keithley2110tc()
    relays = arduinorelayinterface.Arduino('COM8')

    tc_temp = keithley.thermoCoupleTemp()
    supply.set_voltage(12)

    pid = PID(p, i, d, setpoint = tc_temp) 
    if prev_pid != None: pid = prev_pid

    pid.output_limits = (current_min, current_max) 

    original_temp = tc_temp
    start_time = time.time()
    current_time = time.time()

    wait_time = 0
    wait_timer = False
    hit_initial_value = False
    hit_initial_value_counter = 0

    desired_temp = original_temp

    while True:
        if time.time() - current_time > adjust_rate:
            pass
        else:
            time.sleep(adjust_rate- (time.time() - current_time))
        
        current_time = time.time()
        
        tc_temp = keithley.thermoCoupleTemp()
        
        kill_function(tc_temp)

        if not hit_initial_value: 
            print("WAITING TO REACH START VALUE, counter =",hit_initial_value_counter,"/ 100")
            hit_initial_value_counter += 1
            start_time = time.time()

        if hit_initial_value_counter > 100 and not hit_initial_value:
            hit_initial_value = True

        if not wait_timer and hit_initial_value: desired_temp = original_temp + direction*rate*(time.time()-start_time)
        if wait_timer: desired_temp = target_temp
        #print("tar",target_temp,"des",desired_temp,"curr",tc_temp)

        if desired_temp > target_temp and direction == 1 and wait_timer == False and hit_initial_value:
            wait_time = time.time()
            wait_timer = True
            print("REACHED TARGET TEMP ... WAITING FOR EQUILIBRIUM")
        if desired_temp < target_temp and direction == -1 and wait_timer == False and hit_initial_value:
            wait_time = time.time()
            wait_timer = True
            print("REACHED TARGET TEMP ... WAITING FOR EQUILIBRIUM")


        if tc_temp > original_temp and direction == 1 and not hit_initial_value:
            hit_initial_value = True
        if tc_temp < original_temp and direction == -1 and not hit_initial_value:
            hit_initial_value = True


        if wait_timer and (time.time() - wait_time > waittime_set): return pid


        # flipping relays. Note that P1 -> cooling, P2 -> heating
        if heat == -1: relays.enable_P1()
        if heat == 1: relays.enable_P2()

        pid.setpoint = heat * desired_temp # by inverting both quantities when cooling, we also invert the delta
        current = pid(heat * tc_temp)
        if waitatambient and wait_timer: current = 0
        supply.set_current(current)
        print("desired_temp = " + str(desired_temp), "current = " + str(current), "tc_temp = " +  str(tc_temp))

        f = open(logfname,"a")
        f.write(str(time.time())+","+str(desired_temp)+","+str(current)+","+str(tc_temp)+"\n")
        f.close()


def approach_desired(prev_val = None, max_temp = 10, p= 0.5, i = 0.02, d = 0, current_min = 0, current_max = 1, rate = 1/60, adjust_rate = 5):
    """increases desired temp. by constant rate and sets current accordingly used pid. 
    Once desired temperature is reached, holds that temperature
    """
    print("running approach_desired")
    
    supply = spd3303x()
    keithley = keithley2110tc()

    
    tc_temp = keithley.thermoCoupleTemp()
    supply.set_voltage(12)

    pid = PID(p, i, d, setpoint = tc_temp) 
    pid.output_limits = (current_min, current_max) 
    if prev_val != None: pid.set_auto_mode(True, last_output=prev_val)

    original_temp = tc_temp
    start_time = time.time()
    current_time = time.time()

    #abs(keithley.thermoCoupleTemp() - desired_temp) > .01
    while True:
        if time.time() - current_time > adjust_rate:
            pass
        else:
            time.sleep(adjust_rate- (time.time() - current_time))
        
        current_time = time.time()
        
        tc_temp = keithley.thermoCoupleTemp()
        
        kill_function(tc_temp)

        desired_temp = original_temp + rate*(time.time()-start_time)
        if desired_temp > max_temp:
            desired_temp = max_temp

        pid.setpoint = desired_temp
        current = pid(tc_temp)
        supply.set_current(current)
        print("desired_temp = " + str(desired_temp), "current = " + str(current), "tc_temp = " +  str(tc_temp))

def kill_function(tc_temp):
    """ kills if temp above 70 C"""

    if tc_temp > 70:
        supply = spd3303x()
        supply.set_voltage = 0
        supply.set_current = 0
        print("temp above 70C")
        print("EXITING - TEMP > 70 C")
        sys.exit()

#while True: tempSweepHyst(60,30)


while True:
    tempSweepHyst(50,5)
    tempSweepHyst(50,5)
    print("Waiting for next sweep...")
    waitstarttime = time.time()
    while (time.time() - waitstarttime < 60*60*4):
        time.sleep(3)

#approach_desired_exit(target_temp = 10, waittime_set = 60*20, heat = -1, direction = -1, rate = 1/60)