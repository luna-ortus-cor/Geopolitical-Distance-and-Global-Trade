import json
import pandas as pd
import geopandas as gpd
import numpy as np
import pycountry_convert as pc

df = pd.read_csv('Backend/data/finaldataset.csv')

#selecting the columns we need
df = df[['country_d','year', 'country_id_d' , 
        'geodistance']] 


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
df.rename(columns={"country_d": "Name", "year": "Year", 
                   'geodistance': 'GDI'}, inplace=True)

# Convert the 'Year' column to numeric and sort the dataframe by 'Year'
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
df = df.sort_values("Year").reset_index(drop=True)

df.to_csv('Frontend/data/gdi_cleaned.csv', index=False)









