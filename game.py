import pygame, sys

from player import Player
from weapon import DefaultWeapon
from terrain import Terrain
from constants import WHITE, FPS


class Game:
    def __init__(
        self, player1: Player, player2: Player, DISPLAYSURF, FramePerSec
    ) -> None:
        self.players = [player1, player2]
        self.DISPLAYSURF = DISPLAYSURF
        self.FramePerSec = FramePerSec
        self.terrain = Terrain(self.DISPLAYSURF)
        self.active_player = None

    def run(self):
        while not self.is_game_over():
            self.DISPLAYSURF.fill(WHITE)
            self.terrain.draw(self.DISPLAYSURF)
            pygame.display.update()
            self._round()
            self.FramePerSec.tick(FPS)

    def _round(self):
        self._select_active_player()
        self.active_player.step()
        weapon = DefaultWeapon()
        aimedColumn = int(input())
        self.terrain.destruct(aimedColumn, weapon)
        kaka = str(input())
        print("------------")
        print("End of round")
        print("------------")

    def _select_active_player(self):
        if self.active_player is None:
            self.active_player = self.players[0]
        else:
            self.active_player = next(
                filter(lambda x: x != self.active_player, self.players)
            )

        print("Selected " + self.active_player.get_name() + " as active player.")

    def is_game_over(self) -> bool:
        return False
