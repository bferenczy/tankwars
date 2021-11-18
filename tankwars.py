import pygame, sys
from pygame.locals import *


from player import HumanPlayer, AIPlayer
from model.game_model import GameModel
from controller.game_controller import GameController
from view.game_view import GameView
from model.terrain_model import TerrainModel
from controller.terrain_controller import TerrainController
from view.terrain_view import TerrainView
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


    args = {
        "MIN_SPLINE_POINTS": 2,
        "MAX_SPLINE_POINTS": 5,
        "MIN_X_DISTANCE": 50,
        "MIN_Y_DISTANCE": 20
    }
    terrain_model = TerrainModel(args=args)
    terrain_view = TerrainView(DISPLAYSURF=DISPLAYSURF)
    terrain_controller = TerrainController()
    terrain_view.register_model(terrain_model=terrain_model)
    terrain_controller.register_model(terrain_model=terrain_model)
    terrain_controller.register_view(terrain_view=terrain_view)


    game_view = GameView(DISPLAYSURF=DISPLAYSURF)
    game_model = GameModel(player1=player1,
                           player2=player2,
                           terrain_model=terrain_model)
    game_controller = GameController(game_model=game_model,
                                     game_view=game_view)

    game_controller.register_controller(controller=terrain_controller)

    try:
        game_controller.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
