from enum_type import *

style = {
    "rectangle": "block",
    "diamond": "decision",
    "circle": "start_end"
}

def draw_node(sorted_shape_lst):
    count = 0
    sorted_shape_lst[0].set_name("shape" + str(count))
    code = node_code_gen(style[sorted_shape_lst[0].get_shape()], sorted_shape_lst[0].get_name())
    
    for shape in sorted_shape_lst[1:]:
        count += 1
        name = "shape" + str(count)
        shape.set_name(name)
        code += node_code_gen(style[shape.get_shape()], name, "below", "shape" + str(count - 1))
    return sorted_shape_lst, code

def draw_edge(sorted_shape_lst, arrow_lst):
    code = ""
    for arrow in arrow_lst:
        print("arrow", arrow.get_center(), arrow.get_direction())
        minDis = 10000
        firstNode = None
        secondNode = None
        arrow_coord = 0
        for shape in sorted_shape_lst:
            shape_coord = 0
            if arrow.get_direction() == "horizontal":
                arrow_coord, _ = arrow.get_center()
                shape_coord, _ = shape.get_center()
                print(shape.get_center())
            else:
                _, arrow_coord = arrow.get_center()
                _, shape_coord = shape.get_center()
                print("2",shape.get_center())

            if abs(shape_coord - arrow_coord) < minDis:
                secondNode = firstNode
                firstNode = shape
                

        print(firstNode, secondNode)
        code += edge_code_gen(firstNode.get_name(), secondNode.get_name())

    return code



def node_code_gen(shape, name, relative_pos="", relative_obj=""):
    
    block_exp = "{}, {} of= {}".format(shape, relative_pos, relative_obj) if relative_obj != "" else shape
    return "\\node [{}] ({}) {{{}}};".format(block_exp, name, "placeholder") + '\n'

def edge_code_gen(node_from, node_to):
    return "\path [line] ({}) -- ({})".format(node_from, node_to) + '\n'