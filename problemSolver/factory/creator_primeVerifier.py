from factory.i_factory import IProblemCreator
from factory.i_problem_solver import IProblemSolver
from factory.primeVerifier import PrimeVerifier

class CreatorPrimeVerifier(IProblemCreator):

    def factory_method(self) -> IProblemSolver:
        return PrimeVerifier()