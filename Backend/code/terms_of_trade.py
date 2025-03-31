import pandas as pd
from exportdata import allexports

# Importing data
terms_of_trade = pd.read_csv("../data/terms_of_trade.csv", skiprows = 4)

columns_to_drop = ['Indicator Name', 'Indicator Code']
terms_of_trade = terms_of_trade.drop(columns_to_drop, axis = 1)
terms_of_trade = terms_of_trade.iloc[:, :66]

terms_of_trade_long = terms_of_trade.melt(id_vars=['Country Name', 'Country Code'], var_name='Year', value_name='Value')
#print(terms_of_trade_long)

# Change to 2020 as base year
# Convert "Year" column to integer
terms_of_trade_long["Year"] = terms_of_trade_long["Year"].astype(int)

# Create a dictionary mapping each country to its 2020 value
base_year_values = terms_of_trade_long[terms_of_trade_long["Year"] == 2020].set_index("Country Name")["Value"].to_dict()

# Map the 2020 value to each row
terms_of_trade_long["base_year_value"] = terms_of_trade_long["Country Name"].map(base_year_values)

# Compute the adjusted ratio, avoiding division errors
terms_of_trade_long["adjusted_ratio"] = terms_of_trade_long.apply(
    lambda row: (row["Value"] / row["base_year_value"] * 100) if pd.notna(row["Value"]) and pd.notna(row["base_year_value"]) else "", 
    axis=1
)

#terms_of_trade_long.to_excel("terms_of_trade_clean.xlsx", index=False)
