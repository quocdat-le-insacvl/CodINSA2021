import requests

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

    def create_AIgame(self, AItype):
        data = {
            "ai": AItype,
        }
        r = requests.get(self.url + "game/new", data, cookies=self.cookie)
        return r.json()

    def init_map(self, json_map):
        self.map = Map(json_map)

    def list_game(self):
        r = requests.get(self.url + "current", cookies=self.cookie)
        return r.json()["games"]

    def leave_game(self, game=None):
        if game is None:
            game = self.game_id
        requests.delete(self.url + "game/" + game, cookies=self.cookie)
