import math

import networkx as nx
import ast
import pylab
from numpy import array


def euclidean(node1, node2):
    return math.sqrt((node2['x'] - node1['x']) ** 2 +
                     (node2['y'] - node1['y']) ** 2)


def get_x_y(node1, node2, epn):
    """Recieve ({'y': 3, 'x': 2}, {'y': 4, 'x': 3}, 0.1)
    Return {'x': 3.2, 'y': 3.3}
    """
    x = node1['x'] + epn * (node2['x'] - node1['x'])
    y = node1['y'] + epn * (node2['y'] - node1['y'])
    return {'x': x, 'y': y}


def get_direction_codes(nodes_list):
    """
    Codes:
    1 up
    2 down
    3 right
    4 left

    Return list of directions viewed from the sky not from cart direction
    """
    directions = []
    for index, node in enumerate(nodes_list):
        try:
            next_node = nodes_list[index + 1]
        except IndexError:
            break
        if R.node[node]['x'] == R.node[next_node]['x']:
            if R.node[node]['y'] < R.node[next_node]['y']:
                directions += [1]
            else:
                directions += [2]
        elif R.node[node]['y'] == R.node[next_node]['y']:
            if R.node[node]['x'] < R.node[next_node]['x']:
                directions += [3]
            else:
                directions += [4]
    return directions

def add_coordinates_to_node(node):
    """ Add coordinates to node with notation (id, (a, b), %)

    a - node closer to (0,0)
    b - node farther from (0,0)
    $ - relative percent of total length of (a, b) edge from a
    return (id, (a, b), %, {'x': 3, 'y': 2}) node
    """
    k = node[2]
    neighbor1 = node[1][0]
    neighbor2 = node[1][1]
    node += (
        {
            'x': B.node[neighbor1]['x'] +
            (B.node[neighbor2]['x'] - B.node[neighbor1]['x']) * k,
            'y': B.node[neighbor1]['y'] +
            (B.node[neighbor2]['y'] - B.node[neighbor1]['y']) * k
        },
    )
    return node

def add_products_to_graph(products, B):
    """ Insert nodes with notation (id, (a, b) %)
    Recieves dictionary:
        {('a', 'b'): ((2741, ('a', 'b',) 0.5),), ('d', 'c'): ((..),(..),)}

    a - node closer to (0,0)
    b - node farther from (0,0)
    $ - relative percent of total length of (a, b) edge from a

    """
    for k, v in products.items():
        previous_node = k[0]
        # sort by %
        v = sorted(v, key=lambda tup: tup[2])
        B.remove_edge(k[0], k[1])
        for product in v:
            product = add_coordinates_to_node(product)
            id, (abs_prev_node, forward_node), percent, coordinates = product
            # calculate here which is the closest
            B.add_node(id, x=coordinates['x'], y=coordinates['y'])
            B.add_edge(previous_node, id,
                       weight=euclidean(B.node[previous_node], coordinates))
            # imitate node on edge
            previous_node = id
        B.add_edge(id, forward_node, weight=euclidean(B.node[forward_node],
                                                      coordinates))


def add_product_to_corridor(product):
    x_y = get_x_y(B.node[product[1][0]], B.node[product[1][0]], product[2])
    edge_to_remove, epn_on_closest = graphlocation_from_location(R, x_y)
    print epn_on_closest
    new_x_y = get_x_y(R.node[edge_to_remove[0]], R.node[edge_to_remove[1]],
                      epn_on_closest)
    product_id = product[0]
    R.remove_edge(*edge_to_remove)

    R.add_node(product[0], x=new_x_y['x'], y=new_x_y['y'])
    R.add_edge(edge_to_remove[0], product[0], weight=euclidean(
        R.node[product_id], R.node[edge_to_remove[0]])
    )
    R.add_edge(product[0], edge_to_remove[1], weight=euclidean(
        R.node[product_id], R.node[edge_to_remove[1]])
    )


def clamp(x, xmin, xmax):
    return min(max(x, xmin), xmax)


def epn_distance(x, y, p1x, p1y, p2x, p2y):
    # vector a = p - p1
    ax = x - p1x
    ay = y - p1y
    # vector b = p2 - p1
    bx = p2x - p1x
    by = p2y - p1y
    # dot product a*b
    dot = ax * bx + ay * by
    # squared length of vector b
    len_sq = bx * bx + by * by
    # normalized projection of vector a to vector b
    epn = float(dot) / float(len_sq) if len_sq != 0 else -1

    epn = clamp(epn, 0.0, 1.0)

    xx = p1x + epn * bx
    yy = p1y + epn * by


    dx = x - xx
    dy = y - yy

    distance = math.hypot(dx, dy)

    return (epn, distance)


def graphlocation_from_location(graph, location):
    edges = graph.edges()
    nodes = graph.nodes()
    closest_edge = None
    epn_on_closest = 0.0
    distance_to_closest = 0.0
    for node1, node2 in edges:
        epn, dist = epn_distance(
            location['x'], location['y'],
            graph.node[node1]['x'], graph.node[node1]['y'],
            graph.node[node2]['x'], graph.node[node2]['y'],
        )
        if (dist < distance_to_closest) or (closest_edge is None):
            distance_to_closest = dist
            epn_on_closest = epn
            closest_edge = (node1, node2)

    return closest_edge, epn_on_closest


# Blue graph
B = nx.Graph()
R = nx.Graph()

with open('map.txt', 'r') as f:
    gr = f.read()

gr = ast.literal_eval(gr)

for key, value in gr.items():
    for k, v in value.items():
        if key == "corridors":
            graph = R
        elif key == "shelves":
            graph = B
        for i, l in enumerate(v, start=1):
            if k == "nodes":
                graph.add_node(i, x=l[0], y=l[1])
            elif k == "edges":
                graph.add_edge(l[0], l[1], weight=euclidean(graph.node[l[0]],
                                                            graph.node[l[1]]))

temp_graph = list(nx.connected_components(R))
for i, c in enumerate(temp_graph):
    if i == 0:
        continue
    for node in c:
        R.remove_node(node)

nodes = [[d['x'], d['y']] for n, d in R.nodes(data=True)]

nodes_indices = {n: i + 1 for i, n in enumerate(R.nodes())}

edges = [(nodes_indices[n1], nodes_indices[n2]) for n1, n2 in R.edges()]

import json
red_graph = {'nodes': nodes, 'edges': edges}
json.dumps(red_graph)

pylab.rcParams['figure.figsize'] = (16.0, 11.0)
pos = {n: (d['x'], d['y']) for n, d in R.nodes(data=True)}
nx.draw_networkx_nodes(R, pos, node_size=3,
                       node_color='r')
label_pos = {n: array(p) + array([10, 10]) for n, p in pos.items()}
labels = {n: str(n) for n in R.nodes()}
lab = nx.draw_networkx_labels(R, label_pos, labels=labels)
nx.draw_networkx_edges(R, pos, alpha=0.2, edgelist=R.edges())

p0 = (2738, (16, 15), 0.3)

l = [p0]

d = {}
for p in l:
    if p[1] in d.keys():
        d[p[1]] += (p,)
    else:
        d[p[1]] = (p,)

add_products_to_graph(d, B)

add_product_to_corridor(p0)
print get_direction_codes(nx.shortest_path(R, 39, 2738, 'weight'))
