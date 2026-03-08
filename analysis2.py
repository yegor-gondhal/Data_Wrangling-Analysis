# Second example of Data Analysis after cleaning the data in clean.py
# This example focuses on analyzing the correlation between certain products
# and in what quantity they are purchased in

# My hypothesis is that sweets, like Cake and Cookies, will be bought in larger quantities
# over the other items since they can often be presents for others or come home for later consumption

import pandas as pd
import matplotlib.pyplot as plt
from clean import wanted_columns

# Import cleaned data
data = pd.read_csv("clean_data.csv")
columns = ["Item", "Quantity"] # Wanted columns
new_data = wanted_columns(data, columns) # Create new dataset using function from clean.py

# Average how many of an item are purchased at once
# Automatically causes the index to be the "Item" column, and Series to be the "Quantity" column
# Use ".reset_index()" at the end to shift the index ("Item" column right now) to be part of the data
avg = new_data.groupby("Item")["Quantity"].mean().reset_index()

print(avg)

plt.figure()
plt.bar(avg["Item"], avg["Quantity"]) # Bar graph of Item vs Quantity
plt.tight_layout() # Prevent text from overlapping
plt.show()