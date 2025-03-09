import streamlit as st
import plotly.express as px
import pandas as pd

# Load cleaned data
df = pd.read_csv("cleaned_population_density.csv")

import numpy as np

# Apply log transformation (log(1+x) to handle zero values)
df["log_2022"] = np.log1p(df["2022"])  # log1p = log(1 + x) to avoid log(0)

# Create choropleth map using the log-transformed values
fig = px.choropleth(
    df,
    locations="Country Code",
    color="log_2022",  # Use log-transformed values
    hover_name="Country Name",
    color_continuous_scale="YlGnBu",
    range_color=[df["log_2022"].min(), df["log_2022"].max()],
    projection="natural earth"
)

st.title("World Population Density Choropleth")
st.plotly_chart(fig)

# Dropdown for selecting country
country_options = df['Country Name'].unique()
selected_country = st.selectbox('Select a country', country_options)

# Display information based on the selected country
if selected_country:
    country_info = df[df['Country Name'] == selected_country].iloc[0]
    
    # Display country details
    country_description = f"""
    **Country Name**: {country_info['Country Name']}<br>
    **last year**: {country_info['2020']}<br>
    **Population Density (2022)**: {country_info['2022']}<br>
    **Log Population Density (2022)**: {country_info['log_2022']}<br>
    """
    
    additional_description = """
    More detailed information about the country can be added here.
    For example, you could include economic data, geographical features, and more.
    """
    
    st.markdown(country_description, unsafe_allow_html=True)
    st.markdown(additional_description)



