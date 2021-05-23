import random


class Unit:

    def __init__(self, pos, unit_type, isOur):
        self.pos = pos
        self.unit_type = unit_type
        self.isOur = isOur
        if unit_type == "V":
            self.price = 20
            self.life = 20
            self.attack = 10
            self.movement = 2
            self.score_killed = 10
            self.spawn_building = "S"
            self.canBuild = True
        elif unit_type == "L":
            self.price = 30
            self.life = 60
            self.attack = 20
            self.movement = 4
            self.score_killed = 15
            self.spawn_building = "Amphitheatre"
            self.canBuild = False
        else:
            self.price = 100
            self.life = 100
            self.attack = 40
            self.movement = 2
            self.score_killed = 35
            self.spawn_building = "Amphitheatre"
            self.canBuild = False

    def __str__(self):
        return "Type:{0}; Cout:{1}; Point de vie: {2}; Point attaque : {3}; Point de mouvement: {4}; Point gagne si tue : {5}; Capacite: {6}; Batiment de formation : {7}".format(self.unit_type,self.price, self.life, self.attack, self.movement, self.score_killed, self.capability, self.spawn_building,)

    def __repr__(self):
        return "Type:{0}; Cout:{1}; Point de vie: {2}; Point attaque : {3}; Point de mouvement: {4}; Point gagne si tue : {5}; Capacite: {6}; Batiment de formation : {7}".format(self.unit_type,self.price, self.life, self.attack, self.movement, self.score_killed, self.capability, self.spawn_building)

    def get_letter(self):
        return self.unit_type

    def move(self, grid):
        i = self.movement
        possible_move = [[1,0,0], [0,-1,0], [0,0,0]] if self.pos[2] else [[-1,0,1],[0,1,1],[0,0,1]]
        moves = []
        last_pos = self.pos
        while i != 0:
            choice = random.choice(possible_move)
            pos = [last_pos[0] + choice[0], last_pos[1] + choice[1], choice[2]]
            cost = grid[pos[1]][pos[0]][pos[2]].cost
            if i >= cost:
                moves.append(pos)
                last_pos = pos
                i -= cost
        return moves

    def action_attack(self, grid):
        possible_attack = [[1,0,0], [0,-1,0], [0,0,0]] if self.pos[2] else [[-1,0,1],[0,1,1],[0,0,1]]
        attacks = []
        for (x,y,bool) in possible_attack:
            pos = [y + self.pos[1], x + self.pos[0], bool]
            if grid[pos[0]][pos[1]][pos[2]].unit is not None and not grid[pos[0]][pos[1]][pos[2]].unit.isOur or grid[pos[0]][pos[1]][pos[2]].building is not None and not grid[pos[0]][pos[1]][pos[2]].building.isOur:
                attacks.append(pos)
        return attacks

    def build(self):
        pass

    def dig(self):
        pass
