# the gravity data used here comes from gravity2.py, arms and idealpointestimates are excluded

import pandas as pd
from exportdata import allexports
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


# Importing data
gravity = pd.read_csv("../data/Gravity_Adjusted.csv")

gravity_clean = gravity[gravity['country_exists_d'] == 1]
gravity_clean = gravity_clean.dropna(subset=['adjustedexport'])
print(gravity_clean)


############################################
# Feature ranking with RandomForestRegressor

# Train test split
columns_to_include = [
    'distw_harmonic_jh', 'dist', 'diplo_disagreement', 'scaled_sci_2021',
    'comlang_ethno', 'comcol', 'col_dep_ever', 'sibling_ever', 'gdp_d', 'gdp_ppp_d',
    'pop_pwt_d', 'wto_o', 'wto_d', 'gatt_o', 'gatt_d',
    'fta_wto', 'entry_cost_d', 'entry_tp_d', 'contig', 'comrelig'
]

X = gravity_clean[columns_to_include]
y = gravity_clean['adjustedexport']
columns_name = X.columns

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# KNN Imputer
from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors = 5)

X_train = imputer.fit_transform(X_train)
X_train = pd.DataFrame(X_train, columns = columns_name)

X_test = imputer.transform(X_test)
X_test = pd.DataFrame(X_test, columns = columns_name)

forest = RandomForestRegressor(n_estimators=100, random_state=42)
forest.fit(X_train, y_train)
importances = forest.feature_importances_

# Create a DataFrame with feature names and importances, sorted by importance in descending order
X = pd.DataFrame(X, columns = gravity_clean.columns)
feature_importance_df = pd.DataFrame({'Feature': X_train.columns, 'Importance': importances})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

# Plot the feature importances
fig, ax = plt.subplots()
feature_importance_df.plot.bar(x='Feature', y='Importance', ax=ax)
ax.set_title("Feature Importance")
ax.set_ylabel("Importance")
ax.set_xticklabels(feature_importance_df['Feature'], rotation=45, ha='right')
fig.tight_layout()

plt.show()


############################################
# Feature ranking with PCA

# Step 1: Standardize the data (Important for PCA)
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 2: Apply PCA
from sklearn.decomposition import PCA

# Initialize PCA and fit it to the standardized data
pca = PCA(n_components=X_train_scaled.shape[1])  # All components (number of features)
pca.fit(X_train_scaled)

# Step 3: Analyze the explained variance of each component
explained_variance = pca.explained_variance_ratio_
print(f"Explained Variance of Each Principal Component:\n{explained_variance}")

# Step 4: Look at the loadings (coefficients) of each feature in the components
# Loadings represent the contribution of each feature to each principal component
loadings = pca.components_

# Create a DataFrame for loadings
loadings_df = pd.DataFrame(loadings.T, columns=[f"PC{i+1}" for i in range(loadings.shape[0])], index=columns_name)

# Step 5: Rank features based on their contributions to the principal components
# We calculate the absolute value of each feature's contribution to all principal components and sum them
feature_importance_pca = loadings_df.abs().sum(axis=1).sort_values(ascending=False)

# Display feature importance based on PCA
print(f"\nFeature Importance Based on PCA (Ranked):\n{feature_importance_pca}")

# Step 6: Visualize the Feature Importance Based on PCA
import matplotlib.pyplot as plt

# Plot the feature importance
fig, ax = plt.subplots(figsize=(10, 6))
feature_importance_pca.plot.bar(ax=ax)
ax.set_title("Feature Importance Based on PCA")
ax.set_ylabel("Importance")
ax.set_xticklabels(feature_importance_pca.index, rotation=45, ha='right')
fig.tight_layout()

plt.show()
