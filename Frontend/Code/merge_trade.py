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
        # Extract the good type from the file name 
        good_type = os.path.basename(file).replace('.xlsx', '')
        
        # Add a new column for the good type
        df['Good_Type'] = good_type
        
        # Append the dataframe to the list
        dfs.append(df)
    else:
        print(f"Warning: The second sheet in {file} is empty.")

# If any DataFrames were added to the list, concatenate them
if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Save the combined dataframe to a new Excel file
    combined_df.to_excel('Frontend/Data/WITS Trade Volume/combined_data.xlsx', index=False)
    
    print("Files combined successfully!")
else:
    print("No valid files to combine.")
