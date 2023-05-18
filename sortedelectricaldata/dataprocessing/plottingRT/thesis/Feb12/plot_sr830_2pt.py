import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("IV13.txt")

curr = abs(data["x"])
volt = data["v"]

resistance = volt/curr

plt.scatter(volt, curr)
plt.show()

plt.plot(volt, resistance)
plt.show()

