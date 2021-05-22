from Model.Case import Case

class Map:

    def __init__(self, json_map):
        rows = (json_map.splitlines())
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

    def __repr__(self):
        [print(''.join(str(ligne)).strip('[]')) for ligne in self.grid]
        return ""

    def __str__(self):
        [print(''.join(str(ligne)).strip('[]')) for ligne in self.grid]
        return ""
