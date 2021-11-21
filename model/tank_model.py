from collections import namedtuple
from math import sin, cos, tan, radians
from shapely import geometry

from constants import WIDTH, HEIGHT
# TODO:remov
from weapon import DefaultWeapon


Position = namedtuple("Position", "x y")
Vector = namedtuple("Vector", "x y")


class TankModel():


    def __init__(self):
        self.terrain_model = None
        self.position = None
        self.angle = None
        self.strength = None
        self._trajectory = list()


    def register_terrain_model(self, terrain_model):
        self.terrain_model = terrain_model


    def get_trajectory(self):
        return [[int(v.x), int(v.y)] for v in self._trajectory]


    def set_position(self, x, y):
        self.position = Position(x, y)


    def set_angle(self, new_angle):
        self.angle = new_angle


    def set_strength(self, new_strength):
        self.strength = new_strength


    def modifiy_angle(self, angle_difference):
        self.angle = self.angle + angle_difference


    def modifiy_strength(self, strength_difference):
        self.strength = self.strength + strength_difference


    def _calculate_collision(self):
        terrain = self.terrain_model.get_terrain_surface()
        terrain_surface = geometry.LineString(terrain)
        projectile_trajectory = geometry.LineString(self.get_trajectory())

        intersection = terrain_surface.intersection(projectile_trajectory)
        weapon = DefaultWeapon()
        self.terrain_model.destruct(int(intersection.coords[0][0]), weapon)


    def _calculate_trajectory(self):
        # https://courses.lumenlearning.com/boundless-physics/chapter/projectile-motion/
        u = self.strength

        # gravitational force
        g = 10

        trajectory = list()
        # parabolic form of the projectile motion
        for x in range(WIDTH):
            y = (tan(radians(self.angle)) * x) - ((g/(2 * u*u * cos(radians(self.angle)))) * x*x)
            trajectory.append(Vector(x + self.position.x, y + self.position.y))

        self._trajectory = trajectory


    def execute(self):
        trajectory = self._calculate_trajectory()
        self._calculate_collision()


