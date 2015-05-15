# coding: utf-8

import networkx as nx
G = nx.Graph()
from math import sqrt
G.add_edge(1, 2)
G
G.edges()
G[1]
G.node[1]
G.node[1]['x'] = 3
G.node[1]
G.node[1]['y'] = 4
G.nodes9)
G.nodes()
G.nodes(data=True)
G.node[2]['x'] = 4
G.node[2]['y'] = 7
G.nodes(data=True)
G.remove_ege((1,2))
G.remove_edge((1,2))
G.remove_edge(1,2)
G.nodes()
G.edges()
G.add_edge(1, 2, weight=sqrt(sum( (G.node[1]['x'] - G.node[2]['x'])**2))

)
G.add_edge(1, 2, weight=sqrt(sum( (G.node[1]['x'] - G.node[2]['x']))**2)
)
G.add_edge(1, 2, weight=sqrt(sum( (G.node[1]['x'] - G.node[2]['x'])**2, (G.node[1]['y'] - G.node[2]['y'])**2))
)
G.add_edge(1, 2, weight=sqrt(sum( (G.node[1]['x'] - G.node[2]['x'])**2, (G.node[1]['y'] - G.node[2]['y'])**2)))
)
G.add_edge(1, 2, weight=sqrt(sum( (G.node[1]['x'] - G.node[2]['x'])**2, (G.node[1]['y'] - G.node[2]['y'])**2)))
)
G.add_edge(1, 2, weight=sqrt(sum( (G.node[1]['x'] - G.node[2]['x'])**2, (G.node[1]['y'] - G.node[2]['y'])**2)))
G.add_edge(1, 2, weight=sqrt(sum( (G.nodes[1]['x'] - G.node[2]['x'])**2, (G.node[1]['y'] - G.node[2]['y'])**2)))
G.add_edge(1, 2, weight=sqrt(sum( (G.node[1]['x'] - G.node[2]['x'])**2, (G.node[1]['y'] - G.node[2]['y'])**2)))
G.add_edge(1, 2, weight=sqrt(sum( (G.node[1]['x'] - G.node[2]['x'])**2, (G.node[1]['y'] - G.node[2]['y'])**2)))
G.add_edge(1, 2, weight=sqrt((G.node[1]['x'] - G.node[2]['x'])**2 + (G.node[1]['y'] - G.node[2]['y'])**2))
G.edges()
G.edges(data=True)
G.nodes()
G.nodes(data=True)
G.edge[1]
G.edge[1]['weight']
G.edge[1]
G.edge[1][2]
G.edge[1][2]['weight']
w = G.edge[1][2]['weight']
w
G.remove_edge(1,2)
G.add_edge(1, 3, weight=0.8*w)
G.add_edge(2, 3, weight=0.2*w)
