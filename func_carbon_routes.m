function [out] = func_carbon_routes(distance, count)
%Calculates carbon per route
taxi_out = 450;
takeoff = 150;
climb = 400;
landing = 300;
taxi_in = 200;
rate = 17.05; %carbon emissions per nmi
out = count*(taxi_out + takeoff + climb + landing + taxi_in + (distance*rate));
end
