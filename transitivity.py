import pdb
from collections import defaultdict
from itertools import combinations
from functools import reduce
import time
import csv

OUTFILE = 'closures3.csv'
DATA_FILES = [
'com-youtube.ungraph.txt', 
'soc-Epinions1.txt', 
'twitter_combined.txt', 
'wiki-Vote.txt'
]

#DATA_FILES = ['facebook_combined.txt', 'test2.txt',  'email-Enron.txt',  'com-youtube.ungraph.txt', 'com-amazon.ungraph.txt', 'twitter_combined.txt']
#'soc-Epinions1.txt', 

# def transitivity2(graph):
#     nodes = graph.keys()
#     print("CREATE COMBOS")
#     triples = combinations(nodes, 3)
#     print("COMBOS CREATED")


#     triangles = 0
#     wedges = 0

#     i = 0

#     for triple in triples:
#         i += 1
#         if i % 100000000 == 0:
#             print(i)

#         edge1 = triple[0] in graph[triple[1]]
#         edge2 = triple[1] in graph[triple[2]]
#         edge3 = triple[2] in graph[triple[0]]


#         if edge1 and edge2 and edge3:
#             triangles += 1
#         if edge1 and edge2:
#             wedges += 1
#         if edge2 and edge3:
#             wedges += 1
#         if edge3 and edge1:
#             wedges +=1

#     pdb.set_trace()
#     print("TEST TRIANGLES: " + str(triangles))
#     print("TEST WEDGES: " + str(wedges))
#     print("TEST TRANSITIVITY: " + str(triangles*3/wedges))

def count_edges(graph):
    edges = 0
    for key in graph.keys():
        edges += len(graph[key])

    return edges/2

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

    @param dict(int, set) graph             dict mapping nodes to set of nodes its connected to
    @param string filename                  name of file to create graph from
    
    @return dict(tuple, int) closures       dict mapping pairs of nodes with no edge to their count of mutual neighbors
    @return int triangles                   count triangles found on graph (each triangle is triple counted), so we divide by 3
    @return int wedges                      count wedges found on graph
    @return int n_nodes                     total nodes in graph
    """
    print(filename + ": counting closures ...")
    triangles = 0
    wedges = 0


    acc_sum = 0

    closures = defaultdict(int)

    #edges is the set of all edges from each node

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
    print('\n' + "*****************************")
    print("***      GRAPH STATS      ***")
    print("*****************************" + '\n')
    print("Nodes: " + str(len(graph.keys())))
    print("Triangles: " + str(triangles))
    print("Wedges: " + str(wedges))
    print("Transitivity: " + str((triangles * 3)  / wedges))
    #print(closure_frequencies)

def write_stats_to_file(filename, nodes, edges, triangles, wedges, closure_frequencies, elapsed):
    with open(OUTFILE, 'at', encoding='utf8') as csvfile:
        csvfile.write(filename + '\n')
        csvfile.write("Elapsed time: " + str(elapsed) + '\n')
        csvfile.write("Nodes: " + str(nodes) + '\n')
        csvfile.write("Edges: " + str(edges) + '\n')
        csvfile.write("Triangles: " + str(triangles) + '\n')
        csvfile.write("Wedges: " + str(wedges) + '\n')
        csvfile.write("Transitivity: " + str((triangles * 3)  / wedges) + '\n')

        closurewriter = csv.writer(csvfile, dialect='excel', delimiter=',',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)
        closurewriter.writerow([key for key in closure_frequencies.keys()])
        closurewriter.writerow([value for value in closure_frequencies.values()])
        csvfile.write('\n')

#double check that dicts are passed by reference
def fill_closures(graph, closures):
    """
    @param dict(int, set) graph            dict mapping nodes to set of nodes its connected to
    @param dict(tuple, int) closures       dict mapping pairs of nodes with no edge to their count of mutual neighbors

    """
    added_edges = 0

    #while there are still closures
    while closures:
        for closure in closures.keys():
            graph[closure[0]].add(closure[1])
            graph[closure[1]].add(closure[0])
            added_edges += 1
        print("ADDED EDGES: " + str(added_edges))
        closures = get_closures(graph, filename)[0]
        closure_frequencies = reduce(lambda prev, c: prev.update({(c, prev.get(c, 0) + 1)}) or prev, closures.values(), {})
        print(closure_frequencies)

        #make and output new histogram


def compute_graph_stats(filename):
    """
    Reads in graph, computes transitivity, computes histogram for closures

    @param string filename      name of file to compute stats for
    """


    print("----------     " + filename + "     ----------")
    start = time.time()

    # graph is a dict from int (representing a node) to a set of ints (representing nodes)
    graph = create_graph(filename)

    closures, triangles, wedges, n_nodes = get_closures(graph, filename)

    # converts closure counts into frequency table


    print(filename + ": building frequency table ...")
    closure_frequencies = reduce(lambda prev, c: prev.update(
        {(c, prev.get(c, 0) + 1)}) or prev, closures.values(), {})
    print(filename + ": building frequency table complete")


    end = time.time()
    elapsed = end - start
    print(filename + ": processed in " + str(elapsed))

   
    print_stats(graph, triangles, wedges, closure_frequencies)
    print("----------------------------------------------------------\n\n\n\n")

    #paramaters: graph, nodes, edges, triangles, wedges, closure frequency counts, elapsed time
    write_stats_to_file(filename, len(graph.keys()), count_edges(graph), triangles, wedges, closure_frequencies, elapsed)



if __name__ == '__main__':
    """
    Computes stats for each file in DATA_FILES
    """

    for filename in DATA_FILES:
        compute_graph_stats('data/' + filename)

