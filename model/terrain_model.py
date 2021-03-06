import random
from shapely import geometry
from scipy.interpolate import InterpolatedUnivariateSpline
from .model import IModel
from model.tank_model import TankModel
from interfaces.collideable import ICollideable
from helper.constants import WIDTH, HEIGHT
from interfaces.weapon import IWeapon


def has_min_distance(points, distance) -> bool:
    for idx, p in enumerate(points):
        if idx != len(points) - 1:
            if (abs(points[idx + 1] - p)) < distance:
                return False

    return True


class TerrainModel(ICollideable, IModel):

    def __init__(self, args):
        # holds only the y coordinates sorted by x [0-WIDTH)
        self.columns = list()
        self._generate_random_terrain(args)
        self.collideables = list()

    def get_terrain_state(self):
        return self.columns

    def register_collideable(self, collideable):
        self.collideables.append(collideable)

    def hit(self, other_collideable_surface: geometry, other_object) -> bool:
        pos_x = other_object.current_position.x
        pos_y = other_object.current_position.y
        if pos_x < 0 or pos_x >= len(self.columns):
            return False

        height = self.columns[int(pos_x)]
        return height >= pos_y

    def get_surface(self):
        # Shapely geometry representation of obejct's surface
        surface_points = list(zip([x for x in range(WIDTH)], self.columns))
        return geometry.LineString(surface_points)

    def collide(self, intersection, collideable):
        if isinstance(collideable, IWeapon):
            x = intersection[0]
            self.destruct(x, collideable)
        elif isinstance(collideable, TankModel):
            x = int(intersection[0])
            self.destruct(x, collideable)
        else:
            raise NotImplementedError

        for collideable in self.collideables:
            collideable.update()

    def execute(self, collideables):
        pass

    def _generate_random_terrain(self, args):
        # args = {
        #   MIN_SPLINE_POINTS: int
        #   MAX_SPLINE_POINTS: int
        #   MIN_X_DISTANCE: int
        #   MIN_Y_DISTANCE: int
        # }
        #
        # We generate a spline to create a terrain
        # Randomly generate the number of points to connect with a spline
        num_of_points = random.randrange(args["MIN_SPLINE_POINTS"],
                                         args["MAX_SPLINE_POINTS"])

        # Randomly generate the X position for each point
        x = sorted(random.sample(range(WIDTH), num_of_points))
        x = sorted(x + [0, WIDTH])

        # Limit the spline if it goes out from the screen
        while not has_min_distance(x, args["MIN_X_DISTANCE"]):
            x = sorted(random.sample(range(WIDTH), num_of_points))
            x = sorted(x + [0, WIDTH])
        # Randomly generate the Y position for each point
        y = sorted(random.sample(range(int(HEIGHT * (2 / 3))), num_of_points))
        y.insert(0, int(HEIGHT / 2))
        y.append(int(HEIGHT / 2))

        while not has_min_distance(y, args["MIN_Y_DISTANCE"]):
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

    def destruct(self, x, collideable):
        y = HEIGHT - self.columns[x]
        radius = int(collideable.get_damage())

        # Calculate the intersection with collideable
        circle = geometry.Point(x, y).buffer(radius)

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
