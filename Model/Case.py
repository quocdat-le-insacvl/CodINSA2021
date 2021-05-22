from Model.Building import Building
from Model.Unit import Unit


class Case:

    def __init__(self, info, pos):
        s = info.split(";")
        self.tiles_type = s[0]
        self.build_type = Building(pos, s[1]) if len(s) != 1 and s in ["C", "S", "T", "W"] else None
        self.unit_type = Unit(pos, s[1]) if len(s) != 1 and s in ["L", "V", "H"] else None
        self.life_point = s[2] if len(s) != 1 else ""
        self.pos = pos

    def __str__(self):
        return "{0};{1};{2}".format(self.tiles_type, self.build_type, self.life_point)

    def __repr__(self):
        return "{0};{1};{2}".format(self.tiles_type, self.build_type, self.life_point)
