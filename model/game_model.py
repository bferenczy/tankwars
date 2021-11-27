from .model import IModel
from player import Player


class GameModel(IModel):


    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.active_player = None
        self.tank_model = None
        self.collideables = list()


    def register_terrain_model(self, terrain_model):
        self.terrain_model = terrain_model
        self.collideables.append(terrain_model)


    def register_tank_model(self, tank_model):
        self.tank_model = tank_model
        self.collideables.append(tank_model)
        # TODO: Move 
        self.tank_model.set_position(120, 200)


    def modify_angle(self, difference):
        self.tank_model.modify_angle(difference)
        self.tank_model._calculate_trajectory()


    def modify_strength(self, difference):
        self.tank_model.modify_strength(difference)
        self.tank_model._calculate_trajectory()


    def execute(self):
        return self.tank_model.execute(self.collideables)


    def select_active_player(self):
        if self.active_player is None:
            self.active_player = self.players[0]
        else:
            self.active_player = next(
                filter(lambda x: x != self.active_player, self.players)
            )

        print("Selected " + self.active_player.get_name() + " as active player.")


