import requests 
from bs4 import BeautifulSoup
import pandas as pd

# Load the Excel file
df = pd.read_csv('airport-data.csv')

# Get the list of IATA codes
from_codes = df['origin'].tolist()
to_codes = df['destination'].tolist()
frequencies = df['count'].tolist()


# Prepare the CSV file
with open('output1.csv', 'w') as f:
    f.write('from_code,to_code,count,Flight Distance,Flight Time,Direct Flights\n')

for i in range(len(df)):

    from_code = from_codes[i]
    to_code = to_codes[i]
    freq = frequencies[i]
    
    url = f"https://www.travelmath.com/from/{from_code}/to/{to_code}"
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the 'Flying' table
    table = soup.find('div', id='Flying')
    
    # If the 'Flying' table is found, find the rows and extract the data
    if table is not None:
        # Find all rows in the table
        table2 = table.find('table', class_='table')
        rows = table2.find_all('tr', class_='myrow2')
        
        # Prepare a dictionary to store the data for this pair of IATA codes
        data = {'from_code': from_code, 'to_code': to_code, 'count': freq}
        
        # Iterate over the rows
        for row in rows:
            # Find the 'left2' and 'right2' columns in the row
            left2 = row.find('td', class_='left2')
            right2 = row.find('td', class_='right2')
            
            # Check if the 'left2' value is one of the desired headers and the 'right2' value is not None
            if left2.text.strip() in ['Flight Distance', 'Flight Time', 'Direct Flights'] and right2 is not None:
                # Add the data to the dictionary
                data[left2.text.strip()] = right2.text.strip()
            elif left2.text.strip() == 'Direct Flights' and right2 is None:
                # If no value is returned for 'Direct Flights', assign 'N/A' to the corresponding key
                data[left2.text.strip()] = 'N/A'

        
        # Check if data contains all three 'left2' categories
        #if all(key in data for key in ['Flight Distance', 'Flight Time', 'Direct Flights']):
            # Convert the dictionary to a DataFrame
        df = pd.DataFrame([data])
            
            # Append the DataFrame to the CSV file
        df.to_csv('output1.csv', mode='a', header=False, index=False)
