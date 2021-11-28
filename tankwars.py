import pygame, sys
from pygame.locals import *

from model.player_model import HumanPlayerModel
from model.game_model import GameModel
from controller.game_controller import GameController
from view.game_view import GameView
from model.terrain_model import TerrainModel
from view.gui import GUI
from view.terrain_view import TerrainView
from model.tank_model import TankModel
from view.tank_view import TankView
from constants import WIDTH, HEIGHT, WHITE
from basic_types import Position


DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(WHITE)


def main():
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("Game")

    player1 = HumanPlayerModel(name="Bazsi")
    player2 = HumanPlayerModel(name="Laci")

    game_view = GameView(DISPLAYSURF=DISPLAYSURF)
    game_model = GameModel(player1=player1,
                           player2=player2)
    game_controller = GameController(game_model=game_model,
                                     game_view=game_view)
    game_model.register_controller(controller=game_controller)

    args = {
        "MIN_SPLINE_POINTS": 2,
        "MAX_SPLINE_POINTS": 5,
        "MIN_X_DISTANCE": 50,
        "MIN_Y_DISTANCE": 20
    }
    terrain_model = TerrainModel(args=args)
    terrain_view = TerrainView(DISPLAYSURF=DISPLAYSURF)
    terrain_view.register_model(terrain_model=terrain_model)
    game_view.register_terrain_view(terrain_view=terrain_view)
    game_model.register_terrain_model(terrain_model=terrain_model)

    tank_model = TankModel(position=Position(100, 400),
                           angle=45,
                           strength=40)
    tank_view = TankView(DISPLAYSURF=DISPLAYSURF)
    tank_view.register_model(tank_model)
    tank_model.register_terrain_model(terrain_model=terrain_model)
    game_model.register_tank_model(tank_model=tank_model)
    game_view.register_tank_view(tank_view=tank_view)
    player1.register_tank_model(tank_model=tank_model)


    tank_model_2 = TankModel(position=Position(WIDTH-100, 400),
                             angle=135,
                             strength=40, color = [0,0,255])
    tank_view_2 = TankView(DISPLAYSURF=DISPLAYSURF)
    tank_view_2.register_model(tank_model_2)
    tank_model_2.register_terrain_model(terrain_model=terrain_model)
    game_model.register_tank_model(tank_model=tank_model_2)
    game_view.register_tank_view(tank_view=tank_view_2)
    player2.register_tank_model(tank_model=tank_model_2)
    terrain_model.register_collideable(tank_model)
    terrain_model.register_collideable(tank_model_2)
    game_view.register_model(game_model=game_model)


    try:
        game_controller.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()

