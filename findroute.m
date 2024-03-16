function [out] = findroute(from_num, to_num, route_pairs)
%Finds the number of an airport
out = [find((route_pairs(:, 1) == from_num) & (route_pairs(:, 2) == to_num))];
end