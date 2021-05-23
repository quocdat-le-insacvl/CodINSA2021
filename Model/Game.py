import requests

from Controller.Turn import Turn
from Model.Map import Map


class Game:

    def __init__(self, url, cookie, ai_mode):
        self.url = url
        self.cookie = cookie
        for game in self.list_game():
            self.leave_game(game)
        game_info = self.create_AIgame(ai_mode)
        self.port = game_info["port"]
        self.game_id = game_info["game_id"]
        self.password = game_info["password"]
        self.map = None
        self.spawn = None
        self.list_unit = []

    def create_AIgame(self, AItype):
        data = {
            "ai": AItype,
        }
        r = requests.get(self.url + "game/new", data, cookies=self.cookie)
        return r.json()

    def init(self, json):
        self.spawn = (json["spawn"][0], json["spawn"][1], int(json["spawn"][2]))
        self.map = Map(json["map"], self.spawn)

    def analyse(self, data):
        print()
        print()
        print("-----------------------------------")
        for key in data:
            print(key , data[key])
        print("-----------------------------------")
        print()
        print()
        pass

    def list_game(self):
        r = requests.get(self.url + "current", cookies=self.cookie)
        return r.json()["games"]

    def leave_game(self, game=None):
        if game is None:
            game = self.game_id
        requests.delete(self.url + "game/" + game, cookies=self.cookie)

    def new_turn(self):
        turn = Turn()

        """ Unit movement, attack, build and dig"""
        for unit in self.list_unit:
            unit.move()
            unit.attack()
            unit.build()
            unit.dig()

        for building in self.list_building:
            building.create_unit()

