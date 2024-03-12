import pandas as pd

# Read the original CSV file
original_df = pd.read_csv('matlab_out.csv')

# Read the full dataset CSV file
full_df = pd.read_csv('iata-icao.csv')

# Assuming there's a common column/key to merge on, let's call it 'ID'
# Adjust the column name according to your actual data
merged_df = pd.merge(original_df, full_df, on='iata', how='left')

# Write the merged DataFrame back to a new CSV file
merged_df.to_csv('merged.csv', index=False)
