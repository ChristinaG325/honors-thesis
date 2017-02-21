import pdb
from collections import defaultdict
from itertools import combinations
from functools import reduce
import time
import csv
import sys
import io

DATA_FILES = [
'ca-GrQc.txt',
'ca-HepTh.txt',
'p2p-Gnutella04.txt',
'p2p-Gnutella05.txt',
'p2p-Gnutella06.txt',
'p2p-Gnutella08.txt',
'p2p-Gnutella09.txt',
'facebook_combined.txt',
'wiki-Vote.txt',
'email-Enron.txt',
'soc-Epinions1.txt',
'twitter-combined.txt'
]

def create_graph(filename):
    """
    Initializes graph from data file.

    @param string filename     name of file to create graph from
    @return dict(int, set)     dict mapping nodes to set of nodes its connected to
    """

    with open(filename, 'r') as f:

        tuples = [(int(line.split()[0]), int(line.split()[1]))
                  for line in f if line[0] != '#']

        graph = defaultdict(set)
        for tup in tuples:
            graph[tup[0]].add(tup[1])
            graph[tup[1]].add(tup[0])

        return graph


def get_closures(graph, filename):
    """
    Counts closures of each size

    @param dict(int, set) graph             dict mapping nodes to set of nodes its connected to
    @param string filename                  name of file to create graph from
    
    @return dict(tuple, int) closures       dict mapping pairs of nodes with no edge to their count of mutual neighbors
    """

    closures = defaultdict(int)

    #edges is the set of all edges from each node

    for edges in graph.values():
        pairs = combinations(edges, 2)
        for pair in pairs:
            if pair[0] not in graph[pair[1]]:
            # if the pair is not connected (we only want to count each closure once)
                closures[pair] += 1

    return closures

def compute_iterations_to_fix_violations(filename):
    """
    Reads in graph, computes the number of iterations needed to fix closure violations, total number of added edges
    Writes results to outfile

    @param string filename      name of file to compute stats for
    """


    # graph is a dict from int (representing a node) to a set of ints (representing nodes)
    graph = create_graph(filename)

    closures = get_closures(graph, filename)
    max_closure = 0

    for c in closures.values():
        if c > max_closure:
            max_closure = c

    print(filename + " is " + str(max_closure) + "-closed")


if __name__ == '__main__':
    """
    Computes stats for each file in DATA_FILES
    """

    #TODO: in get_closures, check to make sure we don't need to add pairs in just one direction, or make sure it's consistent (eg combinations function always does lower, higher)
    #TODO: CHANGE RANGE IN COMPUTE ITERATIONS TO FIX VIOLATIONS FROM MAX-C - 3 to 0

    for filename in DATA_FILES:
        compute_iterations_to_fix_violations('data/' + filename)
