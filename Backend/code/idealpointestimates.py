import pandas as pd

# Importing
countryCodes = pd.read_csv("../data/COW country codes.csv") # Checked, 0 missing value
agreementScores = pd.read_csv("../data/AgreementScoresAll_Jun2024.csv")

# Adding in country names to data
agreementScoresMerged = pd.merge(agreementScores, countryCodes, left_on = "ccode1", right_on = "CCode", how = "inner")
agreementScoresMerged = agreementScoresMerged.drop(columns = ["CCode"])
agreementScoresMerged.rename(columns = {"StateAbb":"StateAbb1", "StateNme":"StateName1"}, inplace = True)

agreementScoresMerged = pd.merge(agreementScoresMerged, countryCodes, left_on = "ccode2", right_on = "CCode", how = "inner")
agreementScoresMerged = agreementScoresMerged.drop(columns = ["CCode"])
agreementScoresMerged.rename(columns = {"StateAbb":"StateAbb2", "StateNme":"StateName2"}, inplace = True)

# Filtering for data relevant only to Singapore
agreementScoresMerged = agreementScoresMerged[(agreementScoresMerged["StateName1"] == "Singapore") | (agreementScoresMerged["StateName2"] == "Singapore")]

# Removing duplicate entries. Checked that no ('ccode1', 'ccode2', 'year') combination have different IdealPointDistance
agreementScoresMerged.drop_duplicates(
    subset=['ccode1', 'ccode2', 'year', 'IdealPointDistance'],
    inplace=True
)

# Removing duplicate symmetric rows - (ccode1, ccode2) and (ccode2, ccode1)
agreementScoresMerged['sorted_pair'] = agreementScoresMerged.apply(
    lambda row: tuple(sorted([row['ccode1'], row['ccode2']])), axis=1
)
agreementScoresMerged = agreementScoresMerged.drop_duplicates(subset=['sorted_pair', 'IdealPointDistance', 'year', 'session.x'])
agreementScoresMerged = agreementScoresMerged.drop(columns=['sorted_pair'])

# Making ccode1 and StateName1 always refer to Singapore
def ensure_singapore_first(row):
    if row['StateName1'] != "Singapore":
        # Swap values
        row['ccode1'], row['ccode2'] = row['ccode2'], row['ccode1']
        row['StateName1'], row['StateName2'] = row['StateName2'], row['StateName1']
    return row

agreementScoresMerged = agreementScoresMerged.apply(ensure_singapore_first, axis=1)

# Keeping only relevant columns
agreementScoresMerged = agreementScoresMerged[['StateName1', 'StateName2', 'year', 'IdealPointDistance']]

agreementScoresMerged.to_csv("../data/AgreementScoresMerged.csv", index=False)
