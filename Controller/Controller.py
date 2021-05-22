import json
import socket

import requests

from Model.Game import Game
from View.View import View


class Controller:

    def __init__(self):
        self.url = "http://codinsa.insa-rennes.fr/"
        self.host = "codinsa.insa-rennes.fr"
        self.cookie = self.login()
        self.game = Game(self.url, self.cookie)
        self.view = View()
        self.run()

    def login(self):
        data = {
            "username": "CVL1",
            "password": "+GC;GY8]dK1EYbS=ja*;U"
        }
        r = requests.post(self.url + "init", json=data)
        return r.cookies

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.game.port))
            try:
                while True:
                    data = s.recv(1024)
                    if data is not None:
                        data = json.loads(data.decode("UTF-8"))
                        print(data)
                        if "game" in data and data["game"] == "begin":
                            print(data["map"])
                            self.view.convert_map(data)
                            game_spawn = data["spawn"]

                        if "moved" in data:
                            pass

                        if data["your_turn"]:
                            toSend = {
                                'summon': {
                                    '[9,1,false]': 'V'
                                },
                                'token': self.game.password
                            }
                            s.send((json.dumps(toSend) + "\n").encode())

                    print("\n")
            except Exception as e:
                print(str(e))
                pass
        self.game.leave_game()