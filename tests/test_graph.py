#!/usr/bin/env python

from figleaf.graph import Graph, GraphNode, Edge
import unittest

class TestGraph(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_init_empty_graph(self):
        g = Graph()
        self.assertEquals(g.nodes, [])
        
    def test_add_node(self):
        g = Graph()
        g.add_node(GraphNode('Mary', [Edge('Mary', 'Jane', 'friend', 90),
                                      Edge('Mary', 'Alicia', 'friend', 80),
                                      Edge('Mary', 'Nancy', 'friend', 40)
        ]))
        self.assertEquals(len(g.nodes), 4)
        self.assertEquals(sorted([node.value for node in g.nodes]), sorted(['Mary', 'Jane', 'Alicia', 'Nancy']))
        
    def test_add_edge(self):
        g = Graph()
        g.add_edge('Cara', 'Kiera', 'cousin', 0)
        self.assertEquals(len(g.nodes), 2)
        cara_nodes = g.find_nodes('Cara')
        self.assertEquals(len(cara_nodes), 1)
        self.assertEquals(len(cara_nodes[0].edges), 1)
        self.assertEquals(cara_nodes[0].edges[0].fv, 'Cara')
        self.assertEquals(cara_nodes[0].edges[0].tv, 'Kiera')
        self.assertEquals(cara_nodes[0].edges[0].name, 'cousin')
        self.assertEquals(cara_nodes[0].edges[0].weight, 0)

    def test_add_node_with_properties(self):
        g = Graph()
        g.add_node(GraphNode('Alice', properties={'age':25, 'job': 'doctor', 'education': 'pHd'}))
        alice_nodes = g.find_nodes('Alice')
        self.assertEquals(len(alice_nodes), 1)
        self.assertEquals(len(alice_nodes[0].properties), 3)
        self.assertEquals(alice_nodes[0].properties['age'], 25)
        self.assertEquals(alice_nodes[0].properties['job'], 'doctor')
        self.assertEquals(alice_nodes[0].properties['education'], 'pHd')

    def test_add_edge_with_properties(self):
        g = Graph()
        g.add_edge('Cara', 'Kiera', 'cousin', properties={'known_since': '04/05/1980', 'together_at': ['Inglemoore High', 'Naval Academy', 'Skagit Fishing']})
        self.assertEquals(len(g.nodes), 2)
        cara_nodes = g.find_nodes('Cara')
        self.assertEquals(len(cara_nodes), 1)
        self.assertEquals(len(cara_nodes[0].edges), 1)
        self.assertEquals(len(cara_nodes[0].edges[0].properties), 2)
        self.assertEquals(cara_nodes[0].edges[0].properties['known_since'], '04/05/1980')
        self.assertEquals(cara_nodes[0].edges[0].properties['together_at'], ['Inglemoore High', 'Naval Academy', 'Skagit Fishing'])

if __name__ == '__main__':
    unittest.main()
