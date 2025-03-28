import pandas as pd

# Importing data
allexports = pd.read_excel("../data/WITS-Partner-All.xlsx", sheet_name='Partner-Timeseries')
chemicalexports = pd.read_excel("../data/WITS-Partner-Chemical.xlsx", sheet_name='Product-TimeSeries-Partner')
consumerexports = pd.read_excel("../data/WITS-Partner-Consumer.xlsx", sheet_name='Product-TimeSeries-Partner')
foodexports = pd.read_excel("../data/WITS-Partner-Food.xlsx", sheet_name='Product-TimeSeries-Partner')
machineryexports = pd.read_excel("../data/WITS-Partner-MachinerynTransport.xlsx", sheet_name='Product-TimeSeries-Partner')
manufacturesexports = pd.read_excel("../data/WITS-Partner-Manufactures.xlsx", sheet_name='Product-TimeSeries-Partner')
cpi = pd.read_excel("../data/cpi.xlsx", skiprows = 11)

# Making country names consistent with COW data set
name_mapping = {
    'Korea, Rep.': 'South Korea',
    'Korea, Dem. Rep.': 'North Korea',
    'Antigua and Barbuda': 'Antigua & Barbuda',
    'Micronesia, Fed. Sts.': 'Federated States of Micronesia',
    'Congo, Dem. Rep.': 'Democratic Republic of the Congo',
    'Kyrgyz Republic': 'Kyrgyzstan',
    'Slovak Republic': 'Slovakia',
    'Russian Federation': 'Russia',
    'Iran, Islamic Rep.': 'Iran',
    'Egypt, Arab Rep.': 'Egypt',
    'Bahamas, The': 'Bahamas',
    'Syrian Arab Republic': 'Syria',
    'Lao PDR': 'Laos',
    'United States': 'United States of America',
}

allexports['Partner Name'] = allexports['Partner Name'].replace(name_mapping)
chemicalexports['Partner Name'] = chemicalexports['Partner Name'].replace(name_mapping)
consumerexports['Partner Name'] = consumerexports['Partner Name'].replace(name_mapping)
foodexports['Partner Name'] = foodexports['Partner Name'].replace(name_mapping)
machineryexports['Partner Name'] = machineryexports['Partner Name'].replace(name_mapping)
manufacturesexports['Partner Name'] = manufacturesexports['Partner Name'].replace(name_mapping)

# Convert from US$ Thousand to US$
def convert_to_usd(df):
    for year in df.columns[5:39]:
        df[year] = df[year] * 1000
    return df

allexports = convert_to_usd(allexports)
chemicalexports = convert_to_usd(chemicalexports)
consumerexports = convert_to_usd(consumerexports)
foodexports = convert_to_usd(foodexports)
machineryexports = convert_to_usd(machineryexports)
manufacturesexports = convert_to_usd(manufacturesexports)

allexports = allexports.drop(columns=['Indicator'])
chemicalexports = chemicalexports.drop(columns=['Indicator'])
consumerexports = consumerexports.drop(columns=['Indicator'])
foodexports = foodexports.drop(columns=['Indicator'])
machineryexports = machineryexports.drop(columns=['Indicator'])
manufacturesexports = manufacturesexports.drop(columns=['Indicator'])

# Adjusting for inflation, base year = 2022
cpi = cpi[['Year', 'Annual']]
cpi['Year'] = cpi['Year'].astype(str)
cpi_dict = dict(zip(cpi['Year'], cpi['Annual']))
base_year_cpi = cpi_dict['2022']

def adjust_for_inflation(df, cpi_dict, base_year_cpi):
    for year in df.columns[5:39]:
        if year in cpi_dict:
            df[year] = df[year] * (base_year_cpi / cpi_dict[year])
    return df


# Tidy format
allexports = pd.melt(allexports, id_vars=['Reporter Name', 'Partner Name'], value_vars=[str(year) for year in range(1989, 2023)], var_name='Year', value_name='Export Value')
chemicalexports = pd.melt(chemicalexports, id_vars=['Reporter Name', 'Partner Name'], value_vars=[str(year) for year in range(1989, 2023)], var_name='Year', value_name='Export Value')
consumerexports = pd.melt(consumerexports, id_vars=['Reporter Name', 'Partner Name'], value_vars=[str(year) for year in range(1989, 2023)], var_name='Year', value_name='Export Value')
foodexports = pd.melt(foodexports, id_vars=['Reporter Name', 'Partner Name'], value_vars=[str(year) for year in range(1989, 2023)], var_name='Year', value_name='Export Value')
machineryexports = pd.melt(machineryexports, id_vars=['Reporter Name', 'Partner Name'], value_vars=[str(year) for year in range(1989, 2023)], var_name='Year', value_name='Export Value')
manufacturesexports = pd.melt(manufacturesexports, id_vars=['Reporter Name', 'Partner Name'], value_vars=[str(year) for year in range(1989, 2023)], var_name='Year', value_name='Export Value')
