import json
import socket

import requests

from Controller.Turn import Turn
from Model.Game import Game
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
            try:
                while flag:
                    data = sock.recv(1024)
                    if data is not None:
                        data = json.loads(data.decode("UTF-8"))

                        """ Début du jeu """
                        if "game" in data and data["game"] == "begin":
                            self.game.init(data)

                        if data["your_turn"]:
                            turn = Turn()

                            turn.send(socket, self.game.password)
            except Exception as e:
                print(str(e))
                pass
        self.game.leave_game()