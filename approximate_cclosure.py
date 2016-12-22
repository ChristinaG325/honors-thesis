"""
File: approxmite_cclosure.py
-------------------

Authors: Christina Gilbert
Computes the value of c, where c is the lowest value for 
which a graph is approximately c-closed
"""
import numpy as np
from collections import defaultdict
from itertools import combinations
import time
import pdb

MATRIX_DATA_TYPE = np.int16

#NOTE if we change the sentinal value to be non-negative, need to update the
#remove_node code to ignore the "NULL" cells
NULL_SENTINEL = -500
DATA_TYPE_MAX = np.iinfo(MATRIX_DATA_TYPE).max
DATA_FILES = ['p2p-Gnutella09.txt']

#test.txt
#test2.txt
#facebook_combined.txt

#youtube

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

###function not currently in use .... ###
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


##### MAIN #####

def remove_node(node, matrix, matrix_len, graph):
    matrix[node, :] = NULL_SENTINEL
    matrix[:, node] = NULL_SENTINEL

    neighbor_set = graph[node]
    neighbor_pairs = combinations(neighbor_set, 2)

    #NOTE if we change the sentinal value to be non-negative, need to update this
    #code to ignore the "NULL" cells
    for pair in neighbor_pairs:
        # print("removing node " + str(node))
        # print(pair)
        if matrix[pair[0], pair[1]] != NULL_SENTINEL:
            matrix[pair[0], pair[1]] -= 1
            matrix[pair[1], pair[0]] -= 1
    #     print(matrix)
    # print("-- -- -- --")
    #-1s on its row, col in the matrix
    #in the graph, iterate over its pairs of neighbors, and decrement the closure count by 1

def compute_min(maxima):
    maxima_without_negative = [value if value != NULL_SENTINEL else DATA_TYPE_MAX for value in maxima]
    return np.amin(maxima_without_negative)

#matrix_len is the dimensions of the matrix, which is n_nodes + 1
def compute_c(graph, matrix, matrix_len):
    remaining_nodes = matrix_len - 1

    max_minimum = 0

    while(remaining_nodes > 0):


        #the size of the largest closure each node is a part of
        maxima = [np.amax(matrix[row]) for row in range(1, matrix_len)]

        #the c-value for the "best" node (TODO: May be a better way to do this, dont have internet now)
        
        #TODO -- verify this function works
        #TODO -- through this iterative process, store the maximum of the minimum values
        #that we remove on each iteration
        minimum = compute_min(maxima)
        if minimum > max_minimum:
            max_minimum = minimum
        #I am still not totally clear on what the termination condition is, but I think it's when we
        #remove all the nodes.

        # print("===============\n\n")
        # print("Matrix while " + str(remaining_nodes) + " remain")
        # print(matrix)
        print(minimum)
        # print("\n\n===============")

        #I think there is a problem with changes persisting in the matrix bewteen iterations of the while loop
        
        

        for i, value in enumerate(maxima):
            if value == minimum:
                remove_node(i + 1, matrix, matrix_len, graph)
                remaining_nodes -= 1

    print ("Max Minimum: "  + str(max_minimum))
    print ("The graph is approximately " + str(max_minimum + 1) + "-closed")

if __name__ == '__main__':
    """
    Computes the value of c, where c is the lowest
    value for which the graph is approximately c-closed
    """

    for filename in DATA_FILES:

        print(filename + ": initializing ...")
        graph = create_graph('data/' + filename)
        n_nodes = np.amax(list(graph.keys()))
        print(n_nodes)
        print(filename + ": initialization complete")


        matrix_start = time.time()
        print(filename + ": constructing matrix ...")
        matrix = create_matrix(graph, n_nodes)
        matrix_end = time.time()
        print(filename + ": matrix constructed")
        print("Time elapsed: " + str(matrix_end - matrix_start))
        print(matrix)
        print('\n')
        print('\n')


        compute_c(graph, matrix, n_nodes + 1)

        
    # build graph
    # build matrix
    # remove rows in matrix until c is found
