from abc import ABC, abstractmethod
from random import randrange
from .model import IModel


class IPlayerModel(IModel, ABC):

    @abstractmethod
    def get_name(self):
        return

    @abstractmethod
    def get_health(self):
        return

    @abstractmethod
    def register_tank_model(self):
        return


class HumanPlayerModel(IPlayerModel):

    def __init__(self, name=None, tank_model=None):
        self.name = name
        self.tank_model = tank_model

    def get_name(self):
        return self.name

    def register_tank_model(self, tank_model):
        self.tank_model = tank_model

    def get_tank_model(self):
        return self.tank_model

    def get_health(self):
        return self.tank_model.health

    def execute(self):
        pass


class AIPlayerModel(IPlayerModel):

    def __init__(self, name=None, tank_model=None):
        self.name = name
        self.tank_model = tank_model
        self.other_tank_model = None
        self.terrain_model = None

    def register_other_tank_model(self, other_tank_model):
        self.other_tank_model = other_tank_model

    def register_terrain_model(self, terrain_model):
        self.terrain_model = terrain_model

    def get_name(self):
        return self.name

    def register_tank_model(self, tank_model):
        self.tank_model = tank_model

    def get_tank_model(self):
        return self.tank_model

    def execute(self, collideables):
        pass

    def set_attack(self):
        angle = randrange(110, 160)
        strength = randrange(40, 80)
        self.tank_model.set_angle(angle)
        self.tank_model.set_strength(strength)

    def get_health(self):
        return self.tank_model.health
