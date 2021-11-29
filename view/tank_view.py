import pygame
import math

from .view import View

from helper.constants import BLACK, HEIGHT


class TankView(View):

    def __init__(self, screen):
        self.screen = screen
        self.tank_model = None

    def register_model(self, tank_model):
        self.tank_model = tank_model

    def draw(self):
        for x, y in self.tank_model.get_trajectory():
            point = [x, -y + HEIGHT]
            pygame.draw.line(self.screen, BLACK, point, point)

        position, width, height = self.tank_model.get_state()
        top_left_corner = (int(position[0] - width / 2),
                           -int(position[1] + height / 2) + HEIGHT)

        tank_polygon = list(self.tank_model.get_surface().exterior.coords)
        tank_polygon = list(map(lambda z: [z[0], HEIGHT - z[1]], tank_polygon))
        pygame.draw.polygon(self.screen, self.tank_model.color, tank_polygon)

        # Draw gun
        starting_point = [top_left_corner[0] + width / 2, top_left_corner[1]]
        unit_circle_x = math.cos(math.radians(self.tank_model.angle))
        unit_circle_y = math.sin(math.radians(self.tank_model.angle))
        gun_length = 15
        end_point = [starting_point[0] + (unit_circle_x * gun_length), starting_point[1] - (unit_circle_y * gun_length)]
        pygame.draw.line(self.screen, self.tank_model.color, starting_point, end_point, width=4)

    def update_view(self):
        self.draw()
