from random import random
from cs1lib import *
from math import sin, cos, pi, inf
"""
Nathan Schneider
vertex.py is my own class for node/vertices
They exist in spherical coordinates with lists
of neighbors, and a backpoint when 
doing graph searches. 

"""



# These globals define window size, the scale of the visuals, spin speed,
# and the amount the nodes get larger when they are "closer"
HEIGHT = 1000
WIDTH = 1000
SCALE = min(WIDTH, HEIGHT) / 3
SPIN_SPEED = .04
SWELL = 5


class Vertex:
    def __init__(self):
        #Each vertex is a point in space, defined in spherical coordinates
        #Using spherical coordinates works well for this project as it makes
        #rotation laughably simply if translation is not needed
        #A sphere full of these points are created
        self.rho = random()
        self.phi = random() * pi
        self.theta = random() * 2 * pi

        #Each point also has graph information
        self.neighbors = []
        self.distance = inf
        self.backpointer = None


        #The points are drawn in psuedo-3D, with "camera" pointing down the x
        # axis towards the origin
        #Therefore, the points are plotted in 2D with y and z values.
    def draw(self, r=1, g=1, b=1, expand=1):
        y, z = self.get_display()
        alpha = self.get_x() / 2 + .5
        set_stroke_color(r, g, b, alpha)

        set_fill_color(r, g, b)
        draw_circle(y, z, expand + SWELL * (1 + self.get_x()))


    #Draw all edges between this and neighbor nodes
    def draw_edges(self):
        for neighbor in self.neighbors:
            alpha = self.rho * sin(self.phi) * cos(self.theta) / 2 + .5
            set_stroke_color(1, 1, 1, alpha)
            self\
                .draw_line(neighbor)

    #Draw a line
    def draw_line(self, other, r=1, g=1, b=1):
        y1, z1 = self.get_display()
        y2, z2 = other.get_display()
        set_stroke_color(r, g, b)
        draw_line(y1, z1, y2, z2)


    #Spin the node
    def spin_left(self):
        self.theta += SPIN_SPEED

    def spin_right(self):
        self.theta -= SPIN_SPEED

    #convert spherical coordinates to cartesian
    def get_cartesian(self):
        x = self.rho * sin(self.phi) * cos(self.theta)
        y = self.rho * sin(self.phi) * sin(self.theta)
        z = self.rho * cos(self.phi)
        return x, y, z


    def get_display(self):
        y = WIDTH / 2 + SCALE * self.rho * sin(self.phi) * sin(self.theta)
        z = HEIGHT / 2 - SCALE * cos(self.phi) * self.rho
        return y, z

    def get_cartesian_distance(self, other):
        x1, y1, z1 = self.get_cartesian()
        x2, y2, z2 = other.get_cartesian()
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** .5

    def get_size(self):
        return SWELL * (1 + self.get_x)

    def get_x(self):
        return self.rho * sin(self.phi) * cos(self.theta)

    def __str__(self):
        return "Rho: %f,Phi: %f,Theta:%f" % (self.rho, self.phi, self.theta)
