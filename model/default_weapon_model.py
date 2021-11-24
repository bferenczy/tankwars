from shapely import geometry


from collideable import ICollideable
from basic_types import Position


class DefaultWeaponModel(ICollideable):


    def __init(self):
        self.position = Position(0, 0)
        self.damage = 30
        self.falloff = 0
        self.weight = 40
        self.radius = 10


    def hit(self) -> bool:
        pass


    def collide(self) -> None:
        pass


    def get_surface(self):
        # Shapely geometry representation of obejct's surface
        return geometry.Point(self.position.x, self.position.y)
                       .buffer(self.radius)
