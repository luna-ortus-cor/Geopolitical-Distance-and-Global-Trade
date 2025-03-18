from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv("cleaned_population_density_time.csv")

app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H4('Animated Population Density Over Time'),
    
    # Choropleth map
    dcc.Loading(dcc.Graph(id="choropleth-map"), type="cube"),
    
    # Country info display
    html.Div(id="country-info", style={"margin-top": "20px", "font-weight": "bold"})
])


# Callback to update the choropleth map
@app.callback(
    Output("choropleth-map", "figure"),
    Input("choropleth-map", "id")  # Dummy input to trigger the function
)
def update_map(_):
    fig = px.choropleth(
        df,
        locations="Country Code",
        color="log_Density",
        hover_name="name",
        animation_frame="Year",  # Enables animation
        color_continuous_scale="Plasma",  # More distinct colors
        projection="natural earth",
        range_color=[df["log_Density"].quantile(0.05), df["log_Density"].quantile(0.95)]  # Avoid extreme outliers
    )
    return fig


# Callback to display country info when clicked
@app.callback(
    Output("country-info", "children"),
    Input("choropleth-map", "clickData")
)
def display_country_info(clickData):
    if clickData is None:
        return "Click on a country to see details."
    
    clicked_country = clickData["points"][0]["location"]
    country_info = df[df["Country Code"] == clicked_country].iloc[0]

    return f"Country: {country_info['name']} (Code: {clicked_country})"


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
