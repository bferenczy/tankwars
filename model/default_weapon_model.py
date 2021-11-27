from shapely import geometry
from math import sin, cos, radians
import pygame


from collideable import ICollideable
from basic_types import Position, Vector


class DefaultWeaponModel(ICollideable):


    def __init__(self):
        self.current_position = None
        self.start_position = None
        self.radius = 10
        self.strength = None
        self.angle = None
        self.start_time = None
        self.moving = False
        self.collideables = list()


    def hit(self, other_surface) -> bool:
        projectile_surface = self.get_surface()
        intersection = projectile_surface.intersection(other_surface)

        return True if intersection.coords else False


    def collide(self) -> None:
        pass


    def get_surface(self):
        # Shapely geometry representation of obejct's surface
        return geometry.Point(self.current_position.x, self.current_position.y).buffer(self.radius)


    def is_moving(self):
        return self.moving


    def fire(self, position, strength, angle, collideables):
        self.collideables = collideables
        self.start_time = pygame.time.get_ticks() # save t0 in millis
        self.current_position = position
        self.start_position = position
        self.strength = strength
        self.angle = angle
        self.moving = True


    def get_state(self):
        return list(self.current_position), self.radius


    def get_damage(self):
        return self.radius


    def move(self):
        current_time = pygame.time.get_ticks() # in millis
        t = (current_time - self.start_time) / 1000
        g = 10

        displacement = Vector(
            x = self.strength * t * cos(radians(self.angle)),
            y = self.strength * t * sin(radians(self.angle)) - (0.5 * g * t*t)
        )

        self.current_position = Position(
            x = self.start_position.x + displacement.x,
            y = self.start_position.y + displacement.y
        )

        for collideable in self.collideables:
            if (intersection := collideable.hit(self.get_surface())):
                print("Hit", intersection)
                x = intersection[0][0]
                collideable.collide(int(x), self)
                self.moving = False

