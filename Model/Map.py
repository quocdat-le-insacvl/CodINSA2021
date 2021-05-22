import math

from Model.Case import Case

class Map:

    def __init__(self, json_map):
        rows = (json_map.splitlines())
        self.grid = []
        for i in range(len(rows)):
            mapped_line = []
            split_line = rows[i].split(" ")
            for j in range(len(split_line)):
                mapped_line.append(Case(split_line[j], (math.floor(j / 2), i, bool(j % 2))))
            self.grid.append(mapped_line)

    def __repr__(self):
        [print(''.join(str(ligne)).strip('[]')) for ligne in self.grid]
        return ""

    def __str__(self):
        [print(''.join(str(ligne)).strip('[]')) for ligne in self.grid]
        return ""
