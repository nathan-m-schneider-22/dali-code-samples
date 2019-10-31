from vertex import *

"""
Nathan Schneider
network.py
This network class is the class used to build the entire 
graph seen in the interface. It supports methods for
modifying the graph, updating its nodes/edges, and generating
new graphs quickly. 
"""

class Network:
    def __init__(self, vertex_count, spacing, degree):
        self.vertex_list = []
        self.spacing = spacing
        self.degree = degree
        for i in range(vertex_count):
            self.add_vertex()
        self.generate_edges()

    def add_vertex(self):
        new_vertex = Vertex()
        while not self.check(new_vertex, self.spacing):
            new_vertex = Vertex()
        self.vertex_list.append(new_vertex)

    def add_edged_vertex(self):
        self.add_vertex()
        for i in range(self.degree):
            self.add_edge(self.vertex_list[-1])

    def add_edge(self, vertex, bad_vertex=None):
        mindis = inf
        minvertex = None
        for other in self.vertex_list:
            if vertex.get_cartesian_distance(other) < mindis and other not in vertex.neighbors \
                    and other is not vertex and other is not bad_vertex:
                mindis = vertex.get_cartesian_distance(other)
                minvertex = other
        if not minvertex == None:
            vertex.neighbors.append(minvertex)
            minvertex.neighbors.append(vertex)

    def generate_edges(self):
        for i in range(self.degree):
            for vertex in self.vertex_list:
                self.add_edge(vertex)

    def increment_edges(self):
        self.degree += 1
        for vertex in self.vertex_list:
            if len(vertex.neighbors) < self.degree:
                self.add_edge(vertex)

    def remove_edge(self):
        self.degree = max(0, self.degree - 1)
        for vertex in self.vertex_list:
            if len(vertex.neighbors) > 0:
                vertex.neighbors[-1].neighbors.remove(vertex)
                del vertex.neighbors[-1]

    def remove_vertex(self):
        if not len(self.vertex_list) == 0:
            for vertex in self.vertex_list:
                if self.vertex_list[-1] in vertex.neighbors:
                    vertex.neighbors.remove(self.vertex_list[-1])
                    if len(vertex.neighbors) == 0:
                        self.add_edge(vertex, self.vertex_list[-1])
            del self.vertex_list[-1]

    def check(self, new_vertex, spacing):
        for vertex in self.vertex_list:
            if vertex.get_cartesian_distance(new_vertex) < spacing:
                return False
        return True

    def draw(self):
        set_stroke_width(1)
        for vertex in self.vertex_list:
            vertex.draw()
            vertex.draw_edges()

    def spin_left(self):
        for vertex in self.vertex_list:
            vertex.spin_left()

    def spin_right(self):
        for vertex in self.vertex_list:
            vertex.spin_right()

    def update(self):
        if mouse_x() < WIDTH / 8 and mouse_y() > HEIGHT / 8:
            self.spin_right()
        if mouse_x() > WIDTH - WIDTH / 8 and mouse_y() > HEIGHT / 8:
            self.spin_left()

    def reset(self):
        for vertex in self.vertex_list:
            vertex.distance = inf
