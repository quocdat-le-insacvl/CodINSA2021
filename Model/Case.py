from Model.Building import Building
from Model.Unit import Unit


class Case:

    def __init__(self, info, pos, game):
        self.game = game
        s = info.split(";")
        self.pos = pos
        self.tiles_type = s[0]
        self.cost = 1 if s[0] == "F" or s[0] == "A" else 2 if s[0] == "M" else 0
        self.building = Building(pos, s[1]) if len(s) != 1 and s[1] in ["C", "S", "T", "W"] else None
        self.unit = Unit(pos, s[1], game) if len(s) != 1 and s[1] in ["L", "V", "H"] else None
        self.life_point = s[2] if len(s) != 1 else ""
        self.visible = False

    def __str__(self):
        return "{0};{1};{2};{3}".format(self.tiles_type, self.building, self.unit, self.life_point)

    def __repr__(self):
        return "{0};{1};{2};{3}".format(self.tiles_type, self.building, self.unit, self.life_point)
