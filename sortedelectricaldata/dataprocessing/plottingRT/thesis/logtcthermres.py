import bk5491bthermistor
import keithley20004pt
import keithley2110tc
import time

thermistor = bk5491bthermistor.bkthermistor('com3')
filmres    = keithley20004pt.keithley2000('com4')
tc         = keithley2110tc.keithley2110tc()

filename = 'logthermistortcfilmres.txt'
f = open(filename, "a")
f.write("time (unix), tc temp (C), tr temp (C), tr res (ohm), film res (ohm)\n")
f.close()

while True:
    temp_tc = tc.thermoCoupleTemp()
    res_tr, temp_tr = thermistor.fetchtemp()
    res_film = filmres.readval()

    print(temp_tc, temp_tr, res_film)

    f = open(filename, "a")
    f.write(str(time.time())+","+str(temp_tc)+","+str(temp_tr)+","+str(res_tr)+","+str(res_film)+"\n")
    f.close()


