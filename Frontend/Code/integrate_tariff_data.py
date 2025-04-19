import pandas as pd

# Load the AHS Weighted Average (%) dataset
ahs_raw = pd.read_csv("Frontend/Data/wits_tariff.csv")

# Step 1: Keep only the relevant columns — 'Partner Name' and years
columns_to_keep = ['Partner Name'] + [str(year) for year in range(1989, 2023)]
ahs_cleaned = ahs_raw[columns_to_keep]

# Step 2: Reshape from wide to long format
ahs_long = ahs_cleaned.melt(
    id_vars='Partner Name',
    var_name='Year',
    value_name='AHS Weighted Average (%)'
)

# Step 3: Rename columns for consistency
ahs_long = ahs_long.rename(columns={'Partner Name': 'Country'})

# Step 4: Convert year to integer and tariff values to float
ahs_long['Year'] = ahs_long['Year'].astype(int)
ahs_long['AHS Weighted Average (%)'] = pd.to_numeric(ahs_long['AHS Weighted Average (%)'], errors='coerce')

# Step 5 : Filter out rows with no data with the value "No data"
ahs_long["AHS Weighted Average (%)"] = ahs_long["AHS Weighted Average (%)"].fillna("No Data")

# Final result: cleaned long-format DataFrame
ahs_long.to_csv("Frontend/Data/updated_ahs_cleaned.csv", index=False)