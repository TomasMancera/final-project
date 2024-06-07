from factory.i_factory import IProblemCreator
from factory.i_problem_solver import IProblemSolver
from factory.fibonacci import Fibonnaci

class CreatorFibonacci(IProblemCreator):

    def factory_method(self) -> IProblemSolver:
        return Fibonnaci()