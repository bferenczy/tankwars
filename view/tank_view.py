from .view import View


class TankView(View):


    def __init__(self):
        self.tank_model = None


    def register_model(self, tank_model):
        self.tank_model = tank_model


    def draw(self):
        pass


    def update_view(self):
        self.draw()


