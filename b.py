import matplotlib.pyplot as plt
import networkx as nx
from math import sqrt


def euclidean(node1, node2):
    return sqrt((node2['x'] - node1['x']) ** 2 +
                (node2['y'] - node1['y']) ** 2)


def add_coordinates_to_node(node):
    """ Add coordinates to node with notation (id, (a, b), %)

    a - node closer to (0,0)
    b - node farther from (0,0)
    $ - relative percent of total length of (a, b) edge from a
    return (id, (a, b), %, {'x': 3, 'y': 2}) node
    """
    k = node[2]
    node += ({'x': B.node[node[1][0]]['x'] + (B.node[node[1][1]]['x'] - B.node[node[1][0]]['x']) * k,
              'y': B.node[node[1][1]]['y'] + (B.node[node[1][1]]['y'] - B.node[node[1][0]]['y']) * k},)
    return node


def add_products_to_graph(products, B):
    """ Insert nodes with notation (id, (a, b) %)
    Recieves dictionary: {('a', 'b'): ((2741, ('a', 'b',) 0.5),), ('d', 'c'): ((..),(..),)}

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
            id, (abs_previous_node, forward_node), percent, coordinates = product
            # calculate here which is the closest 
            B.add_node(id, x=coordinates['x'], y=coordinates['y'])
            B.add_edge(previous_node, id, weight=euclidean(B.node[previous_node], coordinates))
            # imitate node on edge
            previous_node = id
        B.add_edge(id, forward_node, weight=euclidean(B.node[forward_node], coordinates))


def group_products_on_corridor_edges(product):
    """ Return on which corridor edge should the product be added
    """
    min = 99999999
    closest_node = R.node[1]
    for node in R.nodes(data=True):
        coordinates = node[1]
        val = euclidean(coordinates, B.node[product])
        if val < min:
            min = val
            closest_node = node
    neighbor1, neighbor2 = B.neighbors(product)
    # determine x and y of product in corridor
    if B.node[neighbor1]['x'] == B.node[neighbor2]['x']:
        coordinate_to_change = 'x'
    if B.node[neighbor1]['y'] == B.node[neighbor2]['y']:
        coordinate_to_change = 'y'

    coordinate_to_keep = 'y' if coordinate_to_change != 'y' else 'x'

    # determine which edge to remove temporary

    # get name of closest node
    closest_node = closest_node[0]

    # determine corridor that has two nodes with same coordinate_to_change values
    neighbors = R.neighbors(closest_node)
    try:
        neighbor1 = neighbors[0]
        neighbor2 = neighbors[1]
        neighbor3 = neighbors[2]
        neighbor4 = neighbors[3]
    except IndexError:
        pass
    if R.node[neighbor1][coordinate_to_change] == R.node[closest_node][coordinate_to_change]:
        return (neighbor1, closest_node) if neighbor1 < closest_node\
                else (closest_node, neighbor1)
    elif R.node[neighbor2][coordinate_to_change] == R.node[closest_node][coordinate_to_change]:
        return (neighbor2, closest_node) if neighbor2 < closest_node\
                else (closest_node, neighbor2)
    elif R.node[neighbor3][coordinate_to_change] == R.node[closest_node][coordinate_to_change]:
        return (neighbor3, closest_node) if neighbor3 < closest_node\
                else (closest_node, neighbor3)
    elif R.node[neighbor4][coordinate_to_change] == R.node[closest_node][coordinate_to_change]:
        return (neighbor4, closest_node) if neighbor4 < closest_node\
                else (closest_node, neighbor4)


def add_products_to_corridor(product):
    """Recieves {(4, 1): ((2743, {'y': 8.2, 'x': 2.0}), (2744, {'y': 7.4, 'x': 2.0}),
    (2745, {'y': 10.6, 'x': 2.0})), (3, 2): ((2742, {'y': 9.0, 'x': 10.0}),),
    (3, 4): ((2740, {'y': 3.0, 'x': 5.2})))}
    kind of dictionary andd adds those nodes to graph

    populates R graph
    """
    for k, v in product.items():
        R.remove_edge(k[0], k[1])
        node_has_same = 'y' if R.node[k[0]]['y'] == R.node[k[1]]['y'] else 'x'
        node_has_different = 'y' if node_has_same != 'y' else 'x'
        # start adding nodes 
        previous = k[0]
        for node in sorted(v, key=lambda tup: tup[1][node_has_different]):
            data = {}
            data[node_has_same] = R.node[k[0]][node_has_same]
            data[node_has_different] = node[1][node_has_different]
            R.add_node(node[0], **data)
            R.add_edge(previous, node[0], weight=euclidean(R.node[previous], node[1]))
            previous = node[0]
        R.add_edge(previous, k[1], weight=euclidean(R.node[previous], R.node[k[1]]))


# Red graph
R=nx.Graph()
R.add_node(1, x=1, y=8)
R.add_node(2, x=11, y=8)
R.add_node(3, x=11, y=2)
R.add_node(4, x=1, y=2)
R.add_node(5, x=1, y=17)
R.add_edge(1, 2, weight=euclidean(R.node[1], R.node[2]))
R.add_edge(2, 3, weight=euclidean(R.node[2], R.node[3]))
R.add_edge(3, 4, weight=euclidean(R.node[3], R.node[4]))
R.add_edge(4, 1, weight=euclidean(R.node[4], R.node[1]))
R.add_edge(5, 1, weight=euclidean(R.node[5], R.node[1]))

# Blue graph
B = nx.Graph()
B.add_node('a', x=2, y=7)
B.add_node('b', x=10, y=7)
B.add_node('c', x=10, y=3)
B.add_node('d', x=2, y=3)
B.add_edge('a', 'b', weight=euclidean(B.node['a'], B.node['b']))
B.add_edge('b', 'c', weight=euclidean(B.node['b'], B.node['c']))
B.add_edge('d', 'c', weight=euclidean(B.node['d'], B.node['c']))
B.add_edge('d', 'a', weight=euclidean(B.node['d'], B.node['a']))

p0 = (2738, ('d', 'c'), 0.7)
p1 = (2739, ('d', 'c'), 0.5)
p2 = (2740, ('d', 'c'), 0.4)
p3 = (2741, ('a', 'b'), 0.5)
p4 = (2742, ('c', 'b'), 0.5)
p5 = (2743, ('d', 'a'), 0.3)
p6 = (2744, ('d', 'a'), 0.1)
p7 = (2745, ('d', 'a'), 0.9)

l = [p0, p1, p2, p3, p4, p5, p6, p7]
d = {}
for p in l:
    if p[1] in d.keys():
        d[p[1]] += (p,)
    else:
        d[p[1]] = (p,)

add_products_to_graph(d, B)
product = 2743
products_in_corridor = {}
for product in B.nodes(data=True):
    if isinstance(product[0], basestring):
        continue
    k = group_products_on_corridor_edges(product[0])
    if k in products_in_corridor.keys():
        products_in_corridor[k] += (product,)
    else:
        products_in_corridor[k] = (product,)

add_products_to_corridor(products_in_corridor)
print R.edges(data=True)

if False:
    pos = nx.spring_layout(B)
    nx.draw_networkx_nodes(B, pos, node_size=300)
    nx.draw_networkx_edges(B, pos)
    nx.draw_networkx_labels(B, pos)

pos = nx.spring_layout(R)
nx.draw_networkx_nodes(R, pos, node_size=400)
nx.draw_networkx_edges(R, pos)
nx.draw_networkx_labels(R, pos)
plt.axis('off')
plt.savefig('test.png')
plt.show()
