import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt  

#dummy dataset for visualization
data = {
    "Year": [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "Trade volumn": [1000, 20000, 3000, 4000, 5000, 6000, 7000]
}

st.title("More visualizations on US")

#button to go back to map
# if st.button("Back to Map"):
#     st.switch_page("Map.py")
