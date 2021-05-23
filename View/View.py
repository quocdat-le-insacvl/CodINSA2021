import os


class View:
    def __init__(self):
        pass

    @staticmethod
    def convert_map(grid):
        result = ""
        for line in grid:
            for row in line:
                for case in row:
                    result += case.tiles_type  # case.tiles_type
                    if case.building is not None:
                        result += case.building.building_type
                    elif case.unit is not None:
                        print(case.unit.unit_type, end="")
                    if case.owned == True:
                        result += "1"
                    elif case.owned == False:
                        result += "2"
                    result += " "
            result += "\n"
        print(result)
        if os.path.isfile("out.txt"):
            with open('out.txt', 'w') as f:
                f.write(result)

