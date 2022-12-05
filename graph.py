import matplotlib.pyplot as plt
import networkx as nx

class Vertex:

    def __init__(self, v, is_source, is_target, pos):
        '''
        creates a vertex object
        v         - label of vertex
        is_source - whether vertex is source
        is_target - whether vertex is target
        pos       - position of vertex (for drawing)
        '''

        self.label = v
        self.is_source = is_source
        self.is_target = is_target
        self.pos = pos

    def get_label(self):
        '''
        returns label of vertex
        '''

        return self.label

    def is_source(self):
        '''
        returns whether vertex is source
        '''

        return self.is_source

    def is_target(self):
        '''
        returns whether vertex is target
        '''

        return self.is_target

class Arc:

    def __init__(self, u, v, is_attackable):
        '''
        creates an arc object
        u             - tail of arc
        v             - head of arc
        is_attackable - whether arc is attackable
        '''

        self.tail = u
        self.head = v
        self.is_attackable = is_attackable

    def get_tail(self):
        '''
        return tail of arc
        '''

        return self.tail

    def get_head(self):
        '''
        returns head of arc
        '''

        return self.head

    def get_is_attackable(self):
        '''
        returns whether arc is attackable
        '''

        return self.is_attackable


class DiGraph:

    def __init__(self):
        '''
        creates a digraph object
        '''

        self.vertices = []
        self.vertex_labels = []
        self.label_map = {}
        self.sources = []
        self.targets = []

        self.arcs = []
        self.in_arcs = {}
        self.out_arcs = {}

    def add_vertex(self, v, is_source=False, is_target=False, pos=None):
        '''
        adds vertex to graph
        v - vertex to be added
        '''

        # check wether vertex already exists
        if v in self.vertex_labels:
            print("did not add vertex, it already exists in graph")
            return None

        if is_source and is_target:
            print("added vertex being both source and target")

        vert = Vertex(v, is_source, is_target, pos)
        self.label_map[v] = len(self.vertices)
        self.vertices.append(vert)
        self.vertex_labels.append(v)

        if is_source:
            self.sources.append(v)
        if is_target:
            self.targets.append(v)

        return vert

    def add_arc(self, u, v, attackable=False):
        '''
        adds arc to graph
        u - tail of arc
        v - head of arc

        optional:
        attackable - whether arc is attackable
        '''

        # check whether head and tail exist
        if not (u in self.vertex_labels and v in self.vertex_labels):
            print("did not add arc, head or tail does not exist in graph")
            return None

        tail = self.vertices[self.label_map[u]]
        head = self.vertices[self.label_map[v]]

        arc = Arc(tail, head, attackable)
        self.arcs.append(arc)

        if not v in self.in_arcs:
            self.in_arcs[v] = [arc]
        else:
            self.in_arcs[v].append(arc)

        if not u in self.out_arcs:
            self.out_arcs[u] = [arc]
        else:
            self.out_arcs[u].append(arc)

    def get_vertices(self):
        '''
        returns vertices
        '''

        return self.vertices

    def get_vertex_labels(self):
        '''
        returns vertex labels
        '''

        return self.vertex_labels

    def get_sources(self):
        '''
        returns sources of graph
        '''

        return self.sources

    def get_targets(self):
        '''
        returns targets of graph
        '''

        return self.targets

    def get_arcs(self):
        '''
        returns arcs
        '''

        return self.arcs

    def get_in_arcs(self, v):
        '''
        returns arcs pointing to v
        '''

        if not v in self.in_arcs:
            return None

        return self.in_arcs[v]

    def get_out_arcs(self, v):
        '''
        returns arcs leaving v
        '''

        if not v in self.out_arcs:
            return None

        return self.out_arcs[v]

    def in_degree(self, v):
        '''
        returns in-degree of vertex with label v
        '''

        if not v in self.vertex_labels:
            return None

        if not v in self.in_arcs:
            return 0

        return len(self.in_arcs[v])


    def out_degree(self, v):
        '''
        returns out-degree of vertex with label v
        '''

        if not v in self.vertex_labels:
            return None

        if not v in self.out_arcs:
            return 0

        return len(self.out_arcs[v])

    def visualize(self):
        '''
        visualizes graph
        '''

        G = nx.MultiDiGraph()

        vertex_color_map = []
        vertex_positions = {}
        has_none_pos = False
        for v in self.get_vertices():
            G.add_node(v.get_label())
            if v.is_source:
                vertex_color_map.append('green')
            elif v.is_target:
                vertex_color_map.append('blue')
            else:
                vertex_color_map.append('yellow')

            vertex_positions[v.get_label()] = v.pos
            if v.pos is None:
                has_none_pos = True

        arc_color_map = []
        for arc in self.get_arcs():
            G.add_edge(arc.get_tail().get_label(), arc.get_head().get_label())
            if arc.is_attackable:
                arc_color_map.append('red')
            else:
                arc_color_map.append('black')

        if has_none_pos:
            nx.draw(G, node_color=vertex_color_map, edge_color=arc_color_map)
        else:
            nx.draw(G, node_color=vertex_color_map, edge_color=arc_color_map, pos=vertex_positions, arrows=True)

        plt.show()
