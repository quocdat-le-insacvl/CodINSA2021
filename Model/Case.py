from Model.Building import Building
from Model.Unit import Unit


class Case:

    def __init__(self, info, pos, owned):
        s = info.split(";")
        self.pos = pos
        self.owned = owned
        self.tiles_type = s[0]
        self.building = Building(pos, s[1]) if len(s) != 1 and s[1] in ["C", "S", "T", "W"] else None
        self.unit = Unit(pos, s[1]) if len(s) != 1 and s[1] in ["L", "V", "H"] else None
        self.life_point = s[2] if len(s) != 1 else ""

        if self.owned is None and len(s) != 1 and s[1] in ["S", "L", "V", "H"]:  # Others spawn or units
            self.owned = False

    def __str__(self):
        return "{0};{1};{2};{3}".format(self.tiles_type, self.building, self.unit, self.life_point)

    def __repr__(self):
        return "{0};{1};{2};{3}".format(self.tiles_type, self.building, self.unit, self.life_point)
