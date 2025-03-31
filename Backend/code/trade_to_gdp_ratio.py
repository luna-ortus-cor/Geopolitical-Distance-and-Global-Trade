import pandas as pd
from exportdata import allexports

# Importing data
trade_to_gdp_ratio = pd.read_csv("../data/trade_to_gdp_ratio.csv", skiprows = 4)

columns_to_drop = ['Indicator Name', 'Indicator Code']
trade_to_gdp_ratio = trade_to_gdp_ratio.drop(columns_to_drop, axis = 1)
trade_to_gdp_ratio = trade_to_gdp_ratio.iloc[:, :66]

trade_to_gdp_ratio_clean = terms_of_trade.melt(id_vars=['Country Name', 'Country Code'], var_name='Year', value_name='Value')

#trade_to_gdp_ratio_clean.to_excel("trade_to_gdp_ratio_clean.xlsx", index=False)
