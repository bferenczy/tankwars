from attack import Attack


class Player:
    def __init__(self, name: str, pos: int) -> None:
        self.name = name
        self.attack = Attack()
        self.pos = pos


    def get_name(self) -> str:
        return self.name


    def step(self) -> None:
        print("It's " + self.name + "'s turn")
        # self.attack.changeAngle()
        # self.attack.changeStrength()
        # self.attack.execute()


class HumanPlayer(Player):
    def __init__(self, name: str, pos: int) -> None:
        super().__init__(name, pos)


class AIPlayer(Player):
    def __init__(self, name: str, pos: int) -> None:
        super().__init__(name, pos)

