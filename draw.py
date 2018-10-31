def draw_shape(shape, name, relative_pos="", relative_obj=""):
    block_exp = "{}, {} of= {}".format() if relative_obj != "" else shape
    return "\node [{}] ({}) {{{}}};".format(block_exp, name, name)

