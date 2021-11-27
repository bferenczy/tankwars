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
        for x, y in self.tank_model.get_trajectory():
            point = [x, -y + HEIGHT]
            pygame.draw.line(self.DISPLAYSURF, BLACK, point, point)


        position, width, height = self.tank_model.get_state()
        bottom_left_corner = (int(position[0] - width/2),
                              -int(position[1] - height/2)+HEIGHT)
        pygame.draw.rect(self.DISPLAYSURF,
                         [0, 0, 255],
                         [bottom_left_corner[0],
                          bottom_left_corner[1],
                          width,
                          height])



    def update_view(self):
        self.draw()


