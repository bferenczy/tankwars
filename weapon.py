from abc import ABC, abstractmethod


class IWeapon(ABC):


    @abstractmethod
    def get_damage(self) -> int:
        return self.damage

