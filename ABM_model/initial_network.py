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
    
    # print(nx.get_node_attributes(G,'node_weight'))

    return G

# could maybe incorporate some methods into the aircraft class for some operations?
class Aircraft():
    """Generates the aircraft object"""
    def __init__(self, aircraft_id, start_node, aircraft_range):
        self.aircraft_id = aircraft_id # id of the aircraft
        self.current_node = start_node # origin
        self.airport_list = [self.current_node] # list of airports
        self.active = True # whether the aircraft is active or not
        self.range = aircraft_range # range of the aircraft
        self.current_range = aircraft_range # current range of the aircraft


# generate graph
G = generate_graph()
population_num = 10 # number of aircraft
aircraft_list = [] # list of aircraft objects

# generate the aircraft objects at hydrogen airports
for i in range(population_num):
    test_range = 5
    aircraft_list.append(Aircraft(i, np.random.choice([n for n in G.nodes if G.nodes[n]['hydrogen'] == 1]), test_range))


# number of timesteps (number of journeys each aircraft will make)
num_iterations = 100

# update function
def update():
 
    

    # for each iteration, get next airport for each aircraft
    for _ in range(num_iterations):
        for aircraft in aircraft_list:
            if aircraft.active:
                # gets the weights of each neighbour of the current node
                neighbour_weights = [nx.get_node_attributes(G, 'node_weight')[n] for n in G.neighbors(aircraft.current_node)]
                # print(neighbour_weights)
                neighbour_weights = np.array(neighbour_weights)
                # normalise the weights to sum to 1 (could interpret as a probability)
                normalized_weights = neighbour_weights/np.sum(neighbour_weights)
                normalized_weights = np.reshape(normalized_weights, (normalized_weights.shape[0]))
  
                # if range - edge weight < 0, remove it from possible choices
                for i, n in enumerate(list(G.neighbors(aircraft.current_node))):
                    if G.get_edge_data(aircraft.current_node, n)['edge_weight'] > aircraft.current_range:
                        normalized_weights[i] = 0
                
                # if all weights are 0, break
                if np.sum(normalized_weights) == 0:
                    aircraft.active = False
                    print(f'Aircraft {aircraft.aircraft_id} has run out of range')
                    break

                # normalise the weights again after removing to ensure they sum to 1
                normalized_weights = normalized_weights/np.sum(normalized_weights)
               
                # get the next node based on a weighted random choice of the neighbours
                next_node = np.random.choice(list(G.neighbors(aircraft.current_node)), p=normalized_weights)

                # get the edge weight between the current node and the next node
                edge_weight = G.get_edge_data(aircraft.current_node, next_node)['edge_weight']
                aircraft.current_range -= edge_weight
                
                # append airport to the aircraft's list of airports
                aircraft.airport_list.append(next_node)
                # set the current node to the next node
                aircraft.current_node = next_node
                # if aircraft reaches a hydrogen airport, refuel
                if G.nodes[next_node]['hydrogen'] == 1:
                    aircraft.current_range = aircraft.range

                # if aircraft reaches the origin airport, set active to False
                if aircraft.current_node == aircraft.airport_list[0]:
                    aircraft.active = False
                    print(f'Aircraft {aircraft.aircraft_id} has completed its journey')
                    break


update()
for i in range(len(aircraft_list)):
    print(f'aircraft{i}', aircraft_list[i].airport_list)
plt.show()
        