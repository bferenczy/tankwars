from .model import IModel
from player import Player


class GameModel(IModel):


    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.active_player = None
        self.tank_models = list()
        self.active_tank_model = None
        self.collideables = list()


    def register_terrain_model(self, terrain_model):
        self.terrain_model = terrain_model
        self.collideables.append(terrain_model)


    def register_tank_model(self, tank_model):
        self.tank_models.append(tank_model)
        self.collideables.append(tank_model)


    def modify_angle(self, difference):
        self.active_tank_model.modify_angle(difference)
        self.active_tank_model._calculate_trajectory()


    def modify_strength(self, difference):
        self.active_tank_model.modify_strength(difference)
        self.active_tank_model._calculate_trajectory()


    def execute(self):
        return self.active_tank_model.execute(self.collideables)


    def select_active_player(self):
        if self.active_player is None:
            self.active_player = self.players[0]
        else:
            self.active_player = next(
                filter(lambda x: x != self.active_player, self.players)
            )

        self.active_tank_model = self.active_player.get_tank_model()

        print("Selected " + self.active_player.get_name() + " as active player.")


