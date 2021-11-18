from abc import ABC, abstractmethod


class Controller(ABC):


    @abstractmethod
    def register_controller(self):
        return


    @abstractmethod
    def register_model(self):
        return


    @abstractmethod
    def register_view(self):
        return


    @abstractmethod
    def update_view(self):
        return
