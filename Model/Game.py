import json

import requests
import random

from Controller.Turn import Turn
from Model.Map import Map
from Model.Unit import Unit
from Controller.Util import find_enemy_spawn
from Controller.Util import adjPos


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
        self.balance = 300
        self.turn = 0

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
        for moved in data["moved"]:
            if moved[2]:
                dep = moved[0]
                arr = moved[1][-1]
                self.map.grid[arr[1]][arr[0]][arr[2]].unit = self.map.grid[dep[1]][dep[0]][dep[2]].unit
                self.map.grid[arr[1]][arr[0]][arr[2]].unit.pos = [arr[0], arr[1], arr[2]]
                self.map.grid[dep[1]][dep[0]][dep[2]].unit = None

        for attacked in data["attacked"]:
            pass
        for mined in data["mined"]:
            pass
        for summoned in data["summoned"]:
            if summoned[2]:
                unit = Unit(summoned[0], summoned[1])
                self.map.list_unit.append(unit)
                self.map.grid[summoned[0][1]][summoned[0][0]][int(summoned[0][2])].unit = unit
        for killed in data["killed"]:
            pass

        for line in self.map.grid:
            for row in line:
                for case in row:
                    case.visible = False
        for visible in data["visible"]:
            pos = json.loads(visible)
            self.map.grid[pos[1]][pos[0]][int(pos[2])].visible = True

        self.balance = data["balance"]
        self.turn = data["turn"]
        # Check in case of error
        for val in data["errors"].values():
            assert(val == []) , data["errors"]
        self.show_analyse(data)


    def show_analyse(self, data):
        print()
        print()
        print("-----------------------------------")
        for key in data:
            print(key, data[key])
        print("-----------------------------------")
        print(self.map.list_unit)
        print()
        print()

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
        posSpawnEnemie = find_enemy_spawn(self.map)
        for unit in self.map.list_unit:
            list_Path = self.map.pathFinder(tuple(unit.pos), adjPos(posSpawnEnemie)[random.randint(0,2)])
            print("deplacement", unit.pos, list_Path)
            if list_Path is not None:
                print("deplacement", unit.pos, list_Path)
                turn.move(unit.pos, list_Path[0:1])
                unit.action_attack()
                unit.build()
                unit.dig()

        for building in self.map.list_building:
            new_unit = building.create_unit()
            for i in new_unit:
                for pos in new_unit[i]:
                    turn.summon(pos, i)
        return turn
