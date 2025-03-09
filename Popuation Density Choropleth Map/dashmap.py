import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np

# Load cleaned data
df = pd.read_csv("cleaned_population_density.csv")
print(df.head())
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
    projection="natural earth",
    custom_data=["Country Name", "Indicator Name", "2022"]  # Adding additional data
)

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("World Population Density Choropleth"),
    
    # Create a Plotly graph
    dcc.Graph(
        id='choropleth-map',
        figure=fig
    ),
    
    # Placeholder for the detailed country info
    html.Div(id='country-info')
])

# Callback to update the country info when a country is clicked
@app.callback(
    dash.dependencies.Output('country-info', 'children'),
    [dash.dependencies.Input('choropleth-map', 'clickData')]
)
def display_country_info(clickData):
    if clickData is None:
        return "Click on a country to see more information."
    
    # Extract country data from clickData
    clicked_country = clickData['points'][0]['location']
    country_info = df[df["Country Code"] == clicked_country].iloc[0]
    
    # Display detailed information for the selected country
    country_description = f"""
    **Country Name**: {country_info['Country Name']}<br>
    **Indicator Name**: {country_info['Indicator Name']}<br>
    **Population Density (2022)**: {country_info['2022']}<br>
    **Log Population Density (2022)**: {country_info['log_2022']}<br>
    """
    
    # You can add more detailed information here (replace the following placeholder)
    additional_description = """
    More detailed information about the country can be added here. 
    For example, you could include economic data, geographical features, and more.
    """
    
    return html.Div([html.Div([country_description]), html.Div([additional_description])])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
