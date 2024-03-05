import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load the Excel file
df = pd.read_excel('ICAO.xlsx', sheet_name='ALL')

# Get the list of IATA codes
iata_codes = df['IATA'].tolist()

# Prepare an empty list to store all the data
all_data = []

for i in range(len(iata_codes)):
    for j in range(len(iata_codes)):
        if i != j:  # Exclude the case where from_code is the same as to_code
            from_code = iata_codes[i]
            to_code = iata_codes[j]
            
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
                data = {'from_code': from_code, 'to_code': to_code}
                
                # Iterate over the rows
                for row in rows:
                    # Find the 'left2' and 'right2' columns in the row
                    left2 = row.find('td', class_='left2')
                    right2 = row.find('td', class_='right2')
                    
                    # Check if the 'left2' value is one of the desired headers and the 'right2' value is not None
                    if left2.text.strip() in ['Flight Distance', 'Flight Time', 'Direct Flights'] and right2.text.strip() != 'None':
                        # Add the data to the dictionary
                        data[left2.text.strip()] = right2.text.strip()
                
                # Check if data contains all three 'left2' categories
                if all(key in data for key in ['Flight Distance', 'Flight Time', 'Direct Flights']):
                    # Add the data to the all_data list
                    all_data.append(data)
                    #print(all_data)
# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(all_data)

# Write the DataFrame to a CSV file
df.to_csv('output.csv', index=False)
