#!/usr/bin/env python

import sys
from operator import attrgetter, itemgetter
import logging

from wildhops.graph import Graph 

logger = logging.getLogger(__name__)

def removed(distance, v):
    del distance[v]
    return distance

def update_state(distance, unknown, vertex):
    """ Update the distances from <vertex> to all its adjacent vertices.
    Remove <vertex> from <unknown> as the distance to it is now known.
    """

    for e in vertex.edges:
        dist_to_fv, vertices_to_fv = distance.get(e.fv, 0)
        new_dist = dist_to_fv + e.weight
        vertices_to_tv = vertices_to_fv + [e.fv]

        dist_to_tv, _ = distance.get(e.tv, (sys.maxsize, []))
        if new_dist < dist_to_tv:
            distance[e.tv] = (new_dist, vertices_to_tv)
            unknown[e.tv] = new_dist

    del unknown[vertex.value]
    return distance, unknown

def closest_vertex(distance):
    """ Return the tuple (vertex, distance) for the vertex with the minumum distance. """

    return min(distance.items(), key=itemgetter(1))

def shortest_paths(graph, from_label):
    """ Return shortest paths from <from_label> to all the vertices in the graph <graph>.
    Returns a list of tuples, where each tuple is of the form (to_label, (distance, [v1,v2..vk]))
    where v1 through vk are the vertices from <from_label>, inclusive to <to_lablel>, exclusive.
    """

    logger.debug('finding paths from {}'.format(from_label))

    #we keep track of 3 hashes to compute the shortest path

    #this holds the increasingly shorter distance to each vertex from <from_label>
    #as and when we find a better route, we update this. even after we find the shortest path
    #to a node, that node is *not* deleted from here. this is how we can differentiate between
    #a so far unexplored vertex from an explored (shortest path known) vertex.
    #the key is the vertex name, the value is a tuple where the first element is the distance
    #to the vertex, second is the list of vertices that leads up to it.
    distance = {from_label: (0, [])} #accumulate known min distance to each vertex

    #this holds the vertices where the shortest path is not known yet. the algorithm
    #keeps going until this is empty. whenever a vertex is determined to have the shortest path,
    #it gets removed from this hash.
    unknown = {from_label: 0} #vertices to which the distance is not known

    #this holds the vertices the distance to which are known. at the end, all vertices
    #connected to <from_label> should have an entry here. whenever a vertex is found to have the
    #shortest path, it is added here and removed from <unknown>
    completed = {from_label: 0} #distance to itself is zero

    fv = graph.find_node(from_label)
    if not fv: #unconnected vertex
        return []

    while unknown:
        logger.debug('exploring vertices: {}'.format(unknown))
        logger.debug('distances: {}'.format(distance))
        minv, dist = closest_vertex(unknown)

        logger.debug('minimum vertex:distance {}:{}'.format(minv, dist))
        min_vertex = graph.find_node(minv)
        logger.debug('minimum vertex {}'.format(min_vertex))
        completed[minv] = dist
        logger.debug('completed vertices {}'.format(completed))
        distance, unknown = update_state(distance, unknown, min_vertex)

    logger.debug('finished computing distances')
    logger.debug('distances:         {}'.format(distance))
    logger.debug('completed vertices {}'.format(completed))
    return zip(distance.keys(), distance.values())


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)

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


    logger.debug('going to find shortest distance to each vertex from A')
    logger.debug(g)

    logger.debug('...')
    logger.info(shortest_paths(g, 'A'))
