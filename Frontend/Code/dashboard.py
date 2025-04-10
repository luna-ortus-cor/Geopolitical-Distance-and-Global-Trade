from dash import Dash, dcc, html, Output, Input, exceptions, callback_context
import plotly.express as px
import pandas as pd

# Load the datasets
df = pd.read_csv("Frontend/Data/gdi_cleaned.csv")
exports_df = pd.read_csv("Frontend/Data/combined_trade_volume.csv")
trade_to_gdp = pd.read_csv("Backend/data/trade_to_gdp_ratio_clean.csv")
trade_to_gdp = trade_to_gdp[(trade_to_gdp["Year"]>=1989) & (trade_to_gdp["Year"]<=2022)]
ahs_df = pd.read_csv("Frontend/Data/updated_ahs_cleaned.csv")


# Only take years from 1989 to 2020
df = df[(df["Year"] >= 1989) & (df["Year"] <= 2020)]

app = Dash(__name__)

# App layout
app.layout = html.Div(id="app-container", 
    children=[
        #banner
        html.Div(id="banner", className="banner", children=[html.Div("Geopolitical Distance Dashboard", className="banner-title")]),
        #row container for left and right columns
        html.Div(className="row", children=[
            #left column
            html.Div(id="left-column", className="three columns", 
                children=[
                    html.Div(id="left-section-1", children=[
                        html.Div(id="instruction-card", children=[
                            html.Div(className="section-header", children=[
                                html.H5("Explore the Dashboard", className="section-title")
                            ]),
                            html.Div(className="section-body", children=[                            html.H6([
                                "Our dashboard helps ",
                                html.Span("Singapore-based businesses", style={"fontWeight": "bold", "color":"#235284"}),
                                " choose better export partners by showing geopolitical relationships and trade data."
                                ], style={"marginBottom":"4px"}
                            ),                 
                            html.Ul(children=[
                                html.Li("Explore the heatmap to view countries' geopolitical distances from Singapore (Lower GDI means closer ties)"),
                                html.Li("Scroll through time to see how GDI changed"),
                                html.Li("Click any country in the map to see more detailed trade-related visualizations"),
                                html.Li("Go to recommendations tab to get personalized export advice")                                       
                            ], style={"marginBottom":"4px"}),
                            html.Div(id="dropdown", children=[
                                #region dropdown              
                                dcc.Dropdown(
                                    id="region-dropdown",
                                    placeholder="Select a Region",
                                    options= [{"label": "World", "value": "World"}]  + [{"label": region, "value": region} for region in df["region"].unique()],
                                    style={
                                        "width": "260px",
                                        "display": "block",
                                        "padding": "3px",
                                        "borderRadius": "5px",
                                        "border": "1px solid #ccc",
                                        "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)",
                                        "fontSize": "15px"},
                                    multi=False
                                ),
                                #country dropdown
                                dcc.Dropdown(
                                    id="country-dropdown",
                                    placeholder="Select a Country",
                                    options=["World"]+[country for country in df["Name"].unique()],
                                    style={
                                        "width": "260px",
                                        "display": "block",
                                        "padding": "3px",
                                        "borderRadius": "5px",
                                        "border": "1px solid #ccc",
                                        "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)",
                                        "fontSize": "15px"},
                                    multi=True
                                )],style={"marginBottom":"10px"}
                            )]),
                        ])
                    ]),
                    #data description
                    html.Div(id="left-section-2", style={"marginTop":"10px"}, children=[
                        html.Div(className="section-header", children=[
                            html.H5("About our Data", className="section-title")
                        ]),
                        html.Div([
                                html.P("Singapore Net Export to Countries Data:", style={"fontWeight": "bold", "marginBottom": "5px"}),
                                html.P([
                                    "Data source: World Bank (2025) – ",
                                    html.A("Learn more about this data", 
                                           href="https://wits.worldbank.org/CountryProfile/en/Country/SGP/StartYear/1989/EndYear/2022/TradeFlow/Export/Indicator/XPRT-TRD-VL/Partner/BY-COUNTRY/Product/Total", 
                                             target="_blank",
                                             style={"color": "#1f77b4", "textDecoration": "underline"})
                                ])
                            ], style={"fontSize": "15px", "marginTop": "10px"})

                    ])
                ]          
            ),
            #right column
            html.Div(id="right-column", className="nine columns",
                children=[
                    dcc.Tabs(id="tabs", value="heatmap", persistence=True, 
                        children=[
                            #Heatmap Tab
                            dcc.Tab(label="HeatMap", value="heatmap", 
                                children=[
                                html.H4('Animated Geopolitical Distance Over Time', style={"textAlign":"center", "margin-top":"15px", "fontWeight":"bold"}),  
                                # Choropleth map
                                dcc.Loading(dcc.Graph(id="choropleth-map", 
                                                      style={"height": "600px", "width": "100%","margin-top": "-25px"}), type="cube"), 
                                # Country info display
                                html.Div(id="country-info", style={"margin-top": "-5px", "font-weight": "bold", "marginLeft":"40px","fontSize": "18px"})
                                ]
                            ),
                            #details tab
                            dcc.Tab(label="Details", value="details",
                                children=[
                                    html.Div(children=[
                                        #title of detail tab
                                        html.H5(id="details-title", children="Please Click a Country on the Map to View Details", style={"textAlign":"center", "margin-top":"30px", "fontWeight":"bold"}),
                                        #Dropdown to select Product Groups
                                        html.Div(children=[
                                            dcc.Dropdown(
                                                id="product-group-dropdown",
                                                placeholder="Select a Product Group",
                                                style={
                                                    "width": "200px",
                                                    "display": "block",
                                                    "height":"30px",
                                                    "padding": "3px",
                                                    "borderRadius": "5px",
                                                    "border": "1px solid #ccc",
                                                    "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)",
                                                    "fontSize": "15px",
                                                    "fontWeight":"normal"
                                                }
                                            )], style={"marginLeft":"40px"}
                                        ),
                                        # Line chart for export volume
                                        dcc.Graph(id="line-chart", style={"height": "400px"}),
                                        html.Span("Click ", style={"marginLeft":"40px"}),
                                        html.Button("here", id="go-to-recommend", style={"color":"blue"}),
                                        html.Span(" to view recommendations for export strategies to the selected country"),
                                        #trade to gdp chart
                                        html.Hr(style={'border': '1px solid #ccc'}),
                                        html.Div(children=[dcc.Graph(id="gdp-chart", style={"height": "400px"})]),
                                        #tariff chart
                                        html.Div(children=[dcc.Graph(id="ahs-chart", style={"height": "400px"})])
                                        ]
                                    ),
                                ]
                            ),                   
                            #recommendation tab
                            dcc.Tab(label="Recommendations", value="recommendations", children=[])
                        ],
                    )
                ], style={
                    "padding": "2px 2px 2px 0px",
                    "fontSize": "13px",
                    "border": "1px solid #ccc",
                    "borderBottom": "none",
                    "cursor": "pointer",
                    "borderTopLeftRadius": "6px",
                    "borderTopRightRadius": "6px",
                    "fontWeight":"bold",
                    "width": "100%"
                })
            ]
        )
    ]
)

# Callback to update the list of countries based on selected region
@app.callback(
    [Output("country-dropdown", "options"),
     Output("country-dropdown", "value")],  
    Input("region-dropdown", "value")
)
def update_country_dropdown(selected_region):
    if not selected_region or "World" in selected_region:  # If no region or world is selected, show all countries and no default selection
        return [{"label": country, "value": country} for country in df["Name"].unique()], []
    
    # Filter countries by the selected region
    filtered_countries = df[df["region"] == selected_region]["Name"].unique()
    
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
    country_info = df[df["country_id_d"] == clicked_country].iloc[0]

    return f"Country: {country_info['Name']} (Code: {clicked_country})"

# Callback to update the choropleth map
@app.callback(
    Output("choropleth-map", "figure"),
    Input("country-dropdown", "value")  # Dummy input to trigger the function
)
def update_map(selected_countries):
    if not selected_countries:  # If no countries are selected, show the whole world
        filtered_df = df
    else:
        filtered_df = df[df["Name"].isin(selected_countries)]  # Filter by selected countries
    
    fig = px.choropleth(
        filtered_df,
        locations="country_id_d",
        color="GDI",
        hover_name="Name",
        animation_frame="Year",  # Enables animation
        color_continuous_scale=["#08306b", "#4292c6", "#f7fbff"],  # More distinct colors
        projection="natural earth",
        range_color=[df["GDI"].quantile(0.05), df["GDI"].quantile(0.95)]  # Avoid extreme outliers
    )
    fig.update_geos(
    projection_scale=1.2,  #zoom
    center={"lat": 10, "lon": 0},  # centre the map slightly above earth centre to exclude antartica on loading
    showcountries=True)
    return fig

# Callback to update the product group dropdown based on the clicked country
@app.callback(
    Output("product-group-dropdown", "options"),
    Output("product-group-dropdown", "value"),
    Input("choropleth-map", "clickData")
)
def update_product_group_dropdown(clickData):
    if clickData is None:
        raise exceptions.PreventUpdate

    clicked_country = clickData["points"][0]["location"]
    country_matches = df[df["country_id_d"] == clicked_country]
    
    if country_matches.empty:
        return [], None

    country_name = country_matches.iloc[0]["Name"]
    country_exports = exports_df[exports_df["Country"] == country_name]

    product_groups = sorted(country_exports["Product Group"].dropna().unique())
    options = [{"label": pg, "value": pg} for pg in product_groups]
    return options, "All Products" if "All Products" in product_groups else product_groups[0]


#click on the map to go to details tab, update details tab's title and chart
#click to switch to recommendation tab
@app.callback(
    [Output("tabs", "value"),
     Output("details-title", "children")],
    [Input("choropleth-map", "clickData"),
     Input("go-to-recommend", "n_clicks")],
    prevent_initial_call=True
)

def go_to_details(clickData, n_clicks):
    ctx = callback_context
    if not ctx.triggered:
        raise exceptions.PreventUpdate
    
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    # Initialize default title
    title="Please Click a Country on the Map to View Details"

    # Handle choropleth-map click
    if trigger_id == "choropleth-map" and clickData is not None:
        clicked_country = clickData["points"][0]["location"]
        country_data = df[df["country_id_d"] == clicked_country]
        
        if not country_data.empty:
            country_name = country_data.iloc[0]["Name"]
            title = f"Visualization for {country_name}"
        else:
            title = "No data available for selected country."

    # Handle button click to go to recommendations
    elif trigger_id == "go-to-recommend" and n_clicks is not None:
        return "Recommendations", title

    return "details", title
    
@app.callback(
    Output("line-chart", "figure"),
    Output("gdp-chart", "figure"),
    Output("ahs-chart", "figure"),
    Input("choropleth-map", "clickData"),
    Input("product-group-dropdown", "value")
)

def update_line_chart(clickData, selected_group):
    if clickData is None:
        raise exceptions.PreventUpdate

    clicked_country = clickData["points"][0]["location"]
    country_matches = df[df["country_id_d"] == clicked_country]
    
    if country_matches.empty:
        return px.line(title="No export data available")

    country_name = country_matches.iloc[0]["Name"]
    country_exports = exports_df[exports_df["Country"] == country_name]

    if selected_group and selected_group != "All Products":
        country_exports = country_exports[country_exports["Product Group"] == selected_group]

    if country_exports.empty:
        return px.line(title=f"No export data available for {country_name}")

    country_exports["Export by SG Volume"] *= 1000  # Convert to actual USD
    fig = px.line(
        country_exports,
        x="Year",
        y="Export by SG Volume",
        title="Singapore's Export Volume to Selected Country",
        markers=True
    )
    fig.update_layout(
        yaxis_title="Export Volume (US$)" ,
        yaxis_tickformat=",.2s" 
    )
    gdp_chart_data=trade_to_gdp[trade_to_gdp["Country Code"] == clicked_country]
    gdp_chart = px.line(
        gdp_chart_data,
        x="Year",
        y="Value",
        title="Selected Country's Trade-to-GDP Ratio Over Time",
        markers=True
    )
    gdp_chart.update_layout(
        yaxis_title="Trade to GDP ratio",
        yaxis_tickformat=",.2s"
    )

    # AHS Tariff Chart
    country_ahs = ahs_df[ahs_df["Country"] == country_name]
    if country_ahs.empty:
        ahs_fig = px.line(title=f"No AHS data for {country_name}")
    else:
        # Clean out "No Data" values
        country_ahs = country_ahs[country_ahs["AHS Weighted Average (%)"] != "No Data"]
        country_ahs["AHS Weighted Average (%)"] = country_ahs["AHS Weighted Average (%)"].astype(float)

        ahs_fig = px.line(
            country_ahs,
            x="Year",
            y="AHS Weighted Average (%)",
            title="Applied Tariff (AHS Weighted Average %) Over Time",
            markers=True
        )
        ahs_fig.update_layout(yaxis_title="Tariff (%)", yaxis_tickformat=".2%")

    return fig, gdp_chart, ahs_fig



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
