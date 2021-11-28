from abc import ABC, abstractmethod
from .model import IModel


class IPlayerModel(IModel, ABC):


    @abstractmethod
    def get_name(self):
        return


    @abstractmethod
    def register_tank_model(self):
        return



class HumanPlayerModel(IPlayerModel):


    def __init__(self, name=None, tank_model=None):
        self.name = name
        self.tank_model = None


    def get_name(self):
        return self.name


    def register_tank_model(self, tank_model):
        self.tank_model = tank_model


    def get_tank_model(self):
        return self.tank_model


    def execute(self):
        pass


class AIPlayerModel(IPlayerModel):


    def __init__(self, name=None, tank_model=None):
        self.name = name
        self.tank_model = None
        self.health = 100


    def get_name(self):
        return self.name


    def register_tank_model(self, tank_model):
        self.tank_model = tank_model


    def get_tank_model(self):
        return self.tank_model


