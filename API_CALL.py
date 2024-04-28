import http.client
import json
import requests

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
                "year": int(flight["timestamp"].split('-')[0]),
                "month": int(flight["timestamp"].split('-')[1]),
                "day": int(flight["timestamp"].split('-')[2].split('T')[0])

            }
        }
        flights.append(flight_info)

    api_key = "AIzaSyCohgD5x1eSa1SpKP7cetyZrnttU9_eWks"
    url = f"https://travelimpactmodel.googleapis.com/v1/flights:computeFlightEmissions?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {"flights": flights}

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def main():
    origin = input("Enter origin: ")
    destination = input("Enter destination: ")
    
    response = get_flight_data(origin, destination)
    
    if 'data' not in response:
        print(f"No data for {origin}-{destination}")
    else:
        flight_data_list = response['data']
        print(flight_data_list)
        emissions_data = compute_flight_emissions(flight_data_list)
        print(emissions_data)

if __name__ == "__main__":
    main()
