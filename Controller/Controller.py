import json
import socket

import requests

from Controller.Turn import Turn
from Model.Game import Game
from Model.Unit import Unit
from View.View import View


class Controller:

    def __init__(self):
        self.ai_mode = "InactiveAI"
        self.url = "http://codinsa.insa-rennes.fr/"
        self.host = "codinsa.insa-rennes.fr"
        self.cookie = self.login()
        self.game = Game(self.url, self.cookie, self.ai_mode)
        self.view = View()
        self.run()

    def login(self):
        data = {
            "username": "CVL3",
            "password": ".WCX6_KO9<PVh-F9V@PmNlL?"
        }
        r = requests.post(self.url + "init", json=data)
        return r.cookies

    def send(self, sock, data):
        sock.send((json.dumps(data) + "\n").encode())

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.game.port))
            flag = True
            while flag:
                data = sock.recv(20480)
                if data is not None:
                    data = json.loads(data.decode("UTF-8"))

                    """ Début du jeu """
                    if "game" in data and data["game"] == "begin":
                        self.game.init(data)
                        # print(self.game.map.grid[1][8][1].pos)
                        # print(self.game.map.pathFinder(self.game.map.grid[1][8][1].pos, self.game.map.grid[10][8][1].pos))
                    else:
                        if data["your_turn"]:
                            turn = Turn()
                            turn.summon((self.game.spawn[0], self.game.spawn[1], 1), "V")
                            turn.send(sock, self.game.password)
                        else:
                            self.game.analyse(data)

                    View.convert_map(self.game.map.grid)
        self.game.leave_game()
