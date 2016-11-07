import pdb
from collections import defaultdict
from itertools import combinations
from functools import reduce
import time
import csv

DATA_FILES = ['com-amazon.ungraph.txt', 'twitter_combined.txt']
#'soc-Epinions1.txt', 

def create_graph(filename):
    """
    Initializes graph from data file
    """

    print("Initializing " + filename + "...")
    with open(filename, 'r') as f:

        tuples = [(int(line.split()[0]), int(line.split()[1]))
                  for line in f if line[0] != '#']

        graph = defaultdict(set)
        for tup in tuples:
            graph[tup[0]].add(tup[1])
            graph[tup[1]].add(tup[0])

        print(filename + " initialization complete")
        return graph
    


def get_closures(graph):
    """
    Counts closures of each size
    """
    triangles = 0
    wedges = 0

    closures = defaultdict(int)

    for edges in graph.values():
        pairs = combinations(edges, 2)
        for pair in pairs:
            wedges += 1
            # if the pair is connected
            if pair[1] in graph.keys() and pair[0] in graph[pair[1]]:
                triangles += 1
            # if the pair is not connected
            elif pair[0] < pair[1]:
                closures[pair] += 1
    return (closures, triangles, wedges)

def compute_graph_stats(filename):
    """
    Reads in graph, computes transitivity, computes histogram for closures
    """
    start = time.time()

    # graph is a dict from int (representing a node) to a set of ints
    # (representing nodes)

    graph = create_graph(filename)
    closures, triangles, wedges = get_closures(graph)

    # converts closure counts into frequency table
    closure_frequencies = reduce(lambda prev, c: prev.update(
        {(c, prev.get(c, 0) + 1)}) or prev, closures.values(), {})

    end = time.time()
    elapsed = end - start

    print(len(graph.keys()))
    print("triangles x3: " + str(triangles))
    print("triangles: " + str(triangles / 3))
    print("wedges: " + str(wedges))
    print("transitivity: " + str(triangles / (3 * wedges)))
    print(closure_frequencies)

    with open('closures.csv', 'at', encoding='utf8') as csvfile:
        csvfile.write(filename + '\n')
        #csvfile.write(str(elapsed) + '\n')
        closurewriter = csv.writer(csvfile, dialect='excel', delimiter=',',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)
        closurewriter.writerow([key for key in closure_frequencies.keys()])
        closurewriter.writerow(
            [value for value in closure_frequencies.values()])

if __name__ == '__main__':
    """
    Computes stats for each file in DATA_FILES
    """

    for filename in DATA_FILES:
        compute_graph_stats('data/' + filename)

