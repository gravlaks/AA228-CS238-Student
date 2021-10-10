from scipy.special import loggamma
#from networkx import topological_sort
import numpy as np
from networkx.algorithms.dag import topological_sort


def get_j(parents, row, k_max):
    if not len(list(parents)):
        return 0
    return np.ravel_multi_index(np.array([list(parents), row[parents]]), dims = (len(list(parents)), k_max))

def calculate_M(graph, df):
    """
    Input: 
    graph: Networkx object, a DAG

    df: DataFrame containing all the sampled variables. 

    This function creates a 3-dimensional matrix M 

    i: per node
    j: instantiation of parents
    k: value that data takes


    """
    k_max = df.to_numpy().max()

    M = create_empty_M(graph, k_max)
    topo_sort = np.array(list((topological_sort(graph))))
    #Iterate over data samples: row by row
    for _, row in df.iterrows():
        # iterate over node in topological sort
        for node in topo_sort:
            i = node
            j = get_j(parents=graph.predecessors(node), row=row, k_max=k_max)
            k = row[node]

            M[i][j, k] += 1

    return M

def create_empty_M(graph, k_max):

    """
    Let M be an empty dictionary, containing 2D numpy arrays

    """
    M = {}
    for node in graph.nodes:
        parents = graph.predecessors(node)
        j_max = k_max**len(list(parents))
  

        M[node] = np.zeros(shape=(j_max+1, k_max+1))
    return M

def bayesian_score(graph, M):
    score = 0
    k_max = M[0].shape[1]
    ## Ask about this?
    alpha_i = 1 

    for node in graph.nodes:
        i = node
        for j in range(M[i].shape[0]):

            score += loggamma(k_max)
            score -= loggamma(k_max+np.sum(M[i][j]))
            score += np.sum(
                loggamma(alpha_i+M[i][j])
                #- loggamma(1) #this is equal to 0
            )

    return score
