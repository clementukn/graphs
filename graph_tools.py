"""
helpers for dealing with graphs
"""

import random
import dpa_trial

EX_GRAPH0 = {0: set([1, 2]), 
             1: set([]), 
             2: set([])}

EX_GRAPH1 = {0: set([1, 4, 5]), 
             1: set([2, 6]), 
             2: set([3]), 
             3: set([0]),
             4: set([1]), 
             5: set([2]), 
             6: set([])}

EX_GRAPH2 = {0: set([1, 4, 5]), 
             1: set([2, 6]), 
             2: set([3, 7]), 
             3: set([7]),
             4: set([1]), 
             5: set([2]), 
             6: set([]), 
             7: set([3]), 
             8: set([1, 2]), 
             9: set([0, 4, 5, 6, 7, 3])}


def make_complete_graph(num_nodes):
    """ 
    Return a dictionary representing a graph whith num_nodes 
    having all possible edges
    """
    graph = {}

    for node in range(num_nodes):
        graph[node] = set()
        for neighbor in range(num_nodes):
            if neighbor == node:
                continue
            else:
                graph[node].add(neighbor)
    return graph


def compute_in_degrees(digraph):
    """
    Return a dictionary which keys are the nodes in the directed
    graph and the values represent the edges to that node
    """
    # init result with all nodes in digraph
    in_degrees = {}
    for node in digraph.keys():
        in_degrees[node] =  0
        
    for neighbors in digraph.values():
        for neighbor in neighbors:
            in_degrees[neighbor] += 1
    return in_degrees
        
    
def in_degree_distribution(digraph):
    """
    Return the distribution of in_degree of digraph represented
    as a dictionary
    """
    in_degrees = compute_in_degrees(digraph)
    in_degrees_distrib = {}
    for dummy_node, distrib in in_degrees.items():
        nodes_count = in_degrees_distrib.get(distrib, 0)
        in_degrees_distrib[distrib] = nodes_count + 1
    return in_degrees_distrib
        

def normalize_distribution(distrib):
    """
    Normalize a given distribution so that the sum of all
    the values gives 1
    """
    total_values = sum(distrib.values())
    norm_distrib = {}
    for key, val in distrib.items():
        norm_distrib[key] = float(val) / total_values
    return norm_distrib


def ER(nbr_nodes, prob):
    """
    Create a random graph with nbr_nodes where each pair (i, j) has
    probability prob to be added
    """
    graph = {}
    debug_degrees = 0
    for node in range(nbr_nodes):
        debug_degrees = 0
        graph[node] = set()
        for neighbor in range(nbr_nodes):
            if node == neighbor:
                continue
            a = random.random()
            if a < prob:
                graph[node].add(neighbor)
                debug_degrees += 1
    return graph


def DPA_beta(nodes, nodes_connections):
    """
    Create a random graph by first creating a complete graph 
    and then add random connections
    """
    if nodes_connections > nodes or nodes_connections < 1:
        return
    
    graph = make_complete_graph(nodes_connections)
    
    for id_node in range(nodes_connections, nodes):
        in_degree_nodes = compute_in_degrees(graph)
        totindef = sum(in_degree_nodes)
        
        # randomly choose nodes_connections nodes
        count = 0
        idx_node = 0
        # use a set to avoid duplicate node connections
        connections = set()
        while count < nodes_connections:
            rdm_nbr = random.random()
            # compute the probability of adding node idx_node
            prob =  float(in_degree_nodes[idx_node] + 1) / (totindef + len(graph))
            if rdm_nbr < prob:
                connections.add(idx_node)
                count += 1
            
            # whether the node has been added or not we check the next one
            idx_node += 1
            if idx_node >= len(graph):
                idx_node = 0
    
        # add the node to the graphs and connect it to the randomly 
        # selected nodes
        graph[id_node] = connections
    
    return graph


def DPA(nodes, nodes_connections):
    """
    Create a random graph by first creating a complete graph 
    and then add random connections
    """
    if nodes_connections > nodes or nodes_connections < 1:
        return
    
    graph = make_complete_graph(nodes_connections)
    dpa = dpa_trial.DPATrial(nodes_connections)
    
    for id_node in range(nodes_connections, nodes):
        connections = dpa.run_trial(nodes_connections)
        # add the node to the graphs and connect it to the randomly 
        # selected nodes
        graph[id_node] = connections
    
    return graph
        
        
def test():
    """
    test different methods
    """
    # test make_complete_graph
#    print make_complete_graph(-2)
#    print make_complete_graph(0)
#    print make_complete_graph(4)
    
    # test compute_in_degrees
    print compute_in_degrees(EX_GRAPH0)
    print compute_in_degrees(EX_GRAPH1)
    print compute_in_degrees(make_complete_graph(4))
    
    # test in_degree_distribution
    print "degree distribution : "
    print in_degree_distribution(EX_GRAPH0)
    print in_degree_distribution(EX_GRAPH1)
    print in_degree_distribution(make_complete_graph(4))
    
    # test normalize_distribution
    print normalize_distribution(in_degree_distribution(EX_GRAPH0))
    print normalize_distribution(in_degree_distribution(EX_GRAPH1))
    print normalize_distribution(in_degree_distribution(make_complete_graph(4)))
    
    # test ER
    print ER(5, 0)
    print ER(5, 1)
    print ER(5, 0.5)
    
    
    # test DPA
    print "-- DPA -- "
    print DPA(5, 2)
    print DPA(5, 1)
    print DPA(20, 2)
    print DPA(27770, 12)

#test()