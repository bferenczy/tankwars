from .controller import Controller
from model.game_model import GameModel
from view.default_weapon_view import DefaultWeaponView
from model.default_weapon_model import DefaultWeaponModel
from view.game_view import GameView
import pygame


from time import sleep


class GameController(Controller):


    def __init__(self, game_model=None, game_view=None):
        self.game_model = game_model
        self.game_view = game_view


    def register_model(self, game_model):
        self.game_model = game_model


    def register_view(self, game_view):
        self.game_view = game_view


    def run(self):
        while not self._is_game_over():
            self.game_model.select_active_player()
            self._get_events()
            self._step()


    def _get_events(self):
        submitted = False
        while not submitted:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.game_model.modify_angle(0.1)
            if keys[pygame.K_DOWN]:
                self.game_model.modify_angle(-0.1)
            if keys[pygame.K_LEFT]:
                self.game_model.modify_strength(-0.1)
            if keys[pygame.K_RIGHT]:
                self.game_model.modify_strength(0.1)

            self.update_view()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        submitted = True
                    if event.key == pygame.QUIT:
                        exit(1)


    def _step(self):
        model = self.game_model.execute()
        if model and isinstance(model, DefaultWeaponModel):
             default_weapon_view = self._create_default_weapon_view(model)

        while model.is_moving() is True:
            self.game_view.tick()
            model.move()
            self.update_view()

        self._deregister_model(model)
        del default_weapon_view
        self.update_view()


    def _deregister_model(self, model):
        self.game_view.deregister_weapon_view()
        del model


    def _create_default_weapon_view(self, model):
        default_weapon_view = DefaultWeaponView()
        default_weapon_view.register_model(model)
        self.game_view.register_weapon_view(default_weapon_view)

        return default_weapon_view


    def update_view(self):
        self.game_view.draw()


    def _is_game_over(self):
        return False;

