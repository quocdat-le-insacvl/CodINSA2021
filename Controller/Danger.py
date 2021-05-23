from Controller.Util import str_to_pos
from Controller.Util import distance
import Model.Unit


class Danger:

    def __init__(self):
        # the first in each list are the most dangerous
        # offensive tower go first, then enemy unit that are already next to his target and then the other units
        self.spawn = []
        self.resources = []
        self.buildings = []
        self.units = []

    def check(self, map, visible, units, buildings, spawn):
        # todo resources
        self.spawn = []
        self.resources = []
        self.buildings = []
        self.units = []
        unit_threats = []
        tower_threats = []
        for pos in visible:
            x, y, down = str_to_pos(pos)

            # if there's smth on the tile   and it's a tower           and not ours
            if len(visible[pos]) > 1 and visible[pos][2] == "T" and len([b for b in buildings if b.pos == [x, y, down]]) == 0:
                tower_threats.append((x, y, down))

            # if there's smth on the tile      and it's an unit                     and not ours
            if len(visible[pos]) > 1 and visible[pos][2] in ["V", "L", "H"] and len([u for u in units if u.pos == [x, y, down]]) == 0:
                unit_threats.append((x, y, down))

        # uses distance() so not precise if there is an abyss/a wall
        # todo sort threat according to distance and damages
        # sort the threat according to the thing they are threatening by using there distance
        # an enemy unit is considered a threat at 3 or less movement cost, can be changed
        for t in unit_threats:
            for u in units:
                # distance between our unit and the threat
                dist = distance(t, u.pos)
                if dist == 1:  # the threat is next to our unit
                    if t in self.units:  # threat already seen as a threat
                        self.units.remove(t)  # remove the old because now it is top priority
                    self.units.insert(0, t)  # insert the threat at the top of the threat list
                elif dist <= 3:  # the threat if far from our unit
                    if t in self.units:  # threat already seen as a threat
                        continue  # no need to insert it
                    self.units.append(t)  # append the threat to the threat list

            # same goes for buildings
            for b in buildings:
                dist = distance(t, b.pos)
                if dist == 1:
                    if t in self.buildings:
                        self.buildings.remove(t)
                    self.buildings.insert(0, t)
                elif dist <= 3:
                    if t in self.buildings:
                        continue
                    self.buildings.append(t)

            # same goes for spawn
            dist = distance(t, spawn)
            if dist == 1:
                self.spawn.insert(0, t)
            elif dist <= 3:
                self.spawn.append(t)

        # a tower has a range of 2 tiles and cannot move so it is considered a threat a 2 or less tiles
        # insert first because it is more dangerous than anything
        for t in tower_threats:
            for u in units:
                dist = distance(t, u.pos)
                if t in self.unit:  # threat already seen as a threat
                    continue  # no need to add it
                if dist <= 2:  # our unit is in tower's range
                    self.units.insert(0, t)  # insert the tower at the top of the threat list

            # same for buildings
            for b in buildings:
                dist = distance(t, b.pos)
                if t in self.buildings:
                    continue
                if dist <= 2:
                    self.buildings.insert(0, t)

            # same for spawn
            dist = distance(t, spawn)
            if dist <= 2:
                self.spawn.insert(0, t)



