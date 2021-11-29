import pygame

from .view import View
from helper.constants import BLACK, HEIGHT


class DefaultWeaponView(View):

    def __init__(self, screen=None, default_weapon_model=None):
        self.screen = screen
        self.default_weapon_model = default_weapon_model

    def register_model(self, default_weapon_model):
        self.default_weapon_model = default_weapon_model

    def update_view(self):
        self.draw()

    def draw(self):
        weapon_position, weapon_radius = self.default_weapon_model.get_state()
        weapon_position[1] = (-1 * weapon_position[1]) + HEIGHT
        pygame.draw.circle(surface=self.screen,
                           color=BLACK,
                           center=weapon_position,
                           radius=weapon_radius,
                           width=0)
