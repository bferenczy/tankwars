from .controller import Controller
from model.game_model import GameModel
from view.game_view import GameView


class GameController(Controller):


    def __init__(self, game_model=None, game_view=None):
        self.game_model = game_model
        self.game_view = game_view


    def register_model(self, game_model):
        self.game_model = game_model


    def register_view(self, game_view):
        self.game_view = game_view


    def run(self):
        while not self._is_game_over():
            self._step()


    def _step(self):
        self.update_view()
        # read user input - attack
        aimed_column = self._get_user_input()
        self.game_model.round(aimed_column=aimed_column)
        # Why is this necessary?
        self.game_view.tick()


    def update_view(self):
        self.game_view.draw()


    def _get_user_input(self):
        return int(input())


    def _is_game_over(self):
        return False;

