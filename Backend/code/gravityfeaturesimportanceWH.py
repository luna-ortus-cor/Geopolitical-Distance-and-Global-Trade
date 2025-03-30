import pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

# Importing
gravityfinal = pd.read_csv("../data/gravityarmsideal.csv")

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
