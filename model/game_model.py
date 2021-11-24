from player import Player
from weapon import DefaultWeapon


class GameModel():

    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.active_player = None
        self.tank_model = None


    def register_terrain_model(self, terrain_model):
        self.terrain_model = terrain_model


    def register_tank_model(self, tank_model):
        self.tank_model = tank_model


    def round(self, aimed_column):
        self._select_active_player()
        self.active_player.step()
        weapon = DefaultWeapon()
        self.tank_model.set_strength(40)
        self.tank_model.set_angle(aimed_column)
        self.tank_model.set_position(120, 150)
        self.tank_model.execute()
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


