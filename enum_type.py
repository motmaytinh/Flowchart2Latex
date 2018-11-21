from enum import Enum

class Shape(Enum):
    rectangle = "rectangle"
    circle = "circle"
    diamond = "diamond"

class Position(Enum):
    left = "left"
    right = "right"
    below = "below"

class Shape_and_the_contour(object):
    def __init__(self, shape, contour):
        self.shape = shape
        self.coordinate = contour

    def get_cnts(self):
        return self.contour