import json
import pandas as pd
import geopandas as gpd
import numpy as np

# Load the CSV file, skipping the first 4 rows
df = pd.read_csv("pop_dense.csv", skiprows=4)

df = df.drop(df.columns[[2, 3,4, 67,68]], axis=1)

df_long = pd.melt(df, id_vars=["Country Name", "Country Code"], var_name="Year", value_name="Population Density")

#pop_dense22 = df[['Country Name', '2022']]

# Load GeoJSON file
geo_data = gpd.read_file("countries.geo.json")

df_long.rename(columns={"Country Name": "name"}, inplace=True)  

df2 = geo_data.merge(df_long, on="name", how="left") 

df2["log_Density"] = np.log1p(df2["Population Density"])  # Apply log transformation



#drop na values
df2 = df2.dropna(subset=['Year'])
df2 = df2.dropna(subset=['Population Density'])

df2["Year"] = df2["Year"].astype(int)  # Ensure Year is numeric

print(df2.head())

df2.to_csv("cleaned_population_density_time.csv", index=False)