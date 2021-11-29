from helper.ui_elements import *


class GUI:

    def __init__(self, screen, players=None) -> None:
        self.players = players
        self.screen = screen
        self.health_p1 = ProgressBar(self.screen, [22, 25, 270, 10], Align.RIGHT, C_HEALTH)
        self.strength_p1 = ProgressBar(self.screen, [192, 38, 100, 10], Align.RIGHT, C_STRENGTH)
        self.p1_name = Text(self.screen, self.players[0].name, pos=[22, 35])
        self.p2_name = Text(self.screen, self.players[1].name, pos=[617, 35], align=Align.RIGHT)
        self.vs = Text(self.screen, "vs", pos=[0, 21], align=Align.CENTER, size=26)
        self.health_p2 = ProgressBar(self.screen, [348, 25, 270, 10], Align.LEFT, C_HEALTH)
        self.strength_p2 = ProgressBar(self.screen, [348, 38, 100, 10], Align.LEFT, C_STRENGTH)
        self.__update()

    def draw(self):
        self.__update()
        self.health_p1.draw()
        self.strength_p1.draw()
        self.p1_name.draw()
        self.p2_name.draw()
        self.vs.draw()
        self.health_p2.draw()
        self.strength_p2.draw()

    def __update(self):
        self.strength_p1.set_status(self.players[0].tank_model.strength / 100)
        self.health_p1.set_status(self.players[0].tank_model.health / 100)
        self.health_p2.set_status(self.players[1].tank_model.health / 100)
        self.strength_p2.set_status(self.players[1].tank_model.strength / 100)
