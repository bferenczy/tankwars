import pygame

from .view import View
from constants import HEIGHT, BLACK


class TerrainView(View):


    def __init__(self, DISPLAYSURF, terrain_model=None):
        self.DISPLAYSURF = DISPLAYSURF
        self.terrain_model = terrain_model


    def register_model(self, terrain_model):
        self.terrain_model = terrain_model


    def draw(self):
        # surface: list of [x,y] pairs, ex.: [[0, 0], [1, 2]]
        # where x and y are integers
        terrain = self._terrain_state()
        for x, y in enumerate(terrain):
            pygame.draw.rect(self.DISPLAYSURF, BLACK, [x, HEIGHT - y, 1, y])

        pygame.display.update()


    def _terrain_state(self):
        return self.terrain_model.get_terrain_state()

