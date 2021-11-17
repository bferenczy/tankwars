from player import Player
from weapon import DefaultWeapon

class GameModel:

    def __init__(self, player1, player2, terrain):
        self.players = [player1, player2]
        self.terrain = terrain
        self.active_player = None


    def round(self, aimed_column):
        self._select_active_player()
        self.active_player.step()
        weapon = DefaultWeapon()
        self.terrain.destruct(aimed_column, weapon)
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


