import json

from Controller.Util import pos_to_str
from Model.Building import Building
from Model.Unit import Unit


class Turn:

    def __init__(self):
        self.moves = {}
        self.attacks = {}
        self.mines = {}
        self.builds = {}
        self.summons = {}

    def move(self, pos, dests):
        self.moves[pos_to_str(pos)] = [[dest[0], dest[1], bool(dest[2])] for dest in dests]

    def attack(self, pos, dest):
        self.attacks[pos_to_str(pos)] = [dest[0], dest[1], bool(dest[2])]

    def mine(self, pos, dest):
        self.mines[pos_to_str(pos)] = [dest[0], dest[1], bool(dest[2])]

    def build(self, pos, dest, type):
        self.builds[pos_to_str(pos)] = [[dest[0], dest[1], bool(dest[2])], type]

    def summon(self, pos, type):
        self.summons[pos_to_str(pos)] = type

    def send(self, sock, token):
        data = json.dumps({
            "move": self.moves,
            "attack": self.attacks,
            "mine": self.mines,
            "build": self.builds,
            "summon": self.summons,
            "token": token
        })
        print(data)
        sock.send((data + "\n").encode())

# if __name__ == '__main__':
#     turn = Turn()
#     pos1 = (8, 1, 0)
#     pos2 = (8, 1, 1)
#     pos3 = (9, 1, 0)
#     turn.summon(pos1, unit)
#     turn.move(pos1, pos2, pos3, pos1)
#     turn.build(pos1, pos2, building)
#
#     turn.send(None, "")
