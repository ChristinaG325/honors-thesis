import numpy as np
from collections import defaultdict
from itertools import combinations

DATA_FILES = ['test.txt']

def create_graph(filename):
    """
    Initializes graph from data file.

    @param string filename     name of file to create graph from
    @return dict(int, set)     dict mapping nodes to set of nodes its connected to
    """

    #print(filename + ": initializing ...")
    with open(filename, 'r') as f:

        tuples = [(int(line.split()[0]), int(line.split()[1]))
                  for line in f if line[0] != '#']

        graph = defaultdict(set)
        for tup in tuples:
            graph[tup[0]].add(tup[1])
            graph[tup[1]].add(tup[0])

        #print(filename + ": initialization complete")
        return graph

def symmetrize_matrix(matrix, matrix_len):
    for i in range(matrix_len):
        for j in range(i):
            matrix[i][j] = matrix[j][i]

    return matrix


#TODO: look into null types for numpy matrix in python? Cant do it right
#now becuase no internet
def fill_connected_nodes_in_matrix(graph, matrix, matrix_len):
    for i in range(matrix_len):
        matrix[i][i] = -1

    for node in graph.keys():
        for connected_node in graph[node]:
            matrix[node][connected_node] = -1

def create_matrix(graph, n_nodes):

    #the snap datasets are 1-indexed, so the matrix is 1-indexed as well
    matrix_shape = (n_nodes + 1, n_nodes + 1)
    matrix = np.zeros(matrix_shape, dtype=np.int)
    #remember to handle the diagonal

    neighbors_sets = graph.values()

    for neighbor_set in neighbors_sets:
        neighbor_pairs = combinations(neighbor_set, 2)

        for pair in neighbor_pairs:
            ordered_pair = (pair[0], pair[1]) if pair[0] < pair[1] else (pair[1], pair[0])
            matrix[ordered_pair[0], ordered_pair[1]] += 1

    fill_connected_nodes_in_matrix(graph, matrix, n_nodes + 1)
    matrix = symmetrize_matrix(matrix, n_nodes + 1)
    return matrix



if __name__ == '__main__':
    """
    Computes the value of c, where c is the lowest
    value for which the graph is approximately c-closed
    """

    for filename in DATA_FILES:
        graph = create_graph('data/' + filename)
        matrix = create_matrix(graph, len(graph.keys()))
        print matrix 
    #build graph
    #build matrix
    #remove rows in matrix until c is found

