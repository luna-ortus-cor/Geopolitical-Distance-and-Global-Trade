import streamlit as st
import folium
import geopandas as gpd
from folium import Choropleth, GeoJson
from folium import GeoJsonTooltip
from streamlit_folium import folium_static  # Import folium_static

# Load the GeoJSON data
geo_data = gpd.read_file("world_population_density.geojson")

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
folium_static(m)  # Render the map
