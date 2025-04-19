# Geopolitical-Distance-and-Global-Trade  
DSE3101 Project  

The main objective of our project is to develop a new measure of geopolitical distance between Singapore and other countries, and to provide export strategy recommendations.

---

## Models  
We implemented a Darts-based time series forecasting approach on a per-country basis (final_forecast_model.ipynb),      enabling country-specific modeling to capture the unique patterns in each trade relationship, considering both          economic factors and geopolitical considerations that impact export dynamics. Some pre-processing was conducted to      ensure data validity by replacing/removing `NaNs`. Cross-validation was also performed using an expanding window        cross-validation framework. Hyperparameters were finetuned using grid search.

## Cross Validation
All metrics were computed at both the country level and in aggregate (mean and median across all countries) to ensure a balanced and nuanced comparison. Across the board, Random Forest consistently achieved the lowest MAPE, MAE, MSE, RMSE, AIC and BIC, demonstrating both strong predictive accuracy and parsimony, and were therefore selected as the preferred model for the final forecast. 
| Metric          | Random Forest     | XGBoost          | LightGBM         |
|-----------------|-------------------|------------------|------------------|
| **MAPE (%)**    | **2.9051**        | 3.0657           | 3.1693           |
| **MAE**         | **0.4738**        | 0.4993           | 0.5170           |
| **MSE**         | **0.5402**        | 0.6284           | 0.6759           |
| **RMSE**        | **0.5985**        | 0.6302           | 0.6577           |
| **AIC**         | **13.7956**       | 14.7270          | 15.5796          |
| **BIC**         | **19.7640**       | 20.6954          | 21.5480          |
---


## Key Files and Folders  
- `Frontend/Data/combined_trade_volume.csv`: Export volume of Singapore by product categories.  
- `Frontend/Data/gdi_cleaned.csv`: Geopolitical Distance Index (GDI) data for countries, including regional classifications.  
- `Frontend/Data/updated_ahs_cleaned.csv`: Tariff rates applied to Singaporean exports over time.  
- `Frontend/Code/dashboard.py`: Main script to launch the dashboard.  
- `Backend/data/trade_to_gdp_ratio_clean.csv`: Trade to GDP ratio data
- `Backend/code/geopoliticalmeasure.ipynb`: Code for constructing our geopolitical distance
- `Backend/code/[clean]XXX.ipynb`: Codes for cleaning our data

```
Geopolitical-Distance-and-Global-Trade/
├── Frontend/
│   ├── Code/
│   │   └── dashboard.py                 # Dash application entry point
│   └── Data/
│       ├── combined_trade_volume.csv   # Export volumes by product
│       ├── gdi_cleaned.csv             # Geopolitical Distance Index
│       ├── updated_ahs_cleaned.csv     # Tariff rates over time
├── Backend/
│   ├── code/
│   │   ├── geopoliticalmeasure.ipynb   # GDI computation
│   │   └── [clean]XXX.ipynb            # Data cleaning scripts
│   └── data/
│       ├── trade_to_gdp_ratio_clean.csv  # Trade-to-GDP ratio data
│       └── recommendations.csv           # Forecasted trade volume
└── README.md
```
---

## Running Our Dashboard Locally  

1. **Clone or download** the repository and set it as your working directory.  

2. Install dependencies:  
   ```bash  
   pip install -r Frontend/Code/requirements.txt  
   ```  

3. Run the dashboard:  
   ```bash  
   python -m Frontend.Code.dashboard  
   ```  

   After running, the terminal will display:  
   ```  
   Dash is running on http://0.0.0.0:8080/  
   * Running on http://127.0.0.1:8080  
   * Running on http://192.168.X.X:8080  
   ```  

4. **Access the dashboard**:  
   - **Local machine**: Use `http://127.0.0.1:8080` in your browser.  
   - **Other devices on the same network**: Use `http://192.168.X.X:8080` (replace `X.X` with the IP shown in your terminal).  

---
