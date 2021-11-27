import pygame

from .view import View

from constants import BLACK, WIDTH, HEIGHT


class TankView(View):


    def __init__(self, DISPLAYSURF):
        self.DISPLAYSURF = DISPLAYSURF
        self.tank_model = None


    def register_model(self, tank_model):
        self.tank_model = tank_model


    def draw(self):
        trajectory = self.tank_model.get_trajectory()

        if not trajectory:
            return

        for x, y in trajectory:
            point = [x, -y + HEIGHT]
            pygame.draw.line(self.DISPLAYSURF, BLACK, point, point)

        # pygame.display.update()


    def update_view(self):
        self.draw()


