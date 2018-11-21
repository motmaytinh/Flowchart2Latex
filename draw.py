from enum_type import *

def draw_node(shape, name, relative_pos="", relative_obj=""):
    block_exp = "{}, {} of= {}".format(shape, relative_pos, relative_obj) if relative_obj != "" else shape
    return "\node [{}] ({}) {{{}}};".format(block_exp, name, "placeholder")

def draw_edge(node_from, node_to):
    return "\path [line] ({}) -- ({})".format(node_from, node_to)