from model.game_model import GameModel
from view.game_view import GameView


class GameController:


    def __init__(self, game_model, game_view):
        self.game_model = game_model
        self.game_view = game_view


    def run(self):
        while not self._is_game_over():
            self._step()


    def _step(self):
        self.game_view.refresh_screen()
        # read user input - attack
        aimed_column = self._get_user_input()
        self.game_model.round(aimed_column=aimed_column)
        # Why is this necessary?
        self.game_view.tick()


    def _get_user_input(self):
        return int(input())


    def _is_game_over(self):
        return False;

