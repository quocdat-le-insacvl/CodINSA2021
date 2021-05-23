import heapq


class PriorityQueue:

    def __init__(self):
        self.elements = []

    def empty(self):
        return not self.elements

    def push(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def pop(self):
        return heapq.heappop(self.elements)[1]


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


def find_enemy_spawn(gameMap):
    for x in range(len(gameMap.grid)):
        for y in range(len(gameMap.grid[x])):
            for z in range(len(gameMap.grid[x][y])):
                if gameMap.grid[x][y][z].building is not None:
                    if gameMap.grid[x][y][z].building.building_type == "S":
                        if gameMap.grid[x][y][z].building.pos is not gameMap.spawn.pos:
                            return gameMap.grid[x][y][z].building.pos


def pos_to_str(pos: tuple):
    return "[{0},{1},{2}]".format(pos[0], pos[1], "true" if pos[2] else "false")


def distance(pos1, pos2):
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1]) + abs(
        pos2[1] - pos1[1] + pos1[0] - pos2[0] + pos2[2] - pos1[2])


def adjPos(pos):
    list = []
    if pos[2]:
        list.append((pos[0] + 1, pos[1], 0))
        list.append((pos[0], pos[1] - 1, 0))
        list.append((pos[0], pos[1], 0))
    else:
        list.append((pos[0] - 1, pos[1], 1))
        list.append((pos[0], pos[1] + 1, 1))
        list.append((pos[0], pos[1], 1))
    return list
