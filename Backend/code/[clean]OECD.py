import pandas as pd
from exportdata import allexports

# Importing data
oecd_export = pd.read_csv("../data/OECD_TIVA_EXPORT.csv", encoding='ISO-8859-1')
oecd_import = pd.read_csv("../data/OECD_TIVA_IMPORT.csv", encoding='ISO-8859-1')
cpi = pd.read_excel("../data/cpi.xlsx", skiprows = 11)
cpi = cpi[['Year', 'Annual']]

#OECD Export data
# Drop useless columns
export_columns_to_drop = [
    'STRUCTURE', 'STRUCTURE_ID', 'STRUCTURE_NAME', 'ACTION', 'MEASURE', 'Measure', 'VALUE_ADDED_SOURCE_ACTIVITY', 'Value added origin activity',
    'EXPORTING_ACTIVITY', 'Exporting activity', 'UNIT_MEASURE', 'Unit of measure', 'FREQ', 'Frequency of observation', 'Time period', 'Observation value', 'UNIT_MULT', 'Unit multiplier'
    ]
oecd_export = oecd_export.drop(export_columns_to_drop, axis = 1)

# Convert export values from US $ Million to US $
oecd_export['OBS_VALUE'] = oecd_export['OBS_VALUE'] * 1000000

# Adjust for inflation using 2020 as base year
oecd_export_adjusted = oecd_export.merge(cpi, left_on='TIME_PERIOD', right_on='Year', how='left').drop('Year', axis=1)
oecd_export_adjusted = oecd_export_adjusted.rename(columns={'TIME_PERIOD': 'year'})
base_year = 2020
base_cpi = cpi.loc[cpi['Year'] == base_year, 'Annual'].values[0]
oecd_export_adjusted['adjustedexport'] = oecd_export_adjusted['OBS_VALUE'] * (base_cpi / oecd_export_adjusted['Annual'])

print(oecd_export_adjusted)
# honestly don't know how useful this dataset can be? since it is only for OECD countries, specifically at value added in exports

#OECD Import data
# Drop useless columns
import_columns_to_drop = [
    'STRUCTURE', 'STRUCTURE_ID', 'STRUCTURE_NAME', 'ACTION', 'MEASURE', 'Measure', 
    'EXPORTING_ACTIVITY', 'Exporting activity', 'UNIT_MEASURE', 'Unit of measure', 'FREQ', 'Frequency of observation', 'Time period', 'Observation value', 'UNIT_MULT', 'Unit multiplier'
    ]
oecd_import = oecd_import.drop(import_columns_to_drop, axis = 1)

# Convert export values from US $ Million to US $
oecd_import['OBS_VALUE'] = oecd_import['OBS_VALUE'] * 1000000

# Adjust for inflation using 2020 as base year
oecd_import_adjusted = oecd_import.merge(cpi, left_on='TIME_PERIOD', right_on='Year', how='left').drop('Year', axis=1)
oecd_import_adjusted = oecd_import_adjusted.rename(columns={'TIME_PERIOD': 'year'})
base_year = 2020
base_cpi = cpi.loc[cpi['Year'] == base_year, 'Annual'].values[0]
oecd_import_adjusted['adjustedexport'] = oecd_import_adjusted['OBS_VALUE'] * (base_cpi / oecd_import_adjusted['Annual'])

print(oecd_import_adjusted)
# honestly don't know how useful this dataset can be? since it is only for OECD countries, didnt specify which country the import comes from
