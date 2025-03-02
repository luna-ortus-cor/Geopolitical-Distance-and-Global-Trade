import json
import pandas as pd
import geopandas as gpd

# Load the CSV file, skipping the first 4 rows
df = pd.read_csv("pop_dense.csv", skiprows=4)
pop_dense22 = df[['Country Name', '2022']]

# Load GeoJSON file
geo_data = gpd.read_file("countries.geo.json")

pop_dense22.rename(columns={"Country Name": "name", "2022": "population_density"}, inplace=True)  

df2 = geo_data.merge(pop_dense22, on="name", how="left") 



df2.to_file("world_population_density.geojson", driver="GeoJSON")
