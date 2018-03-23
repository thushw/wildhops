# An easy to use graph

![alt text](fig.jpeg "graph")

Reference-style: 
This is a graph written completely in python. It provides an intuitive way to initialize a graph and add vertices and edges. One of the goals is to have the user to the least possible work. The library will guess and work on the user's behalf in some circumstances. For ex, the API allows an edge to be added even when the vertices have not yet been added. In this case, the vertices will be added with the minimal defaults.

## Usage

### First initialize the graph
g = Graph() 

### Add a vertex to the graph, the vertices will be automatically added
g.add_node(GraphNode('seattle', [Edge('seattle', 'bellevue', 'dist', 10), Edge('seattle', 'lynwood', 'dist', 20)]))

### Grow the graph by adding a vertex
g.add_node(GraphNode('austin'))

### Grow the graph by adding an edge
g.add_edge('bellevue', 'lynwood', 'dist', 5)

### You can add multiple edges between vertices, the edge name is unique between 2 vertices.
g.add_edge('bellevue', 'lynwood', 'growth', 5)
g.add_edge('lynwood', 'bellevue', 'growth', 5)

### Look at the graph
print (g)

### Run tests
From the top level directory type:
`python -munittest discover -v tests`
