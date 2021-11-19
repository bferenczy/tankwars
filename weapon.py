class IWeapon:
    def __init__(self) -> None:
        self.damage = 3
        self.weight = 10

    def get_damage(self) -> int:
        return self.damage


class DefaultWeapon(IWeapon):
    def __init__(self) -> None:
        self.damage = 30
        self.falloff = 0
        self.weight = 10
