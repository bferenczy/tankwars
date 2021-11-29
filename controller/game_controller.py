import pygame, sys
from pygame.locals import *

from model.player_model import HumanPlayerModel, AIPlayerModel
from model.game_model import GameModel
from view.game_view import GameView
from model.terrain_model import TerrainModel
from view.terrain_view import TerrainView
from model.tank_model import TankModel
from view.tank_view import TankView
from model.default_weapon_model import DefaultWeaponModel
from view.default_weapon_view import DefaultWeaponView
from constants import Scenes, WIDTH, HEIGHT, RED, BLUE
from basic_types import Position


class GameController():


    def __init__(self, DISPLAYSURF, init_state):
        self.DISPLAYSURF = DISPLAYSURF
        self.game_model = None
        self.game_view = None
        self._create_scene(init_state)


    def new_model_created(self, model):
        if model and isinstance(model, DefaultWeaponModel):
            self._weapon_model_created(model)
        else:
            raise NotImplementedError


    def _weapon_model_created(self, weapon_model):
        default_weapon_view = self._create_default_weapon_view(weapon_model)
        while weapon_model and weapon_model.is_moving():
            self.game_view.tick()
            weapon_model.move()
            self.update_view()

        self.game_view.deregister_weapon_view()
        del weapon_model
        del default_weapon_view


    def run(self):
        pygame.mixer.init()
        pygame.mixer.music.load("sound/ambience.wav")
        pygame.mixer.music.play(-1)

        while not self.game_model.is_game_over():
            self.game_model.select_active_player()
            if isinstance(self.game_model.active_player, AIPlayerModel):
                self.game_model.active_player.set_attack()
            else:
                self._get_events()

            self.game_model.execute()

        return Scenes.RESULT, self.game_model.get_result()


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
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit()


    def _create_default_weapon_view(self, model):
        default_weapon_view = DefaultWeaponView()
        default_weapon_view.register_model(model)
        self.game_view.register_weapon_view(default_weapon_view)

        return default_weapon_view


    def update_view(self):
        self.game_view.draw()


    def _create_scene(self, init_state):
        #self.DISPLAYSURF.fill(WHITE)
        pygame.display.set_caption("Tank Wars")

        player1 = HumanPlayerModel(name=init_state['player1'])

        if init_state["AI"]:
            player2 = AIPlayerModel(name=init_state['player2'])
        else:
            player2 = HumanPlayerModel(name=init_state['player2'])


        self.game_view = GameView(DISPLAYSURF=self.DISPLAYSURF)
        self.game_model = GameModel(player1=player1, player2=player2)
        self.game_model.register_controller(controller=self)

        args = {
            "MIN_SPLINE_POINTS": 2,
            "MAX_SPLINE_POINTS": 5,
            "MIN_X_DISTANCE": 50,
            "MIN_Y_DISTANCE": 20
        }
        terrain_model = TerrainModel(args=args)
        terrain_view = TerrainView(DISPLAYSURF=self.DISPLAYSURF)
        terrain_view.register_model(terrain_model=terrain_model)
        self.game_view.register_terrain_view(terrain_view=terrain_view)
        self.game_model.register_terrain_model(terrain_model=terrain_model)

        color = RED if init_state['p1_color'] == 'Red' else BLUE
        tank_model = TankModel(position=Position(100, 400),
                               angle=45,
                               strength=40,
                               color=color)
        tank_view = TankView(DISPLAYSURF=self.DISPLAYSURF)
        tank_view.register_model(tank_model)
        tank_model.register_terrain_model(terrain_model=terrain_model)
        self.game_model.register_tank_model(tank_model=tank_model)
        self.game_view.register_tank_view(tank_view=tank_view)
        player1.register_tank_model(tank_model=tank_model)

        color = RED if init_state['p2_color'] == 'Red' else BLUE
        tank_model_2 = TankModel(position=Position(WIDTH-100, 400),
                                 angle=135,
                                 strength=40,
                                 color=color)
        tank_view_2 = TankView(DISPLAYSURF=self.DISPLAYSURF)
        tank_view_2.register_model(tank_model_2)
        tank_model_2.register_terrain_model(terrain_model=terrain_model)
        self.game_model.register_tank_model(tank_model=tank_model_2)
        self.game_view.register_tank_view(tank_view=tank_view_2)
        player2.register_tank_model(tank_model=tank_model_2)

        terrain_model.register_collideable(tank_model)
        terrain_model.register_collideable(tank_model_2)
        self.game_view.register_model(game_model=self.game_model)

        if isinstance(player2, AIPlayerModel):
            player2.register_other_tank_model(tank_model)
            player2.register_terrain_model(terrain_model)


