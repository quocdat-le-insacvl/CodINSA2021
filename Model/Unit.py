import random


class Unit:

    def __init__(self, pos, unit_type):
        self.pos = pos
        self.unit_type = unit_type
        if unit_type == "V":
            self.price = 20
            self.life = 20
            self.max_life = 20
            self.attack = 10
            self.movement = 2
            self.score_killed = 10
            self.capability = "Construction de batiment, recolte de ressources"
            self.spawn_building = "S"
        elif unit_type == "L":
            self.price = 30
            self.life = 60
            self.max_life = 60
            self.attack = 20
            self.movement = 4
            self.score_killed = 15
            self.capability = None
            self.spawn_building = "Amphitheatre"
        else:
            self.price = 100
            self.life = 100
            self.max_life = 100
            self.attack = 40
            self.movement = 2
            self.score_killed = 35
            self.capability = None
            self.spawn_building = "Amphitheatre"

    def __str__(self):
        return "Type:{0}-Pos{1}-Life{2}\n".format (self.unit_type, self.pos, self.life)

    def __repr__(self):
        return "Type:{0}-Pos{1}-Life{2}\n".format (self.unit_type, self.pos, self.life)

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

    def move_complex(self, grid):
        pass

    def action_attack(self):
        pass

    def build(self):
        pass

    def dig(self):
        pass
