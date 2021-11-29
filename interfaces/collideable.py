from abc import ABC, abstractmethod

class ICollideable(ABC):

    @abstractmethod
    def hit(self, other_surface, other_object) -> bool:
        pass

    @abstractmethod
    def collide(self, intersection, other_surface) -> None:
        pass

    @abstractmethod
    def get_surface(self):
        # Shapely geometry representation of obejct's surface
        pass
