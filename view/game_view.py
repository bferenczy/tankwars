import pygame

from terrain import Terrain
from constants import WHITE, FPS

class GameView:

    def __init__(self, DISPLAYSURF, terrain):
        self.DISPLAYSURF = DISPLAYSURF
        self.terrain = terrain
        self.FramePerSec = pygame.time.Clock()


    def refresh_screen(self):
        self.DISPLAYSURF.fill(WHITE)
        self.terrain.draw(self.DISPLAYSURF)
        pygame.display.update()


    def tick(self):
        self.FramePerSec.tick(FPS)


    def draw(self):
        pass

