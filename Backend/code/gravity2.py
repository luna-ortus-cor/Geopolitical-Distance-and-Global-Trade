import pandas as pd

# Importing data
gravity = pd.read_csv("../data/Gravity_V202211.csv", dtype={"col_dep_end_conflict": str}, low_memory=False)
countries = pd.read_csv("../data/Countries_V202211.csv")
cpi = pd.read_excel("../data/cpi.xlsx", skiprows = 11)
cpi = cpi[['Year', 'Annual']]

# Filtering for country
gravity = gravity[gravity['country_id_o'] == 'SGP']

# Adding country names
gravity2 = gravity.merge(countries[['country_id', 'country']], 
                        left_on='country_id_o', right_on='country_id', 
                        how='left').rename(columns={'country': 'country_o'}).drop('country_id', axis=1)
gravity2 = gravity2.merge(countries[['country_id', 'country']], 
                        left_on='country_id_d', right_on='country_id', 
                        how='left').rename(columns={'country': 'country_d'}).drop('country_id', axis=1)

# Filtering for years with data
gravity3 = gravity2[(gravity2['year'] >= 1965) & (gravity2['year'] <= 2020)]

# Convert to US $ from US Thousand $
gravity3['tradeflow_comtrade_o'] = gravity3['tradeflow_comtrade_o'] * 1000

# Adjusting for inflation (base year 2020)
gravity4 = gravity3.merge(cpi, left_on='year', right_on='Year', how='left').drop('Year', axis=1)
base_year = 2020
base_cpi = cpi.loc[cpi['Year'] == base_year, 'Annual'].values[0]
gravity4['adjustedexport'] = gravity4['tradeflow_comtrade_o'] * (base_cpi / gravity4['Annual'])

gravity4.to_csv("../data/gravity_sg.csv", index=False)
