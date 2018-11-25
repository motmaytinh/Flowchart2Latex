from enum_type import *

style = {
    "rectangle": "block",
    "diamond": "decision",
    "circle": "start_end"
}

def draw_node(sorted_shape_lst):
    count = 0
    sorted_shape_lst[0].set_name("shape" + str(count))
    code = node_code_gen(style[sorted_shape_lst[0].get_shape()], sorted_shape_lst[0].get_name()) + '\n'
    for shape in sorted_shape_lst:
        count += 1
        name = "shape" + str(count)
        shape.set_name(name)
        code += node_code_gen(style[shape.get_shape()], name, "below", "shape" + str(count - 1)) + '\n'
    return sorted_shape_lst, code

def draw_edge(sorted_shape_lst, arrow_lst):
    code = ""
    for arrow in arrow_lst:
        minDis = 10000
        firstNode = [None, minDis]
        secondNode = [None, minDis]
        arrow_coord = 0
        for shape in sorted_shape_lst:
            shape_coord = 0
            if arrow.get_direction() == "horizontal":
                arrow_coord, _ = arrow.get_center()
                shape_coord, _ = shape.get_center()
            else:
                _, arrow_coord = arrow.get_center()
                _, shape_coord = shape.get_center()
            if abs(shape_coord - arrow_coord) < firstNode[1]:
                firstNode[0] = shape
            elif abs(shape_coord - arrow_coord) < secondNode[1]:
                secondNode[0] = shape
        print(firstNode, secondNode)
        code += edge_code_gen(firstNode[0].get_name(), secondNode[0].get_name())

    return code



def node_code_gen(shape, name, relative_pos="", relative_obj=""):
    
    block_exp = "{}, {} of= {}".format(shape, relative_pos, relative_obj) if relative_obj != "" else shape
    return "\\node [{}] ({}) {{{}}};".format(block_exp, name, "placeholder")

def edge_code_gen(node_from, node_to):
    return "\path [line] ({}) -- ({})".format(node_from, node_to)