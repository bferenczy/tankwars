import pygame, sys
from pygame.locals import *


from player import HumanPlayer, AIPlayer
from game import Game
from constants import WIDTH, HEIGHT, WHITE


DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(WHITE)
FramePerSec = pygame.time.Clock()


def main():

    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("Game")

    player1 = HumanPlayer("Bazsi", 2)
    player2 = AIPlayer("Laci", 6)
    game = Game(player1, player2, DISPLAYSURF, FramePerSec)
    game.run()


if __name__ == "__main__":
    main()
