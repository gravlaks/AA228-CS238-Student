import networkx as nx
import matplotlib.pyplot as plt

def create_unconnected_graph(nodes):

    # create a directed graph
    g = nx.DiGraph()

    for node in nodes:
        g.add_node(node,)
    return g

def draw_graph(g, labels=None):
    nx.draw(g, pos = nx.spring_layout(g),labels = labels, with_labels=True)
    #nx.draw_networkx_labels(g, pos=nx.spring_layout(g), labels = labels)
    plt.show()