# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 19:40:37 2024

@author: max
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

# Load the airport data
airport_data = pd.read_csv('updated_locations.csv')  # Replace with the path to your CSV file

# Haversine formula function
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    dLat = np.radians(lat2 - lat1)
    dLon = np.radians(lon2 - lon1)
    a = np.sin(dLat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dLon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c * 0.539957  # Convert km to nautical miles

# Function to plot airports based on a provided list or based on distance
def plot_airports_using_csv(csv_path=None, iata_code=None):
    plt.figure(figsize=(10, 6))
    m = Basemap(projection='merc', llcrnrlon=-170, llcrnrlat=5, urcrnrlon=-50, urcrnrlat=75, resolution='i')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.fillcontinents(color='lightgray', lake_color='lightblue')
    m.drawmapboundary(fill_color='lightblue')

    x, y = m(airport_data['longitude'].values, airport_data['latitude'].values)
    m.scatter(x, y, color='blue', s=10, label='All Airports', zorder=5)

    if csv_path:
        highlight_data = pd.read_csv(csv_path)
        # Merge highlight data with the main airport data to get latitude and longitude
        valid_airports = pd.merge(highlight_data, airport_data, on='iata', how='inner')
        hx, hy = m(valid_airports['longitude'].values, valid_airports['latitude'].values)
        m.scatter(hx, hy, color='red', s=10, label='Highlighted Airports', zorder=5)
    elif iata_code:
        base_airport = airport_data[airport_data['iata'] == iata_code]
        base_lat = base_airport['latitude'].values[0]
        base_lon = base_airport['longitude'].values[0]
        distances = airport_data.apply(lambda row: haversine(base_lat, base_lon, row['latitude'], row['longitude']), axis=1)
        close_airports = airport_data[distances <= 1000]
        close_x, close_y = m(close_airports['longitude'].values, close_airports['latitude'].values)
        m.scatter(close_x, close_y, color='red', s=10, label='Within 1000 NMs', zorder=5)
        mx, my = m(base_lon, base_lat)
        m.scatter(mx, my, color='green', s=50, marker='*', label=f'Base Airport ({iata_code})', zorder=5)

    plt.title('Airport Map')
    plt.legend(loc='upper left')
    plt.show()

# Main interaction
if __name__ == "__main__":
    use_csv = input("Would you like to use a CSV file for highlighted airports? (yes/no): ").strip().lower()
    if use_csv == 'yes':
        csv_path = input("Enter the path to the CSV file: ").strip()
        plot_airports_using_csv(csv_path=csv_path)
    else:
        user_iata = input("Enter an IATA code: ").strip().upper()
        plot_airports_using_csv(iata_code=user_iata)
