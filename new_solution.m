function in = new_solution(in)
%Shuffles the input vector into a new solution, ignoring 2s
non_twos = find(in < 2);
shuffled = non_twos(randperm(length(non_twos)));
in(non_twos) = in(shuffled);
end