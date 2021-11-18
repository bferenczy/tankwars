import random
import pygame, sys
from shapely import geometry

from weapon import IWeapon
from constants import WIDTH, HEIGHT, BLACK


class Terrain:
    def __init__(self, DISPLAYSURF) -> None:
        self.columns = list()
        self._generate_random_terrain()
        self.DISPLAYSURF = DISPLAYSURF


    def draw(self, surface):
        for x, y in enumerate(self.columns):
            pygame.draw.rect(self.DISPLAYSURF, BLACK, [x, HEIGHT - y, 1, y])


    def destruct(self, x, weapon: IWeapon):
        y = HEIGHT - self.columns[x]
        point_of_impact = [x, y]
        radius = weapon.get_damage()

        # Calculate the intersection with weapon's radius for each column
        circle = geometry.Point(x, y).buffer(radius)
        circle_points = circle.exterior.coords
        circle_points = [[int(x), int(y)] for [x, y] in circle_points]

        # Determine the affected columns
        affected_start = max(0, x - radius)
        affected_end = min(x + radius, len(self.columns))

        # Create Linestrings from the affected colums
        line_strings = list()
        for col_x in range(affected_start, affected_end):
            line_strings.append(
                geometry.LineString([(col_x, 480), (col_x, 480 - self.columns[col_x])])
            )

        # Subtract the length of the intersected part of the linestring
        # for each individual column in the affected area.
        for ls in line_strings:
            intersection = ls.intersection(circle)
            length = intersection.length
            if intersection.coords:
                self.columns[int(intersection.coords[0][0])] -= int(length)

