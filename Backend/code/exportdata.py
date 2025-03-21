import pandas as pd

# Importing data
allexports = pd.read_excel("../data/WITS-Partner-All.xlsx", sheet_name='Partner-Timeseries')
chemicalexports = pd.read_excel("../data/WITS-Partner-Chemical.xlsx", sheet_name='Product-TimeSeries-Partner')
consumerexports = pd.read_excel("../data/WITS-Partner-Consumer.xlsx", sheet_name='Product-TimeSeries-Partner')
foodexports = pd.read_excel("../data/WITS-Partner-Food.xlsx", sheet_name='Product-TimeSeries-Partner')
machineryexports = pd.read_excel("../data/WITS-Partner-MachinerynTransport.xlsx", sheet_name='Product-TimeSeries-Partner')
manufacturesexports = pd.read_excel("../data/WITS-Partner-Manufactures.xlsx", sheet_name='Product-TimeSeries-Partner')

# Making country names consistent with COW data set
# Take note, 'Czechslovakia', 'German Federal Republic', 'Yugoslavia, FR (Serbia/Montenegro)' has not been touched
allexports['Partner Name'] = allexports['Partner Name'].replace({
    'Hong Kong, China': 'Hong Kong',
    'Korea, Dem. Rep.': 'North Korea',
    'Korea, Rep.': 'South Korea',
    'Macao': 'Macau',
    'United Arab Emirates': 'UAE',
})

chemicalexports['Partner Name'] = chemicalexports['Partner Name'].replace({
    'Hong Kong, China': 'Hong Kong',
    'Korea, Dem. Rep.': 'North Korea',
    'Korea, Rep.': 'South Korea',
    'Macao': 'Macau',
    'United Arab Emirates': 'UAE',
})

consumerexports['Partner Name'] = consumerexports['Partner Name'].replace({
    'Hong Kong, China': 'Hong Kong',
    'Korea, Dem. Rep.': 'North Korea',
    'Korea, Rep.': 'South Korea',
    'Macao': 'Macau',
    'United Arab Emirates': 'UAE',
})

foodexports['Partner Name'] = foodexports['Partner Name'].replace({
    'Hong Kong, China': 'Hong Kong',
    'Korea, Dem. Rep.': 'North Korea',
    'Korea, Rep.': 'South Korea',
    'Macao': 'Macau',
    'United Arab Emirates': 'UAE',
})

machineryexports['Partner Name'] = machineryexports['Partner Name'].replace({
    'Hong Kong, China': 'Hong Kong',
    'Korea, Dem. Rep.': 'North Korea',
    'Korea, Rep.': 'South Korea',
    'Macao': 'Macau',
    'United Arab Emirates': 'UAE',
})

manufacturesexports['Partner Name'] = manufacturesexports['Partner Name'].replace({
    'Hong Kong, China': 'Hong Kong',
    'Korea, Dem. Rep.': 'North Korea',
    'Korea, Rep.': 'South Korea',
    'Macao': 'Macau',
    'United Arab Emirates': 'UAE',
})

# Tidy format
allexports = pd.melt(allexports, id_vars=['Reporter Name', 'Partner Name', 'Trade Flow', 'Product Group', 'Indicator'], value_vars=[str(year) for year in range(1989, 2023)], var_name='Year', value_name='Export Value')
chemicalexports = pd.melt(chemicalexports, id_vars=['Reporter Name', 'Partner Name', 'Trade Flow', 'Product Group', 'Indicator'], value_vars=[str(year) for year in range(1989, 2023)], var_name='Year', value_name='Export Value')
consumerexports = pd.melt(consumerexports, id_vars=['Reporter Name', 'Partner Name', 'Trade Flow', 'Product Group', 'Indicator'], value_vars=[str(year) for year in range(1989, 2023)], var_name='Year', value_name='Export Value')
foodexports = pd.melt(foodexports, id_vars=['Reporter Name', 'Partner Name', 'Trade Flow', 'Product Group', 'Indicator'], value_vars=[str(year) for year in range(1989, 2023)], var_name='Year', value_name='Export Value')
machineryexports = pd.melt(machineryexports, id_vars=['Reporter Name', 'Partner Name', 'Trade Flow', 'Product Group', 'Indicator'], value_vars=[str(year) for year in range(1989, 2023)], var_name='Year', value_name='Export Value')
manufacturesexports = pd.melt(manufacturesexports, id_vars=['Reporter Name', 'Partner Name', 'Trade Flow', 'Product Group', 'Indicator'], value_vars=[str(year) for year in range(1989, 2023)], var_name='Year', value_name='Export Value')

