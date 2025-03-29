import pandas as pd
from sipri import armsintensity
from idealpointestimates import agreementScoresMerged
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

print("Takes at least 1 minute to run btw")

# Importing
gravity = pd.read_csv("../data/Gravity_V202211.csv", dtype={'empire': 'str'})
countries = pd.read_csv("../data/Countries_V202211.csv")
cpi = pd.read_excel("../data/cpi.xlsx", skiprows = 11)
cpi = cpi[['Year', 'Annual']]

# Filter for SG exports only
gravity = gravity[gravity['country_id_o'] == 'SGP']

# Add country names
gravity2 = gravity.merge(countries[['country_id', 'country']], 
                        left_on='country_id_o', right_on='country_id', 
                        how='left').rename(columns={'country': 'country_o'}).drop('country_id', axis=1)
gravity2 = gravity2.merge(countries[['country_id', 'country']], 
                        left_on='country_id_d', right_on='country_id', 
                        how='left').rename(columns={'country': 'country_d'}).drop('country_id', axis=1)

# Filter for years with observations
gravity3 = gravity2[(gravity2['year'] >= 1965) & (gravity2['year'] <= 2020)]

# Convert export values from US $ Thousand to US $
gravity3['tradeflow_comtrade_o'] = gravity3['tradeflow_comtrade_o'] * 1000

# Adjust for inflation using 2020 as base year
gravity4 = gravity3.merge(cpi, left_on='year', right_on='Year', how='left').drop('Year', axis=1)
base_year = 2020
base_cpi = cpi.loc[cpi['Year'] == base_year, 'Annual'].values[0]
gravity4['adjustedexport'] = gravity4['tradeflow_comtrade_o'] * (base_cpi / gravity4['Annual'])

# Add in SIPRI Arms dataset
gravity5 = gravity4.merge(armsintensity, left_on=['country_d', 'year'], right_on=['country2', 'year'], how='left')
gravity5 = gravity5.rename(columns={'total': 'armsintensity'})
gravity5 = gravity5.drop(['Annual', 'country2', 'country1'], axis=1)

# Add in IdealPointDistance dataset (note that a few countries are omitted for now)
gravity6 = gravity5.merge(agreementScoresMerged, left_on=['country_d', 'year'], right_on=['StateName2', 'year'], how='left')
gravity6 = gravity6.drop(['StateName1', 'StateName2'], axis=1)

# Dropping irrelevant columns (including diplo_disagreement and extra values from other sources)
# You may want to keep values like 'entry_cost_d', 'entry_proc_d', 'entry_time_d'
columns_to_drop = [
    'country_exists_o', 'country_exists_d', 'gmt_offset_2020_o', 'gmt_offset_2020_d',
    'main_city_source_o', 'main_city_source_d', 'legal_old_o', 'legal_old_d', 'legal_new_o',
    'legal_new_d', 'transition_legalchange', 'col_dep_end_year', 'empire', 'sever_year',
    'sib_conflict', 'pop_source_o', 'pop_source_d', 'gdp_source_o', 'gdp_source_d', 'pop_pwt_o',
    'pop_pwt_d', 'gdp_ppp_pwt_o', 'gdp_ppp_pwt_d', 'gatt_o', 'wto_o', 'eu_o', 'fta_wto_raw',
    'rta_coverage', 'rta_type', 'entry_cost_o', 'entry_cost_d', 'entry_proc_o', 'entry_proc_d',
    'entry_time_o', 'entry_time_d', 'entry_tp_o', 'entry_tp_d', 'tradeflow_baci',
    'manuf_tradeflow_baci', 'tradeflow_imf_o', 'tradeflow_imf_d', 'diplo_disagreement', 'col_dep_end_conflict'
]
gravity7 = gravity6.drop(columns_to_drop, axis = 1)

# Accounting for NA/NaN values (might be bad to drop NA adjustedexport values as it consists of no exports too)
gravityfinal = gravity7.dropna(subset=['IdealPointDistance', 'pop_d', 'gdp_d', 'comrelig', 'adjustedexport'])
gravityfinal.loc[:, 'armsintensity'] = gravityfinal['armsintensity'].fillna(0)
gravityfinal.loc[:, 'fta_wto'] = gravityfinal['fta_wto'].fillna(0)
gravityfinal.loc[:, 'comlang_off'] = gravityfinal['comlang_off'].fillna(0)

###########################################
# Feature Ranking
###########################################
# Lasso Regression
lasso_columns_to_drop = [
    'year', 'country_id_o', 'country_id_d', 'iso3_o', 'iso3_d', 'iso3num_o', 'iso3num_d',
    'distw_harmonic', 'distw_arithmetic', 'distw_harmonic_jh', 'distw_arithmetic_jh', 'dist',
    'scaled_sci_2021', 'comlang_ethno', 'comcol', 'comleg_pretrans', 'comleg_posttrans',
    'heg_o', 'heg_d', 'col45', 'col_dep', 'sibling_ever', 'sibling', 'pop_o', 'gdpcap_o',
    'gdpcap_d', 'gdp_o', 'gdpcap_ppp_o', 'gdpcap_ppp_d', 'gdp_ppp_o', 'gdp_ppp_d', 
    'tradeflow_comtrade_o', 'tradeflow_comtrade_d', 'country_o', 'country_d', 
    'adjustedexport', 'supplied', 'received'
]
lassoX = gravityfinal.drop(lasso_columns_to_drop, axis = 1)
scaler = StandardScaler()
lassoXscaled = scaler.fit_transform(lassoX)
lassoY = gravityfinal['adjustedexport']

lassoModel = LassoCV().fit(lassoXscaled, lassoY)
lassoImportance = pd.Series(lassoModel.coef_, index=lassoX.columns)
print("=== Feature Importance using Lasso Regression (Absolute Values) ===")
print(lassoImportance.abs().sort_values(ascending=False))

# Random Forest
rf_columns_to_drop = [
    'year', 'country_id_o', 'country_id_d', 'iso3_o', 'iso3_d', 'iso3num_o', 'iso3num_d',
    'scaled_sci_2021', 'tradeflow_comtrade_o', 'tradeflow_comtrade_d', 
    'country_o', 'country_d', 'adjustedexport'
]
rfX = gravityfinal.drop(rf_columns_to_drop, axis = 1)
rfY = gravityfinal['adjustedexport']

rfModel = RandomForestRegressor().fit(rfX, rfY)
rfImportance = pd.Series(rfModel.feature_importances_, index=rfX.columns)
print("=== Feature Importance using Random Forest ===")
print(rfImportance.sort_values(ascending=False))
