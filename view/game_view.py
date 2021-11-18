import pygame

from .view import View
from constants import WHITE, FPS


class GameView(View):

    def __init__(self, DISPLAYSURF, game_model=None):
        self.DISPLAYSURF = DISPLAYSURF
        self.FramePerSec = pygame.time.Clock()
        self.game_model = game_model


    def register_model(self, game_model):
        self.game_model = game_model


    def tick(self):
        self.FramePerSec.tick(FPS)


    def draw(self):
        self.DISPLAYSURF.fill(WHITE)
        pygame.display.update()

