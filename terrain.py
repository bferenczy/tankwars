import random
from scipy.interpolate import InterpolatedUnivariateSpline
import pygame, sys
from shapely import geometry

from weapon import IWeapon
from constants import WIDTH, HEIGHT, BLACK


class Terrain:
    def __init__(self, DISPLAYSURF) -> None:
        self.columns = list()
        self.poly = None
        self._generate_random_terrain()
        self.DISPLAYSURF = DISPLAYSURF

    def _generate_random_terrain(self):
        # We generate a spline to create a terrain
        # Randomly generate the number of points to connect with a spline
        MIN_SPLINE_POINTS = 2
        MAX_SPLINE_POINTS = 5
        num_of_points = random.randrange(MIN_SPLINE_POINTS, MAX_SPLINE_POINTS)

        # Randomly generate the X position for each point
        MIN_X_DISTANCE = 50
        x = sorted(random.sample(range(WIDTH), num_of_points))
        x = sorted(x + [0, WIDTH])

        while not self._has_min_distance(x, MIN_X_DISTANCE):
            x = sorted(random.sample(range(WIDTH), num_of_points))
            x = sorted(x + [0, WIDTH])

        # Randomly generate the Y position for each point
        MIN_Y_DISTANCE = 20
        y = sorted(random.sample(range(int(HEIGHT * (2 / 3))), num_of_points))
        y.insert(0, int(HEIGHT / 2))
        y.append(int(HEIGHT / 2))

        while not self._has_min_distance(y, MIN_Y_DISTANCE):
            y = random.sample(range(int(HEIGHT * (2 / 3))), num_of_points)
            y.insert(0, int(HEIGHT / 2))
            y.append(int(HEIGHT / 2))

        # Create spline
        spline = InterpolatedUnivariateSpline(x, y)

        # Get all coordinates
        y_coords = spline(range(WIDTH))

        for p in y_coords:
            if p < 20:
                p = 20
            if p > HEIGHT * (2 / 3):
                p = HEIGHT * (2 / 3)
            self.columns.append(int(p))

    def _has_min_distance(self, points, distance) -> bool:
        for idx, p in enumerate(points):
            if idx != len(points) - 1:
                if (abs(points[idx + 1] - p)) < distance:
                    return False

        return True

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

        # Draw a circle from weapon's radius
        pygame.draw.polygon(self.DISPLAYSURF, (0, 255, 0), circle_points)
        pygame.display.update()

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
