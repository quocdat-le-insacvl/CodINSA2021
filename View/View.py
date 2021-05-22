import math


class View:
    def __init__(self):
        pass

    @staticmethod
    def convert_map(grid):
        for line in grid:
            for row in line:
                for case in row:
                    print(case.tiles_type, end="")
                    if case.building is not None:
                        print(case.building.building_type, end="")
                    elif case.unit is not None:
                        print(case.unit.unit_type, end="")
                    if case.owned == True:
                        print(1, end="")
                    elif case.owned == False:
                        print(2, end="")
                    print(" ", end="")
            print()
