from abc import ABC, abstractmethod
from random import randrange
import pygame
from math import sin, radians

from .model import IModel
from constants import G


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
        self.tank_model = None


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
        self.tank_model = None
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


    def execute(self):
        pass


    def set_attack(self):
        angle = randrange(90, 160)
        strength = randrange(40, 100)

        while self._check_distance(angle, strength) is False:
            strength = randrange(40, 90)

        self.tank_model.set_angle(angle)
        self.tank_model.set_strength(strength)


    def _check_distance(self, angle, strength):
        tank_distance = abs(self.tank_model.position.x - self.other_tank_model.position.x)
        return True


    def _calculate_trajectory(self, angle, strength, x):
        # https://courses.lumenlearning.com/boundless-physics/chapter/projectile-motion/
        u = strength
        a = angle
        # parabolic form of the projectile motion
        y = (tan(radians(a)) * x) - ((G/(2 * u*u * cos(radians(a)) * cos(radians(a)) )) * x*x)

        

    def get_health(self):
        return self.tank_model.health

