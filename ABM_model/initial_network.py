# just a very basic network just to see feasibility of the appraoch

# imports
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def generate_graph():
    """Function that just generate a simple graph with 
    random node weights and returns the graph object"""
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    G.add_edges_from([(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (2,3), (3,4), (4,5),
                    (5,6), (6,7), (7,8), (8,9), (9,10)])
    # get a list of the nodes
    nodes = list(G.nodes)
    # assign random weights to each node
    weight_dict = {nodes[i]: np.random.rand(1) for i in range(len(nodes))}
    nx.set_node_attributes(G, weight_dict, 'node_weight')
    # plot the graph
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()
    # print(nx.get_node_attributes(G,'node_weight'))

    return G

class Aircraft():
    """Generates the aircraft object"""
    def __init__(self, aircraft_id, start_node):
        self.aircraft_id = aircraft_id # id of the aircraft
        self.current_node = start_node # origin
        self.airport_list = [self.current_node] # list of airports


population_num = 10 # number of aircraft
aircraft_list = [] # list of aircraft objects

# generate the aircraft objects
for i in range(population_num):
    aircraft_list.append(Aircraft(i, 1))    

# number of timesteps (number of journeys each aircraft will make)
num_iterations = 10

# update function
def update():
    # generate graph
    G = generate_graph()

    # for each iteration, get next airport for each aircraft
    for _ in range(num_iterations):
        for aircraft in aircraft_list:
            # gets the weights of each neighbour of the current node
            neighbour_weights = [nx.get_node_attributes(G, 'node_weight')[n] for n in G.neighbors(aircraft.current_node)]
            # print(neighbour_weights)
            neighbour_weights = np.array(neighbour_weights)
            # normalise the weights to sum to 1 (could interpret as a probability)
            normalized_weights = neighbour_weights/np.sum(neighbour_weights)
            normalized_weights = np.reshape(normalized_weights, (normalized_weights.shape[0]))
            # print(normalized_weights)
            # print(list(G.neighbors(aircraft.current_node)))
            # get the next node based on a weighted random choice of the neighbours
            next_node = np.random.choice(list(G.neighbors(aircraft.current_node)), p=normalized_weights)
            # append airport to the aircraft's list of airports
            aircraft.airport_list.append(next_node)
            # set the current node to the next node
            aircraft.current_node = next_node


update()
print(aircraft_list[0].airport_list)
print(aircraft_list[1].airport_list)

        