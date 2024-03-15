function [out] = findnum(in, portnames)
%Finds the number of an airport
out = find(matches(portnames, in));
end