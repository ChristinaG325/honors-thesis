"""
File: approxmite_cclosure.py
-------------------

Authors: Christina Gilbert
Group: Christina Gilbert, Eric Ehizokhale, Jake Rachleff
Computes the value of c, where c is the lowest value for 
which a graph is approximately c-closed
"""
import numpy as np
from collections import defaultdict
from itertools import combinations

MATRIX_DATA_TYPE = np.uint16
NULL_SENTINEL = np.iinfo(np.uint16).max
DATA_FILES = ['test.txt']


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


def symmetrize_matrix(matrix, matrix_len):
    """
    Copies values from the top half of a triangluar matrix into the lower half

    @param np.matrix matrix             matrix mapping number of common neighbors
                                        shared by nodes
    @param matrix_len int               number of rows, cols in square matrix
    """
    for i in range(matrix_len):
        for j in range(i):
            matrix[i][j] = matrix[j][i]


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
    @paran n_nodes int                  number of nodes in graph

    @return np.matrix matrix            matrix mapping number of common neighbors
                                        shared by nodes
    """
    # the snap datasets are 1-indexed, so the matrix is 1-indexed as well
    matrix_shape = (n_nodes + 1, n_nodes + 1)
    # WARNING uint16 stores values from 0 to 65535, on very large graphs this
    # may be insufficient
    matrix = np.zeros(matrix_shape, dtype=MATRIX_DATA_TYPE)

    neighbors_sets = graph.values()

    for neighbor_set in neighbors_sets:
        neighbor_pairs = combinations(neighbor_set, 2)

        for pair in neighbor_pairs:
            ordered_pair = (
                pair[0], pair[1]) if pair[0] < pair[1] else (
                pair[1], pair[0])
            matrix[ordered_pair[0], ordered_pair[1]] += 1

    fill_connected_nodes_in_matrix(graph, matrix, n_nodes + 1)
    symmetrize_matrix(matrix, n_nodes + 1)
    return matrix


##### MAIN #####


if __name__ == '__main__':
    """
    Computes the value of c, where c is the lowest
    value for which the graph is approximately c-closed
    """

    for filename in DATA_FILES:

        print(filename + ": initializing ...")
        graph = create_graph('data/' + filename)
        print(filename + ": initialization complete")

        print(filename + ": constructing matrix ...")
        matrix = create_matrix(graph, len(graph.keys()))
        print(filename + ": matrix constructed ...")

        print(matrix)
    # build graph
    # build matrix
    # remove rows in matrix until c is found
