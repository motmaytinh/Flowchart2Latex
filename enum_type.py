from enum import Enum

class Shape(Enum):
    rectangle = "rectangle"
    circle = "circle"
    diamond = "diamond"
    ellipse = "ellipse"
    rhombus = "rhombus"

class Position(Enum):
    left = "left"
    right = "right"
    above = "above"
    below = "below"

class Arrow(object):
    def __init__(self, direction, contour, center):
        self.direction = direction
        self.contour = contour
        self.center = center

    def get_direction(self):
        return self.direction

    def get_center(self):
        return self.center

class Shape_and_the_contour(object):
    def __init__(self, shape, contour, center):
        self.shape = shape
        self.contour = contour
        self.center = center
        self.anchor = False

    def get_cnts(self):
        return self.contour

    def get_shape(self):
        return self.shape.name

    def get_center(self):
        return self.center

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_anchor(self):
        self.anchor = True

    def get_anchor(self):
        return self.anchor