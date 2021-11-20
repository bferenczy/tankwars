from collections import namedtuple


Position = namedtuple("Position", "x y")


class TankModel():


    def __init__(self):
        self.position = Position()
        self.angle = None


    def set_position(self, positions):
        self.position = position


    def change_angle(self, new_angle):
        self.angle = new_angle


    def change_strength(self, new_strength):
        self.strength = new_strength


    def modifiy_angle(self, angle_difference):
        self.angle = self.angle + angle_difference


    def modifiy_strength(self, strength_difference):
        self.strength = self.strength + strength_difference


    def execute(self):
        pass


