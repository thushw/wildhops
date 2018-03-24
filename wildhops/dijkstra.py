#!/usr/bin/env python

from operator import attrgetter

from wildhops.graph import Graph 

def removed(edges, edge):
    return [e for e in edges if not e == edge]

def shotest_paths(graph, from_label):
    """ Return shortest paths from <from_label> to all the vertices in the graph <graph>.
    Returns a list of tuples, where each tuple is of the form (to_label, distance)
    """

    print ('finding paths from {}'.format(from_label))
    completed = {from_label: 0} #distance to itself is zero
    print ('completed vertices {}'.format(completed))
    
    fv = graph.find_node(from_label)
    if not fv: #unconnected vertex
        return []

    unexplored_edges = fv.edges
    
    while unexplored_edges:
        print ('exploring edges: {}'.format(unexplored_edges))
        min_edge = min(unexplored_edges, key=attrgetter('weight'))
        print ('minimum edge {}'.format(min_edge))
        to_vertex = graph.find_node(min_edge.tv)
        print ('to vertex of the minimum edge {}'.format(to_vertex))
        completed[min_edge.tv] = min_edge.weight + completed[min_edge.fv]))
        print ('completed vertices {}'.format(completed))
        unexplored_edges = removed(unexplored_edges, min_edge) + to_vertex.edges

    return zip(completed.keys(), completed.values())


if __name__ == '__main__':
    g = Graph()
    
    g.add_edge('A','B',weight=7)
    g.add_edge('A','C',weight=5)
    g.add_edge('A','D',weight=4)
    g.add_edge('A','E',weight=2)

    g.add_edge('B','H',weight=2)
    g.add_edge('B','G',weight=4)

    g.add_edge('D','I',weight=3)
    
    g.add_edge('E','F',weight=1)

    g.add_edge('F','C',weight=2)
    g.add_edge('F','G',weight=3)

    print ('going to find shortest distance to each vertex from A')
    print (g)

    print ('...')
    print (shortest_paths(g, 'A'))
