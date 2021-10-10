from bayesian_scoring import bayesian_score, calculate_M
from networkx.algorithms.cycles import simple_cycles
from itertools import combinations
def local_search(init_graph, M, max_iter = 50, type="k2"):

    if type=="k2":
        return k2_search(init_graph, M)

def k2_search(init_graph, df):
    current_graph = init_graph
    M = calculate_M(current_graph, df)
    current_best_score = bayesian_score(init_graph, M)
    max_parents = 5
    
    for node in current_graph.nodes:

        current_neighbour_graph = current_graph.copy()
        for neighbour in current_graph.nodes:
            print("neighbour", neighbour)
            if (neighbour == node or #same node
                neighbour in list(current_graph.predecessors(node)) or # neighbour already parent
                len(list(current_graph.predecessors(node))) == max_parents #Node has maximum amount of parents.
                ): 
                print("skip")
                continue


            current_neighbour_graph.add_edge(neighbour, node)
            # remove cycled graphs
            if len(list(simple_cycles(current_neighbour_graph))):
                print('cycle')
                continue

            M = calculate_M(current_neighbour_graph, df)

            potential_next_score = bayesian_score(current_neighbour_graph, M)

            # if score is better
            if potential_next_score > current_best_score:
                current_graph = current_neighbour_graph
                current_best_score = potential_next_score
        

    return current_graph, current_best_score

def fake_k2_search(init_graph, M, max_iter, k_max):
    current_graph = init_graph
    current_best_score = bayesian_score(init_graph, M, k_max)
    max_parents = 5
    
    for iter in range(max_iter):
        pairs = list(combinations(range(len(list(current_graph.nodes))), 2))
        current_neighbour_graph = current_graph.copy()
        best_neighbour_graph = current_neighbour_graph.copy()
        local_optimum = True

        for pair in pairs:
            
            if (pair[0] == pair[1] or #same node
                pair[0] in list(current_graph.predecessors(pair[1]))  # neighbour already parent
                ): 
                continue


            current_neighbour_graph.add_edge(pair)

            # remove cycled graphs
            if len(current_neighbour_graph.simple_cycles()):
                continue
            potential_next_score = bayesian_score(current_neighbour_graph)


            # if score is better
            if potential_next_score > current_best_score:
                best_neighbour_graph = current_neighbour_graph
                current_best_score = potential_next_score
                local_optimum = False

        current_graph = best_neighbour_graph

        if local_optimum:
            return current_graph, current_best_score

        return best_neighbour_graph, current_best_score