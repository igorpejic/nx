#!/usr/bin/env python

__author__ = """Aric Hagberg (hagberg@lanl.gov)"""
try:
        import matplotlib.pyplot as plt
except:
        raise

import networkx as nx
from math import sqrt

G=nx.Graph()
K=nx.Graph()
K.add_node('a')
K.add_node('b')
K.add_node('c')
K.add_node('d')
K.node['a']['x'] = 2
K.node['b']['x'] = 10
K.node['c']['x'] = 10
K.node['d']['x'] = 2
K.node['a']['y'] = 7
K.node['b']['y'] = 7
K.node['c']['y'] = 3
K.node['d']['y'] = 3
K.add_edge('a', 'b')
K.add_edge('b', 'c')
K.add_edge('c', 'd')
K.add_edge('d', 'a')
print K.edges()
for i in K.edges():
    g, k = i
    K.add_edge(g, k, weight = sqrt((K.node[g]['x'] - K.node[k]['x'])**2 + (K.node[g]['y'] - K.node[k]['y'])**2))
p1 = ('c', 'd', 0.3)
p2 = ('c', 'd', 0.4)
p3 = ('d', 'c', 0.2)
lis = [[p1, p2, p3]]
print 'aaaa'
nl = []
for l in lis:
    n = []
    for tupl in l:
        tupl = tupl + ({'x':2, 'y':2},)
        n += (tupl,)
    nl += n
print nl[0][3]['x']

def euclidean(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def get_coordinates_between_nodes(node):
    """ Get coordinates of node with notation (a, b, %)

    a - node closer to (0,0)
    b - node farther from (0,0)
    $ - relative percent of total length of (a, b) edge from a
    """
    k = node[2]
    node += ({'x': K.node[node[0]]['x'] + (K.node[node[1]]['x'] - K.node[node[0]]['x']) * k, 'y': K.node[node[0]]['y'] + (K.node[node[1]]['y'] - K.node[node[0]]['y']) * k},)
    print 'beba:' 
    print node
    

get_coordinates_between_nodes(p3)
print euclidean(0, 0, 1, 1)

a = 0
for l in lis:
    for tupl in sorted(l, key=lambda tup: tup[2]):
        if a == 0:
            i, j, k = tupl
        a += 1
        K.add_node(a)
        K.node[a]['x'] = K.node[j]['x'] - (K.node[j]['x'] - K.node[i]['x']) * k
        K.node[a]['y'] = K.node[j]['y'] - (K.node[j]['y'] - K.node[i]['y']) * k
        K.remove_edge(i, j)
        K.add_edge(i, a)
        K.add_edge(a, j)
        i = a
        
                     




print K.neighbors('a')
print K.nodes(data=True)
print K.edges(data=True)

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
print G.edges()
for i in G.edges():
    g, k = i
    G.edge[g][k]['weight'] = sqrt((G.node[g]['x'] - G.node[k]['x'])**2 + (G.node[g]['y'] - G.node[k]['y'])**2)
    print G.edge[g][k]['weight']
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

print 'bbbbbbbbbbbbbbbbbb'
G.add_node(6, x=2, y=3)
print G.node[6]
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
print G.edges()
for i in G.edges():
    g, k = i
    G.edge[g][k]['weight'] = sqrt((G.node[g]['x'] - G.node[k]['x'])**2 + (G.node[g]['y'] - G.node[k]['y'])**2)
    print G.edge[g][k]['weight']
print nx.shortest_path(G, 2, 3, weight='weight')
print G.node[2]['x']
print G.node[2]['y']
print G.node[3]['x']
print G.node[3]['y']
# Closest to red graph
min = 9999999 
closest_node = G.nodes(data=True)[0]
print 'aaaaaaaaa'
for node in G.nodes(data=True):
    print node
    val =  euclidean(node[1]['x'], node[1]['y'], K.node[2]['x'], K.node[2]['y'])
    print val
    if val < min:
        min = val
        closest_node = node
print K.node[2]
print G.nodes(data=True)
print closest_node
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
