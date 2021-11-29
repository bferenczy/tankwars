import pygame

from .view import View
from helper.constants import HEIGHT, BLACK


class TerrainView(View):

    def __init__(self, screen, terrain_model=None):
        self.screen = screen
        self.terrain_model = terrain_model

    def register_model(self, terrain_model):
        self.terrain_model = terrain_model

    def update_view(self):
        self.draw()

    def draw(self):
        terrain = self._terrain_state()
        for x, y in enumerate(terrain):
            pygame.draw.rect(self.screen, BLACK, [x, HEIGHT - y, 1, y])

    def _terrain_state(self):
        return self.terrain_model.get_terrain_state()
