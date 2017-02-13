import pdb
from collections import defaultdict
from itertools import combinations
from functools import reduce
import time
import csv
import sys

OUTFILE = 'count_added_edges.csv'
DATA_FILES = [
'wiki-Vote.txt'
]

MAX_C = 50

def fill_closures_write_stats_to_file(filename, elapsed, c, edges_added_on_iteration, total_added_edges, n_iterations):
    with open(OUTFILE, 'at', encoding='utf8') as csvfile:
        csvfile.write(filename + '\n')


        closurewriter = csv.writer(csvfile, dialect='excel', delimiter=',',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)

        csvfile.write(["Elapsed time: "], elapsed])
        csvfile.write(["Total Added Edges", total_added_edges])
        csvfile.write("n iterations", n_iterations])

        closurewriter.writerow([i for i in range(n_iterations)])
        closurewriter.writerow(edges_added_on_iteration)
        csvfile.write('\n')


#TODO: WRITE THIS FUNCTION
def is_not_c_closed(c):
	"""
	@param c 			Value of c for which graph is c-closed

	@return bool 		TRUE if graph is not c-closed, FALSE otherwise
	"""
	return true


def fill_closures(graph, closures, c):
    """
    @param dict(int, set) graph            		dict mapping nodes to set of nodes its connected to
    @param dict(tuple, int) closures       		dict mapping pairs of nodes with no edge to their count of mutual neighbors
    @param c                               		minimum value of c for which we fill closures

    @return int[] edges_added_on_iteration		array of the number of edges added on each iteration, indexed from 0
    """
    edges_added_on_iteration = []

    iteration = 0

    #while there are still closures
    while is_not_c_closed(c):                               #TODO: WRITE A FUNCTION TO CHECK IF THIS SHOULD TERMINATE EG IF THERE EXIST CLOSURES WITH C>C
    	added_edges = 0
    	print("ITERATION: " + str(iteration))
    	iteration += 1
        for closure in closures.keys():
            if closures[closure] > c:                       #if the number of common nodes is greater than c, add an edge                                  
                graph[closure[0]].add(closure[1])
                graph[closure[1]].add(closure[0])
                added_edges += 1
        print("ADDED EDGES: " + str(added_edges))
        edges_added_on_iteration.append(added_edges)
        closures = get_closures(graph, filename)			#update closures

     return edges_added_on_iteration


def get_closures(graph, filename):
    """
    Counts closures of each size

    @param dict(int, set) graph             dict mapping nodes to set of nodes its connected to
    @param string filename                  name of file to create graph from
    
    @return dict(tuple, int) closures       dict mapping pairs of nodes with no edge to their count of mutual neighbors
    """
    print(filename + ": counting closures ...")

    closures = defaultdict(int)

    #edges is the set of all edges from each node

    for edges in graph.values():
        pairs = combinations(edges, 2)
        for pair in pairs:
            if pair[0] not in graph[pair[1]]:
            # if the pair is not connected (we only want to count each closure once)
                closures[pair] += 1
    print(filename + ": counting closures complete")

    return closures

def compute_iterations_to_fix_violations(filename):
    """
    Reads in graph, computes the number of iterations needed to fix closure violations, total number of added edges
    Writes results to outfile

    @param string filename      name of file to compute stats for
    """

        for c in range(MAX_C, MAX_C - 3, -1):
            print("----------     " + filename + "     ----------")
            print("----------     c-value:" + c + "     ----------")
            start = time.time()

            # graph is a dict from int (representing a node) to a set of ints (representing nodes)
            graph = create_graph(filename)

            closures = get_closures(graph, filename)

            #return value is an array of the number of edges added on each iteration
            edges_added_on_iteration = fill_closures(graph, closures, c)
            total_added_edges = sum(edges_added_on_iteration)
            n_iterations = len(edges_added_on_iteration)


            end = time.time()
            elapsed = end - start
            fill_closures_write_stats_to_file(filename, elapsed, c, edges_added_on_iteration, total_added_edges, n_iterations)
            print(filename + "on c: " +  c + ": processed in " + str(elapsed))
            print("n iterations: " + str(n_iterations))
            
           
            print("----------------------------------------------------------\n\n\n\n")




    #construct graph

    #iterative fill edges process

    #write to outfile


if __name__ == '__main__':
    """
    Computes stats for each file in DATA_FILES
    """

    #TODO: Write function that checks if graph is c-closed
    #TODO: in get_closures, check to make sure we don't need to add pairs in just one direction, or make sure it's consistent (eg combinations function always does lower, higher)
    #TODO: CHANGE RANGE IN COMPUTE ITERATIONS TO FIX VIOLATIONS FROM MAX-C - 3 to 0

    for filename in DATA_FILES:
        compute_iterations_to_fix_violations('data/' + filename)
