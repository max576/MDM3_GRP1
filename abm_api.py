# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 18:44:10 2024

@author: max
"""

import http.client
import json
import requests
import pandas as pd

def get_flight_data(origin, destination):
    conn = http.client.HTTPSConnection("fr24api.flightradar24.com")
    payload = ''
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer 9b8c4b0c-9997-4948-a2a3-fbf3f9fe1f81|bllsoEf3E9s4NIPc6H2MQkYoW1f3n4U4UOoC9zVy939e8fa3'
    }
    conn.request("GET", f"/api/flights?routes={origin}-{destination}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    response = json.loads(data.decode("utf-8"))
    return response

def compute_flight_emissions(flight_data):
    flights = []
    for flight in flight_data:
        carrier_code = flight['flight'][:2]
        flight_number = flight['flight'][2:]
        flight_info = {
            "origin": flight["orig_iata"],
            "destination": flight["dest_iata"],
            "operatingCarrierCode": carrier_code,
            "flightNumber": int(flight_number),
            "departureDate": {
                "year": int(2023),#flight["timestamp"].split('-')[0]),
                "month": int(12),#flight["timestamp"].split('-')[1]),
                "day": int(12)#flight["timestamp"].split('-')[2].split('T')[0])
            }
        }
        flights.append(flight_info)

    api_key = "AIzaSyCohgD5x1eSa1SpKP7cetyZrnttU9_eWks"
    url = f"https://travelimpactmodel.googleapis.com/v1/flights:computeFlightEmissions?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {"flights": flights}

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def parse_journeys(journey):
    """Parse the journey string into a list of (origin, destination) tuples."""
    legs = journey.split(" -> ")
    return [(legs[i], legs[i+1]) for i in range(len(legs) - 1)]

def main():
    # Load the CSV file
    file_path = 'aircraft_journeys.csv'
    data = pd.read_csv(file_path)
    
    # Prepare the dictionary to collect all the emissions data
    aircraft_emissions = {}

    # Iterate over each row in the DataFrame
    for index, row in data.iterrows():
        aircraft_id = row['Aircraft ID']
        journey = row['Journey']
        legs = parse_journeys(journey)
        
        emissions_list = []
        for origin, destination in legs:
            response = get_flight_data(origin, destination)
            
            if 'data' not in response:
                emissions_list.append("No data")
            else:
                flight_data_list = response['data']
                emissions_data = compute_flight_emissions(flight_data_list)
                emissions_list.append(emissions_data)

        aircraft_emissions[aircraft_id] = emissions_list

    # Create DataFrame to save to CSV
    emissions_df = pd.DataFrame.from_dict(aircraft_emissions, orient='index')
    emissions_df.columns = [f"Leg {i+1}" for i in range(emissions_df.shape[1])]  # Creating column names based on leg number
    emissions_df.to_csv('emissions_output.csv')

if __name__ == "__main__":
    main()
