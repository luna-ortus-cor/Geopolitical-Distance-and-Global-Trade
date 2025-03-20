import pandas as pd

sgrecipient = pd.read_csv("../data/trade-register-sg-recipient.csv", header = 10, encoding= "ISO-8859-1")
sgsupplier = pd.read_csv("../data/trade-register-sg-supplier.csv", header = 10, encoding= "ISO-8859-1")

# Removing empty columns
sgrecipient = sgrecipient.drop(sgrecipient.columns[[3, 5, 9]], axis=1)
sgsupplier = sgsupplier.drop(sgsupplier.columns[[3, 5, 9]], axis=1)

# No missing values for key variables

# Renaming and keeping relevant columns only
sgrecipient.rename(columns = {"Recipient":"recipient", "Supplier":"supplier", "Year of order":"year", "SIPRI TIV for total order":"value"}, inplace = True)
sgrecipient = sgrecipient.iloc[:, [0, 1, 2, 11]]

sgsupplier.rename(columns = {"Recipient":"recipient", "Supplier":"supplier", "Year of order":"year", "SIPRI TIV for total order":"value"}, inplace = True)
sgsupplier = sgsupplier.iloc[:, [0, 1, 2, 11]]

#print(sgsupplier.head())

# Variables of interest:  Recipient, Supplier, Year of order, SIPRI TIV for total order

# Why Year/SIPRI TIV of order instead of Year/SIPRI TIV of delivery:
# Captures strategic partnerships and economic alignment before trade flow
