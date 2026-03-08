import pandas as pd
import numpy as np
import cupy as cp

xp = cp


df = {"order": [4, 3, 5, 1, 0, 2]}
df = pd.DataFrame(df)
order = np.argsort(df["order"].values)
print(df[order])

