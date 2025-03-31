import pandas as pd

# Load the datasets
df = pd.read_csv("cleaned_population_density_time.csv")  # Original dataset
gdp_df = pd.read_csv("API_NY.GDP.MKTP.CD_DS2_en_csv_v2_26433.csv", skiprows= 4)  # GDP dataset

#remove unnecessary columns from the GDP dataset
gdp_df = gdp_df.drop(columns=["Indicator Name", "Indicator Code"])

# Reshape from wide to long format
gdp_df_long = gdp_df.melt(id_vars=["Country Name", "Country Code"], 
                          var_name="Year", 
                          value_name="GDP")



# Convert the Year column to integer type while ignoring nan values
gdp_df_long["Year"] = pd.to_numeric(gdp_df_long["Year"], errors='coerce')

merged_df = df.merge(gdp_df_long, left_on=["Country Code", "Year"], right_on=["Country Code", "Year"], how="left")


# extract as excel file
merged_df.to_csv("merged_population_density_gdp.csv", index=False)

