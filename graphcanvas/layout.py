import networkx
import numpy

def tree_layout(graph, dim=2, scale=1):

    if dim != 2:
        raise ValueError('currently only 2D graphs are supported')

    if not graph.is_directed():
        raise ValueError('graph must be directed')

    if not networkx.is_directed_acyclic_graph(graph):
        raise ValueError('graph must not contain cycles')

    roots = numpy.array([
        node for node, degree in graph.in_degree_iter() if degree < 1
    ])

    # Find the tree width at every depth in order to layout
    # the nodes in a justified manner

    depths = []
    for node in graph.nodes():
        depth = 0
        parents = graph.predecessors(node)
        while len(parents) > 0:
            node = parents[0]
            parents = graph.predecessors(node)
            depth += 1
        depths.append(depth)

    max_depth = max(depths)
    widths = [depths.count(i) for i in range(max_depth+1)]
    max_width = max(widths)
    nodes_positioned_at_depth = [0] * len(widths)

    # breadth first tree transversal
    positions = {}
    for root in roots:
        node_stack = [(0, root)]
        while len(node_stack) > 0:
            curr_depth, curr_node = node_stack.pop()
            for child in graph.successors(curr_node):
                node_stack.append((curr_depth + 1, child))

            # top-down
            draw_depth = 1.0 - float(curr_depth)/max_depth
            depth_width = float(widths[curr_depth])

            # center align
            nodes_positioned_at_depth[curr_depth] += 1
            width_positions = numpy.linspace(0, 1, depth_width+2)
            draw_width = width_positions[nodes_positioned_at_depth[curr_depth]]

            positions[curr_node] = (draw_width, draw_depth)


    return positions


def circular_layout(graph):
    graph_size = len(graph)
    radius = numpy.log2(graph_size) * 50

    if networkx.is_directed(graph):
        roots = numpy.array([
            node for node, degree in graph.in_degree_iter() if degree < 1
        ])
        depths = []
        for node in graph.nodes():
            depth = 0
            parents = graph.predecessors(node)
            while len(parents) > 0:
                node = parents[0]
                parents = graph.predecessors(node)
                depth += 1
                depths.append(depth)
        max_depth = max(depths)
        widths = [depths.count(i) for i in range(max_depth+1)]
        # Find the tree width at every depth in order to layout
        # the nodes in a justified manner
        max_width = max(widths)
        nodes_positioned_at_depth = [0] * len(widths)

        # breadth first tree transversal
        positions = {}
        for root in roots:
            node_stack = [(0, root)]
            while len(node_stack) > 0:
                curr_depth, curr_node = node_stack.pop()
                for child in graph.successors(curr_node):
                    node_stack.append((curr_depth + 1, child))

                    # top-down
                    draw_depth = radius * float(curr_depth) / max_depth
                    depth_width = float(widths[curr_depth])

                    # center align
                    nodes_positioned_at_depth[curr_depth] += 1
                    angles = numpy.linspace(0, 1, depth_width+2) * numpy.pi * 2
                    draw_x = numpy.cos(
                        angles[nodes_positioned_at_depth[curr_depth]]
                    ) * draw_depth
                    draw_y = numpy.sin(
                        angles[nodes_positioned_at_depth[curr_depth]]
                    ) * draw_depth

                    positions[curr_node] = (draw_x, draw_y)
    else:
        roots = numpy.array([node for node in graph.nodes_iter()])
        angles = numpy.linspace(0, 1, graph_size) * numpy.pi * 2
        draw_x = numpy.cos(angles) * radius
        draw_y = numpy.sin(angles) * radius
        positions = {node: (x, y) for node, x, y in zip(roots, draw_x, draw_y)}



    return positions
