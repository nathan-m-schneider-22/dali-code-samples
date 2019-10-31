from network import *
from pathfinder import *
from button import *
"""
Nathan Schneider
interface.py
This is the interface code for the display, with callbacks for
clicking, mouse interaction and drawing the image
"""


NODE_COUNT = 30
DEGREE = 2


def is_over(object, mx, my):
    if type(object) == Vertex:
        error = 5 * (1 + object.get_x())
        # error = 5
        x, y = object.get_display()
        if mx - error < x < mx + error and my - error < y < my + error:
            return True

    elif type(object) == Button:
        x = object.x
        y = object.y
        if x < mx < x + object.width and y < my < y + object.height:
            return True

    return False


class Interface:
    def __init__(self):
        self.node_count = NODE_COUNT
        self.spacing = .2
        self.degree = DEGREE
        self.net = Network(self.node_count, self.spacing, self.degree)
        self.types = ['Depth First Search', "Breadth First Search", "Dijstra's Algorithm", "A* Search"]
        self.type_count = 1
        self.start_vertex = None
        self.end_vertex = None
        self.type = self.types[self.type_count]
        self.path = None
        self.animate_delay = 10
        self.button_list = []
        self.create_buttons()


    def new_net(self):
        self.net = Network(self.node_count, self.spacing, self.degree)

    def add_vertex(self):
        self.net.add_edged_vertex()
        self.node_count += 1

    def remove_vertex(self):
        if self.node_count > 0:
            self.node_count -= 1
            self.net.remove_vertex()

    def increase_degree(self):
        self.degree += 1
        self.net.increment_edges()

    def decrease_degree(self):
        self.degree = max(0, self.degree - 1)
        self.net.remove_edge()

    def reset(self):
        self.degree = DEGREE
        self.node_count = NODE_COUNT
        self.new_net()

    def change_mode(self):
        self.type_count += 1
        self.type = self.types[self.type_count % 4]
        self.button_list[5].text = "Change Mode: " + self.type

    def create_buttons(self):
        self.button_list.append(Button(0, 0, 160, 35, "Add Vertex", self.add_vertex))
        self.button_list.append(Button(160, 0, 220, 35, "Remove Vertex", self.remove_vertex))
        self.button_list.append(Button(380, 0, 240, 35, "Increase Edges", self.increase_degree))
        self.button_list.append(Button(620, 0, 240, 35, "Decrease Edges", self.decrease_degree))
        self.button_list.append(Button(860, 0, 240, 35, "Generate Network", self.new_net))
        self.button_list.append(Button(0, 35, 520, 35, "Change Mode: " + self.type, self.change_mode))
        self.button_list.append(Button(520,35,320,35,"Status: ",self.update))
    def draw(self):

        self.net.draw()
        for button in self.button_list:
            button.draw()

        if self.start_vertex != None:
            self.start_vertex.draw(1, 0, 0, 5)

        if self.path != None:
            self.path.animate()
            if self.end_vertex.backpointer!=None:
                self.button_list[6].text = "Status: Path Found"
            else:
                self.button_list[6].text = "Status: Not Found"
        if self.end_vertex != None:
            self.end_vertex.draw(0, .8, 0, 5)

    def update(self):
        self.net.update()

    def mouse_press(self, mx, my):
        min_x = -1
        self.start_vertex = None
        for vertex in self.net.vertex_list:
            if is_over(vertex, mx, my):
                if vertex.get_x() > min_x and vertex != self.end_vertex:
                    self.start_vertex = vertex
                    min_x = vertex.get_x()
        for button in self.button_list:
            if is_over(button, mx, my):
                button.do()
        self.path = None
        self.end_vertex = None

    def mouse_move(self, mx, my):
        min_x = -1
        old_vertex = self.end_vertex
        # self.end_vertex = None
        # self.path = None
        for vertex in self.net.vertex_list:
            if is_over(vertex, mx, my):
                if vertex.get_x() > min_x and self.start_vertex != None:
                    self.end_vertex = vertex
                    min_x = vertex.get_x()
        if self.start_vertex != None and self.end_vertex != None \
                and self.end_vertex != old_vertex:
            self.make_path()
        if self.start_vertex == self.end_vertex:
            self.path = None

    def make_path(self):
        self.path = Pathfinder(self.start_vertex, self.end_vertex, self.net, self.type)
