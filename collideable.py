from abc import ABC, abstractmethod
from shapely import geometry


class ICollideable(ABC):


    @abstractmethod
    def hit(self) -> bool:
        pass


    @abstractmethod
    def collide(self) -> None:
        pass


    @abstractmethod
    def get_surface(self):
        # Shapely geometry representation of obejct's surface
        pass
