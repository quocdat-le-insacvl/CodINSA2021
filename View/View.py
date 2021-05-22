import math


class View:
    def __init__(self):
        pass

    def convert_map(self, data):
        game_map = []
        rows = data["map"].splitlines()
        for i in range(len(rows)):
            mapped_line = []
            split_line = rows[i].split(" ")
            for j in range(len(split_line)):
                mapped_line.append([math.floor(j / 2), i, bool(j % 2)])
            game_map.append(mapped_line)