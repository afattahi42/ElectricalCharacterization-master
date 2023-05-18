import matplotlib.pyplot as plt
import pandas as pd
import statistics
import math

plot_raw = False
plot_vtemp  = False
plot_vtime = True

plt.rcParams["figure.figsize"] = (12,6)

data = pd.read_csv('logthermistortcfilmres - Copy (3).txt')

time = data["time (unix)"]
tctemp = data[" tc temp (C)"]
trtemp = data[" tr temp (C)"]
trres  = data[" tr res (ohm)"]
filmres = data[" film res (ohm)"]

filmres_pos = abs(filmres)

if plot_raw:
    fig, (ax1, ax2) = plt.subplots(1,2)

    ax1.scatter([t+273 for t in trtemp], filmres_pos, label="thermistor", marker='+')
    ax1.scatter([t+273 for t in tctemp], filmres_pos, label="tc", marker='+')
    ax1.legend()
    ax1.set_xlabel("temperature (K)")
    ax1.set_ylabel("$V_{34}/I_{12}$ (ohms)")
    ax1.grid()

    ax2.scatter([(t-time[0])/60 for t in time], [t+273 for t in trtemp], label="thermistor", marker='+')
    ax2.scatter([(t-time[0])/60 for t in time], [t+273 for t in tctemp], label="tc", marker='+')
    ax2.legend()
    ax2.set_xlabel("time (minutes)")
    ax2.set_ylabel("temperature (K)")
    ax2.grid()

    plt.show()


# now - process data to eliminate hysteresis
# naively, we round all resistivity measurements to the nearest degree, then average all measurements

if plot_vtemp:

    res_tctemp_dict = {}
    res_trtemp_dict = {}

    tctemp_rounded = [round(t)+273 for t in tctemp]
    trtemp_rounded = [round(t)+273 for t in trtemp]

    for tc, tr, res in zip(tctemp_rounded, trtemp_rounded, filmres_pos):
        if tc in res_tctemp_dict.keys():
            res_tctemp_dict[tc].append(res)
        else:
            res_tctemp_dict[tc] = [res]

        if tr in res_trtemp_dict.keys():
            res_trtemp_dict[tr].append(res)
        else:
            res_trtemp_dict[tr] = [res]

    res_tctemp_avg = []
    res_trtemp_avg = []
    tctemp_avg = []
    trtemp_avg = []  

    for key in res_tctemp_dict.keys():
        tctemp_avg.append(key)
        res_tctemp_avg.append(statistics.mean(res_tctemp_dict[key]))

    for key in res_trtemp_dict.keys():
        trtemp_avg.append(key)
        res_trtemp_avg.append(statistics.mean(res_trtemp_dict[key]))

    plt.scatter(trtemp_avg, res_trtemp_avg, label="thermistor", marker='+')
    #plt.scatter(tctemp_avg, res_tctemp_avg, label="thermocouple", marker='+')

    plt.legend()
    plt.xlabel("temperature (K)")
    plt.ylabel("$V_{34}/I_{12}$ (ohms)")
    plt.grid()

    plt.show()

if plot_vtime:

    plt.scatter([(t-time[0])/60 for t in time], filmres_pos, marker='+')
    plt.xlabel("time (minutes)")
    plt.ylabel("$V_{34}/I_{12}$ (ohms)")
    plt.yscale('log')
    plt.ylim([1,1e9])
    plt.grid()
    plt.show()

# trying to fit to variable-range hopping model for conductivity

#logtr = [math.log(1/res) for temp, res in zip(trtemp_avg, res_trtemp_avg)]
#t14 = [math.pow(temp+273, 1) for temp, res in zip(trtemp_avg, res_trtemp_avg)]

#plt.scatter(logtr, t14, marker='+')
#plt.xlabel('$T^{-1/4}$ (K)')
#plt.ylabel('$ln(\sigma)$')
#plt.grid()
#plt.show()