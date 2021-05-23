import json

import requests
from Controller.Danger import Danger
import random

from Controller.Turn import Turn
from Model.Map import Map
from Model.Unit import Unit
from Model.Building import Building
from Controller.Util import find_enemy_spawn, find_nearby_enemy, pos_to_str
from Controller.Util import adjPos


class Game:

    def __init__(self, url, cookie, ai_mode, multiplayer, code, game_id):
        self.url = url
        self.cookie = cookie
        for game in self.list_game():
            self.leave_game(game)
        game_info = self.create_multiplayer_game(code, game_id) if multiplayer else self.create_AIgame(ai_mode)
        self.port = game_info["port"]
        self.game_id = game_info["game_id"]
        self.password = game_info["password"]
        self.map = None
        self.spawn = None
        self.danger = None
        self.balance = 300
        self.turn = 0
        self.list_enemy_unit = []
        self.list_enemy_building = []
        print(self.game_id)

    def create_AIgame(self, AItype):
        data = {
            "ai": AItype,
        }
        r = requests.get(self.url + "game/new", data, cookies=self.cookie)
        return r.json()

    def create_multiplayer_game(self, code, game_id):
        r = None

        if game_id is not None:
            r = requests.get(self.url + "game/" + game_id + "?privkey=" + code, cookies=self.cookie)
        elif code is not None:
            r = requests.get(self.url + "game/new?privkey=" + code, cookies=self.cookie)
        else:
            r = requests.get(self.url + "game/new?multiplayer=1", cookies=self.cookie)

        return r.json()

    def init(self, json):
        self.danger = Danger()
        self.spawn = (json["spawn"][0], json["spawn"][1], int(json["spawn"][2]))
        self.map = Map(json["map"], self.spawn, self)

    def analyse_visible(self, data):
        list_pos_unit = [unit.pos for unit in self.map.list_unit]
        list_pos_building = [building.pos for building in self.map.list_building]
        visible_data = data["visible"]
        self.list_enemy_unit = []
        self.list_enemy_building = []
        for key in visible_data:
            # iterate every signle case visible
            # check if it's a enemy | a building of enemy
            value = visible_data[key]
            if len(value) > 1:
                value = value.split(";")
                _type = value[1]
                if _type in ["C", "S", "T", "W"]:
                    # this is a building!
                    key = tuple(json.loads(key))
                    if key not in list_pos_building:
                        self.list_enemy_building.append(Building(key, _type, False))
                else:
                    key = json.loads(key)
                    if key not in list_pos_unit:
                        self.list_enemy_unit.append(Unit(key, _type, False))

                        # print(key)
                        # print("enemy unit")
                        # print(list_pos_unit)

        # print("LIST our units :", self.map.list_unit)
        print("Enemy unit: ")
        print(self.list_enemy_unit)
        print("Enemy building: ")
        print(self.list_enemy_building)

    def analyse(self, data):
        try:
            for killed in data["killed"]:
                pos = json.loads(killed)
                for unit in self.map.list_unit:
                    if pos == unit.pos:
                        self.map.list_unit.remove(unit)
                        break
        except Exception as E:
            print(str(E))
            print("Error killed/function ")

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
                unit = Unit(summoned[0], summoned[1], True)
                self.map.list_unit.append(unit)
                # self.map.list_unit[unit] = summoned[0]
                self.map.grid[summoned[0][1]][summoned[0][0]][int(summoned[0][2])].unit = unit

        for line in self.map.grid:
            for row in line:
                for case in row:
                    case.visible = False
                    if not pos_to_str(case.pos) in data["visible"]:
                        if case.unit is not None and not case.unit.isOwned:
                            case.unit = None
        for visible in data["visible"]:
            pos = json.loads(visible)
            content = data["visible"][visible].split(";")
            self.map.grid[pos[1]][pos[0]][int(pos[2])].visible = True
            if len(content) > 2:
                if content[1] in ["S", "C", "T", "W"]:
                    if self.map.grid[pos[1]][pos[0]][int(pos[2])].building is None:
                        self.map.grid[pos[1]][pos[0]][int(pos[2])].building = Building((pos[0], pos[1], bool(pos[2])),
                                                                                       content[1])
                    self.map.grid[pos[1]][pos[0]][int(pos[2])].building.life = int(content[2])
                else:
                    if content[1] in ["V", "L", "H"]:
                        if self.map.grid[pos[1]][pos[0]][int(pos[2])].unit is None:
                            self.map.grid[pos[1]][pos[0]][int(pos[2])].unit = Unit(
                                (pos[0], pos[1], bool(pos[2])), content[1])
                        self.map.grid[pos[1]][pos[0]][int(pos[2])].unit.life = int(content[2])

        self.balance = data["balance"]
        self.turn = data["turn"]
        # Check in case of error
        for val in data["errors"].values():
            assert (val == []), data["errors"]

        if "visible" in data:
            self.danger.check(self.map, data["visible"], self.map.list_unit, self.map.list_building, self.spawn)

        self.show_analyse(data)
        self.analyse_visible(data)

    def show_analyse(self, data):
        print()
        print()
        print("-----------------------------------")
        for key in data:
            print(key, data[key])
        print("-----------------------------------")
        print("\nThreat on units: ")
        for d in self.danger.units:
            print(d)
        print("\nThreat on buildings: ")
        for d in self.danger.buildings:
            print(d)
        print("\nThreat on spawn: ")
        for d in self.danger.spawn:
            print(d)
        print("\nThreat on resources: ")
        for d in self.danger.resources:
            print(d)

        print("\nOur units")
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
        current_moves = []
        for unit in self.map.list_unit:
            posToMove = None
            if unit.focus == "Spawn":
                # Liste des positions autour du spawn enemie
                listPositiontoAttackSpawnEnemie = adjPos(posSpawnEnemie)
                listPositiontoAttackSpawnEnemieExtended = listPositiontoAttackSpawnEnemie.copy()
                for newpos in listPositiontoAttackSpawnEnemie.copy():
                    for newposadd in adjPos(newpos):
                        if self.map.isValid(newposadd):
                            listPositiontoAttackSpawnEnemieExtended.append(newposadd)

                # Récuppère une position d'attaque disponible
                posToAttack = None
                # Récuppère une position d'attaque disponible
                for pos in listPositiontoAttackSpawnEnemieExtended:
                    if tuple(unit.pos) in listPositiontoAttackSpawnEnemie:
                        break
                    if self.map.isValid(pos) and self.map.pathFinder(tuple(unit.pos), pos) is not None:
                        if self.map.grid[pos[1]][pos[0]][pos[2]].unit is None or self.map.grid[pos[1]][pos[0]][pos[2]].unit is not None and not self.map.grid[pos[1]][pos[0]][pos[2]].unit.isOwned:
                            posToAttack = pos
                            break
                posToMove = posToAttack
            elif unit.focus == "Mined":
                voisins = adjPos(unit.pos)
                flag_moove = True
                for pos in voisins:
                    xmax = len(self.map.grid)
                    ymax = len(self.map.grid[0])
                    if 0 <= pos[1] < xmax and 0 <= pos[0] < ymax:
                        if self.map.grid[pos[1]][pos[0]][pos[2]].tiles_type == "R":
                            flag_moove = False
                            break
                posToMined = None
                if flag_moove:
                    posToMined = None
                    for res_pos in self.map.list_ressource:
                        list_pos = adjPos(res_pos)
                        for pos in list_pos:
                            if self.map.isValid(pos) and self.map.pathFinder(tuple(unit.pos), pos) is not None:
                                if self.map.grid[pos[1]][pos[0]][pos[2]].unit is None or self.map.grid[pos[1]][pos[0]][pos[2]].unit is not None and not self.map.grid[pos[1]][pos[0]][pos[2]].unit.isOwned:
                                    posToMined = pos
                        if posToMined is not None:
                            break

                posToMove = posToMined

            # print("pathfinder",unit.pos, listPositiontoAttackSpawnEnemie, listPositiontoAttackSpawnEnemieExtended, posToAttack)
            # Calcule le déplacement pur aller vers cette position
                #Calcule le déplacement pur aller vers cette position
            list_Path = None
            if posToMove is not None:
                list_Path = self.map.pathFinder(tuple(unit.pos), posToMove)

            # Déplace l'unit
            if list_Path is not None:
                if self.map.grid[list_Path[0][1]][list_Path[0][0]][list_Path[0][2]].tiles_type == "M":
                    imax = (unit.movement // 2)
                    while imax != 0:
                        moves = list_Path[0:imax]
                        if moves[-1] not in current_moves and self.map.grid[moves[-1][1]][moves[-1][0]][moves[-1][2]].unit is None :
                            current_moves.append(moves[-1])
                            turn.move(unit.pos, moves)
                            break
                        imax -= 1
                else:
                    if len(list_Path) > 1 and self.map.grid[list_Path[1][1]][list_Path[1][0]][
                        list_Path[1][2]].tiles_type == "M":
                        imax = (unit.movement // 2)
                        while imax != 0:
                            moves = list_Path[0:imax]
                            if moves[-1] not in current_moves  and self.map.grid[moves[-1][1]][moves[-1][0]][moves[-1][2]].unit is None:
                                current_moves.append(moves[-1])
                                turn.move(unit.pos, moves)
                                break
                            imax -= 1
                    else:
                        imax = unit.movement
                        while imax != 0:
                            moves = list_Path[0:imax]
                            if moves[-1] not in current_moves  and self.map.grid[moves[-1][1]][moves[-1][0]][moves[-1][2]].unit is None:
                                current_moves.append(moves[-1])
                                turn.move(unit.pos, moves)
                                break
                            imax -= 1

            possibility = find_nearby_enemy(self.map.grid, unit.pos)
            possibility.append(posSpawnEnemie)

            if len(possibility) > 0:
                turn.attack(unit.pos, possibility[0])

            near_pos = adjPos(unit.pos)
            available = list(set(near_pos).intersection(self.map.list_ressource))
            if len(available) > 0:
                turn.mine(unit.pos, available[0])

        for building in self.map.list_building:
            new_unit = building.create_unit()
            for i in new_unit:
                for pos in new_unit[i]:
                    turn.summon(pos, i)
        return turn
