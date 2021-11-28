from .model import IModel


class GameModel(IModel):


    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.controller = None
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


    def register_controller(self, controller):
        self.controller = controller


    def modify_angle(self, difference):
        self.active_tank_model.modify_angle(difference)
        #self.active_tank_model._calculate_trajectory()


    def modify_strength(self, difference):
        self.active_tank_model.modify_strength(difference)
        #self.active_tank_model._calculate_trajectory()


    def execute(self):
        weapon = self.active_tank_model.execute(self.collideables)
        self.controller.new_model_created(weapon)


    def select_active_player(self):
        if self.active_player is None:
            self.active_player = self.players[0]
        else:
            self.active_player = next(
                filter(lambda x: x != self.active_player, self.players)
            )

        self.active_tank_model = self.active_player.get_tank_model()

        print("Selected " + self.active_player.get_name() + " as active player.")


    def get_result(self):
        result = []
        for p in self.players:
            result.append({
                "name": p.get_name(),
                "winner": p.get_health() > 0
            })

        return result


    def is_game_over(self):
        for p in self.players:
            if p.get_health() <= 0:
                return True

        return False


