from math import sin, cos, radians
from shapely import geometry
import pygame
from .model import IModel
from interfaces.collideable import ICollideable
from helper.constants import RED
from helper.basic_types import Position
from .default_weapon_model import DefaultWeaponModel


class TankModel(IModel, ICollideable):

    def __init__(self, position=None, angle=None, strength=None, color=RED):
        self.terrain_model = None
        self.trajectory = list()
        self.position = position
        self.width = 39
        self.height = 14.5
        self.angle = angle
        self.strength = strength
        self.health = 100
        self.color = color
        self.last_damage = 0
        self.update() if self.terrain_model else None

    def register_terrain_model(self, terrain_model):
        self.terrain_model = terrain_model
        self.update()

    def get_trajectory(self):
        return [[int(v.x), int(v.y)] for v in self.trajectory]

    def set_position(self, x, y):
        self.position = Position(x, y)

    def set_angle(self, new_angle):
        self.angle = new_angle

    def set_strength(self, new_strength):
        self.strength = new_strength

    def get_surface(self):
        tank_shape = [[0, -3.5], [9, -3.5], [12.5, 0], [26, 0], [29.5, -3.5],
                      [39, -3.5], [39, -7], [29.5, -14.5], [9, -14.5], [0, -7]]
        tank_shape = list(
            map(lambda x: [x[0] + self.position[0] - self.width / 2, x[1] + self.position[1] + self.height / 2],
                tank_shape))
        return geometry.Polygon(tank_shape)

    def collide(self, intersection, other_surface):
        if isinstance(other_surface, DefaultWeaponModel):
            current_time = pygame.time.get_ticks()  # in millis
            t = (current_time - other_surface.start_time) / 100
            total_damage = max(other_surface.get_damage() + other_surface.strength / 2 - t * 2.5,
                               other_surface.get_damage() / 2)
            self.health -= total_damage
            self.last_damage = total_damage
            self.terrain_model.collide(self.position, self)

    def modify_angle(self, angle_difference):
        self.angle = self.angle + angle_difference
        if self.angle == 90 or self.angle == 270:
            if angle_difference > 0:
                self.angle += 1
            else:
                self.angle -= 1

    def modify_strength(self, strength_difference):
        self.strength = self.strength + strength_difference
        if self.strength < 0:
            self.strength = 0

        if self.strength > 100:
            self.strength = 100

    def hit(self, other_surface, other_object) -> bool:
        tank_surface = self.get_surface()
        return tank_surface.intersects(other_surface)

    def get_state(self):
        return self.position, self.width, self.height

    def get_damage(self):
        return self.last_damage

    def execute(self, collideables):
        weapon = DefaultWeaponModel()

        unit_circle_x = cos(radians(self.angle))
        unit_circle_y = sin(radians(self.angle))
        gun_length = 15

        position = Position(
            x=self.position.x + unit_circle_x * gun_length,
            y=self.position.y + self.height + unit_circle_y * gun_length
        )
        weapon.fire(position, self.strength, self.angle, collideables)

        return weapon

    def update(self):
        terrain_state = self.terrain_model.get_terrain_state()
        self.position = Position(
            x=self.position.x,
            y=terrain_state[self.position.x] + self.height / 2
        )
