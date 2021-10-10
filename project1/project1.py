from os import kill, read
import sys

import networkx
import numpy as np
import pandas as pd
from file_handling import read_from_csv
from graph_operations import *
from bayesian_scoring import * 

from optimization import local_search


def write_gph(dag, idx2names, filename):
    with open(filename, 'w+') as f:
        for edge in dag.edges():
            f.write("{}, {}\n".format(idx2names[edge[0]], idx2names[edge[1]]))



def compute(infile, outfile):
    # WRITE YOUR CODE HERE
    # FEEL FREE TO CHANGE ANYTHING ANYWHERE IN THE CODE
    # THIS INCLUDES CHANGING THE FUNCTION NAMES, MAKING THE CODE MODULAR, BASICALLY ANYTHING
    df = read_from_csv(infile)
    print(df.info())
    idx2names = {i: df.columns[i] for i in range(len(df.columns))}
    nodes = np.arange(len(df.columns))

    graph = create_unconnected_graph(nodes)
    #draw_graph(graph, idx2names)
    #write_gph(graph, idx2names=idx2names, filename=outfile)

    M = calculate_M(graph=graph, df=df)
    score = bayesian_score(graph, M)
    print(score)

    best_graph, opt_score = local_search(graph, df)
    print(opt_score)
    draw_graph(best_graph, idx2names)
    


def main():
    if len(sys.argv) != 3:
        inputfilename = "data/small.csv"
        outputfilename = "data/output/small.gph"
        #raise Exception("usage: python project1.py <infile>.csv <outfile>.gph")
    else:
        inputfilename = sys.argv[1]
        outputfilename = sys.argv[2]
    compute(inputfilename, outputfilename)


if __name__ == '__main__':
    main()
