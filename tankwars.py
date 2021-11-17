import pygame, sys
from pygame.locals import *


from player import HumanPlayer, AIPlayer
from model.game_model import GameModel
from controller.game_controller import GameController
from view.game_view import GameView
from constants import WIDTH, HEIGHT, WHITE
from terrain import Terrain


DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(WHITE)


def main():
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("Game")

    terrain = Terrain(DISPLAYSURF=DISPLAYSURF)
    player1 = HumanPlayer("Bazsi", 2)
    player2 = AIPlayer("Laci", 6)

    game_view = GameView(DISPLAYSURF=DISPLAYSURF, terrain=terrain)
    game_model = GameModel(player1=player1, player2=player2, terrain=terrain)
    game_controller = GameController(game_model=game_model, game_view=game_view)

    try:
        game_controller.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
