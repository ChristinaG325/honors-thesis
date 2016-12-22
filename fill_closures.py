import pdb
from collections import defaultdict
from itertools import combinations
from functools import reduce
import time
import csv
from array import array


DATA_FILES = ['com-amazon.ungraph.txt']
#test2.txt'
#'email-Enron.txt'
#'facebook_combined.txt'

def graph_size(graph):
    values = 0
    for key in graph.keys():
        values += 1 + len(graph[key])

    return values

#fills closures but does not make keep count of the frequencies of any of the closures
def fill_closures_no_freq(filename):
    """
    @param dict(int, set) graph            dict mapping nodes to set of nodes its connected to
    @param set(tuple) closures             set of all tuples mapping with mutual friends that are not connected

    """
    graph = create_graph(filename)
    closures = get_closures_no_freq(graph)

    added_edges = 0
    iteration = 0

    #while there are still closures
    while closures:
        added_edges_this_it = 0
        for closure in closures:
            
            graph[closure[0]].append(closure[1])
            graph[closure[1]].append(closure[0])

            added_edges_this_it += 1
            added_edges += 1


            ########   MEMORY DEBUG CODE   ###########
            # if added_edges % 100000 == 0:
            #     print("GRAPH SIZE " + str(graph_size(graph)))
            ########   MEMORY DEBUG CODE   ###########

        iteration += 1

        print("EDGES ADDED ON IT " + str(iteration) + ": " + str(added_edges_this_it))
        print("TOTAL ADDED EDGES: " + str(added_edges))
        del closures
        closures = get_closures_no_freq(graph)

def create_graph(filename):
    """
    Initializes graph from data file.

    @param string filename     name of file to create graph from
    @return dict(int, set)     dict mapping nodes to set of nodes its connected to
    """

    print(filename + ": initializing ...")
    with open(filename, 'r') as f:

        tuples = [(int(line.split()[0]), int(line.split()[1]))
                  for line in f if line[0] != '#']

        graph = defaultdict(lambda: array('I'))
        for tup in tuples:

            graph[tup[0]].append(tup[1])
            graph[tup[1]].append(tup[0])

        print(filename + ": initialization complete")
        return graph


def get_closures_no_freq(graph):
    """
    Counts closures of each size

    @param dict(int, set) graph             dict mapping nodes to set of nodes its connected to
    
    @return set(tuple) closures       dict mapping pairs of nodes with no edge to their count of mutual neighbors
    """

    closures = set()

    #edges is the set of all edges from each node

    for edges in graph.values():
        pairs = combinations(edges, 2)

        for pair in pairs:
            # if the pair not is connected 
            if pair[0] not in graph[pair[1]]:
                #only store closures in one direction, with smaller index first
                closure = (pair[1], pair[0]) if pair[1] < pair[0] else pair
                closures.add(closure)

    return closures


if __name__ == '__main__':
    """
    Computes stats for each file in DATA_FILES
    """

    for filename in DATA_FILES:
        fill_closures_no_freq('data/' + filename)
