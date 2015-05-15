#!/usr/bin/env python

__author__ = """Aric Hagberg (hagberg@lanl.gov)"""
try:
        import matplotlib.pyplot as plt
except:
        raise

import networkx as nx
from math import sqrt

G=nx.Graph()

G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.node[1]['x'] = 1
G.node[2]['x'] = 2
G.node[3]['x'] = 1
G.node[4]['x'] = 4
G.node[5]['x'] = 1
G.node[1]['y'] = 1
G.node[2]['y'] = 2
G.node[3]['y'] = 3
G.node[4]['y'] = 4
G.node[5]['y'] = 100 
G.add_edge(1, 2, weight=sqrt((G.node[1]['x'] - G.node[2]['x'])**2 + (G.node[1]['y'] - G.node[2]['y'])**2))
G.add_edge(1,3, weight=sqrt((G.node[1]['x'] - G.node[2]['x'])**2 + (G.node[1]['y'] - G.node[2]['y'])**2))
G.add_edge(3,4, weight=sqrt((G.node[1]['x'] - G.node[2]['x'])**2 + (G.node[1]['y'] - G.node[2]['y'])**2))
G.add_edge(3,5, weight=sqrt((G.node[1]['x'] - G.node[2]['x'])**2 + (G.node[1]['y'] - G.node[2]['y'])**2))
G.add_edge(3,5, weight=sqrt((G.node[1]['x'] - G.node[2]['x'])**2 + (G.node[1]['y'] - G.node[2]['y'])**2))
G.add_edge(1,4, weight=sqrt((G.node[1]['x'] - G.node[2]['x'])**2 + (G.node[1]['y'] - G.node[2]['y'])**2))
print nx.shortest_path(G, 2, 3, weight='weight')
print G.node[2]['x']
print G.node[2]['y']
print G.node[3]['x']
print G.node[3]['y']
elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]

pos=nx.spring_layout(G) # positions for all nodes

# nodes
nx.draw_networkx_nodes(G,pos,node_size=700)

# edges
nx.draw_networkx_edges(G,pos,edgelist=elarge,
                       width=6)
nx.draw_networkx_edges(G,pos,edgelist=esmall,
                                           width=6,alpha=0.5,edge_color='b',style='dashed')

# labels
nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')

plt.axis('off')
plt.savefig("weighted_graph.png") # save as png
plt.show() # display
