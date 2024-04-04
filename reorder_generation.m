function [gen, eval] = reorder_generation(gen, eval)
[eval, order] = sort(eval, 'descend');
gen = gen(order, :);
end