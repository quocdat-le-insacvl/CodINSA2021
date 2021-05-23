import math

from Model.Building import Building
from Model.Case import Case
from View.View import View

from Controller.Util import distance
from Controller.Util import adjPos
from Controller.Util import PriorityQueue

class Map:

    def __init__(self, json_map, spawn):
        rows = (json_map.splitlines())
        self.height = len(rows)
        self.grid = []
        self.list_unit = []
        self.list_building = []
        i = 0
        for row in rows:
            row = row.split(" ")
            self.width = len(row)
            y_dimension = []
            j = 0
            while j < len(row):
                z_dimension = []
                z_dimension.append(Case(row[j], (j//2, i, 0), None))
                z_dimension.append(Case(row[j+1], ((j+1)//2, i, 1), None))
                j += 2
                y_dimension.append(z_dimension)
            self.grid.append(y_dimension)
            i += 1
        self.spawn = Building((spawn[0], spawn[1], spawn[2]), "S")
        self.grid[spawn[1]][spawn[0]][spawn[2]].building = self.spawn
        self.grid[spawn[1]][spawn[0]][spawn[2]].owned = True
        self.list_building = [self.spawn]
            
    def isValid(self, pos):
        return pos[0]>=0 and pos[0]<self.height and pos[1]>=0 and pos[1]<self.width and self.grid[pos[0]][pos[1]][pos[2]].tiles_type !="A" and self.grid[pos[0]][pos[1]][pos[2]].tiles_type !="R"

    def pathFinder(self, start, finish):
        pile = PriorityQueue()
        visited = set()

        pile.push((start, []), distance(start, finish))
        visited.add(start)
        finded = False

        while not pile.empty() and not finded:
            current, route = pile.pop()
            for next in adjPos(current):
                if next not in visited and self.isValid(next):
                    if next==finish:
                        pile.push((next, route+[next]), -1)
                        finded = True
                        break
                    else:
                        pile.push((next, route+[next]), distance(next, finish))
                        visited.add(next)

        if finded:
            return pile.pop()[1]
        else:
            return None

    def __repr__(self):
        [print(''.join(str(ligne)).strip('[]')) for ligne in self.grid]
        return ""

    def __str__(self):
        [print(''.join(str(ligne)).strip('[]')) for ligne in self.grid]
        return ""
