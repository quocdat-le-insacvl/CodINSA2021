import requests
import json
import socket
import math

url = "http://codinsa.insa-rennes.fr/"
host = "codinsa.insa-rennes.fr"

# Tuiles
Abyss = 'A'
Field = 'F'
Mountain = 'M'
Ressource = 'R'

# Bâtiments :
Camp = 'C'
Spawn = 'S'
Turret = 'T'
Wall = 'W'

# Unités :
Scout = 'L'  # L for Light
Villager = 'V'
Tank = 'H'  # H for Heavy

game_map = []
game_spawn = []


def login():
    data = {
        "username": "CVL1",
        "password": "+GC;GY8]dK1EYbS=ja*;U"
    }
    r = requests.post(url + "init", json=data)
    return r.cookies


def create_game(cookies, AItype):
    data = {
        "ai": AItype,
    }
    r = requests.get(url + "game/new", data, cookies=cookies)
    print(r.json())
    return r.json()


def list_game(cookies):
    r = requests.get(url + "current", cookies=cookies)
    return r.json()["games"]


def leave_game(cookies, code):
    requests.delete(url + "game/" + code, cookies=cookies)


def convert_map(data):
    game_map = []
    rows = data["map"].splitlines()
    for i in range(len(rows)):
        mapped_line = []
        split_line = rows[i].split(" ")
        for j in range(len(split_line)):
            mapped_line.append([math.floor(j / 2), i, bool(j % 2)])
        game_map.append(mapped_line)


if __name__ == "__main__":
    cookies = login()

    for game in list_game(cookies):
        leave_game(cookies, game)

    game_info = create_game(cookies, "InactiveAI")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, game_info["port"]))

        try:
            while True:
                data = s.recv(1024)
                if data is not None:
                    data = json.loads(data.decode("UTF-8"))
                    print(data)
                    if "game" in data and data["game"] == "begin":
                        print(data["map"])
                        convert_map(data)
                        game_spawn = data["spawn"]

                    if "moved" in data:
                        pass

                    if data["your_turn"]:
                        toSend = {
                            'summon': {
                                '[9,1,false]': 'V'
                            },
                            'token': game_info["password"]
                        }
                        s.send((json.dumps(toSend) + "\n").encode())

                print("\n")
        except Exception as e:
            print(str(e))
            pass

    leave_game(cookies, game_info["game_id"])
