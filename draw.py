from enum_type import *

DELTA = 100

style = {
    "rectangle": "block",
    "diamond": "decision",
    "circle": "start_end",
    "ellipse": "my_ellipse",
    "rhombus": "io"
}


def draw(sorted_shape_lst, arrow_lst):
    code_node = node_code_gen(
        style[sorted_shape_lst[0].get_shape()], sorted_shape_lst[0].get_name())
    code_edge = ''
    sorted_shape_lst[0].set_anchor()

    for arrow in arrow_lst:
        minDis = 10000
        firstNode = [None, minDis]
        secondNode = [None, minDis]
        arrow_x, arrow_y = arrow.get_center()
        # print('arrow',arrow.get_center())
        # print(arrow.get_direction())
        for shape in sorted_shape_lst:
            shape_x, shape_y = shape.get_center()
            if arrow.get_direction() == "horizontal":
                if abs(arrow_y - shape_y) < DELTA:
                    if abs(arrow_x - shape_x) < minDis:
                        secondNode[0] = firstNode[0]
                        secondNode[1] = firstNode[1]
                        firstNode[0] = shape
                        minDis = abs(arrow_x - shape_x)
                        # print('shape',shape.get_center())
                    elif abs(arrow_x - shape_x) < secondNode[1] and firstNode[0] is not shape:
                        secondNode[0] = shape
                        secondNode[1] = abs(arrow_y - shape_y)
            elif abs(arrow_x - shape_x) < DELTA:
                # print("< delta")
                if abs(arrow_y - shape_y) < firstNode[1]:
                    secondNode[0] = firstNode[0]
                    secondNode[1] = firstNode[1]
                    firstNode[0] = shape
                    firstNode[1] = abs(arrow_y - shape_y)
                elif abs(arrow_y - shape_y) < secondNode[1] and firstNode[0] is not shape:
                    secondNode[0] = shape
                    secondNode[1] = abs(arrow_y - shape_y)
        if secondNode[0] is None:
            # print('None')
            minDis = 10000
            for shape in sorted_shape_lst:
                shape_x, shape_y = shape.get_center()
                if arrow.get_direction() == "horizontal":
                    if abs(arrow_y - shape_y) < DELTA:
                        if abs(arrow_x - shape_x) < minDis:
                            if shape is not firstNode:
                                secondNode = shape
                                minDis = abs(arrow_x - shape_x)
                                # print('shape second',shape.get_center())
                elif abs(arrow_x - shape_x) < DELTA:
                    # print('< delta 2')
                    if abs(arrow_y - shape_y) < minDis:
                        if shape is not firstNode:
                            secondNode = shape
                            minDis = abs(arrow_y - shape_y)
                            # print('shape second',shape.get_center())
        # print(firstNode, secondNode)
        if arrow.get_direction() == "horizontal":
            x1, _ = firstNode[0].get_center()
            x2, _ = secondNode[0].get_center()
            if (x1 < x2):
                if firstNode[0].get_anchor():
                    code_node += node_code_gen(style[secondNode[0].get_shape(
                    )], secondNode[0].get_name(), Position.right.name, firstNode[0].get_name())
                elif secondNode[0].get_anchor():
                    code_node += node_code_gen(style[firstNode[0].get_shape(
                    )], firstNode[0].get_name(), Position.left.name, secondNode[0].get_name())
                else:
                    arrow_lst.append(arrow)
                    continue
            else:
                if secondNode[0].get_anchor():
                    code_node += node_code_gen(style[firstNode[0].get_shape(
                    )], firstNode[0].get_name(), Position.right.name, secondNode[0].get_name())
                elif firstNode[0].get_anchor():
                    code_node += node_code_gen(style[secondNode[0].get_shape(
                    )], secondNode[0].get_name(), Position.left.name, firstNode[0].get_name())
                else:
                    arrow_lst.append(arrow)
                    continue
        else:
            _, y1 = firstNode[0].get_center()
            _, y2 = secondNode[0].get_center()
            if (y1 < y2):
                if firstNode[0].get_anchor():
                    code_node += node_code_gen(style[secondNode[0].get_shape(
                    )], secondNode[0].get_name(), Position.below.name, firstNode[0].get_name())
                elif secondNode[0].get_anchor():
                    code_node += node_code_gen(style[firstNode[0].get_shape(
                    )], firstNode[0].get_name(), Position.above.name, secondNode[0].get_name())
                else:
                    arrow_lst.append(arrow)
                    continue
            else:
                if secondNode[0].get_anchor():
                    code_node += node_code_gen(style[firstNode[0].get_shape(
                    )], firstNode[0].get_name(), Position.below.name, secondNode[0].get_name())
                elif firstNode[0].get_anchor():
                    code_node += node_code_gen(style[secondNode[0].get_shape(
                    )], secondNode[0].get_name(), Position.above.name, firstNode[0].get_name())
                else:
                    arrow_lst.append(arrow)
                    continue

        firstNode[0].set_anchor()
        secondNode[0].set_anchor()
        code_edge += edge_code_gen(secondNode[0].get_name(),
                                   firstNode[0].get_name())

    return code_node + code_edge


def node_code_gen(shape, name, relative_pos="", relative_obj=""):
    block_exp = "{}, {} of= {}".format(
        shape, relative_pos, relative_obj) if relative_obj != "" else shape
    return "\\node [{}] ({}) {{{}}};\n".format(block_exp, name, name)


def edge_code_gen(node_from, node_to):
    return "\path [line] ({}) -- ({});\n".format(node_from, node_to)
