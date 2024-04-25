import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
from funcs import generate_arbitrary_graph, generate_graph, Aircraft, data_preprocessing

# data preprocessing
routes, airport_labels, carbon, frequency, distance = data_preprocessing()

# generate graph
G = generate_graph(routes, airport_labels, carbon, frequency, distance)


population_num = 10 # number of aircraft
aircraft_list = [] # list of aircraft objects

# generate the aircraft objects at hydrogen airports
for i in range(population_num):
    test_range = 2000
    # aircraft_list.append(Aircraft(i, np.random.choice([n for n in G.nodes]), test_range))
    aircraft_list.append(Aircraft(i, 'ATL', test_range))
    # aircraft_list.append(Aircraft(i, np.random.choice([n for n in G.nodes if G.nodes[n]['hydrogen'] == 1]), test_range))

# number of timesteps (number of journeys each aircraft will make)
num_iterations = 100

# Initialize a matrix to represent visited edges
visited_edges = np.zeros((len(G.nodes), len(G.nodes)))

# Create a mapping from airport labels to integer indices
airport_indices = {label: idx for idx, label in enumerate(G.nodes)}

#load carbon emissions data
carbon_matrix = pd.read_csv('route_carbon_updated.csv')
# Convert the DataFrame to a dictionary of dictionaries for easier access
carbon_dict = carbon_matrix.set_index('Unnamed: 0').T.to_dict('index')


# update function
def update():
 
    

    # for each iteration, get next airport for each aircraft
    for _ in range(num_iterations):
        for aircraft in aircraft_list:
            start_node_index = aircraft.airport_list[0]
            if aircraft.active:
                # gets the weights of each neighbour of the current node
                neighbour_weights = [nx.get_node_attributes(G, 'freq')[n] for n in G.neighbors(aircraft.current_node)]
                
                # print(neighbour_weights)
                neighbour_weights = np.array(neighbour_weights)
                # normalise the weights to sum to 1 (could interpret as a probability)
                normalized_weights = neighbour_weights/np.sum(neighbour_weights)
                normalized_weights = np.reshape(normalized_weights, (normalized_weights.shape[0]))

                shortest_paths_list = []

                neighbours = list(G.neighbors(aircraft.current_node))

                # get the shortest path between the potential neighbour nodes and the origin node
                for n in neighbours:
                    shortest_path = nx.shortest_path_length(G, source=n, target=aircraft.airport_list[0], weight='dist')
                    # add distance from current node to neighbour node
                    shortest_path += G.get_edge_data(aircraft.current_node, n)['dist']
                    shortest_paths_list.append(shortest_path)
            
                
                # if range - edge weight < 0, remove it from possible choices
                for i, n in enumerate(list(G.neighbors(aircraft.current_node))):
                    # if G.get_edge_data(aircraft.current_node, n)['edge_weight'] > aircraft.current_range:
                    if G.get_edge_data(aircraft.current_node, n)['dist'] > aircraft.current_range:
                        normalized_weights[i] = 0
                    # if shortest path to get to neighbour and back to origin is greater than the range, remove it from possible choices
                    if shortest_paths_list[i] > aircraft.current_range:
                        normalized_weights[i] = 0
                
                # if all weights are 0, break
                if np.sum(normalized_weights) == 0:
                    aircraft.active = False
                    print(f'Aircraft {aircraft.aircraft_id} has run out of range')
                    break

                # normalise the weights again after removing to ensure they sum to 1
                normalized_weights = normalized_weights/np.sum(normalized_weights)
               
                # get the next node based on a weighted random choice of the neighbours
                next_node = np.random.choice(list(G.neighbors(aircraft.current_node)), p=normalized_weights) # just remove p=normalized_weights to get a uniform random choice

                # get the edge weight between the current node and the next node
                edge_weight = G.get_edge_data(aircraft.current_node, next_node)['dist']
                aircraft.current_range -= edge_weight
                
                # Add the carbon emissions for the current edge to the aircraft's total
                aircraft.carbon_emissions += carbon_dict[aircraft.current_node][next_node]

                
                # append airport to the aircraft's list of airports
                aircraft.airport_list.append(next_node)
                # set the current node to the next node
                aircraft.current_node = next_node
                
                # Convert airport labels to integer indices
                current_node_index = airport_indices[aircraft.current_node]
                next_node_index = airport_indices[next_node]
             
                
                # if aircraft reaches a hydrogen airport, refuel
                # if G.nodes[next_node]['hydrogen'] == 1:
                #     aircraft.current_range = aircraft.range

                # if aircraft reaches the origin airport, set active to False
                if aircraft.current_node == aircraft.airport_list[0]:
                    aircraft.active = False
                    print(f'Aircraft {aircraft.aircraft_id} has completed its journey')
                    print(f'Aircraft {aircraft.aircraft_id} has returned with range:', aircraft.current_range) #how much range the plane returns with
                    break

update()
for i in range(len(aircraft_list)):
    print(f'aircraft{i}', aircraft_list[i].airport_list)
plt.show()

total_carbon = sum(aircraft.carbon_emissions for aircraft in aircraft_list)
print(f'Total carbon emissions for all aircraft: {total_carbon}')

# Carbon emissions from the entire network
total_network_carbon = sum(sum(values.values()) for values in carbon_dict.values())

# Percentage carbon covered by the aircraft (will indicate saving upon hydrogen switch)
carbon_percentage = (total_carbon / total_network_carbon) * 100
print(f"Carbon emissions by the aircraft are {carbon_percentage:.2f}% of the total potential network emissions.")

# Load carbon emissions data
#route_carbon = np.genfromtxt("route_carbon_updated.csv", delimiter=",", filling_values=0)

# Set the first column as the index to facilitate summing
#route_carbon.set_index('Unnamed: 0', inplace=True)

# Compute the undirected graph by summing emissions in both directions
#undirected_carbon = route_carbon + route_carbon.transpose()

# Since the above operation doubles the diagonal (self-loops which should actually be zero), we set the diagonal to zero
#np.fill_diagonal(undirected_carbon.values, 0)

#export to csv
#undirected_carbon.to_csv('undirected_route_carbon.csv')

#total_carbon_emission = np.sum(visited_edges * undirected_carbon)

        
