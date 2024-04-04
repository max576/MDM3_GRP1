function fitness = genetic_eval(route_graph, initial_carbon, solution)
%Finds the amount of carbon saved with solution

%Redefining the route_graph
len = length(solution);
hydroports = find(solution > 0);
onekports = zeros(len);
twokports = zeros(len);
for i = hydroports
    onekports(i, :) = route_graph(i, :, 1) <= 1000;
    onekports(:, i) = route_graph(:, i, 1) <= 1000;
    twokports(i, hydroports) = route_graph(i, hydroports, 1) <= 2000;
    twokports(hydroports, i) = route_graph(hydroports, i, 1) <= 2000;
end
route_graph(:, :, 4) = or(onekports, twokports);
total = sum(route_graph(:, :, 3).*~route_graph(:, :, 4), 'all');
fitness = initial_carbon - total;

end