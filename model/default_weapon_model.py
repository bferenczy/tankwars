from shapely import geometry
from shapely.validation import make_valid, explain_validity
from math import sin, cos, radians
import pygame


from collideable import ICollideable
from weapon import IWeapon
from constants import WIDTH, HEIGHT, G
from basic_types import Position, Vector


class DefaultWeaponModel(IWeapon ,ICollideable):

    SOUND_SHOT = pygame.mixer.Sound("sound/shot.wav")
    SOUND_IMPACT = pygame.mixer.Sound("sound/impact.wav")

    def __init__(self):
        self.current_position = None
        self.start_position = None
        self.radius = 5
        self.strength = None
        self.angle = None
        self.start_time = None
        self.moving = False
        self.collideables = list()


    def hit(self, other_surface) -> bool:
        projectile_surface = self.get_surface()
        intersection = projectile_surface.intersection(other_surface)

        return False if not list(intersection.coords) else list(intersection.coords)


    def collide(self) -> None:
        pass


    def get_surface(self):
        # Shapely geometry representation of obejct's surface
        return geometry.Point(self.current_position.x, self.current_position.y).buffer(self.radius)


    def is_moving(self):
        return self.moving


    def fire(self, position, strength, angle, collideables):
        pygame.mixer.Sound.play(DefaultWeaponModel.SOUND_SHOT)
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
        return self.radius**2


    def move(self):
        if not self.is_valid_position():
            self.moving = False
            return

        current_time = pygame.time.get_ticks() # in millis
        t = (current_time - self.start_time) / 100

        if t == 0: return

        displacement = Vector(
            x = self.strength * t * cos(radians(self.angle)),
            y = self.strength * t * sin(radians(self.angle)) - (0.5 * G * t*t)
        )

        new_x = int(self.start_position.x + self.strength * t * cos(radians(self.angle)))
        horizontal_range = sorted([int(self.current_position.x), new_x])

        self.current_position = Position(
            x = self.start_position.x + displacement.x,
            y = self.start_position.y + displacement.y
        )
        
        for x in range(horizontal_range[0], horizontal_range[1]):
            if x == 0: x = 0.01
            dt = (self.strength * cos(radians(self.angle))) / x
            y = self.start_position.y + (self.strength * dt * sin(radians(self.angle)) - (0.5 * G * dt*dt))

            for collideable in self.collideables:
                if (collideable.hit(self.get_surface(), self)):
                    intersection = [int(x), int(y)]
                    pygame.mixer.Sound.play(DefaultWeaponModel.SOUND_IMPACT)
                    collideable.collide(intersection, self)
                    self.moving = False
                    return
        

        


    def is_valid_position(self):
        if self.current_position.x < 0 or self.current_position.x > WIDTH:
            return False

        if self.current_position.y < 0:
            return False

        return True

