import pandas as pd
import numpy as np

airport_labels = pd.read_csv('first_network.csv')['iata'].to_list()

carbon = pd.read_csv('route_carbon.csv', names=airport_labels)
carbon.index = airport_labels
print(carbon)

frequency = pd.read_csv('route_frequency.csv', names=airport_labels)
frequency.index = airport_labels
print(frequency)

distance = pd.read_csv('route_distance.csv', names=airport_labels)
distance.index = airport_labels
print(distance)

# if adjacency matrix has a zero in one direction, it should have a zero in the other direction
# check if the adjacency matrix is symmetric
for i in range(len(airport_labels)):
    for j in range(len(airport_labels)):
        if carbon.iloc[i, j] == 0:
            carbon.iloc[j, i] = 0
            
        if frequency.iloc[i, j] == 0:
            frequency.iloc[j, i] = 0
            
        if distance.iloc[i, j] == 0:
            distance.iloc[j, i] = 0

# if a column has all zeros, then remove row and column of corresponding airport
zero_rows = carbon.index[(carbon == 0).all(axis=1)]
carbon = carbon.drop(zero_rows, axis=0)
carbon = carbon.drop(zero_rows, axis=1)

zero_rows = frequency.index[(frequency == 0).all(axis=1)]
frequency = frequency.drop(zero_rows, axis=0)
frequency = frequency.drop(zero_rows, axis=1)

zero_rows = distance.index[(distance == 0).all(axis=1)]
distance = distance.drop(zero_rows, axis=0)
distance = distance.drop(zero_rows, axis=1)

print(zero_rows)
# remove airport from airpirt_labels
airport_labels = [label for label in airport_labels if label not in zero_rows]
            
carbon.to_csv('route_carbon_updated.csv')
frequency.to_csv('route_frequency_updated.csv')
distance.to_csv('route_distance_updated.csv')

# generate tuples of possible routes
routes = []
for i in range(len(airport_labels)):
    for j in range(len(airport_labels)):
        if carbon.iloc[i, j] != 0:
            routes.append((airport_labels[i], airport_labels[j]))



print(carbon)


# check the dataframes have symmetric zeros
# create a mask of the zeros
mask = (carbon == 0)
# print(mask)
# print(mask.T)
# # check if the mask is symmetric
# print(mask.equals(mask.T))

# not symmetric as i think there are some routes only in one direction
# how to go about this? 
# reckon only use the routes that are in both directions
# and then take the minimum of the two values for the carbon and frequency

# remove routes that are not in both directions





