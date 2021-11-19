from abc import ABC, abstractmethod


class View(ABC):


    @abstractmethod
    def register_model(self):
        return


    @abstractmethod
    def draw(self):
        return


    @abstractmethod
    def update_view(self):
        return

