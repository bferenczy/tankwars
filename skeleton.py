import random
import pygame, sys
from pygame.locals import *
from shapely import geometry
from scipy.interpolate import InterpolatedUnivariateSpline


WIDTH = 640
HEIGHT = 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60


DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(WHITE)
FramePerSec = pygame.time.Clock()


class Collideable:
    def hit(position, strength) -> bool:
        pass


class IWeapon:
    def __init__(self) -> None:
        self.damage = 3
        self.weight = 10

    def get_damage(self) -> int:
        return self.damage


class Terrain:
    def __init__(self) -> None:
        self.columns = list()
        self.poly = None
        self._generate_random_terrain()

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
            pygame.draw.rect(DISPLAYSURF, BLACK, [x, HEIGHT - y, 1, y])

    def destruct(self, x, weapon: IWeapon):
        y = HEIGHT - self.columns[x]
        point_of_impact = [x, y]
        radius = weapon.get_damage()

        # Calculate the intersection with weapon's radius for each column
        circle = geometry.Point(x, y).buffer(radius)
        circle_points = circle.exterior.coords
        circle_points = [[int(x), int(y)] for [x, y] in circle_points]

        # Draw a circle from weapon's radius
        pygame.draw.polygon(DISPLAYSURF, (0, 255, 0), circle_points)
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


class Player:
    def __init__(self, name: str, pos: int) -> None:
        self.name = name
        self.attack = Attack()
        self.pos = pos
        pass

    def get_name(self) -> str:
        return self.name

    def step(self) -> None:
        print("It's " + self.name + "'s turn")
        # self.attack.changeAngle()
        # self.attack.changeStrength()
        # self.attack.execute()


class DefaultWeapon(IWeapon):
    def __init__(self) -> None:
        self.damage = 30
        self.falloff = 0
        self.weight = 10


class Attack:
    def __init__(self) -> None:
        self.angle, self.strength = 0, 0
        self.weapon = DefaultWeapon()

    def change_angle(self) -> None:
        print("Angle of the shot:")
        self.angle = int(input())

    def change_strength(self) -> None:
        print("Strength of the shot:")
        self.strength = int(input())

    def execute(self) -> None:
        print(
            "Executing attack with strength: "
            + str(self.strength)
            + " and angle: "
            + str(self.angle)
        )


class HumanPlayer(Player):
    def __init__(self, name: str, pos: int) -> None:
        super().__init__(name, pos)


class AIPlayer(Player):
    def __init__(self, name: str, pos: int) -> None:
        super().__init__(name, pos)


class Game:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.players = [player1, player2]
        self.terrain = Terrain()
        self.active_player = None

    def run(self):
        while not self.is_game_over():
            DISPLAYSURF.fill(WHITE)
            self.terrain.draw(DISPLAYSURF)
            pygame.display.update()
            self._round()
            FramePerSec.tick(FPS)

    def _round(self):
        self._select_active_player()
        self.active_player.step()
        weapon = DefaultWeapon()
        aimedColumn = int(input())
        self.terrain.destruct(aimedColumn, weapon)
        kaka = str(input())
        print("------------")
        print("End of round")
        print("------------")

    def _select_active_player(self):
        if self.active_player is None:
            self.active_player = self.players[0]
        else:
            self.active_player = next(
                filter(lambda x: x != self.active_player, self.players)
            )

        print("Selected " + self.active_player.get_name() + " as active player.")

    def is_game_over(self) -> bool:
        return False


def main():

    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption("Game")

    player1 = HumanPlayer("Bazsi", 2)
    player2 = AIPlayer("Laci", 6)
    game = Game(player1, player2)
    game.run()


if __name__ == "__main__":
    main()
