function [out] = func_carbon_routes(distance, count, rate, takeoff, landing)
%Calculates carbon per route
out = count*(takeoff + landing + (distance*rate));
end