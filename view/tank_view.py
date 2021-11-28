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
        top_left_corner = (int(position[0] - width/2),
                           -int(position[1] + height/2)+HEIGHT)
        pygame.draw.rect(self.DISPLAYSURF,
                         [0, 0, 255],
                         [top_left_corner[0],
                          top_left_corner[1],
                          width,
                          height])


        # surface = self.tank_model.get_surface()
        # for i in range(len(list(surface.coords))-1):
        #     p1 = [list(surface.coords)[i][0], -list(surface.coords)[i][1]+HEIGHT]
        #     p2 = [list(surface.coords)[i+1][0], -list(surface.coords)[i+1][1]+HEIGHT]
        #     pygame.draw.line(self.DISPLAYSURF, [255, 0, 0], p1, p2)



    def update_view(self):
        self.draw()


