import matplotlib.pyplot as plt
import pandas as pd

resistorRes = 10*10**3
data = pd.read_csv("DiffRes.txt")

voltAcrossResistor = abs(data["x2"])

dI = voltAcrossResistor/resistorRes
dV = abs(data["r8"])

bias = data["b2"]
R = dV/dI

plt.scatter(bias, R)
plt.xlim(-10,10)
plt.ylim(115,125)
plt.show()


