import pandas as pd
import statsmodels.api as sm
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from idealpointestimates import agreementScoresMerged as ideal_point_estimates
from exportdata import allexports

ideal_point_estimates = ideal_point_estimates[['StateName1', 'StateName2', 'year', 'IdealPointDistance']]
allexports['Year'] = allexports['Year'].astype(int)

df = ideal_point_estimates.merge(
    allexports[['Reporter Name', 'Partner Name', 'Year', 'Export Value']], 
    left_on=['StateName1', 'StateName2', 'year'], 
    right_on=['Reporter Name', 'Partner Name', 'Year'], 
    how='left'
)

df = df[df['year'] >= 1989]
df = df[['StateName1', 'StateName2', 'year', 'IdealPointDistance', 'Export Value']]
df = df.dropna()

# Split 75-25, was thinking to split earlier years into train/later years into test
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
train_size = int(0.75 * len(df))
train_df = df[:train_size]
test_df = df[train_size:]

train_df.loc[:, 'Log_ExportValue'] = np.log(train_df['Export Value'])
test_df.loc[:, 'Log_ExportValue'] = np.log(test_df['Export Value'])

X_train = train_df[['IdealPointDistance']]
X_train = sm.add_constant(X_train)
y_train = train_df['Log_ExportValue']

model = sm.OLS(y_train, X_train).fit()

X_test = test_df[['IdealPointDistance']]
X_test = sm.add_constant(X_test)
y_test = test_df['Log_ExportValue']

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse}") # 2.648335288833558
print(f"R^2 Score: {r2}") # 0.08745929204191205

# horrible results, don't use linear reg
