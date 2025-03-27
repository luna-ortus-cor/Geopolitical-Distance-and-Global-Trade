import pandas as pd

# Importing data
sgrecipient = pd.read_csv("../data/trade-register-sg-recipient.csv", header = 10, encoding= "ISO-8859-1")
sgsupplier = pd.read_csv("../data/trade-register-sg-supplier.csv", header = 10, encoding= "ISO-8859-1")

# Removing empty columns
sgrecipient = sgrecipient.drop(sgrecipient.columns[[3, 5, 9]], axis=1)
sgsupplier = sgsupplier.drop(sgsupplier.columns[[3, 5, 9]], axis=1)

# No missing values for key variables

# Renaming and keeping relevant columns only
# Variables of interest:  Recipient, Supplier, Year of order, SIPRI TIV for total order
# Why Year/SIPRI TIV of order instead of Year/SIPRI TIV of delivery:
# Captures strategic partnerships and economic alignment before trade flow
sgrecipient.rename(columns = {"Recipient":"recipient", "Supplier":"supplier", "Year of order":"year", "SIPRI TIV for total order":"value"}, inplace = True)
sgrecipient = sgrecipient.iloc[:, [0, 1, 2, 11]]

sgsupplier.rename(columns = {"Recipient":"recipient", "Supplier":"supplier", "Year of order":"year", "SIPRI TIV for total order":"value"}, inplace = True)
sgsupplier = sgsupplier.iloc[:, [0, 1, 2, 11]]

# Standardising country name
sgrecipient['supplier'] = sgrecipient['supplier'].replace('United States', 'United States of America')
sgsupplier['recipient'] = sgsupplier['recipient'].replace({
    'United States': 'United States of America',
    'UAE': 'United Arab Emirates'
})

# Arms intensity: sum up both exports/imports of military arms
armsintensity = pd.merge(
    sgsupplier.rename(columns={'supplier': 'country1', 'recipient': 'country2', 'value': 'supplied'}), 
    sgrecipient.rename(columns={'supplier': 'country2', 'recipient': 'country1', 'value': 'received'}), 
    how='outer', 
    left_on=['country1', 'country2', 'year'], 
    right_on=['country1', 'country2', 'year']
)
armsintensity['total'] = armsintensity['supplied'].fillna(0) + armsintensity['received'].fillna(0)
