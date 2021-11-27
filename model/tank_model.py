from collections import namedtuple
from math import sin, cos, tan, radians
from shapely import geometry


from .model import IModel
from collideable import ICollideable
from constants import WIDTH, HEIGHT, G
from basic_types import Position, Vector
from .default_weapon_model import DefaultWeaponModel


class TankModel(IModel, ICollideable):


    def __init__(self, position=None, angle=None, strength=None):
        self.terrain_model = None
        self.trajectory = list()
        self.position = position
        self.width = 20
        self.height = 15
        self.angle = angle
        self.strength = strength


    def register_terrain_model(self, terrain_model):
        self.terrain_model = terrain_model


    def get_trajectory(self):
        return [[int(v.x), int(v.y)] for v in self.trajectory]


    def set_position(self, x, y):
        self.position = Position(x, y)


    def set_angle(self, new_angle):
        self.angle = new_angle


    def set_strength(self, new_strength):
        self.strength = new_strength


    def get_surface(self):
        pass


    def collide(self):
        pass


    def modify_angle(self, angle_difference):
        self.angle = self.angle + angle_difference
        if self.angle == 90 or self.angle == 270:
            if angle_difference > 0:
                self.angle += 1
            else:
                self.angle -= 1


    def modify_strength(self, strength_difference):
        self.strength = self.strength + strength_difference


    def hit(self, other_surface) -> bool:
        pass


    def get_state(self):
        return self.position, self.width, self.height


    def _calculate_trajectory(self):
        # https://courses.lumenlearning.com/boundless-physics/chapter/projectile-motion/
        u = self.strength

        trajectory = list()
        # parabolic form of the projectile motion
        for x in range(-WIDTH, WIDTH):
            y = (tan(radians(self.angle)) * x) - ((G/(2 * u*u * cos(radians(self.angle)) * cos(radians(self.angle)) )) * x*x)
            trajectory.append(Vector(x + self.position.x, y + self.position.y))


        self.trajectory = trajectory


    def execute(self, collideables):
        weapon = DefaultWeaponModel()
        weapon.fire(self.position, self.strength, self.angle, collideables)
        #self.trajectory = []

        return weapon


    def update(self):
        terrain_state = self.terrain_model.get_terrain_state()
        self.position = Position(
            x = self.position.x,
            y = terrain_state[self.position.x] + self.height
        )
