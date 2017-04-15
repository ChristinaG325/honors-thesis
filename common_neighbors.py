"""
File: common_neighbors.py
-------------------

Authors: Christina Gilbert
Common neighbors vs c
"""
import numpy as np
from collections import defaultdict
from itertools import combinations
import time
import pdb
import csv

OUTFILE = "common_neighbors_outfile.csv"
MATRIX_DATA_TYPE = np.int8

NULL_SENTINEL = -1
DATA_TYPE_MAX = np.iinfo(MATRIX_DATA_TYPE).max
DATA_FILES = ['p2p-Gnutella31.txt',
              'ca-GrQc.txt',
              'ca-HepTh.txt',
              'facebook.txt',
              'wiki-Vote.txt',
              'ca-CondMat.txt',
              'ca-HepPh.txt',
              'email-Enron.txt']

##### GRAPH INITALIZATION #####


def create_graph(filename):
    """
    Initializes graph from data file which maps each node to its set of neighbors.
    We consider all graphs as undericted, all relationships are symmetrical. If
    there is an edge between nodes 1 and 2, then 2 will be in 1's neighbor set,
    and 1 will be in 2's neighbors set.

    @param string filename     name of file to create graph from
    @return dict(int, set)     dict mapping nodes to set of neighbors
    """

    graph = defaultdict(set)

    with open(filename, 'r') as f:

        tuples = [(int(line.split()[0]), int(line.split()[1]))
                  for line in f if line[0] != '#']

        for tup in tuples:
            graph[tup[0]].add(tup[1])
            graph[tup[1]].add(tup[0])

        f.close()

    return graph


##### MATRIX CONSTRUCTION #####


def fill_connected_nodes_in_matrix(graph, matrix, matrix_len):
    """
    Constructs a (symmetric) numpy matrix where matrix[i][j] is the
    number of common neighbors shared by i and j. Connected nodes
    and self-loops (matrix diagonal) are marked with NULL_SENTINEL

    @param dict(int, set) graph         dict mapping nodes to set of neighbors
    @paran n_nodes int                  number of nodes in graph

    @return np.matrix matrix            matrix mapping number of common neighbors
                                        shared by nodes
    """
    for i in range(matrix_len):
        matrix[i][i] = NULL_SENTINEL

    for node in graph.keys():
        for connected_node in graph[node]:
            matrix[node][connected_node] = NULL_SENTINEL


def create_matrix(graph, n_nodes):
    """
    Constructs a (symmetric) numpy matrix where matrix[i][j] is the
    number of common neighbors shared by i and j. Connected nodes
    and self-loops are marked with NULL_SENTINEL

    @param dict(int, set) graph         dict mapping nodes to set of neighbors
    @param n_nodes int                  number of nodes in graph

    @return np.matrix matrix            matrix mapping number of common neighbors
                                        shared by nodes
    """
    # the snap datasets are 1-indexed, so the matrix is 1-indexed as well
    matrix_shape = (n_nodes + 1, n_nodes + 1)
    # WARNING uint16 stores values from -32768 to 32767, on very large graphs this
    # may be insufficient
    matrix = np.zeros(matrix_shape, dtype=MATRIX_DATA_TYPE)

    neighbors_sets = graph.values()

    for neighbor_set in neighbors_sets:
        neighbor_pairs = combinations(neighbor_set, 2)

        for pair in neighbor_pairs:
            matrix[pair[0], pair[1]] += 1
            matrix[pair[1], pair[0]] += 1

    fill_connected_nodes_in_matrix(graph, matrix, n_nodes + 1)
    return matrix

def find_max_c(graph, n_nodes):
    """
    Find the maximum value of c in an array
    """
    max = 0

    for i in range(n_nodes):
        for j in range(i):
            if graph[i][j] > max:
                max = graph[i][j]

    return max

def count_c(graph, n_nodes):
    """
    Given a matrix where graph[i][j] is the number of common neighbors between two nodes i and j
    For each value x, 1 through c, where c is the max number of common neighbors 
    for a non-adjacent pair, the y-value is the number of non-adjacent pairs 
    with exactly x common neighbors
    """
    #frequency = defaultdict(int)
    max_c = find_max_c(graph, n_nodes)
    frequencies = [0] * (max_c + 1)

    for i in range(n_nodes):
        for j in range(i):
            if graph[i][j] >= 0:
                frequencies[graph[i][j]] += 1

    return frequencies

def write_to_file(filename, pair_counts):

    with open(OUTFILE, 'at') as csvfile:
        csvfile.write(filename + '\n')

        closurewriter = csv.writer(csvfile, dialect='excel', delimiter=',', 
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)

        closurewriter.writerow(pair_counts)
        csvfile.write('\n')
        csvfile.close()

if __name__ == '__main__':
    """
    For each value 1 through c, where c is the max number of common neighbors for a non-adjacent pair,
    the y-value is the number of non-adjacent pairs with exactly x common neighbors
    """

    for filename in DATA_FILES:

        print(filename + ": initializing ...")
        graph = create_graph('data2/' + filename)
        n_nodes = np.amax(list(graph.keys()))
        print(n_nodes)
        print(filename + ": initialization complete")

        #Matrix Construction

        matrix_start = time.time()
        print(filename + ": constructing matrix ...")
        matrix = create_matrix(graph, n_nodes)
        matrix_end = time.time()
        print(filename + ": matrix constructed")
        print("Time elapsed: " + str(matrix_end - matrix_start))

        counting_start = time.time()
        print(filename + ": countaing pairs ...")
        pair_counts = count_c(matrix, n_nodes)
        print(filename + ": countaing pairs completed")
        counting_end = time.time()
        print("Time elapsed: " + str(counting_end - counting_start))

        print pair_counts
        write_to_file(filename, pair_counts)


