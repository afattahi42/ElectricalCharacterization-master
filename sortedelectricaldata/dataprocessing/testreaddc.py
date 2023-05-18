# just trying to read one of the ASC dc files

import pandas as pd

fname ="Feb25_DYT048_NiAu_Ag/IV12DC.asc"

data = pd.read_csv(fname, delim_whitespace=True, skiprows=5, skipfooter=13, header=None, names=['V', 'I', 'time', 'type', 'other'])
print(data)
