import pygame
import math

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

        tankPolygon = list(self.tank_model.get_surface().exterior.coords)
        tankPolygon = list(map(lambda x: [x[0], HEIGHT-x[1]], tankPolygon))
        pygame.draw.polygon(self.DISPLAYSURF, self.tank_model.color, tankPolygon)

        # Draw gun
        startingPoint = [top_left_corner[0] + width/2, top_left_corner[1]]
        unitCircleX = math.cos(math.radians(self.tank_model.angle))
        unitCircleY = math.sin(math.radians(self.tank_model.angle))
        gunLength = 15
        endPoint = [startingPoint[0] + (unitCircleX * gunLength), startingPoint[1]-(unitCircleY * gunLength)]
        pygame.draw.line(self.DISPLAYSURF, self.tank_model.color, startingPoint, endPoint, width=4)

        #surface = self.tank_model.get_surface()
        #for i in range(len(list(surface.exterior.coords))-1):
        #    p1 = [list(surface.exterior.coords)[i][0], -list(surface.exterior.coords)[i][1]+HEIGHT]
        #    p2 = [list(surface.exterior.coords)[i+1][0], -list(surface.exterior.coords)[i+1][1]+HEIGHT]
        #    pygame.draw.line(self.DISPLAYSURF, [255, 255, 0], p1, p2)



    def update_view(self):
        self.draw()


