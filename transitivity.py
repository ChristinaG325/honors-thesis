import pdb
from collections import defaultdict
from itertools import combinations
from functools import reduce
import time
import csv

DATA_FILES = ['facebook_combined.txt', 'test2.txt',  'email-Enron.txt',  'com-youtube.ungraph.txt', 'com-amazon.ungraph.txt', 'twitter_combined.txt']
#'soc-Epinions1.txt', 

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

        graph = defaultdict(set)
        for tup in tuples:
            graph[tup[0]].add(tup[1])
            graph[tup[1]].add(tup[0])

        print(filename + ": initialization complete")
        return graph
    


def get_closures(graph, filename):
    """
    Counts closures of each size

    @param dict(int, set)                   dict mapping nodes to set of nodes its connected to
    @param filename                         name of file to create graph from
    
    @return dict(tuple, int) closures       dict mapping pairs of nodes with no edge to their count of mutual neighbors
    @return int triangles                   count triangles found on graph (each triangle is triple counted), so we divide by 3
    @return int wedges                      count wedges found on graph
    @return int n_nodes                     total nodes in graph
    """
    print(filename + ": counting closures ...")
    triangles = 0
    wedges = 0

    closures = defaultdict(int)

    #edges is the set of all edges from each node


    print(len(graph.values()))
    print(len(graph.keys()))
    for edges in graph.values():

        pairs = combinations(edges, 2)
        ##pdb.set_trace()
        for pair in pairs:
            wedges += 1
            # if the pair is connected (eg. forms a triangle)
            if pair[0] in graph[pair[1]]:
#            if pair[1] in graph.keys() and pair[0] in graph[pair[1]]:
                triangles += 1
            # if the pair is not connected (we only want to count each closure once)
            else:
                closures[pair] += 1
    print(filename + ": counting closures complete")

    n_nodes = len(graph.keys())
    return (closures, triangles/3, wedges, n_nodes)

def print_stats(graph, triangles, wedges, closure_frequencies):
    print(len(graph.keys()))
    print("triangles: " + str(triangles))
    print("wedges: " + str(wedges))
    print("transitivity: " + str((triangles * 3)  / wedges))
    #print(closure_frequencies)

def transitivity2(graph):
    nodes = graph.keys()
    print("CREATE COMBOS")
    triples = combinations(nodes, 3)
    print("COMBOS CREATED")


    triangles = 0
    wedges = 0

    i = 0

    for triple in triples:
        i += 1
        if i % 100000000 == 0:
            print(i)

        edge1 = triple[0] in graph[triple[1]]
        edge2 = triple[1] in graph[triple[2]]
        edge3 = triple[2] in graph[triple[0]]


        if edge1 and edge2 and edge3:
            triangles += 1
        if edge1 and edge2:
            wedges += 1
        if edge2 and edge3:
            wedges += 1
        if edge3 and edge1:
            wedges +=1

    pdb.set_trace()
    print("TEST TRIANGLES: " + str(triangles))
    print("TEST WEDGES: " + str(wedges))
    print("TEST TRANSITIVITY: " + str(triangles*3/wedges))


def compute_graph_stats(filename):
    """
    Reads in graph, computes transitivity, computes histogram for closures
    """
    start = time.time()

    # graph is a dict from int (representing a node) to a set of ints
    # (representing nodes)

    graph = create_graph(filename)

    transitivity2(graph)

    closures, triangles, wedges, n_nodes = get_closures(graph, filename)

    # converts closure counts into frequency table
    print(filename + ": building frequency table ...")
    closure_frequencies = reduce(lambda prev, c: prev.update(
        {(c, prev.get(c, 0) + 1)}) or prev, closures.values(), {})
    print(filename + ": building frequency table complete")

    end = time.time()
    elapsed = end - start

    print_stats(graph, triangles, wedges, closure_frequencies)

    pdb.set_trace()

    with open('closures.csv', 'at', encoding='utf8') as csvfile:
        csvfile.write(filename + '\n')
        #csvfile.write(str(elapsed) + '\n')
        closurewriter = csv.writer(csvfile, dialect='excel', delimiter=',',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)
        closurewriter.writerow([key for key in closure_frequencies.keys()])
        closurewriter.writerow(
            [value for value in closure_frequencies.values()])

    print(filename + ": processed in " + str(elapsed))


if __name__ == '__main__':
    """
    Computes stats for each file in DATA_FILES
    """

    for filename in DATA_FILES:
        compute_graph_stats('data/' + filename)

