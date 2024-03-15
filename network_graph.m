clear all

%Set as mass of carbon per nmi per flight and carbon total per takeoff and
%landing per flight
carbonrate = 1;
carbontakeoff = 0;
carbonlanding = 0;

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
    carbon = func_carbon_routes(distance, count, carbonrate, carbontakeoff, carbonlanding)
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
km_to_nmi = 0.539957;
route_graph(:, :, 1) = route_graph(:, :, 1)*km_to_nmi;

%ATL carbon test
func_carbon_port(1, route_graph)