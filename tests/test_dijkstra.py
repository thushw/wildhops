#!/usr/bin/env python

import unittest
from operator import itemgetter

from wildhops.graph import Graph, GraphNode
from wildhops.dijkstra import shortest_paths


class TestDijkstra(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_no_paths_graph(self):
        g = Graph()
        g.add_node(GraphNode('A'))
        self.assertEquals(shortest_paths(g, 'A'), [('A',(0,[]))])

    def test_linear_graph(self):
        g = Graph()
        g.add_edge('paris', 'london', weight=20)
        g.add_edge('london', 'dublin', weight=10)
        self.assertEquals(sorted(shortest_paths(g, 'paris'), key=itemgetter(0)),
                          sorted([('paris', (0,[])),
                                  ('london', (20,['paris'])),
                                  ('dublin', (30,['paris','london']))
                          ])
        )

    def test_unique_paths_graph(self):
        g = Graph()
        g.add_edge('paris', 'london', weight=20)
        g.add_edge('paris', 'brussels', weight=30)
        g.add_edge('london', 'dublin', weight=8)
        g.add_edge('london', 'stockholm', weight=5)
        g.add_edge('brussels', 'luxembourg', weight=6)
        self.assertEquals(sorted(shortest_paths(g, 'paris'), key=itemgetter(0)),
                          sorted([('paris', (0, [])), ('london', (20,['paris'])), ('dublin', (28,['paris','london'])),
                                  ('brussels', (30,['paris'])), ('stockholm', (25,['paris','london'])),
                                  ('luxembourg', (36,['paris','brussels']))]))

    def test_longer_dup_path_graph(self):
        g = Graph()
        g.add_edge('paris', 'london', weight=20)
        g.add_edge('paris', 'brussels', weight=30)
        g.add_edge('london', 'dublin', weight=8)
        g.add_edge('london', 'stockholm', weight=5)
        g.add_edge('brussels', 'luxembourg', weight=6)
        g.add_edge('dublin', 'luxembourg', weight=10)
        self.assertEquals(sorted(shortest_paths(g, 'paris'), key=itemgetter(0)),
                          sorted([('paris', (0, [])), ('london', (20,['paris'])), ('dublin', (28,['paris','london'])),
                                  ('brussels', (30,['paris'])), ('stockholm', (25,['paris','london'])),
                                  ('luxembourg', (36,['paris','brussels']))]))

    def test_shorter_dup_path_graph(self):
        g = Graph()
        g.add_edge('paris', 'london', weight=20)
        g.add_edge('paris', 'brussels', weight=30)
        g.add_edge('london', 'dublin', weight=8)
        g.add_edge('london', 'stockholm', weight=5)
        g.add_edge('brussels', 'luxembourg', weight=6)
        g.add_edge('dublin', 'luxembourg', weight=2)
        self.assertEquals(sorted(shortest_paths(g, 'paris'), key=itemgetter(0)),
                          sorted([('paris', (0, [])), ('london', (20,['paris'])), ('dublin', (28,['paris','london'])),
                                  ('brussels', (30,['paris'])), ('stockholm', (25,['paris','london'])),
                                  ('luxembourg', (30,['paris','london','dublin']))]))

    def test_two_shorter_dup_paths_graph(self):
        g = Graph()
        g.add_edge('paris', 'london', weight=20)
        g.add_edge('paris', 'brussels', weight=25)
        g.add_edge('london', 'dublin', weight=8)
        g.add_edge('london', 'stockholm', weight=5)
        g.add_edge('brussels', 'luxembourg', weight=6)
        g.add_edge('brussels', 'amsterdam', weight=15)
        g.add_edge('dublin', 'luxembourg', weight=2)
        g.add_edge('luxembourg', 'amsterdam', weight=9)
        self.assertEquals(sorted(shortest_paths(g, 'paris'), key=itemgetter(0)),
                          sorted([('paris', (0, [])), ('london', (20,['paris'])), ('dublin', (28,['paris','london'])),
                                  ('brussels', (25,['paris'])), ('stockholm', (25,['paris','london'])),
                                  ('luxembourg', (30,['paris','london','dublin'])),
                                  ('amsterdam', (39, ['paris','london','dublin','luxembourg']))]))

if __name__ == '__main__':
    unittest.main()

        
        
