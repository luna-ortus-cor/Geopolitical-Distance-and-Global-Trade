import pandas as pd
from exportdata import allexports

# Importing data
gravity = pd.read_csv("../data/Gravity_V202211.csv", dtype={"col_dep_end_conflict": str}, low_memory=False)
countries = pd.read_csv("../data/Countries_V202211.csv")

countries = countries[['iso3', 'country']]

# Filtering variables of interest only
columns_to_select = ['year', 'iso3num_o', 'iso3_o', 'iso3num_d', 'iso3_d', 'distcap', 'diplo_disagreement', 'contig', 
                     'comlang_off', 'comlang_ethno', 'comrelig', 'gdpcap_o', 'gdpcap_d', 'fta_wto']
gravity2 = gravity[columns_to_select]

# Filtering for data and country
gravity3 = gravity2[(gravity2['year'] >= 1989) & 
                    (gravity2['iso3_d'] == 'SGP') & 
                    ~(gravity2['iso3_o'] == 'SGP') ]

# Adding in country names
gravity4 = gravity3.merge(countries, left_on='iso3_o', right_on='iso3', how='left')
gravityfinal = gravity4.drop(columns=['iso3']).rename(columns={'country': 'country_o'})

gravityfinal.to_csv("../data/gravity_all.csv", index=False)

#### Variables (delete this after you have used the data):
# dist: Geodesic distance between most populated cities (km) (bilateral)
# diplo_disagreement:  UN diplomatic disagreement score (bilateral)
# contig: Dummy equal to 1 if countries are contiguous (bilateral)
# comlang_off: 1 if countries share common official or primary language (bilateral)
# comlang_ethno: 1 if countries share a common language spoken by at least 9% of the population (bilateral)
# comrelig: Religious proximity index (bilateral)
# fta_wto: 1 if pair currently engaged in a regional trade agreement (source: WTO supplemented by Thierry Mayer)
