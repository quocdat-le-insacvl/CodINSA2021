class Building:

    def __init__(self, pos, building_type):
        self.pos = pos
        self.building_type = building_type
        if building_type == "S":
            self.can_attack = False
            self.price = None
            self.life = 240
            self.score_killed = 100
            self.unit = ["V"]
        elif building_type == "C":
            self.can_attack = False
            self.price = 250
            self.life = 160
            self.score_killed = 60
            self.unit = ["L", "H"]
        elif building_type == "T":
            self.can_attack = True
            self.price = 70
            self.attack = 35
            self.life = 60
            self.attack_distance = 2
            self.score_killed = 30
            self.unit = []
        elif building_type == "W":
            self.can_attack = False
            self.price = 30
            self.life = 120
            self.score_killed = 15
            self.unit = []
        else: 
            assert "Error : Wrong building type!"

    def __repr__(self):
        return "type {0}; life {1}; price{2}".format(self.building_type, self.life, self.price)

    def __str__(self):
        return "type {0}; life {1}; price{2}".format(self.building_type, self.life, self.price)

    def get_letter(self):
        return self.building_type

    def create_unit(self):
        possible_pos = [[1, 0, 0], [0, -1, 0], [0, 0, 0]] if self.pos[2] else [[-1, 0, 1], [0, 1, 1], [0, 0, 1]]
        unit = {"V": [], "L": [], "H": []}
        for (x, y, bool) in possible_pos:
            unit["V"].append([self.pos[0] + x, self.pos[1] + y, bool])
        return unit



