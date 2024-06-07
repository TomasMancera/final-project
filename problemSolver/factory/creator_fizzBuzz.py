from factory.i_factory import IProblemCreator
from factory.i_problem_solver import IProblemSolver
from factory.fizzbuzz import FizzBuzz

class CreatorFizzBuzz(IProblemCreator):

    def factory_method(self) -> IProblemSolver:
        return FizzBuzz()