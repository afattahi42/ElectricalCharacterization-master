import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("sampletest_dyt48.txt")

time = [(t - data["time"][0])/60 for t in data["time"]]
res = data["res"]

plt.plot(time, res)
plt.xlabel("time (minutes)")
plt.ylabel("resistance (uncal)")
plt.show()