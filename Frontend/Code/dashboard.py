from dash import Dash, dcc, html, Output, Input, exceptions, callback_context
import plotly.express as px
import pandas as pd

# Load the datasets
df = pd.read_csv("Frontend/Data/gdi_cleaned.csv")
exports_df = pd.read_csv("Frontend/Data/combined_trade_volume.csv")
trade_to_gdp = pd.read_csv("Backend/data/trade_to_gdp_ratio_clean.csv")
trade_to_gdp = trade_to_gdp[(trade_to_gdp["Year"] >= 1989) & (trade_to_gdp["Year"] <= 2022)]
ahs_df = pd.read_csv("Frontend/Data/updated_ahs_cleaned.csv")
predictions_df = pd.read_csv("Backend/data/recommendations.csv").assign(country_id_d=lambda x: x['country_id_d'].astype(str).str[:3])

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
                            html.Div(className="section-body",
                                     children=[
                                            # New GeoDistance Overview and Instructions
                                            html.P(["Our dashboard helps ",
                                                     html.Span("Singapore-based businesses", style={"fontWeight": "bold", "color":"#235284"}),
                                                                " choose better export partners by analysing geopolitical relations and trade data."
                                                            ], style={"marginBottom":"4px", "marginTop":"0px"}
                                            ),
                                            html.P( ["We have introduced a new ",
                                                html.Span("geopolitical Distance Index (GDI)", style={"fontWeight": "bold", "color":"#235284"}),
                                                            ", combining key factors like free trade agreements, arms trade relations, language/cultural commonalities, political alignment, and democracy levels to gauge each country's geopolitical proximity to Singapore. Lower values indicate closer ties, while higher values signal greater distance.",
                                                ], style={"marginBottom": "0px"}
                                            ),
                                            html.H6(html.Span("Navigate the World Map"), style={"fontWeight": "bold", "marginBottom": "0"}),
                                            html.Ul(children=[
                                                html.Li(html.Span("Use the slider to see how GDI changes over time."), style={"marginBottom": "0"}),
                                                html.Li("Click on any country for deeper insights.")
                                            ], style={"marginBottom": "0px"}),
                                            html.H6(html.Span("Filter by Region or Country"), style={"fontWeight": "bold", "marginBottom": "0"}),
                                            # Region and Country dropdowns
                                            html.Div(
                                                id="dropdown",
                                                children=[
                                                    dcc.Dropdown(
                                                        id="region-dropdown",
                                                        placeholder="Select a Region",
                                                        options=[{"label": "World", "value": "World"}] + [
                                                            {"label": region, "value": region}
                                                            for region in df["region"].unique()
                                                        ],
                                                        style={
                                                            "width": "200px",
                                                            "display": "block",
                                                            "padding": "3px",
                                                            "borderRadius": "5px",
                                                            "border": "1px solid #ccc",
                                                            "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)",
                                                            "fontSize": "15px"
                                                        },
                                                        multi=False
                                                    ),
                                                    dcc.Dropdown(
                                                        id="country-dropdown",
                                                        placeholder="Select a Country",
                                                        options=["World"] + [country for country in df["Name"].unique()],
                                                        style={
                                                            "width": "200px",
                                                            "display": "block",
                                                            "padding": "3px",
                                                            "borderRadius": "5px",
                                                            "border": "1px solid #ccc",
                                                            "boxShadow": "2px 2px 5px rgba(0,0,0,0.1)",
                                                            "fontSize": "15px"
                                                        },
                                                        multi=True
                                                    )
                                                ],
                                                style={"marginBottom": "10px"}
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    # Data description and Sources
                    html.Div(
                        id="left-section-2",
                        style={"marginTop": "10px"},
                        children=[
                            html.Div(
                                className="section-header",
                                children=[html.H5("About our Data", className="section-title")]
                            ),
                            html.Div(className="section-body", children=[
                                html.P("GDI measure data sources:", style={"fontWeight": "bold", "marginBottom": "5px", "marginTop":"0px"}),
                                html.Ul([
                                    html.Li([
                                        html.A(
                                            "CEPII Gravity Dataset",
                                            href="https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=8",
                                            target="_blank",
                                            style={"color": "#1f77b4", "textDecoration": "underline"}
                                        ),
                                        " – Offers trade friction metrics such as distance, shared language, colonial ties."
                                    ]),
                                    html.Li([
                                        html.A(
                                            "SIPRI Arms Transfer Database",
                                            href="https://armstransfers.sipri.org/ArmsTransfer/TransferRegister",
                                            target="_blank",
                                            style={"color": "#1f77b4", "textDecoration": "underline"}
                                        ),
                                        " – Provides detailed arms trade data, revealing security and partnership dimensions."
                                    ]),
                                    html.Li([
                                        html.A(
                                            "UNGA Voting Records",
                                            href="http://unvotes.org/",
                                            target="_blank",
                                            style={"color": "#1f77b4", "textDecoration": "underline"}
                                        ),
                                        " – Reflects diplomatic policy alignment among nations."
                                    ]),
                                    html.Li([
                                        html.A(
                                            "V-Dem Dataset",
                                            href="https://www.v-dem.net/data/the-v-dem-dataset/country-year-v-dem-core-v15/",
                                            target="_blank",
                                            style={"color": "#1f77b4", "textDecoration": "underline"}
                                        ),
                                        " – Delivers democracy metrics and governance differences between countries."
                                    ])
                                ])
                            ])
                        ]
                    )
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
                                html.H5('Geopolitical Distance Between Singapore and World', style={"textAlign":"center", "margin-top":"15px", "fontWeight":"bold", "marginBottom": "40px"}),  
                                # Choropleth map
                                dcc.Loading(dcc.Graph(id="choropleth-map", 
                                                      style={"height": "600px", "width": "100%", "marginTop": "0px"}), type="cube"),
                                # Country info display
                                html.Div(id="country-info", style={"margin-top": "-5px", "font-weight": "bold", "marginLeft":"40px","fontSize": "18px", "marginBottom":"10px"})
                                ], style={"padding": "10px 20px"} 
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
                                        html.Div(id="line-chart-description", children=[
                                            html.P("This chart shows Singapore's export volume to the selected country over time. An upward trend can indicate growing demand or more robust trading relationships while a downward trend could signal a potential decline in trade activity. Higher values mean stronger export performance, while lower values reflect weaker market activity.",
                                                   style={"textAlign": "center", "margin": "10px", "fontSize": "14px"})
                                        ]),
                                        #trade to gdp chart
                                        html.Hr(style={'border': '1px solid #ccc'}),
                                        html.Div(children=[dcc.Graph(id="gdp-chart", style={"height": "400px"}),
                                                        # Description under the gdp chart
                                            html.Div(id="gdp-chart-description", children=[
                                                html.P("This graph displays the trade-to-GDP ratio of the selected country, measuring trade volume relative to the size of its economy. Higher ratios indicate that trade plays a larger role in the country’s economic activity.",
                                                       style={"textAlign": "center", "margin": "10px", "fontSize": "14px"})
                                            ])
                                        ]),
                                        #tariff chart
                                        html.Hr(style={'border': '1px solid #ccc'}),
                                        html.Div(children=[dcc.Graph(id="ahs-chart", style={"height": "400px"}),
                                                        # Description under the AHS tariff chart
                                            html.Div(id="ahs-chart-description", children=[
                                                html.P("This visualization tracks the changes in applied tariff rates over time. An increasing trend implies that tariff rates are rising, which may reflect tighter trade policies, potentially raising the cost of imports. A decreasing trend indicates lower tariff rates, suggesting a shift toward a more open trade environment with reduced trade barriers.",
                                                       style={"textAlign": "center", "margin": "10px", "fontSize": "14px"})
                                            ])
                                        ]),
                                        html.Span("Click ", style={"marginLeft":"10px", "marginTop":"10px"}),
                                        html.Button("here", id="go-to-recommend", style={"color":"blue"}),
                                        html.Span(" to view recommendations for export strategies to the selected country", style={"marginBottom":"10px"})
                                    ]),
                                ]),
                            #recommendation tab
                            dcc.Tab(label="Recommendations", value="Recommendations", children=[
                                html.H5("Export Strategy Recommendations", id="recommendation-title", style={"textAlign":"center", "margin-top":"15px", "fontWeight":"bold"}),
                                html.Div([
                                    # Export Volume Section
                                    html.Div([
                                        html.P([
                                            html.Strong("Predicted Export Volume of "),
                                            html.Span(id="country-name-prediction"),
                                            ": ",
                                            html.Span(id="predicted-export-value"),
                                            html.Div(id="export-recommendation-text", style={"marginTop":"0px"})
                                            ])
                                            ], className="recommendation-box"),
                                    # GDI Section
                                    html.Div([
                                        html.P([
                                            html.Strong("Predicted Geopolitical Distance Index (GDI): "),
                                            html.Span(id="predicted-gdi-value"),
                                            html.Div(id="gdi-recommendation-text", style={"marginTop":"0px"})
                                            ]),
                                            ], className="recommendation-box"),
                                    # Trade-to-GDP Section
                                    html.Div([
                                        html.P([
                                            html.Strong("Trade-to-GDP Ratio: "),
                                            html.Span(id="trade-gdp-value"),
                                            html.Div(id="trade-gdp-recommendation-text")
                                            ])
                                            ], className="recommendation-box"),
                                    # AHS Tariff Section
                                    html.Div([
                                        html.P([
                                            html.Strong("Tariff Rate: "),
                                            html.Span(id="tariff-value"),
                                            html.P(id="tariff-recommendation-text")
                                            ])
                                            ], className="recommendation-box")
                                        ], style={"marginLeft":"20px"
                                        })
                            ])
                        ],
                    )
                ], style={
                    "padding": "2px 2px 2px 0px",
                    "fontSize": "13px",
                    "border": "1px solid #ccc",
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



# Thresholds for Recommendations
# Filter to only include 2021
trade_to_gdp_2021 = trade_to_gdp[trade_to_gdp["Year"] == 2021]
ahs_df_2021 = ahs_df[ahs_df["Year"] == 2021]
ahs_df_2021 = ahs_df_2021[ahs_df_2021["AHS Weighted Average (%)"] != "No Data"] #exclude "No Data" values
thresholds = {
    "export": {
        "low": predictions_df["exp_export_2021"].quantile(0.25),
        "high": predictions_df["exp_export_2021"].quantile(0.75)
    },
    "gdp_ratio": {
        "low": trade_to_gdp_2021["Value"].quantile(0.25),
        "high": trade_to_gdp_2021["Value"].quantile(0.75)
    },
    "gdi": {
        "low": predictions_df["geodistance"].quantile(0.25),
        "high": predictions_df["geodistance"].quantile(0.75)
    }
}

@app.callback(
    [
        Output("tabs", "value"),
        Output("details-title", "children"),
        Output("recommendation-title", "children"),
        Output("country-name-prediction", "children"),
        Output("predicted-export-value", "children"),
        Output("export-recommendation-text", "children"),
        Output("predicted-gdi-value", "children"),
        Output("gdi-recommendation-text", "children"),
        Output("trade-gdp-value", "children"),  
        Output("trade-gdp-recommendation-text", "children"),
        Output("tariff-value", "children"),  
        Output("tariff-recommendation-text", "children")
    ],
    [
        Input("choropleth-map", "clickData"),
        Input("go-to-recommend", "n_clicks")
    ],
    prevent_initial_call=True
)
def tabs_callback(clickData, n_clicks):
    ctx = callback_context
    if not ctx.triggered:
        raise exceptions.PreventUpdate
    
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    # Initialize default values
    tab_value = "details"
    details_title = "Please Click a Country on the Map to View Details"
    recommendation_outputs = ["Please click a country on the map to view recommendation", 
                            "", "", "", "", "", "", "", "", ""]
    
    if clickData is not None:
        clicked_country = clickData["points"][0]["location"]
        country_data = df[df["country_id_d"] == clicked_country]
        country_name = country_data.iloc[0]["Name"]
        country_id = country_data.iloc[0]["country_id_d"]
        
        # Update details title if map was clicked
        if trigger_id == "choropleth-map":
            if not country_data.empty:
                details_title = f"In-Depth Trade Trends & Analysis for {country_name}"
            else:
                details_title = "No data available for selected country."
        try:
            # Get prediction data (assumed to always exist)
            row = predictions_df[predictions_df["country_id_d"] == country_data["country_id_d"].values[0]].iloc[0]
                
            # Get trade-to-GDP data (might be missing)
            trade_gdp_row = trade_to_gdp_2021[trade_to_gdp_2021["Country Code"] == clicked_country]
            has_trade_gdp = (
                not trade_gdp_row.empty and 
                pd.notna(trade_gdp_row["Value"].iloc[0])
            )
            trade_gdp_value = trade_gdp_row["Value"].values[0] if has_trade_gdp else None
                
            # Get tariff data (might be missing)
            tariff_row = ahs_df_2021[ahs_df_2021["Country"] == country_data["Name"].values[0]]
            has_tariff = not tariff_row.empty
            tariff_value = float(tariff_row["AHS Weighted Average (%)"].values[0]) if has_tariff else None
                
            def classify(value, metric):
                if value is None:
                    return ""
                if value < thresholds[metric]["low"]:
                    return "LOW"
                elif value > thresholds[metric]["high"]:
                    return "HIGH"
                else:
                    return "AVERAGE"
                
            # Predicted export volume
            export_class = classify(row["exp_export_2021"], "export")
            export_text = {
                "HIGH": "This value is >75th percentile and considerd HIGH. A high export volume suggests strong and sustained demand, signaling solid commercial potential. It is recommended to expand export commitments and explore long-term trade contracts",
                "AVERAGE": "This value is at 25-75th percentile and considered AVERAGE. This market is neighter a top performer not significantly underperforming. Maintain current export strategy but keep a lookout for new markets.",
                "LOW": "This value is <25th percentile and considered LOW. Low volume may reflect poor fit, weak demand, or external barriers (e.g. regulations). Monitor market before making decisions, and consider reducing export volume or exploring new destinations."
            }.get(export_class, "No data available")

            # Predicted GDI
            gdi_class = classify(row["geodistance"], "gdi")
            gdi_text = {
                "HIGH": "This value is >75th percentile and considered geopolitically FAR. This country is geopolitically distant from Singapore, which may expose your business to elevated political risks. It is advisable to reassess your engagement and consider diversifying exports to more geopolitically aligned markets.",
                "AVERAGE": "This value is at 25th–75th percentile and considered AVERAGE. This market shows moderate geopolitical alignment with Singapore. Maintain current level of engagement, while monitoring for political shifts or new bilateral opportunities",
                "LOW": "This value is <25th percentile and considered geopolitically CLOSE. This country maintains close geopolitical ties with Singapore, offering a stable and cooperative trade environment. You are encouraged to improve diplomatic alignment, expand market, and consider long-term presence"
            }.get(gdi_class, "No data available")

            # Trade-to-GDP ratio (might be missing)
            if has_trade_gdp:
                trade_to_gdp_class = classify(trade_gdp_value, "gdp_ratio")
                trade_gdp_text = {
                    "HIGH": "This value is >75th percentile and considered HIGH. This country relies heavily on international trade, suggesting a favorable environment for export activites. Consider this market a strong candidate for expanding your trade footprint.",
                    "AVERAGE": "This value is at 25th-75th percentile and considered AVERAGE. This country has moderate trade dependence. Maintain your current trade strategy while monitoring for olicy direction or economic trends before acting",
                    "LOW": "This value is <25th percentile and considered LOW. Trade may not be a priority for this country, better to deprioritize this market and focus on other regions with stronger trade incentives."
                    }.get(trade_to_gdp_class, "")
            else:
                trade_gdp_text = "No trade-to-GDP data available"
            trade_gdp_display = f"{trade_gdp_value:,.1f}%" if has_trade_gdp else "No data available"

            # Tariff rate (might be missing)
            if has_tariff:
                tariff_class = "Zero" if tariff_value == 0 else "Non-Zero"
                tariff_text = {
                    "Non-Zero": "This country imposes NON-ZERO tariffs on imports, which may squeeze profit margins. Consider shifting to lower-tariff countries or look for FTA opportunities",
                    "Zero": "This country has NO tariffs on imports, indicating minimal barriers to entry. The favorable trade conditions present a strong opportunity to expand your exports with fewer cost concerns"
                    }.get(tariff_class, "")
            else:
                tariff_text = ""
            tariff_display = f"{tariff_value:.5f}%" if has_tariff else "No data available"

            recommendation_outputs = [
                f"Export Strategy Recommendation for {country_name}",
                country_name,
                f"{row['exp_export_2021']:,.0f} USD",
                export_text,
                f"{row['geodistance']:,.0f}",
                gdi_text,
                trade_gdp_display,
                trade_gdp_text,
                tariff_display,
                tariff_text
            ]
                
        except Exception as e:
            print(f"Error getting data: {e}")
            recommendation_outputs = ["Error loading data"] * 10

    
    # Handle direct tab switch
    if trigger_id == "go-to-recommend":
        tab_value = "Recommendations"
    elif trigger_id == "choropleth-map":
        tab_value = "details"
    
    
    return [tab_value, details_title] + recommendation_outputs

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
