from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv("cleaned_population_density_time.csv")

app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H2('Animated Population Density Over Time', style={"textAlign":"center"}),
    #country dropdown
    dcc.Dropdown(
                id="dropdown",
                placeholder="Select a Country",
                options=["World"]+[country for country in df["name"].unique()],
                style={
                    "width": "250px", 
                    "height": "30px",
                    "display": "block", 
                    "padding": "3px",
                    "borderRadius": "5px",
                    "border": "1px solid #ccc",
                    "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)",
                    "fontSize": "15px"},
                multi=True
                ),    

    # Choropleth map
    dcc.Loading(dcc.Graph(id="choropleth-map"), type="cube"),
    
    # Country info display
    html.Div(id="country-info", style={"margin-top": "20px", "font-weight": "bold"})
])

# Callback to update the choropleth map
@app.callback(
    Output("choropleth-map", "figure"),
    Input("dropdown", "value")  # Dummy input to trigger the function
)
def update_map(selected_countries):
    if not selected_countries or "World" in selected_countries: #show world map by default
        filtered_df=df 
    else:
        if isinstance(selected_countries, str):
            selected_countries=[selected_countries]
        filtered_df=df[df["name"].isin(selected_countries)] #if select a country show animation for this country only
    fig = px.choropleth(
        filtered_df,
        locations="Country Code",
        color="log_Density",
        hover_name="name",
        animation_frame="Year",  # Enables animation
        color_continuous_scale="Plasma",  # More distinct colors
        projection="natural earth",
        range_color=[df["log_Density"].quantile(0.05), df["log_Density"].quantile(0.95)]  # Avoid extreme outliers
    )
    return fig


#Callback to display country info when clicked
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
