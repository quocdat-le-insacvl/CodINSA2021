class Unit:

    def __init__(self, pos_building_spawn, pos, unit_type):
        self.pos_building_spawn = pos_building_spawn
        self.unit_type = unit_type
        self.pos = pos
        if unite_type == "V":
            self.price = 20
            self.life = 20
            self.attack = 10
            self.movement = 2
            self.score_killed = 10
            self.capability = "Construction de batiment, recolte de ressources"
            self.spawn_building = "S"
        elif unit_type == "L":
            self.price = 30
            self.life = 60
            self.attack = 20
            self.movement = 4
            self.score_killed = 15
            self.capability = None
            self.spawn_building = "Amphitheatre"
        else:
            self.price = 100
            self.life = 100
            self.attack = 40
            self.movement = 2
            self.score_killed = 35
            self.capability = None
            self.spawn_building = "Amphitheatre"

    def __str__(self):
        return "Type:{0}; Cout:{1}; Point de vie: {2}; Point attaque : {3}; Point de mouvement: {4}; Point gagne si tue : {5}; Capacite: {6}; Batiment de formation : {7};Position de batiment attitre: {8} ".format(self.unit_type,self.price, self.life, self.attack, self.movement, self.score_killed, self.capability, self.spawn_building, self.pos_building_spawn);

    def __repr__(self):
        return "Type:{0}; Cout:{1}; Point de vie: {2}; Point attaque : {3}; Point de mouvement: {4}; Point gagne si tue : {5}; Capacite: {6}; Batiment de formation : {7};Position de batiment attitre: {8} ".format(self.unit_type,self.price, self.life, self.attack, self.movement, self.score_killed, self.capability, self.spawn_building, self.pos_building_spawn);

    def get_letter(self):
        return self.unit_type
