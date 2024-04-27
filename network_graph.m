clear all

%Set as mass of carbon per nmi per flight and carbon total per takeoff and
%landing per flight
carbonrate = 17.05;
carbontakeoff = 1000;
carbonlanding = 500;

%Importing airport data
portdata = readtable("first_network.csv");
portnames = portdata.iata;
coordinates = [portdata.latitude, portdata.longitude];

%Is each airport a hydrogen airport or no?
hydroports = zeros(303, 1);

%How much carbon in total are thes airports using?
carbonports = zeros(303, 1);

%Importing route data
route_data = readtable("airportdatatable.txt", Delimiter=",");
fromnames = route_data.from_code;
tonames = route_data.to_code;
flightdistances = route_data.flightdistance;

%Creating the Network
%Key: 1 = route distance, 2 = route frequency, 3 = route total carbon, 4 =
% route hydrogen status
%Route integer pairings for the graph - [from, to]
route_graph = zeros([303, 303, 4]);
route_pairs = zeros([5337, 2]);
route_distances = zeros([5337, 1]);
route_counts = zeros([5337, 1]);
for i = 1:height(route_data)
    route_pairs(i, :) = [find(matches(portnames, fromnames(i))), find(matches(portnames, tonames(i)))];
    distance = sscanf(char(flightdistances(i)), "%d");
    if distance < 10
        distance = distance*1000 + sscanf(char(flightdistances(i)), strcat(string(distance), ",%d"));
    end
    count = route_data.count(i);
    carbon = func_carbon_routes(distance, count, carbonrate, carbontakeoff, carbonlanding);
    route_distances(i) = distance;
    route_counts(i) = count;
    route_graph(route_pairs(i, 1), route_pairs(i, 2), :) = [distance, count, carbon, 0];
end

%Checking for problematic routes
problem_routes = [];
problem_numbers = [];
for i = 1:303
    if route_graph(i, i, 1) ~= 0
        problem_numbers = [problem_numbers; find(matches(fromnames, portnames(i)) & route_distances == route_graph(i, i, 1))];
        problem_routes = [problem_routes; route_data(problem_numbers(end), :)];
    end
end


%Removing problematic routes from the data
fromnames(problem_numbers) = [];
tonames(problem_numbers) = [];
flightdistances(problem_numbers) = [];
route_distances(problem_numbers) = [];
route_pairs(problem_numbers, :) = [];
route_data(problem_numbers, :) = [];
route_counts(problem_numbers, :) = [];

for i = 1:303
    route_graph(i, i, :) = 0;
end

%Convert distance to nmi
mi_to_nmi = 0.868976;
route_graph(:, :, 1) = route_graph(:, :, 1)*mi_to_nmi;

%Centrality list - [port number, centrality]
portcarbon = zeros(303, 2);
for i = 1:303
    portcarbon(i, 2) = func_carbon_port(i, route_graph);
    portcarbon(i, 1) = i;
end


%Exporting the route carbon and route distance
writematrix(route_graph(:, :, 1), 'route_distance');
writematrix(route_graph(:, :, 2), 'route_frequency');
writematrix(route_graph(:, :, 3), 'route_carbon');

% %Carbon calc test
% i = findroute(1, 2, route_pairs);
% j = findroute(2, 1, route_pairs);
% func_carbon_routes(route_distances(i), route_counts(i), carbonrate, carbontakeoff, carbonlanding) + func_carbon_routes(route_distances(j), route_counts(j), carbonrate, carbontakeoff, carbonlanding)
% 
% %ATL carbon test
% func_carbon_port(1, route_graph)
% route_graph(1, 2, 4) = 1;
% route_graph(2, 1, 4) = 1;
% func_carbon_port(1, route_graph)