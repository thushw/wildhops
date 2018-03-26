import logging
logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

class Edge:
    def __init__(self, fv, tv, name='default', weight=0, properties=None):
        self.fv = fv
        self.tv = tv
        self.name = name
        self.weight = weight
        self.properties = {} if not properties else properties

    def __repr__(self):
        return '{}:{}:{}:{}'.format(self.fv, self.tv, self.name, self.weight)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class GraphNode:
    def __init__(self, value, edges=None, properties=None):
        self.value = value
        self.edges = [] if not edges else edges
        self.properties = {} if not properties else properties

    def __repr__(self):
        return '{}:{} -> {}'.format(self.value, self.properties, 
                                 ' '.join([e.__repr__() for e in self.edges]))

    def edge_exists(self, tov, edge_name=None):
        list_edges = ([edge for edge in self.edges if edge.tv == tov and 
                       (edge_name is None or edge.name == edge_name)])
        return len(list_edges) > 0
        
class Graph:
    def __init__(self):
        self.nodes = []
    
    def __repr__(self):
        return '\n'.join([node.__repr__() for node in self.nodes])
        
    def add_node(self, node):
        if self.find_nodes(node.value):
            raise ValueError('duplicate vertex {}'.format(node.value))
            
        if any([e.fv != node.value for e in node.edges]):
            raise ValueError('the from vertex should be the same as the node you are adding it to')
        
        #add any nodes on the other side of edges
        for e in node.edges:
            if not self.find_nodes(e.tv):
                logger.debug ('adding missing node for {}'.format(e.tv))
                self.nodes.append(GraphNode(e.tv))
        
        self.nodes.append(node)

    def find_node(self, tgt):
        """ Return the vertex with the given name. """
        
        vertices = self.find_nodes(tgt)
        return vertices[0] if vertices else None
        
    def find_nodes(self, tgt):
        """ Return a list of vertices with the given name. """
        
        return [node for node in self.nodes if node.value == tgt]
        
    def add_edge(self, fromv, tov, name='default', weight=0, properties=None):
        to_nodes = self.find_nodes(tov)
        from_nodes = self.find_nodes(fromv)
        if len(from_nodes) == 0:
            logger.debug ('adding missing from vertex')
            self.add_node(GraphNode(fromv))
        elif len(from_nodes) > 1:
            raise ValueError('{} duplicate vertices exist for: {}'.format(len(from_nodes)-1, fromv))
        if len(to_nodes) > 1:
            raise ValueError('{} duplicate vertices exist for: {}'.format(len(to_nodes)-1, tov))
        elif len(to_nodes) == 0:
            logger.debug ('adding missing to vertex')
            self.add_node(GraphNode(tov))
            
        #refresh from_nodes, since we may have added some
        from_nodes = self.find_nodes(fromv)
        if from_nodes[0].edge_exists(tov, name):
            raise ValueError('duplicate edge for: {}:{}:{}'.format(fromv, tov, name))

        from_nodes[0].edges.append(Edge(fromv, tov, name, weight, properties))

if __name__ == '__main__':

    logger.setLevel(logging.DEBUG)

    g = Graph()
    g.add_node(GraphNode('seattle', 
                         [Edge('seattle', 'bellevue', 'dist', 10), Edge('seattle', 'lynwood', 'dist', 20)]))
    g.add_edge('bellevue', 'lynwood', 'dist', 5)
    g.add_edge('woodenville', 'lynwood', 'dist', 7)
    
    g.add_edge('bellevue', 'lynwood', 'friends',  15)

    g.add_node(GraphNode('redmond', properties={'population': 72000, 'area': '12000 sqmiles'}))

    logger.info (g)
