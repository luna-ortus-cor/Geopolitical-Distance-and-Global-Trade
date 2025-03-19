import os
import streamlit as st
import folium
import geopandas as gpd
from folium import Choropleth, GeoJson
from folium import GeoJsonTooltip
from streamlit_folium import folium_static
from streamlit_folium import st_folium # Import folium_static

#initialize session state
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None
if "geo_data" not in st.session_state:
    geo_data = gpd.read_file("world_population_density.geojson") # Load the GeoJSON data

# Create a base map using Folium with a better TileLayer (CartoDB positron)
m = folium.Map(location=[20, 0], zoom_start=2, max_zoom=10)  # Set max_zoom to 10 to avoid extreme zooming out

# Add CartoDB positron TileLayer for a more optimized world map
folium.TileLayer('cartodb positron').add_to(m)

# Add choropleth layer
choropleth = Choropleth(
    geo_data=geo_data,
    data=geo_data,
    columns=['name', 'population_density'],  # Make sure 'population_density' exists in your data
    key_on="feature.properties.name",  # Linking data with GeoJSON
    fill_color="YlGnBu",  # Color scheme
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Population Density"
).add_to(m)

# Add GeoJsonTooltip to the GeoJson layer inside the choropleth
geo_json = choropleth.geojson  # Access the underlying GeoJson object
tooltip = GeoJsonTooltip(
    fields=["name", "population_density"],  # Adjust according to the columns in your data
    aliases=["Country", "Population Density"],
    localize=True
)
tooltip.add_to(geo_json)

# Fit map bounds to GeoJSON data (auto-adjust view based on data)
m.fit_bounds(m.get_bounds())

# Display map in Streamlit app
st.title("World Population Density Choropleth Map")
st.sidebar.page_link("pages/visualization.py", label="Go to Visualization Page")

#handle click on the map
clicked_data = st_folium(m, width=800, height=500) #store click data on the map
if clicked_data and "last_active_drawing" in clicked_data: #check if user clicks on a country in the map
    last_active = clicked_data["last_active_drawing"] 
    if last_active and "properties" in last_active and "name" in last_active["properties"]:
        selected_country = last_active["properties"]["name"]  # Retrieve country name
        st.session_state.selected_country = selected_country
if st.session_state.selected_country:
    st.switch_page("pages/visualization.py") #redirect to details page with visualizations