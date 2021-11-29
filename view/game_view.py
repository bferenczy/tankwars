import pygame
from helper.ui_elements import Background, Smoke
from .view import View
from helper.constants import WHITE, FPS
from .gui import GUI


class GameView(View):

    def __init__(self, screen, game_model=None):
        self.screen = screen
        self.FramePerSec = pygame.time.Clock()
        self.game_model = game_model
        self.terrain_view = None
        self.tank_views = list()
        self.weapon_view = None
        self.gui = None
        self.bg = Background(self.screen, "img/game_bg.jpg")
        self.smoke = Smoke(self.screen)

    def register_terrain_view(self, terrain_view):
        self.terrain_view = terrain_view

    def register_tank_view(self, tank_view):
        self.tank_views.append(tank_view)

    def register_model(self, game_model):
        self.game_model = game_model
        self.gui = GUI(self.screen, self.game_model.players)

    def register_weapon_view(self, weapon_view):
        self.weapon_view = weapon_view

    def deregister_weapon_view(self):
        self.weapon_view = None

    def tick(self):
        self.FramePerSec.tick(FPS)

    def update_view(self):
        self.draw()

    def draw(self):
        self.screen.fill(WHITE)
        self.bg.draw()
        if self.terrain_view:
            self.terrain_view.update_view()
        if self.tank_views:
            for tank_view in self.tank_views:
                tank_view.update_view()
        if self.weapon_view:
            self.weapon_view.update_view()
        if self.gui:
            self.gui.draw()
        self.smoke.draw()
        pygame.display.update()
