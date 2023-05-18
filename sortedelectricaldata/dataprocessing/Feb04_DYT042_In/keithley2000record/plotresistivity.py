import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("resistivitytest.txt", header=None)
print(data)

times = data[0]
resistivities = data[1]

plt.plot(times, resistivities)
plt.show()
