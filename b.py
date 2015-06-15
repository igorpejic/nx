# import matplotlib.pyplot as plt
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

    # coordinate_to_keep = 'y' if coordinate_to_change != 'y' else 'x'

    # get name of closest node
    closest_node = closest_node[0]

    # determine corridor that has two nodes with same coord_to_change values

    neighbors = R.neighbors(closest_node)

    # select neighbor closest to product which has same coordinate_to_change
    closest_neighbor_to_closest_node = neighbors[0]
    min = 9999999

    # select node which is closest to product and is neighbor of closest_node
    for neighbor in neighbors:
        temp_val = euclidean(R.node[neighbor], B.node[product])

        same_coord_to_change = R.node[closest_node][coordinate_to_change] ==\
            R.node[neighbor][coordinate_to_change]
        if temp_val < min and same_coord_to_change:
            min = temp_val
            closest_neighbor_to_closest_node = neighbor
    higher_node_value = closest_node < closest_neighbor_to_closest_node
    return (closest_node, closest_neighbor_to_closest_node)\
        if higher_node_value\
        else (closest_neighbor_to_closest_node, closest_node)


def add_products_to_corridor(product):
    """Recieves {(4, 1): ((2743, {'y': 8.2, 'x': 2.0}),
    (2744, {'y': 7.4, 'x': 2.0}), (2745, {'y': 10.6, 'x': 2.0})),
    (3, 2): ((2742, {'y': 9.0, 'x': 10.0}),),
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
            R.add_edge(previous, node[0], weight=euclidean(R.node[previous],
                                                           node[1]))
            previous = node[0]
        R.add_edge(previous, k[1], weight=euclidean(R.node[previous],
                                                    R.node[k[1]]))


def get_direction_codes(nodes_list):
    """
    Codes:
    1 up
    2 down
    3 right
    4 left

    Return list of directions, skip product nodes
    """
    directions = []
    for index, node in enumerate(nodes_list):
        # skip products
        if node > 100:
            continue
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

# Red graph
R = nx.Graph()
R.add_node(1, x=1, y=1)
R.add_node(2, x=1, y=7)
R.add_node(3, x=10, y=7)
R.add_node(4, x=10, y=1)
R.add_node(5, x=1, y=13)
R.add_node(6, x=10, y=13)
R.add_edge(1, 2, weight=euclidean(R.node[1], R.node[2]))
R.add_edge(2, 3, weight=euclidean(R.node[2], R.node[3]))
R.add_edge(3, 4, weight=euclidean(R.node[3], R.node[4]))
R.add_edge(4, 1, weight=euclidean(R.node[4], R.node[1]))
R.add_edge(2, 5, weight=euclidean(R.node[2], R.node[5]))
R.add_edge(5, 6, weight=euclidean(R.node[5], R.node[6]))
R.add_edge(3, 6, weight=euclidean(R.node[3], R.node[6]))

# Blue graph
B = nx.Graph()
B.add_node('a', x=2, y=2)
B.add_node('b', x=2, y=6)
B.add_node('c', x=9, y=6)
B.add_node('d', x=9, y=2)
B.add_node('e', x=2, y=8)
B.add_node('h', x=2, y=12)
B.add_node('g', x=9, y=12)
B.add_node('f', x=9, y=8)
B.add_edge('a', 'b', weight=euclidean(B.node['a'], B.node['b']))
B.add_edge('b', 'c', weight=euclidean(B.node['b'], B.node['c']))
B.add_edge('d', 'c', weight=euclidean(B.node['d'], B.node['c']))
B.add_edge('d', 'a', weight=euclidean(B.node['d'], B.node['a']))
B.add_edge('e', 'f', weight=euclidean(B.node['e'], B.node['f']))
B.add_edge('e', 'h', weight=euclidean(B.node['e'], B.node['h']))
B.add_edge('h', 'g', weight=euclidean(B.node['h'], B.node['g']))
B.add_edge('f', 'g', weight=euclidean(B.node['f'], B.node['g']))

if False:
    p0 = (2738, ('d', 'c'), 0.7)
    p1 = (2739, ('d', 'c'), 0.5)
    p2 = (2740, ('d', 'c'), 0.4)
    p3 = (2741, ('a', 'b'), 0.5)
    p4 = (2742, ('c', 'b'), 0.5)
    p5 = (2743, ('d', 'a'), 0.3)
    p6 = (2744, ('d', 'a'), 0.1)
    p7 = (2745, ('d', 'a'), 0.9)
    p8 = (2746, ('d', 'a'), 0.3)
    p9 = (2747, ('d', 'a'), 0.4)
    p10 = (2748, ('d', 'a'), 0.3)

    l = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]

if True:
    p0 = (2738, ('f', 'g'), 0.3)
    p1 = (2739, ('h', 'g'), 0.3)
    p2 = (2740, ('h', 'g'), 0.7)
    p3 = (2741, ('a', 'd'), 0.7)
    l = [p0, p1, p2, p3]

d = {}
for p in l:
    if p[1] in d.keys():
        d[p[1]] += (p,)
    else:
        d[p[1]] = (p,)

add_products_to_graph(d, B)
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

if False:
    pos = nx.spring_layout(B)
    nx.draw_networkx_nodes(B, pos, node_size=300)
    nx.draw_networkx_edges(B, pos)
    nx.draw_networkx_labels(B, pos)

if False:
    pos = nx.spring_layout(R)
    nx.draw_networkx_nodes(R, pos, node_size=400)
    nx.draw_networkx_edges(R, pos)
    nx.draw_networkx_labels(R, pos)
    # plt.axis('off')
# plt.savefig('test.png')
# plt.show()
print nx.shortest_path(R, 1, 2738, 'weight')
print nx.shortest_path(R, 4, 2739, 'weight')
print nx.shortest_path(R, 4, 2740, 'weight')
print nx.shortest_path(R, 6, 2741, 'weight')
l = nx.shortest_path(R, 4, 2739, 'weight')
print get_direction_codes(l)

with open('graf', 'w') as f:
    nx.write_gml(B, f)

with open('graf2', 'w') as f:
    nx.write_gml(R, f)


gr = {"corridors": {"nodes":[[130,98],[192,98],[192,285],[234,98],[277,285],[319,285],[319,98],[277,98],[319,285],[234,285],[30,98],[30,218],[30,285],[130,161],[130,218],[30,161],[30,426],[30,368],[113,285],[30,501],[66,501],[130,438],[30,477],[130,382],[130,501],[192,501],[234,501],[277,501],[319,501],[192,312],[130,328],[130,312],[130,285],[234,312],[277,312],[319,312],[364,285],[407,285],[364,98],[407,98],[364,501],[407,501],[364,312],[407,312],[451,285],[451,312],[451,98],[533,312],[533,501]],"edges":[[1,2],[2,4],[4,8],[8,7],[9,7],[9,5],[5,10],[10,3],[2,3],[10,4],[8,5],[13,12],[11,1],[14,1],[14,15],[11,16],[16,12],[12,15],[14,16],[18,19],[19,13],[18,17],[21,22],[23,17],[24,23],[23,20],[20,21],[22,24],[25,21],[22,25],[17,31],[24,31],[31,32],[32,33],[33,15],[19,33],[33,3],[3,30],[30,32],[25,26],[26,30],[26,27],[27,34],[34,30],[10,34],[34,35],[35,5],[35,36],[36,9],[29,28],[28,27],[28,35],[36,29],[29,41],[41,43],[43,37],[37,39],[39,7],[39,40],[40,38],[38,37],[37,9],[36,43],[43,44],[44,42],[42,41],[44,38],[40,47],[47,45],[45,46],[46,48],[48,49],[49,42],[46,44],[38,45]]}, "shelves": {"nodes":[[159,114],[177,114],[177,275],[159,275],[203,114],[221,114],[221,275],[203,275],[263,114],[307,114],[334,114],[351,114],[377,114],[393,114],[421,114],[437,114],[437,275],[421,275],[393,275],[377,275],[351,275],[334,275],[307,275],[291,275],[263,275],[51,114],[97,114],[97,146],[51,146],[247,114],[263,275],[247,275],[291,114],[51,175],[51,204],[97,204],[97,175],[97,234],[97,264],[51,264],[51,234],[82,334],[93,344],[59,377],[48,366],[82,389],[93,401],[82,447],[93,458],[48,479],[59,491],[59,434],[48,424],[159,326],[177,326],[203,326],[221,326],[247,326],[263,326],[291,326],[307,326],[334,326],[351,326],[377,326],[393,326],[393,479],[334,479],[351,479],[377,479],[291,479],[307,479],[263,479],[247,479],[221,479],[203,479],[177,479],[159,479],[437,334],[437,479],[516,334],[516,479]],"edges":[[4,1],[1,2],[2,3],[3,4],[5,6],[6,7],[7,8],[8,5],[26,27],[27,28],[28,29],[29,26],[9,30],[31,9],[31,32],[32,30],[33,10],[10,23],[23,24],[24,33],[11,22],[22,21],[21,12],[12,11],[20,19],[19,14],[14,13],[13,20],[15,16],[16,17],[17,18],[18,15],[34,37],[37,36],[36,35],[35,34],[38,39],[39,40],[40,41],[41,38],[42,43],[43,44],[44,45],[45,42],[46,47],[47,52],[52,53],[53,46],[48,49],[49,51],[51,50],[50,48],[54,55],[55,76],[76,77],[77,54],[56,57],[57,74],[74,75],[75,56],[58,59],[59,72],[72,73],[73,58],[60,61],[61,71],[71,70],[70,60],[62,63],[63,68],[68,67],[67,62],[64,65],[65,66],[66,69],[69,64],[79,78],[81,80],[80,78],[79,81]]}}

graph = nx.to_networkx_graph(gr)
print graph.nodes()
print graph.edges()
