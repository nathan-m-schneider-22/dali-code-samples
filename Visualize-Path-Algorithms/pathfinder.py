from network import *
from path_algorithms import *
from que import *


class Pathfinder:
    def __init__(self, start_vertex, end_vertex, graph, type):
        self.animate_frame = 1
        self.animate_delay = 10
        self.end_vertex = end_vertex
        self.start_vertex = start_vertex
        self.visited = []

        if type == "Depth First Search":
            start_vertex.backpointer = None
            self.depth_first_search(start_vertex)

        if type == "Breadth First Search":
            self.breadth_first_search(graph)

        if type == "Dijstra's Algorithm":
            self.best_first_search(graph, False)

        if type == "A* Search":
            self.best_first_search(graph, True)

    def draw_backpointers(self, vertex):
        current_vertex = vertex
        while current_vertex.backpointer != None:
            set_stroke_width(4)
            current_vertex.draw_line(current_vertex.backpointer, 1, 1, 0)
            current_vertex = current_vertex.backpointer

    def animate(self):
        if self.animate_frame // self.animate_delay <= len(self.visited):
            for i in range(self.animate_frame // self.animate_delay):
                self.draw_backpointers(self.visited[i])
        elif self.animate_frame // self.animate_delay > len(self.visited):
            self.draw_backpointers(self.end_vertex)
        self.animate_frame += 1

    def depth_first_search(self, current_vertex):
        self.visited.append(current_vertex)
        if current_vertex == self.end_vertex:
            return
        for neighbor in current_vertex.neighbors:
            if neighbor not in self.visited and self.end_vertex not in self.visited:
                neighbor.backpointer = current_vertex
                self.depth_first_search(neighbor)

    def breadth_first_search(self,graph):
        self.visited = [self.start_vertex]
        que = Que()
        que.append(self.start_vertex)
        self.start_vertex.backpointer = None

        while self.end_vertex not in self.visited:
            popped = que.popleft()
            self.visited.append(popped)
            for neighbor in popped.neighbors:
                if neighbor not in self.visited:
                    neighbor.backpointer = popped
                    self.visited.append(neighbor)
                    que.append(neighbor)
            if que.is_empty():
                self.end_vertex.backpointer = None
                return

    def best_first_search(self, graph, direction_weighting):
        graph.reset()
        self.start_vertex.distance = 0
        self.start_vertex.backpointer = None
        count = 1
        current_vertex = self.start_vertex
        while current_vertex is not self.end_vertex:
            current_vertex.order = count
            self.visited.append(current_vertex)
            for neighbor in current_vertex.neighbors:
                if neighbor not in self.visited and \
                        current_vertex.distance + current_vertex.get_cartesian_distance(neighbor) < neighbor.distance:
                    neighbor.distance = current_vertex.get_cartesian_distance(neighbor) + current_vertex.distance
                    neighbor.backpointer = current_vertex

            current_vertex = self.find_min(graph, direction_weighting)
            if current_vertex==None:
                self.end_vertex.backpointer = None
                return

    def find_min(self, graph, direction_weighting):
        min_dis = inf
        min_vertex = None
        for vertex in graph.vertex_list:
            if direction_weighting:
                if vertex.distance + vertex.get_cartesian_distance(self.end_vertex) < min_dis \
                        and vertex not in self.visited:
                    min_dis = vertex.distance + vertex.get_cartesian_distance(self.end_vertex)
                    min_vertex = vertex
            else:
                if vertex.distance < min_dis and vertex not in self.visited:
                    min_dis = vertex.distance
                    min_vertex = vertex

        return min_vertex
