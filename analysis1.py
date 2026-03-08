# First example of Data Analysis after cleaning the data in clean.py
# This example focuses on analyzing smoothie and coffee buying trends over the year
# My hypothesis is that the number of Smoothies bought increases during summer and lowers during winter
# and that the number of Coffees bought increases during winter and lowers during summer

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from clean import wanted_columns

# Import cleaned data
data = pd.read_csv("clean_data.csv")

columns = ["Transaction Date", "Item"] # Wanted columns
new_data = wanted_columns(data, columns) # New dataset using function from clean.py
new_data["Transaction Date"] = pd.to_datetime(new_data["Transaction Date"]) # Turn the "Transaction Date" strings to datetime datatype
all_dates = pd.date_range( # Create series of all dates for filling in missing values later
    start=new_data["Transaction Date"].min(),
    end=new_data["Transaction Date"].max()
)
smoothie_data = new_data[new_data["Item"] == "Smoothie"] # Isolate rows that have Smoothie as the Item
coffee_data = new_data[new_data["Item"] == "Coffee"] # Isolate rows that have Coffee as the Item
smoothie_data = smoothie_data.groupby("Transaction Date")["Item"].count() # Count the number of smoothies per date
# Above line automatically removes Dates where no smoothies were purchased
smoothie_data = smoothie_data.reindex(all_dates, fill_value=0) # Fill in the missing dates (no purchase) with a count of 0
coffee_data = coffee_data.groupby("Transaction Date")["Item"].count() # Count the number of coffees per date
coffee_data = coffee_data.reindex(all_dates, fill_value=0) # Fill in the missing dates (no purchase) with a count of 0

# Data is a Series right now with index being the "Transaction Date" and the data being the count with name "Item"
# Want the index to instead be the row number to represent days after January 1st, 2023
# Turn index ("Transaction Date" right now) into its own column, creating a new index that is the row number
smoothie_data = smoothie_data.reset_index()
coffee_data = coffee_data.reset_index()

# Control data for visualizing how the Autocorrelation Function
x = np.arange(365) # Array of days going from 0 to 364
# Function that mimics what I was expecting, a cosine wave with small variations throughout it
# Graph in Desmos for better understanding
y = -20*np.cos(2*np.pi*x/365) + 3*np.sin(2*x) + 20

# Create a 3x2 matrix of graphs when visualizing; Control, Smoothie, and Coffee graphs in the column
# on the left, and a corresponding ACF graph on the right
fig, axes = plt.subplots(3, 2)
axes[0, 0].scatter(x, y, color="red", s=1) # Control scatter plot
axes[0, 0].set_title("Control vs Day")
plot_acf(y, lags=30, ax=axes[0, 1]) # Control ACF graph
axes[1, 0].scatter(smoothie_data.index, smoothie_data["Item"], color="red", s=2) # Smoothie scatter plot
axes[1, 0].set_title("Number of Smoothies vs Day")
plot_acf(smoothie_data["Item"], lags=30, ax=axes[1, 1]) # Smoothie ACF graph
axes[2, 0].scatter(coffee_data.index, coffee_data["Item"], color="red", s=2) # Coffee scatter plot
axes[2, 0].set_title("Number of Coffees vs Day")
plot_acf(coffee_data["Item"], lags=30, ax=axes[2, 1]) # Coffee ACF graph
plt.tight_layout() # Prevents overlap of text
plt.show()

# The Control demonstrates a graph that I was expecting for the Smoothie buying trend, low in
# the winter and high in the summer with gradual shifts. As you can see from the corresponding
# ACF graph, the number of buys heavily correlates to the values of the previous months, a clear pattern.
# In both the Smoothie graph and the Coffee graph the data looks random, and further analysis using ACF
# reveals a correlation of almost 0, so no pattern. The buying trends of Smoothies and Coffee are random
# according to this data.