import pdb
from collections import defaultdict
from itertools import combinations
from functools import reduce
import time
import csv

OUTFILE = 'closures.csv'
DATA_FILES = [
'facebook_combined.txt', 
'email-Enron.txt', 
'com-amazon.ungraph.txt', 
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
        ##pdb.set_trace()
        for pair in pairs:
            # if the pair is connected (eg. forms a triangle)
            if pair[0] not in graph[pair[1]]:

                #only store closures in one direction, with smaller index first
                closure = (pair[1], pair[0]) if pair[1] < pair[0] else pair
                closures.add(closure)

    return closures



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

def write_stats_to_file(filename, triangles, wedges, closure_frequencies, elapsed):
    with open(OUTFILE, 'at', encoding='utf8') as csvfile:
        csvfile.write(filename + '\n')
        csvfile.write("Elapsed time: " + str(elapsed) + '\n')
        csvfile.write("Triangles: " + str(triangles))
        csvfile.write("Wedges: " + str(wedges))
        csvfile.write("Transitivity: " + str((triangles * 3)  / wedges))

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
            graph[closure[0]].add(closure[1])
            graph[closure[1]].add(closure[0])
            added_edges_this_it += 1
            added_edges += 1
        iteration += 1
        print("EDGES ADDED ON IT " + str(iteration) + ": " + str(added_edges_this_it))
        print("TOTAL ADDED EDGES: " + str(added_edges))
        closures = get_closures_no_freq(graph)
    

def compute_graph_stats(filename, outfile):
    """
    Reads in graph, computes transitivity, computes histogram for closures

    @param string filename      name of file to compute stats for
    """
    print("----------     " + filename + "     ----------")
    start = time.time()

    # graph is a dict from int (representing a node) to a set of ints (representing nodes)
    graph = create_graph(filename)

    #transitivity2(graph)

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

    write_stats_to_file(filename, triangles, wedges, closure_frequencies, elapsed)

    fill_closures(graph, closures)
    #fill_closures_no_freq(graph, closures)



if __name__ == '__main__':
    """
    Computes stats for each file in DATA_FILES
    """

    for filename in DATA_FILES:
        fill_closures_no_freq('data/' + filename, )
        #compute_graph_stats('data/' + filename)

