from abc import ABC, abstractmethod

from moveable import IMoveable

class IWeapon(IMoveable, ABC):


    @abstractmethod
    def get_damage(self) -> int:
        return self.damage

