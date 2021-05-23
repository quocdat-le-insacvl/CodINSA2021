import requests

from Controller.Turn import Turn
from Model.Map import Map
from Model.Unit import Unit


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
        self.map = Map(json["map"], self.spawn, self)

    def update_list_unit(self):
        for key in self.map.list_unit :
            self.map.list_unit[key] = key.pos

    def analyse_visible(self, data):
        print("TESTING")
        visible_data = data["visible"]
        print(self.map.list_building)

        self.update_list_unit()

        for key in visible_data:
            # iterate every signle case visible 
            # check if it's a enemy | a building of enemy
            value = visible_data[key]
            print(key, value)
            
            if len(value) > 1:
                value = value.split(";")
                print("this", value[1])
                _type = value[1]
                if _type in ["C", "S", "T", "W"]:
                    # this is a building!
                    
                    key = tuple(key[1:len(key)-1].split(", "))
                    key = (int(key[0]), int(key[1]), int(bool(key[2])))
                    print(key, self.map.list_building.values())
                    if key not in self.map.list_building.values():
                        print("Dectected enemy's building!")
                else:
                    key = tuple(key[1:len(key)-1].split(", "))
                    key = (int(key[0]), int(key[1]), int(bool(key[2])))
                    print(key, self.map.list_unit.values())
                    if key not in self.map.list_unit.values():
                        print("Dectected enemy's unit!")


    def analyse(self, data):
        self.analyse_visible(data)
        for moved in data["moved"]:
            if moved[2]:
                dep = moved[0]
                arr = moved[1][-1]
                self.map.grid[arr[1]][arr[0]][arr[2]].unit = self.map.grid[dep[1]][dep[0]][dep[2]].unit
                self.map.grid[dep[1]][dep[0]][dep[2]].unit = None

        for attacked in data["attacked"]:
            pass
        for mined in data["mined"]:
            pass
        for summoned in data["summoned"]:
            if summoned[2]:
                unit = Unit(summoned[0], summoned[1], self)
                self.map.list_unit[unit] = summoned[0]
                self.map.grid[summoned[0][1]][summoned[0][0]][int(summoned[0][2])].unit = unit
        for killed in data["killed"]:
            pass
        


                
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
        for unit in self.map.list_unit:
            turn.move(unit.pos, unit.move(self.map.grid))
            unit.action_attack()
            unit.build()
            unit.dig()

        for building in self.map.list_building:
            new_unit = building.create_unit()
            for i in new_unit:
                for pos in new_unit[i]:
                    turn.summon(pos, i)
        return turn
