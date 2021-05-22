def pos_to_str(pos: tuple):
    return "[{0},{1},{2}]".format(pos[0], pos[1], "true" if pos[2] else "false")
