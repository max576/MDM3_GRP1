clear all

%Creating the variables
switch_num = 5;
gen_size = 50;
gen_num = 50;
hydroports_list = [2, 3];
changenum = max(2.*ceil(gensize/20), 2);
route_graph = zeros(303, 303, 4);
route_graph(:, :, 1) = readmatrix('route_distance.txt');
route_graph(:, :, 2) = readmatrix('route_frequency.txt');
route_graph(:, :, 3) = readmatrix('route_carbon.txt');

%Creating unshuffled solutions
initial_hydroports = zeros(303, 1);
initial_hydroports(hydroports_list) = 2;
unshuffled = initial_hydroports;
initial_newports = find(initial_hydroports < 2);
unshuffled(initial_newports(1:switch_num)) = 1;

%Evaluating initial carbon
init_eval = -1.*genetic_eval(route_graph, 0, initial_hydroports);


%Creating and evaluating generation 0
generation = zeros(gen_size, 303);
eval = zeros(gen_size, 1);
for i = 1:gen_size
    generation(i, :) = new_solution(unshuffled);
    eval(i) = genetic_eval(route_graph, init_eval, generation(i, :));
end
[generation, eval] = reorder_generation(generation, eval);

%Starting the loop
g = 0;
while g < gen_num 

    %Conducting crossover
    for i = 1:changenum/2
        first = i;
        second = changenum + 1 - i;
        onelocs = [find(generation(first, :) == 1), find(generation(second, :) == 1)];
    end

    %Reordering and mutating


    %Reordering and replacing

    
    %Final reordering


    %Increasing the iteration
    g = g+1;
end

%Final reordering
[generation, eval] = reorder_generation(generation, eval);

%Choosing best solution
generation(1, :)
eval(1)