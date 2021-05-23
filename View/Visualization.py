import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
BROWN = (135,62,35)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
VISIBLE_COLOR = (169,169,169)
PROGRESS = (46, 117, 49)

# game settings
WIDTH = 1024 + 900   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768 + 300  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 30
TITLE = "Visualization"
BGCOLOR = DARKGREY

class Visualization:

    def __init__(self, game):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.game = game
        self.dict_color =  {'F':  GREEN, 'A' : BROWN, 'R': YELLOW, 'M': DARKGREY}
        self.font = pg.font.SysFont(None, 35)
        self.big_font = pg.font.SysFont(None, 50)
        # img = font.render(text, True, RED)

    def DrawBar(self, pos, size, barC, progress):
        innerPos = (pos[0] + 3, pos[1] + 3)
        innerSize = ((size[0] - 6) * progress, size[1] - 6)
        pg.draw.rect(self.screen, barC, (*innerPos, *innerSize))

    def draw(self):
        pg.key.get_pressed()
        self.dt = self.clock.tick(FPS) / 1000
        self.screen.fill(WHITE)
        self.map = self.game.map
        width = self.map.width
        height = self.map.height
        R = 60
        R2 = R/2
        offset = 800
        circle_rate = 12
        offset_char = 10
        print(self.game.list_enemy_unit)
        for j in range(height):
            for i in range(width):
                building1 = self.map.grid[j][i][0].building
                building2 = self.map.grid[j][i][1].building
                unit1 = self.map.grid[j][i][0].unit
                unit2 = self.map.grid[j][i][1].unit
                case0 = self.map.grid[j][i][0].tiles_type
                case1 = self.map.grid[j][i][1].tiles_type
                color0 = self.dict_color[case0]
                color1 = self.dict_color[case1]
                x1, y1 = [offset + R/2 + i*R - R2*j, R/2 + j*R2]
                x1 += offset +i*R - R2*j
                y1 += R + j*R2
                x1 += offset +R + i*R - R2*j
                y1 += R+ j*R2
                x1 /= 3
                y1 /= 3

                if self.map.grid[j][i][0].visible:
                    pg.draw.polygon(self.screen, VISIBLE_COLOR, [[x1 + 30, y1 + 10], [x1 - 30, y1 + 10], [x1, y1 - 20]])

                pg.draw.circle(self.screen, color0, (x1,y1), circle_rate)
                pg.draw.polygon(self.screen, BLACK, [[offset + R/2 + i*R - R2*j, R/2 + j*R2], [offset +i*R - R2*j , R + j*R2], [offset +R + i*R - R2*j, R+ j*R2]], 5)
                if building1 is not None:
                    building1 = building1.building_type
                    img = self.font.render(building1, True, RED if self.map.grid[j][i][0].building.isOwned else BLUE)
                    self.screen.blit(img, (x1-offset_char + 1,y1-offset_char - 5))
                    self.DrawBar((x1 - 20, y1), (40, 10), PROGRESS, self.map.grid[j][i][0].building.life / self.map.grid[j][i][0].building.max_life)
                if unit1 is not None:
                    unit1 = unit1.unit_type
                    # img = self.font.render(unit1, True, RED if self.map.grid[j][i][0].unit.isOwned else BLUE)
                    img = self.font.render(unit1, True, BROWN if self.map.grid[j][i][0].unit.focus == "Mined" else BLUE)
                    self.screen.blit(img, (x1-offset_char + 1, y1-offset_char - 5))
                    self.DrawBar((x1 - 20, y1), (40, 10), PROGRESS,
                                 self.map.grid[j][i][0].unit.life / self.map.grid[j][i][0].unit.max_life)


                x2, y2 = [offset +R/2 + i*R - j*R2, R/2+ j*R2]
                x2 += offset +R*3/2 + i*R -j*R2
                y2 += R/2+ j*R2
                x2 += offset +R + i*R - j*R2
                y2 += R+ j*R2
                x2 /= 3
                y2 /= 3

                if self.map.grid[j][i][1].visible:
                    pg.draw.polygon(self.screen, VISIBLE_COLOR, [[x2 + 30, y2 - 10], [x2 - 30, y2 - 10], [x2, y2 + 20]])

                pg.draw.circle(self.screen, color1, (x2,y2), circle_rate)
                pg.draw.polygon(self.screen, BLACK, [[offset +R/2 + i*R - j*R2, R/2+ j*R2], [offset +R*3/2 + i*R -j*R2, R/2+ j*R2], [offset +R + i*R - j*R2, R+ j*R2]], 5)
                if building2 is not None:
                    building2 = building2.building_type
                    img = self.font.render(building2, True, RED if self.map.grid[j][i][1].building.isOwned else BLUE)
                    self.screen.blit(img, (x2-offset_char + 1, y2-offset_char + 5))
                    self.DrawBar((x2 - 20, y2 - 9), (40, 10), PROGRESS,
                                 self.map.grid[j][i][1].building.life / self.map.grid[j][i][1].building.max_life)
                if unit2 is not None:
                    unit2 = unit2.unit_type
                    img = self.font.render(unit2, True, BROWN if self.map.grid[j][i][1].unit.focus == "Mined" else BLUE)
                    self.screen.blit(img, (x2-offset_char + 1,y2 - offset_char + 5))
                    self.DrawBar((x2 - 20, y2 - 9), (40, 10), PROGRESS,
                                 self.map.grid[j][i][1].unit.life / self.map.grid[j][i][1].unit.max_life)

                # show enemy
                # for enemy_unit in self.game.list_unit:
                    # print("enemy here!", enemy_unit.pos)
                    # if enemy_unit.pos == [i, j, 0]:
                        # img = self.font.render('e' + enemy_unit.unit_type, True, RED)
                        # self.screen.blit(img, (x1-offset_char + 1, y1 - offset_char + 5))
                        


                # print balance
                img = self.big_font.render("balance : " + str(self.game.balance), True, BLACK)
                self.screen.blit(img, (0,0))
                # print turn
                img = self.big_font.render("turn : " + str(self.game.turn), True, BLACK)
                self.screen.blit(img, (0,60))


        # pg.draw.polygon(self.screen, RED, [[100, 100], [200, 200]], 5)
        pg.display.flip()



