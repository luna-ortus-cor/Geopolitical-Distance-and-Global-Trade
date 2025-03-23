from dash import Dash, dcc, html, Output, Input, exceptions, callback_context
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv("cleaned_population_density_time.csv")

app = Dash(__name__)

# App layout
app.layout = html.Div(style={"margin":"50px"}, children=[
    dcc.Tabs(id="tabs", value="heatmap", persistence=True, children=[
        #Heatmap Tab
        dcc.Tab(label="HeatMap", value="heatmap", children=[
            html.H2('Animated Population Density Over Time', style={"textAlign":"center"}),
            #country dropdown
            dcc.Dropdown(
                    id="region-dropdown",
                    placeholder="Select a Region",
                    options= [{"label": "World", "value": "World"}]  + [{"label": region, "value": region} for region in df["region"].unique()],
                    style={
                        "width": "250px",
                        "height": "30px",
                        "display": "block",
                        "padding": "3px",
                        "borderRadius": "5px",
                        "border": "1px solid #ccc",
                        "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)",
                        "fontSize": "15px"},
                        multi=False
                        ),
            dcc.Dropdown(
                        id="country-dropdown",
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
        ]),
        #details tab
        dcc.Tab(label="Details", value="details", children=[
            html.H2(id="details-title", style={"textAlign":"center"}),
            dcc.Graph(id="line-chart"), 
            html.Span("Click "),
            html.Button("here", id="go-to-recommend", style={"color":"blue"}),
            html.Span(" to view recommendations for export strategies to the selected country")
        ]),
        #recommendation tab
        dcc.Tab(label="Recommendations", value="recommendations", children=[])
    ], 
    style={
        "padding": "5px 2px 2px 0px",
        "fontSize": "13px",
        "backgroundColor": "#f2f2f2",
        "border": "1px solid #ccc",
        "borderBottom": "none",
        "cursor": "pointer",
        "borderTopLeftRadius": "6px",
        "borderTopRightRadius": "6px",
        "fontWeight":"bold"
    })
])

# Callback to update the list of countries based on selected region
@app.callback(
    [Output("country-dropdown", "options"),
     Output("country-dropdown", "value")],  
    Input("region-dropdown", "value")
)
def update_country_dropdown(selected_region):
    if not selected_region or "World" in selected_region:  # If no region or world is selected, show all countries and no default selection
        return [{"label": country, "value": country} for country in df["name"].unique()], []
    
    # Filter countries by the selected region
    filtered_countries = df[df["region"] == selected_region]["name"].unique()
    
    # Return options for the dropdown and set all filtered countries as the selected values
    return [{"label": country, "value": country} for country in filtered_countries], list(filtered_countries)

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

# Callback to update the choropleth map
@app.callback(
    Output("choropleth-map", "figure"),
    Input("country-dropdown", "value")  # Dummy input to trigger the function
)
def update_map(selected_countries):
    if not selected_countries:  # If no countries are selected, show the whole world
        filtered_df = df
    else:
        filtered_df = df[df["name"].isin(selected_countries)]  # Filter by selected countries
    
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

#click on the map to go to details tab, update details tab's title and chart
#click to switch to recommendation tab
@app.callback(
    Output("tabs", "value"),
    Output("details-title", "children"),
    Input("choropleth-map", "clickData"),
    Input("go-to-recommend", "n_clicks"),
    prevent_initial_call=True
)
def go_to_details(clickData, n_clicks):
    ctx=callback_context
    if not ctx.triggered:
        raise exceptions.PreventUpdate
    trigger_id=ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id=="choropleth-map":
        clicked_country = clickData["points"][0]["location"]
        country_data = df[df["Country Code"] == clicked_country]
        if country_data.empty:
            return "details", "No data available for selected country."
        country_name=country_data.iloc[0]["name"]
        return "details", f"Visualization for {country_name}"
    elif trigger_id == "go-to-recommend":
        return "recommendations", ""
    raise exceptions.PreventUpdate
    
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
