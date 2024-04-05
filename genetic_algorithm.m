clear all

%Creating the variables
switch_num = 5; % 0<x<152
gen_size = 50; % 2<x
gen_num = 50;
hydroports_list = [2, 3];
changenum = max(2.*ceil(gen_size/20), 2);
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
    crosslist = randsample(2*changenum, changenum);
    crosslist = reshape(crosslist, [2, changenum/2]);
    for i = 1:changenum/2
        first = crosslist(1, i);
        second = crosslist(2, i);
        tempa = generation(first, :);
        tempb = generation(second, :);
        difs = tempa - tempb;
        plus = find(difs == 1);
        minus = find(difs == -1);
        indexnum = min(ceil(switch_num/2), length(plus));
        if indexnum > 0
            if length(plus) > 1
                switchinds = [randsample(plus, indexnum), randsample(minus, indexnum)];
            else
                switchinds = [plus, minus];
            end

            for j = switchinds
                a = generation(first, j);
                tempa(j) = generation(second, j);
                tempb(j) = a;
            end
        end

        if genetic_eval(route_graph, init_eval, tempa) > genetic_eval(route_graph, init_eval, generation(first, :))
            generation(first, :) = tempa;
        end

        if genetic_eval(route_graph, init_eval, tempb) > genetic_eval(route_graph, init_eval, generation(second, :))
            generation(second, :) = tempb;
        end
    end
    
    %Reordering and mutating
    for i = 1:gen_size
        eval(i) = genetic_eval(route_graph, init_eval, generation(i, :));
    end
    [generation, eval] = reorder_generation(generation, eval);
    
    mutlist = randsample((2*changenum + 1):gen_size, 2*changenum);
    for i = mutlist
        zeroinds = find(generation(i, :) == 0);
        oneinds = find(generation(i, :) == 1);
        indexnum = min(length(oneinds), ceil(switch_num/2));

        if length(oneinds) == 1
            switchinds = [oneinds, randsample(zeroinds, 1)];
        else
            switchinds = [randsample(zeroinds, indexnum), randsample(oneinds, indexnum)];
        end
        
        generation(i, switchinds) = mod(generation(i, switchinds) + 1, 2);
    end

    %Reordering and replacing
    for i = 1:gen_size
        eval(i) = genetic_eval(route_graph, init_eval, generation(i, :));
    end
    [generation, eval] = reorder_generation(generation, eval);
    
    replist = randsample((2*changenum + 1):gen_size, 2*changenum);
    for i = replist
        generation(i, :) = new_solution(unshuffled);
    end

    
    %Final reordering
    for i = 1:gen_size
        eval(i) = genetic_eval(route_graph, init_eval, generation(i, :));
    end
    [generation, eval] = reorder_generation(generation, eval);

    %Increasing the iteration
    g = g+1;
end

%Final reordering
for i = 1:gen_size
    eval(i) = genetic_eval(route_graph, init_eval, generation(i, :));
end
[generation, eval] = reorder_generation(generation, eval);

%Choosing best solution
validity_check = sum(sum(generation, 2) - (2*length(hydroports_list) + switch_num)) %Should equal to zero
airports_converted = find(generation(1, :) == 1)
total_saving = eval(1)
percent_saving = 100*eval(1)/init_eval