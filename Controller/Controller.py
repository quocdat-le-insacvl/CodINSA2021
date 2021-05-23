import json
import socket
import time

import requests

from Controller.Turn import Turn
from Model.Game import Game
from Model.Unit import Unit
from View.View import View
from View.Visualization import Visualization


class Controller:

    def __init__(self):
        self.ai_mode = "InactiveAI"
        self.url = "http://codinsa.insa-rennes.fr/"
        self.host = "codinsa.insa-rennes.fr"
        self.cookie = self.login()
        self.game = Game(self.url, self.cookie, self.ai_mode)
        self.view = View()
        self.visualization = Visualization(self.game)
        self.run()

    def login(self):
        data = {
            "username": "CVL1",
            "password": "+GC;GY8]dK1EYbS=ja*;U"
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
                data = sock.recv(1024)
                while len(data) > 0 and data[-1] != 10:
                    data += sock.recv(1024)

                if data is not None or data != b'':
                    try:
                        data = json.loads(data.decode("UTF-8"))
                    except Exception as E:
                        print(data)
                        print(str(E))
                        print("Une erreur est survenue!")
                        break 


                    """ Début du jeu """
                    if "game" in data and data["game"] == "begin":
                        self.game.init(data)
                        turn = self.game.new_turn()
                        turn.send(sock, self.game.password)
                        # print(self.game.map.grid[1][8][1].pos)
                        # print(self.game.map.pathFinder(self.game.map.grid[1][8][1].pos, self.game.map.grid[10][8][1].pos))
                    else:
                        print(data)
                        if "your_turn" in data :
                            if data["your_turn"]:
                                """ On récupère le jeu de l'ia puis on joue notre tour"""
                                turn = self.game.new_turn()
                                turn.send(sock, self.game.password)
                               
                                # turn = Turn()
                                # turn.summon((self.game.spawn[0], self.game.spawn[1], 1), "V")
                                # turn.send(sock, self.game.password)
                            else:
                                """ On récupère les infos de notre tour """
                                self.game.analyse(data)
                        else:
                            print(data)
                            flag = False

                    self.visualization.draw()
        self.game.leave_game()
