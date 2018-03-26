#!/usr/bin/env python

import unittest
from operator import itemgetter

from wildhops.graph import Graph, GraphNode
from wildhops.coloring import is_bipartite

class TestColoring(unittest.TestCase):
    def setUp(self):
        pass

    def test_one_vertex(self):
        g = Graph()
        g.add_node(GraphNode('A'))
        self.assertEquals(is_bipartite(g), True)

    def test_one_edge(self):
        g = Graph()
        g.add_edge('A', 'B')
        self.assertEquals(is_bipartite(g), True)

    def test_two_edges(self):
        g = Graph()
        g.add_edge('A', 'B')
        g.add_edge('A', 'C')
        self.assertEquals(is_bipartite(g), True)

    def test_linear(self):
        g = Graph()
        g.add_edge('A', 'B')
        g.add_edge('B', 'C')
        g.add_edge('C', 'D')
        g.add_edge('D', 'E')
        g.add_edge('E', 'F')
        g.add_edge('F', 'G')
        g.add_edge('G', 'H')
        g.add_edge('H', 'I')
        g.add_edge('I', 'J')
        self.assertEquals(is_bipartite(g), True)

    def test_tree(self):
        g = Graph()
        g.add_edge('A', 'B')
        g.add_edge('A', 'C')
        g.add_edge('A', 'D')
        g.add_edge('B', 'E')
        g.add_edge('B', 'F')
        g.add_edge('F', 'G')
        g.add_edge('F', 'H')
        g.add_edge('F', 'I')
        g.add_edge('F', 'J')
        self.assertEquals(is_bipartite(g), True)

    def test_triangle(self):
        g = Graph()
        g.add_edge('A', 'B')
        g.add_edge('A', 'C')
        g.add_edge('B', 'C')
        self.assertEquals(is_bipartite(g), False)

    def test_ok_back_edge(self):
        g = Graph()
        g.add_edge('A', 'B')
        g.add_edge('A', 'C')
        g.add_edge('B', 'D')
        g.add_edge('B', 'E')
        g.add_edge('E', 'F')
        g.add_edge('E', 'G')
        g.add_edge('G', 'H')
        g.add_edge('G', 'I')
        g.add_edge('I', 'C')
        self.assertEquals(is_bipartite(g), True)

    def test_not_ok_back_edge(self):
        g = Graph()
        g.add_edge('A', 'B')
        g.add_edge('A', 'C')
        g.add_edge('C', 'S')
        g.add_edge('B', 'D')
        g.add_edge('B', 'E')
        g.add_edge('E', 'F')
        g.add_edge('E', 'G')
        g.add_edge('G', 'H')
        g.add_edge('G', 'I')
        g.add_edge('I', 'S')
        self.assertEquals(is_bipartite(g), False)

if __name__ == '__main__':
    unittest.main()
