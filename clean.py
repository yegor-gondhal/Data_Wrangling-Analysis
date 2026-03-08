import pandas as pd
import numpy as np

# Import uncleaned data
data = pd.read_csv("dirty_cafe_sales.csv")

# Turn cells with "ERROR" or "UNKNOWN" into empty cells
data = data.replace("ERROR", None)
data = data.replace("UNKNOWN", None)

# Turn "Quantity", "Price Per Unit", and "Total Spent" from string to number
for col_name in ["Quantity", "Price Per Unit", "Total Spent"]:
    data[col_name] = pd.to_numeric(data[col_name], errors="coerce")

# The data table follows the rule that Quantity x Price Per Unit = Total Spent

# First find "Quantity" cells that are empty, and then fill them if "Price Per Unit" and "Total Spent" exist
condition = (data["Quantity"].isnull() & data["Price Per Unit"].notnull() & data["Total Spent"].notnull())
data.loc[condition, "Quantity"] = data.loc[condition, "Total Spent"]/data.loc[condition, "Price Per Unit"]

# Second find "Price Per Unit" cells that are empty, and then fill them if "Quantity" and "Total Spent" exist
condition = (data["Quantity"].notnull() & data["Price Per Unit"].isnull() & data["Total Spent"].notnull())
data.loc[condition, "Price Per Unit"] = data.loc[condition, "Total Spent"]/data.loc[condition, "Quantity"]

# Finally, find "Total Spent" cells that are empty, and then fill them if "Quantity" and "Price Per Unit" exist
condition = (data["Quantity"].notnull() & data["Price Per Unit"].notnull() & data["Total Spent"].isnull())
data.loc[condition, "Total Spent"] = data.loc[condition, "Quantity"]*data.loc[condition, "Price Per Unit"]

# Export cleaned data
data.to_csv("clean_data.csv")

# Function for selecting specific columns from the cleaned data
def wanted_columns(data, columns):
    # Record initial size as metric for later
    init_size = len(data[columns[0]])

    # Go through each column and remove the rows that have emtpy cells
    for col in columns:
        condition = data[col].notnull()
        data = data.loc[condition]

    # Organize data by date if "Transaction Date" is needed
    if "Transaction Date" in columns:
        dates = data["Transaction Date"] # Isolate "Transaction Data"
        dates = dates.str[:4] + dates.str[5:7] + dates.str[8:] # Turn from form "2023-01-01" to "20230101"
        dates = dates.astype(np.int64) # Turn them into numbers for numpy manipulation
        order = np.argsort(dates.values) # Find the order that they should go in to be organized
        data = data.iloc[order] # Apply that order to each row


    # Select only the columns that are wanted
    new_data = data[columns]

    # Record number of rows after to see how many remain
    after_size = len(new_data[columns[0]])
    print("Number of Rows: ", after_size)
    print("Percentage of what was: ", 100*after_size/init_size)

    return new_data