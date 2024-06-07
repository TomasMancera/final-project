from abc import ABC, abstractmethod
from factory.i_problem_solver import IProblemSolver

class IProblemCreator(ABC):
    
    @abstractmethod
    def factory_method(self) -> IProblemSolver:
        pass

    def compute_results(self, data):
        problem = self.factory_method()
        result = problem.compute_results(data)

        return result