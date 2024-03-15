function [out] = func_carbon_port(port_num, route_graph)
%Calculates total carbon of any route
carbon_h = route_graph(:, port_num, 3)
carbon_v = route_graph(port_num, :, 3)
hydrogen = ~[(route_graph(port_num, :, 4) > 0) & (route_graph(:, port_num, 4)' > 0)]
out = sum((carbon_h' + carbon_v) .* hydrogen)
end