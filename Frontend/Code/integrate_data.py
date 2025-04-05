import json
import pandas as pd
import geopandas as gpd
import numpy as np
import pycountry_convert as pc

df = pd.read_csv('Backend/data/gdi.csv')

#selecting the columns we need
df = df[['StateName2','year', 'country_id_d' , 
         'gdp_d', 'tgdp_ratio_d', 'linear_gdi']]  #consider selecting pop_o which is population in million


# Helper Function to add region (continent) column
def get_continent_from_code(country_code):
    try:
        #convert the country code to alpha2
        alpha2 = pc.country_name_to_country_alpha2(country_code)
        continent_code = pc.country_alpha2_to_continent_code(alpha2)
        continent_names = {
            "AF": "Africa",
            "AS": "Asia",
            "EU": "Europe",
            "NA": "North America",
            "SA": "South America",
            "OC": "Oceania"
        }
        return continent_names.get(continent_code, "Other")
    except:
        return "Other"
    
# Add the region (continent) column based on the 3-letter country code
df['region'] = df['country_id_d'].apply(get_continent_from_code)

# Rename columns for clarity 
df.rename(columns={"StateName2": "Name", "year": "Year", 
                   "gdp_d": "GDP", "tgdp_ratio_d": "tgdp_ratio",
                   'linear_gdi': 'GDI'}, inplace=True)

# Convert the 'Year' column to numeric and sort the dataframe by 'Year'
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
df = df.sort_values("Year").reset_index(drop=True)

print(df["Year"].dtype)

# save the dataframe to a csv file
#df.to_csv('Frontend/data/gdi_cleaned.csv', index=False)









