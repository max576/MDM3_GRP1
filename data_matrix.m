% Load the data
data = readtable('flights-airport.csv');

% Get unique locations (both origins and destinations)
locations = unique([data.origin; data.destination]);

% Initialize matrix
matrix = zeros(length(locations));

% Fill the matrix
for i = 1:length(locations)
    for j = 1:length(locations)
        % Find rows with the current origin and destination
        rows = strcmp(data.origin, locations(i)) & strcmp(data.destination, locations(j));
        
        % Sum the counts for these rows and store in the matrix
        matrix(i, j) = sum(data.count(rows));
    end
end

% Create a directed graph from the adjacency matrix
G = digraph(matrix, 'OmitSelfLoops');

% Compute in-degree and out-degree centralities for the nodes
indegree_centrality = centrality(G, 'indegree');
outdegree_centrality = centrality(G, 'outdegree');

% Store the centrality measures in the Nodes table of the graph
G.Nodes.InDegreeCentrality = indegree_centrality;
G.Nodes.OutDegreeCentrality = outdegree_centrality;

% Access the weights of the connections
weights = G.Edges.Weight;

% Display the graph
plot(G, 'EdgeLabel',G.Edges.Weight);

% Display the centrality measures
disp(G.Nodes);

% Sort the nodes by centrality in descending order
[~, idx] = sort(G.Nodes.InDegreeCentrality, 'descend');

% Initialize the list with the most central node
list = idx(1);

% Get the adjacency matrix of the graph
A = adjacency(G);

% Iteratively add the next most central node that is connected to the list
for i = 2:length(idx)
    % Check if the node is connected to any node in the list
    isConnected = false;
    for j = 1:length(list)
        if A(idx(i), list(j))
            isConnected = true;
            break;
        end
    end
    
    % If the node is connected, add it to the list
    if isConnected
        list = [list; idx(i)];
    end
end

locations_names = locations(list);

% Display the list
disp(locations_names);

