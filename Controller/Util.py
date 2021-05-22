def find_resources(game_map):
    resources = []
    x = 0
    y = 0
    down = 0
    for c in game_map:
        if c == " ":
            continue
        if c == "\n":
            y = y + 1
            x = 0
            down = 0
            continue
        if c == "R":
            resources.append((x, y, down, "R"))
        if down == 0:
            down = 1
        else:
            down = 0
            x = x + 1
    return resources


def find_enemy_spawn(game_map, spawn):
    x = 0
    y = 0
    down = 0
    for c in game_map:
        if c == " ":
            continue
        if c == "\n":
            y = y + 1
            x = 0
            down = 0
            continue
        if c == "S":
            if x == spawn[0] and y == spawn[1] and down == spawn[2]:
                continue
            return x, y, down, "S"
        if down == 0:
            down = 1
        else:
            down = 0
            x = x + 1
