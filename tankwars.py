import pygame, sys
from pygame.locals import *


from player import HumanPlayer, AIPlayer
from model.game_model import GameModel
from controller.game_controller import GameController
from view.game_view import GameView
from model.terrain_model import TerrainModel
from view.terrain_view import TerrainView
from model.tank_model import TankModel
from view.tank_view import TankView
from constants import WIDTH, HEIGHT, WHITE


DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(WHITE)


def main():
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("Game")

    player1 = HumanPlayer("Bazsi", 2)
    player2 = AIPlayer("Laci", 6)


    game_view = GameView(DISPLAYSURF=DISPLAYSURF)
    game_model = GameModel(player1=player1,
                           player2=player2)
    game_controller = GameController(game_model=game_model,
                                     game_view=game_view)

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

    tank_model = TankModel()
    tank_view = TankView()
    tank_view.register_model(tank_model)
    game_model.register_tank_model(tank_model=tank_model)
    game_view.register_tank_view(tank_view=tank_view)

    try:
        game_controller.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
