from enum_type import *

style = {
    "rectangle": "block",
    "diamond": "decision",
    "circle": "start_end"
}

def draw(sorted_shape_lst, arrow_lst):
    code = node_code_gen(style[sorted_shape_lst[0].get_shape()], sorted_shape_lst[0].get_name())
    delta = 100
    sorted_shape_lst[0].set_anchor()
    for arrow in arrow_lst:
        minDis = 10000
        firstNode = None
        secondNode = None
        arrow_x, arrow_y = arrow.get_center()
        print('arrow',arrow.get_center())
        for shape in sorted_shape_lst:
            shape_x, shape_y = shape.get_center()
            if arrow.get_direction() == "horizontal":
                if abs(arrow_y - shape_y) < delta:
                    if abs(arrow_x - shape_x) < minDis:
                        secondNode = firstNode
                        firstNode = shape
                        minDis = arrow_x - shape_x
                        print('shape',shape.get_center())
            elif abs(arrow_x - shape_x) < delta:
                if abs(arrow_y - shape_y) < minDis:
                    secondNode = firstNode
                    firstNode = shape
                    minDis = arrow_y - shape_y
                    print('shape',shape.get_center())
        if secondNode is None:
            minDis = 10000
            for shape in sorted_shape_lst:
                if arrow.get_direction() == "horizontal":
                    if abs(arrow_y - shape_y) < delta:
                        if abs(arrow_x - shape_x) < minDis:
                            if shape is not firstNode:
                                secondNode = shape
                                minDis = arrow_x - shape_x
                                print('shape',shape.get_center())
                elif abs(arrow_x - shape_x) < delta:
                    if abs(arrow_y - shape_y) < minDis:
                        if shape is not firstNode:
                            secondNode = shape
                            minDis = arrow_y - shape_y
                            print('shape',shape.get_center())
        # print(firstNode, secondNode)
        if arrow.get_direction() == "horizontal":
            x1, _ = firstNode.get_center()
            x2, _ = secondNode.get_center()
            if (x1 < x2):
                code += node_code_gen(style[secondNode.get_shape()], secondNode.get_name(), Position.right.name, firstNode.get_name())
            else:
                code += node_code_gen(style[firstNode.get_shape()], firstNode.get_name(), Position.right.name, secondNode.get_name())
        else:
            _, y1 = firstNode.get_center()
            _, y2 = secondNode.get_center()
            if (y1 < y2):
                if firstNode.get_anchor():
                    code += node_code_gen(style[secondNode.get_shape()], secondNode.get_name(), Position.below.name, firstNode.get_name())
                else:
                    code += node_code_gen(style[firstNode.get_shape()], firstNode.get_name(), Position.above.name, secondNode.get_name())
            else:
                if secondNode.get_anchor():
                    code += node_code_gen(style[firstNode.get_shape()], firstNode.get_name(), Position.below.name, secondNode.get_name())
                else:
                    code += node_code_gen(style[secondNode.get_shape()], secondNode.get_name(), Position.above.name, firstNode.get_name())

        firstNode.set_anchor()
        secondNode.set_anchor()
        code += edge_code_gen(secondNode.get_name(), firstNode.get_name())

    return code



def node_code_gen(shape, name, relative_pos="", relative_obj=""):
    block_exp = "{}, {} of= {}".format(shape, relative_pos, relative_obj) if relative_obj != "" else shape
    return "\\node [{}] ({}) {{{}}};\n".format(block_exp, name, "placeholder")

def edge_code_gen(node_from, node_to):
    return "\path [line] ({}) -- ({});\n".format(node_from, node_to)