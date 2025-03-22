import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import streamlit as st
from exportdata import allexports, chemicalexports, consumerexports, foodexports, machineryexports, manufacturesexports

def plot_export_volume(dataframe, country):
    filtered_data = dataframe[dataframe['Partner Name'] == country]
    filtered_data.loc[:, 'Year'] = pd.to_datetime(filtered_data['Year'], format='%Y')

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(filtered_data['Year'], filtered_data['Export Value'], marker='o', linestyle='-', color='b')

    ax.set_title(f'Singapore"s Export Volume to {country} Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Export Volume (in US $)')

    formatter = FuncFormatter(lambda x, pos: '{:,.0f}'.format(x))
    ax.yaxis.set_major_formatter(formatter)

    plt.xticks(rotation=45)
    plt.grid(False)
    plt.tight_layout()

    st.pyplot(fig)

sectors = {
    'All Products': allexports,
    'Chemicals': chemicalexports,
    'Consumer goods': consumerexports,
    'Food Products': foodexports,
    'Machinery and Transport Equipment': machineryexports,
    'Manufactures': manufacturesexports
}

st.title("Export Volume Analysis")

sector = st.selectbox("Select Sector", list(sectors.keys()))
df = sectors[sector]

country = st.selectbox("Select Country", df['Partner Name'].unique())

st.write(f"Showing data for Exports to {country} in {sector} sector.")
filtered_data = df[df['Partner Name'] == country][['Year', 'Export Value']]
filtered_data = filtered_data.dropna()
filtered_data = filtered_data.sort_values(by='Year', ascending=False)
filtered_data['Export Value'] = filtered_data['Export Value'].apply(lambda x: f'${x:,.0f}')
st.write("### Export Volume Data (US $)", filtered_data.set_index('Year'))

plot_export_volume(df, country)
