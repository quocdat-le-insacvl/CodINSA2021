import math

from Model.Case import Case


class Map:

    def __init__(self, json_map):
        rows = (json_map.splitlines())
<<<<<<< HEAD
        self.height = len(rows)
        self.grid = []
        for row in rows:
            row = row.split(" ")
            self.width = len(row)
            y_dimension = []
            i = 0
            while i<len(row):
                z_dimension = []
                z_dimension.append(row[i])
                z_dimension.append(row[i+1])
                i += 2
                y_dimension.append(z_dimension)
            self.grid.append(y_dimension)
        print("test map : height + width == ", self.height, self.width)
        for x in self.grid:
            for y in x:
                for z in y:
                    print(z, end="/") 
                print(" ", end="")
            print()
=======
        self.grid = []
        for i in range(len(rows)):
            mapped_line = []
            split_line = rows[i].split(" ")
            for j in range(len(split_line)):
                mapped_line.append(Case(split_line[j], (math.floor(j / 2), i, bool(j % 2))))
            self.grid.append(mapped_line)
>>>>>>> 0d617e4e4715f3e43f4baa7bebecc62a4c916c38

    def __repr__(self):
        [print(''.join(str(ligne)).strip('[]')) for ligne in self.grid]
        return ""

    def __str__(self):
        [print(''.join(str(ligne)).strip('[]')) for ligne in self.grid]
        return ""
