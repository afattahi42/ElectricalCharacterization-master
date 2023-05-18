import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("DYT048-RH-400K-decrease.txt", skiprows=12, delim_whitespace=True, header=None)

print(data)

vdp = data[3]
lia_x = data[4]
lia_y = data[5]
h = data[2]

lia_x_filt_1 = []
lia_y_filt_1 = []
lia_x_filt_2 = []
lia_y_filt_2 = []
lia_x_filt_3 = []
lia_y_filt_3 = []
h_filt_1 = []
h_filt_2 = []
h_filt_3 = []

for v, x, y, h in zip(vdp, lia_x, lia_y, h):
    if v == 1:
        lia_x_filt_1.append(x)
        lia_y_filt_1.append(y)
        h_filt_1.append(h)
    if v == 2:
        lia_x_filt_2.append(x)
        lia_y_filt_2.append(y)
        h_filt_2.append(h)
    if v == 3:
        lia_x_filt_3.append(x)
        lia_y_filt_3.append(y)
        h_filt_3.append(h)

    plt.ylabel("$V_{34}/I_{12}$ (ohms)")

plt.plot(h_filt_1, lia_x_filt_1, label="$V_{34}(I_{12})$")
plt.plot(h_filt_2, lia_x_filt_2, label="$V_{23}(I_{14})$")
plt.plot(h_filt_3, lia_x_filt_3, label="$V_{24}(I_{13})$")

plt.legend()

plt.xlabel("Field Strength (Oe)")
plt.ylabel("Measured Voltage (V)")
plt.grid()
plt.show()
