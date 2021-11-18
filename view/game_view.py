import pygame

from .view import View
from constants import WHITE, FPS


class GameView(View):

    def __init__(self, DISPLAYSURF, game_model=None):
        self.DISPLAYSURF = DISPLAYSURF
        self.FramePerSec = pygame.time.Clock()
        self.game_model = game_model
        self.terrain_view = None


    def register_terrain_view(self, terrain_view):
        self.terrain_view = terrain_view


    def register_model(self, game_model):
        self.game_model = game_model


    def tick(self):
        self.FramePerSec.tick(FPS)


    def update_view(self):
        self.draw()


    def draw(self):
        self.DISPLAYSURF.fill(WHITE)
        pygame.display.update()
        self.terrain_view.update_view()

