# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 15:56:14 2024

@author: max
"""

import pandas as pd
import folium
import random
import re

def split_journey(journey):
    """Split the journey string into a list of airport codes."""
    return re.split(r'\s*->\s*', journey)

def random_color():
    """Generate a random hex color."""
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def plot_route_color(group, map_obj, colors_dict):
    """Plot each route on the map with a specific color."""
    route = group[['latitude', 'longitude']].values
    route_color = colors_dict[group['Aircraft ID'].iloc[0]]
    folium.PolyLine(route, color=route_color, weight=1.5, opacity=0.8).add_to(map_obj)
    for _, row in group.iterrows():
        folium.CircleMarker(location=(row['latitude'], row['longitude']), radius=3, color=route_color, fill=True).add_to(map_obj)

def main(data_path, locations_path, output_path):
    # Load data
    aircraft_journeys = pd.read_csv(data_path)
    airport_locations = pd.read_csv(locations_path)
    
    # Process routes
    aircraft_journeys['Route'] = aircraft_journeys['Journey'].apply(split_journey)
    routes = aircraft_journeys.explode('Route')
    routes = routes.merge(airport_locations, how='left', left_on='Route', right_on='iata')
    routes = routes[['Aircraft ID', 'Route', 'latitude', 'longitude']]
    routes.dropna(subset=['latitude', 'longitude'], inplace=True)
    
    # Create map
    m = folium.Map(location=[39.50, -98.35], zoom_start=4)
    aircraft_colors = {aid: random_color() for aid in routes['Aircraft ID'].unique()}
    
    # Plot each aircraft's route with different colors
    routes.groupby('Aircraft ID').apply(lambda x: plot_route_color(x, m, aircraft_colors))
    
    # Save to HTML
    m.save(output_path)

# Usage
if __name__ == "__main__":
    main('path_to_aircraft_journeys.csv', 'path_to_airport_locations.csv', 'output_path_to_map.html')
