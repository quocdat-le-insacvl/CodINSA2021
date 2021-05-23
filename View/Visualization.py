import pygame as pg
import sys

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
BROWN = (135,62,35)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1024+ 800   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768   # 16 * 48 or 32 * 24 or 64 * 12
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
        # img = font.render(text, True, RED)

    def draw(self):
        pg.key.get_pressed()
        self.dt = self.clock.tick(FPS) / 1000
        self.screen.fill(WHITE)
        self.map = self.game.map
        width = self.map.width
        height = self.map.height
        R = 60
        R2 = R/2
        offset = 600
        circle_rate = 12
        offset_char = 10
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
                
                pg.draw.circle(self.screen, color0, (x1,y1), circle_rate)
                pg.draw.polygon(self.screen, BLACK, [[offset + R/2 + i*R - R2*j, R/2 + j*R2], [offset +i*R - R2*j , R + j*R2], [offset +R + i*R - R2*j, R+ j*R2]], 5)
                if building1 is not None:
                    building1 = building1.building_type
                    img = self.font.render(building1, True, RED)
                    self.screen.blit(img, (x1-offset_char,y1-offset_char))
                if unit1 is not None:
                    unit1 = unit1.unit_type
                    img = self.font.render(unit1, True, RED)
                    self.screen.blit(img, (x1-offset_char,y1-offset_char))

                
                x2, y2 = [offset +R/2 + i*R - j*R2, R/2+ j*R2]
                x2 += offset +R*3/2 + i*R -j*R2
                y2 += R/2+ j*R2
                x2 += offset +R + i*R - j*R2
                y2 += R+ j*R2
                x2 /= 3
                y2 /= 3
                pg.draw.circle(self.screen, color1, (x2,y2), circle_rate)
                pg.draw.polygon(self.screen, BLACK, [[offset +R/2 + i*R - j*R2, R/2+ j*R2], [offset +R*3/2 + i*R -j*R2, R/2+ j*R2], [offset +R + i*R - j*R2, R+ j*R2]], 5)
                if building2 is not None:
                    building2 = building2.building_type
                    img = self.font.render(building2, True, RED)
                    self.screen.blit(img, (x2-offset_char,y2-offset_char))
                if unit2 is not None:
                    unit2 = unit2.unit_type
                    img = self.font.render(unit1, True, RED)
                    self.screen.blit(img, (x1-offset_char,y1-offset_char))

        # pg.draw.polygon(self.screen, RED, [[100, 100], [200, 200]], 5)

        pg.display.flip()



