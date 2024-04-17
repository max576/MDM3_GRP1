# just a very basic network just to see feasibility of the appraoch

# imports
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def generate_arbitrary_graph():
    """Function that just generate a simple graph with 
    random node weights and returns the graph object"""
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    G.add_edges_from([(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (2,3), (3,4), (4,5),
                    (5,6), (6,7), (7,8), (8,9), (9,10), (2,1)])
    # get a list of the nodes
    nodes = list(G.nodes)
    edges = list(G.edges)
    # assign random weights to each node
    node_weight_dict = {nodes[i]: np.random.rand(1) for i in range(len(nodes))}
    nx.set_node_attributes(G, node_weight_dict, 'node_weight')

    # set an airport to be hydrogen or not
    airport_dict = {nodes[i]: np.random.choice([0, 1]) for i in range(len(nodes))}
    nx.set_node_attributes(G, airport_dict, 'hydrogen')
    print(airport_dict)
    # do the same for the edges
    edge_weight_dict = {edges[i]: np.random.rand(1) for i in range(len(edges))}
    nx.set_edge_attributes(G, edge_weight_dict, 'edge_weight')
    # plot the graph
    nx.draw(G, pos=nx.spectral_layout(G), with_labels=True, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'edge_weight')
    nx.draw_networkx_edge_labels(G, pos=nx.spectral_layout(G), edge_labels=edge_labels)
    plt.show()
    # print(nx.get_node_attributes(G,'node_weight'))

    return G

def generate_graph(routes, airport_labels, carbon, frequency, distance):
    """Function that generates a graph from a csv file"""
    
    G = nx.Graph()

    # add a node for each airport, with a weight equal to number of flights out
    
    for airport in airport_labels:
        
        num_flights = frequency.loc[airport].sum() # change this to be the sum of the row and column
        num_flights += frequency.loc[:, airport].sum()
        
        
        G.add_node(airport, freq=num_flights)
        # should also add a node attribute for the hydrogen status of the airport (potentially not needed)
        

    # add edges for each possible route
    # so set the has_travelled attribute to 1 for each edge.
    for route in routes:
        source, destination = route
        # change how the carbon attribute is defined - just copy the 2 lines used for num_flights, but change frequency to carbon
        G.add_edge(source, destination, dist=distance.loc[source][destination], carbon=carbon.loc[source][destination], visited=1)
    
    # draw graph
    # nx.draw(G, pos=nx.spectral_layout(G), with_labels=True, font_weight='bold')
    # edge_labels = nx.get_edge_attributes(G, 'dist')
    # nx.draw_networkx_edge_labels(G, pos=nx.spectral_layout(G), edge_labels=edge_labels)
    # plt.show()
    return G


def data_preprocessing():
    """Function that preprocesses the data"""
    # read in the data
    carbon = pd.read_csv('route_carbon_updated.csv', index_col=0)
    # get the airport labels from the CSV
    airport_labels = carbon.columns
    carbon.index = airport_labels
    frequency = pd.read_csv('route_frequency_updated.csv', index_col=0)
    frequency.index = airport_labels
    distance = pd.read_csv('route_distance_updated.csv', index_col=0)
    distance.index = airport_labels

    
    # generate tuples of possible routes
    routes = []
    for i in range(len(airport_labels)):
        for j in range(len(airport_labels)):
            if carbon.iloc[i, j] != 0:
                routes.append((airport_labels[i], airport_labels[j]))
    return routes, airport_labels, carbon, frequency, distance


# could maybe incorporate some methods into the aircraft class for some operations?
class Aircraft():
    """Generates the aircraft object"""
    def __init__(self, aircraft_id, start_node, aircraft_range):
        self.aircraft_id = aircraft_id # id of the aircraft
        self.start_node = start_node
        self.current_node = start_node # origin
        self.airport_list = [self.current_node] # list of airports
        self.active = True # whether the aircraft is active or not
        self.range = aircraft_range # range of the aircraft
        self.current_range = aircraft_range # current range of the aircraft


