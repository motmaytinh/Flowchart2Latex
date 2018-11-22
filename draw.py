from enum_type import *

style = {
    "rectangle": "block",
    "diamond": "decision",
    "circle": "start_end"
}

def draw(sorted_shape_lst, bounding_rect):
    count = 0
    code = draw_node(style[sorted_shape_lst[0].get_shape()], "shape" + str(count)) + '\n'
    for shape in sorted_shape_lst:
        count += 1
        code += draw_node(style[shape.get_shape()], "shape" + str(count), "below", "shape" + str(count - 1)) + '\n'
    return code


def draw_node(shape, name, relative_pos="", relative_obj=""):
    
    block_exp = "{}, {} of= {}".format(shape, relative_pos, relative_obj) if relative_obj != "" else shape
    return "\\node [{}] ({}) {{{}}};".format(block_exp, name, "placeholder")

def draw_edge(node_from, node_to):
    return "\path [line] ({}) -- ({})".format(node_from, node_to)