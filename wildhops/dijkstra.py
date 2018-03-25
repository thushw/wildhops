#!/usr/bin/env python

from operator import attrgetter, itemgetter

from wildhops.graph import Graph 

def removed(distance, v):
    del distance[v]
    return distance

def update_state(distance, unknown, vertex):
    """ Update the distances from <vertex> to all its adjacent vertices.
    Remove <vertex> from <unknown> as the distance to it is now known.
    """

    for e in vertex.edges:
        new_dist = distance.get(e.fv, 0) + e.weight
        if distance.get(e.tv, 0) == 0:
            distance[e.tv] = new_dist
            unknown[e.tv] = new_dist
        elif new_dist < distance.get(e.tv, 0):
            distance[e.tv] = new_dist
            unknown[e.tv] = new_dist

    del unknown[vertex.value]
    return distance, unknown

def closest_vertex(distance):
    """ Return the tuple (vertex, distance) for the vertex with the minumum distance. """

    return min(distance.items(), key=itemgetter(1))

def shortest_paths(graph, from_label):
    """ Return shortest paths from <from_label> to all the vertices in the graph <graph>.
    Returns a list of tuples, where each tuple is of the form (to_label, distance)
    """

    print ('finding paths from {}'.format(from_label))
    completed = {from_label: 0} #distance to itself is zero
    print ('completed vertices {}'.format(completed))

    distance = {from_label: 0} #accumulate known min distance to each vertex
    unknown = {from_label: 0} #vertices to which the distance is not known

    fv = graph.find_node(from_label)
    if not fv: #unconnected vertex
        return []

    distance, unknown = update_state(distance, unknown, fv)
    
    while unknown:
        print ('exploring vertices: {}'.format(unknown))
        print ('distances: {}'.format(distance))
        minv, dist = closest_vertex(unknown)

        print ('minimum vertex:distance {}:{}'.format(minv, dist))
        min_vertex = graph.find_node(minv)
        print ('minimum vertex {}'.format(min_vertex))
        completed[minv] = dist
        print ('completed vertices {}'.format(completed))
        distance, unknown = update_state(distance, unknown, min_vertex)

    return zip(completed.keys(), completed.values())


if __name__ == '__main__':
    g = Graph()
    
    g.add_edge('A','B',weight=8)
    g.add_edge('A','C',weight=5)
    g.add_edge('A','D',weight=4)
    g.add_edge('A','E',weight=2)

    g.add_edge('B','H',weight=2)
    g.add_edge('B','G',weight=4)

    g.add_edge('D','I',weight=3)
    
    g.add_edge('E','F',weight=1)

    g.add_edge('F','C',weight=1)
    g.add_edge('F','G',weight=3)

    g.add_edge('G','B',weight=1)
    g.add_edge('G','I',weight=2)

    print ('going to find shortest distance to each vertex from A')
    print (g)

    print ('...')
    print (shortest_paths(g, 'A'))
