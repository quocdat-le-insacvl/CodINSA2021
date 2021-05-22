from Model.Case import Case

class Map:

    def __init__(self, json_map):
        rows = (json_map.splitlines())
        self.grid = [[Case(info) for info in row.split(" ")] for row in rows]
        print(self.grid)

    def __repr__(self):
        [print(''.join(str(ligne)).strip('[]')) for ligne in self.grid]
        return ""

    def __str__(self):
        [print(''.join(str(ligne)).strip('[]')) for ligne in self.grid]
        return ""
