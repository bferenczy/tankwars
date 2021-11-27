from abc import ABC, abstractmethod


class IModel(ABC):


    @abstractmethod
    def execute(self):
        pass
