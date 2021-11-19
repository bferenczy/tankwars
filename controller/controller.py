from abc import ABC, abstractmethod


class Controller(ABC):


    @abstractmethod
    def register_model(self):
        return


    @abstractmethod
    def register_view(self):
        return

