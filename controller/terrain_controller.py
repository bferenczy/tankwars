from .controller import Controller
from model.terrain_model import TerrainModel


class TerrainController(Controller):


    def __init__(self, terrain_model=None, terrain_view=None):
        self.terrain_model = terrain_model
        self.terrain_view = terrain_view


    def register_view(self, terrain_view):
        self.terrain_view = terrain_view


    def register_model(self, terrain_model):
        self.terrain_model = terrain_model


    def update_view(self):
        self.terrain_view.draw()


    def register_controller(self):
        pass

