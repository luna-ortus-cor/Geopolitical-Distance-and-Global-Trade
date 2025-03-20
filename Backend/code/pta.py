import pandas as pd

# importing data, using sheet: WTO+ LE 
pta = pd.read_excel("../data/DTA 1.0 - Horizontal Content (v2).xlsx", sheet_name = "WTO+ LE")

# filter for Singapore-related PTAs only
ptasg = pta[pta["Agreement"].str.contains("|".join(["Singapore", "ASEAN", "RCEP", "Trans-Pacific Strategic Economic Partnership", "CPTPP"]), case=False, na=False)]

# expand data to bilateral observations, where Singapore will always be Country 1
asean_countries = ["Brunei", "Cambodia", "Indonesia", "Laos", "Malaysia", "Myanmar", "Philippines", "Thailand", "Vietnam"]
efta_countries = ["Iceland", "Liechtenstein", "Norway", "Switzerland"]
rcep_countries = ["Australia", "Brunei", "Cambodia", "China", "Indonesia", "Japan", "Laos", "Malaysia", "Myanmar", "New Zealand", "Philippines", "South Korea", "Thailand", "Vietnam"]
gcc_countries = ["Bahrain","Kuwait","Oman","Qatar","Saudi Arabia","United Arab Emirates"]
eu_countries = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic","Denmark", "Estonia", "Finland", "France", "Germany", "Greece","Hungary", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg","Malta", "Netherlands", "Poland", "Portugal", "Romania", "Slovakia","Slovenia", "Spain", "Sweden"]
cptpp_countries = ["Australia", "Brunei", "Canada", "Chile", "Japan", "Malaysia", "Mexico", "New Zealand", "Peru", "Vietnam"]
tpsec_countries = ["Brunei", "Chile", "New Zealand"]

def expand_agreement(row):
    agreement = row["Agreement"]
    countries_involved = agreement.split(" - ")
    new_rows = []
    expanded_countries = []
    
    special_keywords = {
        "ASEAN": asean_countries,
        "EFTA": efta_countries,
        "GCC": gcc_countries,
        "RCEP": rcep_countries,
        "EU": eu_countries,
        "CPTPP": cptpp_countries,
        "Trans-Pacific Strategic Economic Partnership": tpsec_countries
    }
    
    for country in countries_involved:
        country = country.strip()
        found = False
        
        for keyword, member_list in special_keywords.items():
            if keyword in country:
                expanded_countries.extend(member_list)
                found = True
                break
        
        if not found and country != "Singapore":
            expanded_countries.append(country)
    
    for country2 in expanded_countries:
        new_row = row.copy()
        new_row["Country 1"] = "Singapore"
        new_row["Country 2"] = country2
        new_rows.append(new_row)
    
    return new_rows

expanded_rows = []
for _, row in ptasg.iterrows():
    expanded_rows.extend(expand_agreement(row))

ptasg_expanded = pd.DataFrame(expanded_rows)


# Housekeeping, following country names given in COW country codes.csv
ptasg_expanded = ptasg_expanded[~ptasg_expanded['Country 2'].str.contains("1992")]
ptasg_expanded['Country 2'] = ptasg_expanded['Country 2'].replace({"Chinese Taipei": "Taiwan", "Türkiye": "Turkey", "Korea, Republic of": "South Korea", "Hong Kong, China": "Hong Kong"})

#print(ptasg_expanded.head())

# Before deciding which variable to use, consider how we going to use it also, for example, do we take the HIGHEST value of FTAIndustrial for duplicated rows, or take the mean/median or what?

