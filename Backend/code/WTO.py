import pandas as pd
from exportdata import allexports

# Importing data
wto = pd.read_csv("../data/WTO_import_export.csv", encoding='ISO-8859-1')
cpi = pd.read_excel("../data/cpi.xlsx", skiprows = 11)
cpi = cpi[['Year', 'Annual']]

# Drop useless columns
wto_columns_to_drop = [
    'Indicator Category', 'Indicator Code', 'Indicator', 'Reporting Economy Code', 'Partner Economy Code', 'Partner Economy ISO3A Code', 'Product/Sector Classification Code', 'Product/Sector Classification',
    'Period Code', 'Period', 'Frequency Code', 'Frequency', 'Unit', 'Unit Code', 'Value Flag Code', 'Value Flag', 'Text Value'
    ]
wto = wto.drop(wto_columns_to_drop, axis = 1)
wto = wto[wto["Reporting Economy"] != "World"]

# Convert export values from US $ Million to US $
wto['Value'] = wto['Value'] * 1000000

# Adjust for inflation using 2020 as base year
wto_adjusted = wto.merge(cpi, on='Year', how='left')
base_year = 2020
base_cpi = cpi.loc[cpi['Year'] == base_year, 'Annual'].values[0]
wto_adjusted['adjustedexport'] = wto_adjusted['Value'] * (base_cpi / wto_adjusted['Annual'])
wto_adjusted = wto_adjusted[wto_adjusted["Year"] != "2023"] #note: 2023 cpi data unavailable so dropped rows where year == 2023; gravity dataset until 2021 only, so model shouldn't use data in 2022/2023

print(wto_adjusted)
# honestly don't know how useful this dataset can be? since it is for world, not country-country pair
