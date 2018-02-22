import networkx as nx
import collections

def partition_statistics(partition, graph, weight=None):
    '''
    Calculates statistics for each partition of a network.
    Treats the network as undirected.
    
    :param partition: dict {node: community}
    :param graph: networkx graph
    :return: statistics
    '''

    reverse_partition = collections.defaultdict(list)
    for n in partition:
        reverse_partition[partition[n]].append(n)

    statistics = {comm: {} for comm in reverse_partition}
    for c in reverse_partition:
        subgraph = graph.subgraph(reverse_partition[c])
        statistics[c]['size'] = nx.number_of_nodes(subgraph)
        statistics[c]['total_degree'] = sum(graph.degree(reverse_partition[c]).values())
        statistics[c]['internal_degree'] = nx.number_of_edges(subgraph)
        statistics[c]['average_internal_degree'] = statistics[c]['internal_degree'] / statistics[c]['size']
        statistics[c]['external_degree'] = statistics[c]['total_degree'] - statistics[c]['internal_degree']
        statistics[c]['average_external_degree'] = statistics[c]['external_degree'] / statistics[c]['size']
        statistics[c]['conductance'] = statistics[c]['external_degree'] / statistics[c]['total_degree']
        if weight is not None:
            statistics[c]['total_strength'] = sum(graph.degree(reverse_partition[c], weight).values())
            statistics[c]['internal_strength'] = sum(nx.get_edge_attributes(subgraph, weight).values())
            statistics[c]['average_internal_strength'] = statistics[c]['internal_strength'] / statistics[c]['size']
            statistics[c]['external_strength'] = statistics[c]['total_strength'] - statistics[c]['internal_strength']
            statistics[c]['average_external_strength'] = statistics[c]['external_strength'] / statistics[c]['size']
            statistics[c]['weighted_conductance'] = statistics[c]['external_strength'] / statistics[c]['total_strength']
    return statistics