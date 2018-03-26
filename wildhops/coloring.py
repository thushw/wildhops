#!/usr/bin/env python

import sys
from operator import attrgetter, itemgetter
import logging

from wildhops.graph import Graph

logger = logging.getLogger(__name__)

def is_bipartite(graph):
    """ Return True iff the vertices can be colored with two colors
    such that no two directly connected vertices share the same color
    """

    vertex_colors = {}

    def complement(color):
        return (color + 1)%2

    def color_walk(vertex, color):
        cur_color = vertex_colors.get(vertex.value, None)
        if cur_color is None:
            vertex_colors[vertex.value] = color
            for e in vertex.edges:
                tv = graph.find_node(e.tv)
                if not color_walk(tv, complement(color)):
                    return False
            return True
        elif cur_color != color: #already colored the same as a parent
            return False
        else: #already colored
            return True

    #we have to color all the vertices by iterating through the nodes list as
    #the graph may have disconnected components. therefore, we should pick the
    #color the vertex is already colored in.
    return all (color_walk(node, vertex_colors.get(node.value, 0)) for node in graph.nodes)

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)

    g = Graph()

    g.add_edge('A','B')
    g.add_edge('A','C')
    g.add_edge('A','D')
    g.add_edge('A','E')

    g.add_edge('B','H')
    g.add_edge('B','G')

    logger.debug('is this graph bipartite?')
    logger.debug(g)

    logger.info(is_bipartite(g))
