# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 16:09:57 2024

@author: max
"""

import pandas as pd
import folium
import folium.plugins as plugins
import random
import re

# Load data
data_path = '90_aircraft_journeys.csv'
locations_path = 'updated_locations.csv'
aircraft_journeys = pd.read_csv(data_path)
airport_locations = pd.read_csv(locations_path)

# Function to split the journey into separate airport codes
def split_journey(journey):
    return re.split(r'\s*->\s*', journey)

# Expand the journey into individual legs
aircraft_journeys['Route'] = aircraft_journeys['Journey'].apply(split_journey)

# Explode the dataframe to get one row per leg
routes = aircraft_journeys.explode('Route')
routes = routes.merge(airport_locations, how='left', left_on='Route', right_on='iata')
routes = routes[['Aircraft ID', 'Route', 'latitude', 'longitude']]
routes.dropna(subset=['latitude', 'longitude'], inplace=True)

# Map initialization
m_color = folium.Map(location=[39.50, -98.35], zoom_start=4)

# Generate random colors
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

aircraft_colors = {aid: random_color() for aid in routes['Aircraft ID'].unique()}

def plot_route_color(group):
    route = group[['latitude', 'longitude']].values
    route_color = aircraft_colors[group['Aircraft ID'].iloc[0]]
    folium.PolyLine(route, color=route_color, weight=1.5, opacity=0.8).add_to(m_color)
    for idx, row in group.iterrows():
        folium.CircleMarker(location=(row['latitude'], row['longitude']), radius=3, color=route_color, fill=True).add_to(m_color)

routes.groupby('Aircraft ID').apply(plot_route_color)
map_color_path = 'Aircraft_Routes_Map_Color.html'
m_color.save(map_color_path)

# Heatmap for airport visits
airport_counts = routes['Route'].value_counts().reset_index()
airport_counts.columns = ['iata', 'visits']
airport_counts = airport_counts.merge(airport_locations[['iata', 'latitude', 'longitude']], on='iata')
heatmap_map = folium.Map(location=[39.50, -98.35], zoom_start=4)
heat_data = [[row['latitude'], row['longitude'], row['visits']] for index, row in airport_counts.iterrows()]
heatmap = plugins.HeatMap(heat_data, radius=15, gradient={0.2: 'blue', 0.4: 'green', 0.6: 'yellow', 0.8: 'orange', 1: 'red'})
heatmap_map.add_child(heatmap)
heatmap_path = 'Airport_Visit_Heatmap.html'
heatmap_map.save(heatmap_path)
