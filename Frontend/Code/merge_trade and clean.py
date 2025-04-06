import pandas as pd
import glob
import os

#Get files
files = glob.glob('Frontend/Data/WITS Trade Volume/*.xlsx'  )

dfs = []

# Read each file and append to df
for file in files:
    print(f"Reading file: {file}")
    
    # Read second sheet
    df = pd.read_excel(file, sheet_name=1)
    
    # If the data is not empty, process 
    if not df.empty:
        # Append the dataframe to the list
        dfs.append(df)
    else:
        print(f"Warning: The second sheet in {file} is empty.")


combined_df = pd.concat(dfs, ignore_index=True)

#Replace some of the country names that mismatch main df
replacements = {
    "Syrian Arab Republic": "Syria",
    "United States": "United States of America",
    "Yugoslavia,FR(Serbia/Montenegr": "Yugoslavia",
    "Egypt, Arab Rep.": "Egypt",
    "Iran, Islamic Rep.": "Iran",
    "Lao PDR": "Laos",
    "Gambia, The": "Gambia",
    "Bahamas, The": "Bahamas",
    "Korea, Dem. Rep.": "North Korea",
    "Korea, Rep.": "South Korea",
    "Russian Federation": "Russia",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Ethiopia(excludes Eritrea)": "Ethiopia"
}

combined_df['Partner Name'] = combined_df['Partner Name'].replace(replacements)

#rename columns to match main df
combined_df.rename(columns={'Partner Name': 'Country',}, inplace=True)

#remove unused columns
combined_df.drop(columns=['Reporter Name', 'Trade Flow', 'Indicator'], inplace=True)

#pivot longer to extract year from column names
combined_df = combined_df.melt(id_vars=['Country','Product Group'], var_name='Year', value_name='Export by SG Volume')

#convert export volume to numeric
combined_df['Export by SG Volume'] = pd.to_numeric(combined_df['Export by SG Volume'], errors='coerce')

#save the combined dataframe to a new Excel file
combined_df.to_csv('Frontend/Data/combined_trade_volume.csv', index=False)

