class Building:

    def __init__(self, pos, building_type):
        self.pos = pos 
        self.building_type = building_type
        if building_type == "S":
            self.can_attack = False
            self.price = None
            self.life = 240
            self.score_killed = 100
        elif building_type == "C":
            self.can_attack = False
            self.price = 250
            self.life = 160
            self.score_killed = 60
        elif building_type == "T":
            self.can_attack = True
            self.price = 70
            self.attack = 35
            self.life = 60
            self.attack_distance = 2
            self.score_killed = 30
        elif building_type == "W":
            self.can_attack = False
            self.price = 30
            self.life = 120
            self.score_killed = 15
        else: 
            assert "Error : Wrong building type!"

    def __repr__(self):
        return "type {0}; life {1}; price{2}".format(self.building_type, self.life, self.price)

    def __str__(self):
        return "type {0}; life {1}; price{2}".format(self.building_type, self.life, self.price)

    def get_letter(self):
        return self.building_type




