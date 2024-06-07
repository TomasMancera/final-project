from abc import ABC, abstractmethod

class INumberRandomSolver(ABC):
    
    @abstractmethod
    def get_numbers(self, min, max, cant):
        pass