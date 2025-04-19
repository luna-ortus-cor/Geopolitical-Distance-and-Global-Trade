# Geopolitical-Distance-and-Global-Trade  
DSE3101 Project  
The main objective of our project is to develop a new measure of geopolitical distance between Singapore and other countries, and to provide export strategy recommendations.
---

## Models  
*(Describe your models here if needed)*  

---

## Key Files and Folders  
- `Frontend/Data/combined_trade_volume.csv`: Export volume of Singapore by product categories.  
- `Frontend/Data/gdi_cleaned.csv`: Geopolitical Distance Index (GDI) data for countries, including regional classifications.  
- `Frontend/Data/updated_ahs_cleaned.csv`: Tariff rates applied to Singaporean exports over time.  
- `Frontend/Code/dashboard.py`: Main script to launch the dashboard.  
- `Backend/data/trade_to_gdp_ratio_clean.csv`: Trade to GDP ratio data
- `Backend/code/geopoliticalmeasure.ipynb`: Code for constructing our geopolitical distance
- `Backend/code/[clean]XXX.ipynb`: Codes for cleaning our data
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
